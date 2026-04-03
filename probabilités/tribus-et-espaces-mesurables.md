# Probabilités

## I. Tribus et espaces mesurables

### 1. Le problème de la mesure

Le point de départ est une question simple : peut-on attribuer une « taille » à tous les sous-ensembles de ℝ ?

On connaît la longueur d'un intervalle : la longueur de [a, b] est b − a. On voudrait étendre cette notion à des ensembles plus compliqués — des unions d'intervalles, des ensembles de Cantor, etc. — sous forme d'une fonction m définie sur les parties de ℝ, à valeurs dans [0, +∞], qui respecte des propriétés raisonnables.

**Ce qu'on demande à m.** Au minimum :

- **Prolongement.** m([a, b]) = b − a pour tout intervalle.
- **Invariance par translation.** m(A + t) = m(A) pour tout t ∈ ℝ. (Déplacer un ensemble ne change pas sa taille.)
- **Additivité.** Si A et B sont disjoints, m(A ∪ B) = m(A) + m(B).

L'additivité finie (pour deux ensembles, ou pour un nombre fini d'ensembles) est naturelle mais insuffisante pour faire de l'analyse. On a besoin d'une propriété plus forte.

**σ-additivité (additivité dénombrable).** Si $(A_n)_{n \geq 1}$ est une suite d'ensembles **deux à deux disjoints**, alors :

$$m\Bigl(\bigcup_{n=1}^{\infty} A_n\Bigr) = \sum_{n=1}^{\infty} m(A_n)$$

Pourquoi cette propriété est-elle indispensable ? Parce qu'en analyse, on passe constamment à la limite : un ouvert est une union dénombrable d'intervalles, un fermé est un complementaire d'ouvert, un point est une intersection dénombrable d'intervalles emboîtés. Sans σ-additivité, la mesure ne se comporterait pas bien vis-à-vis de ces limites. En particulier :

- La σ-additivité entraîne la **continuité par en bas** : si $A_1 \subset A_2 \subset \cdots$, alors $m(\bigcup_n A_n) = \lim_n m(A_n)$. (Preuve : poser $B_1 = A_1$, $B_n = A_n \setminus A_{n-1}$, les $B_n$ sont disjoints, $\bigcup B_n = \bigcup A_n$, et $m(\bigcup A_n) = \sum m(B_n) = \lim_N \sum_{n=1}^N m(B_n) = \lim_N m(A_N)$.)
- Et la **continuité par en haut** : si $A_1 \supset A_2 \supset \cdots$ avec $m(A_1) < \infty$, alors $m(\bigcap_n A_n) = \lim_n m(A_n)$.

Sans σ-additivité, on pourrait avoir $A_n \downarrow \emptyset$ et pourtant $m(A_n)$ ne tendant pas vers 0. L'additivité finie seule ne l'interdit pas.

**Le théorème de Vitali : c'est impossible sur 𝒫(ℝ).** Vitali (1905) a montré qu'aucune fonction m définie sur *tous* les sous-ensembles de ℝ ne peut satisfaire simultanément le prolongement, l'invariance par translation et la σ-additivité.

*Construction.* On définit sur [0, 1) la relation x ~ y ⟺ x − y ∈ ℚ. C'est une relation d'équivalence (par exemple, 0.3 ~ 0.3, et 0.5 ~ 0.1 car 0.5 − 0.1 = 0.4 ∈ ℚ, etc.). Par l'axiome du choix, on sélectionne exactement un représentant par classe d'équivalence : soit V l'ensemble obtenu.

Pour chaque rationnel q ∈ ℚ ∩ [0, 1), on forme le translaté V + q (mod 1). Ces translatés sont :
- **deux à deux disjoints** : si x ∈ (V + q₁) ∩ (V + q₂), alors x − q₁ et x − q₂ sont tous deux dans V et dans la même classe (leur différence est q₁ − q₂ ∈ ℚ), donc q₁ = q₂ puisque V ne contient qu'un représentant par classe.
- **de réunion [0, 1)** : tout x ∈ [0, 1) est dans la même classe qu'un certain v ∈ V, donc x ∈ V + (x − v) mod 1.

Supposons V mesurable, de mesure m(V). Par invariance par translation, m(V + q) = m(V) pour tout q. Par σ-additivité :

$$1 = m\bigl([0,1)\bigr) = \sum_{q \in \mathbb{Q} \cap [0,1)} m(V) $$

Le membre de droite est une somme dénombrable d'un terme constant. Si m(V) = 0, la somme vaut 0 ≠ 1. Si m(V) > 0, la somme vaut +∞ ≠ 1. **Contradiction.**

**Conséquence.** On ne peut pas mesurer toutes les parties de ℝ. Il faut choisir une sous-famille de 𝒫(ℝ) — suffisamment riche pour contenir tous les ensembles qu'on utilise en pratique, mais pas trop grosse pour que la mesure reste cohérente. C'est le rôle de la **σ-algèbre**.

### 2. σ-algèbres : définition et premières propriétés

Soit Ω un ensemble quelconque. On note 𝒫(Ω) l'ensemble de toutes les parties de Ω.

**Définition.** Une **σ-algèbre** (ou **tribu**) sur Ω est une famille 𝒜 ⊂ 𝒫(Ω) qui vérifie :

1. Ω ∈ 𝒜 (l'ensemble « total » est mesurable)
2. Si A ∈ 𝒜, alors Aᶜ ∈ 𝒜 (stabilité par passage au complémentaire)
3. Si $(A_n)_{n \geq 1}$ est une suite d'éléments de 𝒜, alors $\bigcup_{n=1}^{\infty} A_n \in \mathcal{A}$ (stabilité par union dénombrable)

Le couple (Ω, 𝒜) s'appelle un **espace mesurable**. Les éléments de 𝒜 sont les ensembles qu'on s'autorise à mesurer — on les appelle les **ensembles mesurables**, ou en probabilités, les **événements**.

**Conséquences immédiates des axiomes.**

- ∅ ∈ 𝒜 (appliquer (2) à Ω : ∅ = Ωᶜ).
- Stabilité par **intersection dénombrable** : par les lois de De Morgan, $\bigcap_n A_n = \bigl(\bigcup_n A_n^c\bigr)^c$. Le complémentaire des $A_n$ est dans 𝒜 par (2), leur union par (3), le complémentaire de cette union par (2) à nouveau.
- Stabilité par **différence** : A \ B = A ∩ Bᶜ.
- Stabilité par union ou intersection **finies** (cas particulier du dénombrable, en complétant la suite par des ∅).

En résumé, une σ-algèbre est stable par toute opération ensembliste dénombrable.

**Exemples extrêmes.**
- La plus petite tribu sur Ω : {∅, Ω}. On l'appelle la tribu **grossière**. Elle ne distingue rien.
- La plus grande tribu sur Ω : 𝒫(Ω). On l'appelle la tribu **discrète**. Elle distingue tout.
- Toute σ-algèbre est comprise entre ces deux extrêmes : {∅, Ω} ⊂ 𝒜 ⊂ 𝒫(Ω).

**Exemple concret.** Ω = {1, 2, 3, 4} (un dé à 4 faces). On peut choisir la tribu 𝒜 = {∅, {1,2}, {3,4}, Ω}. Avec cette tribu, on peut distinguer « pair ou impair » (au sens 1,2 vs 3,4) mais pas les faces individuelles. Ajouter {1} à la tribu forcerait à y mettre aussi {1}ᶜ = {2,3,4}, puis {1} ∪ {3,4} = {1,3,4}, puis {1,3,4}ᶜ = {2}, etc. — la tribu s'enrichit par les axiomes.

**Pourquoi dénombrable et pas quelconque ?** La stabilité par union *dénombrable* (et non quelconque) est un compromis :
- Elle **suffit** pour faire de l'analyse : les passages à la limite en analyse font intervenir des suites (dénombrables). On peut former $\limsup_n A_n = \bigcap_{n} \bigcup_{k \geq n} A_k$ et $\liminf_n A_n = \bigcup_n \bigcap_{k \geq n} A_k$ — ce sont des opérations dénombrables.
- Exiger la stabilité par union **quelconque** serait trop fort : tout singleton {x} est dans la tribu borélienne (section 4), et si l'on pouvait prendre des unions quelconques, on obtiendrait n'importe quelle partie de ℝ — on retomberait sur 𝒫(ℝ), ce que Vitali interdit.

### 3. Tribu engendrée par une famille de parties

En pratique, on ne construit jamais une tribu en listant tous ses éléments (elle en a en général beaucoup trop — souvent autant que 𝒫(ℝ)). On part d'une famille « simple » d'ensembles et on laisse les axiomes faire le travail.

**Définition.** Soit ℰ ⊂ 𝒫(Ω) une famille quelconque de parties. La **tribu engendrée** par ℰ, notée σ(ℰ), est la plus petite σ-algèbre contenant ℰ :

$$\sigma(\mathcal{E}) = \bigcap \bigl\{ \mathcal{A} \subset \mathcal{P}(\Omega) : \mathcal{A} \text{ est une σ-algèbre et } \mathcal{E} \subset \mathcal{A} \bigr\}$$

Autrement dit, on prend l'intersection de toutes les σ-algèbres qui contiennent ℰ.

**Pourquoi ça marche.**
- L'intersection est bien définie car il existe au moins une σ-algèbre contenant ℰ, à savoir 𝒫(Ω).
- Une intersection quelconque (même non dénombrable) de σ-algèbres est encore une σ-algèbre. Vérification : si Ω est dans chaque 𝒜ᵢ, il est dans leur intersection ; si A est dans toutes les 𝒜ᵢ, Aᶜ l'est aussi ; si chaque $A_n$ est dans toutes les 𝒜ᵢ, leur union l'est aussi.
- Donc σ(ℰ) est une σ-algèbre, et c'est la plus petite par construction (elle est incluse dans toute σ-algèbre contenant ℰ).

**Ce que σ(ℰ) contient.** Intuitivement : tous les éléments de ℰ, leurs complémentaires, les unions dénombrables de tout cela, les complémentaires de ces unions, les unions de ces complémentaires, etc. — toutes les combinaisons dénombrables d'opérations ensemblistes appliquées aux éléments de ℰ. (La construction rigoureuse de cette hiérarchie est transfinite et n'est pas nécessaire en pratique.)

**Propriété utile.** Si ℰ₁ ⊂ ℰ₂, alors σ(ℰ₁) ⊂ σ(ℰ₂). Plus les générateurs sont nombreux, plus la tribu engendrée est riche. Réciproquement, si ℰ₁ ⊂ σ(ℰ₂) et ℰ₂ ⊂ σ(ℰ₁), alors σ(ℰ₁) = σ(ℰ₂) : deux familles qui s'engendrent mutuellement donnent la même tribu.

### 4. Tribu borélienne sur ℝ et sur ℝⁿ

C'est la tribu la plus importante en pratique. Elle capture « tout ce qu'on rencontre en analyse » sans tomber dans les pathologies de Vitali.

**Définition.** La **tribu borélienne** de ℝ, notée ℬ(ℝ), est la tribu engendrée par les ouverts de ℝ :

$$\mathcal{B}(\mathbb{R}) = \sigma\bigl(\{O \subset \mathbb{R} : O \text{ ouvert}\}\bigr)$$

**Ce qu'elle contient.** Les ouverts, les fermés (complémentaires d'ouverts), les intersections dénombrables d'ouverts (ensembles Gδ), les unions dénombrables de fermés (ensembles Fσ), et ainsi de suite en alternant. Les singletons {x} sont boréliens (comme intersections $\{x\} = \bigcap_n (x - 1/n, x + 1/n)$). Les intervalles de toute forme sont boréliens. Tous les ensembles qu'on manipule en analyse courante sont boréliens. (Construire un ensemble non borélien requiert l'axiome du choix, comme dans Vitali.)

**Générateurs équivalents.** Les familles suivantes engendrent toutes ℬ(ℝ) :

| Famille de générateurs | Pourquoi elle suffit |
|---|---|
| Ouverts de ℝ | Définition |
| Intervalles ouverts (a, b) | Tout ouvert de ℝ est union dénombrable d'intervalles ouverts (car ℚ est dense dans ℝ : pour chaque point d'un ouvert, on trouve un intervalle à bornes rationnelles contenu dans l'ouvert) |
| Demi-droites (−∞, t], t ∈ ℝ | (a, b) = ⋃ₙ ( (−∞, b − 1/n] \ (−∞, a] ), et réciproquement (−∞, t] = ⋂ₙ (−∞, t + 1/n) |
| Demi-droites (−∞, t), t ∈ ℝ | (−∞, t] = ⋂ₙ (−∞, t + 1/n), et (−∞, t) = ⋃ₙ (−∞, t − 1/n] |

La dernière ligne est importante en probabilités : dire qu'une variable aléatoire X est mesurable, c'est exiger que {X < t} soit un événement pour tout t — ce qui est équivalent à exiger {X ≤ t} un événement pour tout t, puisque les deux familles engendrent la même tribu.

**Sur ℝⁿ.** La tribu borélienne ℬ(ℝⁿ) est engendrée par les ouverts de ℝⁿ. On peut aussi l'engendrer par les « pavés » $A_1 \times \cdots \times A_n$ où chaque $A_i \in \mathcal{B}(\mathbb{R})$ — on parle de **tribu produit** :

$$\mathcal{B}(\mathbb{R}^n) = \mathcal{B}(\mathbb{R}) \otimes \cdots \otimes \mathcal{B}(\mathbb{R})$$

Autrement dit, la tribu borélienne du produit est le produit des tribus boréliennes. (C'est un fait non trivial, qui repose sur le fait que ℝⁿ a une base dénombrable d'ouverts. Pour des espaces topologiques plus exotiques, l'égalité peut être fausse.)

### 5. Tribu engendrée par une application

C'est la notion clé pour les probabilités : elle formalise l'idée d'**information**.

**Définition.** Soit f : Ω → (E, ℰ) une application, où (E, ℰ) est un espace mesurable. La **tribu engendrée par f** est :

$$\sigma(f) = \{ f^{-1}(B) : B \in \mathcal{E} \} = f^{-1}(\mathcal{E})$$

Autrement dit, on « tire en arrière » par f tous les ensembles mesurables de E. Pour chaque ensemble mesurable B dans l'espace d'arrivée, on forme la préimage f⁻¹(B) = {ω ∈ Ω : f(ω) ∈ B} dans l'espace de départ.

**Vérification que c'est une tribu.** f⁻¹(E) = Ω ✓. f⁻¹(B)ᶜ = f⁻¹(Bᶜ) ✓. f⁻¹(⋃ Bₙ) = ⋃ f⁻¹(Bₙ) ✓. (Les préimages commutent avec toutes les opérations ensemblistes.)

**Interprétation.** σ(f) est la plus petite σ-algèbre sur Ω qui rend f mesurable. Elle représente exactement **l'information que l'on obtient en observant f** : un sous-ensemble A de Ω appartient à σ(f) si et seulement si, connaissant la valeur de f(ω), on peut déterminer sans ambiguïté si ω ∈ A ou non.

*Exemple.* Ω = {1,2,3,4,5,6} (un dé), f(ω) = ω mod 2 (pair ou impair). Alors σ(f) = {∅, {1,3,5}, {2,4,6}, Ω}. Observer f sépare pair/impair, mais pas les faces individuelles. L'événement {1,2} ∉ σ(f) : il n'est pas déterminable à partir de la parité seule.

**Lemme de factorisation (Doob).** Soit g : Ω → ℝ. Alors g est σ(f)-mesurable si et seulement s'il existe une fonction mesurable φ : E → ℝ telle que g = φ ∘ f.

En langue courante : **g est mesurable par rapport à σ(f) exactement quand g est une fonction de f.** C'est intuitif — si l'information disponible est celle de f, les seules quantités qu'on peut calculer sont celles qui ne dépendent que de f.

Ce lemme est fondamental pour la suite : il donne un sens précis à l'expression « g ne dépend que de f », et c'est lui qui, en probabilités, fait le lien entre σ-algèbres et conditionnement.

**Tribu engendrée par une famille d'applications.** Si $(f_i)_{i \in I}$ est une famille d'applications $f_i : \Omega \to (E_i, \mathcal{E}_i)$, on pose :

$$\sigma\bigl((f_i)_{i \in I}\bigr) = \sigma\Bigl(\bigcup_{i \in I} f_i^{-1}(\mathcal{E}_i)\Bigr)$$

C'est la plus petite tribu rendant toutes les $f_i$ mesurables simultanément. Elle encode l'information conjointe de toutes les $f_i$ : un événement A ∈ σ((fᵢ)) est un événement qu'on peut déterminer en observant les valeurs de toutes les $f_i$.
