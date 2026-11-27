---
chapitre: 02
titre: Ingénierie du contexte
statut: relu
derniere_revision: 2026-11-27
---

# 02 — Ingénierie du contexte

> Décider, à chaque étape, de ce qui entre dans la fenêtre de contexte d'un agent, de ce qui en sort et de ce qui reste dehors, parce que la qualité du raisonnement en dépend davantage que la formulation du prompt.

## Objectifs

À l'issue de ce chapitre, le lecteur sait :

- expliquer pourquoi un contexte plus long dégrade un agent, et nommer les modes de défaillance observés ;
- décrire ce que Claude Code charge dans la fenêtre au démarrage, à la demande, et ce qui survit à une compaction ;
- appliquer les quatre leviers (écrire, sélectionner, compresser, isoler) avec les mécanismes concrets de l'outil ;
- tenir compte du cache de préfixe dans ses choix de session ;
- situer les débats ouverts : partage de contexte entre agents, utilité réelle des fichiers d'instructions.

## Concepts clés

**Fenêtre de contexte.** L'ensemble des tokens que le modèle reçoit à chaque requête : instructions système, définitions d'outils, fichiers d'instructions, historique de la conversation, sorties d'outils. Un agent de code renvoie l'intégralité de la conversation à chaque tour : « Claude Code sends your full conversation with every request » [6].

**Ingénierie du contexte.** Anthropic la définit comme l'art de trouver « the smallest possible set of high-signal tokens » qui maximise la probabilité du résultat voulu [1]. Elle englobe le prompt engineering : le prompt n'est qu'une des sources de tokens, et pour un agent ce n'est généralement pas la plus volumineuse.

**Context rot.** Dégradation des performances d'un modèle à mesure que la longueur de l'entrée augmente, y compris sur des tâches simples. Le terme vient d'un rapport technique de Chroma qui a mesuré le phénomène sur 18 modèles [9].

**Divulgation progressive** (*progressive disclosure*). Ne charger d'abord qu'une description courte d'une ressource (skill, outil, règle), et son contenu complet seulement quand la tâche le requiert [2], [3].

**Compaction.** Remplacement de l'historique par un résumé quand la fenêtre approche de sa limite [2].

**Isolation.** Exécution d'une sous-tâche dans une fenêtre séparée, dont seul le résultat revient au contexte principal [2], [7].

**Cache de préfixe.** Réutilisation, côté fournisseur, du calcul déjà effectué sur un début de requête identique au caractère près [5].

## Mécanismes

### Pourquoi le contexte se dégrade

Le rapport de Chroma [9] établit trois résultats utiles au praticien :

- **Les modèles n'exploitent pas leur contexte de façon uniforme** : « models do not use their context uniformly ». La performance baisse avec la longueur, d'autant plus vite que l'information utile ressemble peu à la question posée.
- **Les distracteurs coûtent cher** : un seul passage proche mais non pertinent suffit à faire baisser la performance, et plusieurs distracteurs cumulent leurs effets.
- **Le bruit pèse plus que le volume brut** : sur LongMemEval, une version focalisée (environ 300 tokens) fait mieux que la version complète (environ 113 000 tokens) contenant la même information.

Les auteurs ne savent pas expliquer certains de ces effets (« we do not have a definitive answer ») et notent que la difficulté de la tâche peut être confondue avec la longueur [9]. Le constat de dégradation, lui, est robuste sur l'ensemble des modèles testés.

Drew Breunig classe les défaillances observées en quatre modes [10], qui servent de grille de diagnostic :

| Mode | Description | Manifestation typique chez un agent de code |
|---|---|---|
| Empoisonnement | Une erreur ou hallucination entre dans le contexte et y est ensuite tenue pour vraie | L'agent répète une hypothèse fausse sur l'API d'une bibliothèque lue trois tours plus tôt |
| Distraction | Le contexte accumulé l'emporte sur ce que le modèle a appris | L'agent répète des actions passées au lieu d'en concevoir de nouvelles |
| Confusion | Du contenu superflu influence la réponse | Trop d'outils disponibles dégradent le choix d'outil |
| Conflit | Des éléments du contexte se contredisent | Une consigne de début de session contredit une correction ultérieure |

Les exemples chiffrés de Breunig proviennent de benchmarks tiers et d'anecdotes qu'il cite ; ils illustrent les modes sans les quantifier de façon générale [10].

### Anatomie du contexte d'une session Claude Code

Avant le premier message, Claude Code charge [2], [3], [4] :

| Élément | Chargement | Ordre de grandeur, limite |
|---|---|---|
| Prompt système, informations d'environnement | Au démarrage | Fixe |
| `CLAUDE.md` du répertoire courant et de tous ses parents, `CLAUDE.local.md` | Au démarrage, concaténés de la racine vers le répertoire courant | Cible recommandée : moins de 200 lignes par fichier [4] |
| `AGENTS.md` | Au démarrage, **seulement en l'absence de CLAUDE.md** | Voir [chapitre 13](13-portabilite-et-standards.md) |
| Imports `@fichier` | Avec le fichier qui les contient, jusqu'à quatre niveaux | Un import ne réduit pas le coût en contexte [4] |
| Règles `.claude/rules/` sans `paths` | Au démarrage | Comme un CLAUDE.md |
| Mémoire automatique (`MEMORY.md`) | Au démarrage | 200 premières lignes ou 25 Ko [2] |
| Descriptions des skills | Au démarrage | Budget proportionnel à la fenêtre ; 1 536 caractères par entrée **(Daté)** [3] |
| Noms des outils MCP | Au démarrage ; définitions complètes chargées à la demande par *tool search* | [2], [8] |
| Descriptions des subagents | Au démarrage | Avertissement au-delà de 15 000 tokens cumulés [7] |

Sont chargés **à la demande** : le corps d'un skill quand il est invoqué, les règles dont le champ `paths` correspond à un fichier lu ou modifié, les `CLAUDE.md` des sous-répertoires dès qu'un fichier de ce sous-répertoire est touché [4], les définitions d'outils MCP [8].

La commande `/context` affiche l'occupation de la fenêtre par catégorie ; `/context all` liste les fichiers de mémoire effectivement chargés [4]. C'est le premier réflexe de diagnostic.

### Les quatre leviers

Lance Martin regroupe les techniques en quatre familles [12]. Elles se transposent directement :

| Levier | Principe | Mécanismes Claude Code |
|---|---|---|
| **Écrire** | Sortir l'information de la fenêtre vers un support persistant | `SPEC.md`, plan, notes de progression ; mémoire automatique ; CLAUDE.md |
| **Sélectionner** | Ne faire entrer que ce qui sert la tâche en cours | Divulgation progressive des skills et outils ; règles par chemin ; lecture ciblée (`grep`, plages de lignes) plutôt que fichiers entiers |
| **Compresser** | Réduire le volume en conservant le signal | Compaction automatique ou `/compact <focus>` ; section « Compact Instructions » dans CLAUDE.md [2], [6] |
| **Isoler** | Exécuter une sous-tâche dans une fenêtre séparée | Subagents, dont seul le résumé revient [2] ; sessions distinctes |

Anthropic décrit la même logique pour les tâches longues : compaction, prise de notes structurée hors fenêtre, sous-agents qui renvoient une synthèse condensée, souvent de 1 000 à 2 000 tokens [1]. La récupération « juste à temps » (chemins de fichiers, commandes `head`/`tail`) combinée à un socle chargé d'emblée (CLAUDE.md) y est présentée comme une approche hybride [1].

### Ce que la compaction conserve

La compaction est une requête de résumé : elle relit l'historique et le remplace [5]. Claude Code réinjecte ensuite une partie du contexte depuis le disque [3] :

| Conservé ou réinjecté | Perdu ou résumé |
|---|---|
| Prompt système et style de sortie | Détails de la conversation, y compris des consignes données oralement en début de session [2] |
| `CLAUDE.md` racine et règles sans `paths`, relus depuis le disque | Règles par chemin et `CLAUDE.md` imbriqués, jusqu'à ce qu'un fichier déclencheur soit à nouveau touché |
| Mémoire automatique | Contenu complet des fichiers lus : seuls les cinq plus récemment modifiés sont relus, et un fichier de plus de 5 000 tokens revient sous forme de chemin |
| Plan issu du mode plan | Corps des skills au-delà de 5 000 tokens chacun et 25 000 au total, les plus anciens d'abord |
| Descriptions des skills, reconstruites | — |

Conséquence directe : **toute règle qui doit survivre à une compaction vit dans un fichier, pas dans la conversation** [2]. Les hooks `PreCompact` et `PostCompact`, ainsi qu'un hook `SessionStart` filtré sur `compact`, permettent de réinjecter du contexte de façon déterministe après coup [3], [21].

### L'isolation par subagents

Un subagent travaille dans sa propre fenêtre ; ses appels d'outils n'entrent pas dans le contexte principal, qui ne reçoit qu'un résumé final [2]. Les subagents intégrés Explore et Plan démarrent sans les fichiers CLAUDE.md [7]. L'isolation a deux effets distincts :

- **protection du contexte principal** : une exploration de cinquante fichiers coûte quelques centaines de tokens de synthèse au lieu de dizaines de milliers ;
- **indépendance du jugement** : un relecteur qui n'a pas vu la production ne partage pas ses présupposés (voir [chapitre 08](08-workflows-developpement.md)).

Le coût est réel : dans le système de recherche multi-agents d'Anthropic, un agent consomme environ 4 fois plus de tokens qu'une conversation, et un système multi-agents environ 15 fois plus [14]. La synthèse renvoyée est en outre une compression avec perte, ce qui alimente le débat présenté plus bas.

### Le cache de préfixe

Le cache est préfixe et exact : « a change anywhere in the prefix recomputes everything after it » [5]. Claude Code ordonne la requête en couches stables vers volatiles : prompt système et outils, puis contexte de projet (CLAUDE.md, mémoire, règles), puis conversation [5]. Invalident le cache : changement de modèle, changement d'effort sur la plupart des modèles, bascule du mode rapide, ajout ou retrait d'une définition d'outil quand *tool search* est désactivé, compaction, mise à jour de l'outil [5].

La durée de vie dépend du mode de facturation : une heure pour la conversation principale dans le cadre d'un abonnement, cinq minutes avec une clé d'API ou des crédits d'usage ; les subagents ont cinq minutes par défaut ; chaque lecture du cache relance le minuteur [5] **(Daté)**. Modifier CLAUDE.md en cours de session ne casse pas le cache : la modification n'est prise en compte qu'après `/clear`, `/compact` ou un redémarrage [5].

L'équipe de Manus fait du taux de succès du cache « the single most important metric for a production-stage AI agent », avec un rapport entrée/sortie d'environ 100 pour 1 et un écart de prix de 1 à 10 entre tokens en cache et hors cache [11]. Ces chiffres sont auto-déclarés et propres à leur système, mais l'ordre de grandeur explique pourquoi un agent qui garde un préfixe stable coûte nettement moins cher.

## Bonnes pratiques

1. **Une session par unité de travail cohérente.** `/clear` entre deux tâches sans lien ; il ne coûte rien [6]. OpenAI formule la même règle pour Codex : « Keep one chat per coherent unit of work » [18].
2. **Repartir plutôt que corriger indéfiniment.** Après deux corrections infructueuses, `/clear` et un meilleur prompt valent mieux qu'une troisième correction [17] : l'historique d'échecs alimente l'empoisonnement et la distraction [10].
3. **Externaliser l'état de la tâche** dans des fichiers relus à la demande : spec, plan, liste de tâches cochées. Le fichier survit à la compaction et à `/clear`, la conversation non [3]. Manus pousse la logique jusqu'à réécrire régulièrement sa liste de tâches pour garder l'objectif dans la partie récente du contexte [11].
4. **Garder les fichiers d'instructions courts et non déductibles.** Le test proposé par Anthropic : l'agent pourrait-il le trouver en lisant le code, et irait-il vraiment chercher ? Si oui aux deux, la ligne n'a rien à faire dans CLAUDE.md [17]. L'équipe OpenAI qui a construit un produit sans code écrit à la main traite AGENTS.md comme une table des matières d'une centaine de lignes, qui renvoie vers une documentation versionnée [19].
5. **Charger par la structure plutôt que par l'instruction.** Règles par chemin, CLAUDE.md de sous-répertoire et skills placent une consigne au moment où elle sert, au lieu de la payer à chaque requête [4].
6. **Déléguer la lecture volumineuse** (exploration d'une base de code, recherche documentaire, analyse de journaux) à un subagent qui renvoie une synthèse, et exiger dans le prompt de délégation un format de retour court et structuré.
7. **Diriger la compaction** : `/compact focus on <x>` plutôt que la compaction automatique au pire moment, et section « Compact Instructions » pour ce qui doit toujours être conservé [2], [6].
8. **Préserver le cache** : choisir modèle et effort en début de session, éviter de les changer en cours de route, ne pas injecter d'éléments variables (horodatage, identifiant) en tête de contexte [5], [11].
9. **Mesurer** avec `/context` et `/usage` plutôt qu'à l'intuition [4], [6].

## Pièges et anti-patterns

- **Le CLAUDE.md fourre-tout.** Chaque ligne est payée à chaque requête et dilue les autres. Thoughtworks classe l'*agent instruction bloat* dans les pratiques à surveiller (anneau *Caution*) dans le volume 35 de son Radar [20].
- **La consigne critique donnée en conversation.** Elle disparaît à la première compaction [2]. Si elle ne souffre aucune exception, elle relève d'un hook (voir [chapitre 07](07-hooks-et-garde-fous.md)), pas d'un fichier d'instructions.
- **La session marathon.** Plusieurs sujets enchaînés dans une même fenêtre : le contexte ancien évince les fichiers utiles (« Old conversation crowds out the files you need next ») [3].
- **Le subagent qui renvoie tout.** Une délégation sans contrainte de format rapatrie dans le contexte principal le volume qu'elle devait lui épargner.
- **Les serveurs MCP installés « au cas où ».** Même différés, leurs noms et instructions occupent la fenêtre ; sans *tool search*, leurs définitions complètes y sont chargées d'emblée [8]. La multiplication des outils dégrade le choix d'outil [10].
- **Le fichier d'instructions généré puis oublié.** Une étude récente ne trouve aucune amélioration générale du taux de réussite, pour un surcoût d'inférence de plus de 20 % (voir l'état du débat) [15].
- **L'élément volatil en tête de prompt** (date, identifiant de requête) qui invalide le cache à chaque appel [11].

## État du débat

### Partager le contexte ou l'isoler ?

**Contesté.** Cognition soutient qu'il faut partager le contexte complet, traces comprises, entre agents, et que des agents parallèles prennent des décisions implicites incompatibles : « Actions carry implicit decisions, and conflicting decisions carry bad results » [13]. Anthropic rapporte au contraire qu'un système multi-agents dépasse de 90,2 % un agent unique sur son évaluation interne de recherche [14], tout en reconnaissant que les domaines où tous les agents doivent partager le même contexte s'y prêtent mal, et que le code offre moins de tâches réellement parallélisables que la recherche [14].

Les deux positions convergent plus qu'elles ne s'opposent : l'isolation convient aux sous-tâches **en lecture** ou **à périmètre disjoint** (recherche, exploration, relecture), le partage s'impose quand plusieurs agents **écrivent** des parties interdépendantes. Le chiffre de 90,2 % provient d'une évaluation interne non reproduite.

### Les fichiers d'instructions servent-ils ?

**Contesté.** Tous les éditeurs recommandent un fichier d'instructions de dépôt [17], [18]. Une étude de Gloaguen et al. (arXiv, révisée en septembre 2026) conclut que fournir de tels fichiers « does not generally improve task success rates, while increasing inference cost by over 20% on average », que leurs consignes sont bien suivies, mais que les vues d'ensemble du dépôt n'aident pas, que les fichiers soient générés ou écrits par des développeurs [15]. L'étude mesure le taux de réussite sur des tâches de benchmark, pas le respect des conventions d'équipe, qui est souvent la raison d'être de ces fichiers. Lecture prudente : un fichier d'instructions doit contenir des **consignes**, pas une description du dépôt que l'agent peut obtenir seul.

### Les grandes fenêtres rendent-elles la discipline inutile ?

Les modèles récents utilisés par Claude Code disposent par défaut d'une fenêtre d'un million de tokens **(Daté)** [3]. Les résultats de Chroma indiquent que la capacité nominale ne garantit pas l'exploitation uniforme du contenu [9] : une fenêtre plus grande repousse la limite dure, pas la dégradation. Aucune source consultée ne mesure ce compromis sur les fenêtres d'un million de tokens en conditions réelles de développement ; la question reste ouverte.

### Ingénierie du contexte et ingénierie du harnais

Böckeler présente la construction d'un harnais pour agent de code comme « a specific form of context engineering », organisée en guides (qui orientent avant l'action) et capteurs (qui observent après) [16]. Ce cadrage, encore récent, place les fichiers d'instructions parmi les guides et les tests parmi les capteurs ; il est repris au [chapitre 01](01-fondamentaux-boucle-agentique.md) et au [chapitre 09](09-verification-et-evaluation.md).

## Dans ce dépôt

- **Composants** : le workflow de l'[ADR-001](../docs/decisions/ADR-001-workflow-developpement.md) fait de la spec et du plan une mémoire externe ; [CLAUDE.md](../CLAUDE.md) se limite à importer [AGENTS.md](../AGENTS.md) et à six lignes propres à l'outil ; le subagent `chercheur` du plugin [`workflow`](../plugins/workflow/) applique l'isolation (à venir).
- **Labs** : à venir.

## Sources

Consultées le 2026-11-26 ou le 2026-11-27.

1. **[O]** Anthropic (Rajasekaran et al.), *Effective context engineering for AI agents*, 29/09/2025. <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
2. **[O]** Anthropic, *How Claude Code works*. <https://code.claude.com/docs/en/how-claude-code-works>
3. **[O]** Anthropic, *Context window*. <https://code.claude.com/docs/en/context-window>
4. **[O]** Anthropic, *Memory*. <https://code.claude.com/docs/en/memory>
5. **[O]** Anthropic, *Prompt caching*. <https://code.claude.com/docs/en/prompt-caching>
6. **[O]** Anthropic, *Manage costs effectively*. <https://code.claude.com/docs/en/costs>
7. **[O]** Anthropic, *Subagents*. <https://code.claude.com/docs/en/sub-agents>
8. **[O]** Anthropic, *MCP*. <https://code.claude.com/docs/en/mcp>
9. **[P]** Hong, Troynikov, Huber (Chroma), *Context Rot: How Increasing Input Tokens Impacts LLM Performance*, 14/07/2025. <https://www.trychroma.com/research/context-rot>
10. **[P]** Breunig, *How Long Contexts Fail*, 22/06/2025. <https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html>
11. **[P]** Ji (Manus), *Context Engineering for AI Agents: Lessons from Building Manus*, 18/07/2025. Chiffres auto-déclarés. <https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus>
12. **[P]** Martin, *Context Engineering for Agents*, 23/06/2025. <https://rlancemartin.github.io/2025/06/23/context_engineering/>
13. **[P]** Yan (Cognition), *Don't Build Multi-Agents*, 12/06/2025. <https://cognition.com/blog/dont-build-multi-agents>
14. **[O]** Anthropic (Hadfield et al.), *How we built our multi-agent research system*, 13/06/2025. Évaluations internes. <https://www.anthropic.com/engineering/multi-agent-research-system>
15. **[P]** Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv 2602.11988, v3 du 29/09/2026 (résumé lu, corps non lu). <https://arxiv.org/abs/2602.11988>
16. **[P]** Böckeler, *Harness engineering for coding agent users*, 02/04/2026. <https://www.martinfowler.com/articles/harness-engineering.html>
17. **[O]** Anthropic, *Best practices for Claude Code*. <https://code.claude.com/docs/en/best-practices>
18. **[O]** OpenAI, *Codex — Best practices*. <https://learn.chatgpt.com/guides/best-practices.md>
19. **[O]** Lopopolo (OpenAI), *Harness engineering: leveraging Codex in an agent-first world*, 11/02/2026. <https://openai.com/index/harness-engineering/>
20. **[P]** Thoughtworks, *Technology Radar*, vol. 35, novembre 2026 (anneaux relevés, fiches détaillées non lues). <https://www.thoughtworks.com/radar>
21. **[O]** Anthropic, *Hooks reference*. <https://code.claude.com/docs/en/hooks>
