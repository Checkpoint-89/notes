# Le sport comme laboratoire pour la prédiction tactique sur le champ de bataille

## L'idée

Pré-entraîner un Transformer sur des séquences d'événements de matchs de football (massives, complètes, publiques), puis transférer vers la **prédiction de la prochaine action dans un engagement tactique** (classifié, rare, bruité). Le sport sert de proxy accessible pour un problème structurellement similaire mais dont les données sont inaccessibles.

## Pourquoi la prédiction tactique (pas l'insurrection)

Le transfert sport → conflit de type insurrection (ACLED, War Diary) est fragile : les échelles de temps (jours/mois), le nombre d'acteurs inconnus, et le caractère ouvert du système cassent l'analogie. En revanche, la **prédiction tactique au niveau de l'engagement** partage la structure du sport :

| Dimension | Football | Engagement tactique |
|---|---|---|
| Espace | Terrain borné 105×68 m | Zone d'opération bornée (secteur assigné) |
| Temps | ~90 min, résolution à la seconde | Engagement en minutes/heures, résolution capteur |
| Agents | 2×11 identifiés, rôles différenciés | Unités identifiées (Blue Force Tracking), formations |
| Séquences | Possession → pression → tir → corner | Contact → suppression → débordement → assaut |
| Dynamique | Action → réaction immédiate de l'adversaire | Feu → riposte, manœuvre → contre-manœuvre |
| Système | Fermé (règles, terrain, durée) | Quasi-fermé (ROE, secteur, mission bornée) |
| Données | Event logs StatsBomb/Opta, publics | C4ISR / drones / capteurs — format similaire, classifié |

C'est ce dernier point qui justifie le détour par le sport : les données d'engagement tactique réel sont **classifiées et inaccessibles** pour une thèse universitaire. Le sport est la seule source de séquences adversariales denses qu'on puisse utiliser en clair et publier dessus.

## Le précédent : transferts cross-domaine sur séquences d'événements

Le **processus de Hawkes** n'est pas le modèle qu'on utiliserait, mais il fournit la **preuve historique** que la structure du problème (séquences spatio-temporelles en cascade) se transfère entre domaines :

| Transfert | Papier | Citations | Statut |
|---|---|---|---|
| Sismologie → Crime | Mohler et al. 2011, JASA | 1 240 | Validé opérationnellement (*predictive policing*) |
| Sismologie → Conflit armé | Zammit-Mangion et al. 2012, PNAS | 189 | Appliqué au War Diary afghan |
| Cross-domain Hawkes | Li 2021, NTU Thesis | — | Mécanisme de transfert prouvé techniquement |

Le point clé : c'est la **structure du problème** qui permet le transfert, pas le modèle spécifique.

## Ce qui existe

1. **En sport** : des Transformers axiaux sur processus ponctuels marqués (Yeung 2025) modélisent les séquences d'événements de match — c'est l'état de l'art. Plus anciennement : Hawkes classiques (Narayanan 2023).

2. **En défense — prédiction d'engagement** : pas de Transformer publié sur des séquences d'événements tactiques réels (données classifiées). Les travaux existants sur le conflit (Zammit-Mangion 2012, Chukwuemeka 2026) opèrent à l'échelle de l'insurrection, pas de l'engagement.

3. **Simulateurs militaires** : JCATS, VBS, OneSAF génèrent des logs d'événements au même format que les event logs sportifs. C'est un pont intermédiaire naturel entre le sport et le terrain réel.

## Le pipeline : sport → simulateur → terrain

```
Données sport (publiques, massives)
    │ pré-entraînement Transformer
    ▼
Données simulateur militaire (accessibles via industriel)
    │ fine-tuning
    ▼
Données terrain réel (classifiées, accès restreint)
    │ fine-tuning final
    ▼
Modèle de prédiction tactique déployé
```

Ce pipeline en 3 étapes résout le problème d'accès aux données :
- **Étape 1** (thèse, publiable) : pré-entraînement sur sport, architecture et méthode validées.
- **Étape 2** (collaboration industriel) : fine-tuning sur logs de simulateur — données non classifiées mais réalistes.
- **Étape 3** (post-thèse, industriel) : fine-tuning sur données terrain classifiées.

## Ce qu'on construit d'abord dans le sport

| Composante | Ce qu'on apprend | Analogue tactique |
|---|---|---|
| **Dépendances séquentielles** | Comment un événement influence la probabilité et la nature des suivants | Contact → quelle suite probable ? |
| **Structure des marques** | Types d'événements et leurs dépendances conditionnelles | Types d'actions (feu direct, mouvement, appui, observation) |
| **Dynamique spatiale** | Comment les séquences se propagent dans l'espace borné | Progression dans le secteur d'opération |
| **Interaction adversariale** | Action d'un camp → réaction de l'autre | Manœuvre → contre-manœuvre |
| **Architecture Transformer** | Attention axiale (temps × espace × type) | Même architecture, mêmes mécanismes |

## Ce qui est transférable

### Directement

- **L'architecture** : un Transformer sur séquences d'événements spatio-temporels marqués a la même structure d'entrée/sortie. Les poids sport initialisent le modèle tactique.
- **Les représentations apprises** : embeddings de types d'événements, encodages positionnels temporels et spatiaux, mécanismes d'attention — capturent des patterns séquentiels génériques (cascades, inhibitions, clustering) qui existent des deux côtés.
- **Le clustering spatio-temporel** : les événements s'agrègent dans l'espace et le temps (séquences offensives ↔ séquences d'engagement). Invariant structurel.
- **Les techniques d'évaluation** : métriques de calibration, quantification d'incertitude.

### À adapter

| Aspect | Sport | Engagement tactique | Adaptation |
|---|---|---|---|
| Échelle spatiale | 105×68 m | Secteur ~1-10 km² | Rescaling des encodages positionnels |
| Vocabulaire des marques | {passe, tir, faute, but…} | {feu direct, mouvement, appui, brèche…} | Remapping des embeddings de type |
| Complétude | Quasi-totale | Partielle (fog of war, capteurs limités) | Protocole de dégradation (voir ci-dessous) |
| Nombre d'agents | 2 × 11 identifiés | Sections/groupes, effectifs variables | Tokenisation flexible des unités |
| Troisième dimension | Plat | Terrain 3D, dénivelé, couverture | Ajouter un encodage d'élévation/couverture |

### Non transférable

- Les **paramètres numériques** appris (taux de fond, amplitudes) — spécifiques au domaine.
- Les **features contextuelles** sport (score, minutes de jeu, cartons).

## Stratégie de dégradation progressive

On ne saute pas du sport propre au terrain réel. On **dégrade les données sport** par paliers pour simuler les conditions du champ de bataille :

| Palier | Dégradation | Ce qu'on simule | Métrique |
|---|---|---|---|
| **0** | Baseline sport complète | — | Performance de référence |
| **1** | Supprimer X% des événements | Fog of war, capteurs hors couverture | Robustesse à la censure |
| **2** | Bruit gaussien sur coordonnées | Géolocalisation imprécise (GPS dégradé, SIGINT) | Robustesse spatiale |
| **3** | X% des types → "inconnu" | Identification incertaine de l'action adverse | Robustesse aux marques manquantes |
| **4** | Masquer un camp sauf contacts | N'observer l'adversaire que lors des contacts directs | Prédiction avec information partielle sur OPFOR |
| **5** | Réduire à N séquences | Peu de données de fine-tuning disponibles | Seuil minimal de données |
| **6** | Combiné aux niveaux réalistes | Conditions terrain réelles | Performance résiduelle |

Le palier **4** est spécifique au tactique : en sport on observe les deux équipes en permanence, au combat on ne voit l'ennemi que par intermittence. C'est le test critique.

### Ce que ça apporte

- **Courbes de robustesse** quantifiées pour chaque type de dégradation.
- **Seuil de viabilité** : conditions minimales pour que le transfert ait un sens.
- **Validation empirique** : si le modèle sport dégradé bat un modèle entraîné from scratch sur données dégradées seules, le pré-entraînement est validé.
- **Contribution méthodologique publiable** indépendamment du transfert effectif.

## Choix du modèle : pourquoi un Transformer

| Critère | Hawkes classique | Transformer axial |
|---|---|---|
| Expressivité | Noyau paramétrique figé | Attention libre, pas de forme fonctionnelle imposée |
| Passage à l'échelle | Petites séquences | Conçu pour longues séquences |
| Transfer learning | Difficile (paramètres rigides) | Naturel (pré-entraînement + fine-tuning) |
| État de l'art sport | Narayanan 2023 | Yeung 2025 |
| Gestion du spatial | Noyau spatial séparé | Attention axiale (temps × espace) |
| Observabilité partielle | Pas prévu | Masking natif (comme BERT) |

Le Hawkes reste utile comme **baseline** interprétable et pour l'analyse structurelle (décomposition endogène/exogène).

## Pourquoi c'est crédible

- La **tâche** est structurellement la même : prédire le prochain événement (quand, où, quoi) dans une séquence spatio-temporelle adversariale en espace borné.
- Le transfert cross-domaine a **déjà été prouvé** sur des séquences d'événements (sismologie → crime, 1 240 citations), même avec des modèles moins expressifs.
- Le sport fournit ce que le domaine tactique n'a pas en clair : des **millions de séquences complètes** avec ground truth, dans un contexte adversarial avec deux agents stratégiques.
- Le paradigme **pré-entraînement + fine-tuning** est dominant en deep learning — l'appliquer à des séquences d'événements spatio-temporels est une extension naturelle.
- Le pipeline **sport → simulateur → terrain** débloque le problème d'accès aux données en fractionnant en étapes de classification croissante.

## Pourquoi un industriel de défense financerait

- **Livrable court terme** (thèse) : architecture Transformer validée sur données publiques + protocole de dégradation = publiable, reproductible, non classifié.
- **Livrable moyen terme** (avec industriel) : fine-tuning sur logs de simulateur (JCATS/VBS) — données accessibles, résultats démontrant le gain du pré-entraînement sport.
- **Livrable long terme** : modèle déployable sur données terrain réelles pour aide à la décision tactique.
- **Risque faible** : même si le transfert sport → tactique ne marche pas, l'architecture et le protocole de dégradation sont des contributions réutilisables.

## En une phrase

Pré-entraîner un Transformer sur des séquences d'événements sportifs pour prédire la prochaine action dans un engagement tactique — parce que la structure du problème est la même, mais les données sont en clair.

## Références

- Mohler, G.O. et al. (2011). *Self-exciting point process modeling of crime.* JASA. [1 240 cit.]
- Zammit-Mangion, A. et al. (2012). *Point process modelling of the Afghan War Diary.* PNAS. [189 cit.]
- Lewis, E. & Mohler, G. (2012). *Self-exciting point process models of civilian deaths in Iraq.* Security Journal. [182 cit.]
- Reinhart, A. (2018). *A Review of Self-Exciting Spatio-Temporal Point Processes and Their Applications.* Statistical Science. [327 cit.]
- Li, T. (2021). *Advanced Hawkes processes for practical event sequence analysis: models and accelerations.* NTU Thesis.
- Narayanan, S. & Kosmidis, I. (2023). *Flexible marked spatio-temporal point processes with applications to event sequences from association football.* JRSS-C, 72(5). [13 cit.]
- Yeung, C. et al. (2025). *Transformer-based neural marked spatio temporal point process model for analyzing football match events.* Applied Intelligence. [14 cit.]
- Chukwuemeka, C. et al. (2026). *Multivariate Spatio-Temporal Neural Hawkes Processes.* arXiv:2602.23629.
