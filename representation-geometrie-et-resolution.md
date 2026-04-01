# Représentation, géométrie et résolution

Beaucoup de problèmes en mathématiques appliquées, en statistique, en optimisation ou en apprentissage ne consistent pas seulement à "chercher une solution". Ils consistent à trouver un **bon compromis** entre trois choix :

1. la **représentation** des données du problème,
2. la **géométrie** dans laquelle on le formule,
3. les **méthodes** utilisées pour le résoudre.

Ces trois choix se contraignent mutuellement. Une représentation rend certaines géométries naturelles ; une géométrie favorise certaines méthodes ; une contrainte algorithmique peut pousser à changer la représentation elle-même.

**En une ligne** : on cherche une représentation qui rende le problème plus simple, une géométrie adaptée au type de solution cherché, des méthodes efficaces dans cette représentation et cette géométrie.

---

## 1) Représentation

Premier choix : **dans quel espace pose-t-on le problème ?**

La représentation fixe le terrain de travail : les variables, les coordonnées, la dimension, les invariances, les relations qu'on choisit de rendre simples ou visibles.

- **Changement de variables** : reformule le problème dans un espace plus commode.
- **PCA** : projection linéaire, réduit la dimension et met en avant les directions dominantes.
- **Kernels** : plongement implicite dans un espace où certaines séparations deviennent linéaires.
- **Deep learning** : représentation apprise à partir des données.

Une bonne représentation ne résout pas encore le problème, mais elle peut le rendre plus simple, plus régulier, plus séparable, plus parcimonieux, ou plus stable numériquement.

---

## 2) Géométrie du problème

Une fois le problème représenté dans un espace, il faut définir ce que signifie **bien le résoudre** dans cet espace.

C'est le rôle de la géométrie du problème. Elle fixe les notions pertinentes : proximité, taille, régularité, séparation, coût, contrainte, admissibilité. Autrement dit, elle donne au problème sa forme mathématique effective.

Cette géométrie peut apparaître de plusieurs façons :

- par une **distance** ou une **norme**, qui dit ce que signifie "être proche" ou "être petit" ;
- par une **fonction de coût**, qui donne une hauteur à chaque solution possible ;
- par une **contrainte**, qui restreint l'ensemble des solutions admissibles ;
- par une **régularisation**, qui privilégie certaines solutions plutôt que d'autres.

Quelques exemples :

- En **clustering**, la distance choisie détermine ce qu'on considère comme un groupe.
- En **k-NN**, la métrique définit les voisins pertinents.
- En **régression**, la fonction de coût définit ce qu'est une bonne approximation.
- En **Ridge** ou **Lasso**, la pénalisation ajoute une structure géométrique supplémentaire : elle favorise soit des coefficients petits, soit des solutions parcimonieuses.

La géométrie du problème détermine donc non seulement où se trouvent les bonnes solutions, mais aussi ce que "bonne solution" veut dire.

---

## 3) Méthodes de résolution

Une fois le problème représenté et géométriquement formulé, il faut encore le résoudre effectivement.

Chaque méthode de résolution fait des hypothèses sur la structure du problème et exploite certaines propriétés géométriques plutôt que d'autres. Le choix de la méthode détermine ce qu'on peut obtenir en pratique : vitesse, stabilité, sensibilité aux mauvaises échelles, qualité de l'approximation, possibilité même de calculer la solution.

- **Gradient classique** : suppose une géométrie euclidienne — toutes les directions sont traitées de la même façon.
- **Préconditionnement / Newton** : exploite la courbure locale pour corriger les directions mal conditionnées.
- **Gradient naturel** : exploite la géométrie statistique du modèle plutôt que celle des coordonnées.
- **k-means** : suppose une géométrie euclidienne (centroïdes = moyennes, cellules de Voronoï). Changer la distance change l'algorithme entier.
- **k-medoids** : ne suppose pas de structure euclidienne — fonctionne avec une distance quelconque.
- **DBSCAN** : exploite la notion de voisinage induite par la métrique. Changer la métrique change les clusters.
- **Clustering hiérarchique** : dépend du couple distance + critère de liaison.

Dans tous les cas, la méthode impose des contraintes sur la géométrie du problème qu'elle est capable d'exploiter. Un décalage entre la géométrie du problème et les hypothèses de la méthode se paie en performance ou en qualité de solution.

---

## Résumé

| Choix | Question | Détermine |
|---|---|---|
| **Représentation** | Dans quel espace pose-t-on le problème ? | Le terrain de travail |
| **Géométrie du problème** | Que signifie bien résoudre le problème dans cet espace ? | La forme mathématique du problème |
| **Méthodes de résolution** | Comment trouver effectivement une solution ? | La dynamique et le coût du calcul |

**À retenir** : résoudre un problème, ce n'est pas seulement chercher une solution dans un espace donné. C'est trouver un bon compromis entre une représentation des données, une géométrie du problème et des méthodes de résolution adaptées.