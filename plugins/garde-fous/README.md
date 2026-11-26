# Plugin `garde-fous`

Hooks de garde-fous et de qualité : ce qui ne souffre pas d'exception est imposé par du code, pas demandé par une instruction.

Chapitres de référence : [07 — Hooks et garde-fous](../../knowledge/07-hooks-et-garde-fous.md), [10 — Sécurité](../../knowledge/10-securite.md).

## Installation

```text
/plugin install garde-fous --marketplace wApMorty/AtelierAgentique
```

ou, en deux temps :

```text
/plugin marketplace add wApMorty/AtelierAgentique
/plugin install garde-fous@atelier-agentique
```

Prérequis : `bash` (fourni par Git pour Windows) et Python 3.10 ou plus récent, sans dépendance. Le lanceur [`scripts/run.sh`](scripts/run.sh) utilise `python3`, sinon `python` (sous Windows, `python3` peut être l'alias du Microsoft Store, qui échoue).

## Hooks

| Hook | Événement | Effet | En cas d'échec du hook |
|---|---|---|---|
| [`commandes_destructrices`](scripts/commandes_destructrices.py) | `PreToolUse` sur `Bash`, `PowerShell` | Bloque suppression récursive forcée hors du projet, push forcé, `git reset --hard`, `git clean -f`, `--no-verify` et `commit -n`, téléchargement suivi d'exécution, écriture sur un périphérique, et l'approbation de `verifier_fin` par l'agent | Bloque (`onFailure: block`) |
| [`ecriture_secrets`](scripts/ecriture_secrets.py) | `PreToolUse` sur `Write`, `Edit`, `MultiEdit` | Refuse l'écriture dans `.env`, `.envrc`, `.netrc`, `credentials(.json)`, `*.pem`, `*.key`, `*.p12`, clés SSH…, et tout texte écrit au format d'un secret connu (clés AWS, GitHub, Anthropic, Slack, Google, clés privées, webhooks Discord) ; le texte remplacé n'est pas analysé, pour qu'on puisse retirer une clé fuitée | Bloque (`onFailure: block`) |
| [`formater`](scripts/formater.py) | `PostToolUse` sur `Write`, `Edit`, `MultiEdit` | Formate le fichier avec `ruff` (Python) ou, dans un projet approuvé, le `prettier` local ; renvoie à l'agent les erreurs de `ruff check` ou de l'`eslint` local | Laisse passer |
| [`verifier_fin`](scripts/verifier_fin.py) | `Stop` | Exécute la commande de vérification du projet ; empêche l'agent de conclure tant qu'elle échoue | Laisse passer |

Un blocage renvoie le code 2 et une raison en français, transmise à l'agent, qui l'invite à expliquer le besoin à l'utilisateur plutôt qu'à contourner.

### Activer la vérification de fin

Créer à la racine du projet un fichier `.garde-fous.json` :

```json
{ "verification": "npm run typecheck" }
```

La commande s'exécute à chaque fin de tour de l'agent : choisir une vérification rapide (typage, tests unitaires ciblés) plutôt que toute la suite d'intégration ([chapitre 07](../../knowledge/07-hooks-et-garde-fous.md)).

Puis approuver une fois le couple projet–commande, **vous-même, dans un terminal**, depuis la racine du projet :

```sh
python "<chemin indiqué par le hook>/verifier_fin.py" --approuver
```

Le hook indique le chemin exact au premier déclenchement. L'approbation affiche la commande et demande de taper « oui » ; elle est refusée hors terminal interactif et bloquée si l'agent tente de la lancer. Les approbations sont enregistrées dans `~/.garde-fous/approbations.tsv`.

Sans approbation, la commande n'est jamais exécutée, et `formater` n'utilise pas les outils de `node_modules/.bin`, qui sont du code fourni par le dépôt : un dépôt cloné ne lance rien à votre insu. Toute modification de la commande exige une nouvelle approbation.

## Limites connues

- **Filtrage textuel** : `commandes_destructrices` lit le texte de la commande ; `sh -c '…'`, un script ou un alias le contournent. Il évite les accidents, il n'arrête pas un attaquant ; la barrière réelle est le bac à sable (`/sandbox`, [chapitre 10](../../knowledge/10-securite.md)).
- **Secrets au format libre** : un mot de passe sans format reconnaissable n'est pas détecté.
- **Écriture par le shell** : `ecriture_secrets` ne voit que les outils d'édition ; `cat > .env` ou `echo … >> config` lancés par Bash lui échappent.
- **Approbation contournable par un agent déterminé** : l'agent peut écrire directement dans `~/.garde-fous/approbations.tsv` s'il en a la permission. Le blocage de `--approuver` évite l'accident, pas l'attaque ; une règle `deny` sur ce fichier ferme la voie des outils d'édition.
- **Lecture des secrets** : ce plugin ne bloque que l'écriture. Pour la lecture, ajouter des règles `deny` dans les réglages, par exemple :

  ```json
  { "permissions": { "deny": ["Read(./.env)", "Read(./.env.*)", "Read(~/.ssh/**)"] } }
  ```

- **Python absent** : les deux hooks de sécurité bloquent alors tous les appels concernés, par construction.
- **Boucle sur `Stop`** : Claude Code accorde l'arrêt après plusieurs blocages consécutifs ; une suite durablement rouge ne bloque donc pas la session indéfiniment.

## Tests

```sh
python -m unittest discover -s plugins/garde-fous/tests
```

Les tests exécutent chaque hook comme Claude Code le fait (JSON sur l'entrée standard, code de sortie) et couvrent cas bloqués et cas autorisés. Ils tournent en CI.

## Équivalents

| Outil | Emplacement | Remarque |
|---|---|---|
| GitHub Copilot | `.github/hooks/*.json` | Scripts réutilisables tels quels ; noms d'événements et format d'entrée à adapter |
| OpenAI Codex | `.codex/hooks.json` ou `[hooks]` dans `config.toml` | Événements `PreToolUse`, `PostToolUse`, `Stop` disponibles ; format d'entrée à vérifier |

Sources des emplacements : [chapitre 13](../../knowledge/13-portabilite-et-standards.md).
