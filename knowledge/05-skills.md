---
chapitre: 05
titre: Skills
statut: brouillon
derniere_revision: 2026-11-28
---

# 05 — Skills

> Empaqueter un savoir-faire procédural que l'agent charge seulement quand il en a besoin, dans un format lisible par plusieurs outils.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- expliquer la divulgation progressive à trois niveaux et son intérêt pour le contexte ;
- écrire un skill conforme au standard Agent Skills, et identifier les extensions propres à Claude Code ;
- rédiger une description qui déclenche le skill au bon moment ;
- distinguer skill, fichier d'instructions, subagent et hook ;
- évaluer le risque d'un skill tiers.

## Concepts clés

**Skill.** « A directory containing a SKILL.md file » qui regroupe instructions, scripts et ressources [1]. Le fichier `SKILL.md` commence par un frontmatter YAML comportant au minimum `name` et `description` [1], [2].

**Agent Skills.** Format publié en standard ouvert par Anthropic en décembre 2025 [1], spécifié sur agentskills.io [2] et pris en charge par Claude Code, GitHub Copilot et OpenAI Codex (voir [chapitre 13](13-portabilite-et-standards.md)).

**Divulgation progressive.** Trois niveaux de chargement [1], [2] :

1. **Métadonnées** (`name`, `description`) : chargées au démarrage, environ 100 tokens par skill selon la spécification [2] ;
2. **Corps** du `SKILL.md` : lu quand le skill est jugé pertinent, moins de 5 000 tokens recommandés [2] ;
3. **Ressources** (`references/`, `scripts/`, `assets/`) : lues ou exécutées à la demande.

## Mécanismes

### Format standard

La spécification impose [2] :

| Champ | Contraintes |
|---|---|
| `name` (requis) | 1 à 64 caractères, minuscules, chiffres et tirets, sans tiret initial, final ou double ; identique au nom du répertoire |
| `description` (requis) | 1 à 1 024 caractères ; dit ce que fait le skill et quand l'utiliser |
| `license`, `compatibility`, `metadata` | Optionnels |
| `allowed-tools` | Optionnel, marqué expérimental |

Elle recommande un `SKILL.md` de moins de 500 lignes et des références à un seul niveau de profondeur [2].

### Extensions de Claude Code

Claude Code ajoute des champs hors standard [3] : `disable-model-invocation` (le skill ne se déclenche que sur commande explicite), `user-invocable`, `argument-hint`, `arguments`, `model`, `effort`, `context: fork` (exécution dans un subagent), `agent`, `hooks`, `paths`, `shell`, entre autres. Il prend aussi en charge des substitutions (`$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`…) et l'injection dynamique de contexte (`` !`commande` ``), dont l'échec interrompt l'invocation [3]. Les anciennes commandes personnalisées (`.claude/commands/`) ont été fusionnées dans les skills : « Custom commands have been merged into skills » [3].

Un skill invoqué reste dans le contexte pour les tours suivants ; après une compaction, les corps de skills sont conservés dans la limite de 5 000 tokens chacun et 25 000 au total [4] **(Daté)**.

### Le déclenchement

Le modèle décide de charger un skill d'après sa seule description. Une description efficace répond à deux questions : que fait le skill, et dans quelles situations l'utiliser [2]. Claude Code tronque description et `when_to_use` à 1 536 caractères par entrée, dans un budget global proportionnel à la fenêtre [3], [4] **(Daté)**. Pour un skill à effet de bord (commit, déploiement), Anthropic recommande `disable-model-invocation: true`, afin qu'il ne parte jamais sans demande explicite [5].

### Skill, instructions, subagent, hook

| Besoin | Mécanisme | Pourquoi |
|---|---|---|
| Consigne valable à chaque tour | Fichier d'instructions ([chapitre 03](03-prompting-pour-agents.md)) | Toujours chargée |
| Procédure ponctuelle, éventuellement outillée | Skill | Chargée à la demande |
| Sous-tâche volumineuse à isoler | Subagent ([chapitre 06](06-subagents-et-orchestration.md)) | Fenêtre séparée |
| Règle sans exception | Hook ([chapitre 07](07-hooks-et-garde-fous.md)) | Déterministe |

Un skill peut combiner plusieurs de ces mécanismes : `context: fork` l'exécute dans un subagent, et un skill peut déclarer ses propres hooks [3].

### Scripts et déterminisme

Un script fourni avec un skill s'exécute sans que son code entre dans le contexte ; seule sa sortie y entre [1]. C'est le moyen de rendre déterministe une partie de la procédure (extraction, validation, formatage) tout en laissant au modèle le jugement.

## Bonnes pratiques

1. **Un skill, une tâche** : OpenAI formule la même règle (« Keep each skill scoped to one job ») [6].
2. **Soigner la description** comme un prompt de déclenchement : situations d'usage concrètes, mots que l'utilisateur emploiera.
3. **S'en tenir aux champs standards** quand la portabilité compte ; isoler et documenter les extensions (voir [ADR-003](../docs/decisions/ADR-003-portabilite.md)).
4. **Protéger les skills à effet de bord** par `disable-model-invocation: true` [5].
5. **Déporter le volumineux** dans `references/` et le déterministe dans `scripts/`.
6. **Valider le format** avec l'outil de la spécification (`skills-ref validate`) [2] ou `claude plugin validate` pour un plugin [7].

## Pièges et anti-patterns

- **La description vague** (« aide pour le code ») : le skill ne se déclenche jamais, ou toujours.
- **Le skill encyclopédique** : un `SKILL.md` de mille lignes annule le bénéfice de la divulgation progressive.
- **Le skill tiers non audité** : Anthropic avertit que des skills malveillants peuvent « direct Claude to exfiltrate data » ; n'installer que des sources de confiance et auditer scripts, dépendances et accès réseau [1].
- **Les extensions non signalées** : un champ propre à Claude Code dans un skill présenté comme portable. **Non vérifié** : le comportement exact de chaque outil tiers face à une clé inconnue (ignorée ou rejetée) n'a pas été confirmé dans les documentations consultées.

## État du débat

- **Gouvernance désormais neutre.** Le document de gouvernance adopté le 04/11/2026 fait du projet « Agent Skills a Series of LF Projects, LLC », la structure de la Linux Foundation qui héberge déjà MCP, avec un comité technique de mainteneurs nommés à titre individuel et la règle « No seats are reserved for specific companies » [9]. Les commits correspondants sont intitulés « AAIF Donation », ce qui le rattache à l'Agentic AI Foundation, comme AGENTS.md [9]. Le format n'est donc plus porté par le seul éditeur qui l'a créé. **Daté.**
- **Skills ou serveurs MCP ?** La révision 2026-07-28 de MCP introduit une extension « skills over MCP » [8] : la frontière entre les deux mécanismes de distribution reste à stabiliser. **Émergent.**

## Dans ce dépôt

- **Composants** : les skills du plugin [`workflow`](../plugins/workflow/) suivent le format standard, avec `disable-model-invocation` sur les étapes à effet de bord ; les skills internes `veille` et `talk` vivent dans `.claude/skills/`.
- **Labs** : [lab 03 — conception d'un skill](../labs/README.md).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Zhang, Lazuka, Murag (Anthropic), *Equipping agents for the real world with Agent Skills*, 16/10/2025, mis à jour le 18/12/2025. <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
2. **[O]** Agent Skills, *Specification*. <https://agentskills.io/specification>
3. **[O]** Anthropic, *Skills* (Claude Code). <https://code.claude.com/docs/en/skills>
4. **[O]** Anthropic, *Context window*. <https://code.claude.com/docs/en/context-window>
5. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
6. **[O]** OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
7. **[O]** Anthropic, *Plugin marketplaces*. <https://code.claude.com/docs/en/plugin-marketplaces>
8. **[O]** Model Context Protocol, *Changelog* de la révision 2026-07-28. <https://modelcontextprotocol.io/specification/2026-07-28/changelog>
9. **[O]** Agent Skills, *Agent Skills Governance*, adopté le 04/11/2026, et commits « AAIF Donation » du même jour, consultés le 2026-11-28. <https://github.com/agentskills/agentskills/blob/main/GOVERNANCE.md>
