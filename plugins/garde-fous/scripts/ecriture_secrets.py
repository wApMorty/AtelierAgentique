"""Hook PreToolUse (Write, Edit, MultiEdit) : refuse d'écrire un secret ou un fichier de secrets.

Chapitre de référence : knowledge/10-securite.md (section « Secrets »).
Code de sortie 2 = blocage ; la raison, sur stderr, est transmise à l'agent.

ponytail: détection par motifs de formats connus ; un secret au format libre passe.
Compléter par une règle permissions.deny sur la lecture des fichiers de secrets (voir README).
"""

import json
import re
import sys
from pathlib import PurePath

FICHIERS = re.compile(
    r"^(?:\.env(?:\.(?!example$|sample$|template$|exemple$)[\w.-]+)?|\.envrc|\.netrc|.*\.(?:pem|key|p12|pfx)|"
    r"id_(?:rsa|ecdsa|ed25519)(?:\.\w+)?|\.npmrc|\.pypirc|credentials(?:\.json)?)$",
    re.IGNORECASE,
)

SECRETS = [
    (r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY", "clé privée"),
    (r"\bAKIA[0-9A-Z]{16}\b", "clé d'accès AWS"),
    (r"\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b", "jeton GitHub"),
    (r"\bsk-ant-[A-Za-z0-9_-]{20,}", "clé d'API Anthropic"),
    (r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}", "clé d'API de type sk-"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}", "jeton Slack"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "clé d'API Google"),
    (r"https://discord(?:app)?\.com/api/webhooks/\d+/[\w-]+", "webhook Discord"),
]


def _textes_ecrits(tool_input: dict):
    """Le texte qui sera écrit (Write : content ; Edit : new_string ; MultiEdit : edits[*].new_string).
    Le texte remplacé (old_string) n'est pas analysé : retirer une clé fuitée doit rester possible."""
    for cle in ("content", "new_string"):
        if isinstance(tool_input.get(cle), str):
            yield tool_input[cle]
    for edition in tool_input.get("edits") or []:
        if isinstance(edition, dict) and isinstance(edition.get("new_string"), str):
            yield edition["new_string"]


def raison(tool_input: dict) -> str | None:
    chemin = tool_input.get("file_path") or ""
    if chemin and FICHIERS.match(PurePath(chemin.replace("\\", "/")).name):
        return f"écriture dans un fichier de secrets ({PurePath(chemin).name})"
    for texte in _textes_ecrits(tool_input):
        for motif, nature in SECRETS:
            if re.search(motif, texte):
                return f"le contenu ressemble à un secret ({nature})"
    return None


def main() -> int:
    entree = json.load(sys.stdin)
    motif_raison = raison(entree.get("tool_input") or {})
    if motif_raison is None:
        return 0
    print(
        f"Écriture bloquée par le plugin garde-fous : {motif_raison}.\n"
        "Utilise une variable d'environnement ou un gestionnaire de secrets, "
        "et un fichier d'exemple sans valeur réelle (.env.example).",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
