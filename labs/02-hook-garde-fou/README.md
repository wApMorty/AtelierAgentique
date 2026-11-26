# Lab 02 — Écriture d'un hook de garde-fou

Chapitre lié : [07 — Hooks et garde-fous](../../knowledge/07-hooks-et-garde-fous.md). Composant de référence : plugin [`garde-fous`](../../plugins/garde-fous/).

## Objectif

Transformer une règle d'équipe que l'on confierait d'ordinaire à une instruction (« ne jamais modifier une migration déjà écrite ») en hook déterministe, testé hors de l'agent, puis branché dans Claude Code.

## Prérequis

- Python 3.10 ou plus récent ;
- avoir lu les sections « Configuration », « Entrée et sortie » et « Limites à connaître » du chapitre 07.

## Énoncé

1. Compléter [`depart/hook.py`](depart/hook.py) : un hook `PreToolUse` qui **bloque** toute écriture (`Write`, `Edit`, `MultiEdit`) sur un fichier **existant** du répertoire `migrations/` à la racine du projet, et **autorise** la création d'une nouvelle migration comme tout autre fichier.
2. Le blocage renvoie le code 2 et, sur stderr, une raison qui dit à l'agent quoi faire à la place.
3. Le chemin reçu peut être absolu ou relatif au projet ; un fichier dont le nom contient seulement « migrations » ne doit pas être bloqué.
4. Brancher le hook dans un projet de test, via `.claude/settings.json` :

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit|MultiEdit",
           "hooks": [{ "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/hook.py\"", "onFailure": "block" }]
         }
       ]
     }
   }
   ```

5. Demander à Claude Code de corriger une faute dans une migration existante et observer sa réaction au blocage.

## Critères de réussite

```sh
python -m unittest discover -s labs/02-hook-garde-fou/tests
```

Six tests, tous verts : blocage par outil, chemin relatif, nouvelle migration autorisée, reste du projet autorisé, nom voisin non bloqué, message utile. Ils échouent sur le fichier de départ.

Critère observé à la main : dans Claude Code, l'agent reçoit le message et propose une nouvelle migration au lieu de contourner.

## Questions de réflexion

- Pourquoi `onFailure: "block"` ? Que se passe-t-il si Python est absent ?
- Ce hook arrête-t-il `sed -i` lancé par Bash sur une migration ? Quelle couche le ferait ([chapitre 10](../../knowledge/10-securite.md)) ?
- Que gagne-t-on à tester le hook hors de l'agent ?

## Solution indicative

[`solution/hook.py`](solution/hook.py), vérifiable par :

```sh
LAB02_HOOK=labs/02-hook-garde-fou/solution/hook.py python -m unittest discover -s labs/02-hook-garde-fou/tests
```
