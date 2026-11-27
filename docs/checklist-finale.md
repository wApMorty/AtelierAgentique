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

Mise à jour du 2026-11-27 : dépôt publié, `main` protégé par un ruleset (PR et contrôle « Périmètre des PR de veille » obligatoires), CI distante verte avec lychee, tâche de veille planifiée chaque lundi, secret `DISCORD_WEBHOOK_URL` en place, base relue.

- **Mesurer le quota** consommé par une exécution planifiée de la veille, pour ajuster les plafonds de l'ADR-004.
- **Essai réel des plugins** dans une session Claude Code : seuls l'installation et les hooks hors agent ont été testés, pas un déroulé complet du workflow ni le déclenchement des hooks en session.
- **Points non vérifiés**, signalés dans les documents : déclenchement de la notification par une PR ouverte par l'application Claude (la PR #2 a été ouverte sous le compte du propriétaire), application de la liste blanche aux tâches planifiées, traitement des clés de frontmatter non standard par Copilot et Codex, liste détaillée du Top 10 OWASP agentique.
- **Échecs TLS locaux** : sept sources n'ont pas pu être lues depuis Python sous Windows ; le comportement attendu dans le cloud est à confirmer.

## Prochaines actions recommandées

1. **Dérouler le lab 01 vous-même** avec les deux plugins installés : c'est le test réel du workflow, des hooks et du relecteur, et la première démonstration pour une présentation interne.
2. **Relire la PR de la veille du lundi 2026-11-30** et noter sa consommation, pour ajuster les plafonds de l'ADR-004.
