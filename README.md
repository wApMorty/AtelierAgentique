# AtelierAgentique

> Comprendre, outiller et transmettre l'engineering agentique : une base de connaissances sourcée, un système de développement qui l'applique, une veille qui la maintient à jour.

[![CI](https://github.com/wApMorty/AtelierAgentique/actions/workflows/ci.yml/badge.svg)](https://github.com/wApMorty/AtelierAgentique/actions/workflows/ci.yml)
[![Code : MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Contenu : CC BY 4.0](https://img.shields.io/badge/contenu-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT)

## Objectif

Les agents de code ont changé la pratique du développement plus vite que la littérature ne l'a décrite. Ce dépôt réunit, en français, ce qu'un ingénieur doit savoir pour travailler avec eux de façon rigoureuse :

- ce que l'on sait, avec des sources datées et leur niveau de fiabilité ;
- ce que l'on en fait, sous forme d'outils installables ;
- comment on le transmet, par des labs et des présentations.

Chaque composant du système cite le chapitre qui justifie sa conception : le système applique ce que la base enseigne.

## Contenu

| Dossier | Contenu | État |
|---|---|---|
| [`knowledge/`](knowledge/) | Base de connaissances : 15 chapitres sourcés et un glossaire | Brouillon complet, à relire |
| [`plugins/`](plugins/) | Plugins Claude Code : [`workflow`](plugins/workflow/), [`garde-fous`](plugins/garde-fous/) | Version 0.1.0, testés |
| [`veille/`](veille/) | Veille hebdomadaire automatisée | Prête ; tâche planifiée à créer |
| [`labs/`](labs/) | Exercices pratiques en TypeScript/Angular et Python | 3 labs |
| [`talks/`](talks/) | Gabarits et plans de présentation | Gabarit et skill `talk` |
| [`docs/decisions/`](docs/decisions/) | Décisions d'architecture (ADR) | En place |

## Installer les plugins

Dans Claude Code :

```text
/plugin marketplace add wApMorty/AtelierAgentique
/plugin install workflow@atelier-agentique
/plugin install garde-fous@atelier-agentique
```

Les deux plugins s'installent indépendamment. Les skills suivent le standard ouvert [Agent Skills](https://agentskills.io) et restent utilisables sous GitHub Copilot et Codex ; les hooks et subagents sont propres à Claude Code. Le détail figure dans l'[ADR-003](docs/decisions/ADR-003-portabilite.md) et dans le README de chaque plugin.

## Naviguer dans la base

Le [sommaire](knowledge/README.md) présente les chapitres dans l'ordre de lecture conseillé. Chaque chapitre suit le même plan : objectifs, concepts clés, mécanismes, bonnes pratiques, pièges, état du débat, liens vers les labs et composants, sources datées. Les sources sont classées en trois niveaux : **officiel**, **pratique reconnue**, **opinion / émergent**.

## Décisions structurantes

- [ADR-001 — Workflow de développement](docs/decisions/ADR-001-workflow-developpement.md)
- [ADR-002 — Architecture du dépôt](docs/decisions/ADR-002-architecture-repo.md)
- [ADR-003 — Portabilité multi-outils](docs/decisions/ADR-003-portabilite.md)
- [ADR-004 — Architecture de la veille](docs/decisions/ADR-004-architecture-veille.md)

## Licences

- Code (plugins, hooks, scripts, labs) : [MIT](LICENSE).
- Contenu (base de connaissances, présentations, documentation) : [CC BY 4.0](LICENSE-CONTENT).
