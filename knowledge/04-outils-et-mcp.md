---
chapitre: 04
titre: Outils et MCP
statut: relu
derniere_revision: 2026-11-27
---

# 04 — Outils et MCP

> Concevoir des outils qu'un agent utilise bien, connaître le Model Context Protocol tel qu'il est aujourd'hui, et ne brancher un serveur MCP que lorsqu'il apporte plus qu'il ne coûte.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- appliquer les principes de conception d'outils pour agents ;
- décrire l'architecture de MCP, ses primitives et l'état de sa spécification ;
- évaluer le coût en contexte et le risque d'un serveur MCP avant de l'installer ;
- choisir entre un outil MCP, une commande shell, un script appelé par un skill et l'exécution de code.

## Concepts clés

**Outil.** Fonction exposée au modèle par un nom, une description et un schéma d'entrée. Le modèle choisit l'outil et ses arguments ; le harnais l'exécute.

**MCP (Model Context Protocol).** Standard ouvert de connexion entre applications d'IA et systèmes externes [1]. Un **client** (Claude Code, Codex, Copilot…) se connecte à des **serveurs** qui exposent des primitives. Le projet relève de LF Projects, LLC, structure de la Linux Foundation, avec des mainteneurs nommés à titre individuel [2].

**Primitives serveur** : *tools* (fonctions exécutées par le modèle), *resources* (données), *prompts* (gabarits) [1]. **Primitive client** : *elicitation* (demande d'information à l'utilisateur) [1].

## Mécanismes

### Concevoir un outil pour un agent

Anthropic pose que les outils doivent être conçus pour des agents, pas comme des fonctions ou des API destinées à des développeurs [3]. Principes [3] :

- **Consolider** : un outil `schedule_event` vaut mieux que trois outils `list_users`, `list_events`, `create_event` que l'agent doit enchaîner.
- **Nommer par espace** : préfixer par service et ressource (`asana_projects_search`) pour lever les ambiguïtés entre outils voisins.
- **Renvoyer du signal** : un paramètre `response_format` (concis ou détaillé) ; dans l'exemple de l'article, la réponse concise coûte 72 tokens contre 206 pour la détaillée.
- **Économiser les tokens** : pagination, filtrage, troncature ; Claude Code plafonne par défaut une réponse d'outil à 25 000 tokens [3].
- **Des erreurs exploitables** : un message qui dit quoi corriger, pas un code opaque.
- **Soigner les descriptions** : ce sont des prompts. L'article rapporte qu'un outil de recherche ajoutait « 2025 » aux requêtes jusqu'à ce que sa description soit corrigée.

La méthode recommandée est empirique : prototyper, écrire des tâches d'évaluation réalistes à plusieurs étapes, lire les transcriptions, mesurer précision, durée, nombre d'appels, tokens et erreurs, puis faire réécrire les outils par un agent [3] (voir [chapitre 09](09-verification-et-evaluation.md)).

### MCP aujourd'hui

La version courante de la spécification est la révision `2026-07-28`, qui succède à `2025-11-25` [4] **(Daté)**. Ses changements majeurs [4] :

- **Protocole sans état** : la poignée de main `initialize` et l'en-tête de session disparaissent ; chaque requête porte sa version et ses capacités.
- **Dépréciation** de *roots*, *sampling* et *logging* au profit de mécanismes plus simples (paramètres d'outil, appel direct d'une API de modèle, journalisation sur stderr ou OpenTelemetry).
- **Transports** : stdio et Streamable HTTP ; l'ancien HTTP+SSE est déprécié.
- **Extensions** négociées : tâches longues, skills via MCP, applications MCP, registre.

L'autorisation, optionnelle, s'appuie sur OAuth 2.1 : le serveur est un serveur de ressources, et il « MUST validate that access tokens were issued specifically for them » [5].

### MCP dans Claude Code

Trois portées de configuration : locale (par défaut), projet (fichier `.mcp.json` versionné), utilisateur ; un plugin peut aussi embarquer ses serveurs [6]. Les définitions d'outils MCP sont **différées par défaut** et chargées à la demande par *tool search* : seuls les noms et les instructions des serveurs occupent le contexte au démarrage [6], [7]. Une réponse MCP est plafonnée par défaut à 25 000 tokens [6] **(Daté)**.

### Le coût caché des outils

Chaque outil a un coût en contexte et un coût en décision. Anthropic décrit deux problèmes à grande échelle : les définitions chargées d'avance (des centaines de milliers de tokens avec des milliers d'outils) et les résultats intermédiaires qui transitent deux fois par le contexte [8]. Sa proposition, l'**exécution de code** : présenter les serveurs MCP comme une arborescence de modules que l'agent importe dans du code, de sorte que les données volumineuses restent hors du contexte. Dans l'exemple donné, un transfert de document passe de 150 000 à 2 000 tokens [8] ; ce chiffre illustre un cas, ce n'est pas une mesure générale. La contrepartie est explicite : exécuter du code généré exige un environnement isolé [8].

Côté décision, la multiplication des outils dégrade le choix d'outil (confusion de contexte) [9].

### Choisir le bon véhicule

| Besoin | Véhicule préférable | Raison |
|---|---|---|
| Commande disponible en CLI (git, gh, npm) | Bash | Aucun coût de contexte supplémentaire ; le modèle connaît déjà l'outil |
| Procédure répétable avec scripts | Skill avec scripts ([chapitre 05](05-skills.md)) | Divulgation progressive ; le script s'exécute sans entrer dans le contexte |
| Service distant authentifié, sans CLI | Serveur MCP | Authentification OAuth, découverte standard |
| Traitement de gros volumes de données | Exécution de code | Les données restent hors du contexte [8] |

## Bonnes pratiques

1. **N'installer un serveur MCP qu'après avoir vérifié qu'aucune CLI ne couvre le besoin.**
2. **Préférer la portée projet** (`.mcp.json`) pour ce que l'équipe partage, et la relire en revue comme du code [6].
3. **Concevoir peu d'outils, consolidés, bien nommés** [3].
4. **Mesurer** : un outil se valide sur des tâches réelles, pas sur sa description [3].
5. **Limiter les portées OAuth** : pas de « full-access » quand une portée restreinte suffit [10].

## Pièges et anti-patterns

- **Le serveur « au cas où »** : coût en contexte et surface d'attaque sans usage.
- **L'API REST exposée telle quelle** : des dizaines d'outils fins que l'agent doit orchestrer, au lieu de quelques outils orientés tâche [3].
- **La réponse exhaustive** : un outil qui renvoie des milliers de lignes remplit le contexte [3].
- **Faire confiance à la description d'un outil tiers** : elle peut contenir des instructions cachées (*tool poisoning*) ou changer après approbation (*rug pull*) [11] ; voir [chapitre 10](10-securite.md).
- **Le jeton relayé** (*token passthrough*) : un serveur qui accepte ou transmet des jetons qui ne lui étaient pas destinés, explicitement qualifié d'anti-pattern par la spécification [10].

## État du débat

- **MCP ou CLI ?** **Émergent.** La documentation d'Anthropic sur l'exécution de code [8] et la pratique répandue de faire appeler `gh` ou `kubectl` directement par l'agent relativisent l'intérêt de serveurs MCP pour les outils déjà scriptables ; MCP garde l'avantage pour l'authentification et les services sans CLI.
- **Stabilité du protocole** : la révision `2026-07-28` a cassé la compatibilité (suppression des sessions, dépréciations) [4] ; un serveur maintenu doit suivre ces évolutions. **Daté.**

## Dans ce dépôt

- **Composants** : aucun serveur MCP n'est embarqué dans les plugins ; la justification figure dans le README du plugin [`workflow`](../plugins/workflow/) : les besoins couverts (git, GitHub, recherche web) le sont par des CLI et des outils intégrés.
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Model Context Protocol, page d'accueil et spécification. <https://modelcontextprotocol.io/specification/latest>
2. **[O]** Model Context Protocol, *Governance*. <https://modelcontextprotocol.io/community/governance>
3. **[O]** Aizawa (Anthropic), *Writing effective tools for AI agents*, 11/09/2025. <https://www.anthropic.com/engineering/writing-tools-for-agents>
4. **[O]** Model Context Protocol, *Changelog* de la révision 2026-07-28 (date de publication non indiquée). <https://modelcontextprotocol.io/specification/2026-07-28/changelog>
5. **[O]** Model Context Protocol, *Authorization*, révision 2026-07-28. <https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization>
6. **[O]** Anthropic, *MCP* (Claude Code). <https://code.claude.com/docs/en/mcp>
7. **[O]** Anthropic, *How Claude Code works*. <https://code.claude.com/docs/en/how-claude-code-works>
8. **[O]** Jones, Kelly (Anthropic), *Code execution with MCP*, 04/11/2025. <https://www.anthropic.com/engineering/code-execution-with-mcp>
9. **[P]** Breunig, *How Long Contexts Fail*, 22/06/2025. <https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html>
10. **[O]** Model Context Protocol, *Security Best Practices*. <https://modelcontextprotocol.io/specification/latest/basic/security_best_practices>
11. **[P]** Beurer-Kellner, Fischer (Invariant Labs), *MCP Security Notification: Tool Poisoning Attacks*, 01/04/2025. Éditeur d'une solution de protection. <https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks>
