# ADR-002 — Architecture du dépôt et découpage en plugins

- **Statut** : proposé
- **Date** : 2026-11-26

## Contexte

Le dépôt réunit une base de connaissances, un système agentique distribuable, une veille et des labs. Il doit être installable comme marketplace de plugins Claude Code sur plusieurs machines, rester lisible comme vitrine publique, et séparer ce qui est portable de ce qui est propre à Claude Code (voir ADR-003).

## Décision

### Le dépôt est un marketplace

Le fichier `.claude-plugin/marketplace.json`, à la racine, déclare les plugins par chemin relatif. Installation : `/plugin marketplace add <owner>/<repo>`, puis `/plugin install <plugin>@<marketplace>` [1]. Validation en CI par `claude plugin validate` [1].

### Deux plugins distribués, deux skills internes au dépôt

| Composant | Nature | Contenu | Raison du découpage |
|---|---|---|---|
| `workflow` | plugin | Skills des cinq étapes de l'ADR-001, subagents `relecteur` et `chercheur` | Cœur réutilisable sur tout projet |
| `garde-fous` | plugin | Hooks : blocage des commandes destructrices et de l'écriture de secrets, formatage/lint après édition, vérification avant fin de tâche | Propre à Claude Code ; activable indépendamment du workflow, y compris sur des projets où le workflow ne convient pas |
| `veille` | skill de projet (`.claude/skills/`) | Commande `/veille` | N'a de sens que dans ce dépôt (elle modifie `knowledge/` et `veille/`) : la distribuer n'apporterait rien |
| `talk` | skill de projet (`.claude/skills/`) | Génération de plans de présentation | Idem : dépend des chapitres de ce dépôt |

Un troisième plugin ne sera créé que si un besoin d'installation séparée apparaît.

### Arborescence cible

```text
.
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── workflow/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/<etape>/SKILL.md
│   │   ├── agents/{relecteur,chercheur}.md
│   │   └── README.md
│   └── garde-fous/
│       ├── .claude-plugin/plugin.json
│       ├── hooks/hooks.json
│       ├── scripts/          # implémentation des hooks
│       ├── tests/
│       └── README.md
├── .claude/skills/{veille,talk}/SKILL.md
├── knowledge/                # NN-slug.md, README.md (sommaire), glossaire.md
├── veille/                   # sources.yaml, state.json, digests/, scheduled-task.md
├── labs/NN-slug/             # README.md (énoncé), solution/
├── talks/
├── docs/decisions/
├── .github/                  # workflows CI, gabarits d'issue et de PR
├── AGENTS.md
├── CLAUDE.md                 # importe AGENTS.md
└── README.md
```

### Conventions

- Dépôt nommé `AtelierAgentique` (PascalCase, cohérent avec les autres projets du propriétaire) ; marketplace nommé `atelier-agentique` (kebab-case). Installation : `/plugin marketplace add <owner>/AtelierAgentique`, puis `/plugin install workflow@atelier-agentique`.
- Noms de plugins, skills et agents en kebab-case français sans accents, conformément aux contraintes de nommage des skills (minuscules, chiffres, tirets) [2] ; aucun préfixe réservé (`claude-`, `anthropic-`…) [1].
- Les composants de plugin suivent les emplacements par défaut, sans chemins personnalisés dans `plugin.json` [1].
- Scripts de hooks en **Python, bibliothèque standard uniquement** : portable entre Windows, macOS et Linux, testable sans dépendance. Toute donnée persistante va dans `${CLAUDE_PLUGIN_DATA}`, jamais dans `${CLAUDE_PLUGIN_ROOT}`, qui change à chaque mise à jour [1].

## Alternatives écartées

- **Un plugin monolithique** : impose les hooks à qui ne veut que le workflow, et inversement.
- **Un plugin par étape du workflow** : granularité sans usage réel ; multiplie les manifestes et les installations.
- **Dépôt séparé pour le marketplace** : contredit l'objectif d'un socle unique où le système applique ce que la base enseigne.
- **Distribuer `veille` et `talk` comme plugins** : ils dépendent du contenu de ce dépôt.

## Conséquences

- Les subagents de plugin ne prennent en charge ni `hooks`, ni `mcpServers`, ni `permissionMode` [3] : les garde-fous vivent dans `hooks/hooks.json` du plugin `garde-fous`, jamais dans la définition d'un agent.
- Les skills de plugin sont invoqués sous un espace de noms (`/workflow:<skill>`) [2].

## Incertitudes

- Lancement de Python depuis un hook sous Windows (`python`, `python3` ou `py`) : à vérifier en phase 3 ; le champ `shell` des hooks de type `command` [3] et la forme exec (`args`) sont les pistes.

## Sources

Consultées le 2026-11-26. Toutes de niveau **officiel**.

1. Anthropic, *Plugins reference* et *Plugin marketplaces*. <https://code.claude.com/docs/en/plugins-reference> · <https://code.claude.com/docs/en/plugin-marketplaces>
2. Anthropic, *Skills*. <https://code.claude.com/docs/en/skills> ; Agent Skills, *Specification*. <https://agentskills.io/specification>
3. Anthropic, *Subagents* et *Hooks reference*. <https://code.claude.com/docs/en/sub-agents> · <https://code.claude.com/docs/en/hooks>
