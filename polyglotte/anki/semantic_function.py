import base64
import mimetypes
from pathlib import Path

import instructor
import openai
from pydantic import model_validator

from model import VocabEntry, Vocabulary

_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
_SUPPORTED_SUFFIXES = _IMAGE_SUFFIXES | {".pdf", ".txt", ".md"}

SYSTEM_PROMPT = """\
Tu es un lexicographe germaniste. À partir du texte fourni, extrais tous les \
mots de vocabulaire intéressants (noms, verbes forts/irréguliers, adjectifs \
utiles, expressions figées) en respectant les conventions dictionnaires classiques.
"""

LEXICON_PROMPT = """\
Tu es un lexicographe germaniste. Le document fourni est déjà un lexique ou \
un lexique de vocabulaire allemand. Extrais-en TOUS les mots sans exception, \
en respectant les conventions dictionnaires classiques pour chaque entrée :\
noms avec article défini et pluriel abrégé, verbes avec prétérit et auxiliaire \
si ≠ haben, adjectifs/adverbes en forme de base. \
Pour chaque mot, extrais également TOUS les exemples présents dans le document \
(phrases allemandes avec leur traduction française). \
"""

REVIEW_PROMPT = """\
Tu es un correcteur expert en allemand et en français. \
On te donne une fiche de vocabulaire DE→FR. Vérifie et corrige si nécessaire :
1. Le mot allemand suit les conventions dictionnaire \
   (article + pluriel pour les noms, prétérit pour les verbes forts, etc.).
2. La phrase exemple allemande est grammaticalement correcte \
   et illustre bien le mot.
3. La traduction française est juste et naturelle.
4. La traduction française de l'exemple est fidèle et correcte.
Retourne la fiche corrigée (identique si aucune erreur).
"""


def sf_build_messages(path: Path, system_prompt: str = SYSTEM_PROMPT) -> list[dict]:
    """Construit les messages OpenAI en envoyant le fichier brut (base64).
    GPT gère le parsing — aucune bibliothèque locale requise."""
    suffix = path.suffix.lower()
    mime, _ = mimetypes.guess_type(path.name)

    if suffix in _IMAGE_SUFFIXES:
        data = base64.b64encode(path.read_bytes()).decode()
        file_content = {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{data}"},
        }
    elif suffix != ".txt" and suffix != ".md":
        # PDF ou tout autre binaire : content type "file"
        data = base64.b64encode(path.read_bytes()).decode()
        file_content = {
            "type": "file",
            "file": {
                "filename": path.name,
                "file_data": f"data:{mime or 'application/octet-stream'};base64,{data}",
            },
        }
    else:
        # Texte brut (markdown, txt)
        file_content = {
            "type": "text",
            "text": path.read_text(encoding="utf-8"),
        }

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [file_content]},
    ]


def sf_extract_vocabulary(
    path: Path,
    model: str = "gpt-5.4-mini",
    system_prompt: str = SYSTEM_PROMPT,
) -> Vocabulary:
    client = instructor.from_openai(openai.OpenAI())
    return client.chat.completions.create(
        model=model,
        response_model=Vocabulary,
        messages=sf_build_messages(path, system_prompt=system_prompt),
        temperature=0.2,
    )


def _make_review_model(original: VocabEntry) -> type[VocabEntry]:
    """Sous-type de VocabEntry qui restaure automatiquement page
    si le LLM de review la modifie (ce champ est une métadonnée source)."""
    _page = original.page

    class _ReviewedEntry(VocabEntry):
        @model_validator(mode="after")
        def _restore_metadata(self) -> "_ReviewedEntry":
            self.page = _page
            return self

    return _ReviewedEntry


def sf_review_entry(entry: VocabEntry, model: str = "gpt-5.4-mini") -> VocabEntry:
    client = instructor.from_openai(openai.OpenAI())
    return client.chat.completions.create(
        model=model,
        response_model=_make_review_model(entry),
        messages=[
            {"role": "system", "content": REVIEW_PROMPT},
            {"role": "user", "content": entry.model_dump_json(indent=2)},
        ],
        temperature=0.1,
    )
