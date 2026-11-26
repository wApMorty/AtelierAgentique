# ADR-001 — Workflow de développement agentique

- **Statut** : proposé
- **Date** : 2026-11-26

## Contexte

Le système agentique du dépôt doit outiller un workflow de développement professionnel. La question est de savoir lequel : l'état de l'art oscille entre le *spec-driven development* outillé (spec-kit, Kiro), des boucles plus légères « plan → implémentation → revue », et des harnais plus ou moins lourds selon le modèle employé.

## Décision

Un workflow unique, **proportionné au risque**, en cinq étapes. Les étapes 1 et 2 sont allégées ou omises pour les changements triviaux ; elles ne le sont jamais pour un changement risqué.

| Étape | Contenu | Sortie vérifiable |
|---|---|---|
| 1. Cadrer | Entretien de l'agent avec l'humain jusqu'à pouvoir écrire une spec courte : objectif, hors-périmètre, critères d'acceptation testables. | `SPEC.md` (ou section d'issue) validée par l'humain |
| 2. Planifier | Exploration en lecture seule, puis découpage en tâches testables isolément. | Plan relu par l'humain |
| 3. Implémenter | Une tâche à la fois, en commençant par un test qui échoue (TDD) dès qu'un comportement est en jeu ; session neuve ou `/clear` entre tâches non liées. | Tests verts, commit atomique |
| 4. Vérifier | Boucle déterministe : tests, lint, types, build. Imposée par hook, pas seulement demandée par instruction. | Sortie des commandes, pas une affirmation |
| 5. Relire | Revue par un agent indépendant, en contexte neuf, contre la spec et non contre le style ; puis revue humaine de la PR, dont l'exigence dépend du risque. | Rapport de revue, PR approuvée |

Gestion du contexte, transverse : la spec et le plan servent de mémoire externe ; l'exploration volumineuse est déléguée à un subagent qui ne renvoie qu'une synthèse ; une session par unité de travail cohérente.

Parallélisation : réservée aux tâches indépendantes (fichiers disjoints), chacune dans son propre worktree. Elle n'est pas le mode par défaut, en raison du quota Pro.

## Justification

- **Une boucle de vérification exécutable est le point de consensus le plus fort** chez les éditeurs comme chez les praticiens : « Give Claude something it can run that comes back pass or fail » [1] ; même recommandation côté OpenAI (tests, lint, types, revue du diff) [5] et GitHub [6].
- **Le déterministe l'emporte sur l'instruction pour ce qui ne souffre pas d'exception** : une règle qu'on renforce à répétition dans CLAUDE.md « belongs in a hook » [1]. D'où l'étape 4 portée par des hooks.
- **La revue indépendante en contexte neuf** est recommandée par Anthropic (subagent relecteur, ou seconde session) [1] et pratiquée à grande échelle par l'équipe Claude Code (« a second agent reviews the diff in a fresh context », niveau d'approbation humaine fixé par le risque du changement) [4]. Elle répond au risque, signalé par Jain, d'un agent qui écrit code et tests à partir de la même mauvaise lecture [8].
- **Une spec courte, issue d'un entretien**, est la forme recommandée par Anthropic (« Interview me until you could write the spec ») [1] et par OpenAI (mode Plan, entretien, PLANS.md pour le travail long) [5]. Le *spec-first* est jugé utile même par ses critiques [7].
- **La proportionnalité** répond aux critiques documentées du SDD lourd : un petit bug transformé en 4 user stories et 16 critères d'acceptation, une surcharge de Markdown à relire [7]. Elle suit aussi le principe éditeur de partir de la solution la plus simple et de n'ajouter de complexité que mesurée utile [2].
- **Le TDD** fournit le signal pass/fail dès l'implémentation ; il est explicitement rapproché du découpage en tâches testables par GitHub [6] et cité comme formulation de prompt par Anthropic [1].

## Alternatives écartées

- **spec-kit complet (constitution → specify → plan → tasks → implement → converge)** [3] : rigoureux, mais disproportionné pour la majorité des changements et coûteux en relecture [7]. Ses idées utiles (critères vérifiables, tâches isolables) sont reprises.
- **Spec-as-source** (la spec est l'artefact maintenu, le code est régénéré) : encore expérimental, aucun outillage stable [7]. Suivi par la veille.
- **Itération libre sans spec ni vérification imposée** : contredit le consensus sur la boucle de vérification [1], [5], [6].
- **Harnais lourd systématique** (multiples agents, revues en éventail à chaque changement) : son bénéfice dépend du modèle — nul pour un modèle fort, décisif pour un modèle plus faible, au prix d'environ 10 fois plus de tokens [8]. Incompatible avec un quota Pro comme réglage par défaut.

## Conséquences

- Le plugin de workflow expose une commande par étape ; les étapes 4 et 5 s'appuient sur des hooks et un subagent relecteur sans accès en écriture.
- Le chapitre « Workflows de développement » de la base justifie et détaille ce choix ; le chapitre « Vérification et évaluation » couvre les étapes 4 et 5.

## Incertitudes

- **Gains de productivité non établis** : l'essai randomisé de METR (2025) mesurait un ralentissement de 19 % ; METR juge désormais ses propres données de suivi biaisées par des effets de sélection et « only very weak evidence » [9]. Les chiffres favorables publiés par les éditeurs sont auto-déclarés [4]. Ce workflow vise la fiabilité et la vérifiabilité, pas un gain de vitesse démontré.
- **Le niveau de harnais optimal évolue avec les modèles** [8], [10] : la proportion entre étapes « guides » et « capteurs » est à réévaluer par la veille.

## Sources

Consultées le 2026-11-26. Niveaux : **O** = officiel, **P** = pratique reconnue, **E** = opinion / émergent.

1. **O** — Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
2. **O** — Anthropic, *Building effective agents*, 19/12/2024 (signalé partiellement daté par l'éditeur). <https://www.anthropic.com/engineering/building-effective-agents>
3. **O** — GitHub, *spec-kit*, README. <https://github.com/github/spec-kit>
4. **O** — Osmani, Lunt, Wang (équipe Claude Code), *How the Claude Code team does code review*, 15/10/2026. Chiffres auto-déclarés. <https://claude.dev/blog/solving-code-review-at-anthropic>
5. **O** — OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
6. **O** — Delimarsky (GitHub), *Spec-driven development with AI*, 02/09/2025. <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>
7. **P** — Böckeler, *Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl*, 15/10/2025. <https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html>
8. **P** — Jain, *Are Harnesses Worth the Cost?*, 13/10/2026. Expérience unique, auteur affilié à l'outil testé ; non généralisable selon l'auteur. <https://martinfowler.com/articles/are-harnesses-worth-the-cost.html>
9. **P** — METR, *We are Changing our Developer Productivity Experiment Design*, 24/02/2026. <https://metr.org/blog/2026-02-24-uplift-update/>
10. **O** — Anthropic, *Scaling Managed Agents*, 08/04/2026 (« harnesses encode assumptions [...] can go stale »). <https://www.anthropic.com/engineering/managed-agents>
