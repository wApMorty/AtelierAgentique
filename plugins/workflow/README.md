# Plugin `workflow`

Outille le workflow de développement de l'[ADR-001](../../docs/decisions/ADR-001-workflow-developpement.md) : cinq étapes, chacune produisant une sortie vérifiable, avec une rigueur proportionnée au risque du changement.

Chapitre de référence : [08 — Workflows de développement](../../knowledge/08-workflows-developpement.md).

## Installation

```text
/plugin install workflow --marketplace wApMorty/AtelierAgentique
```

ou, en deux temps :

```text
/plugin marketplace add wApMorty/AtelierAgentique
/plugin install workflow@atelier-agentique
```

## Usage

| Étape | Commande | Sortie | Chapitre |
|---|---|---|---|
| 1. Cadrer | `/workflow:cadrer` | `specs/<slug>/spec.md` validée | [08](../../knowledge/08-workflows-developpement.md) |
| 2. Planifier | `/workflow:planifier` | `specs/<slug>/plan.md` relu | [08](../../knowledge/08-workflows-developpement.md) |
| 3. Implémenter | `/workflow:implementer [tâche]` | Un commit par tâche, tâche cochée | [08](../../knowledge/08-workflows-developpement.md) |
| 4. Vérifier | `/workflow:verifier` | Rapport critère par critère | [09](../../knowledge/09-verification-et-evaluation.md) |
| 5. Relire | `/workflow:relire` | Rapport du relecteur indépendant | [08](../../knowledge/08-workflows-developpement.md), [09](../../knowledge/09-verification-et-evaluation.md) |

Pour un changement trivial, `cadrer` le signale et propose de passer directement à l'implémentation.

Coût permanent en contexte : environ 520 tokens par session (descriptions des skills et agents), d'après `claude plugin details workflow` ; le corps d'un skill (250 à 470 tokens) n'est chargé qu'à l'invocation.

## Composants

### Skills

Format standard [Agent Skills](https://agentskills.io/specification) : `name`, `description`, `license`, `metadata` (chapitre et étape).

**Extension propre à Claude Code** : `disable-model-invocation: true` sur `implementer`, seul skill qui crée des commits, pour qu'il ne se déclenche jamais sans demande explicite ([ADR-003](../../docs/decisions/ADR-003-portabilite.md), [chapitre 05](../../knowledge/05-skills.md)).

### Subagents

| Agent | Rôle | Outils | Modèle | Justification |
|---|---|---|---|---|
| `relecteur` | Revue indépendante du diff contre la spec, sans voir la production | `Read, Grep, Glob, Bash` (git en lecture et tests) | Celui de la session | [08](../../knowledge/08-workflows-developpement.md), [09](../../knowledge/09-verification-et-evaluation.md) |
| `chercheur` | Recherche documentaire sourcée et datée, isolée du contexte principal | `Read, Grep, Glob, WebSearch, WebFetch` | Haiku | [02](../../knowledge/02-ingenierie-du-contexte.md), [06](../../knowledge/06-subagents-et-orchestration.md) |

Aucun des deux n'a d'outil d'écriture de fichier. Les subagents de plugin ne peuvent pas fixer `permissionMode` ni déclarer de hooks ; la restriction de Bash du relecteur aux commandes en lecture relève donc de son prompt, et les garde-fous du plugin [`garde-fous`](../garde-fous/) s'appliquent à lui comme à la session.

### MCP

Aucun serveur MCP. Les besoins du workflow (git, forge, tests, recherche web) sont couverts par la CLI et les outils intégrés ; un serveur ajouterait un coût en contexte et une surface d'attaque sans gain démontré ([chapitre 04](../../knowledge/04-outils-et-mcp.md)).

## Équivalents

| Composant | GitHub Copilot | OpenAI Codex |
|---|---|---|
| Skills | Copier `skills/*` dans `.github/skills/` ou `.claude/skills/` du projet ; le format est le même | Copier `skills/*` dans `.agents/skills/` du projet ou de l'utilisateur |
| `disable-model-invocation` | Non standard : à retirer, et ne lancer `implementer` que sur demande | Idem |
| `relecteur`, `chercheur` | Agent personnalisé dans `.github/agents/`, corps du prompt réutilisable | Agent personnalisé TOML dans `.codex/agents/`, prompt dans `developer_instructions` |

Sources des emplacements : [chapitre 13](../../knowledge/13-portabilite-et-standards.md).
