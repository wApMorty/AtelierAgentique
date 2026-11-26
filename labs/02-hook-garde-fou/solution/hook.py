"""Solution indicative du lab 02 : une migration déjà écrite ne se modifie pas, on en crée une nouvelle."""

import json
import os
import sys
from pathlib import Path


def main() -> int:
    entree = json.load(sys.stdin)
    chemin = (entree.get("tool_input") or {}).get("file_path")
    if not chemin:
        return 0
    projet = Path(os.environ.get("CLAUDE_PROJECT_DIR") or entree.get("cwd") or ".").resolve()
    fichier = (projet / chemin).resolve()  # un chemin absolu remplace la base
    try:
        relatif = fichier.relative_to(projet)
    except ValueError:
        return 0
    if relatif.parts[:1] == ("migrations",) and fichier.exists():
        print(
            f"Modification refusée : {relatif.as_posix()} est une migration existante, potentiellement déjà appliquée. "
            "Crée une nouvelle migration qui corrige la précédente.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
