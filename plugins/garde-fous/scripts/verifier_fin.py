"""Hook Stop : exécute la commande de vérification du projet avant que l'agent ne s'arrête.

Chapitre de référence : knowledge/07-hooks-et-garde-fous.md et knowledge/09-verification-et-evaluation.md.

La commande est lue dans .garde-fous.json à la racine du projet : {"verification": "npm test"}.
Sans ce fichier, le hook ne fait rien. En cas d'échec, code 2 : l'agent ne peut pas s'arrêter
et reçoit la fin de la sortie (Claude Code lève le blocage après plusieurs refus consécutifs).

Sécurité : la commande vient du dépôt. Pour qu'un dépôt cloné n'exécute rien à l'insu de
l'utilisateur, le couple (projet, commande) doit avoir été approuvé une fois :
    python verifier_fin.py --approuver      (depuis la racine du projet)
Toute modification de la commande exige une nouvelle approbation.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

CONFIG = ".garde-fous.json"


def fichier_approbations() -> Path:
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or Path.home() / ".garde-fous"
    return Path(base) / "approbations.tsv"


def commande_du_projet(projet: Path) -> str | None:
    chemin = projet / CONFIG
    if not chemin.is_file():
        return None
    return (json.loads(chemin.read_text(encoding="utf-8")).get("verification") or "").strip() or None


def _ligne(projet: Path, commande: str) -> str:
    return f"{projet.resolve()}\t{commande}"


def est_approuvee(projet: Path, commande: str) -> bool:
    fichier = fichier_approbations()
    return fichier.is_file() and _ligne(projet, commande) in fichier.read_text(encoding="utf-8").splitlines()


def approuver(projet: Path) -> int:
    commande = commande_du_projet(projet)
    if commande is None:
        print(f"Aucune commande de vérification dans {projet / CONFIG}.", file=sys.stderr)
        return 1
    fichier = fichier_approbations()
    fichier.parent.mkdir(parents=True, exist_ok=True)
    with fichier.open("a", encoding="utf-8") as f:
        f.write(_ligne(projet, commande) + "\n")
    print(f"Approuvé pour {projet.resolve()} : {commande}")
    return 0


def main() -> int:
    if "--approuver" in sys.argv:
        return approuver(Path.cwd())
    entree = json.load(sys.stdin)
    projet = Path(os.environ.get("CLAUDE_PROJECT_DIR") or entree.get("cwd") or ".")
    commande = commande_du_projet(projet)
    if commande is None:
        return 0
    if not est_approuvee(projet, commande):
        message = (
            f"garde-fous : vérification de fin non exécutée, commande « {commande} » non approuvée "
            f"pour ce projet. Pour l'approuver, lancer depuis la racine du projet : "
            f"python <plugin>/scripts/verifier_fin.py --approuver (fichier : {fichier_approbations()})."
        )
        print(json.dumps({"systemMessage": message}, ensure_ascii=False))
        return 0
    resultat = subprocess.run(commande, shell=True, cwd=projet, capture_output=True, text=True, timeout=280)
    if resultat.returncode == 0:
        return 0
    sortie = (resultat.stdout + resultat.stderr).strip()[-3000:]
    print(
        f"La vérification du projet échoue (`{commande}`, code {resultat.returncode}). "
        f"Corrige avant de conclure, ou explique à l'utilisateur pourquoi l'échec est hors périmètre.\n{sortie}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
