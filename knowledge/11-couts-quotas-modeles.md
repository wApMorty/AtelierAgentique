---
chapitre: 11
titre: Coûts, quotas et modèles
statut: brouillon
derniere_revision: 2026-11-27
---

# 11 — Coûts, quotas et modèles

> Savoir où partent les tokens d'une session d'agent, et arbitrer modèle, effort, délégation et cache pour tenir un budget sans sacrifier la qualité.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- expliquer pourquoi le coût d'une session croît plus vite que sa durée ;
- décrire les limites d'usage d'un abonnement et leur partage entre outils ;
- utiliser le cache de préfixe à son avantage ;
- choisir modèle et effort selon la tâche ;
- estimer le surcoût d'un subagent ou d'un système multi-agents.

## Concepts clés

**Tokens d'entrée et de sortie.** Un agent renvoie toute la conversation à chaque requête : « Claude Code sends your full conversation with every request » [1]. Les tokens d'entrée dominent ; Manus rapporte un rapport entrée/sortie d'environ 100 pour 1 dans son système [2].

**Cache de préfixe.** Les tokens d'entrée identiques à une requête récente sont facturés beaucoup moins cher ; Manus cite un écart de 1 à 10 sur les tarifs qu'il utilisait [2] (voir [chapitre 02](02-ingenierie-du-contexte.md)).

**Effort.** Niveau de raisonnement demandé au modèle (`low` à `max` dans Claude Code) ; il augmente la qualité sur les tâches difficiles et la consommation sur toutes [3].

## Mécanismes

### Pourquoi une session coûte de plus en plus cher

Chaque tour renvoie l'historique complet ; le coût d'un tour croît donc avec la longueur de la session, et celui de la session croît plus vite que linéairement. « Token costs scale with context size » [1]. D'où la règle la plus rentable : `/clear` entre deux tâches sans lien, qui « costs nothing » [1].

### Limites d'un abonnement

Les offres Pro et Max de Claude ont une limite par session de cinq heures et une limite hebdomadaire, partagées entre Claude et Claude Code : « all activity in both tools counts against the same limits » [4]. Aucun chiffre de quota n'est publié [4] **(Daté)**. Les exécutions planifiées dans le cloud consomment ce même quota [5]. `/usage` affiche le coût de la session, l'état des limites et une ligne sur le cache [1].

### Le cache, levier principal

Le cache est préfixe et exact ; dans le cadre d'un abonnement, la conversation principale bénéficie d'une durée de vie d'une heure, contre cinq minutes avec une clé d'API ou des crédits, et cinq minutes par défaut pour les subagents [6] **(Daté)**. Invalident le cache : changement de modèle, d'effort sur la plupart des modèles, mode rapide, compaction, ajout ou retrait d'outils quand *tool search* est désactivé [6]. Conséquences pratiques :

- choisir modèle et effort **en début de session** ;
- reprendre une session dans l'heure plutôt que le lendemain si l'on veut profiter du cache ;
- préférer `/clear` à une compaction quand la suite n'a pas besoin de l'historique : la compaction relit tout l'historique pour le résumer [6].

### Modèle et effort

Anthropic indique un effort par défaut `medium` pour les modèles de la génération 5.x et réserve les niveaux supérieurs aux tâches qui le justifient ; `ultrathink` relève l'effort pour un seul tour [3] **(Daté)**. Pour les subagents, l'éditeur juge un modèle léger adapté aux tâches simples [3]. L'arbitrage raisonnable :

| Tâche | Modèle | Effort |
|---|---|---|
| Exploration, recherche de fichiers, synthèse | Léger | Bas |
| Implémentation courante | Principal | Défaut |
| Conception, débogage difficile, revue de sécurité | Principal | Élevé |

### Le coût de la délégation

Un subagent a sa propre fenêtre et, par défaut, une durée de cache de cinq minutes [6]. Dans le système de recherche d'Anthropic, un agent consomme environ 4 fois plus de tokens qu'une conversation, un système multi-agents environ 15 fois plus [7]. L'expérience de Jain montre un harnais qui multiplie les tokens par environ 10,5 sans gain avec un modèle performant [8]. La délégation se justifie quand elle **économise** du contexte principal (lecture volumineuse résumée) ou apporte une **indépendance** de jugement ; pas par défaut.

### Coût en contexte des extensions

Fichiers d'instructions, descriptions de skills et de subagents, noms d'outils MCP sont payés à chaque requête ([chapitre 02](02-ingenierie-du-contexte.md)). Une étude mesure un surcoût d'inférence de plus de 20 % lié aux fichiers d'instructions de dépôt, sans gain général de réussite [9].

## Bonnes pratiques

1. **Une session par tâche**, `/clear` entre deux [1].
2. **Modèle et effort fixés en début de session** [6].
3. **Subagents légers pour la lecture**, avec format de retour court [3].
4. **Pas d'éventail d'agents** sans gain attendu explicite.
5. **Surveiller `/usage` et `/context`** plutôt que deviner [1].
6. **Plafonner les exécutions autonomes** en tours et en budget ([chapitre 12](12-execution-autonome.md)).

## Pièges et anti-patterns

- **La session fleuve** : chaque tour coûte l'historique entier.
- **Changer de modèle en cours de route** sans nécessité : cache perdu [6].
- **L'effort maximal par défaut** sur des tâches simples.
- **Le multi-agents pour « aller plus vite »** sur un quota limité.
- **Les extensions dormantes** qui pèsent sur chaque requête.

## État du débat

- **Harnais lourd et modèle léger, ou l'inverse ?** Jain observe qu'un modèle moins capable bien harnaché peut revenir moins cher qu'un modèle performant sans harnais pour un même taux de réussite [8]. Expérience unique, non généralisable selon l'auteur. **Émergent.**
- **Opacité des quotas** : l'absence de chiffres publiés [4] oblige à mesurer empiriquement ; aucun praticien consulté ne propose de méthode établie.

## Dans ce dépôt

- **Composants** : budget plafonné de la veille ([ADR-004](../docs/decisions/ADR-004-architecture-veille.md)) ; parallélisation non systématique ([ADR-001](../docs/decisions/ADR-001-workflow-developpement.md)) ; subagent `chercheur` sur modèle léger.
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic, *Manage costs effectively*. <https://code.claude.com/docs/en/costs>
2. **[P]** Ji (Manus), *Context Engineering for AI Agents: Lessons from Building Manus*, 18/07/2025. Chiffres auto-déclarés. <https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus>
3. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
4. **[O]** Anthropic, *Using Claude Code with your Pro or Max plan*. <https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan>
5. **[O]** Anthropic, *Automate work with scheduled tasks*. <https://code.claude.com/docs/en/routines>
6. **[O]** Anthropic, *Prompt caching* (Claude Code). <https://code.claude.com/docs/en/prompt-caching>
7. **[O]** Anthropic (Hadfield et al.), *How we built our multi-agent research system*, 13/06/2025. <https://www.anthropic.com/engineering/multi-agent-research-system>
8. **[P]** Jain, *Are Harnesses Worth the Cost?*, 13/10/2026. <https://martinfowler.com/articles/are-harnesses-worth-the-cost.html>
9. **[P]** Gloaguen et al., *Evaluating AGENTS.md*, arXiv 2602.11988, v3 du 29/09/2026 (résumé lu). <https://arxiv.org/abs/2602.11988>
