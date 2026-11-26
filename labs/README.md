# Labs

Un lab par concept majeur, en TypeScript/Angular ou en Python selon ce qui sert le mieux le concept. Chaque lab comporte un objectif, des prérequis, un énoncé, des critères de réussite vérifiables par script, une solution indicative séparée et un lien vers le chapitre correspondant de la [base](../knowledge/README.md).

| # | Lab | Concept | Langage | Chapitre |
|---|---|---|---|---|
| 01 | [Workflow complet de bout en bout](01-workflow-bout-en-bout/) | Cadrer, planifier, TDD, vérifier, relire | Python | [08](../knowledge/08-workflows-developpement.md) |
| 02 | [Écriture d'un hook de garde-fou](02-hook-garde-fou/) | Garantie déterministe, testée hors de l'agent | Python | [07](../knowledge/07-hooks-et-garde-fous.md) |
| 03 | [Conception d'un skill](03-conception-skill/) | Description, divulgation progressive, script de vérification | TypeScript/Angular | [05](../knowledge/05-skills.md) |

## Labs proposés ensuite

| Lab | Concept | Langage | Chapitre |
|---|---|---|---|
| Budget de contexte | Mesurer avec `/context` l'effet d'un CLAUDE.md, de skills et de serveurs MCP ; réduire de moitié sans perte | Python | [02](../knowledge/02-ingenierie-du-contexte.md) |
| Délégation à un subagent | Exploration d'une base Angular inconnue, avec et sans subagent ; comparer contexte consommé et qualité de la synthèse | TypeScript/Angular | [06](../knowledge/06-subagents-et-orchestration.md) |
| Injection de prompt | Une issue piégée lue par un agent ; constater l'échec de l'instruction seule, puis le contenir par permissions et bac à sable | Python | [10](../knowledge/10-securite.md) |
| Petite suite d'évaluation | Dix tâches, plusieurs essais, pass@k et pass^k d'un skill ou d'un prompt | Python | [09](../knowledge/09-verification-et-evaluation.md) |
| Outil pour agent | Concevoir un outil MCP consolidé, comparer à l'API brute sur des tâches réelles | TypeScript | [04](../knowledge/04-outils-et-mcp.md) |
| Exécution autonome en CI | Une revue automatique bornée dans GitHub Actions, en `dontAsk` avec liste blanche | Python | [12](../knowledge/12-execution-autonome.md) |
