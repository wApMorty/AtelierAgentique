---
chapitre: 15
titre: Panorama des outils
statut: brouillon
derniere_revision: 2026-11-27
---

# 15 — Panorama des outils

> Situer les principaux agents de code et savoir les comparer sur des critères durables plutôt que sur un classement du mois.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- situer les principaux outils par forme, éditeur et modèle de déploiement ;
- comparer leurs capacités d'extension (instructions, skills, agents, hooks, MCP, exécution distante) ;
- appliquer une grille de choix qui ne dépend pas d'un benchmark ;
- reconnaître les signaux de volatilité du marché.

## Concepts clés

**Forme.** CLI dans le terminal, extension ou IDE, application de bureau, agent cloud qui travaille en arrière-plan et rend une PR. La plupart des outils couvrent désormais plusieurs formes.

**Modèle unique ou multi-fournisseurs.** Certains outils sont liés aux modèles de leur éditeur, d'autres laissent choisir parmi plusieurs fournisseurs.

## Mécanismes

### Vue d'ensemble

Relevé effectué sur les pages officielles le 2026-11-27 **(Daté)** ; « nd » signifie que les pages consultées ne le précisent pas [1]–[9].

| Outil | Éditeur | Formes | Modèles | Code ouvert |
|---|---|---|---|---|
| Claude Code | Anthropic | CLI, VS Code, JetBrains, bureau, web | Claude ; fournisseurs tiers pris en charge selon les formes | nd |
| Codex | OpenAI | CLI, extension IDE, bureau, web, cloud | Modèles OpenAI | nd |
| GitHub Copilot | GitHub | IDE multiples, github.com, CLI, cloud | Choix parmi plusieurs modèles | nd |
| Cursor | Cursor | Application de bureau | Multi-fournisseurs | nd |
| Gemini CLI | Google | CLI | Gemini | Oui (Apache-2.0) |
| Antigravity CLI | Google | CLI (TUI) | nd | nd |
| OpenCode | nd | TUI, bureau, web | Multi-fournisseurs | Oui |
| Amp | nd | Web, CLI, applications | Multi-fournisseurs | nd |
| Kiro | AWS (d'après les mentions légales) | IDE, extension VS Code, CLI, web | nd | nd |

### Capacités d'extension

| Outil | AGENTS.md | Skills | Agents | Hooks | MCP | Exécution distante |
|---|---|---|---|---|---|---|
| Claude Code | Oui (conditions, [chapitre 13](13-portabilite-et-standards.md)) | Oui | Oui | Oui | Oui | Sessions web, tâches planifiées |
| Codex | Oui | Oui | Oui | Oui | Oui | Cloud, tâches planifiées |
| Copilot | Oui | Oui | Oui (selon surface) | Oui | Oui | Agent cloud |
| Cursor | nd | Oui | nd | nd | Oui | nd |
| Gemini CLI | nd (fichiers `GEMINI.md`) | nd | nd | nd | Oui | nd |
| Antigravity CLI | nd | Oui | Oui | Oui | Oui | Sessions locales en arrière-plan |
| OpenCode | nd | nd | nd | nd | Oui | nd |
| Amp | Oui | Oui | Oui | nd | Oui | Machines cloud par fil |
| Kiro | nd (« steering ») | Oui | Oui | Oui | Oui | Sessions cloud |

Deux constats : la convergence fonctionnelle est forte (MCP partout, skills et hooks chez la plupart), et les **formats** restent propres à chaque outil hors AGENTS.md, Agent Skills et MCP ([chapitre 13](13-portabilite-et-standards.md)).

### Signaux de volatilité en 2026

Relevés sur les pages officielles [1]–[9] :

- Google a déplacé l'accès gratuit et les abonnements individuels de Gemini CLI vers Antigravity CLI le 18 juin 2026 ; le dépôt de Gemini CLI vise désormais les offres entreprise [5] ;
- GitHub remplace l'expérience « Copilot cloud agent » par « Copilot in the cloud » pour les offres payantes à partir du 28 octobre 2026 [3] ;
- Claude Code a renommé ses *routines* en « cloud scheduled tasks » [1] ;
- la documentation de Codex a migré de domaine [2].

Un panorama a donc une durée de vie de quelques mois ; c'est l'une des cibles prioritaires de la [veille](../veille/).

### Grille de choix

Les classements par benchmark mesurent un modèle dans un harnais donné, pas votre usage ([chapitre 09](09-verification-et-evaluation.md)). Critères plus durables :

1. **Standards ouverts** : lecture d'AGENTS.md, format Agent Skills, MCP — ils conditionnent la réversibilité du choix.
2. **Contrôle déterministe** : hooks, permissions déclaratives, bac à sable.
3. **Exécution distante** encadrée : branches, PR, protections.
4. **Politique de données et hébergement** compatibles avec le contexte de l'équipe.
5. **Coût prévisible** : quotas publiés ou non ([chapitre 11](11-couts-quotas-modeles.md)).
6. **Choix du modèle** : lié à un fournisseur ou non.

## Bonnes pratiques

1. **Choisir par la grille, essayer sur son dépôt** : une semaine de tâches réelles vaut mieux qu'un classement.
2. **Rester portable** : instructions et skills standards, pour pouvoir changer d'outil ([chapitre 13](13-portabilite-et-standards.md)).
3. **Revoir le panorama régulièrement** : la veille du dépôt le signale.

## Pièges et anti-patterns

- **Les comparatifs de blogs** : versions incohérentes, affiliations non déclarées ; une recherche ciblée sur ce sujet n'a renvoyé presque que des sources secondaires de qualité inégale.
- **Le verrouillage par la configuration** : un harnais entièrement écrit dans des formats propriétaires.
- **Confondre modèle et outil** : le même modèle se comporte différemment selon le harnais ([chapitre 01](01-fondamentaux-boucle-agentique.md)).

## État du débat

- **Outil unique ou combinaison ?** Plusieurs retours de praticiens décrivent l'usage simultané de plusieurs agents selon la tâche ; aucune source primaire consultée ne le mesure. **Émergent.**
- **Code ouvert ou non** : OpenCode et Gemini CLI publient leur code [5], [6] ; l'intérêt pratique (auditabilité, choix du modèle) se paie en intégration. **Opinion.**

## Dans ce dépôt

- **Composants** : le système cible Claude Code et documente ses équivalents sous Copilot et Codex ([ADR-003](../docs/decisions/ADR-003-portabilite.md)).
- **Labs** : sans objet.

## Sources

Pages officielles consultées le 2026-11-27.

1. **[O]** Anthropic, *Claude Code overview*. <https://code.claude.com/docs/en/overview>
2. **[O]** OpenAI, documentation Codex. <https://learn.chatgpt.com/docs>
3. **[O]** GitHub, *About GitHub Copilot coding agent* et *Customization cheat sheet*. <https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent>
4. **[O]** Cursor, documentation (lue en partie sous forme résumée). <https://cursor.com/docs>
5. **[O]** Google, dépôt *gemini-cli* (README). <https://github.com/google-gemini/gemini-cli>
6. **[O]** OpenCode, documentation. <https://opencode.ai/docs>
7. **[O]** Amp, *Manual* (fonctionnalités relevées dans la navigation). <https://ampcode.com/manual>
8. **[O]** Kiro, documentation. <https://kiro.dev/docs>
9. **[O]** Google, *Antigravity CLI*. <https://antigravity.google/product/antigravity-cli>
