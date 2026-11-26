"""Hook PreToolUse à écrire : protège les migrations déjà existantes.

Entrée : JSON sur stdin (voir knowledge/07-hooks-et-garde-fous.md, section « Entrée et sortie »).
Sortie : code 0 pour autoriser, code 2 et une raison sur stderr pour bloquer.
"""

import json
import sys


def main() -> int:
    entree = json.load(sys.stdin)  # noqa: F841 — à utiliser
    # À compléter.
    return 0


if __name__ == "__main__":
    sys.exit(main())
