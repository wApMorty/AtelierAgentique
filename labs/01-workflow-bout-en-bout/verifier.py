"""Vérifie les critères de réussite du lab 01 sur le dépôt de l'apprenant.

Usage : python labs/01-workflow-bout-en-bout/verifier.py <chemin du dépôt de l'apprenant>
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
CONVENTIONAL = re.compile(r"^(feat|fix|refactor|test|docs|chore)(\([\w-]+\))?!?: .+")


def lancer(commande: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(commande, cwd=cwd, capture_output=True, text=True)


def criteres(depot: Path) -> list[tuple[str, bool, str]]:
    spec, plan, revue = (depot / "specs" / "codes-promo" / f for f in ("spec.md", "plan.md", "revue.md"))
    texte_spec = spec.read_text(encoding="utf-8") if spec.is_file() else ""
    texte_plan = plan.read_text(encoding="utf-8") if plan.is_file() else ""
    nb_ca = len(re.findall(r"^- \[[ x]\] CA\d+", texte_spec, re.MULTILINE))
    sections = all(s in texte_spec for s in ("## Objectif", "## Hors périmètre", "## Critères d'acceptation"))
    taches = re.findall(r"^- \[([ x])\] T\d+", texte_plan, re.MULTILINE)
    log = lancer(["git", "log", "--format=%s", "depart..HEAD"], depot).stdout.split("\n")
    commits = [m for m in log if m]
    tests = lancer([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], depot)
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(depot / "panier.py", d)
        shutil.copy(ICI / "solution" / "test_acceptation.py", d)
        acceptation = lancer([sys.executable, "-m", "unittest", "test_acceptation"], Path(d))
    return [
        ("Spec avec les trois sections et au moins trois critères", sections and nb_ca >= 3, f"{nb_ca} critère(s)"),
        ("Plan avec au moins deux tâches, toutes cochées", len(taches) >= 2 and all(t == "x" for t in taches), f"{len(taches)} tâche(s)"),
        ("Au moins deux commits Conventional Commits depuis l'étiquette « depart »", len(commits) >= 2 and all(CONVENTIONAL.match(c) for c in commits), f"{len(commits)} commit(s)"),
        ("Tests de l'apprenant verts", tests.returncode == 0, tests.stderr.strip().splitlines()[-1] if tests.stderr.strip() else ""),
        ("Tests d'acceptation verts", acceptation.returncode == 0, acceptation.stderr.strip().splitlines()[-1] if acceptation.stderr.strip() else ""),
        ("Rapport de revue indépendante présent", revue.is_file() and "verdict" in revue.read_text(encoding="utf-8").lower(), ""),
    ]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    resultats = criteres(Path(sys.argv[1]).resolve())
    for libelle, ok, detail in resultats:
        print(f"{'OK ' if ok else 'KO '} {libelle}" + (f" — {detail}" if detail else ""))
    return 0 if all(ok for _, ok, _ in resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
