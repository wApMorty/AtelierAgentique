@AGENTS.md

## Spécificités Claude Code

- Les hooks, subagents et plugins sont propres à Claude Code : ils restent dans `plugins/` et leur README documente l'équivalent sous Copilot et Codex.
- Les subagents de plugin ignorent `hooks`, `mcpServers` et `permissionMode` : les garde-fous se déclarent dans `plugins/garde-fous/hooks/hooks.json`.
- Une donnée persistante de plugin va dans `${CLAUDE_PLUGIN_DATA}`, jamais dans `${CLAUDE_PLUGIN_ROOT}`.
- Scripts de hooks : Python, bibliothèque standard uniquement. Sous Windows, `python3` peut désigner l'alias du Microsoft Store et échouer.
- Tester le marketplace en local : `/plugin marketplace add ./`, puis `/plugin install <plugin>@atelier-agentique`.
- Valider avant tout commit touchant un manifeste : `claude plugin validate --strict <chemin>`.
