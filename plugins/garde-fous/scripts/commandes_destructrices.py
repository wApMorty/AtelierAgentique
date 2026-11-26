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
    r"\brm\b(?=[^|;&]*(?:\s-\S*r|\s--recursive))(?=[^|;&]*(?:\s-\S*f|\s--force))"
    r"[^|;&]*?\s[\"']?(?:/|~|\$HOME|\*|\.(?:\s|$)|\.\.(?:/|\s|$)|[A-Za-z]:[\\/])"
)

MOTIFS = [
    (_RM, "suppression récursive forcée hors du projet"),
    (r"\bRemove-Item\b(?=.*-Recurse)(?=.*-Force).*(?:\s[\"']?[A-Za-z]:[\\/]?|\s[\"']?[\\/]|\s~|\$HOME|\$env:USERPROFILE)", "suppression récursive forcée hors du projet"),
    (r"\bgit\s+push\b.*(?:\s--force(?:-with-lease)?\b|\s-f\b|\s\+\S+)", "push forcé (réécriture de l'historique distant)"),
    (r"\bgit\s+reset\s+.*--hard\b|\bgit\s+reset\s+--hard\b", "git reset --hard (perte des modifications non commitées)"),
    (r"\bgit\s+clean\s+(?:-\S*f|--force)", "git clean forcé (suppression des fichiers non suivis)"),
    (r"\bgit\s+(?:commit|push|merge|rebase)\b.*\s--no-verify\b", "contournement des hooks git (--no-verify)"),
    (r"\b(?:curl|wget|iwr|Invoke-WebRequest)\b[^|]*\|\s*(?:sudo\s+)?(?:sh|bash|zsh|python3?|iex|Invoke-Expression)\b", "téléchargement et exécution de code"),
    (r"\bmkfs(?:\.\w+)?\b|\bdd\b.*\bof=/dev/", "écriture directe sur un périphérique"),
]


def raison(commande: str) -> str | None:
    """Renvoie la raison du blocage, ou None si la commande est autorisée."""
    for motif, motif_raison in MOTIFS:
        if re.search(motif, commande, re.IGNORECASE | re.DOTALL):
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
