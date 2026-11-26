# Glossaire

Définitions courtes ; le chapitre indiqué détaille et source chaque notion.

| Terme | Définition | Chapitre |
|---|---|---|
| AGENTS.md | Fichier Markdown d'instructions pour agents de code, standard ouvert porté par l'Agentic AI Foundation | [13](13-portabilite-et-standards.md) |
| Agent | Système où un modèle dirige lui-même son processus et l'usage de ses outils, par opposition à un workflow à chemins prédéfinis | [01](01-fondamentaux-boucle-agentique.md) |
| Agent Skills | Format ouvert de skills (`SKILL.md` et ressources) lisible par plusieurs outils | [05](05-skills.md) |
| Bac à sable (*sandbox*) | Isolation imposée par le système d'exploitation aux commandes de l'agent (fichiers, réseau) | [10](10-securite.md) |
| Boucle agentique | Cycle raisonnement, action, observation, répété jusqu'à la fin de la tâche | [01](01-fondamentaux-boucle-agentique.md) |
| Cache de préfixe | Réutilisation du calcul sur un début de requête identique ; réduit coût et latence | [02](02-ingenierie-du-contexte.md), [11](11-couts-quotas-modeles.md) |
| Capteur (*sensor*) | Contrôle qui observe le résultat après l'action de l'agent : tests, linters, revue | [01](01-fondamentaux-boucle-agentique.md), [09](09-verification-et-evaluation.md) |
| Compaction | Remplacement de l'historique par un résumé quand la fenêtre approche de sa limite | [02](02-ingenierie-du-contexte.md) |
| Context rot | Dégradation des performances d'un modèle quand la longueur de l'entrée augmente | [02](02-ingenierie-du-contexte.md) |
| Divulgation progressive | Chargement d'une description courte d'abord, du contenu complet seulement à l'usage | [02](02-ingenierie-du-contexte.md), [05](05-skills.md) |
| Effort | Niveau de raisonnement demandé au modèle | [11](11-couts-quotas-modeles.md) |
| Évaluateur (*grader*) | Logique qui note un aspect de la performance d'un agent lors d'une évaluation | [09](09-verification-et-evaluation.md) |
| Fenêtre de contexte | Ensemble des tokens transmis au modèle à chaque requête | [02](02-ingenierie-du-contexte.md) |
| Fork | Subagent démarré avec une copie de la conversation en cours | [06](06-subagents-et-orchestration.md) |
| Guide | Élément qui oriente l'agent avant l'action : instructions, spec, plan | [01](01-fondamentaux-boucle-agentique.md) |
| Harnais (*harness*) | Ce qui entoure le modèle pour en faire un agent : prompts, outils, contexte, permissions, contrôles | [01](01-fondamentaux-boucle-agentique.md) |
| Hook | Programme déclenché par l'outil à un événement de son cycle de vie, qui peut bloquer ou compléter une action | [07](07-hooks-et-garde-fous.md) |
| Injection de prompt | Instructions malveillantes cachées dans un contenu lu par l'agent | [10](10-securite.md) |
| Ingénierie du contexte | Choix de ce qui entre dans la fenêtre de contexte à chaque étape | [02](02-ingenierie-du-contexte.md) |
| Marketplace | Catalogue de plugins Claude Code installable par `/plugin marketplace add` | [13](13-portabilite-et-standards.md) |
| MCP | Model Context Protocol, standard de connexion entre applications d'IA et systèmes externes | [04](04-outils-et-mcp.md) |
| Mode plan | Mode où l'agent explore et propose sans rien modifier | [08](08-workflows-developpement.md) |
| pass@k / pass^k | Probabilité d'au moins un succès en k essais / de k succès sur k essais | [09](09-verification-et-evaluation.md) |
| Plugin | Paquet distribuable de skills, agents, hooks et serveurs MCP pour Claude Code | [13](13-portabilite-et-standards.md) |
| Revue indépendante | Relecture par un agent ou un humain qui n'a pas participé à la production | [08](08-workflows-developpement.md), [09](09-verification-et-evaluation.md) |
| Skill | Répertoire contenant un `SKILL.md`, chargé à la demande pour une procédure donnée | [05](05-skills.md) |
| Spec-driven development | Approche où une spécification écrite précède et guide l'implémentation | [08](08-workflows-developpement.md) |
| Subagent | Agent lancé par l'agent principal, dans sa propre fenêtre, qui ne renvoie que son résultat | [06](06-subagents-et-orchestration.md) |
| Tâche planifiée | Exécution d'agent déclenchée selon un calendrier, dans le cloud | [12](12-execution-autonome.md) |
| Tool poisoning | Instructions malveillantes cachées dans la description d'un outil | [04](04-outils-et-mcp.md), [10](10-securite.md) |
| Tool search | Chargement à la demande des définitions d'outils MCP | [02](02-ingenierie-du-contexte.md), [04](04-outils-et-mcp.md) |
| Triade létale | Accès aux données privées, exposition à du contenu non fiable, sortie vers l'extérieur : combinaison qui permet l'exfiltration | [10](10-securite.md) |
| Worktree | Copie de travail Git séparée, utilisée pour isoler des sessions parallèles | [06](06-subagents-et-orchestration.md), [08](08-workflows-developpement.md) |
