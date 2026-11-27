---
chapitre: 13
titre: Portabilité et standards
statut: brouillon
derniere_revision: 2026-11-28
---

# 13 — Portabilité et standards

> Écrire une fois instructions et procédures pour plusieurs agents de code, en sachant précisément ce qui est standard, ce qui est propre à un outil, et où se trouvent les équivalents.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- situer les standards ouverts AGENTS.md, Agent Skills et MCP, et leur gouvernance ;
- configurer un dépôt lisible par Claude Code, GitHub Copilot et Codex ;
- identifier les briques non standardisées et leurs équivalents par outil ;
- éviter les pièges de chargement propres à chaque outil.

## Concepts clés

**AGENTS.md.** Fichier Markdown sans champ obligatoire, placé à la racine et éventuellement dans des sous-répertoires, que les agents de code lisent comme instructions ; « The closest AGENTS.md to the edited file wins » [1]. Il est porté par l'Agentic AI Foundation sous l'égide de la Linux Foundation [1].

**Agent Skills.** Format de skill publié en standard ouvert par Anthropic ([chapitre 05](05-skills.md)) [2], devenu le 04/11/2026 un projet de LF Projects, LLC (Linux Foundation) [15].

**MCP.** Protocole de connexion aux outils, hébergé par LF Projects, LLC ([chapitre 04](04-outils-et-mcp.md)) [3].

## Mécanismes

### Matrice de prise en charge

État au 2026-11-27 **(Daté)** :

| Brique | Claude Code | GitHub Copilot | OpenAI Codex |
|---|---|---|---|
| AGENTS.md | Lu seulement en l'absence de CLAUDE.md ; sinon `@AGENTS.md` dans CLAUDE.md [4] | Lu (le plus proche l'emporte) ; CLAUDE.md et GEMINI.md à la racine lus aussi [5] | Natif : fichier global, puis de la racine du dépôt au répertoire courant ; 32 Kio par défaut [6] |
| Skills | `.claude/skills/`, plugins [7] | `.github/skills`, `.claude/skills`, `.agents/skills` [8] | `.agents/skills` (dépôt, utilisateur, admin) [9] |
| Agents personnalisés | Markdown, `.claude/agents/` [10] | `.github/agents/` [11] | TOML, `.codex/agents/` [12] |
| Hooks | Réglages ou `hooks/hooks.json` de plugin | `.github/hooks/*.json` [11] | `hooks.json` ou `config.toml` [13] |
| Plugins | Marketplaces [14] | Non documenté dans les pages consultées | Annuaire commun ChatGPT/Codex [9] |
| MCP | Oui | Oui | Oui |

### Pièges de chargement

- **Claude Code et AGENTS.md** : par défaut, Claude Code ne lit AGENTS.md « only when you have no CLAUDE.md » [4]. Un dépôt qui contient les deux doit importer AGENTS.md depuis CLAUDE.md (`@AGENTS.md`). Un lien symbolique fonctionne mais casse sous Windows [4].
- **Fusion ou remplacement** : Codex concatène les fichiers de la racine au répertoire courant, le plus proche venant en dernier [6] ; Claude Code concatène aussi ses CLAUDE.md [4] ; la règle d'AGENTS.md (« le plus proche l'emporte ») est compatible mais pas identique [1].
- **Plafond de taille** : Codex cesse d'ajouter des fichiers au-delà de 32 Kio cumulés par défaut [6].
- **Extensions de frontmatter** : les champs propres à Claude Code dans un `SKILL.md` ne font pas partie du standard [2], [7] ; leur traitement par les autres outils n'a pas été vérifié **(Non vérifié)**.

### Stratégie de portabilité

1. **AGENTS.md comme source** des instructions ; CLAUDE.md réduit à `@AGENTS.md` et aux spécificités de Claude Code.
2. **Skills au format standard**, dans un répertoire lu par plusieurs outils (`.claude/skills` est lu par Claude Code et Copilot ; `.agents/skills` par Copilot et Codex [8], [9]).
3. **Logique des hooks dans des scripts indépendants de l'outil** (JSON en entrée, code de sortie), seule la déclaration étant propre à l'outil.
4. **Équivalents documentés** plutôt que générés, tant qu'un seul outil est utilisé au quotidien.

## Bonnes pratiques

1. **Tester le chargement dans chaque outil cible** plutôt que supposer : `/context all` dans Claude Code liste les fichiers de mémoire réellement chargés [4].
2. **Garder AGENTS.md sous les plafonds** des outils, et court de toute façon ([chapitre 03](03-prompting-pour-agents.md)).
3. **Isoler et lister les extensions** propres à un outil.

## Pièges et anti-patterns

- **CLAUDE.md et AGENTS.md divergents** : deux sources de vérité, deux comportements.
- **Le lien symbolique** dans un dépôt utilisé sous Windows [4].
- **Supposer qu'un outil lit un emplacement** parce qu'un autre le fait.

## État du débat

- **Gouvernance** : les trois standards relèvent désormais de structures de la Linux Foundation : AGENTS.md via l'Agentic AI Foundation [1], MCP et Agent Skills comme projets de LF Projects, LLC [3], [15], ce dernier depuis le 04/11/2026 dans le cadre d'une donation présentée comme destinée à l'Agentic AI Foundation [15]. Aucun des trois n'est plus gouverné par un seul éditeur. **Daté.**
- **Convergence des formats non standardisés** : hooks et agents personnalisés existent chez les trois éditeurs avec des événements voisins mais des formats distincts ; aucune initiative de standardisation n'a été identifiée dans les sources consultées.

## Dans ce dépôt

- **Composants** : [ADR-003](../docs/decisions/ADR-003-portabilite.md) ; [AGENTS.md](../AGENTS.md) et [CLAUDE.md](../CLAUDE.md) ; README des plugins avec équivalents Copilot et Codex.
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** AGENTS.md. <https://agents.md/>
2. **[O]** Agent Skills, *Specification*. <https://agentskills.io/specification>
3. **[O]** Model Context Protocol, *Governance*. <https://modelcontextprotocol.io/community/governance>
4. **[O]** Anthropic, *Memory*. <https://code.claude.com/docs/en/memory>
5. **[O]** GitHub, *Custom instructions support*. <https://docs.github.com/en/copilot/reference/custom-instructions-support>
6. **[O]** OpenAI, *AGENTS.md* (Codex). <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
7. **[O]** Anthropic, *Skills*. <https://code.claude.com/docs/en/skills>
8. **[O]** GitHub, *About agent skills*. <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>
9. **[O]** OpenAI, *Build skills* (Codex). <https://learn.chatgpt.com/docs/build-skills>
10. **[O]** Anthropic, *Subagents*. <https://code.claude.com/docs/en/sub-agents>
11. **[O]** GitHub, *Customization cheat sheet*. <https://docs.github.com/en/copilot/reference/customization-cheat-sheet>
12. **[O]** OpenAI, *Subagents* (Codex). <https://learn.chatgpt.com/docs/agent-configuration/subagents>
13. **[O]** OpenAI, *Hooks* (Codex). <https://learn.chatgpt.com/docs/hooks>
14. **[O]** Anthropic, *Plugin marketplaces*. <https://code.claude.com/docs/en/plugin-marketplaces>
15. **[O]** Agent Skills, *Agent Skills Governance*, adopté le 04/11/2026, et commits « AAIF Donation » du même jour, consultés le 2026-11-28. <https://github.com/agentskills/agentskills/blob/main/GOVERNANCE.md>
