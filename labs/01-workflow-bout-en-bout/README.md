# Lab 01 — Workflow complet de bout en bout

Chapitre lié : [08 — Workflows de développement](../../knowledge/08-workflows-developpement.md). Composants exercés : plugin [`workflow`](../../plugins/workflow/), plugin [`garde-fous`](../../plugins/garde-fous/).

## Objectif

Conduire une fonctionnalité de bout en bout avec le workflow de l'[ADR-001](../../docs/decisions/ADR-001-workflow-developpement.md) : cadrer, planifier, implémenter en TDD, vérifier, faire relire, et constater ce que chaque étape apporte comme preuve.

## Prérequis

- Claude Code avec les plugins `workflow` et `garde-fous` installés ;
- Python 3.10 ou plus récent, git ;
- environ une heure.

## Mise en place

```sh
cp -r labs/01-workflow-bout-en-bout/depart ~/lab01 && cd ~/lab01
git init -q && git add . && git commit -qm "chore: état de départ" && git tag depart
echo '{ "verification": "python -m unittest discover -s tests -t ." }' > .garde-fous.json
```

Approuver la commande de vérification (voir le README du plugin `garde-fous`), puis lancer Claude Code dans `~/lab01`.

## Énoncé

Le panier (`panier.py`) calcule un total en centimes. Ajouter des **codes promo** :

- `POURCENT10` : 10 % de remise sur le total, arrondie au centime inférieur ;
- `MOINS5` : 5 € de remise, seulement si le total atteint 30 € ;
- un seul code par panier ; un code inconnu ou inapplicable est refusé ;
- la remise suit les ajouts ultérieurs au panier.

Contraintes de déroulement :

1. `/workflow:cadrer` : la spec doit être écrite dans `specs/codes-promo/spec.md`. Répondez aux questions de l'agent ; relevez celles que l'énoncé laissait ouvertes.
2. `/workflow:planifier` : relisez le plan **avant** toute ligne de code, et corrigez-le au moins une fois.
3. `/workflow:implementer`, tâche par tâche.
4. `/workflow:verifier`.
5. `/workflow:relire`, puis enregistrez le rapport du relecteur dans `specs/codes-promo/revue.md`.

## Critères de réussite

Vérifiables par script :

```sh
python labs/01-workflow-bout-en-bout/verifier.py ~/lab01
```

| Critère | Vérification |
|---|---|
| Spec avec objectif, hors-périmètre et au moins trois critères d'acceptation | Structure de `spec.md` |
| Plan d'au moins deux tâches, toutes cochées | `plan.md` |
| Au moins deux commits au format Conventional Commits | `git log depart..HEAD` |
| Tests de l'apprenant verts | `unittest` |
| Tests d'acceptation verts | Tests de [`solution/test_acceptation.py`](solution/test_acceptation.py), exécutés hors de votre dépôt |
| Rapport de revue présent, avec un verdict | `revue.md` |

Les tests d'acceptation ne sont pas copiés dans votre dépôt : l'agent ne doit pas pouvoir modifier le contrôle qui le juge ([chapitre 09](../../knowledge/09-verification-et-evaluation.md)). Ne les lisez qu'après avoir terminé.

## Pour aller plus loin

- Comparer le nombre de questions posées par `cadrer` aux ambiguïtés réelles de l'énoncé (arrondi, ordre d'application, panier vide).
- Introduire volontairement un test affaibli et observer si `verifier` et `relire` le signalent.

## Solution indicative

[`solution/panier.py`](solution/panier.py). Elle n'est qu'une solution possible : votre spec a pu trancher autrement certains points, tant que les tests d'acceptation passent.
