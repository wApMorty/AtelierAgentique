---
chapitre: 09
titre: Vérification et évaluation
statut: brouillon
derniere_revision: 2026-11-27
---

# 09 — Vérification et évaluation

> Produire des preuves que le travail d'un agent est correct, à l'échelle d'un changement comme à l'échelle d'un outil ou d'un workflow.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- distinguer vérification (ce changement est-il correct ?) et évaluation (cet agent, ce skill, ce workflow fonctionnent-ils ?) ;
- combiner capteurs calculatoires et inférentiels ;
- organiser une revue automatique utile et bornée ;
- construire une petite suite d'évaluation et en lire correctement les métriques ;
- lire un score de benchmark avec ses limites.

## Concepts clés

**Capteur calculatoire / inférentiel.** Contrôle déterministe et rapide (tests, linters, typage) d'un côté ; jugement d'un modèle (revue par IA, LLM-juge) de l'autre, plus souple mais non déterministe [1].

**Vocabulaire de l'évaluation** (Anthropic) [2] :

- **tâche** : « a single test with defined inputs and success criteria » ;
- **essai** (*trial*) : une tentative ; on en lance plusieurs car les sorties varient ;
- **évaluateur** (*grader*) : la logique qui note un aspect de la performance ;
- **transcription** : l'enregistrement complet d'un essai ;
- **résultat** (*outcome*) : l'état final de l'environnement, pas ce que l'agent affirme.

**pass@k et pass^k.** pass@k est la probabilité d'au moins un succès en k essais ; pass^k celle que les k essais réussissent tous. Avec 75 % de réussite par essai, pass^3 vaut environ 42 % [2]. Pour un agent qui travaille sans surveillance, c'est pass^k qui compte.

## Mécanismes

### Vérifier un changement

Trois couches, de la plus sûre à la plus souple :

1. **Capteurs calculatoires** : tests, typage, lint, build. Ils constituent la boucle que l'agent exécute lui-même : « Give Claude something it can run that comes back pass or fail » [3].
2. **Revue inférentielle** : un agent relecteur en contexte neuf compare le diff à la spec (voir [chapitre 08](08-workflows-developpement.md)).
3. **Revue humaine**, proportionnée au risque [4].

Böckeler organise les capteurs selon trois cibles : maintenabilité, adéquation à l'architecture, comportement ; elle juge le harnais de comportement « the elephant in the room », car il repose souvent sur des tests eux-mêmes générés par IA [1].

### La qualité des tests

Un test vert ne prouve que ce qu'il vérifie. Deux risques sont propres aux agents :

- **la complicité** : un agent qui écrit le code et ses tests à partir de la même mauvaise lecture produit des tests verts et faux ; le laisser modifier les résultats attendus « can also obscure a defect » [5] ;
- **l'ajustement aux tests** : code qui ne fonctionne que pour les entrées testées, ou tests affaiblis [6], [7].

Le *mutation testing*, qui vérifie que les tests échouent quand le code est altéré, figure dans l'anneau *Adopt* du Radar de Thoughtworks (vol. 35) [8] : c'est un capteur calculatoire de la qualité des tests eux-mêmes.

### Organiser la revue automatique

L'équipe Claude Code décrit un dispositif complet [4] :

- avant la PR, l'agent lance tests, build et linter, puis « a second agent reviews the diff in a fresh context » ;
- les consignes de revue vivent dans CLAUDE.md et un fichier `REVIEW.md` ;
- la revue s'arrête après trois tours sans convergence ;
- des agents de revue parallèles voient leurs constats soumis à des vérificateurs qui votent ;
- une évaluation construite à partir d'incidents passés mesure la revue elle-même.

Elle rapporte un doublement des PR fusionnées et une baisse de plus de 40 % de la part de retours arrière sur la période [4] ; ces chiffres sont auto-déclarés. Elle note aussi qu'environ 59 % des problèmes signalés concernaient du code antérieur à la première passe de revue [4] : un relecteur automatique sans périmètre déborde sur l'existant.

### Évaluer un agent, un skill, un outil

Anthropic recommande, pour les agents de code [2] :

- des évaluateurs **déterministes** autant que possible (tests unitaires, analyse statique), une rubrique notée par un modèle pour la qualité ;
- noter **ce qui est produit**, pas le chemin suivi : imposer un ordre d'étapes rend l'évaluation « overly brittle » ;
- **isoler chaque essai** dans un environnement propre : l'article rapporte un agent avantagé parce qu'il lisait l'historique git des essais précédents ;
- **lire les transcriptions** et durcir les évaluateurs contre les contournements ;
- **commencer petit** : 20 à 50 tâches tirées d'échecs réels.

La même démarche s'applique à un outil MCP [9] ou à un skill : un ensemble de tâches réalistes, plusieurs essais, des métriques de précision, de durée et de tokens.

### Lire un benchmark

SWE-bench Verified est un sous-ensemble de 500 problèmes validés par des annotateurs humains [10]. Ses scores dépendent du harnais utilisé, et le site lui-même prévient que des résultats obtenus avec des versions différentes de son agent de référence « are not necessarily comparable » [10]. Anthropic écrit que les modèles de pointe approchent la saturation au-delà de 80 % [2]. Un score de benchmark renseigne sur le modèle dans un harnais donné, pas sur la performance dans un dépôt particulier.

## Bonnes pratiques

1. **Exiger la sortie des commandes**, pas leur résumé par l'agent [3].
2. **Relire les tests écrits par l'agent** avec plus d'attention que le code : ce sont eux qui définissent « correct ».
3. **Interdire la modification des tests existants** sans demande explicite [6], et faire signaler toute suppression d'assertion par la revue.
4. **Borner la revue automatique** : critères explicites, style exclu, périmètre limité au diff, nombre de tours plafonné [3], [4].
5. **Mesurer pass^k** pour ce qui doit tourner seul [2].
6. **Construire ses évaluations à partir de ses incidents** [2], [4].

## Pièges et anti-patterns

- **« All tests pass »** sans sortie à l'appui.
- **Le relecteur sans consigne** qui trouve toujours quelque chose [3].
- **Le LLM-juge non calibré** : non déterministe et coûteux ; sa notation doit être confrontée à un jugement humain sur un échantillon [2].
- **L'évaluation contaminée** : essais qui partagent un état [2].
- **Le classement de benchmark comme critère de choix d'outil** : il ignore votre dépôt, vos conventions et votre harnais.

## État du débat

- **Revue humaine ou revue par agents ?** **Contesté** ; voir [chapitre 08](08-workflows-developpement.md). L'équipe OpenAI de l'expérience « harness engineering » écrit que les humains peuvent relire les PR « but aren't required to » [11] ; ce choix est propre à son contexte et non mesuré de façon indépendante.
- **Quand faire tourner les capteurs ?** Jain avance que la capacité du modèle change le moment où les capteurs interviennent (pendant le développement ou en barrière finale), pas leur nécessité [5]. Hypothèse non testée au-delà de son expérience. **Émergent.**

## Dans ce dépôt

- **Composants** : hook `Stop` du plugin [`garde-fous`](../plugins/garde-fous/) ; subagent `relecteur` et skill de vérification du plugin [`workflow`](../plugins/workflow/) ; CI du dépôt (lint, liens, manifestes).
- **Labs** : [lab 01](../labs/README.md).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[P]** Böckeler, *Harness engineering for coding agent users*, 02/04/2026. <https://www.martinfowler.com/articles/harness-engineering.html>
2. **[O]** Grace, Hadfield, Olivares, De Jonghe (Anthropic), *Demystifying evals for AI agents*, 09/01/2026. <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
3. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
4. **[O]** Osmani, Lunt, Wang (équipe Claude Code), *How the Claude Code team does code review*, 15/10/2026. Chiffres auto-déclarés. <https://claude.dev/blog/solving-code-review-at-anthropic>
5. **[P]** Jain, *Are Harnesses Worth the Cost?*, 13/10/2026. <https://martinfowler.com/articles/are-harnesses-worth-the-cost.html>
6. **[O]** Anthropic, *Prompting best practices*. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
7. **[P]** Beck, *Augmented Coding: Beyond the Vibes*, 25/06/2025. <https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes>
8. **[P]** Thoughtworks, *Technology Radar*, vol. 35, novembre 2026 (anneaux relevés, fiches non lues). <https://www.thoughtworks.com/radar>
9. **[O]** Aizawa (Anthropic), *Writing effective tools for AI agents*, 11/09/2025. <https://www.anthropic.com/engineering/writing-tools-for-agents>
10. **[P]** SWE-bench, *SWE-bench Verified*. <https://www.swebench.com/verified.html>
11. **[O]** Lopopolo (OpenAI), *Harness engineering: leveraging Codex in an agent-first world*, 11/02/2026. <https://openai.com/index/harness-engineering/>
