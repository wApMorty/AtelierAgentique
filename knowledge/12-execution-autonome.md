---
chapitre: 12
titre: Exécution autonome
statut: relu
derniere_revision: 2026-11-27
---

# 12 — Exécution autonome

> Laisser un agent travailler sans surveillance (en script, en CI, sur planification) à condition d'avoir répondu à l'avance à ce que personne ne sera là pour décider.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- utiliser le mode non interactif de Claude Code et en connaître les options de contrôle ;
- configurer des permissions adaptées à une exécution sans humain ;
- intégrer un agent à GitHub Actions et à une tâche planifiée dans le cloud ;
- appliquer une liste de contrôle avant toute exécution autonome.

## Concepts clés

**Exécution non interactive** (*headless*). Lancement de l'agent par une commande unique qui se termine avec un code de sortie : `claude -p "<prompt>"` [1].

**Tâche planifiée cloud.** Configuration enregistrée (prompt, dépôts, connecteurs) exécutée selon un calendrier, par appel d'API ou sur événement GitHub, chaque exécution ouvrant une session complète consultable ensuite [2].

## Mécanismes

### Le mode non interactif

Options principales [1] :

| Option | Rôle |
|---|---|
| `-p` | Exécute le prompt et termine ; code de sortie nul en cas de succès |
| `--output-format text \| json \| stream-json` | `json` fournit résultat, identifiant de session et coût estimé ; `--json-schema` ajoute une sortie structurée |
| `--allowedTools` | Pré-autorise des outils ou des commandes (`Bash(git diff *)`) |
| `--permission-mode` | Mode de permission de l'exécution |
| `--max-budget-usd` | Plafond de dépense de l'exécution |
| `--bare` | Ignore hooks, skills, plugins, MCP, mémoire et CLAUDE.md découverts automatiquement ; recommandé pour les appels scriptés |
| `--resume <id>` | Reprend une session précise |

`--bare` mérite attention : il rend l'exécution reproductible, mais désactive aussi les hooks de garde-fous non passés explicitement [1]. Une exécution autonome qui compte sur un hook doit donc le fournir par `--settings`.

### Permissions sans humain

Sans mode précisé, `-p` démarre en mode manuel : toute action qui demanderait une approbation est refusée [1], [3] **(Daté)**. Recommandations de l'éditeur [3] :

- en CI, `dontAsk` avec des règles d'autorisation étroites, par exemple `--permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"` ;
- `auto` si l'on accepte qu'un classifieur décide, en sachant qu'il ne garantit pas la sécurité ;
- `bypassPermissions` seulement dans un environnement isolé, conteneur ou VM sans accès internet.

Les sessions cloud ignorent `bypassPermissions` et `dontAsk` placés dans les fichiers de réglages [3].

### GitHub Actions

L'action `anthropics/claude-code-action@v1` fonctionne en mode interactif (réponse à une mention `@claude` dans une issue ou une PR) ou en mode automatisation (prompt fourni, déclenchement sur tout événement, y compris `schedule`) [4]. Points de sécurité documentés [4] :

- seuls les utilisateurs disposant d'un accès en écriture déclenchent l'action par défaut ; les robots sont refusés sauf liste explicite, ce qui évite les boucles ;
- clés dans les secrets GitHub, jamais dans le dépôt ;
- permissions minimales par workflow ;
- une poussée effectuée avec le `GITHUB_TOKEN` par défaut ne déclenche pas d'autres workflows.

### Tâches planifiées cloud

Disponibles sur les offres Pro et supérieures, en *research preview* [2] **(Daté)**. Par défaut, une exécution pousse son travail sur une branche préfixée `claude/` sauf consigne contraire du prompt ; pour contrôler les branches concernées, la documentation renvoie aux règles de protection de GitHub [2]. L'environnement cloud démarre en accès réseau limité (registres de paquets, GitHub, SDK cloud et domaines ajoutés) [5]. Le proxy GitHub rejette GraphQL, donc `gh pr create` ; l'API REST (`gh api`) fonctionne [5].

### Avant de partir

Anthropic résume la préparation d'une exécution sans surveillance en cinq questions [6] :

1. Qu'est-ce qui définit « terminé » ?
2. Comment l'agent vérifie-t-il lui-même son travail ?
3. Que peut-il toucher ?
4. Qu'est-ce qui l'arrête (plafond de tours, de budget) ?
5. Qui approuve le résultat ?

## Bonnes pratiques

1. **Répondre par écrit aux cinq questions** avant toute automatisation [6].
2. **Ne pas planifier avant d'avoir fiabilisé à la main** : OpenAI recommande de ne pas programmer une tâche avant qu'elle soit fiable manuellement [7].
3. **Permissions en liste blanche** (`dontAsk` + `--allowedTools`) [3].
4. **Plafonner** tours, budget et durée [1], [4].
5. **Un résultat qui passe par une revue** : branche et PR, jamais d'écriture directe sur la branche principale ; protection de branche côté forge [2].
6. **Réseau en liste blanche** pour les exécutions qui lisent du contenu externe ([chapitre 10](10-securite.md)).

## Pièges et anti-patterns

- **`bypassPermissions` sur un runner partagé** [3].
- **Compter sur un hook avec `--bare`** sans le fournir explicitement [1].
- **Une tâche planifiée qui écrit sur `main`** faute de protection de branche [2].
- **L'exécution autonome sans plafond de budget** sur un quota partagé avec le travail interactif ([chapitre 11](11-couts-quotas-modeles.md)).
- **Le déclenchement par des utilisateurs externes** sur un dépôt public, qui expose l'agent à du contenu hostile [4].

## État du débat

- **Builds autonomes de nuit** : Thoughtworks place les *unattended overnight agentic builds* en *Trial* et l'*agent sandboxing* en *Adopt* (vol. 35) [8]. La pratique se diffuse ; ses conditions de sûreté restent celles de ce chapitre.
- **Le classifieur du mode `auto`** comme substitut à l'approbation humaine : utile contre la fatigue d'approbation, sans garantie revendiquée [3]. **Émergent.**

## Dans ce dépôt

- **Composants** : la veille hebdomadaire est une tâche planifiée cloud qui applique ces règles ([ADR-004](../docs/decisions/ADR-004-architecture-veille.md), [`veille/`](../veille/)).
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic, *Run Claude Code programmatically* (headless). <https://code.claude.com/docs/en/headless>
2. **[O]** Anthropic, *Automate work with scheduled tasks*. <https://code.claude.com/docs/en/routines>
3. **[O]** Anthropic, *Choose a permission mode* (lu en partie sous forme résumée). <https://code.claude.com/docs/en/permission-modes>
4. **[O]** Anthropic, *Claude Code GitHub Actions*. <https://code.claude.com/docs/en/github-actions>
5. **[O]** Anthropic, *Claude Code on the web* et *Cloud environments*. <https://code.claude.com/docs/en/claude-code-on-the-web>
6. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
7. **[O]** OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
8. **[P]** Thoughtworks, *Technology Radar*, vol. 35, novembre 2026 (anneaux relevés, fiches non lues). <https://www.thoughtworks.com/radar>
