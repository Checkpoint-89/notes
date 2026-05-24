import json
import threading
from pathlib import Path

_LOG_FILE = Path(__file__).parent / "anki_calls.jsonl"
_LOG_LOCK = threading.Lock()


def append_log(entry: dict) -> None:
    """Ajoute une entrée JSON dans le fichier de log (anki_calls.jsonl)."""
    with _LOG_LOCK, _LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
