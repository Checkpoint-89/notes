#!/usr/bin/env python3
"""
Point d'entrée de compatibilité. Le code est désormais organisé en modules :
  model.py, monitoring.py, template.py, semantic_function.py, process.py, main.py

Usage :
  python anki.py extract <fichier|dossier> [--model gpt-…]
  python anki.py lexicon <fichier|dossier> [--model gpt-…]
  python anki.py merge   <fichier.json|dossier/> [-o deck.apkg] [-n "Nom"]
"""
# ── Fin du fichier (tout le code est dans main.py et ses dépendances) ────────

from main import main

if __name__ == "__main__":
    main()
