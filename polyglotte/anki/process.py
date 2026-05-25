import csv
import datetime
import hashlib
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import genanki

from model import VocabEntry, Vocabulary
from monitoring import append_log
from semantic_function import sf_extract_vocabulary, sf_review_entry
from template import (
    BACK_TEMPLATE_DE_FR,
    BACK_TEMPLATE_FR_DE,
    CSS_DARK,
    CSS_LIGHT,
    FRONT_TEMPLATE_DE_FR,
    FRONT_TEMPLATE_FR_DE,
)


def write_csv(vocab: Vocabulary, path: Path) -> None:
    """Exporte les fiches en CSV (une ligne par exemple, ou une ligne sans exemple)."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Mot DE", "Exemple DE", "Traduction FR", "Exemple FR", "Page", "Categorie"])
        for entry in vocab.mots:
            if entry.exemples:
                for ex in entry.exemples:
                    writer.writerow([
                        entry.id,
                        entry.mot_de, ex.de, entry.traduction_fr, ex.fr,
                        entry.page if entry.page is not None else "",
                        entry.categorie,
                    ])
            else:
                writer.writerow([
                    entry.id,
                    entry.mot_de, "", entry.traduction_fr, "",
                    entry.page if entry.page is not None else "",
                    entry.categorie,
                ])


def merge_from_folder(folder: Path) -> Vocabulary:
    """Fusionne tous les lexiques JSON d'un dossier.
    Les doublons (même mot_de) sont dédupliqués en gardant la première occurrence.
    """
    json_files = sorted(folder.glob("*.json"))
    if not json_files:
        sys.exit(f"Aucun fichier .json trouvé dans : {folder}")

    seen: set[str] = set()
    all_entries: list[VocabEntry] = []
    for jf in json_files:
        vocab = Vocabulary.model_validate_json(jf.read_text(encoding="utf-8"))
        for entry in vocab.mots:
            key = entry.mot_de.strip().lower()
            if key not in seen:
                seen.add(key)
                all_entries.append(entry)
        print(f"  {jf.name} → {len(vocab.mots)} mots")

    return Vocabulary(mots=all_entries)


def build_deck(
    vocab: Vocabulary,
    deck_name: str,
    include_notes: bool = True,
    card_filter: str | None = None,
    theme: str = "light",
) -> genanki.Deck:
    # IDs stables dérivés du nom du deck (reproductibles)
    rng = random.Random(f"{deck_name}-{theme}")
    deck_id = rng.randint(1 << 30, 1 << 31)
    model_id = rng.randint(1 << 30, 1 << 31)

    all_templates = [
        {"name": "DE-FR", "qfmt": FRONT_TEMPLATE_DE_FR, "afmt": BACK_TEMPLATE_DE_FR},
        {"name": "FR-DE", "qfmt": FRONT_TEMPLATE_FR_DE, "afmt": BACK_TEMPLATE_FR_DE},
    ]
    templates = [t for t in all_templates if card_filter is None or t["name"] == card_filter]

    anki_model = genanki.Model(
        model_id,
        "Vocabulaire DE/FR",
        fields=[
            {"name": "ID"},
            {"name": "Mot DE"},
            {"name": "Exemple DE"},
            {"name": "Traduction FR"},
            {"name": "Exemple FR"},
            {"name": "page"},
            {"name": "categorie"},
        ],
        templates=templates,
        css=CSS_DARK if theme == "dark" else CSS_LIGHT,
    )

    deck = genanki.Deck(deck_id, deck_name)
    if include_notes:
        for entry in vocab.mots:
            if entry.exemples:
                for ex in entry.exemples:
                    guid = hashlib.md5(f"{entry.id}{ex.de}".encode()).hexdigest()[:10]
                    note = genanki.Note(
                        model=anki_model,
                        fields=[
                            entry.id, entry.mot_de, ex.de, entry.traduction_fr, ex.fr,
                            str(entry.page) if entry.page is not None else "",
                            entry.categorie if entry.categorie is not None else "",
                        ],
                        guid=guid,
                    )
                    deck.add_note(note)
            else:
                note = genanki.Note(
                    model=anki_model,
                    fields=[
                        entry.id, entry.mot_de, "", entry.traduction_fr, "",
                        str(entry.page) if entry.page is not None else "",
                        entry.categorie if entry.categorie is not None else "",
                    ],
                    guid=entry.id,
                )
                deck.add_note(note)
    else:
        # Note fictive pour forcer l'inclusion du modèle dans le .apkg.
        # À supprimer dans Anki après import du CSV.
        deck.add_note(genanki.Note(
            model=anki_model,
            fields=["EXEMPLE", "[EXEMPLE — à supprimer]", "", "[exemple]", "", "", ""],
            guid="__template_placeholder__",
        ))

    return deck


def process_file(file: Path, is_dir: bool, model: str, system_prompt: str) -> None:
    if is_dir:
        print(f"\n── {file.name} ──")

    ts = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

    print(f"  [{file.name}] Extraction avec {model}…")
    append_log({"event": "extract_start", "file": str(file), "model": model, "ts": ts()})
    t0 = time.monotonic()
    try:
        vocab = sf_extract_vocabulary(file, model=model, system_prompt=system_prompt)
    except Exception as exc:
        print(f"  [{file.name}] ✗ Erreur extraction : {exc}")
        append_log({"event": "extract_error", "file": str(file), "model": model, "ts": ts(), "error": str(exc)})
        return
    print(f"  [{file.name}] → {len(vocab.mots)} mots extraits")
    append_log({
        "event": "extract_end", "file": str(file), "model": model, "ts": ts(),
        "duration_s": round(time.monotonic() - t0, 2), "n_entries": len(vocab.mots),
        "vocab": json.loads(vocab.model_dump_json()),
    })

    print(f"  [{file.name}] Vérification de {len(vocab.mots)} entrée(s) en parallèle…")
    append_log({"event": "review_start", "file": str(file), "model": model, "ts": ts(),
                "n_entries": len(vocab.mots)})
    t0 = time.monotonic()
    reviewed: list[VocabEntry] = list(vocab.mots)
    with ThreadPoolExecutor(max_workers=min(len(vocab.mots), 8)) as review_pool:
        future_to_idx = {review_pool.submit(sf_review_entry, entry, model): i
                         for i, entry in enumerate(vocab.mots)}
        for future in as_completed(future_to_idx):
            i = future_to_idx[future]
            try:
                reviewed[i] = future.result()
            except Exception as exc:
                print(f"  [{file.name}] ⚠ Review échoué pour '{vocab.mots[i].mot_de}' : {exc}")
    vocab = Vocabulary(mots=reviewed)
    print(f"  [{file.name}] ✓ Vérification terminée ({len(vocab.mots)} entrées)")
    append_log({
        "event": "review_end", "file": str(file), "model": model, "ts": ts(),
        "duration_s": round(time.monotonic() - t0, 2), "n_entries": len(vocab.mots),
        "vocab": json.loads(vocab.model_dump_json()),
    })

    lex_path = file.with_suffix(".json")
    lex_path.write_text(vocab.model_dump_json(indent=2), encoding="utf-8")
    print(f"  [{file.name}] Lexique sauvegardé : {lex_path}")
