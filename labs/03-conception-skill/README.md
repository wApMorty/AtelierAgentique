# Lab 03 — Conception d'un skill

Chapitre lié : [05 — Skills](../../knowledge/05-skills.md). Voir aussi [03 — Prompting pour agents](../../knowledge/03-prompting-pour-agents.md) et [13 — Portabilité](../../knowledge/13-portabilite-et-standards.md).

## Objectif

Concevoir un skill portable qui encode une convention d'équipe Angular, avec une description qui le déclenche au bon moment, des références chargées à la demande et un script qui rend la vérification déterministe.

## Prérequis

- Node.js 20 ou plus récent, Python 3.10 ou plus récent ;
- Claude Code (ou un autre outil qui lit les skills) et, pour l'essai réel, une application Angular récente ;
- environ 45 minutes.

## Énoncé

Créer, dans `labs/03-conception-skill/composant-angular/`, un skill qui fait créer à l'agent un composant Angular conforme à ces conventions d'équipe (fictives) :

- fichiers `<nom>.ts`, `<nom>.html`, `<nom>.spec.ts` dans un dossier `<nom>/` ;
- sélecteur `app-<nom>` ;
- composant autonome, détection `OnPush` ;
- `input()` et `output()` au lieu des décorateurs `@Input` et `@Output`.

Le skill doit comporter :

1. un `SKILL.md` au format standard (champs `name`, `description` et, au besoin, `license`, `metadata`), de moins de 200 lignes ;
2. un dossier `references/` qui détaille les conventions, lu seulement à la demande ;
3. un script `scripts/verifier.mjs` qui exporte `verifierComposant(dossier)` (liste des écarts, vide si conforme) et s'utilise en ligne de commande (code 1 si non conforme) ; le skill demande à l'agent de le lancer après génération.

Puis évaluer le déclenchement : dans Claude Code, avec le skill installé, soumettre les six demandes ci-dessous et noter si le skill est chargé.

| # | Demande | Déclenchement attendu | Observé |
|---|---|---|---|
| 1 | « Crée un composant qui affiche une carte produit » | oui | |
| 2 | « Ajoute une vue de profil utilisateur à l'appli Angular » | oui | |
| 3 | « Génère le composant de pagination pour la liste » | oui | |
| 4 | « Corrige le test qui échoue dans panier.service.spec.ts » | non | |
| 5 | « Explique la différence entre OnPush et Default » | non | |
| 6 | « Écris un script Python qui renomme des fichiers » | non | |

## Critères de réussite

Automatiques :

```sh
node --test labs/03-conception-skill/tests/
```

| Test | Ce qu'il vérifie |
|---|---|
| Format | `SKILL.md` conforme au standard et aux extensions admises du dépôt (`.github/scripts/verifier_skills.py`) |
| Taille et références | Moins de 200 lignes, renvoi vers `references/` |
| Script, cas conforme | Aucun écart sur le composant de référence de `tests/fixtures/conforme/` |
| Script, cas non conforme | Chaque écart détecté sur `tests/fixtures/non-conforme/` |
| Ligne de commande | Codes de sortie 0 et 1 |

Observé : au moins cinq déclenchements corrects sur six dans le tableau d'évaluation. En cas d'échec, retravailler la description, pas le corps du skill : c'est elle seule que le modèle voit au moment de choisir.

## Questions de réflexion

- Quelle partie de la convention relève du script plutôt que de l'instruction, et pourquoi ?
- Combien de tokens le skill coûte-t-il en permanence, et à l'invocation (`claude plugin details` donne une estimation pour un plugin) ?
- Que faudrait-il changer pour que le skill fonctionne sous Copilot et Codex ([chapitre 13](../../knowledge/13-portabilite-et-standards.md)) ?

## Solution indicative

[`solution/composant-angular/`](solution/composant-angular/), vérifiable par :

```sh
LAB03_SKILL=labs/03-conception-skill/solution/composant-angular node --test labs/03-conception-skill/tests/
```
