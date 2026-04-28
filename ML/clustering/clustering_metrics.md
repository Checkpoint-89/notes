# Évaluer un clustering

Un algorithme de clustering produit une partition des données. Pour mesurer sa qualité, il faut d'abord se demander si on dispose d'étiquettes vraies ou non :

- **Oui** : on compare la partition prédite à la référence. La question est *dans quelle mesure les deux partitions s'accordent-elles ?*
- **Non** : on interroge directement la géométrie. La question est *les groupes sont-ils compacts et bien séparés ?*

Derrière ces deux questions se trouvent deux principes mathématiques distincts : l'**ajustement au hasard sous un modèle de permutation** pour la comparaison de partitions, l'**inertie et les distances** pour la cohérence géométrique. Les métriques concrètes — ARI, AMI, silhouette — en sont des opérationnalisations.

---

## Principe 1 : ajustement au hasard (métriques externes)

Le principe commun à toutes les métriques externes est l'**ajustement au hasard sous un modèle de permutation à marges fixes** : on mesure l'accord observé entre deux partitions, on soustrait ce qu'un tirage aléatoire aurait produit (en conservant les tailles de clusters), et on normalise. *Marges fixes* signifie que le clustering aléatoire de référence conserve exactement les mêmes effectifs par cluster que les partitions réelles — seule l'identité des points dans chaque groupe change. Ce qui varie d'une métrique à l'autre, c'est la *quantité d'accord* qu'on choisit de mesurer.

- L'**AMI** mesure l'accord via l'**information mutuelle** : dans quelle mesure connaître le cluster d'un point dans $U$ réduit-il l'incertitude sur son cluster dans $V$ ?

$$I(U; V) = H(U) - H(U \mid V)$$

où $H(U \mid V) = H(U)$ si les partitions sont indépendantes ($I = 0$), et $H(U \mid V) = 0$ si l'une détermine parfaitement l'autre ($I = H(U)$, maximal).

- L'**ARI** mesure l'accord via le **comptage de paires** : dans quelle mesure deux points traités de la même façon dans $U$ (ensemble ou séparés) le sont-ils aussi dans $V$ ?

Même logique d'ajustement, deux formalisations : entropique pour l'AMI, combinatoire pour l'ARI.

---

## ARI et AMI — deux opérationnalisations

| | **ARI** — Adjusted Rand Index | **AMI** — Adjusted Mutual Information |
|--|--|--|
| *approche* | combinatoire, raisonne sur les paires | entropique, raisonne sur les points |
| **Données** | $N = \binom{n}{2}$ paires ; concordantes si traitées pareil dans $U$ et $V$ (cases $a$ : même/même, $d$ : diff./diff.), discordantes sinon ($b$, $c$) | table de contingence $n_{kl}$ — points dans le cluster $k$ de $U$ et $l$ de $V$, marges $n_k = \sum_l n_{kl}$, $n_l = \sum_k n_{kl}$ |
| **Score brut** | $\text{RI} = \frac{a + d}{N}$ — proportion de paires concordantes | $I(U;V) = \sum_{k,l} \frac{n_{kl}}{n} \log \frac{n \cdot n_{kl}}{n_k \cdot n_l}$ — réduction d'incertitude sur un point |
| **Problème du hasard** | le terme $d$ domine dès que les clusters sont nombreux et petits — RI proche de 1 même sans structure commune | $I > 0$ même au hasard : croît mécaniquement avec le nombre de clusters, sans structure réelle |
| **Baseline** | $\mathbb{E}[\text{RI}] = \frac{PQ + (N-P)(N-Q)}{N^2}$, avec $P = \sum_k \binom{n_k}{2}$, $Q = \sum_l \binom{n_l}{2}$ | $\mathbb{E}[I]$ : somme pondérée sur les valeurs possibles de $n_{kl}$ — exact, sans forme close simple |
| **Score ajusté** | $\text{ARI} = \frac{\text{RI} - \mathbb{E}[\text{RI}]}{1 - \mathbb{E}[\text{RI}]}$ | $\text{AMI} = \frac{I(U;V) - \mathbb{E}[I]}{\frac{H(U)+H(V)}{2} - \mathbb{E}[I]}$, où $H(U) = -\sum_k \frac{n_k}{n} \log \frac{n_k}{n}$ |

**Dérivation de $\mathbb{E}[\text{RI}]$.** On tire au sort les affectations de $U$ et de $V$ séparément — deux mélanges indépendants. Pour une paire quelconque, la probabilité qu'elle tombe dans le même cluster de $U$ est $P/N$ (fraction des paires qui sont intra-cluster dans $U$), et la probabilité qu'elle tombe dans le même cluster de $V$ est $Q/N$. Comme les deux mélanges sont indépendants, ces deux événements le sont aussi : on peut multiplier les probabilités. Donc la probabilité d'être en case $a$ (même cluster dans les deux partitions) est $\frac{P}{N} \cdot \frac{Q}{N}$, et en case $d$ (séparée dans les deux) est $\left(1-\frac{P}{N}\right)\left(1-\frac{Q}{N}\right)$. Par linéarité de l'espérance sur les $N$ paires : $\mathbb{E}[a] = PQ/N$, $\mathbb{E}[d] = (N-P)(N-Q)/N$, et la formule suit.

**Normalisation de l'AMI.** Le dénominateur utilise la moyenne arithmétique des entropies — le choix de scikit-learn. D'autres normalisations (min ou max des entropies) sont possibles et donnent des valeurs légèrement différentes.

<details><summary>Remarque — modèle de Hubert & Arabie</summary>

Ce modèle de permutations séparées est distinct du modèle hypergéométrique de Hubert & Arabie (marges fixées simultanément). Dans ce dernier, les deux partitions sont mélangées conjointement sous une seule contrainte, ce qui crée une légère dépendance entre les événements. Les deux donnent le même $\mathbb{E}[\text{RI}]$, mais l'argument de multiplication des probabilités ci-dessus n'est rigoureux que dans le modèle de permutations séparées.

</details>

### Lecture commune

- **Score = 1** : partitions identiques.
- **Score ≈ 0** : accord compatible avec deux partitions indépendantes.
- **Score < 0** : pire que le hasard.
- **Symétrie** : les deux scores sont symétriques — comparer $U$ à $V$ donne le même résultat que $V$ à $U$.
- **Limite** : ni l'ARI ni l'AMI ne disent *pourquoi* les partitions divergent — seulement *combien*. Ce sont des scalaires globaux, pas des diagnostics.
- **Biais selon le nombre de clusters** : l'ARI tend à favoriser les solutions avec peu de clusters larges — le terme $d$ domine mécaniquement quand les clusters sont nombreux et petits, comme développé ci-dessus. L'AMI est moins sensible à ce biais. C'est un critère pratique pour choisir entre les deux.

---

## Principe 2 : l'inertie (métriques internes)

Sans étiquettes de référence, on interroge la géométrie des données. Le principe unificateur est l'**inertie intra-cluster** : pour un cluster $C$ de centroïde $\mu$ et de taille $n_C$,

$$W(C) = \frac{1}{n_C} \sum_{x \in C} \|x - \mu\|^2$$

Un bon clustering minimise cette quantité — les points sont proches de leur centre. K-means minimise directement $\sum_C W(C)$.

**Inertie intra vs inertie inter.** L'inertie totale se décompose en deux termes :

$$\underbrace{\frac{1}{n}\sum_{x} \|x - \mu\|^2}_{\text{inertie totale}} = \underbrace{\sum_C \frac{n_C}{n} W(C)}_{\text{intra}} + \underbrace{\sum_C \frac{n_C}{n} \|\mu_C - \mu\|^2}_{\text{inter}}$$

L'inertie totale est fixe (elle ne dépend que des données). Minimiser l'intra revient donc à maximiser l'inter — **à $k$ fixé**. Dès qu'on fait varier $k$, l'équivalence disparaît : l'inertie intra décroît mécaniquement quand $k$ augmente, même sans structure réelle. C'est pourquoi elle ne suffit pas à choisir $k$, ni à évaluer la séparation entre clusters.

Il existe également une identité reliant inertie intra et distances entre points :

$$\frac{1}{n_C} \sum_{x \in C} \|x - \mu\|^2 = \frac{1}{2n_C^2} \sum_{x,y \in C} \|x - y\|^2$$

L'inertie est donc la moitié de la distance quadratique moyenne entre deux points du cluster. C'est cette reformulation qui connecte l'inertie à la silhouette.

---

## Silhouette

### Construction

K-means minimise l'inertie totale, mais ne dit pas si un cluster est bien séparé de ses voisins. La silhouette corrige cela en normalisant l'inertie locale de chaque point par la distance au cluster voisin.

Pour chaque point $i$ :

- $a(i)$ : distance moyenne de $i$ aux autres points de son cluster. Par l'identité ci-dessus, $a(i)$ est une version *locale* de $\sqrt{W(C)}$, calculée du point de vue de $i$ seul plutôt que du centroïde.
- $b(i)$ : distance moyenne de $i$ aux points du cluster voisin le plus proche.

$$s(i) = \frac{b(i) - a(i)}{\max(a(i),\, b(i))}$$

### Lecture

$s(i) \in [-1, 1]$ :

- $s(i) \approx 1$ : $a(i) \ll b(i)$, le point est compact dans son cluster et loin du voisin — bien placé.
- $s(i) \approx 0$ : $a(i) \approx b(i)$, le point est à la frontière entre deux clusters.
- $s(i) \approx -1$ : $a(i) \gg b(i)$, le point serait mieux dans le cluster voisin — mal affecté.

Le score global est la moyenne des $s(i)$.

### Ce que la silhouette ajoute à l'inertie

Minimiser l'inertie intra (k-means) et maximiser la silhouette sont alignés — réduire $a(i)$ améliore les deux. Mais ils ne sont pas équivalents : la silhouette normalise par $b(i)$, ce que k-means ignore. Un clustering peut avoir une faible inertie intra tout en ayant une mauvaise silhouette si les clusters sont proches les uns des autres.

**Dépendance à la métrique.** Contrairement à l'ARI, la silhouette dépend entièrement de la distance choisie — comme l'inertie dont elle découle. Un bon score avec la distance euclidienne peut masquer une structure pertinente visible avec une autre métrique (voir [Mesurer la proximité](../../maths%20appliquées/2.%20mesurer-la-proximite.md)).

**Utilisation pratique.** Tracer le score de silhouette moyen en fonction du nombre de clusters $k$ permet de choisir $k$ sans étiquettes — on cherche un pic. C'est l'un des rares guides internes disponibles pour ce choix.
