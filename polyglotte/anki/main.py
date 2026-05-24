#!/usr/bin/env python3
"""
Génère des fiches Anki DE→FR à partir de fichiers texte, PDF ou images.

Usage :
  python main.py extract <fichier|dossier> [--model gpt-…] [--workers N]
  python main.py lexicon <fichier|dossier> [--model gpt-…] [--workers N]
  python main.py merge   <fichier.json|dossier/> [-o deck.apkg] [-n "Nom"] [--card DE-FR|FR-DE]

Variables d'environnement :
  OPENAI_API_KEY  — clé API OpenAI (chargée depuis .env.local)
"""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import genanki
from dotenv import load_dotenv

# Charge .env.local depuis le dossier du script (priorité sur les variables système)
_ENV_FILE = Path(__file__).parent / ".env.local"
load_dotenv(_ENV_FILE, override=True)

from model import Vocabulary
from process import build_deck, merge_from_folder, process_file, write_csv
from semantic_function import LEXICON_PROMPT, SYSTEM_PROMPT, _SUPPORTED_SUFFIXES


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Génère un deck Anki DE→FR à partir d'un texte ou d'un lexique."
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # ── extract ──────────────────────────────────────────────────────────────
    p_extract = sub.add_parser(
        "extract",
        help="Texte (ou PDF) → extraction OpenAI → lexique .json",
    )
    p_extract.add_argument("input", help="Fichier ou dossier source (.txt, .md, .pdf, …)")
    p_extract.add_argument("--model", default="gpt-5.4-mini", help="Modèle OpenAI (défaut : gpt-5.4-mini)")
    p_extract.add_argument("--workers", type=int, default=4, help="Nombre de threads en mode dossier (défaut : 4)")

    # ── lexicon ───────────────────────────────────────────────────────────────
    p_lex = sub.add_parser(
        "lexicon",
        help="Fichier lexique (PDF, image, …) → extraction de TOUS les mots → lexique .json",
    )
    p_lex.add_argument("input", help="Fichier ou dossier lexique source (.pdf, .png, .md, …)")
    p_lex.add_argument("--model", default="gpt-5.4-mini", help="Modèle OpenAI (défaut : gpt-5.4-mini)")
    p_lex.add_argument("--workers", type=int, default=4, help="Nombre de threads en mode dossier (défaut : 4)")

    # ── merge ─────────────────────────────────────────────────────────────────
    p_merge = sub.add_parser(
        "merge",
        help="Fusionne tous les lexiques JSON d'un dossier en un seul deck .apkg",
    )
    p_merge.add_argument("input", help="Fichier .json ou dossier contenant les fichiers .json")
    p_merge.add_argument("-o", "--output", help="Chemin de base du .apkg fusionné")
    p_merge.add_argument("-n", "--name", default="", help="Nom du deck Anki")
    p_merge.add_argument(
        "--card",
        choices=["DE-FR", "FR-DE"],
        default=None,
        help="Limiter à un seul sens de carte (par défaut : les deux)",
    )

    args = parser.parse_args()

    if args.mode == "merge":
        input_path = Path(args.input)
        if input_path.is_file() and input_path.suffix == ".json":
            deck_name = args.name or input_path.stem
            base = Path(args.output).with_suffix("") if args.output else input_path.parent / deck_name
            vocab = Vocabulary.model_validate_json(input_path.read_text(encoding="utf-8"))
        elif input_path.is_dir():
            deck_name = args.name or input_path.name
            base = Path(args.output).with_suffix("") if args.output else input_path / deck_name
            print(f"Fusion des lexiques dans {input_path}…")
            vocab = merge_from_folder(input_path)
        else:
            sys.exit(f"Introuvable ou format non supporté : {input_path}")

        csv_path = base.with_suffix(".csv")
        light_path = Path(f"{base}-light.apkg")
        dark_path = Path(f"{base}-dark.apkg")

        for theme, out_path in [("light", light_path), ("dark", dark_path)]:
            deck = build_deck(vocab, deck_name, include_notes=False, card_filter=args.card, theme=theme)
            genanki.Package(deck).write_to_file(str(out_path))
            print(f"Deck {theme:<5} : {out_path}")

        write_csv(vocab, csv_path)
        print(f"CSV          : {csv_path}")
        return

    # ── extract / lexicon ─────────────────────────────────────────────────────
    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"Introuvable : {input_path}")

    is_dir = input_path.is_dir()
    if is_dir:
        files = [
            f for f in sorted(input_path.iterdir())
            if f.is_file() and f.suffix.lower() in _SUPPORTED_SUFFIXES
        ]
        if not files:
            sys.exit(
                f"Aucun fichier supporté (.pdf, .png, .jpg, .jpeg, .gif, .webp, .txt, .md) dans : {input_path}"
            )
    else:
        if input_path.suffix.lower() not in _SUPPORTED_SUFFIXES:
            sys.exit(
                f"Format non supporté : {input_path.suffix!r}. "
                "Formats acceptés : .pdf, .png, .jpg, .jpeg, .gif, .webp, .txt, .md"
            )
        files = [input_path]

    system_prompt = LEXICON_PROMPT if args.mode == "lexicon" else SYSTEM_PROMPT

    if is_dir:
        print(f"Traitement de {len(files)} fichier(s) avec {args.workers} thread(s)…")
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(process_file, f, is_dir, args.model, system_prompt): f for f in files}
            for future in as_completed(futures):
                exc = future.exception()
                if exc:
                    print(f"  ✗ Erreur inattendue ({futures[future].name}) : {exc}")
    else:
        process_file(files[0], is_dir, args.model, system_prompt)


if __name__ == "__main__":
    main()
