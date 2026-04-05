# Système de Pronostic Live — Note de synthèse

## 1. Le problème

Prédire en temps réel la probabilité de chaque type d'évènement (200 types) dans les prochaines minutes d'un match sportif, avec intervalle de confiance. Contraintes :

| Contrainte | Valeur | Ce que ça implique |
|---|---|---|
| Matchs simultanés | 1 000 | Le système doit traiter 1 000 contextes en parallèle |
| Débit d'évènements | 10 000 evt/s en pic | L'ingestion ne doit perdre aucun évènement |
| Latence bout-en-bout | < 500 ms | De la réception d'un évènement à la mise à jour des probabilités |
| Données d'entraînement | 100K+ matchs | Suffisant pour un modèle profond |
| MySQL existant | Ne pas toucher | Toute nouvelle brique se greffe en lecture seule, sans migration ni modification du schéma |

---

## 2. Architecture technique

```
  MySQL (existant, inchangé)
    │                          ╭─────────────────────────────────╮
    │                          │ Phase 2 (options futures) :     │
    │                          │  · TimescaleDB (séries temp.)   │
    │                          │  · MongoDB (schémas hétérogènes)│
    │                          ╰──────────────┬──────────────────╯
    │                                         │
  Feature Store (lecture seule) ◄─────────────╯
  ├─ Offline : MySQL → Parquet (entraînement)
  └─ Online  : MySQL → Redis (inférence, polling 1-2s → Kafka)
        │
  Transformer Dual-Stream (PyTorch / ONNX Runtime)
        │
  API FastAPI → Consommateurs
```

MySQL n'est pas remplacé. On ajoute une couche intermédiaire en lecture seule. Impact sur l'existant : zéro.

### Pourquoi chaque brique ?

**Feature Store** — Le modèle ne consomme pas directement les données brutes de MySQL. Il a besoin de variables calculées : "nombre de corners dans les 10 dernières minutes", "cote glissante sur 5 min", "temps depuis le dernier but". Le Feature Store est la couche qui calcule et sert ces variables. Ce n'est pas une base de données : il **s'appuie sur deux supports de stockage** selon le contexte :
- **Offline → Parquet** (fichiers optimisés pour la lecture massive — 10-50× plus rapide que SQL pour lire des millions de lignes d'un coup) : utilisé pour l'entraînement du modèle.
- **Online → Redis** (base en mémoire, réponse en < 5 ms) : utilisé pour l'inférence live, où MySQL (20-50 ms/requête) est trop lent pour tenir la contrainte de 500 ms bout-en-bout.

Le Feature Store est aussi critique pour les features pré-match (statistiques de forme, historique par joueur, paramètres Dixon-Coles) — le facteur n°1 de performance du modèle, comme détaillé en section 4. Tout passe par un calcul unique matérialisé dans le Feature Store, identique entre entraînement et production.

→ *Contrainte adressée* : **cohérence entraînement/production**. C'est un risque classique en machine learning : sans Feature Store, deux équipes (ou deux chemins de code) calculent les mêmes variables avec des hypothèses légèrement différentes (arrondis, gestion des valeurs manquantes…). Le modèle reçoit en production des nombres différents de ceux sur lesquels il a été entraîné — ses prédictions se dégradent silencieusement. Le Feature Store impose un calcul unique réutilisé dans les deux contextes.
→ *Contrainte adressée* : **ne pas toucher MySQL**. Le Feature Store lit MySQL en lecture seule et matérialise les résultats dans Parquet/Redis. Aucune écriture, aucune migration.

**Kafka** *(phase 2)* — File d'attente de messages distribuée. Le principe : quand les évènements arrivent plus vite que le modèle ne peut les traiter, Kafka les met en tampon et les restitue dans l'ordre. C'est le même rôle qu'une file d'attente devant un guichet — personne n'est perdu, tout le monde est servi.
→ *Contrainte adressée* : **10 000 evt/s en pic**.

**ONNX Runtime + quantification INT8** — Le modèle est entraîné avec PyTorch (souple, lent). Pour la production, on le convertit dans un format optimisé (ONNX) et on réduit la précision des calculs de 32 bits à 8 bits (quantification INT8). Résultat : ~3× plus rapide, avec une perte de qualité négligeable.
→ *Contrainte adressée* : **latence < 500 ms sous charge** (1 000 matchs simultanés).

**FastAPI** — Framework Python pour exposer les prédictions aux consommateurs via une API web (documentation automatique, hautes performances).
→ *Contrainte adressée* : servir les résultats du modèle aux applications en aval.

### Évolution du stockage

**Phase 1 — MySQL + JSON.** MySQL (existant) stocke tout. Le problème : les 200 types d'évènements ont des attributs différents (un corner a une zone et un pied, un but a un buteur et un xG, un changement a un joueur entrant et sortant). Plutôt que de créer 200 tables ou d'ajouter des colonnes à chaque nouveau type, on utilise une colonne JSON flexible — chaque ligne a les mêmes colonnes fixes, mais le détail spécifique au type est dans le JSON :

```sql
-- Table events (schéma simplifié)
CREATE TABLE events (
  id          BIGINT PRIMARY KEY,
  match_id    INT,
  event_type  VARCHAR(50),   -- 'corner', 'substitution', 'goal', …
  timestamp   DATETIME(3),
  data        JSON           -- ← contenu variable selon event_type
);

-- Un corner :
-- data = {"zone": "gauche", "pied": "droit", "joueur_id": 1042}

-- Un changement de joueur :
-- data = {"joueur_sortant": 1042, "joueur_entrant": 987, "raison": "tactique"}

-- Un but :
-- data = {"buteur_id": 1042, "passeur_id": 987, "zone_tir": "surface", "xG": 0.34}
```

Avantage : aucune migration de schéma quand un nouveau type apparaît — on insère simplement un JSON avec la nouvelle structure. Suffisant pour ~100M lignes.

**Phase 2 — TimescaleDB.** Une **base orientée séries temporelles** (extension PostgreSQL) : elle partitionne automatiquement les données par intervalle de temps. Les écritures à 10 000 evt/s restent rapides (elles ne touchent que la partition active), et la purge des vieux matchs est instantanée (`DROP CHUNK` plutôt que `DELETE` + fragmentation).
→ *Contrainte adressée* : **10 000 evt/s en écriture + requêtes sur fenêtres temporelles**. MySQL tient en phase 1, mais à l'échelle multi-sport le volume d'écriture et les requêtes glissantes deviennent un goulot.

**Si les 200 types hétérogènes deviennent un frein** → migration vers **MongoDB**, une base **NoSQL document** : chaque enregistrement est un document JSON autonome, sans schéma global. Ajouter un nouveau type ou un nouvel attribut ne nécessite aucune migration — on insère simplement un document avec la nouvelle structure.
→ *Contrainte adressée* : **hétérogénéité des schémas** (200 types × attributs différents).

### Monitoring

**Prometheus** collecte les métriques (latence, Brier score, débit) ; **Grafana** les affiche en dashboards temps réel avec alertes. Combinés, ils détectent automatiquement les dégradations de performance ou de qualité.

---

## 3. Deux problèmes en un

*Ce qui suit s'appuie sur une revue succincte de cinq papiers (2 architectures Transformer appliquées au sport, 1 processus ponctuel spatio-temporel, 1 processus de Hawkes par attention, 1 baseline statistique classique). Ce n'est pas un survey exhaustif — c'est suffisant pour illustrer les complexités du problème, pas pour exclure d'autres approches.*

Ce projet résout simultanément **deux problèmes distincts** que la littérature académique traite séparément — voire ignore pour le second.

### Problème 1 — Un match est une séquence

Un match de football peut être vu exactement comme une phrase en traitement du langage naturel (NLP) : une séquence de tokens ordonnés dans le temps. Un corner, un tir cadré, un but — ce sont les "mots" du match. Prédire le prochain évènement revient à prédire le prochain mot d'une phrase.

Cette analogie est le point de départ de toute la littérature récente (Horton & Lucey 2025, Simpson et al. 2022, Yeung et al. 2023). Le mécanisme d'**attention** du Transformer — qui apprend quels éléments passés sont pertinents pour la prédiction suivante — s'applique naturellement : un corner à la 65e minute est pertinent pour prédire un but à la 66e, mais pas un carton jaune de la 12e.

**Mais un match n'est pas une phrase.** La différence fondamentale tient au temps. En NLP, les mots sont sur une grille régulière : position 1, 2, 3. Les évènements sportifs arrivent à des instants quelconques — un corner à t=12.3 min, le suivant à t=34.7 min. Utiliser l'encodage positionnel standard du NLP (qui numérote les positions) revient à traiter ces deux évènements comme consécutifs sans tenir compte du délai entre eux.

L'impact est massif. Zuo et al. (2020) comparent trois configurations :

| Configuration | Log-vraisemblance |
|---|---|
| Attention seule, sans encodage | -5.29 |
| Attention + encodage positionnel NLP (entiers) | -5.25 |
| Attention + encodage temporel continu | **-2.03** |

L'encodage NLP standard n'apporte presque rien sur des évènements asynchrones. L'**encodage temporel continu** — qui encode directement le timestamp réel `t` en vecteur via des fonctions trigonométriques à différentes fréquences — transforme le modèle. C'est l'adaptation NLP → sport la plus impactante, bien plus que le choix d'architecture.

### Problème 2 — Deux natures de signaux

Voici ce que la littérature ne fait pas : **aucun papier n'utilise les cotes des bookmakers comme signal d'entrée du modèle**. Les cotes n'apparaissent que comme benchmark externe — on compare les prédictions aux cotes après coup. Pourtant, les cotes live sont le signal le plus informatif disponible : elles agrègent l'opinion de milliers de parieurs informés et se mettent à jour quasi-instantanément. Une cote qui chute avant même qu'un but soit officiellement enregistré encode de l'information sur la pression du jeu que les données d'évènements bruts ne capturent pas seules.

Le problème, c'est qu'intégrer les cotes crée une **hétérogénéité fondamentale** dans les entrées du modèle :

| | Évènements ponctuels | Signaux continus |
|---|---|---|
| **Exemples** | Corner, but, carton, tir | Cotes, possession, score |
| **Fréquence** | Rare, irrégulière | Régulière (~1×/min) |
| **Nature** | Discrète, sémantique riche | Continue, lisse |
| **Encodage naturel** | Token avec attributs | Vecteur numérique |

Les papiers n'ont pas ce problème : ils travaillent uniquement sur des évènements ponctuels homogènes (passes, tirs, fautes). Un seul encodeur suffit. Horton & Lucey (2025) utilisent un *axial transformer* — une variante qui gère deux dimensions (temps × joueurs) dans une seule grille — parce que toutes leurs entrées sont du même type.

Dès qu'on ajoute les cotes — un signal continu, asynchrone, de sémantique radicalement différente — la question de comment les intégrer se repose. L'axial transformer ne répond pas à cette question. Il la contourne en ne posant pas le problème.

### Une réponse possible: dual-stream

L'architecture **dual-stream** répond aux deux problèmes simultanément. Elle sépare les deux natures de signaux dès l'encodage, avec un encodeur spécialisé pour chaque modalité, puis les fusionne :

| Stream | Contenu | Encodeur | Pourquoi ce choix |
|---|---|---|---|
| **1 — Évènements** | type + timestamp exact + attributs (les 200 types sont regroupés en ~10 familles qui partagent la même structure d'embedding) | Transformer causal | L'attention capture les chaînes causales (corner → tir → but) sans les coder manuellement |
| **2 — Signaux continus** | cotes, possession, score | GRU léger | Signal régulier et lisse — pas besoin de la puissance (ni du coût) du Transformer |

Les deux streams sont fusionnés par **cross-attention** : mécanisme qui permet à chaque stream de "consulter" l'autre. Concrètement, une cote qui chute informe le stream événements qu'un but est probable, et un carton rouge informe le stream continu que les cotes vont bouger.

C'est un pattern classique en deep learning multimodal (vision + texte, audio + texte) : séparer les encodeurs par modalité puis fusionner tard donne systématiquement de meilleurs résultats que l'encodage conjoint précoce.

**Alternative valide.** Inspirée de Horton & Lucey : projeter toutes les modalités vers un espace de dimension commune via une couche linéaire par modalité, puis les concaténer dans une seule grille Transformer. La cross-attention entre modalités est alors gérée implicitement par le mécanisme d'attention standard. C'est plus simple à implémenter, mais perd la spécialisation de l'encodeur par modalité. La littérature ne tranche pas entre les deux approches quand une des modalités est un signal continu à haute fréquence — la comparaison empirique n'existe pas.

---

## 4. Le modèle de prédiction - Insights issus de la litérature

### Ce que la littérature nous apprend

Quatre résultats empiriques guident les décisions d'architecture.

**1. Les features pré-match dominent l'architecture.** Le résultat le plus contre-intuitif de Horton & Lucey (2025) : retirer les features de contexte pré-match (statistiques récentes des joueurs, forme, contexte de la compétition) dégrade les performances *plus* que retirer les interactions entre joueurs (+23% d'erreur vs +10%). Un modèle qui ignore qu'un joueur est en forme repart de zéro à chaque match. Implication directe : investir sur la qualité des features pré-match avant d'optimiser l'architecture.

Trois façons d'encoder cette connaissance pré-match :

- **Features artisanales** — on calcule explicitement des statistiques : paramètres Dixon-Coles α/β, rating Elo, forme récente, buts marqués/encaissés sur N matchs. C'est ce que Horton & Lucey utilisent et ce qui domine dans leur ablation. Avantage : interprétable, fonctionne immédiatement, compatible avec le Feature Store.
- **Embeddings d'entité appris** — on associe un vecteur entraînable à chaque entité (équipe, ligue, joueur). Le modèle remplit ce vecteur seul pendant l'entraînement. Limitations : nécessite beaucoup de données par entité, un promu ou un joueur transféré aura un embedding vide/aléatoire, et on ne sait pas ce que le modèle a encodé.
- **Les deux combinés** — features artisanales + embeddings concaténés. Plus expressif, mais plus complexe à déboguer.

En phase 1, les features artisanales sont le choix par défaut — c'est ce qui a le plus d'impact prouvé. Les embeddings d'entité sont une option d'enrichissement ultérieur, pas un prérequis.

**2. L'encodage temporel continu est l'adaptation la plus impactante.** Comme détaillé en section 3 (Zuo et al. 2020). Le stream événements encode directement le timestamp réel `t` — pas la position dans la séquence.

**3. L'ordre des sorties multiples n'est pas neutre.** Quand on prédit simultanément *quand*, *où* et *quel type* d'évènement, les conditionner les uns aux autres dans l'ordre `temps → zone → action` donne systématiquement les meilleurs résultats (Yeung et al. 2023, écart de 0.11 sur la loss totale). La raison est une causalité naturelle : le timing contraint la zone possible (on ne shoote pas depuis son propre camp à la 89e minute), la zone contraint l'action probable (un centre depuis l'intérieur de la surface est improbable). Les têtes de sortie du modèle respectent cet ordre.

**4. Le Transformer ne domine pas toujours.** Sur un dataset modeste (138 matchs), le LSTM bat le Transformer (loss 0.332 vs 0.379 — Simpson et al. 2022). Avec peu de données, le Transformer sur-apprend. Sur 62 610 matchs (Horton & Lucey), il reprend l'avantage. Si le dataset de phase 1 est limité, tester LSTM d'abord est prudent.

### Sortie et calibration

**Ce que le modèle produit.** Pour chaque type d'évènement (corner, but, carton…), le modèle estime la probabilité que cet évènement survienne dans les Δ prochaines minutes. Concrètement, à chaque mise à jour, il renvoie un tableau de ~200 probabilités — une par type — accompagnées chacune d'un **intervalle de confiance à 90 %** (exemple : "probabilité d'un corner dans les 2 min : 18 %, intervalle [12 %, 25 %]").

**Deux problèmes de calibration distincts.**

1. **Calibration des probabilités.** Le modèle annonce "30 % de chance d'un but" — mais en pratique, ça n'arrive que 15 % du temps. Les probabilités brutes d'un réseau de neurones sont systématiquement mal calibrées (surconfiantes en général). En contexte de paris, une mauvaise calibration a un coût financier direct : on mise sur des évènements qu'on surestime. La méthode standard pour corriger ça est le *temperature scaling* (Guo et al. 2017) — un unique paramètre appris sur un jeu de validation qui rescale les logits du modèle. Simple, peu coûteux, largement adopté en production.

2. **Intervalles de confiance.** Le modèle dit 18 % — mais quelle est l'incertitude autour de ce chiffre ? Aucun des papiers de la littérature ne produit d'intervalles de confiance garantis. Pour un consommateur des prédictions (trader, algorithme de mise), la probabilité seule ne suffit pas : il faut savoir si le modèle est "sûr de ses 18 %" ou si c'est "quelque part entre 8 % et 30 %". C'est un problème distinct de la calibration : un modèle peut être bien calibré en moyenne mais très incertain sur un match atypique. La méthode standard ici est la *prédiction conformale* (Vovk et al. 2005) — elle construit des intervalles à couverture garantie (ex : 90 %) sans hypothèse sur la distribution, en mesurant les erreurs réelles du modèle sur un jeu de calibration.

Les deux sont nécessaires et complémentaires. La calibration corrige le biais systématique des probabilités ; les intervalles quantifient l'incertitude résiduelle match par match. En contexte de paris, les deux ont un impact financier direct.

### Baselines obligatoires — le seuil de déploiement

Le modèle de **Dixon & Coles (1997)** modélise les buts de chaque équipe comme deux lois de Poisson indépendantes — le choix naturel pour modéliser des évènements rares dans un intervalle fixe. Les paramètres sont la force d'attaque (α) et la faiblesse défensive (β) de chaque équipe, plus un avantage à domicile (γ).

Ce modèle a **deux rôles** dans le projet :

1. **Prior pré-match.** Les paramètres α et β estimés sur les matchs passés sont les meilleures features de force d'équipe sans deep learning. Ils initialisent le stream continu à t=0, avant que les évènements intra-match commencent à mettre à jour les prédictions.

2. **Seuil de déploiement.** Les cotes bookmakers sont largement dérivées de variantes de Dixon-Coles. Un Transformer qui ne bat pas Dixon-Coles sur le **Brier score** (mesure de calibration : écart entre prédit et réalisé, plus bas = mieux) ne produit rien que les bookmakers ne sachent déjà — il n'a aucune valeur ajoutée.

Baselines testées : régression logistique, Poisson bivariée (Dixon & Coles), Poisson non-homogène. Le Transformer n'est déployé que s'il bat ces méthodes simples — pour justifier sa complexité et son coût d'exploitation.

---

## 5. Points critiques

| Risque | Explication | Mitigation |
|---|---|---|
| **Latence GPU sous charge** | 1 000 matchs sollicitent le GPU en parallèle → risque de file d'attente | ONNX Runtime + INT8 dès phase 1. Budget interne ×3 vs nominal. |
| **Non-stationnarité** | Transferts, coachs, règles (VAR) changent — un modèle de 2022 est obsolète en 2025 | Ré-entraînement hebdomadaire, warm-start des embeddings, pondération temporelle $w = e^{-\alpha \cdot \text{âge}}$ (les vieux matchs comptent moins). Dixon & Coles (1997) calibrent ξ = 0.0065 par demi-semaine — un point de départ empirique pour la décroissance. |
| **Data leakage** | Si des matchs de 2024 se retrouvent dans le jeu d'entraînement et de test, les scores sont artificiellement gonflés | Split temporel strict : train saisons N-3→N-1, val 1ère moitié N, test 2nde moitié. |
| **Fraîcheur des données live** | Un polling trop lent = le modèle prédit sur un état périmé | Polling MySQL toutes les 1-2 s. Kafka en phase 2. |
| **Dérive silencieuse** | La qualité des prédictions se dégrade sans qu'on le remarque | **Brier score** sur buffer glissant 7 jours. Alerte si > 10 %. |
| **Attention non-décroissante** | Le mécanisme d'attention distribue les poids uniformément sur l'historique (Yeung et al. 2023) — il ne privilégie pas structurellement le passé récent | Pondération temporelle explicite sur les features de forme + fenêtre de contexte limitée (~40 évènements, au-delà le modèle capte le "style" général plutôt que la dynamique en cours — Simpson et al. 2022). |
| **Taille du dataset** | Avec peu de matchs, le Transformer sur-apprend (Simpson et al. 2022 : LSTM bat le Transformer sur 138 matchs) | Tester LSTM en phase 1 si < quelques milliers de matchs. Le Transformer reprend l'avantage au-delà (~60K matchs). |

---

## 6. Stack & roadmap

| Composant | Phase 1 | Phase 2 |
|---|---|---|
| **Objectif** | Battre Dixon-Coles et les cotes (1 sport) | 1 000 matchs live, multi-sport |
| **Modèle** | Transformer dual-stream + ONNX/INT8 | + tête intensité + embeddings enrichis |
| **Ingestion** | Polling MySQL 1-2 s | Kafka (absorbe les pics) |
| **Stockage** | MySQL + JSON + Redis | TimescaleDB + Redis + Parquet/S3 |
| **Infra** | 1-2 GPU, 1 serveur | Kubernetes, multi-GPU, autoscaling |
| **Monitoring** | Prometheus + Grafana | Idem |

---

## 7. Références

- **NMSTPP** (Yeung et al. 2023) — Transformer + processus ponctuel marqué spatio-temporel. Ordre de prédiction `temps → zone → action`. Attention uniformément distribuée sur l'historique.
- **Seq2Event** (Simpson et al. 2022) — next-event prediction. LSTM > Transformer sur petits datasets. Fenêtre de contexte optimale ~40 évènements.
- **Axial Transformer** (Horton & Lucey 2025) — double axe temps × joueur, 75K prédictions/match. Features pré-match > architecture. Latence sub-seconde sur CPU.
- **Transformer Hawkes Process** (Zuo et al. 2020) — self-attention pour l'excitation mutuelle. Démonstration de l'encodage temporel continu.
- **Dixon & Coles** (1997) — baseline Poisson bivariée. Prior pré-match (α, β) et seuil de déploiement.
