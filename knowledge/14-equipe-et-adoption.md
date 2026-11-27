---
chapitre: 14
titre: Équipe et adoption
statut: relu
derniere_revision: 2026-11-27
---

# 14 — Équipe et adoption

> Introduire les agents de code dans une équipe en s'appuyant sur ce que l'on sait réellement de leurs effets, et non sur ce que l'on en dit.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- présenter l'état réel des preuves sur la productivité ;
- expliquer pourquoi l'IA amplifie les forces et faiblesses existantes d'une organisation ;
- proposer une organisation de la revue fondée sur le risque ;
- identifier les capacités d'équipe qui conditionnent le bénéfice ;
- anticiper les résistances et les dérives.

## Concepts clés

**Effet amplificateur.** Selon DORA, le rôle premier de l'IA est d'être « an amplifier, magnifying an organization's existing strengths and weaknesses » [1].

**Revue par niveau de risque.** Nombre et nature des approbations fixés par le risque du changement, non par son auteur, humain ou agent [2].

## Mécanismes

### Ce que l'on sait de la productivité

| Source | Méthode | Résultat | Limites |
|---|---|---|---|
| METR, début 2025 [3] | Essai randomisé, développeurs expérimentés sur leurs propres dépôts | Tâches 19 % plus longues avec IA, alors que les participants s'estimaient 20 % plus rapides | Outils de début 2025 ; METR juge que le résultat ne reflète plus nécessairement les outils actuels |
| METR, suivi lancé en août 2025 [3] | Même protocole, 57 développeurs, plus de 800 tâches | Estimations d'accélération (−18 % et −4 % de durée), intervalles larges | Effets de sélection : des développeurs refusent de travailler sans IA ; METR y voit « only very weak evidence » |
| METR, enquête de mai 2026 [4] | Déclaratif, 349 répondants | Gains médians ressentis importants | Échantillon de convenance, auto-déclaration ; METR invite à la prudence sur l'ampleur |
| DORA 2025 [5] | Enquête, près de 5 000 professionnels | 90 % d'usage, plus de 80 % de gains de productivité déclarés ; débit de livraison en hausse | Déclaratif |
| Équipe Claude Code [2] | Retour d'expérience interne | PR fusionnées doublées, part de retours arrière en baisse de plus de 40 % | Auto-déclaré, éditeur |

Conclusion prudente : **l'adoption est massive, l'effet ressenti est positif, l'effet mesuré de façon contrôlée reste incertain.** Présenter des gains chiffrés à une équipe sans ces nuances expose à la déception.

### La confiance

L'enquête Stack Overflow 2025 relève que 84 % des répondants utilisent ou prévoient d'utiliser des outils d'IA, mais que « More developers actively distrust the accuracy of AI tools (46%) than trust it (33%) » [6]. DORA observe de même qu'environ 30 % des professionnels font peu ou pas confiance au code généré [5]. Cette méfiance est saine : elle se traite par la vérification ([chapitre 09](09-verification-et-evaluation.md)), pas par la persuasion.

### Les capacités qui conditionnent le bénéfice

DORA propose un modèle de sept capacités qui amplifient l'effet de l'IA [7] : une position claire et communiquée sur l'IA ; des écosystèmes de données sains ; des données internes accessibles à l'IA ; de solides pratiques de gestion de versions ; le travail en petits lots ; l'orientation utilisateur ; une plateforme interne de qualité. Plusieurs recoupent directement les pratiques de ce dépôt : petits lots et gestion de versions (un commit par tâche, [chapitre 08](08-workflows-developpement.md)), plateforme (marketplace de plugins partagé).

### Organiser la revue

L'équipe Claude Code vise « the minimum amount of human review time that doesn't raise reverts or incidents » [2] : revue automatique sur chaque PR, puis aucune, une ou deux approbations humaines selon le risque [2]. L'équipe OpenAI de l'expérience « harness engineering » va plus loin, les humains pouvant relire les PR « but aren't required to » [8]. Ces deux organisations reposent sur un harnais de vérification étendu ; les transposer sans lui revient à supprimer la revue.

### Le rôle de l'ingénieur

OpenAI résume son expérience par « Humans steer. Agents execute. », le travail principal devenant de concevoir l'environnement et de préciser l'intention [8]. Le goût et le jugement y sont capturés une fois sous forme de règles vérifiées automatiquement, l'équipe reconnaissant qu'elle apprend encore où le jugement humain apporte le plus [8]. Simon Willison souligne que ces outils « make software engineering even harder » au sens où ils exigent davantage de discipline d'ingénierie [9].

## Bonnes pratiques

1. **Partir des faits** : présenter l'état des preuves avec ses incertitudes [3], [4], [5].
2. **Formaliser une position d'équipe** sur l'usage des agents (première capacité DORA) [7].
3. **Investir d'abord dans la vérification** (tests, CI, revue) : c'est elle que l'IA amplifie [1].
4. **Revue selon le risque**, avec des critères écrits [2].
5. **Partager le harnais** : instructions, skills et hooks versionnés et distribués, plutôt que des configurations individuelles.
6. **Mesurer localement** : retours arrière, incidents, délai de revue, avant et après.

## Pièges et anti-patterns

- **Promettre un multiplicateur de productivité** sans données contrôlées.
- **Le théâtre de la validation humaine** : approbations sans lecture, classées en *Caution* par Thoughtworks [10].
- **Supprimer la revue avant d'avoir le harnais** qui la remplace.
- **Laisser chacun configurer son agent** : comportements divergents, savoir non partagé.
- **Mesurer le volume** (lignes, PR) plutôt que la stabilité (retours arrière, incidents).

## État du débat

- **Productivité** : **Contesté** et en évolution rapide ; METR lui-même revoit son protocole [3].
- **Place de la revue humaine** : **Contesté** ; voir [chapitre 08](08-workflows-developpement.md).
- **Stabilité** : DORA 2025 associe désormais l'adoption de l'IA à un débit plus élevé [5] ; son effet sur la stabilité est rapporté de façon contradictoire par les sources secondaires consultées **(Non vérifié)** dans le rapport complet.

## Dans ce dépôt

- **Composants** : le marketplace de plugins sert de harnais partagé ; [`talks/`](../talks/) fournit le matériel de présentation.
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[P]** DORA, *2025 State of AI-assisted Software Development*. <https://dora.dev/dora-report-2025/>
2. **[O]** Osmani, Lunt, Wang (équipe Claude Code), *How the Claude Code team does code review*, 15/10/2026. Chiffres auto-déclarés. <https://claude.dev/blog/solving-code-review-at-anthropic>
3. **[P]** METR, *We are Changing our Developer Productivity Experiment Design*, 24/02/2026. <https://metr.org/blog/2026-02-24-uplift-update/>
4. **[P]** Becker (METR), *Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity*, 11/05/2026. <https://metr.org/blog/2026-05-11-ai-usage-survey/>
5. **[P]** Salva (Google), *How are developers using AI? Inside our 2025 DORA report*, 23/09/2025. <https://blog.google/technology/developers/dora-report-2025/>
6. **[P]** Stack Overflow, *2025 Developer Survey — AI*. <https://survey.stackoverflow.co/2025/ai>
7. **[P]** DORA, *AI Capabilities Model* (intitulés relevés sur la page des questions, mise à jour du 25/11/2025). <https://dora.dev/ai/capabilities-model/questions/>
8. **[O]** Lopopolo (OpenAI), *Harness engineering: leveraging Codex in an agent-first world*, 11/02/2026. <https://openai.com/index/harness-engineering/>
9. **[E]** Willison, notes du tag *coding-agents* (24/09/2026). <https://simonwillison.net/tags/coding-agents/>
10. **[P]** Thoughtworks, *Technology Radar*, vol. 35, novembre 2026 (anneaux relevés, fiches non lues). <https://www.thoughtworks.com/radar>
