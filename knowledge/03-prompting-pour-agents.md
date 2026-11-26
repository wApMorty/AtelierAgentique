---
chapitre: 03
titre: Prompting pour agents
statut: brouillon
derniere_revision: 2026-11-27
---

# 03 — Prompting pour agents

> Écrire des instructions qu'un agent suit sur des dizaines de tours : fichiers d'instructions, specs, prompts de tâche et prompts de délégation.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- distinguer les quatre niveaux d'instruction d'un agent de code et ce qui relève de chacun ;
- rédiger un fichier d'instructions de dépôt court et utile ;
- formuler un prompt de tâche qui définit ce que « fini » veut dire ;
- prévenir par l'instruction les dérives connues (sur-ingénierie, triche sur les tests, spéculation) ;
- reconnaître quand une instruction doit devenir un hook.

## Concepts clés

**Niveaux d'instruction.** Un agent de code reçoit des consignes à quatre niveaux, de durée de vie décroissante :

| Niveau | Support | Durée de vie | Exemple |
|---|---|---|---|
| Projet | `AGENTS.md`, `CLAUDE.md`, règles par chemin | Toutes les sessions | Commandes de test, conventions |
| Procédure | Skill | Invocation | Étapes d'une revue, d'une release |
| Tâche | Spec, plan, prompt initial | Une tâche | Objectif, critères d'acceptation |
| Délégation | Prompt d'un subagent | Une sous-tâche | Question précise, format de retour |

**Instruction déterministe ou non.** Anthropic oppose ce que le modèle lit et peut ne pas suivre (« Non-deterministic: you write the instruction, and Claude (the model) reads it ») à ce que l'outil applique à chaque fois (hook, règle de permission) [1]. Le prompting couvre le premier cas seulement.

## Mécanismes

### Ce que les modèles récents attendent

Le guide officiel d'Anthropic, mis à jour pour la génération actuelle de modèles, pose plusieurs principes [2] :

- **Explicite plutôt qu'implicite** : « Claude responds well to clear, explicit instructions ». Demander « Can you suggest some changes » produit des suggestions ; « Change this function to improve its performance » produit des modifications [2].
- **Donner la raison** : expliquer le but d'une consigne aide le modèle à la généraliser correctement [2].
- **Le test du collègue** : un prompt qu'un collègue sans contexte ne comprendrait pas est un prompt insuffisant [2].
- **Ne pas crier** : les modèles récents sont plus réceptifs qu'avant ; une formulation comme « CRITICAL: You MUST use this tool » peut provoquer un sur-déclenchement, et « Use this tool when… » suffit [2].

### Prévenir les dérives connues

Le même guide fournit des formulations ciblées pour des dérives observées sur les agents de code [2] :

| Dérive | Formulation proposée par l'éditeur |
|---|---|
| Spéculation sur du code non lu | « Never speculate about code you have not opened » |
| Sur-ingénierie, fichiers superflus | « Only make changes that are directly requested or clearly necessary » |
| Solutions taillées pour les tests | « Do not hard-code values or create solutions that only work for specific test inputs » |
| Tests modifiés pour passer | « It is unacceptable to remove or edit tests » |
| Fin sans vérification | « Before you finish, verify your answer » |

Ces formulations varient selon les modèles : le guide signale par exemple un risque de sur-vérification sur un modèle récent, pour lequel la consigne de vérification finale est à doser [2] **(Daté)**.

### Le fichier d'instructions de dépôt

Les trois éditeurs convergent sur le contenu : commandes de build, de test et de lint, conventions qui ne se déduisent pas du code, structure utile, définition de « terminé » [3], [4]. OpenAI recommande de commencer par l'essentiel et de n'ajouter une règle qu'après une erreur répétée [4] ; Anthropic propose un filtre : l'agent pourrait-il le découvrir en lisant le code, et irait-il vraiment chercher ? [1]. L'équipe OpenAI de l'expérience « sans code écrit à la main » limite AGENTS.md à une table des matières d'environ cent lignes, qui renvoie vers une documentation versionnée [5].

Une étude publiée sur arXiv (révisée en septembre 2026) mesure que ces fichiers n'améliorent pas en général le taux de réussite sur ses tâches de benchmark, augmentent le coût d'inférence de plus de 20 %, sont bien suivis quand ils contiennent des consignes, et que les vues d'ensemble du dépôt n'aident pas [6]. Implication pratique : **des consignes, pas des descriptions** (voir [chapitre 02](02-ingenierie-du-contexte.md)).

### Le prompt de tâche

Un prompt de tâche efficace nomme le fichier, le symptôme et ce que « corrigé » signifie [1]. Exemple donné par Anthropic : écrire d'abord un test qui reproduit le bug, puis le corriger [1]. Pour une tâche plus large, la spec issue d'un entretien remplace le prompt (voir [chapitre 08](08-workflows-developpement.md)). Pour les tâches longues, le guide recommande d'externaliser l'état dans des fichiers structurés (`tests.json`) et libres (`progress.txt`), et de reprendre une session neuve en les relisant avec l'historique git [2].

### Le prompt de délégation

Un subagent ne voit pas la conversation principale (voir [chapitre 06](06-subagents-et-orchestration.md)). Son prompt doit donc être autoporteur : contexte minimal, question précise, périmètre (ce qu'il ne doit pas faire), format et longueur du retour. Un prompt de délégation vague produit soit un retour trop long qui encombre le contexte principal, soit une réponse à une autre question.

### Quand l'instruction ne suffit pas

Si une ligne d'instruction doit être répétée ou renforcée pour être suivie, « that's a sign the line belongs in a hook » [1]. Les instructions orientent ; elles ne garantissent rien face à une compaction, à une injection de prompt ou à une erreur du modèle (voir [chapitre 07](07-hooks-et-garde-fous.md)).

## Bonnes pratiques

1. **Placer chaque consigne au niveau de sa durée de vie** : projet, procédure, tâche ou délégation.
2. **Écrire des consignes vérifiables** (« lancer `npm test` avant de conclure ») plutôt que des intentions (« écrire du code de qualité »).
3. **Donner la raison** d'une règle non évidente [2].
4. **Faire évoluer AGENTS.md à partir des erreurs observées**, en demandant à l'agent une rétrospective quand une erreur se répète [4].
5. **Rendre les prompts de délégation autoporteurs** et imposer un format de retour court.
6. **Basculer en hook** toute consigne qui ne souffre pas d'exception [1].

## Pièges et anti-patterns

- **Le fichier d'instructions généré et jamais relu** : descriptions redondantes, coût sans bénéfice [6].
- **Les majuscules et l'emphase** : effet de sur-déclenchement sur les modèles récents [2].
- **Les consignes contradictoires** entre CLAUDE.md, une règle par chemin et le prompt de tâche : le modèle arbitre seul (conflit de contexte, [chapitre 02](02-ingenierie-du-contexte.md)).
- **La consigne de sécurité en prose** : une instruction « ne jamais lire .env » ne protège pas ; une règle `deny` le fait ([chapitre 10](10-securite.md)).
- **Le prompt de tâche sans critère d'arrêt** : l'agent décide seul qu'il a fini.

## État du débat

- **Utilité des fichiers d'instructions** : **Contesté** — recommandation unanime des éditeurs [1], [3], [4] contre résultats mitigés d'une étude indépendante [6] ; voir [chapitre 02](02-ingenierie-du-contexte.md).
- **Formulations dépendantes du modèle** : les consignes efficaces changent d'une génération à l'autre [2] ; un fichier d'instructions est à relire à chaque changement de modèle. **Daté.**

## Dans ce dépôt

- **Composants** : [AGENTS.md](../AGENTS.md) applique la règle « consignes, pas descriptions » ; les skills du plugin [`workflow`](../plugins/workflow/) portent les procédures ; les prompts des subagents imposent un format de retour.
- **Labs** : voir le [lab 03 — conception d'un skill](../labs/README.md).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
2. **[O]** Anthropic, *Prompting best practices* (non daté ; couvre les modèles jusqu'à la génération 5.5). <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
3. **[O]** AGENTS.md. <https://agents.md/>
4. **[O]** OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
5. **[O]** Lopopolo (OpenAI), *Harness engineering: leveraging Codex in an agent-first world*, 11/02/2026. <https://openai.com/index/harness-engineering/>
6. **[P]** Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv 2602.11988, v3 du 29/09/2026 (résumé lu). <https://arxiv.org/abs/2602.11988>
