---
chapitre: 08
titre: Workflows de développement
statut: brouillon
derniere_revision: 2026-11-27
---

# 08 — Workflows de développement

> Organiser le travail avec un agent de code en étapes dont chacune produit une preuve vérifiable, avec une rigueur proportionnée au risque du changement.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- distinguer les grandes familles de workflows agentiques et leurs domaines de validité ;
- conduire un changement de bout en bout : cadrage, plan, implémentation pilotée par les tests, vérification, revue indépendante ;
- proportionner l'effort de spécification et de revue au risque du changement ;
- décider quand paralléliser, et à quelles conditions ;
- reconnaître les signes qu'un agent dérive, et les critiques documentées des approches les plus lourdes.

## Concepts clés

**Workflow agentique.** Séquence d'étapes, d'artefacts et de points de contrôle humains qui encadre le travail d'un agent sur un changement. Il se distingue d'un simple prompt par ses **sorties vérifiables** : une spec validée, un plan relu, des tests qui passent, un rapport de revue.

**Spec-driven development (SDD).** Approche où une spécification écrite précède le code et guide l'agent. Böckeler distingue trois niveaux [7] :

- *spec-first* : la spec est écrite avant le code, puis peut être abandonnée ;
- *spec-anchored* : la spec est conservée et maintenue avec le code ;
- *spec-as-source* : la spec est l'artefact maintenu, le code en est régénéré.

Elle observe que toutes les approches qu'elle a étudiées sont, en pratique, *spec-first* [7].

**Mode plan.** Mode de Claude Code dans lequel l'agent explore et propose sans rien modifier : il « makes no edits until you approve » [2]. Codex dispose d'un équivalent (`/plan`) [5].

**Boucle de vérification.** Commande que l'agent peut exécuter et dont le résultat est binaire : « Give Claude something it can run that comes back pass or fail » [1].

**Revue indépendante.** Relecture du changement par un agent ou un humain qui n'a pas participé à sa production, donc qui ne partage pas ses présupposés [1], [4].

**Guides et capteurs.** Dans le cadre proposé par Böckeler, les guides orientent l'agent avant qu'il agisse (spec, instructions, plan) et les capteurs l'observent après (tests, linters, revue) ; chacun peut être calculatoire (déterministe) ou inférentiel (jugement d'un modèle) [8].

## Mécanismes

### Pourquoi un workflow plutôt qu'un bon prompt

Un agent de code échoue rarement de façon spectaculaire ; il dérive. Kent Beck, à partir d'un projet mené en *augmented coding*, relève trois signaux d'alerte [10] :

- les **boucles** : l'agent répète des tentatives sans progresser ;
- les **fonctionnalités non demandées** ;
- la **triche**, notamment « disabling or deleting tests » pour obtenir un résultat vert.

Un workflow répond à chacun : la spec borne le périmètre, le test écrit d'abord fixe ce que « fait » veut dire, la vérification exécutée remplace l'affirmation de l'agent, et la revue indépendante détecte ce que l'auteur ne voit pas. Ces signaux proviennent d'un seul projet documenté ; ils recoupent toutefois les pièges décrits par les éditeurs [1], [5].

### Trois familles

| Famille | Principe | Sources représentatives | Domaine de validité |
|---|---|---|---|
| Itération conversationnelle | L'humain guide l'agent tour à tour, sans artefact intermédiaire | Pratique spontanée | Exploration, prototypes jetables |
| Spec → plan → exécution | Une spec puis un plan écrits précèdent l'implémentation, découpée en tâches | Reed [11], spec-kit [3], [6] | Fonctionnalités de taille moyenne à grande |
| Harness-first | L'effort porte sur l'environnement de l'agent : documentation versionnée, contrôles mécaniques, agents de nettoyage | OpenAI [9], Böckeler [8] | Bases de code où l'agent produit l'essentiel du code |

Ces familles se combinent plus qu'elles ne s'excluent. Le workflow de Harper Reed (idée, puis `spec.md` issu d'un échange question par question, puis plan découpé en prompts, puis exécution) en a fixé la forme dès début 2025, avec l'avertissement de son auteur : « it will probably not work in 2 weeks » [11]. spec-kit l'outille de façon prescriptive : constitution, *specify*, *plan*, *tasks*, *implement*, puis *converge* jusqu'à convergence, chaque étape étant relue avant la suivante [3]. À l'autre extrémité, l'équipe OpenAI qui a produit environ un million de lignes sans code écrit à la main décrit un travail centré sur le dépôt comme système de référence, un AGENTS.md réduit à une table des matières, des contrôles mécaniques (linters et tests structurels sur mesure) et des agents chargés de nettoyer la documentation et le code [9]. Ce retour d'expérience est celui d'un éditeur, sans mesure indépendante ; Böckeler note qu'il traite peu de la vérification du comportement fonctionnel [8].

### Un workflow de référence en cinq étapes

Le workflow retenu dans ce dépôt ([ADR-001](../docs/decisions/ADR-001-workflow-developpement.md)) synthétise les points de consensus. Il est décrit ici avec les mécanismes de Claude Code ; les équivalents existent sous Codex [5].

**1. Cadrer.** L'agent interroge l'humain jusqu'à pouvoir écrire une spec courte : « Interview me until you could write the spec, then write it to SPEC.md » [1]. Contenu minimal : objectif, hors-périmètre, critères d'acceptation vérifiables. Anthropic recommande ensuite de démarrer une session neuve pour construire à partir de la spec [1] : la spec devient la mémoire externe de la tâche (voir [chapitre 02](02-ingenierie-du-contexte.md)).

**2. Planifier.** En mode plan (`Shift+Tab` ou `claude --permission-mode plan`), l'agent explore en lecture seule et propose un découpage [2]. GitHub recommande des tâches testables isolément, « almost like a test-driven development process for your AI agent » [6]. L'humain relit le plan : c'est le point de contrôle le moins coûteux, avant qu'une ligne soit écrite.

**3. Implémenter.** Une tâche à la fois, en commençant par un test qui échoue dès qu'un comportement est en jeu. Le prompt de Kent Beck formalise la discipline : suivre `plan.md`, un test à la fois, rouge-vert-refactorisation, et ne jamais mélanger changements structurels et changements de comportement dans un même commit [10]. Simon Willison relève que le test d'abord est « particularly effective with agents that can iterate in a loop » [12]. Un commit par tâche donne des points de retour arrière.

**4. Vérifier.** Tests, lint, typage et build sont exécutés, et leur sortie fait foi, pas le compte rendu de l'agent [1]. Ce qui ne souffre pas d'exception est imposé par un hook plutôt que demandé : un hook `Stop` qui relance la vérification et bloque la fin de tâche en cas d'échec en est l'exemple type [1] (voir [chapitre 07](07-hooks-et-garde-fous.md)).

**5. Relire.** Un subagent relecteur, en contexte neuf et sans droit d'écriture, compare le diff à la spec. Anthropic recommande de lui demander explicitement d'ignorer le style, car un relecteur sommé de trouver des problèmes trouvera toujours quelque chose : « A reviewer that's asked to find problems will always find *something* » [1]. L'équipe Claude Code applique ce schéma avant chaque PR (« a second agent reviews the diff in a fresh context ») et fixe le nombre d'approbations humaines selon le risque du changement, non selon son auteur : « The change sets the tier, not the author » [4]. La PR reste l'unité de travail que l'humain relit et assume [13].

### Proportionner au risque

| Changement | Cadrer | Planifier | Implémenter | Vérifier | Relire |
|---|---|---|---|---|---|
| Trivial (coquille, renommage local) | — | — | Direct | Toujours | Humain, rapide |
| Standard (fonctionnalité, correctif) | Spec courte | Plan relu | TDD | Toujours | Agent puis humain |
| Risqué (sécurité, données, migration, architecture) | Spec complète, hors-périmètre explicite | Plan relu, tâches isolées | TDD, sessions neuves par tâche | Toujours, y compris non-régression | Agent, puis deux humains si possible |

La vérification n'est jamais optionnelle ; seuls le cadrage et la planification se modulent. La proportionnalité répond à la critique la mieux documentée du SDD : appliqué à un petit bug, Kiro a produit 4 *user stories* et 16 critères d'acceptation [7].

### Paralléliser

Claude Code ouvre une session dans un worktree Git dédié avec `claude --worktree <nom>` [2]. OpenAI cite parmi les erreurs courantes le fait de lancer des tâches simultanées sur les mêmes fichiers sans worktrees [5]. Trois conditions rendent la parallélisation rentable :

1. les tâches sont **indépendantes** : fichiers disjoints, aucune ne dépend du résultat d'une autre ;
2. chacune a sa **propre boucle de vérification** ;
3. la capacité de **relecture humaine** suit : paralléliser la production sans paralléliser la revue déplace le goulet d'étranglement.

Le code se prête moins à la parallélisation que la recherche, selon Anthropic elle-même [14], et chaque agent supplémentaire consomme son propre budget de tokens (voir [chapitre 11](11-couts-quotas-modeles.md)).

## Bonnes pratiques

1. **Écrire ce que « fini » veut dire avant de commencer** : critères d'acceptation vérifiables dans la spec, et commande de vérification connue de l'agent [1], [5].
2. **Relire le plan, pas seulement le code.** Une erreur de conception corrigée au plan coûte une phrase ; au code, une session.
3. **Exiger des preuves** : sortie des tests, pas « All tests pass » [1].
4. **Un commit par tâche, structure et comportement séparés** [10] : la revue et le retour arrière en deviennent simples.
5. **Sessions neuves entre tâches non liées** et après deux corrections infructueuses [1] (voir [chapitre 02](02-ingenierie-du-contexte.md)).
6. **Faire évoluer les instructions à partir des erreurs répétées**, pas par anticipation : « add new rules only after you notice repeated mistakes » [5].
7. **Borner la revue automatique** : critères explicites (conformité à la spec, correction, sécurité), style exclu, nombre de tours plafonné ; l'équipe Claude Code prend du recul après trois tours [4].

## Pièges et anti-patterns

- **La bureaucratie de spec.** Des dizaines de fichiers Markdown à relire pour un changement mineur. Böckeler : « I'd rather review code than all these markdown files » [7].
- **Le faux sentiment de contrôle.** Une spec détaillée ne garantit pas que l'agent la suive ; Böckeler a observé des instructions ignorées [7].
- **L'agent juge de ses propres tests.** Un agent qui écrit le code et les tests à partir de la même mauvaise lecture produit des tests verts et faux ; lui laisser modifier les résultats attendus « can also obscure a defect » [15]. D'où la revue indépendante et la relecture humaine des tests.
- **Les tests affaiblis ou supprimés** pour passer au vert [10]. Un hook ou une règle de revue doit signaler toute suppression d'assertion.
- **Le relecteur inflationniste** : sans consigne d'ignorer le style, la revue automatique noie les vrais défauts [1].
- **Le théâtre de la validation humaine** : une approbation systématique sans lecture réelle. Thoughtworks place le *human-in-the-loop theater* dans l'anneau *Caution* [16].
- **Paralléliser par défaut** : conflits de fusion, décisions implicites incompatibles entre agents [17], et revue qui ne suit pas.

## État du débat

### Jusqu'où spécifier ?

**Contesté.** GitHub présente les specs comme des artefacts vivants et « the shared source of truth » [6]. Böckeler se dit « very skeptical that lots of up-front spec design is a good idea », tout en jugant le *spec-first* « definitely valuable » [7]. Le niveau *spec-as-source* reste expérimental [7]. Le Radar de Thoughtworks (vol. 35, novembre 2026) ne classe pas le SDD en tant que tel ; il place en *Trial* des pratiques voisines, comme les plans visuels interactifs avec les agents et l'outil OpenSpec [16]. Le consensus porte sur l'existence d'une spec courte et vérifiable, pas sur sa forme ni sur sa durée de vie.

### Le harnais vaut-il son coût ?

**Contesté, dépendant du modèle.** Dans une expérience menée sur un service avec 178 tests d'acceptation, Naresh Jain observe qu'un modèle performant réussit 10 fois sur 10 avec ou sans harnais, le harnais multipliant les tokens par environ 10,5 sans gain, alors qu'un modèle moins capable passe de 3 à 10 réussites sur 10 grâce au harnais, pour un coût total inférieur à celui du modèle performant [15]. L'auteur, affilié à l'outil testé, juge lui-même le résultat non généralisable. La conclusion qu'il en tire est prudente : ce qui change avec la capacité du modèle, ce n'est pas le besoin de capteurs indépendants, mais le moment où ils interviennent [15].

### Combien de revue humaine ?

**Contesté.** Anthropic écrivait fin 2024 que la revue humaine « remains crucial » [14]. Fin 2026, l'équipe Claude Code fait relire chaque PR par des agents et module l'approbation humaine selon le risque, en déclarant un doublement des PR fusionnées et une baisse de plus de 40 % de la part des retours arrière [4] ; ces chiffres sont auto-déclarés. La revue selon le risque fait consensus ; le niveau de risque en dessous duquel une revue humaine peut être omise ne fait pas consensus.

### Les gains de productivité sont-ils établis ?

**Non établis.** L'essai randomisé de METR (début 2025) mesurait un ralentissement de 19 % chez des développeurs expérimentés, contre une accélération ressentie de 20 % [18]. Le suivi lancé en août 2025 donne des estimations d'accélération (−18 % et −4 % de durée) que METR juge elle-même peu fiables, à cause d'effets de sélection : des développeurs refusent désormais de travailler sans IA [18]. Une enquête de METR de mai 2026, déclarative, fait état de gains médians ressentis importants, avec des réserves explicites sur leur ampleur [19]. Un workflow se justifie donc aujourd'hui par la **fiabilité** et la **vérifiabilité** du résultat, pas par un gain de vitesse démontré.

## Dans ce dépôt

- **Composants** : [ADR-001](../docs/decisions/ADR-001-workflow-developpement.md) ; plugin [`workflow`](../plugins/workflow/), qui expose une commande par étape et le subagent `relecteur` ; plugin [`garde-fous`](../plugins/garde-fous/), qui porte la vérification de fin de tâche.
- **Labs** : [lab 01 — workflow complet de bout en bout](../labs/README.md) (à venir).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
2. **[O]** Anthropic, *Common workflows*. <https://code.claude.com/docs/en/common-workflows>
3. **[O]** GitHub, *spec-kit*, README. <https://github.com/github/spec-kit>
4. **[O]** Osmani, Lunt, Wang (équipe Claude Code), *How the Claude Code team does code review*, 15/10/2026. Chiffres auto-déclarés. <https://claude.dev/blog/solving-code-review-at-anthropic>
5. **[O]** OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
6. **[O]** Delimarsky (GitHub), *Spec-driven development with AI: Get started with a new open source toolkit*, 02/09/2025. <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/>
7. **[P]** Böckeler, *Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl*, 15/10/2025. <https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html>
8. **[P]** Böckeler, *Harness engineering for coding agent users*, 02/04/2026, et *Harness Engineering — first thoughts*, 17/02/2026. <https://www.martinfowler.com/articles/harness-engineering.html> · <https://www.martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html>
9. **[O]** Lopopolo (OpenAI), *Harness engineering: leveraging Codex in an agent-first world*, 11/02/2026. Retour d'expérience d'éditeur, sans mesure indépendante. <https://openai.com/index/harness-engineering/>
10. **[P]** Beck, *Augmented Coding: Beyond the Vibes*, 25/06/2025. Projet unique ; parrainage déclaré. <https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes>
11. **[P]** Reed, *My LLM codegen workflow atm*, 16/02/2025. <https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/>
12. **[E]** Willison, *Vibe engineering*, 07/10/2025, mis à jour le 23/02/2026. Essai, sans données. <https://simonwillison.net/2025/Oct/7/vibe-engineering/>
13. **[E]** Willison, notes du tag *coding-agents* (« The PR is my unit of work », 09/11/2026). <https://simonwillison.net/tags/coding-agents/>
14. **[O]** Anthropic, *Building effective agents*, 19/12/2024 (partiellement daté selon l'éditeur), et *How we built our multi-agent research system*, 13/06/2025. <https://www.anthropic.com/engineering/building-effective-agents> · <https://www.anthropic.com/engineering/multi-agent-research-system>
15. **[P]** Jain, *Are Harnesses Worth the Cost?*, 13/10/2026. Expérience unique, auteur affilié à l'outil testé. <https://martinfowler.com/articles/are-harnesses-worth-the-cost.html>
16. **[P]** Thoughtworks, *Technology Radar*, vol. 35, novembre 2026 (anneaux relevés, fiches détaillées non lues). <https://www.thoughtworks.com/radar>
17. **[P]** Yan (Cognition), *Don't Build Multi-Agents*, 12/06/2025. <https://cognition.com/blog/dont-build-multi-agents>
18. **[P]** METR, *We are Changing our Developer Productivity Experiment Design*, 24/02/2026. <https://metr.org/blog/2026-02-24-uplift-update/>
19. **[P]** Becker (METR), *Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity*, 11/05/2026. Enquête déclarative, échantillon de convenance. <https://metr.org/blog/2026-05-11-ai-usage-survey/>
