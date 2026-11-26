# Checklist finale de l'initialisation

État au 2026-11-27, à l'issue des phases 0 à 6. Rien n'a été poussé.

## Fait

| Phase | Livrable | Vérification |
|---|---|---|
| 0 | ADR-001 à 004 (acceptés), recherche sourcée, nom du dépôt | Sources datées et classées dans chaque ADR |
| 1 | README, AGENTS.md, CLAUDE.md, licences MIT et CC BY 4.0, CI, gabarits, marketplace | `claude plugin validate --strict` vert, y compris sans authentification |
| 2 | Gabarit, 15 chapitres, glossaire, sommaire | Lint Markdown vert ; 96 liens externes répondent ; liens relatifs valides |
| 3 | Plugin `workflow` (5 skills, 2 subagents), plugin `garde-fous` (4 hooks) | Installation testée dans une configuration isolée ; 16 tests des hooks ; format des skills contrôlé en CI |
| 4 | 25 sources, collecteur, skill `/veille`, tâche planifiée, notification Discord, contrôle de périmètre | 6 tests du collecteur ; essai à blanc consigné dans `veille/digests/2026-S48.md` |
| 5 | Labs 01 à 03 avec critères vérifiables par script, gabarit et skill `talk` | Les tests de chaque lab échouent au départ et passent sur la solution ; vérifiés en CI |
| 6 | CI locale complète, revue indépendante | 0 bloquant ; 6 constats importants et les mineurs utiles corrigés |

## Décisions prises sans validation explicite

À relire en priorité, puisque la consigne était d'avancer sans s'arrêter :

- **Liste des sources de veille** (`veille/sources.yaml`) : elle devait vous être soumise avant de continuer.
- **Noms** des skills (`cadrer`, `planifier`, `implementer`, `verifier`, `relire`) et des agents (`relecteur`, `chercheur`).
- **Fichier `.garde-fous.json`** et approbation interactive de la commande de vérification de fin.
- **Titulaire du copyright** de la licence MIT : `wApMorty`.
- **Langage des labs** : Python pour les labs 01 et 02, TypeScript/Angular pour le lab 03.

## Reste à faire

- **Publier** : créer le dépôt GitHub `wApMorty/AtelierAgentique`, pousser `main`, vérifier la CI distante. La vérification des liens par lychee n'a tourné qu'en substitut local (curl).
- **Protéger `main`** avec un ruleset dont le contrôle « Périmètre des PR de veille » est obligatoire (`veille/scheduled-task.md`, étape 1).
- **Mettre en place la veille** : environnement cloud, tâche planifiée, secret `DISCORD_WEBHOOK_URL`, première exécution, mesure du quota.
- **Essai réel des plugins** dans une session Claude Code : seuls l'installation et les hooks hors agent ont été testés, pas un déroulé complet du workflow ni le déclenchement des hooks en session.
- **Points non vérifiés**, signalés dans les documents : déclenchement de la notification par une PR de l'application Claude, application de la liste blanche aux tâches planifiées, traitement des clés de frontmatter non standard par Copilot et Codex, liste détaillée du Top 10 OWASP agentique.
- **Échecs TLS locaux** : sept sources n'ont pas pu être lues depuis Python sous Windows ; le comportement attendu dans le cloud est à confirmer.
- **Relecture de la base** : les chapitres sont au statut « Brouillon ».

## Trois prochaines actions recommandées

1. **Publier le dépôt et protéger `main`** : c'est le préalable à la CI distante, à la veille et à l'installation sur vos autres machines.
2. **Dérouler le lab 01 vous-même** avec les deux plugins installés : c'est le test réel du workflow, des hooks et du relecteur, et la première démonstration pour une présentation interne.
3. **Lancer la première veille planifiée** et mesurer sa consommation, pour ajuster les plafonds de l'ADR-004 avant de la laisser tourner chaque semaine.
