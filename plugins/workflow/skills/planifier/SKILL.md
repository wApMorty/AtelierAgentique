---
name: planifier
description: Transforme une spec validée en plan d'implémentation découpé en tâches testables isolément, écrit dans specs/<slug>/plan.md, sans modifier le code. À utiliser après le cadrage, ou quand l'utilisateur demande un plan, un découpage ou une estimation des tâches.
license: MIT
metadata:
  chapitre: knowledge/08-workflows-developpement.md
  etape: "2/5"
---

# Planifier

Deuxième étape du workflow (voir `knowledge/08-workflows-developpement.md`). Le plan est le point de contrôle le moins coûteux : une erreur de conception corrigée ici coûte une phrase.

## Méthode

1. Lis `specs/<slug>/spec.md`. Si elle n'est pas marquée « validée », demande-le avant de continuer.
2. Explore le code **en lecture seule**. Si l'outil le permet, active le mode plan ou délègue l'exploration volumineuse à un subagent de lecture qui te renvoie une synthèse courte (voir `knowledge/02-ingenierie-du-contexte.md`).
3. Découpe en tâches qui respectent toutes ces conditions :
   - chacune est testable isolément et contribue à au moins un critère d'acceptation ;
   - chacune tient dans un commit ;
   - changements de structure et de comportement sont dans des tâches distinctes.
4. Rédige `specs/<slug>/plan.md` selon le gabarit, puis demande à l'utilisateur de le relire.

## Gabarit

```markdown
# Plan — <Titre>

Spec : ./spec.md
Commande de vérification : <commande unique qui lance tests, lint, typage>

| # | Tâche | Fichiers | Test écrit d'abord | Critères | Dépend de | Parallélisable |
|---|---|---|---|---|---|---|
| T1 | … | … | … | CA1 | — | non |

## Suivi
- [ ] T1
- [ ] T2

## Risques et points d'attention
```

## Règles

- Aucune modification de code à cette étape.
- Une tâche n'est « parallélisable » que si ses fichiers sont disjoints de ceux des autres tâches et qu'elle ne dépend d'aucune (voir `knowledge/06-subagents-et-orchestration.md`).
- Si la commande de vérification du projet est inconnue, demande-la : sans elle, l'étape de vérification est impossible.
- Étape suivante : `implementer`.
