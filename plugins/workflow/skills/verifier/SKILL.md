---
name: verifier
description: Vérifie qu'un changement satisfait sa spec en exécutant la commande de vérification du projet et en associant chaque critère d'acceptation à une preuve (test, sortie de commande). À utiliser avant une revue ou une PR, ou quand l'utilisateur demande si le travail est terminé ou si les critères sont remplis.
license: MIT
metadata:
  chapitre: knowledge/09-verification-et-evaluation.md
  etape: "4/5"
---

# Vérifier

Quatrième étape du workflow (voir `knowledge/09-verification-et-evaluation.md`). Elle produit des preuves, pas des affirmations.

## Méthode

1. Lis la spec et le plan ; récupère la commande de vérification.
2. Exécute-la et conserve sa sortie (résumée si elle est longue, mais avec les lignes de synthèse et toutes les erreurs).
3. Pour chaque critère d'acceptation, identifie la preuve : nom du test qui le couvre et résultat, ou commande et sortie. Un critère sans preuve est « non vérifié », même si tu penses qu'il est rempli.
4. Vérifie que le diff ne contient aucune suppression ni affaiblissement de test ; signale-le sinon.
5. Rends le rapport ci-dessous. Ne corrige rien sans que l'utilisateur le demande.

## Rapport

```markdown
## Vérification — <slug>

Commande : `<commande>` → succès | échec

| Critère | Preuve | Statut |
|---|---|---|
| CA1 | `test_x` (sortie ci-dessus) | vérifié |
| CA2 | — | non vérifié |

Tests modifiés ou supprimés : aucun | liste
```

Étape suivante : `relire`.
