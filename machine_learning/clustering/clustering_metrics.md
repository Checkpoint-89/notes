# Évaluer un clustering

Un algorithme de clustering produit une partition des données. Pour mesurer sa qualité, il faut d'abord se demander si on dispose d'étiquettes vraies ou non :

- **Oui** : on compare la partition prédite à la référence. La question est *dans quelle mesure les deux partitions s'accordent-elles ?*
- **Non** : on interroge directement la géométrie. La question est *les groupes sont-ils compacts et bien séparés ?*

Ces deux questions appellent des choix distincts : comment **représenter** une partition mathématiquement, et quelle **mesure d'accord** utiliser dans cette représentation. ARI et AMI répondent à ces deux choix différemment, tout en partageant la même structure de normalisation. La silhouette opère directement sur la géométrie des données, sans comparer deux partitions.

---

## Principe 1 : comparer deux partitions (métriques externes)

ARI et AMI partagent la même structure de normalisation :

$$\text{score ajusté} = \frac{\text{accord observé} - \text{accord attendu par hasard}}{\text{accord maximal} - \text{accord attendu par hasard}}$$

Ce qui les distingue est double — la **représentation** choisie pour encoder une partition, et la **métrique** choisie pour mesurer l'accord entre deux partitions ainsi encodées.

- L'**ARI** encode la partition comme une **relation binaire sur les paires** :

$$\text{partition} \to \text{relation d'équivalence } (i \sim_U j) \to \text{co-appartenance des paires} \to \text{matrice } C_U(i,j) = \mathbf{1}[i \sim_U j,\; i \neq j], \quad C_U(i,i) = 0$$

La métrique d'accord est le **produit scalaire de Frobenius** entre $C_U$ et $C_V$.

- L'**AMI** encode la partition comme une **variable aléatoire** sur les points :

$$\text{partition} \to \text{variable aléatoire } U(x) \to \text{distribution jointe des clusters} \to \text{table de contingence } n_{kl}$$

La métrique d'accord est l'**information mutuelle** :

$$I(U; V) = H(U) - H(U \mid V)$$

où $H(U \mid V) = H(U)$ si les partitions sont indépendantes, et $H(U \mid V) = 0$ si l'une détermine parfaitement l'autre.

La normalisation par rapport au hasard (tailles de clusters fixées, affectations mélangées) est identique dans les deux cas.

---

## ARI et AMI — deux opérationnalisations

$$\text{ARI} : \text{partition} \to \text{relation d'équivalence} \to \text{paires} \qquad\qquad \text{AMI} : \text{partition} \to \text{variable aléatoire} \to \text{entropie}$$

| | **ARI** | **AMI** |
|--|--|--|
| **Objet** | matrice de co-appartenance $C_U(i,j) = \mathbf{1}[i \sim_U j]$ pour $i \neq j$, diag. = 0 | table de contingence $n_{kl} = \|U_k \cap V_l\|$, marges $n_k$, $n_l$ |
| **Score brut** | $I = \tfrac{1}{2}\langle C_U, C_V\rangle_F = \sum_{kl}\binom{n_{kl}}{2}$ — paires ensemble dans les deux | $I(U;V) = \sum_{k,l} \frac{n_{kl}}{n} \log \frac{n \cdot n_{kl}}{n_k \cdot n_l}$ |
| **Baseline** | $\mathbb{E}[I] = \frac{PQ}{N}$, avec $N=\binom{n}{2}$, $P = \sum_k\binom{n_k}{2}$, $Q = \sum_l\binom{n_l}{2}$ | $\mathbb{E}[I(U;V)]$ — calculable exactement comme somme sur les valeurs possibles de $n_{kl}$, mais sans expression compacte analogue à $PQ/N$ |
| **Maximum** | $\frac{P+Q}{2}$ | $\frac{H(U)+H(V)}{2}$, où $H(U) = -\sum_k \frac{n_k}{n}\log\frac{n_k}{n}$ |
| **Score ajusté** | $\text{ARI} = \dfrac{I - \mathbb{E}[I]}{\frac{P+Q}{2} - \mathbb{E}[I]}$ | $\text{AMI} = \dfrac{I(U;V) - \mathbb{E}[I]}{\frac{H(U)+H(V)}{2} - \mathbb{E}[I]}$ |

**Lecture matricielle.** La matrice $C_U - C_V$ vaut $\pm 1$ exactement sur les paires en désaccord, 0 ailleurs. Donc $\|C_U - C_V\|_F^2 = 2 \times \text{nombre de désaccords}$, et $RI = 1 - \frac{\|C_U - C_V\|_F^2}{2N}$ est bien la proportion de paires concordantes. Le score brut $I = \frac{1}{2}\langle C_U, C_V\rangle_F$ ne compte que les paires ensemble dans les deux partitions — la correction du hasard absorbe la contribution des paires séparées dans les deux, qui domineraient sinon.

**Baseline de l'ARI.** Sous le modèle de permutations séparées et indépendantes, la probabilité qu'une paire soit intra-cluster dans $U$ est $P/N$, et dans $V$ est $Q/N$. Par indépendance, $\mathbb{E}[I] = N \cdot \frac{P}{N} \cdot \frac{Q}{N} = \frac{PQ}{N}$.

**Normalisation de l'AMI.** Le dénominateur $\frac{H(U)+H(V)}{2}$ est le choix de scikit-learn (moyenne arithmétique). D'autres normalisations (min ou max des entropies) sont possibles et donnent des valeurs légèrement différentes.

### Lecture commune

- **Score = 1** : partitions identiques.
- **Score ≈ 0** : accord compatible avec deux partitions indépendantes.
- **Score < 0** : pire que le hasard.
- **Symétrie** : les deux scores sont symétriques — comparer $U$ à $V$ donne le même résultat que $V$ à $U$.
- **Limite** : ni l'ARI ni l'AMI ne disent *pourquoi* les partitions divergent — seulement *combien*. Ce sont des scalaires globaux, pas des diagnostics.
- **Biais selon le nombre de clusters** : deux solutions avec le même taux de recouvrement relatif (même fraction de paires correctement groupées ensemble) n'obtiennent pas le même ARI si elles n'ont pas le même nombre de clusters. L'ARI favorise les solutions avec peu de clusters larges. Le mécanisme : $I = \sum_{kl}\binom{n_{kl}}{2}$ croît quadratiquement avec la taille des chevauchements — des clusters deux fois plus gros produisent environ quatre fois plus de paires concordantes, et la correction $\mathbb{E}[I] = PQ/N$ ne compense pas complètement cet effet. L'AMI n'a pas ce biais : la MI brute a un biais *opposé* (elle augmente mécaniquement avec le nombre de clusters, car plus de clusters capturent plus de détail), et l'ajustement corrige précisément cet effet. Le résultat net est que l'AMI est approximativement neutre par rapport au nombre de clusters.

---

## Principe 2 : l'inertie (métriques internes)

Sans étiquettes de référence, on interroge la géométrie des données. Le principe unificateur est l'**inertie intra-cluster** : pour un cluster $C$ de centroïde $\mu$ et de taille $n_C$,

$$W(C) = \frac{1}{n_C} \sum_{x \in C} \|x - \mu\|^2$$

Un bon clustering minimise cette quantité — les points sont proches de leur centre. K-means minimise directement $\sum_C W(C)$.

**Inertie intra vs inertie inter.** L'inertie totale se décompose en deux termes :

$$\underbrace{\frac{1}{n}\sum_{x} \|x - \mu\|^2}_{\text{inertie totale}} = \underbrace{\sum_C \frac{n_C}{n} W(C)}_{\text{intra}} + \underbrace{\sum_C \frac{n_C}{n} \|\mu_C - \mu\|^2}_{\text{inter}}$$

L'inertie totale est fixe (elle ne dépend que des données). Intra et inter sont donc redondantes : connaître l'une détermine l'autre. Pour discriminer entre deux clusterings, il faut un critère qui mette en rapport la compacité intra-cluster et la séparation inter-cluster — et non l'une ou l'autre séparément. C'est ce que fait la silhouette.

Il existe également une identité reliant inertie intra et distances entre points :

$$\frac{1}{n_C} \sum_{x \in C} \|x - \mu\|^2 = \frac{1}{2n_C^2} \sum_{x,y \in C} \|x - y\|^2$$

L'inertie est donc la moitié de la distance quadratique moyenne entre deux points du cluster. C'est cette reformulation qui connecte l'inertie à la silhouette.

---

## Silhouette

### Point de départ : ce que l'inertie ne mesure pas

K-means minimise l'inertie intra-cluster :

$$W = \sum_C \frac{1}{n_C} \sum_{x \in C} \|x - \mu_C\|^2$$

C'est une mesure de **compacité**. Mais un clustering peut être compact et pourtant mauvais : si les clusters sont très proches les uns des autres, des points compacts dans leur cluster restent ambigus quant à leur appartenance.

L'inertie intra-cluster ignore complètement la **séparation** entre clusters. La silhouette remédie à cela en mettant les deux en rapport — pour chaque point individuellement.

### Construction pas à pas

L'idée directrice : réécrire l'inertie comme une moyenne de distances entre paires de points, puis la localiser à chaque point individuellement — ce qui permet d'introduire naturellement la distance au cluster voisin. La silhouette est le rapport entre ces deux quantités, normalisé pour être interprétable.

1. **Reformuler l'inertie sans centroïde** — montrer que $W(C)$ est une moyenne pairwise.
2. **Localiser à un point** — fixer un des deux arguments pour obtenir $a(i)$, la compacité vue de $x_i$.
3. **Introduire la séparation** — calculer $b(i)$, la distance de $x_i$ au cluster voisin le plus proche.
4. **Mettre les deux en rapport** — normaliser par $\max(a(i), b(i))$ pour obtenir $s(i) \in [-1, 1]$.
5. **Revenir à l'ensemble** — moyenner les $s(i)$ sur tous les points pour obtenir $\bar{s}$, score global du clustering.

#### Étape 1 : reformuler l'inertie sans centroïde

L'inertie d'un cluster peut s'écrire de deux façons :

$$\underbrace{\frac{1}{n_C}\sum_{x \in C} \|x - \mu_C\|^2}_{\text{distance moyenne au centroïde}} = \underbrace{\frac{1}{2n_C^2}\sum_{x,y \in C} \|x - y\|^2}_{\text{distance quadratique moyenne entre points}}$$

Cette identité révèle que l'inertie est fondamentalement une quantité **pairwise** : elle mesure à quel point les points d'un cluster sont écartés les uns des autres, sans avoir besoin du centroïde.

C'est l'idée germinale de la silhouette.

#### Étape 2 : localiser cette idée à un point

Au lieu d'une moyenne sur tout le cluster, on regarde chaque point $x_i$ individuellement :

$$a(i) = \frac{1}{|C_i| - 1} \sum_{j \in C_i,\; j \neq i} \|x_i - x_j\|$$

**$a(i)$ est la distance moyenne du point $x_i$ aux autres membres de son cluster.**

On fixe ici l'un des deux arguments de la somme double à $x_i$ — ce qui ressemble à réintroduire un centre. Mais c'est précisément la liberté gagnée à l'étape 1 : la formulation pairwise ne privilégie aucun point particulier, donc on peut choisir librement le point de référence. En choisissant $x_i$ lui-même — un point réel des données, pas un agrégat — on rend la mesure locale à chaque point, ce qui permettra au pas suivant de la mettre en regard avec la distance au cluster voisin.

> **$a(i)$ petit** → le point est proche des autres membres de son cluster → compacité locale forte.

#### Étape 3 : introduire la séparation

Pour chaque cluster $C' \neq C_i$, on calcule la distance moyenne du point $x_i$ aux membres de $C'$ :

$$d(i, C') = \frac{1}{|C'|} \sum_{j \in C'} \|x_i - x_j\|$$

Puis on retient la distance au cluster voisin le plus proche :

$$b(i) = \min_{C' \neq C_i} d(i, C')$$

**$b(i)$ est la distance moyenne du point $x_i$ aux membres du cluster voisin le plus proche.**

> **$b(i)$ grand** → $i$ est loin de tout autre cluster → l'affectation est sans ambiguïté.

#### Étape 4 : mettre les deux en rapport

$$\boxed{s(i) = \frac{b(i) - a(i)}{\max(a(i),\; b(i))}}$$

Le dénominateur normalise : $s(i) \in [-1, 1]$ quelle que soit l'échelle des données.

### Lecture de $s(i)$

| Valeur | Situation | Interprétation |
|--------|-----------|----------------|
| $s(i) \approx 1$ | $a(i) \ll b(i)$ | compact dans son cluster, loin du voisin — bien placé |
| $s(i) \approx 0$ | $a(i) \approx b(i)$ | à la frontière entre deux clusters |
| $s(i) \approx -1$ | $a(i) \gg b(i)$ | serait mieux dans le cluster voisin — mal affecté |

La silhouette d'un clustering est la moyenne des $s(i)$ : $\bar{s} = \frac{1}{n}\sum_i s(i)$.

### Ce que la silhouette fait que l'inertie ne fait pas

Considérons deux scénarios avec la même inertie intra :

- **Scénario A** : clusters compacts, bien espacés. $a(i)$ petit, $b(i)$ grand → $s(i) \approx 1$.
- **Scénario B** : clusters compacts, mais très proches les uns des autres. $a(i)$ petit, $b(i)$ aussi petit → $s(i) \approx 0$.

L'inertie ne distingue pas A de B. La silhouette si.

### Remarques pratiques

**Choisir $k$.** Tracer $\bar{s}$ en fonction du nombre de clusters $k$ permet de choisir $k$ sans étiquettes — on cherche un pic. C'est l'un des rares critères internes disponibles pour ce choix.

**Dépendance à la métrique.** La silhouette hérite de la métrique choisie pour $\|\cdot\|$. Changer la distance peut changer radicalement les scores et même le $k$ optimal. Un bon score en distance euclidienne ne garantit pas que la structure découverte est pertinente dans une autre métrique (voir [Mesurer la proximité](../../maths%20appliquées/2.%20mesurer-la-proximite.md)).

**Complexité.** Le calcul naïf est en $O(n^2)$ (toutes les distances pairwise). Pour de grands jeux de données, des approximations sont nécessaires.
