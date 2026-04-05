## Revue de littérature — Prédiction d'événements intra-match par apprentissage profond

---

### Introduction — Les insights en un coup d'œil

Six papiers couvrent le sujet, de la baseline statistique classique aux architectures Transformer industrielles. En voici les conclusions les plus importantes avant d'entrer dans le détail.

**Sur l'architecture.** Un match de football peut être traité comme un problème de séquence — exactement comme une phrase en traitement du langage naturel (NLP). Le Transformer fonctionne, mais une variante appelée *axial transformer* est mieux adaptée car elle gère naturellement deux dimensions simultanées : le temps et les joueurs. Elle atteint une latence sub-seconde sur CPU standard en production.

**Sur les features.** Ce que le modèle sait *avant* le match (le niveau des équipes, les statistiques récentes des joueurs) est plus important que la sophistication de l'architecture. Un bon jeu de features pré-match bat une architecture sophistiquée avec de mauvaises features.

**Sur le temps.** En NLP, les mots sont sur une grille régulière (position 1, 2, 3...). Les événements sportifs arrivent à des instants quelconques. Adapter l'encodage positionnel au temps continu est la modification la plus impactante qu'on puisse faire — bien plus que changer d'architecture.

**Sur les baselines.** Le modèle statistique Dixon-Coles de 1997, basé sur la loi de Poisson, reste la référence incontournable. Tout modèle deep learning qui ne le bat pas ne mérite pas d'être déployé.

**Sur ce qui manque dans la littérature.** Aucun papier n'utilise les cotes des bookmakers comme signal d'entrée du modèle, ni ne produit d'intervalles de confiance garantis. Ce sont deux différenciateurs directs pour un usage en paris sportifs.

---

### L'architecture : traiter un match comme une séquence de tokens

La contribution architecturale la plus importante vient de **Horton & Lucey (2025)**. Leur point de départ est une analogie directe avec le NLP : une phrase est une séquence de mots, un match est une séquence d'événements. Le mécanisme d'attention du Transformer — qui apprend quels éléments passés sont pertinents pour prédire le suivant — s'applique naturellement.

Mais un match a une structure que le NLP n'a pas : à chaque instant, plusieurs agents (les joueurs) interagissent simultanément. Horton & Lucey représentent cette structure comme une grille à deux dimensions : les lignes sont les joueurs, les colonnes sont les instants. L'attention est appliquée alternativement sur les lignes (pour chaque joueur, que s'est-il passé dans le passé ?) et sur les colonnes (à cet instant, comment les joueurs interagissent-ils entre eux ?). C'est ce qu'ils appellent l'*axial transformer*.

La propriété mathématique clé est que cette variante est *strictement équivalente* à un Transformer séquentiel standard avec un masque particulier — ce n'est pas une approximation. La différence est computationnelle : la complexité passe de O(H²W²) à O((H+W)HW), où H est le nombre de joueurs et W le nombre d'instants. Sur un match typique (40 joueurs × 150 instants), c'est un gain d'un ordre de grandeur, ce qui explique la latence sub-seconde sur CPU.

Leur ablation est rigoureuse : retirer l'attention temporelle (les lignes) ou l'attention inter-agents (les colonnes) dégrade les performances, et les deux contributions sont indépendantes et additives. Le modèle entraîné sur 62 610 matchs de 28 compétitions produit environ 75 000 prédictions par match en temps réel.

---

### Les features pré-match dominent l'architecture

Le résultat le plus contre-intuitif de **Horton & Lucey (2025)** concerne non pas l'architecture mais les données d'entrée. Dans leur étude d'ablation, retirer les features de contexte pré-match — statistiques agrégées sur les matchs récents de chaque joueur, distance depuis le dernier match, contexte de la compétition — dégrade les performances *plus* que retirer les interactions entre joueurs. Sur les passes tentées, l'erreur augmente de +23% sans features pré-match, contre +10% sans interactions entre joueurs.

L'interprétation est simple : un modèle qui ignore qu'un joueur est en forme ou en méforme repart de zéro à chaque match. La dynamique intra-match seule ne peut pas compenser cette ignorance. Ce résultat a une implication directe pour tout projet dans ce domaine : investir du temps sur la qualité des features pré-match avant d'optimiser l'architecture.

**Simpson et al. (2022)** confirment indirectement cette hiérarchie avec leur feature de différentiel de score (`scrad`, valeur entre -6 et +6). C'est la feature contextuelle qui a le plus d'impact sur la diversité des prédictions spatiales du modèle. Un modèle aveugle au score en cours joue "à l'aveugle" sur la dynamique la plus fondamentale d'un match : une équipe qui mène défend, une équipe qui est menée attaque.

---

### L'encodage temporel continu — l'adaptation NLP → événements asynchrones

En NLP, les tokens sont sur une grille entière régulière : mot 1, mot 2, mot 3. L'encodage positionnel de Vaswani et al. (2017) encode ces entiers avec des fonctions sinus et cosinus pour que le modèle sache "où il en est" dans la séquence. Ce mécanisme suppose implicitement que les positions sont régulièrement espacées.

Les événements sportifs ne respectent pas cette hypothèse. Un corner peut survenir à t=12.3 minutes, le suivant à t=34.7 minutes. Utiliser l'encodage positionnel NLP standard revient à traiter ces deux événements comme consécutifs sans tenir compte du délai entre eux — exactement comme si on ignorait la ponctuation dans une phrase.

**Zuo et al. (2020)** fournissent la démonstration empirique la plus claire de l'importance de ce point. Leur ablation compare trois configurations sur un dataset de séquences temporelles :

| Configuration | Log-vraisemblance |
|---|---|
| Attention seule, sans encodage | -5.29 |
| Attention + encodage positionnel NLP (entiers) | -5.25 |
| Attention + encodage temporel continu | **-2.03** |

L'encodage positionnel NLP standard n'apporte presque rien sur des événements asynchrones. L'encodage temporel continu transforme le modèle. La formule encode directement le timestamp réel `t` en vecteur — pas sa position dans la séquence — via des fonctions trigonométriques à différentes fréquences, de façon analogue à l'encodage positionnel mais en domaine continu.

**Yeung et al. (2023)** valident cette intuition différemment. Plutôt que de spécifier une loi a priori pour la distribution du temps entre deux événements (loi gamma, loi exponentielle...), ils laissent le modèle l'apprendre directement. La distribution prédite colle empiriquement à la distribution réelle observée. Cela suggère que si on laisse le modèle libre d'apprendre le temps, il trouve la bonne distribution — à condition de ne pas discrétiser les timestamps en amont.

---

### L'ordre des sorties multiples n'est pas neutre

Quand on prédit simultanément plusieurs caractéristiques du prochain événement — quand il aura lieu, où sur le terrain, de quel type — on peut soit les prédire en parallèle de façon indépendante, soit les conditionner les unes aux autres. **Yeung et al. (2023)** posent explicitement cette question et y répondent empiriquement.

Leur ablation sur les 6 ordres possibles de prédiction (temps → zone → action, action → zone → temps, etc.) montre que l'ordre `temps → zone → action` donne systématiquement les meilleurs résultats, avec un écart de 0.11 sur la loss totale par rapport au pire ordre. La raison est une causalité naturelle que le modèle doit respecter : le timing contraint la zone possible (on ne shoote pas depuis son propre camp à la 89e minute sous pression), et la zone contraint l'action probable (un centre depuis l'intérieur de la surface de réparation est improbable). Modéliser ces dépendances explicitement — en faisant dépendre chaque prédiction des précédentes — améliore la cohérence des sorties.

Ce résultat a une portée plus large : dans un modèle qui prédit 200 types d'événements hétérogènes, certains types sont causalement liés (un corner peut mener à un tir cadré qui peut mener à un but). Laisser ces dépendances implicites dans le mécanisme d'attention est moins efficace que de les encoder explicitement dans l'architecture des têtes de sortie.

---

### Le Transformer ne domine pas toujours — LSTM reste compétitif

**Simpson et al. (2022)** apportent le résultat le plus sobre. Sur des séquences de longueur 100 et avec un dataset modeste (138 matchs), le réseau de neurones récurrent LSTM (*Long Short-Term Memory*, une architecture séquentielle avec des "portes" qui contrôlent ce qu'on retient ou oublie de l'historique) bat le Transformer sur la qualité des prédictions (loss 0.332 contre 0.379). Le Transformer ne gagne que sur la vitesse d'entraînement (1.4 heures contre 15.5 heures) et sur les séquences courtes (longueur 40).

L'explication est connue en NLP également : avec peu de données, le Transformer a tendance à sur-apprendre. LSTM, plus contraint dans sa façon de traiter la séquence, généralise mieux sur les petits datasets. Sur 62 610 matchs comme dans Horton & Lucey, le Transformer reprend l'avantage. Ce résultat a une implication pratique directe : si le dataset de phase 1 est limité à quelques milliers de matchs, tester LSTM avant d'investir dans un axial transformer complet est prudent.

Simpson et al. soulèvent aussi un point rarement discuté : une fenêtre de contexte trop longue (plus de 40 événements passés) peut être contre-productive. Le modèle commence à capter le "style" de l'équipe en général plutôt que la dynamique du match en cours, ce qui biaise les prédictions vers ce que "cette équipe fait habituellement" plutôt que ce qu'elle est en train de faire.

---

### L'attention seule ne discrimine pas le passé récent du passé lointain

**Yeung et al. (2023)** visualisent les poids d'attention sur les 40 événements historiques de leur modèle. Les poids sont distribués uniformément — entre 0.01 et 0.06 par événement — sans décroissance marquée vers les événements anciens. Le mécanisme d'attention apprend certes quels événements sont pertinents, mais il ne privilégie pas structurellement le passé récent.

Cette observation rejoint une contribution de **Dixon & Coles (1997)** qui reste pertinente malgré l'âge du papier. Pour estimer la force des équipes, ils construisent une vraisemblance pondérée où chaque match passé reçoit un poids `φ(t) = exp(-ξt)` décroissant exponentiellement avec son ancienneté. Le paramètre ξ, calibré à 0.0065 par demi-semaine sur données anglaises des années 90, encode que les matchs récents comptent davantage que les anciens. Ce n'est pas une valeur universelle — elle dépend du sport, de la compétition, de la vitesse de rotation des effectifs — mais c'est un point de départ empiriquement justifié pour tout modèle qui calcule des features de forme à partir de l'historique.

---

### Dixon & Coles : prior bayésien et seuil de déploiement

**Dixon & Coles (1997)** modélisent les buts de chaque équipe comme deux lois de Poisson indépendantes. La loi de Poisson est ici le choix naturel : elle modélise le nombre d'occurrences d'un événement rare dans un intervalle de temps fixé — exactement la structure du nombre de buts en 90 minutes. Les paramètres de ces lois sont le produit de la force d'attaque de l'équipe qui marque (α), de la faiblesse défensive de l'équipe qui encaisse (β), et d'un avantage à domicile (γ). Une correction sur les scores faibles (0-0, 1-0, 0-1, 1-1) adresse la légère dépendance entre les scores que l'indépendance pure ne capture pas.

Ce modèle a deux rôles distincts dans un projet de prédiction moderne. D'abord comme **prior pré-match** : les paramètres α et β estimés par maximum de vraisemblance sur les matchs passés sont les meilleures features de force d'équipe disponibles sans entraînement profond. Ils peuvent initialiser le stream continu à t=0 avant que les événements intra-match commencent à mettre à jour la représentation. Ensuite comme **seuil de déploiement** : les cotes bookmakers sont largement dérivées de variantes de Dixon-Coles. Un modèle Transformer qui ne bat pas Dixon-Coles sur le score de Brier (mesure de calibration des probabilités) ne produit rien que les bookmakers ne sachent déjà — il n'a aucune valeur ajoutée pour les paris.

---

### Ce que la littérature ne fait pas

Deux lacunes traversent tous les papiers et constituent des différenciateurs directs.

La première est l'absence des cotes comme feature d'entrée. Dans tous les papiers, les cotes apparaissent uniquement comme benchmark externe — on compare les probabilités du modèle aux cotes après coup. Pourtant les cotes en temps réel sont le signal le plus informatif disponible : elles agrègent l'opinion de milliers de parieurs informés et se mettent à jour quasi-instantanément après chaque événement significatif. Une cote qui chute avant même qu'un but soit officiellement enregistré encode de l'information sur la pression du jeu que les données d'événements bruts ne capturent pas seules. Aucun des papiers ne tente de l'exploiter comme feature.

La seconde est l'absence d'intervalles de confiance garantis. **Horton & Lucey (2025)** évaluent la calibration de leurs distributions marginales mais ne garantissent pas formellement que "quand le modèle annonce 30% de probabilité, l'événement se produit 30% du temps". Cette garantie — obtenue par calibration conformale, une méthode statistique qui ne fait aucune hypothèse sur la distribution des données — est directement actionnable en contexte de paris, où une mauvaise calibration a un coût financier direct et mesurable.



Bonne question — et la réponse est que c'est un choix défendable, pas une erreur.

---

### La logique derrière le dual-stream

Votre data scientist a identifié un problème réel que tous les papiers reconnaissent implicitement : un match produit deux types de signaux qui ont des natures fondamentalement différentes.

D'un côté, des **événements ponctuels** — un corner, un carton, un but — qui arrivent à des instants aléatoires, sont rares, et ont une sémantique discrète. De l'autre, des **signaux continus** — les cotes bookmakers, la possession, le score — qui sont échantillonnés régulièrement et varient de façon lisse.

Écraser ces deux types de données dans un seul flux perd de l'information structurelle. Un corner et une mise à jour de cote ne sont pas du même type de "token". Traiter la cote qui passe de 1.8 à 1.6 comme un événement au même titre qu'un tir cadré est une simplification discutable.

Le dual-stream répond à ce problème en séparant les deux natures de signaux dès l'encodage, puis en les fusionnant via une cross-attention. C'est une solution architecturale propre, bien motivée, et cohérente avec ce que la littérature sur les architectures multimodales recommande — notamment les travaux sur la fusion de modalités hétérogènes en Transformer.

---

### Pourquoi l'axial transformer n'invalide pas ce choix

**Horton & Lucey (2025)** ne traitent pas le même problème que votre data scientist. Leur modèle n'ingère pas de cotes bookmakers. Il travaille uniquement sur des données d'événements structurés — passes, tirs, fautes — qui ont toutes la même nature : des actions ponctuelles avec des attributs homogènes. Dans ce cadre, l'axial transformer est la solution optimale car toutes les entrées sont du même type.

Dès qu'on ajoute les cotes — un signal continu, asynchrone par rapport aux événements, porteur d'une sémantique radicalement différente — la question de comment les intégrer se repose. L'axial transformer ne répond pas à cette question. Il la contourne en ne posant pas le problème.

---

### Le vrai débat

Ce n'est donc pas "dual-stream vs axial transformer" comme si les deux étaient en compétition directe. C'est plutôt : comment intégrer des signaux hétérogènes dans une architecture Transformer ?

Deux approches sont valides :

La première, celle de votre data scientist, sépare explicitement les modalités en deux encodeurs spécialisés et les fusionne par cross-attention. C'est plus complexe à implémenter et à déboguer, mais conceptuellement propre.

La seconde, inspirée de Horton & Lucey, projette toutes les modalités vers un espace de dimension commune via une couche linéaire par modalité, puis les concatène dans une seule grille avant de passer dans l'axial transformer. C'est ce que Horton & Lucey font avec leurs six types d'entrées hétérogènes (features joueur, features équipe, contexte de jeu, etc.). La cross-attention entre modalités est alors gérée implicitement par le mécanisme d'attention standard.

---

### Ce qu'on ne sait pas encore

La littérature ne répond pas à la question de quelle approche est meilleure quand une des modalités est un signal continu à haute fréquence comme les cotes. C'est précisément parce qu'aucun des papiers n'utilise les cotes comme feature que la comparaison empirique n'existe pas.

Ce que votre data scientist a proposé est donc une hypothèse raisonnable, bien motivée, et différenciante. Elle mérite d'être testée — pas remplacée par l'axial transformer sans justification empirique.