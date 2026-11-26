---
name: cadrer
description: Cadre un changement avant d'écrire du code. Interroge l'utilisateur, une question à la fois, jusqu'à pouvoir rédiger une spec courte (objectif, hors-périmètre, critères d'acceptation vérifiables) dans specs/<slug>/spec.md. À utiliser au début d'une fonctionnalité ou d'un correctif non trivial, ou quand l'utilisateur demande de cadrer, spécifier ou écrire une spec.
license: MIT
metadata:
  chapitre: knowledge/08-workflows-developpement.md
  etape: "1/5"
---

# Cadrer

Première étape du workflow (voir `knowledge/08-workflows-developpement.md`, section « Un workflow de référence en cinq étapes »). Objectif : une spec courte et vérifiable, validée par l'utilisateur, qui servira de mémoire externe aux étapes suivantes.

## Proportionner

Évalue d'abord le risque du changement :

- **trivial** (coquille, renommage local, modification sans effet de comportement) : dis-le, propose de passer directement à l'implémentation et arrête-toi ;
- **standard** : spec courte ;
- **risqué** (sécurité, données, migration, architecture, API publique) : spec complète, hors-périmètre explicite, risques listés.

## Méthode

1. Lis le code et la documentation utiles avant de poser une question dont la réponse s'y trouve. Ne spécule jamais sur du code que tu n'as pas ouvert.
2. Interroge l'utilisateur **une question à la fois**, en proposant ta recommandation. Arrête-toi quand tu peux remplir chaque section du gabarit sans inventer.
3. Choisis un `slug` court en kebab-case et rédige `specs/<slug>/spec.md` selon le gabarit ci-dessous.
4. Présente la spec et demande sa validation. Une spec non validée n'est pas une spec.

## Gabarit

```markdown
# <Titre>

- Statut : brouillon | validée
- Risque : standard | risqué

## Objectif
Une ou deux phrases : le problème résolu et pour qui.

## Hors périmètre
Ce que ce changement ne fera pas.

## Critères d'acceptation
- [ ] CA1 — Comportement observable, vérifiable par un test ou une commande.
- [ ] CA2 — …

## Contraintes
Compatibilité, performance, sécurité, conventions à respecter.

## Questions ouvertes
Ce qui reste à trancher, et qui tranche.
```

## Règles

- Un critère d'acceptation qui ne peut pas être vérifié par une commande ou un test doit être reformulé.
- Pas de solution technique détaillée dans la spec : c'est le rôle du plan.
- Étape suivante : `planifier`.
