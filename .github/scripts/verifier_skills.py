"""Vérifie que les skills du dépôt respectent le format Agent Skills et les extensions admises (ADR-003).

Usage : python .github/scripts/verifier_skills.py
Code de sortie 1 si un SKILL.md est non conforme.
"""

import re
import sys
from pathlib import Path

STANDARD = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
EXTENSIONS_ADMISES = {"disable-model-invocation"}  # propriété de sécurité, voir ADR-003
NOM = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def erreurs(skill: Path) -> list[str]:
    texte = skill.read_text(encoding="utf-8")
    bloc = re.match(r"^---\n(.*?)\n---\n", texte, re.DOTALL)
    if not bloc:
        return ["frontmatter YAML absent"]
    champs = dict(re.findall(r"^([A-Za-z][\w-]*):\s*(.*)$", bloc.group(1), re.MULTILINE))
    resultat = [f"champ non admis : {c}" for c in champs if c not in STANDARD | EXTENSIONS_ADMISES]
    nom, description = champs.get("name", ""), champs.get("description", "")
    if not NOM.match(nom) or len(nom) > 64:
        resultat.append(f"name invalide : {nom!r}")
    if nom != skill.parent.name:
        resultat.append(f"name ({nom}) différent du répertoire ({skill.parent.name})")
    if not 1 <= len(description) <= 1024:
        resultat.append(f"description de {len(description)} caractères (1 à 1024)")
    return resultat


def main() -> int:
    skills = sorted(Path(".").glob("plugins/*/skills/*/SKILL.md")) + sorted(Path(".").glob(".claude/skills/*/SKILL.md"))
    echecs = {s: e for s in skills if (e := erreurs(s))}
    for skill, liste in echecs.items():
        for e in liste:
            print(f"{skill}: {e}")
    print(f"{len(skills)} skills vérifiés, {len(echecs)} non conformes.")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
