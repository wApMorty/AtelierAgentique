# Veille

Veille hebdomadaire automatisée : elle parcourt une liste curatée de sources, retient les nouveautés réelles, produit un digest et propose par PR les mises à jour de la base. Architecture, sécurité et budget : [ADR-004](../docs/decisions/ADR-004-architecture-veille.md).

| Fichier | Rôle |
|---|---|
| [`sources.yaml`](sources.yaml) | 25 sources curatées : URL, type, catégorie, niveau de confiance, justification |
| [`collecter.py`](collecter.py) | Collecte déterministe : une requête par source, déduplication, JSON compact des candidats ; aucune dépendance |
| [`state.json`](state.json) | État persistant : dernière exécution, éléments vus (90 jours), empreintes des pages sans flux |
| [`digests/`](digests/) | Un digest par semaine ISO (`AAAA-Sxx.md`) |
| [`scheduled-task.md`](scheduled-task.md) | Prompt autonome de la tâche planifiée, procédure de mise en place et accès |
| [`../.claude/skills/veille/SKILL.md`](../.claude/skills/veille/SKILL.md) | Méthode, invoquée par `/veille` en local et par la tâche planifiée |

En local : `/veille a-blanc` affiche un digest sans rien écrire ; `/veille` prépare une branche `veille/AAAA-Sxx` sans la pousser.
