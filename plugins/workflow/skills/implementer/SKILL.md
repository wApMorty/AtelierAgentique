---
name: implementer
description: Implémente la prochaine tâche non cochée de specs/<slug>/plan.md en TDD (test qui échoue, code minimal, refactorisation), vérifie, puis crée un commit atomique. Ne se déclenche que sur demande explicite de l'utilisateur.
license: MIT
disable-model-invocation: true
metadata:
  chapitre: knowledge/08-workflows-developpement.md
  etape: "3/5"
---

# Implémenter

Troisième étape du workflow (voir `knowledge/08-workflows-developpement.md`). Ce skill crée des commits : il ne se déclenche que sur demande explicite (`disable-model-invocation`, extension propre à Claude Code, voir `docs/decisions/ADR-003-portabilite.md`).

## Méthode, pour une seule tâche

1. Lis `plan.md` et la spec. Prends la tâche désignée par l'utilisateur, sinon la première non cochée dont les dépendances sont cochées.
2. **Rouge** : écris le test prévu par le plan. Lance-le et montre qu'il échoue pour la bonne raison.
3. **Vert** : écris le code minimal qui le fait passer.
4. **Refactorise** si nécessaire, sans changer le comportement.
5. Lance la **commande de vérification** du plan et montre sa sortie.
6. Crée un commit atomique en Conventional Commits qui référence la tâche (`feat(<portée>): … (T1)`), puis coche la tâche dans `plan.md`.
7. Rends compte en trois lignes au plus : tâche, preuve (sortie de la vérification), tâche suivante.

## Règles

- Ne modifie ni ne supprime un test existant sans l'accord explicite de l'utilisateur. Un test qui échoue signale un problème, pas un obstacle.
- Ne code pas pour les seules entrées de test ; pas de valeurs en dur destinées à faire passer un test.
- Aucune fonctionnalité non demandée par la tâche.
- Ne mélange pas changement de structure et changement de comportement dans un même commit.
- Après deux tentatives infructueuses sur la même erreur, arrête-toi et expose le problème au lieu d'essayer une troisième fois.
- Ne pousse jamais.
- Étape suivante quand toutes les tâches sont cochées : `verifier`, puis `relire`.
