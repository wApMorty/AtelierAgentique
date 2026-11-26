#!/usr/bin/env bash
# Lance un script Python du plugin avec l'interpréteur disponible.
# Sous Windows, « python3 » peut être l'alias du Microsoft Store, qui échoue : on le teste avant de l'utiliser.
if python3 -c "" >/dev/null 2>&1; then P=python3; else P=python; fi
exec "$P" "$(dirname "$0")/$1.py" "${@:2}"
