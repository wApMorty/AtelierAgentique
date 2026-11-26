---
name: talk
description: Génère le plan d'une présentation sur l'engineering agentique à partir d'un ou plusieurs chapitres de knowledge/, selon le gabarit talks/_gabarit.md (public, durée, message clé, déroulé minuté, démonstration, sources, questions anticipées). À utiliser quand l'utilisateur prépare un talk, une présentation interne, un atelier ou un lightning talk.
license: MIT
metadata:
  gabarit: talks/_gabarit.md
  chapitre: knowledge/14-equipe-et-adoption.md
---

# Plan de présentation

## Entrées

Demande à l'utilisateur ce qui manque parmi : chapitres sources, public (rôle, niveau), durée, contexte (réunion d'équipe, conférence interne, atelier). Une question à la fois, avec une proposition. Ne demande pas le message clé : propose-le.

## Méthode

1. Lis les chapitres sources en entier, en particulier « État du débat » et « Sources ».
2. Propose **un seul message clé**, formulé pour ce public, et fais-le valider.
3. Dimensionne le déroulé : environ une idée par tranche de cinq minutes, une démonstration seulement si la durée dépasse quinze minutes, dix à vingt pour cent du temps pour les questions.
4. Choisis une démonstration qui prouve le message clé avec les composants du dépôt (plugins, labs). Prévois un plan B.
5. Reprends chaque chiffre avec sa source, sa date et son niveau ; pour un chiffre auto-déclaré ou une étude unique, indique la précaution orale à employer.
6. Anticipe les objections, en priorité celles que les sections « État du débat » marquent comme contestées.
7. Écris le plan dans `talks/<aaaa-mm>-<slug>.md` selon `talks/_gabarit.md`.

## Règles

- Aucune affirmation absente des chapitres sources ; si le sujet l'exige, signale le manque au lieu de compléter de mémoire.
- Ne présente jamais un point contesté comme acquis, ni un gain de productivité comme démontré (voir `knowledge/14-equipe-et-adoption.md`).
- Le dépôt est public : aucune référence à un employeur, un client ou un projet interne dans le plan.
