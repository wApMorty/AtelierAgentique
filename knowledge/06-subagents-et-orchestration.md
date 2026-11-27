---
chapitre: 06
titre: Subagents et orchestration
statut: relu
derniere_revision: 2026-11-27
---

# 06 — Subagents et orchestration

> Déléguer une sous-tâche à un agent qui travaille dans sa propre fenêtre, en sachant ce que l'on y gagne, ce que l'on y perd, et quand il vaut mieux ne pas le faire.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- décrire le fonctionnement d'un subagent dans Claude Code et le format de sa définition ;
- identifier les tâches qui se prêtent à la délégation et celles qui ne s'y prêtent pas ;
- concevoir un subagent : rôle, outils, modèle, format de retour ;
- organiser du travail parallèle sans conflit ;
- situer le débat sur les systèmes multi-agents.

## Concepts clés

**Subagent.** Agent lancé par l'agent principal, avec son propre prompt système, ses propres outils et sa propre fenêtre de contexte ; seul son résultat final revient à l'appelant [1], [2].

**Fork.** Variante qui démarre avec une copie de la conversation en cours ; ses appels d'outils restent également hors du contexte principal [2].

**Orchestrateur-exécutants.** Motif où un agent central découpe une tâche, délègue les morceaux et synthétise les résultats [3].

## Mécanismes

### Définition d'un subagent dans Claude Code

Un subagent est un fichier Markdown à frontmatter YAML, dont le corps est le prompt système [1]. Seuls `name` et `description` sont requis ; les champs utiles incluent `tools` (liste blanche ; omis, il hérite des outils de l'appelant), `disallowedTools`, `model`, `effort`, `permissionMode`, `skills`, `memory`, `isolation: worktree` et `background` [1].

Emplacements, du plus prioritaire au moins prioritaire : réglages gérés, option `--agents`, `.claude/agents/` du projet, `~/.claude/agents/` de l'utilisateur, répertoire `agents/` d'un plugin [1]. Les subagents de plugin ignorent `hooks`, `mcpServers` et `permissionMode`, « for security reasons » [1].

Les subagents intégrés Explore et Plan sont en lecture seule et démarrent sans les fichiers CLAUDE.md [1], [4]. Un subagent peut en lancer d'autres, dans une limite de profondeur configurable ; retirer l'outil `Agent` de sa liste l'en empêche [1] **(Daté)**.

### Ce que l'on gagne

- **Un contexte principal préservé** : les lectures et sorties d'outils du subagent n'y entrent pas [4] (voir [chapitre 02](02-ingenierie-du-contexte.md)).
- **Un regard indépendant** : un relecteur qui n'a pas vu la production n'en partage pas les présupposés ; c'est le fondement de la revue en contexte neuf (voir [chapitre 08](08-workflows-developpement.md)).
- **Un moindre privilège** : un subagent de revue limité à `Read, Grep, Glob` ne peut rien modifier [5].
- **Un modèle adapté** : Anthropic juge Haiku adapté aux subagents qui accomplissent des tâches simples [5].

### Ce que l'on perd

- **Du contexte** : le subagent ne voit pas la conversation ; son prompt doit être autoporteur ([chapitre 03](03-prompting-pour-agents.md)).
- **De l'information** : le résumé renvoyé est une compression avec perte.
- **Des tokens** : chaque subagent consomme son propre budget ; dans le système de recherche d'Anthropic, un système multi-agents consomme environ 15 fois plus de tokens qu'une conversation [3].
- **De la cohérence** : des agents qui écrivent en parallèle prennent des décisions implicites incompatibles [6].

### Paralléliser l'écriture

Pour des modifications en parallèle, l'isolation du contexte ne suffit pas : il faut isoler le système de fichiers. Claude Code propose des sessions dans des worktrees Git (`claude --worktree <nom>`) et un champ `isolation: worktree` pour les subagents [1], [7]. Les conditions de rentabilité sont détaillées au [chapitre 08](08-workflows-developpement.md) : tâches indépendantes, vérification propre à chacune, capacité de revue suffisante.

## Bonnes pratiques

1. **Déléguer la lecture, garder l'écriture** : exploration, recherche documentaire, analyse de journaux et revue sont de bons candidats ; l'écriture de parties interdépendantes ne l'est pas [3], [6].
2. **Un rôle par subagent**, décrit dans `description` de façon à guider le choix de l'agent principal.
3. **Des outils minimaux** : liste blanche explicite ; aucun droit d'écriture pour un relecteur ou un chercheur [5].
4. **Un format de retour imposé** : structure et longueur maximale, pour que la synthèse n'encombre pas le contexte principal. Anthropic cite des synthèses de 1 000 à 2 000 tokens [8].
5. **Un modèle proportionné** : un modèle léger pour l'exploration simple, le modèle principal pour le jugement [5].
6. **Des descriptions courtes** : elles occupent le contexte de chaque session ; Claude Code avertit au-delà de 15 000 tokens cumulés [1].

## Pièges et anti-patterns

- **L'agent sans rôle** : un subagent « assistant général » dupliqué n'apporte qu'un coût.
- **La délégation de l'essentiel** : confier à un subagent la décision qui demande tout le contexte de la session.
- **L'éventail systématique** : lancer plusieurs agents en parallèle par habitude, au prix d'un multiplicateur de tokens [3], incompatible avec un quota limité ([chapitre 11](11-couts-quotas-modeles.md)).
- **Le relecteur qui hérite de tout** : un subagent de revue lancé avec l'historique complet (fork) perd son indépendance.
- **Les agents parallèles sur les mêmes fichiers** : conflits garantis sans worktrees [9].

## État du débat

**Contesté : faut-il des systèmes multi-agents ?** Cognition défend des agents mono-fil qui partagent tout leur contexte, et souligne que les subagents de Claude Code répondent à des questions étroites sans écrire de code en parallèle [6]. Anthropic rapporte un gain de 90,2 % d'un système multi-agents sur son évaluation interne de recherche, mais note que les tâches nécessitant un contexte partagé s'y prêtent mal et que le code offre moins de parallélisme réel que la recherche [3]. Thoughtworks place l'usage de subagents pour mieux gérer le contexte en *Trial* dans le volume 35 de son Radar [10]. La position la mieux étayée : subagents pour isoler la lecture et le jugement, agent unique pour l'écriture cohérente.

## Dans ce dépôt

- **Composants** : le plugin [`workflow`](../plugins/workflow/) définit deux subagents seulement, `relecteur` (revue indépendante, lecture seule) et `chercheur` (recherche documentaire, lecture seule) ; tout autre agent devra justifier un rôle non couvert.
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic, *Subagents*. <https://code.claude.com/docs/en/sub-agents>
2. **[O]** Anthropic, *How Claude Code works*. <https://code.claude.com/docs/en/how-claude-code-works>
3. **[O]** Anthropic (Hadfield et al.), *How we built our multi-agent research system*, 13/06/2025. Évaluations internes. <https://www.anthropic.com/engineering/multi-agent-research-system>
4. **[O]** Anthropic, *Context window*. <https://code.claude.com/docs/en/context-window>
5. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
6. **[P]** Yan (Cognition), *Don't Build Multi-Agents*, 12/06/2025. <https://cognition.com/blog/dont-build-multi-agents>
7. **[O]** Anthropic, *Common workflows*. <https://code.claude.com/docs/en/common-workflows>
8. **[O]** Anthropic, *Effective context engineering for AI agents*, 29/09/2025. <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
9. **[O]** OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
10. **[P]** Thoughtworks, *Technology Radar*, vol. 35, novembre 2026 (anneaux relevés, fiches non lues). <https://www.thoughtworks.com/radar>
