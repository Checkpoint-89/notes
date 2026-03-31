# Projection orthogonale et produit scalaire

## Espaces euclidiens et hilbertiens

Un **espace euclidien** est un espace vectoriel réel de dimension finie muni d'un produit scalaire. Un **espace de Hilbert** est la généralisation en dimension quelconque (éventuellement infinie) : c'est un espace vectoriel muni d'un produit scalaire, complet pour la norme qu'il induit. La complétude — toute suite de Cauchy converge vers un élément de l'espace — est ce qui garantit qu'on peut passer à la limite sans sortir de l'espace. Sans elle, une suite d'approximations de plus en plus proches d'un optimum pourrait converger vers un point qui n'appartient pas à l'espace, rendant les résultats d'existence (meilleure approximation, projection) caducs. En dimension finie, la complétude est automatique ; en dimension infinie, elle doit être exigée.

Mais en dimension infinie apparaît une autre subtilité. Chercher le plus proche point de x dans V, c'est minimiser ‖x − v‖ sur V. On peut construire une suite minimisante vₙ ∈ V dont la distance à x tend vers le minimum. Deux conditions garantissent que ce minimum est atteint : la complétude de E assure que la suite converge vers un point de E ; la fermeture de V assure que ce point est dans V. En dimension finie, tout sous-espace est automatiquement fermé. En dimension infinie, il faut le vérifier. Dans toute la suite, "sous-espace" signifie sous-espace fermé.

Avec ces deux garanties — complétude de l'espace et fermeture des sous-espaces — tout ce qui suit est valable aussi bien en espace euclidien qu'en espace de Hilbert.

## Produit scalaire

Un **produit scalaire** sur un espace vectoriel réel E est une forme bilinéaire symétrique ⟨·,·⟩ : E × E → ℝ qui vérifie :

- **Bilinéarité** : linéaire en chaque variable
- **Symétrie** : ⟨x,y⟩ = ⟨y,x⟩
- **Positivité** : ⟨x,x⟩ ≥ 0 pour tout x

La quatrième condition — celle qui interdit la dégénérescence — admet deux formulations équivalentes :

- **(Définie positive — vue analyse)** : ⟨x,x⟩ ≥ 0 pour tout x, et ⟨x,x⟩ = 0 ⟹ x = 0. On regarde le signe : la forme est positive et ne s'annule qu'en zéro.
- **(Non dégénérée positive — vue algèbre)** : ⟨x,x⟩ ≥ 0 pour tout x, et si ⟨x,y⟩ = 0 pour tout y, alors x = 0. On regarde le noyau : la forme est positive et aucun vecteur non nul n'est orthogonal à tout l'espace.

**Pourquoi ces deux conditions sont équivalentes.** Définie positive ⟹ non dégénérée : si ⟨x,y⟩ = 0 pour tout y, en particulier pour y = x, donc ⟨x,x⟩ = 0, donc x = 0. Non dégénérée ⟹ définie positive : supposons ⟨x,x⟩ = 0 avec x ≠ 0. Par positivité, ⟨x,x⟩ ≥ 0, donc ⟨x,x⟩ = 0. Par Cauchy-Schwarz (qui ne requiert que bilinéarité, symétrie et positivité), |⟨x,y⟩|² ≤ ⟨x,x⟩⟨y,y⟩ = 0 pour tout y. Donc ⟨x,y⟩ = 0 pour tout y, ce qui contredit la non-dégénérescence.

La vue analyse est plus directe et plus courante. La vue algèbre est plus naturelle en algèbre linéaire : elle dit que l'application x ↦ ⟨x,·⟩ (qui à chaque vecteur associe une forme linéaire) est injective — c'est l'analogue du théorème de représentation de Riesz (trivial en dimension finie, profond en Hilbert).

## Pythagore découle de la bilinéarité

Si x = p + e avec ⟨p,e⟩ = 0, alors :

‖x‖² = ⟨p + e, p + e⟩ = ⟨p,p⟩ + 2⟨p,e⟩ + ⟨e,e⟩ = ‖p‖² + ‖e‖²

C'est tout. Pythagore n'est pas un théorème de géométrie ajouté au produit scalaire — c'est une conséquence directe de la bilinéarité. Développer le carré d'une somme dans un produit scalaire, c'est exactement la même opération que développer (a+b)² = a² + 2ab + b² : le terme croisé est 2⟨p,e⟩, et l'orthogonalité le fait disparaître.

## La projection orthogonale est la meilleure estimation

Soit V un sous-espace fermé de E et x ∈ E. On cherche le point de V le plus proche de x : le vecteur p ∈ V qui minimise ‖x − p‖.

**La décomposition existe.** Posons e = x − p. On veut p ∈ V et e ⊥ V. L'orthogonal de V, noté V⊥ = {z ∈ E : ⟨z,v⟩ = 0 pour tout v ∈ V}, est lui-même un sous-espace fermé. En dimension finie, tout sous-espace admet un supplémentaire orthogonal : E = V ⊕ V⊥, et tout vecteur se décompose de façon unique en une composante dans V et une composante dans V⊥. En dimension infinie, c'est le théorème de projection dans les espaces de Hilbert — qui repose sur la complétude de E et la fermeture de V — qui garantit cette décomposition. Dans les deux cas, x = p + e avec p ∈ V et e ∈ V⊥ est bien défini et unique.

**Cette décomposition donne le minimum.** Pour tout autre candidat v ∈ V :

‖x − v‖² = ‖(p − v) + e‖²

Le vecteur p − v est dans V, et e est orthogonal à V, donc ⟨p − v, e⟩ = 0. Par Pythagore :

‖x − v‖² = ‖p − v‖² + ‖e‖²

Ce terme est minimal quand ‖p − v‖² = 0, c'est-à-dire v = p. Le minimum est ‖e‖², atteint uniquement en p.

**Ce qu'on vient de montrer.** La projection orthogonale p est le meilleur estimateur de x dans V. L'erreur e = x − p est orthogonale à V — elle ne contient aucune composante dans la direction de V qu'on aurait pu exploiter pour réduire la distance. Pythagore garantit que composante utile (dans V) et erreur résiduelle (orthogonale à V) ne se mélangent pas : leurs contributions au carré de la norme s'additionnent indépendamment.

**Pourquoi le produit scalaire est nécessaire.** La preuve repose entièrement sur deux ingrédients : l'orthogonalité (pour définir e ⊥ V) et Pythagore (pour séparer les termes). Les deux viennent du produit scalaire. Sans lui, on ne peut ni décomposer x en composantes indépendantes, ni garantir que l'erreur est incompressible.

## La règle du parallélogramme

Pour tout x, y dans E :

‖x + y‖² + ‖x − y‖² = 2(‖x‖² + ‖y‖²)

**Preuve.** Par bilinéarité :
- ‖x + y‖² = ‖x‖² + 2⟨x,y⟩ + ‖y‖²
- ‖x − y‖² = ‖x‖² − 2⟨x,y⟩ + ‖y‖²

En sommant, les termes croisés s'annulent.

**Interprétation géométrique.** Dans un parallélogramme de côtés x et y, la somme des carrés des diagonales (‖x+y‖ et ‖x−y‖) égale la somme des carrés des quatre côtés. C'est une contrainte rigide sur la forme de la boule unité : elle interdit les boules trop plates ou trop pointues.

**Pourquoi c'est une caractérisation.** La règle du parallélogramme est non seulement nécessaire (on vient de la prouver) mais aussi suffisante : si une norme la vérifie, alors la formule de polarisation

⟨x,y⟩ = ¼(‖x + y‖² − ‖x − y‖²)

définit un produit scalaire dont la norme associée est la norme de départ. C'est le théorème de Jordan–von Neumann. Autrement dit : **une norme vient d'un produit scalaire si et seulement si elle vérifie la règle du parallélogramme.**

## Les normes Lᵖ et pourquoi seule L² a un produit scalaire

Les normes Lᵖ (pour 1 ≤ p ≤ ∞) sont définies sur des espaces de fonctions (ou de vecteurs en dimension finie) par :

‖f‖ₚ = (∫|f|ᵖ)^(1/p)

Chaque valeur de p donne une géométrie différente — c'est-à-dire une forme de boule unité différente.

**Seule L² vérifie la règle du parallélogramme.** Prenons f et g à supports disjoints (fg = 0 presque partout). Alors :

- ‖f + g‖ₚᵖ = ‖f‖ₚᵖ + ‖g‖ₚᵖ
- ‖f − g‖ₚᵖ = ‖f‖ₚᵖ + ‖g‖ₚᵖ

Donc ‖f + g‖ₚ = ‖f − g‖ₚ. La règle du parallélogramme exige alors :

2‖f + g‖² = 2(‖f‖² + ‖g‖²)

soit ‖f + g‖² = ‖f‖² + ‖g‖². Mais on sait aussi que ‖f + g‖ₚᵖ = ‖f‖ₚᵖ + ‖g‖ₚᵖ, c'est-à-dire que la puissance p "additionne" les normes. Pour que la puissance 2 les additionne aussi, il faut p = 2. Pour tout autre p, la règle du parallélogramme est violée, et aucun produit scalaire ne peut engendrer la norme Lᵖ.

**Lien avec la géométrie de la boule.** La note précédente (voir *Mesurer la proximité de points dans un espace*) montrait que le produit scalaire rend la boule unité quadratique — sa frontière est un niveau de ⟨x,x⟩ = 1. En dimension finie, c'est une ellipsoïde. La boule L² est la seule boule Lᵖ qui soit une ellipsoïde : pour p < 2, la boule est pincée (concave sur les diagonales) ; pour p > 2, elle est gonflée (convexe mais trop arrondie aux coins). Seule l'ellipsoïde a la courbure quadratique qui permet projection = plus proche point pour tout sous-espace.