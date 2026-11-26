---
name: relire
description: Fait relire un changement par un relecteur indépendant, en contexte neuf, contre sa spec (correction, sécurité, tests affaiblis), en ignorant le style. À utiliser avant d'ouvrir une PR, ou quand l'utilisateur demande une revue indépendante du travail réalisé.
license: MIT
metadata:
  chapitre: knowledge/08-workflows-developpement.md
  etape: "5/5"
---

# Relire

Cinquième étape du workflow (voir `knowledge/08-workflows-developpement.md` et `knowledge/09-verification-et-evaluation.md`). La valeur de la revue tient à l'indépendance du relecteur : il ne doit pas hériter de la conversation qui a produit le code.

## Méthode

1. Détermine la référence de base du changement (branche principale ou commit de départ) et le chemin de la spec.
2. Lance le subagent `relecteur` avec un prompt autoporteur qui contient uniquement : le chemin de la spec, le chemin du plan, la référence de base. Ne lui transmets ni l'historique de la conversation ni ton avis sur le code.
3. Présente son rapport tel quel, trié par gravité.
4. Ne corrige rien automatiquement : propose les corrections et laisse l'utilisateur choisir.
5. Après correction, une nouvelle revue est possible ; au troisième tour sans convergence, arrête et expose les désaccords à l'utilisateur.

## Sans subagent

Dans un outil sans subagents, ouvre une session neuve et donne-lui les mêmes trois informations ainsi que les consignes de `agents/relecteur.md` du plugin.

Étape suivante : PR, relue par un humain selon le risque indiqué dans la spec.
