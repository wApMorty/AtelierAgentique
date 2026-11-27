---
chapitre: 01
titre: Fondamentaux et boucle agentique
statut: relu
derniere_revision: 2026-11-27
---

# 01 — Fondamentaux et boucle agentique

> Comprendre ce qu'est un agent de code, comment tourne sa boucle, pourquoi elle échoue, et ce que l'on appelle désormais son harnais.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- distinguer un workflow à base de LLM d'un agent, et choisir le niveau d'autonomie adapté ;
- décrire la boucle raisonnement–action–observation et ses origines ;
- nommer les modes d'échec propres à la boucle ;
- définir le harnais, ses guides et ses capteurs, et expliquer pourquoi il vieillit avec les modèles.

## Concepts clés

**Workflow et agent.** Anthropic distingue les *workflows*, où des LLM et des outils sont orchestrés par des chemins de code prédéfinis, des *agents*, où le modèle dirige lui-même son processus et l'usage de ses outils [1]. Un agent de code relève de la seconde catégorie ; il peut être enveloppé dans un workflow (voir [chapitre 08](08-workflows-developpement.md)).

**Boucle agentique.** Cycle où le modèle produit un raisonnement et une action (appel d'outil), reçoit l'observation qui en résulte, et recommence jusqu'à juger la tâche terminée. Le schéma a été formalisé par ReAct, qui fait générer au modèle « reasoning traces and task-specific actions in an interleaved manner » [2].

**Outil.** Fonction que le modèle peut demander d'exécuter : lire un fichier, lancer une commande, interroger un service (voir [chapitre 04](04-outils-et-mcp.md)).

**Harnais** (*harness*). Tout ce qui entoure le modèle pour en faire un agent utile : prompt système, outils, gestion du contexte, permissions, contrôles. Böckeler y distingue les **guides**, qui anticipent et orientent l'action, et les **capteurs**, qui observent après l'action et permettent l'autocorrection ; chacun est **calculatoire** (déterministe : tests, linters, typage) ou **inférentiel** (jugement d'un modèle : revue par IA, LLM-juge) [3].

## Mécanismes

### La boucle

Dans sa forme la plus simple, la boucle est un `while` : envoyer le contexte au modèle, exécuter les appels d'outils qu'il demande, ajouter les résultats au contexte, recommencer tant qu'il demande des outils. Le banc d'essai SWE-bench utilise d'ailleurs comme référence minimale « a simple ReAct agent loop » dans un environnement bash [10].

ReAct a montré que l'entrelacement du raisonnement et de l'action aide le modèle à « induce, track, and update action plans » tout en s'appuyant sur des sources externes, et qu'il réduit les hallucinations par rapport au raisonnement seul [2]. Ce qui distingue un agent de code moderne de cette boucle minimale tient presque entièrement au harnais.

### Ce que le harnais ajoute

| Composant | Rôle | Exemple dans Claude Code |
|---|---|---|
| Prompt système et instructions | Comportement par défaut, conventions | Prompt de l'outil, CLAUDE.md, AGENTS.md ([chapitre 03](03-prompting-pour-agents.md)) |
| Outils | Capacité d'agir | Lecture, édition, Bash, recherche web, MCP |
| Gestion du contexte | Ce que voit le modèle à chaque tour | Compaction, divulgation progressive, subagents ([chapitre 02](02-ingenierie-du-contexte.md)) |
| Permissions | Ce que l'agent a le droit de faire sans demander | Modes, règles allow/ask/deny ([chapitre 10](10-securite.md)) |
| Contrôles déterministes | Ce qui doit arriver à coup sûr | Hooks ([chapitre 07](07-hooks-et-garde-fous.md)) |
| Capteurs | Ce qui prouve que le résultat est correct | Tests, linters, revue indépendante ([chapitre 09](09-verification-et-evaluation.md)) |

On distingue utilement le **harnais de l'éditeur** (ce que fournit Claude Code, Codex ou Copilot) et le **harnais de l'utilisateur** (ce que l'équipe ajoute : instructions, skills, hooks, tests). Böckeler définit l'ingénierie du harnais de l'utilisateur comme « a specific form of context engineering » [3].

### Choisir le niveau d'autonomie

Anthropic recommande de chercher « the simplest solution possible » et de n'ajouter de complexité que si elle améliore mesurablement le résultat [1]. Les motifs qu'elle décrit vont du plus contraint au plus autonome : enchaînement de prompts, routage, parallélisation, orchestrateur et exécutants, évaluateur-optimiseur, puis agent autonome [1]. Pour le code, l'orchestrateur-exécutants convient quand le nombre de fichiers à modifier dépend de la tâche [1] ; l'évaluateur-optimiseur est le schéma de la boucle « implémenter puis relire ».

Cet article de décembre 2024 porte une note de l'éditeur signalant que l'outillage a changé depuis [1] ; ses principes restent cités, ses exemples d'outillage sont datés.

### Pourquoi la boucle échoue

| Échec | Mécanisme | Parade |
|---|---|---|
| Arrêt prématuré | Le modèle juge la tâche finie sans preuve | Capteur exécuté à la fin (hook `Stop`), critères d'acceptation explicites |
| Boucle stérile | Tentatives répétées sans progrès [4] | Plafond de tours, retour à l'humain, session neuve |
| Dérive de périmètre | Fonctionnalités non demandées [4] | Spec bornée, revue contre la spec |
| Triche | Tests désactivés ou affaiblis [4] ; code ajusté aux seules entrées de test [5] | Interdiction explicite, revue des tests, capteurs hors de portée de l'agent |
| Erreur propagée | Une observation erronée est tenue pour vraie (empoisonnement du contexte) | Voir [chapitre 02](02-ingenierie-du-contexte.md) |
| Action dangereuse | Commande destructrice, fuite de données | Permissions, bac à sable, hooks ([chapitre 10](10-securite.md)) |

Le guide de prompting d'Anthropic consacre des consignes spécifiques à plusieurs de ces échecs, par exemple : « Do not hard-code values or create solutions that only work for specific test inputs » [5].

### Le harnais vieillit

Anthropic observe que les harnais « encode assumptions about what Claude can't do », et que ces hypothèses deviennent caduques : un mécanisme de réinitialisation du contexte nécessaire avec un modèle est devenu un poids mort avec le suivant [6]. L'expérience de Naresh Jain va dans le même sens : un harnais lourd est décisif pour un modèle moins capable et inutile, voire coûteux, pour un modèle plus capable [7]. Un harnais doit donc être réévalué à chaque changement de modèle, et ses composants justifiés par un échec observé plutôt que par principe.

## Bonnes pratiques

1. **Partir du plus simple** : un agent unique, outils standards, puis ajouter un composant de harnais en réponse à un échec observé [1].
2. **Doter chaque boucle d'un capteur exécutable** : sans signal pass/fail, l'agent décide seul qu'il a fini [8].
3. **Séparer guides et capteurs** dans sa réflexion : une consigne (guide) n'est pas une garantie ; seul un capteur vérifie [3].
4. **Préférer les capteurs calculatoires** quand ils existent ; réserver les capteurs inférentiels à ce qu'aucun outil déterministe ne mesure [3].
5. **Réévaluer le harnais à chaque changement de modèle** [6], [7].

## Pièges et anti-patterns

- **Le multi-agents par principe** : complexité et coût sans gain démontré pour la tâche (voir [chapitre 06](06-subagents-et-orchestration.md)).
- **Croire le compte rendu de l'agent** plutôt que la sortie des outils.
- **Le harnais fossile** : des contournements conçus pour un ancien modèle qui brident le nouveau [6].
- **Confondre autonomie et absence de contrôle** : plus l'agent est autonome, plus les capteurs et les permissions comptent.

## État du débat

- **Combien de harnais ?** **Contesté.** L'équipe OpenAI qui a construit un produit sans code écrit à la main investit massivement dans le harnais (documentation versionnée, linters sur mesure, agents de nettoyage) [9] ; Jain montre que le bénéfice dépend du modèle [7]. Les deux positions sont compatibles : le harnais nécessaire diminue avec la capacité du modèle, sans disparaître pour les capteurs de comportement [7].
- **Vocabulaire** : « harnais », « scaffold » et « agent » recouvrent des périmètres variables selon les auteurs ; Böckeler reconnaît resserrer volontairement le terme [3]. **Émergent.**

## Dans ce dépôt

- **Composants** : le découpage du système en guides (skills du plugin [`workflow`](../plugins/workflow/)) et capteurs (hooks du plugin [`garde-fous`](../plugins/garde-fous/), subagent relecteur) suit le cadre de ce chapitre.
- **Labs** : voir le [lab 01](../labs/README.md).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic (Schluntz, Zhang), *Building effective agents*, 19/12/2024 (note de l'éditeur : outillage daté). <https://www.anthropic.com/engineering/building-effective-agents>
2. **[P]** Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, arXiv 2210.03629, 2022 (ICLR 2023). <https://arxiv.org/abs/2210.03629>
3. **[P]** Böckeler, *Harness engineering for coding agent users*, 02/04/2026. <https://www.martinfowler.com/articles/harness-engineering.html>
4. **[P]** Beck, *Augmented Coding: Beyond the Vibes*, 25/06/2025. <https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes>
5. **[O]** Anthropic, *Prompting best practices*. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
6. **[O]** Anthropic (Martin, Cemaj, Cohen), *Scaling Managed Agents: Decoupling the brain from the hands*, 08/04/2026. <https://www.anthropic.com/engineering/managed-agents>
7. **[P]** Jain, *Are Harnesses Worth the Cost?*, 13/10/2026. Expérience unique. <https://martinfowler.com/articles/are-harnesses-worth-the-cost.html>
8. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
9. **[O]** Lopopolo (OpenAI), *Harness engineering: leveraging Codex in an agent-first world*, 11/02/2026. <https://openai.com/index/harness-engineering/>
10. **[P]** SWE-bench, *SWE-bench Verified*. <https://www.swebench.com/verified.html>
