---
chapitre: 10
titre: Sécurité
statut: brouillon
derniere_revision: 2026-11-27
---

# 10 — Sécurité

> Un agent de code exécute des commandes avec vos droits en lisant du contenu que vous ne contrôlez pas : la sécurité se raisonne en couches, en partant de l'hypothèse que l'injection de prompt réussira.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- expliquer pourquoi l'injection de prompt n'a pas de parade fiable au niveau du modèle ;
- appliquer le critère de la « triade létale » à une configuration d'agent ;
- configurer permissions, modes et bac à sable de Claude Code en connaissant ce que chacun garantit ;
- évaluer le risque d'un serveur MCP, d'un plugin ou d'un skill tiers ;
- protéger les secrets dans un dépôt travaillé par un agent.

## Concepts clés

**Injection de prompt.** Instructions malveillantes placées dans un contenu que l'agent lit (page web, issue, fichier, description d'outil) et que le modèle suit comme si elles venaient de l'utilisateur.

**Triade létale.** Simon Willison nomme ainsi la combinaison de trois capacités : accès à des données privées, exposition à du contenu non fiable, capacité de communiquer vers l'extérieur ; réunies, elles permettent à un attaquant de faire exfiltrer des données par l'agent [1].

**Défense en profondeur.** Superposition de contrôles indépendants, de sorte que la défaillance de l'un ne suffise pas.

## Mécanismes

### Pourquoi le modèle ne suffit pas

Willison rappelle que l'on ne sait toujours pas empêcher l'injection de prompt de façon fiable à 100 %, et se dit « deeply suspicious » des produits de filtrage qui revendiquent 95 % d'attaques détectées : en sécurité applicative, c'est une note éliminatoire [1]. Anthropic écrit de même que « no system is completely immune to all attacks » [2]. La seule défense côté utilisateur, selon Willison, est d'éviter de réunir les trois éléments de la triade [1].

### Surfaces d'attaque d'un agent de code

| Surface | Exemple de vecteur |
|---|---|
| Contenu lu | Page web, issue GitHub, commentaire de code, journal |
| Outils tiers | Description d'outil MCP contenant des instructions cachées (*tool poisoning*), description modifiée après approbation (*rug pull*), outil qui altère le comportement d'un autre (*shadowing*) [3] |
| Extensions | Skill ou plugin qui embarque des scripts ou des instructions d'exfiltration [4] |
| Configuration du dépôt | `.mcp.json`, hooks, réglages de projet introduits par une PR |
| Commandes | Commande destructrice, téléchargement et exécution de code |

L'OWASP a publié en décembre 2025 un Top 10 dédié aux applications agentiques, élaboré avec plus de cent contributeurs [5] ; la liste détaillée de ses dix risques n'a pas pu être lue pour ce chapitre **(Non vérifié)**.

### Les couches de Claude Code

| Couche | Ce qu'elle garantit | Ce qu'elle ne garantit pas |
|---|---|---|
| **Règles de permission** `allow` / `ask` / `deny` | Évaluées dans l'ordre deny, ask, allow ; « An allow rule can't carve an exception out of a deny rule » ; appliquées par l'outil, pas par le modèle [6] | Une règle sur Bash porte sur le texte de la commande : `Bash(curl *)` n'arrête ni `/usr/bin/curl` ni `sh -c 'curl …'` [6] |
| **Modes** | Manuel (demande avant d'agir), `acceptEdits`, `plan`, `auto` (un classifieur revoit les actions), `dontAsk` (refuse tout ce qui demanderait), `bypassPermissions` [7] | `auto` « reduces permission prompts but does not guarantee safety » [7] ; `bypassPermissions` n'offre aucune protection |
| **Bac à sable** du système | Isolation du shell : écriture limitée au projet et au temporaire, réseau sortant par un proxy filtré par domaine [8] | Ne couvre que les commandes shell : « The sandbox covers shell commands only » ; lecture permise sur la majeure partie de la machine par défaut [8] |
| **Hooks** | Contrôle programmable à chaque événement ([chapitre 07](07-hooks-et-garde-fous.md)) | Échec ouvert par défaut ; filtrage textuel contournable |
| **Confiance du dossier** | Dialogue à l'ouverture d'un dossier inconnu, qui indique depuis la v2.1.329 où sont déclarés les hooks du dossier [12] ; approbation des serveurs de `.mcp.json` [2] | Ni l'un ni l'autre ne s'affiche en mode non interactif (`-p`) [2] |

Points de détail qui comptent :

- les règles `deny` s'appliquent dans tous les modes, y compris `bypassPermissions` [7] ;
- en mode `auto`, les résultats d'outils sont retirés des requêtes au classifieur, pour qu'un contenu hostile ne puisse pas le manipuler directement [7] **(Non vérifié en texte intégral)** ;
- le bac à sable est désactivé par défaut (`/sandbox` pour l'activer) ; s'il n'est pas disponible sur la plateforme, les commandes s'exécutent sans lui, sauf `failIfUnavailable` [8] ;
- sous Windows natif, le bac à sable n'existe pas ; la documentation recommande WSL2 [8] ;
- WebFetch passe par un appel de modèle séparé et ne renvoie à l'agent qu'un résumé [2].

**Alternative : le bac à sable externe.** Willison et Prime Radiant décrivent un schéma où le code exécuté par l'agent tourne dans un bac à sable dédié tandis que l'agent reste à l'extérieur ; trois implémentations (v86 en WebAssembly, Apple Containers, QEMU via Quicksand) exposent la même API locale, avec un proxy HTTP en liste blanche et une substitution des identifiants qui permet des appels authentifiés « without sharing a secret with the agent » [13]. L'auteur y voit un terrain d'expérimentation, non une solution éprouvée. **Émergent.**

### Secrets

Un agent lit ce que l'utilisateur peut lire. Pour ne pas exposer de jeton dans la ligne de commande, `claude mcp add-json <nom> -` lit la configuration d'un serveur MCP sur l'entrée standard (v2.1.327, 17/11/2026) [12]. Le bac à sable autorise par défaut la lecture de `~/.ssh` et `~/.aws/credentials` [8]. Protections complémentaires : règles `deny` sur la lecture des fichiers de secrets (exemple de l'éditeur : `Read(./.env)`) [9], hook qui refuse l'écriture de motifs de clés ([chapitre 07](07-hooks-et-garde-fous.md)), secrets hors du dépôt, et, pour les exécutions en CI, secrets dans le gestionnaire de la plateforme : « Never commit API keys or OAuth tokens directly to your repository » [10].

### Chaîne d'approvisionnement

- **MCP** : Anthropic ne réalise pas d'audit de sécurité des serveurs MCP [2] ; la spécification demande que l'installation en un clic affiche « the exact command » [11]. Invariant Labs recommande d'épingler outils et paquets par empreinte [3].
- **Skills et plugins** : installer depuis des sources de confiance, auditer scripts, dépendances et accès réseau [4]. Un plugin peut déclarer des hooks, donc exécuter du code à chaque événement.
- **Configuration de projet** : un `.mcp.json` ou un `.claude/settings.json` modifié par une PR est du code exécutable ; il se relit comme tel.

## Bonnes pratiques

1. **Casser la triade** : pour une tâche qui lit du contenu non fiable, retirer l'accès aux données sensibles ou la sortie réseau [1].
2. **Mode manuel ou `auto` en local, `dontAsk` avec règles étroites en CI**, `bypassPermissions` uniquement dans un conteneur ou une VM isolés [7].
3. **Activer le bac à sable** là où il existe, avec `allowUnsandboxedCommands: false` [8].
4. **Des règles `deny`** pour les secrets et les commandes irréversibles, en sachant leurs limites [6].
5. **Une liste blanche réseau** plutôt qu'une liste noire pour les exécutions autonomes ([chapitre 12](12-execution-autonome.md)).
6. **Relire toute modification de configuration d'agent** (hooks, MCP, réglages, skills) comme du code.

## Pièges et anti-patterns

- **Le filtre anti-injection comme défense principale** [1].
- **`--dangerously-skip-permissions` sur le poste de travail** : aucune protection contre l'injection ni contre l'erreur [7].
- **La liste blanche réseau trop large** : autoriser un domaine générique comme `github.com` ouvre une voie d'exfiltration [8] **(Non vérifié en texte intégral)**.
- **Les secrets dans le dépôt « parce qu'il est privé »**.
- **Le serveur MCP installé depuis un lien** sans lecture de la commande ni de la source.

## État du débat

- **Garde-fous probabilistes** : des éditeurs de solutions de détection (dont Invariant Labs [3]) en défendent l'intérêt ; Willison les juge insuffisants par construction [1]. **Contesté.** Le consensus porte sur la nécessité de contrôles déterministes en dernier ressort.
- **Le mode `auto`** déplace la décision vers un classifieur : moins de demandes, donc moins de fatigue d'approbation, mais une garantie explicitement non totale [7]. Son efficacité réelle n'a pas été mesurée publiquement dans les sources consultées.

## Dans ce dépôt

- **Composants** : plugin [`garde-fous`](../plugins/garde-fous/) (commandes destructrices, secrets) ; architecture de la veille en couches ([ADR-004](../docs/decisions/ADR-004-architecture-veille.md)).
- **Labs** : [lab 02](../labs/README.md).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[P]** Willison, *The lethal trifecta for AI agents*, 16/06/2025. <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>
2. **[O]** Anthropic, *Security* (Claude Code). <https://code.claude.com/docs/en/security>
3. **[P]** Beurer-Kellner, Fischer (Invariant Labs), *MCP Security Notification: Tool Poisoning Attacks*, 01/04/2025. Éditeur d'une solution de protection. <https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks>
4. **[O]** Zhang, Lazuka, Murag (Anthropic), *Equipping agents for the real world with Agent Skills*, 16/10/2025. <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
5. **[P]** OWASP GenAI Security Project, *OWASP Top 10 for Agentic Applications for 2026*, 09/12/2025. <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>
6. **[O]** Anthropic, *Configure permissions*. <https://code.claude.com/docs/en/permissions>
7. **[O]** Anthropic, *Choose a permission mode* (lu en partie sous forme résumée). <https://code.claude.com/docs/en/permission-modes>
8. **[O]** Anthropic, *Configure the sandboxed Bash tool* (lu en partie sous forme résumée). <https://code.claude.com/docs/en/sandboxing>
9. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
10. **[O]** Anthropic, *Claude Code GitHub Actions*. <https://code.claude.com/docs/en/github-actions>
11. **[O]** Model Context Protocol, *Security Best Practices*. <https://modelcontextprotocol.io/specification/latest/basic/security_best_practices>
12. **[O]** Anthropic, *Changelog* (Claude Code), versions 2.1.327 et 2.1.329, 17 et 19/11/2026, consulté le 2026-11-27. <https://code.claude.com/docs/en/changelog>
13. **[P]** Willison, *External sandboxes for coding agents*, 17/11/2026, consulté le 2026-11-27 ; billet de lien vers Prime Radiant, avec qui l'auteur a travaillé (article source non lu). <https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/>
