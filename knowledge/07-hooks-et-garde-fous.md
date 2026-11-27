---
chapitre: 07
titre: Hooks et garde-fous
statut: relu
derniere_revision: 2026-11-27
---

# 07 — Hooks et garde-fous

> Imposer par du code, à chaque fois, ce qu'une instruction ne garantit qu'en moyenne.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- distinguer instruction, règle de permission, hook et bac à sable, et choisir le bon niveau de garantie ;
- écrire un hook Claude Code : événement, filtre, entrée, codes de sortie, sortie JSON ;
- concevoir les garde-fous usuels : blocage de commandes, protection des secrets, formatage, vérification avant fin de tâche ;
- connaître les limites des hooks, en particulier leur comportement en cas d'échec.

## Concepts clés

**Hook.** Commande, requête HTTP, appel d'outil MCP ou évaluation par un modèle, déclenché par Claude Code à un moment précis de son cycle de vie [1]. Le hook de type `command` reçoit un JSON sur l'entrée standard et répond par son code de sortie et, optionnellement, un JSON sur la sortie standard [1].

**Garde-fou.** Contrôle qui empêche ou corrige une action indésirable de l'agent, indépendamment de ce que le modèle a décidé.

**Hiérarchie des garanties.** Du plus faible au plus fort : instruction (le modèle peut l'ignorer) ; hook (exécuté à chaque événement, mais qui échoue en mode ouvert par défaut) ; règle de permission `deny` (appliquée par l'outil dans tous les modes) ; bac à sable du système d'exploitation (indépendant de l'outil) [2], [3].

## Mécanismes

### Événements

Claude Code expose plus d'une trentaine d'événements [1] **(Daté)**. Les plus utiles pour des garde-fous :

| Événement | Moment | Usage typique |
|---|---|---|
| `PreToolUse` | Avant un appel d'outil | Bloquer une commande, protéger un fichier, réécrire une entrée |
| `PostToolUse` | Après un appel réussi | Formater, linter, signaler une erreur à l'agent |
| `Stop` / `SubagentStop` | Quand l'agent veut s'arrêter | Exiger que la vérification passe |
| `UserPromptSubmit` | À la soumission d'un prompt | Ajouter du contexte, filtrer |
| `SessionStart` | Démarrage, reprise, après compaction | Injecter un état ([chapitre 02](02-ingenierie-du-contexte.md)) |
| `PreCompact` / `PostCompact` | Autour d'une compaction | Sauvegarder ou réinjecter |
| `PreSkillShellCommand` | Au chargement d'un skill ou d'une commande | Refuser les commandes shell en ligne qu'il contient (ajouté en v2.1.332, 25/11/2026) [8] |
| `PermissionDenied` | Après un refus de permission | `retry: true` invite l'agent à refaire l'appel refusé, « only if you asked for that call » depuis la v2.1.331 [8] |

### Configuration

Un hook se déclare dans les réglages (`~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`), dans le fichier `hooks/hooks.json` d'un plugin, ou dans le frontmatter d'un skill ou d'un subagent [1]. Forme :

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python scripts/bloquer.py", "timeout": 30 }]
      }
    ]
  }
}
```

Le `matcher` filtre sur le nom de l'outil ; des lettres et `|` désignent des noms exacts, les autres caractères en font une expression régulière [1]. Un champ `if`, à la syntaxe des règles de permission (`Bash(rm *)`), affine le filtre, mais l'éditeur le qualifie de « best-effort » [1].

### Entrée et sortie

L'entrée JSON contient notamment `session_id`, `cwd`, `permission_mode`, `hook_event_name`, et pour les événements d'outil `tool_name` et `tool_input` [1]. Codes de sortie [1] :

- **0** : succès ; la sortie standard est interprétée comme JSON si c'est un objet unique ;
- **2** : erreur bloquante ; stderr est la raison, transmise à l'agent ; pour `PreToolUse`, l'appel est bloqué ; pour `Stop`, l'arrêt est refusé ;
- **autre** : erreur non bloquante. L'éditeur insiste : « If your hook is meant to enforce a policy, use exit 2 » [1].

En JSON, `PreToolUse` peut renvoyer `permissionDecision` (`allow`, `deny`, `ask`, `defer`), une raison et une entrée modifiée [1].

### Variables utiles

`CLAUDE_PROJECT_DIR` (racine du projet), `CLAUDE_PLUGIN_ROOT` (répertoire du plugin installé, qui change à chaque mise à jour) et `CLAUDE_PLUGIN_DATA` (données persistantes du plugin) [1], [4].

### Limites à connaître

- **Échec ouvert par défaut** : un hook qui plante ou dépasse son délai ne bloque rien, sauf `onFailure: "block"` [1]. Un garde-fou de sécurité doit le préciser. Depuis la v2.1.328 (19/11/2026), l'option vaut aussi pour les hooks `mcp_tool` ; depuis la v2.1.329, un `PreToolUse` en erreur ne refuse plus l'appel d'outil d'un script en Code Mode, comme hors de ce mode, si bien que `onFailure: "block"` y devient également nécessaire [8] **(Daté)**.
- **Code Mode** : les hooks `UserPromptSubmit` ne s'exécutent plus sur la sortie des scripts ; pour l'expurger, l'éditeur renvoie à un `PostToolUse` avec `updatedToolOutput` (v2.1.328) [8] **(Daté)**.
- **Délais** : 600 secondes par défaut pour un hook `command`, moins pour certains événements [1] **(Daté)**.
- **Plafond sur `Stop`** : après huit blocages consécutifs sans appel d'outil, l'arrêt est accordé quand même [2] **(Daté)**. Un hook `Stop` ne peut donc pas boucler indéfiniment.
- **Le filtre par texte de commande est contournable** : un garde-fou qui cherche `rm -rf` dans une chaîne ne voit pas `find . -delete` ni un script qui supprime. Les règles `deny` de Claude Code ont la même limite : `Bash(curl *)` n'arrête pas `sh -c 'curl …'` [3]. Pour une garantie réelle, le bac à sable ([chapitre 10](10-securite.md)).
- **Les hooks héritent de l'environnement** et s'exécutent avec les droits de l'utilisateur [1] : un hook est du code à relire comme tel.

### Les garde-fous usuels

| Garde-fou | Événement | Principe |
|---|---|---|
| Commandes destructrices | `PreToolUse` sur `Bash` | Liste de motifs bloqués (suppression récursive hors du projet, `git push --force`, `git reset --hard`…), exit 2 avec raison |
| Écriture de secrets | `PreToolUse` sur `Write`/`Edit` | Détection de motifs de clés et refus d'écrire dans `.env` et apparentés |
| Formatage et lint | `PostToolUse` sur `Edit`/`Write` | Lancer le formateur du langage du fichier modifié ; signaler les erreurs à l'agent [2] |
| Vérification avant fin | `Stop` | Lancer tests ou typage ; exit 2 si échec : « pnpm tsc --noEmit 1>&2 \|\| exit 2 » [2] |

Geoffrey Huntley, cité par Simon Willison, décrit un hook de pré-commit qui rejette les contournements et renvoie un prompt correctif à l'agent [5] : la même logique appliquée à git.

## Bonnes pratiques

1. **Un hook par règle**, petit, testé, avec un message d'erreur qui dit à l'agent quoi faire.
2. **Exit 2 et `onFailure: "block"`** pour tout ce qui relève de la sécurité [1].
3. **Garder l'ensemble réduit** : Anthropic recommande de limiter les règles imposées à celles qui ne souffrent pas d'exception [2].
4. **Doubler par une règle `deny`** quand la règle peut s'exprimer ainsi : elle s'applique dans tous les modes [3].
5. **Tester les hooks hors de l'agent** : ce sont des programmes qui lisent du JSON ; un test unitaire par cas bloqué et par cas autorisé.
6. **Écrire les hooks dans un langage portable** et sans dépendance (voir [ADR-002](../docs/decisions/ADR-002-architecture-repo.md)).

## Pièges et anti-patterns

- **Le hook de sécurité en exit 1** : non bloquant [1].
- **Le hook lent sur `PostToolUse`** : exécuté après chaque édition, il ralentit toute la session.
- **Le hook `Stop` qui lance toute la suite d'intégration** : coût et délai à chaque fin de tour ; préférer une vérification rapide et ciblée.
- **La liste noire présentée comme une garantie** : elle réduit les accidents, pas les attaques [3].
- **Le hook qui écrit dans `${CLAUDE_PLUGIN_ROOT}`** : données perdues à la mise à jour [4].

## État du débat

- **Instructions ou hooks ?** Consensus éditeur : ce qui doit arriver à chaque fois relève du déterministe [2]. La limite pratique est le coût de maintenance d'un grand nombre de hooks ; les sources ne proposent pas de seuil.
- **Portabilité** : Copilot (`.github/hooks/*.json`) et Codex (`hooks.json`) disposent désormais de hooks, avec des événements voisins mais des formats différents [6], [7] (voir [chapitre 13](13-portabilite-et-standards.md)). **Daté.**

## Dans ce dépôt

- **Composants** : le plugin [`garde-fous`](../plugins/garde-fous/) implémente les quatre garde-fous du tableau, en Python sans dépendance, avec des tests.
- **Labs** : [lab 02 — écriture d'un hook de garde-fou](../labs/README.md).

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic, *Hooks reference*. <https://code.claude.com/docs/en/hooks>
2. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
3. **[O]** Anthropic, *Configure permissions*. <https://code.claude.com/docs/en/permissions>
4. **[O]** Anthropic, *Plugins reference*. <https://code.claude.com/docs/en/plugins-reference>
5. **[E]** Willison, notes du tag *coding-agents* (citation de Geoffrey Huntley, 13/10/2026). <https://simonwillison.net/tags/coding-agents/>
6. **[O]** GitHub, *Customization cheat sheet*. <https://docs.github.com/en/copilot/reference/customization-cheat-sheet>
7. **[O]** OpenAI, *Hooks* (Codex). <https://learn.chatgpt.com/docs/hooks>
8. **[O]** Anthropic, *Changelog* (Claude Code), versions 2.1.328 à 2.1.332, 19 au 25/11/2026, consulté le 2026-11-27. <https://code.claude.com/docs/en/changelog>
