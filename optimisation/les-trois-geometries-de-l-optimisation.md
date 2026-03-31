# Les trois géométries de l'optimisation

Tout problème d'optimisation en machine learning repose sur un préalable et trois choix. Le préalable fixe l'espace de travail. Les trois choix imposent chacun une géométrie distincte sur cet espace.

---

## Préalable : la représentation

Change l'espace dans lequel on pose le problème.

- **PCA** : projection linéaire, réduit la dimension.
- **Kernels** : plongement non linéaire, augmente la dimension pour linéariser le problème.
- **Deep learning** : transformation apprise, construit les features pertinentes.

La représentation intervient **avant** tout le reste. Elle détermine l'espace dans lequel la distance, le coût et le gradient opèrent. Ce n'est pas une géométrie — c'est le choix du terrain.

---

## 1) Distance / norme — géométrie de l'espace

Définit ce que "proche" veut dire.

- Forme de la boule unité : ronde (L²), losange (L¹), carrée (L∞).
- Détermine quels points sont voisins, quelles directions sont courtes ou longues.

La distance intervient à plusieurs endroits :

- **Dans les données** : k-NN, clustering — on mesure directement la proximité entre observations.
- **Dans le coût** : l'attache aux données (‖y − Xβ‖) et la pénalité (‖β‖₁, ‖β‖₂) sont des normes.
- **Dans l'optimisation** : la métrique du gradient est elle-même une distance sur l'espace des paramètres (voir point 3).

---

## 2) Fonction de coût — géométrie du problème

Définit le paysage qu'on optimise : à chaque jeu de paramètres, une hauteur. Les minima de ce paysage sont les solutions.

- **OLS** : paraboloïde lisse. Un seul minimum. Le gradient y mène de partout.
- **Ridge** : paraboloïde resserré autour de l'origine. Le minimum se déplace vers des coefficients plus petits. Le paysage reste lisse.
- **Lasso** : paraboloïde avec des arêtes vives sur les axes. Le paysage incline vers les axes (guide les coefficients vers zéro) et y crée des coins (les piège à zéro).

La fonction de coût détermine **où sont les solutions**. Elle ne dit rien sur comment on s'y rend.

---

## 3) Métrique du gradient — géométrie de la descente

Définit comment on se déplace dans le paysage. La direction de descente dépend d'une métrique sur l'espace des paramètres :

- **Gradient classique** : métrique euclidienne (L²). Toutes les directions sont traitées de la même façon.
- **Préconditionnement** (Newton, Adam…) : métrique adaptative. Les directions mal conditionnées sont corrigées — on avance plus vite dans les directions plates, plus prudemment dans les directions raides.
- **Gradient naturel** : métrique de Fisher sur l'espace des distributions. La descente suit la géométrie du modèle statistique, pas celle des coordonnées.

La métrique change les trajectoires et la vitesse de convergence. **Elle ne change pas les minima** — ceux-ci sont fixés par la fonction de coût.

---

## Résumé

| Choix | Question | Détermine |
|---|---|---|
| **Représentation** | Dans quel espace travaille-t-on ? | Le terrain — les variables, la dimension |
| **Distance** | Qu'est-ce qui est proche ? | La géométrie de l'espace |
| **Fonction de coût** | Qu'est-ce qu'on optimise ? | La forme du paysage, la position des solutions |
| **Métrique du gradient** | Comment se déplace-t-on ? | Les trajectoires, la vitesse de convergence |

La distance intervient dans les trois derniers : elle peut définir l'attache aux données, façonner la pénalité, et déterminer la métrique de descente. Mais ces trois rôles sont des **choix indépendants**. On peut mesurer les écarts aux données en L², pénaliser en L¹, et descendre selon une métrique de Newton. Chaque choix impose sa propre géométrie.

---

**En une ligne** : la représentation fixe l'espace, la distance y définit la proximité, le coût y dessine le paysage, et la métrique du gradient y trace le chemin.