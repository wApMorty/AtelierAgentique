# ADR-003 — Stratégie de portabilité multi-outils

- **Statut** : accepté
- **Date** : 2026-11-26

## Contexte

Claude Code est l'outil principal, mais le système doit rester réutilisable sous GitHub Copilot et OpenAI Codex. Deux standards ouverts existent : **AGENTS.md**, désormais porté par l'Agentic AI Foundation (Linux Foundation) [1], et **Agent Skills**, publié en standard ouvert par Anthropic [2] (mise à jour du 2026-11-28 : projet de LF Projects, LLC depuis le 04/11/2026 [15], ce qui renforce le choix de ce format). Le reste (hooks, subagents, plugins) existe chez les trois éditeurs, mais sous des formats incompatibles.

## État de la prise en charge (au 2026-11-26)

| Brique | Claude Code | GitHub Copilot | OpenAI Codex |
|---|---|---|---|
| AGENTS.md | Lu nativement **seulement en l'absence de CLAUDE.md** ; sinon import `@AGENTS.md` [3] | Lu (le plus proche l'emporte) ; CLAUDE.md lu aussi à la racine [5] | Natif : global, puis de la racine au répertoire courant, plafond 32 Kio par défaut [7] |
| Agent Skills (`SKILL.md`) | Natif, avec extensions propres [4] | `.github/skills`, `.claude/skills`, `.agents/skills` [6] | `.agents/skills` (dépôt, utilisateur, admin) [8] |
| Subagents / agents personnalisés | Markdown + frontmatter, `.claude/agents/` [9] | `.github/agents/*.md` [10] | TOML, `.codex/agents/` [11] |
| Hooks | `settings.json` ou `hooks/hooks.json` de plugin [12] | `.github/hooks/*.json` [10] | `hooks.json` ou `config.toml` [13] |
| Plugins / marketplace | Oui [14] | Non documenté dans les pages consultées | Oui, annuaire commun ChatGPT/Codex [8] |
| MCP | Oui | Oui | Oui |

## Décision

1. **Instructions : AGENTS.md est la source de vérité.** `CLAUDE.md` contient `@AGENTS.md` suivi des seules spécificités de Claude Code, comme le recommande la documentation [3]. Pas de lien symbolique : il casse sous Windows [3].
2. **Skills : format Agent Skills strict par défaut.** Le frontmatter se limite aux champs du standard (`name`, `description`, `license`, `compatibility`, `metadata`) [2]. Une extension Claude Code n'est admise que si elle porte une propriété de sécurité, en premier lieu `disable-model-invocation: true` sur les skills à effet de bord (commit, push, PR) ; chaque extension est listée dans le README du plugin. La CI vérifie que seuls les champs autorisés apparaissent.
3. **Subagents, hooks, plugins : spécifiques à Claude Code, assumés.** Ils restent isolés dans `plugins/`. Chaque README de plugin documente l'équivalent sous Copilot et Codex, sans générer automatiquement ces équivalents : aucun besoin avéré ne justifie aujourd'hui un générateur à maintenir.
4. **Logique des hooks hors du format de configuration.** Les scripts (Python, ADR-002) lisent du JSON sur l'entrée standard et renvoient un code de sortie : seule leur déclaration dépend de l'outil, ce qui rend un portage vers `.github/hooks/` ou `hooks.json` de Codex peu coûteux.

## Alternatives écartées

- **CLAUDE.md comme source, AGENTS.md dérivé** : inverse la dépendance ; Copilot et Codex lisent AGENTS.md en priorité [5], [7].
- **Réglage `claude-md-and-agents-md`** [3] : dépend d'un paramètre utilisateur, donc non reproductible pour un visiteur du dépôt.
- **Générer les agents et hooks pour les trois outils** : trois formats à maintenir et à tester pour un usage hypothétique.

## Incertitudes

- **Clés de frontmatter inconnues** : selon une partie de la documentation lue sous forme résumée, des outils tiers rejetteraient un `SKILL.md` contenant des clés hors standard. **Non vérifié** ; à tester en phase 3 avec Copilot CLI et Codex avant d'admettre une extension.
- `allowed-tools` est marqué « Experimental » dans le standard [2] ; il n'est pas utilisé tant que ce statut tient.
- Le format exact des agents Copilot n'a été lu que dans un récapitulatif [10] ; à confirmer avant de documenter les équivalents.

## Sources

Consultées le 2026-11-26. Toutes de niveau **officiel** sauf mention.

1. AGENTS.md. <https://agents.md/>
2. Agent Skills, *Specification*. <https://agentskills.io/specification>
3. Anthropic, *Memory* (CLAUDE.md et AGENTS.md). <https://code.claude.com/docs/en/memory>
4. Anthropic, *Skills*. <https://code.claude.com/docs/en/skills>
5. GitHub, *Custom instructions support*. <https://docs.github.com/en/copilot/reference/custom-instructions-support>
6. GitHub, *About agent skills*. <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>
7. OpenAI, *AGENTS.md*. <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
8. OpenAI, *Build skills*. <https://learn.chatgpt.com/docs/build-skills>
9. Anthropic, *Subagents*. <https://code.claude.com/docs/en/sub-agents>
10. GitHub, *Customization cheat sheet*. <https://docs.github.com/en/copilot/reference/customization-cheat-sheet>
11. OpenAI, *Subagents*. <https://learn.chatgpt.com/docs/agent-configuration/subagents>
12. Anthropic, *Hooks reference*. <https://code.claude.com/docs/en/hooks>
13. OpenAI, *Hooks*. <https://learn.chatgpt.com/docs/hooks>
14. Anthropic, *Plugin marketplaces*. <https://code.claude.com/docs/en/plugin-marketplaces>
15. Agent Skills, *Agent Skills Governance*, adopté le 04/11/2026, consulté le 2026-11-28. <https://github.com/agentskills/agentskills/blob/main/GOVERNANCE.md>
