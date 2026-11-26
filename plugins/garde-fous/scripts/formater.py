"""Hook PostToolUse (Write, Edit, MultiEdit) : formate le fichier modifié et signale les erreurs de lint.

Chapitre de référence : knowledge/07-hooks-et-garde-fous.md.
N'utilise que des outils déjà installés : ruff (PATH) pour Python, prettier et eslint locaux
au projet (node_modules/.bin) pour TypeScript et JavaScript. Rien n'est téléchargé.
Un outil absent est ignoré. Une erreur de lint renvoie le code 2 : la sortie est montrée à l'agent.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

WEB = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".css", ".scss", ".html"}
LINT_WEB = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}


def _local(projet: Path, outil: str) -> str | None:
    return shutil.which(outil, path=str(projet / "node_modules" / ".bin"))


def _lancer(commande: list[str], projet: Path) -> subprocess.CompletedProcess:
    return subprocess.run(commande, cwd=projet, capture_output=True, text=True, timeout=60)


def commandes(fichier: Path, projet: Path) -> tuple[list[list[str]], list[list[str]]]:
    """Renvoie (commandes de formatage, commandes de lint) applicables au fichier."""
    ext = fichier.suffix.lower()
    formatage, lint = [], []
    if ext == ".py" and (ruff := shutil.which("ruff")):
        formatage.append([ruff, "format", "--quiet", str(fichier)])
        lint.append([ruff, "check", "--quiet", str(fichier)])
    if ext in WEB and (prettier := _local(projet, "prettier")):
        formatage.append([prettier, "--write", "--log-level", "warn", str(fichier)])
    if ext in LINT_WEB and (eslint := _local(projet, "eslint")):
        lint.append([eslint, str(fichier)])
    return formatage, lint


def main() -> int:
    entree = json.load(sys.stdin)
    chemin = (entree.get("tool_input") or {}).get("file_path")
    if not chemin or not Path(chemin).is_file():
        return 0
    projet = Path(os.environ.get("CLAUDE_PROJECT_DIR") or entree.get("cwd") or ".")
    formatage, lint = commandes(Path(chemin), projet)
    for commande in formatage:
        _lancer(commande, projet)
    erreurs = []
    for commande in lint:
        resultat = _lancer(commande, projet)
        if resultat.returncode != 0:
            erreurs.append((resultat.stdout + resultat.stderr).strip()[-3000:])
    if erreurs:
        print("Erreurs de lint après modification :\n" + "\n".join(erreurs), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
