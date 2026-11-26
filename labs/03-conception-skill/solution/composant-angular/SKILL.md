---
name: composant-angular
description: Crée un composant Angular conforme aux conventions de l'équipe (standalone, OnPush, inputs et outputs par fonctions, fichier de test) puis le vérifie avec un script. À utiliser quand l'utilisateur demande de créer, générer ou ajouter un composant Angular, une vue ou un élément d'interface dans une application Angular.
license: MIT
metadata:
  chapitre: knowledge/05-skills.md
---

# Composant Angular

Crée un composant dans `src/app/<chemin>/<nom>/` selon les conventions de [references/conventions.md](references/conventions.md), puis le vérifie.

## Méthode

1. Déduis le nom en kebab-case et le dossier cible ; s'ils sont ambigus, pose une seule question.
2. Lis [references/conventions.md](references/conventions.md) et un composant existant du projet, s'il y en a un, pour reprendre son style.
3. Crée trois fichiers : `<nom>.ts`, `<nom>.html` et `<nom>.spec.ts`. Le test vérifie au minimum le rendu et chaque input.
4. Vérifie de façon déterministe :

   ```sh
   node <dossier de ce skill>/scripts/verifier.mjs src/app/<chemin>/<nom>
   ```

   Corrige jusqu'à ce que le script ne signale plus rien, puis lance les tests du projet.
5. Rends compte : fichiers créés, sortie du script, sortie des tests.

## Règles

- N'ajoute aucune dépendance.
- Ne modifie pas d'autre composant sans le demander.
