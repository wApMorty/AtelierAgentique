"""Hook PreToolUse (Bash, PowerShell) : bloque les commandes destructrices ou irréversibles.

Chapitre de référence : knowledge/07-hooks-et-garde-fous.md.
Code de sortie 2 = blocage ; la raison, sur stderr, est transmise à l'agent.

ponytail: filtrage par motifs sur le texte de la commande, contournable (sh -c, script, alias).
Il réduit les accidents, pas les attaques : la vraie barrière est le bac à sable (knowledge/10-securite.md).
"""

import json
import re
import sys

# Suppression récursive forcée (-rf, -fr, -Rf, -r -f, --recursive --force) visant une cible
# dangereuse : racine, dossier personnel, joker, parent, chemin absolu (Unix ou lecteur Windows).
_RM = (
    r"\brm\b(?=[^|;&]*(?:\s-(?!-)[a-zA-Z]*[rR]|\s--recursive))(?=[^|;&]*(?:\s-(?!-)[a-zA-Z]*f|\s--force))"
    r"[^|;&]*?\s[\"']?(?:/|~|\$HOME|\*|\.(?:\s|$)|\.\.(?:/|\s|$)|[A-Za-z]:[\\/])"
)
# Sous-commande git, avec d'éventuelles options globales (-C chemin, -c clé=valeur) ; [^;|&]* borne à la commande.
_GIT = r"\bgit(?:\s+-[Cc]\s+\S+)*\s+"

MOTIFS = [
    (_RM, "suppression récursive forcée hors du projet"),
    (r"\bRemove-Item\b(?=[^;|&]*-Recurse)(?=[^;|&]*-Force)[^;|&]*(?:\s[\"']?[A-Za-z]:[\\/]?|\s[\"']?[\\/]|\s~|\$HOME|\$env:USERPROFILE)", "suppression récursive forcée hors du projet"),
    (_GIT + r"push\b[^;|&]*(?:\s--force(?:-with-lease)?\b|\s-f\b|\s\+\S+)", "push forcé (réécriture de l'historique distant)"),
    (_GIT + r"reset\b[^;|&]*\s--hard\b", "git reset --hard (perte des modifications non commitées)"),
    (_GIT + r"clean\b[^;|&]*\s(?:-(?!-)[a-zA-Z]*f|--force)", "git clean forcé (suppression des fichiers non suivis)"),
    (_GIT + r"(?:commit|push|merge|rebase)\b[^;|&]*\s--no-verify\b", "contournement des hooks git (--no-verify)"),
    (
        r"\b(?:curl|wget|iwr|Invoke-WebRequest)\b[^|]*\|\s*(?:sudo\s+)?"
        r"(?:(?:sh|bash|zsh|iex|Invoke-Expression)\b|python3?(?:\s*$|\s+-\s*$|\s+-c\b|\s*[;&|]))",
        "téléchargement et exécution de code",
    ),
    (r"\bmkfs(?:\.\w+)?\b|\bdd\b[^;|&]*\bof=/dev/(?!null\b)", "écriture directe sur un périphérique"),
    (r"verifier_fin(?:\.py)?\b[^;|&]*--approuver", "approbation de la vérification de fin réservée à l'utilisateur"),
]

# Motifs évalués sur la commande privée de ses chaînes entre guillemets, pour ne pas confondre
# une option avec le texte d'un message de commit.
MOTIFS_HORS_GUILLEMETS = [
    (_GIT + r"commit\b[^;|&]*\s-(?!-)[a-zA-Z]*n", "contournement des hooks git (git commit -n)"),
]


def raison(commande: str) -> str | None:
    """Renvoie la raison du blocage, ou None si la commande est autorisée."""
    for motif, motif_raison in MOTIFS:
        if re.search(motif, commande, re.IGNORECASE | re.DOTALL):
            return motif_raison
    sans_guillemets = re.sub(r"'[^']*'|\"[^\"]*\"", "''", commande)
    for motif, motif_raison in MOTIFS_HORS_GUILLEMETS:
        if re.search(motif, sans_guillemets, re.DOTALL):
            return motif_raison
    return None


def main() -> int:
    entree = json.load(sys.stdin)
    commande = (entree.get("tool_input") or {}).get("command", "")
    motif_raison = raison(commande)
    if motif_raison is None:
        return 0
    print(
        f"Commande bloquée par le plugin garde-fous : {motif_raison}.\n"
        "Si cette opération est réellement nécessaire, explique pourquoi à l'utilisateur "
        "et laisse-le l'exécuter lui-même.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
