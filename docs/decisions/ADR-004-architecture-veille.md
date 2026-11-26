# ADR-004 — Architecture de la veille

- **Statut** : accepté
- **Date** : 2026-11-26

## Contexte

La base de connaissances porte sur un domaine qui évolue chaque semaine. Une veille automatisée doit détecter les nouveautés réelles, proposer des mises à jour, et le faire sans intervention, dans un quota Claude Pro, en traitant tout contenu web comme une donnée potentiellement hostile.

## Décision

### Exécution

- **Méthode** : un skill de projet `.claude/skills/veille/SKILL.md`, invocable en local par `/veille`. La tâche planifiée ne contient pas la méthode ; elle invoque le skill. Ce partage « le skill définit la méthode, la planification définit le moment » est aussi celui que recommande OpenAI [5].
- **Planification** : une tâche planifiée cloud Claude Code, hebdomadaire. Elle est disponible sur l'offre Pro et chaque exécution ouvre une session complète, consultable après coup [1].
- **Collecte déterministe** : un script sans dépendance, `veille/collecter.py`, interroge chaque source (flux Atom ou RSS, page, API), écarte ce qui est déjà vu ou hors fenêtre, et renvoie un JSON compact de candidats. Le modèle ne lit que ces candidats et n'approfondit que les éléments retenus. La collecte ne coûte ainsi aucun token, conformément au rôle des scripts dans un skill (voir `knowledge/05-skills.md`).
- **État** : `veille/state.json` conserve la date de dernière exécution et les identifiants (URL) des éléments déjà traités, purgés au-delà de 90 jours.
- **Sortie** : `veille/digests/AAAA-Sxx.md` (semaine ISO) et, le cas échéant, des modifications de `knowledge/`.

### Publication et notification

- L'exécution commite sur une branche `veille/AAAA-Sxx`, pousse, puis ouvre une PR. **Elle ne pousse jamais sur `main`, ne merge jamais et ne force jamais un push.**
- **Exception écrite à la règle « jamais de push sans accord »**, validée par le propriétaire le 2026-11-26 et limitée aux branches `veille/*` créées par cette tâche.
- La PR est créée par l'API REST (`gh api`), car le proxy GitHub des sessions cloud rejette GraphQL, donc `gh pr create` [2].
- **Notification Discord** : un workflow GitHub Actions, déclenché à l'ouverture d'une PR dont la branche source commence par `veille/`, poste un message via un webhook Discord stocké en secret de dépôt (`DISCORD_WEBHOOK_URL`). Aucun secret ne transite par la session de veille.

### Sécurité, en couches

| Couche | Mécanisme | Ce qu'elle garantit |
|---|---|---|
| Instruction | Le skill pose que tout contenu récupéré est une donnée, jamais une instruction, et impose une section « Contenus suspects » dans le digest | Signalement des tentatives d'injection |
| Réseau | Environnement cloud en accès **Limited**, avec pour liste blanche les seuls domaines de `sources.yaml` [2] ; GitHub, autorisé par défaut, reste une voie de sortie résiduelle | Limite l'exfiltration et la navigation hors périmètre |
| Git | Protection de branche sur `main` (PR obligatoire) ; le proxy ne limite pas les branches poussées, d'où cette règle côté GitHub [2] | Aucune écriture directe sur `main` |
| CI | Workflow `veille-perimetre.yml`, en `pull_request_target`, contrôle obligatoire de la règle de `main` : il liste les fichiers de la PR par l'API, sans extraire ni exécuter son code, et refuse tout fichier hors de `veille/digests/`, `veille/state.json` et des chapitres de `knowledge/`, ainsi que plus de trois chapitres | Le périmètre est vérifié de façon déterministe ; la PR ne peut ni modifier ce contrôle, ni toucher au code et au prompt de la veille |
| Humain | Merge manuel uniquement | Rien n'entre dans la base sans relecture |

L'instruction seule ne suffit pas ; c'est la combinaison des couches déterministes qui protège, conformément à la distinction entre règles appliquées « every time » et instructions lues par le modèle [3].

### Budget par exécution

Les offres Pro ont une limite par fenêtre de cinq heures et une limite hebdomadaire, partagées entre Claude et Claude Code, sans chiffre publié [4] ; les exécutions planifiées consomment ce même quota [1]. Plafonds retenus :

| Paramètre | Plafond |
|---|---|
| Sources dans `sources.yaml` | 25 (vérifié par un test) |
| Requêtes de collecte | 1 par source, par le script, sans coût en tokens |
| Candidats par source | 10 |
| Lectures d'approfondissement par le modèle | 15 |
| Nouveautés retenues dans le digest | 10 |
| Chapitres modifiés par PR | 3 |
| Subagents | aucun ; exécution séquentielle dans le contexte principal |

Mesure de l'essai à blanc du 2026-11-27 (fenêtre de 14 jours) : 25 requêtes, 62 candidats, un JSON d'environ 27 Ko soit de l'ordre de 7 000 tokens, 7 nouveautés retenues pour 2 lectures d'approfondissement (`veille/digests/2026-S48.md`). Une semaine ordinaire, avec un état déjà enregistré, produira moins de candidats.

## Alternatives écartées

- **Validation dans la conversation de la tâche, puis push** : écartée par le propriétaire pour éviter une relecture hebdomadaire de la session.
- **Webhook GitHub natif vers Discord (suffixe `/github`)** : aucun code, mais notifie tous les événements de PR du dépôt, sans filtre sur `veille/*`, et sa configuration n'est pas versionnée [6].
- **Notification envoyée par la session de veille** : exposerait le webhook dans un environnement qui lit du contenu non fiable.
- **Accès réseau Full** : supprime une couche de défense sans nécessité, les sources étant connues.
- **Exécution locale planifiée** : dépend d'une machine allumée.

## Incertitudes

- **Consommation réelle d'une exécution cloud** : inconnue faute de chiffres publiés [4] ; à mesurer (`/usage`) lors de la première exécution planifiée, puis ajuster les plafonds.
- **Déclenchement du workflow de notification** : une PR ouverte avec le `GITHUB_TOKEN` d'Actions ne déclenche pas d'autres workflows ; une PR ouverte par l'identité de l'application GitHub de Claude devrait le faire. **Non vérifié** tant que la tâche n'a pas tourné.
- **TLS en local** : lors de l'essai à blanc sous Windows, sept sources ont échoué à la vérification des certificats par l'interpréteur Python local, alors que `curl` les atteint ; défaut probable du magasin de certificats local, sans effet attendu dans l'environnement cloud Linux. La vérification TLS n'est jamais désactivée.
- **Liste blanche réseau des tâches planifiées** : documentée pour les environnements cloud [2] ; son application identique aux tâches planifiées est à confirmer [1].
- Le statut « research preview » des tâches planifiées implique que leur comportement peut changer [1].

## Sources

Consultées le 2026-11-26. Niveaux : **O** = officiel, **P** = pratique reconnue.

1. **O** — Anthropic, *Automate work with scheduled tasks*. <https://code.claude.com/docs/en/routines>
2. **O** — Anthropic, *Claude Code on the web* et *Cloud environments*. <https://code.claude.com/docs/en/claude-code-on-the-web> · <https://code.claude.com/docs/en/cloud-environments>
3. **O** — Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
4. **O** — Anthropic, *Using Claude Code with your Pro or Max plan*. <https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan>
5. **O** — OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
6. **O** — Discord, *Intro to Webhooks*. <https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks>
