# Probabilités

## I. Tribus et espaces mesurables

**Vue d'ensemble.** Ce chapitre construit la notion de tribu en six étapes.

1. La σ-additivité est une propriété essentielle d'une mesure, indispensable pour garantir les raisonnements de passage à la limite. L'exemple des parties finies ou cofinies montre que sans σ-additivité, on peut avoir des comportements pathologiques à la limite.
2. Le théorème de Vitali montre qu'on ne peut pas définir sur $\mathcal P(\mathbb R)$ une mesure satisfaisant simultanément le prolongement de la longueur, l'invariance par translation et la σ-additivité. Il illustre qu'une mesure, pour respecter les contraintes qu'on lui impose, peut devoir restreindre les parties qu'elle se propose de mesurer. C'est le rôle des tribus.
3. Les exemples des mesures de Dirac et de comptage montrent que ce n'est pas l'ensemble sous-jacent ($\mathbb R$) qui force à restreindre à une tribu, mais les propriétés qu'on exige de la mesure. Ces deux mesures portent sur $\mathbb R$ et restent cohérentes sur $\mathcal P(\mathbb R)$ entier.
4. La notion de tribu étant motivée, on peut définir formellement un espace mesurable comme un couple $(\Omega, \mathcal A)$ où $\mathcal A$ est une tribu sur $\Omega$. Une mesure sur cet espace est une application $m : \mathcal A \to [0,+\infty]$ telle que $m(\emptyset)=0$ et $m$ soit σ-additive ; le triplet $(\Omega, \mathcal A, m)$ est alors un espace mesuré.
5. En pratique, on construit une tribu à partir d'une famille génératrice. L'exemple principal est la tribu borélienne, engendrée par les ouverts de $\mathbb R$ (ou, de façon équivalente, par les intervalles ouverts, les demi-droites fermées ou ouvertes, etc.). Sur $\mathbb R^n$, la tribu borélienne coïncide avec la tribu produit $\mathcal B(\mathbb R)^{\otimes n}$.
6. Une tribu peut aussi être définie par une application $f : \Omega \to (E, \mathcal E)$ en tirant en arrière les parties mesurables de $E$ par $f^{-1}$. Cette construction mène au lemme de factorisation de Doob : $g$ est $\sigma(f)$-mesurable si et seulement si $g$ se factorise à travers $f$, c'est-à-dire $g = \varphi \circ f$ pour une certaine fonction mesurable $\varphi$.

### 1. Le problème de la mesure

#### Cadre du problème

Le point de départ est une question simple : peut-on attribuer une « mesure » à tous les sous-ensembles de ℝ ?

On connaît la longueur d'un intervalle : la longueur de [a, b] est b − a. On voudrait étendre cette notion à des ensembles plus compliqués de ℝ — des unions d'intervalles, des ensembles de Cantor (ensembles fermés, très découpés, non dénombrables, mais de longueur nulle), etc. — sous forme d'une fonction m définie sur les parties de ℝ, à valeurs dans [0, +∞], qui respecte des propriétés raisonnables.

La question qu'on se pose est donc une **question géométrique sur ℝ.** Peut-on définir sur les parties de ℝ une notion de mesure qui prolonge la longueur usuelle des intervalles ?

La **question générale** sous-jacente est : sur un ensemble quelconque Ω, peut-on définir une mesure sur une famille convenable de parties de Ω ?

Sur ℝ, la question est géométrique car on souhaite que la mesure respecte des exigences liées à la géométrie de ℝ. Ce qu'on demande à m, **au minimum** :

- **Additivité.** Si A et B sont disjoints, m(A ∪ B) = m(A) + m(B).
- **Prolongement.** m([a, b]) = b − a pour tout intervalle.
- **Invariance par translation.** m(A + t) = m(A) pour tout t ∈ ℝ. (Déplacer un ensemble ne change pas sa taille.)

L'idée d'additivité, puis de σ-additivité, appartient à la notion abstraite de mesure.
Les deux dernières exigences en revanche sont spécifiques au problème géométrique d'une mesure sur ℝ : on veut que la mesure construite reflète la longueur usuelle.

#### Nécessité de la σ-additivité

L'additivité finie (pour deux ensembles, ou pour un nombre fini d'ensembles) est naturelle mais insuffisante pour faire de l'analyse. On a besoin d'une propriété plus forte.

**σ-additivité (additivité dénombrable).** Si $(A_n)_{n \geq 1}$ est une suite d'ensembles **deux à deux disjoints**, alors :

$$m\Bigl(\bigcup_{n=1}^{\infty} A_n\Bigr) = \sum_{n=1}^{\infty} m(A_n)$$

**Pourquoi cette propriété est-elle indispensable ?** En analyse et en probabilité, on passe constamment à la limite sur des suites d'ensembles. Voici quatre situations typiques, qui toutes reposent sur des opérations dénombrables.

- _1. Limite inférieure d'ensembles._ L'expression

$$\bigcup_{N=1}^{\infty}\bigcap_{n\ge N} A_n$$

signifie « l'ensemble des $\omega$ tels qu'il existe un rang $N$ à partir duquel, pour tout $n \geq N$, on a $\omega \in A_n$ ».

- _2. Limite supérieure d'ensembles._ L'expression

$$\bigcap_{N=1}^{\infty}\bigcup_{n\ge N} A_n$$

signifie « l'ensemble des $\omega$ tels que $\omega \in A_n$ pour une infinité de valeurs de $n$ ».

Ces deux expressions réapparaîtront plus loin, par exemple dans l'étude des convergences et des lemmes de Borel-Cantelli.

- _3. Continuité par en bas_ (suite croissante). On approche un ensemble par morceaux de plus en plus grands. Si

$$A_1 \subset A_2 \subset \cdots \quad \text{et} \quad A = \bigcup_{n=1}^{\infty} A_n,$$

alors on s'attend à ce que la mesure de $A$ soit la limite des mesures des approximations $A_n$ :

$$m(A) = m\Bigl(\bigcup_n A_n\Bigr) = \lim_n m(A_n).$$

C'est exactement ce que garantit la σ-additivité. Intuitivement, les « nouvelles parties » que l'on ajoute à chaque étape sont disjointes, donc leurs mesures s'additionnent bien.

- _4. Continuité par en haut_ (suite décroissante). On approche un ensemble par des ensembles de plus en plus petits. Si

$$A_1 \supset A_2 \supset \cdots \quad \text{et} \quad A = \bigcap_{n=1}^{\infty} A_n,$$

alors on s'attend à ce que $m(A_n)$ tende vers $m(A)$. C'est encore vrai, à condition que $m(A_1) < \infty$ :

$$m(A) = m\Bigl(\bigcap_n A_n\Bigr) = \lim_n m(A_n).$$

L'hypothèse $m(A_1)<\infty$ évite les soustractions indéterminées du type $+\infty-+\infty$.

Sans σ-additivité, la mesure ne se comporterait pas bien vis-à-vis de ces quatre types de limites. En particulier, on pourrait avoir $A_n \downarrow \emptyset$ et pourtant $m(A_n)$ ne tendant pas vers 0 (voir l'exemple plus bas).

*Exemple.* Sur l'algèbre des parties **finies ou cofinies** de $\mathbb{N}$, définissons

$$
m(A)=
\begin{cases}
0 & \text{si } A \text{ est fini},\\
1 & \text{si } A^c \text{ est fini.}
\end{cases}
$$

Cette fonction est additive finie. Pourtant, elle ne vérifie pas la propriété souhaitable de **continuité par en haut** : pour $A_n = \{n,n+1,n+2,\dots\}$, la suite est décroissante et $\bigcap_n A_n = \emptyset$ (tout entier fixé $k$ sort de $A_n$ dès que $n > k$), donc $A_n \downarrow \emptyset$. Pourtant $m(A_n)=1$ pour tout $n$, tandis que $m(\emptyset)=0$ : la mesure ne suit pas la limite.

#### Le théorème de Vitali

**Le théorème de Vitali.** Vitali (1905) a montré qu'aucune fonction $m$ définie sur *tous* les sous-ensembles de ℝ ne peut satisfaire simultanément le prolongement, l'invariance par translation et la σ-additivité.

L'idée de la construction est la suivante.

On définit sur $[0,1)$ la relation $x \sim y \iff x-y \in \mathbb Q$. C'est une relation d'équivalence. Par l'axiome du choix, on sélectionne exactement un représentant dans chaque classe d'équivalence : soit $V$ l'ensemble obtenu.

Pour chaque rationnel $q \in \mathbb Q \cap [0,1)$, on forme le translaté $V+q$ (mod 1). Ces translatés sont :

- **deux à deux disjoints** ;
- **de réunion $[0,1)$**.

Supposons $V$ mesurable, de mesure $m(V)$. Par invariance par translation, tous les ensembles $V+q$ ont même mesure. Par σ-additivité,

$$1 = m\bigl([0,1)\bigr) = \sum_{q \in \mathbb{Q} \cap [0,1)} m(V).$$

Le membre de droite est une somme dénombrable d'un terme constant. Si $m(V)=0$, la somme vaut 0 ; si $m(V)>0$, la somme vaut $+\infty$. Dans les deux cas, on obtient une contradiction.

#### Conséquence

On ne peut donc pas mesurer toutes les parties de ℝ avec une notion de longueur satisfaisant ces propriétés. Il faut choisir une sous-famille de $\mathcal P(\mathbb R)$ — suffisamment riche pour contenir tous les ensembles qu'on utilise en pratique, mais pas trop grosse pour que la mesure géométrique reste cohérente. C'est précisément le rôle de la **σ-algèbre**.

*Remarque culturelle.* En dimension 3, le paradoxe de Banach-Tarski affirme, très schématiquement, qu'on peut découper une boule en un nombre fini de morceaux très pathologiques puis, en les déplaçant seulement par rotations et translations, reconstituer deux boules identiques à la première. Le point décisif est que, si ces morceaux avaient tous un volume géométrique bien défini, invariant par déplacement et additif, on obtiendrait qu'une boule a le même volume que deux copies d'elle-même, ce qui est absurde. Le paradoxe ne contredit donc pas le volume usuel ; il montre qu'on ne peut pas attribuer un volume raisonnable à toutes les parties de l'espace. Comme pour Vitali, il motive la nécessité de restreindre la mesure à une famille convenable d'ensembles.

#### Des mesures existent tout de même sur $\mathcal P(\mathbb R)$

Le théorème de Vitali ne dit donc pas qu'aucune mesure n'existe sur $\mathcal P(\mathbb R)$. Il dit seulement qu'on ne peut pas y définir une mesure satisfaisant simultanément les exigences géométriques imposées plus haut. Autrement dit, la difficulté dépend des propriétés qu'on exige de la mesure.

Au sens de mesure qui sera formalisé à la section suivante, il existe bien des mesures sur $\mathcal P(\mathbb R)$. Deux exemples importants sont les suivants.

- **Mesure de Dirac en $x_0$**, notée $\delta_{x_0}$ :

$$
\delta_{x_0}(A)=
\begin{cases}
1 & \text{si } x_0 \in A,\\
0 & \text{si } x_0 \notin A.
\end{cases}
$$

Elle est bien définie sur toute $\mathcal P(\mathbb R)$. Intuitivement, elle ne mesure pas la longueur d'un ensemble : elle regarde seulement si $x_0$ appartient ou non à cet ensemble. C'est pourquoi $\delta_{x_0}([0,2])$ vaut 0 ou 1, alors que la longueur de $[0,2]$ vaut 2.

- **Mesure de comptage** :

$$
\#(A)=
\begin{cases}
|A| & \text{si } A \text{ est fini},\\
+\infty & \text{si } A \text{ est infini.}
\end{cases}
$$

Elle aussi est définie sur toute $\mathcal P(\mathbb R)$. Elle ne mesure pas la longueur mais le nombre de points : un intervalle comme $[0,1]$ a alors mesure $+\infty$. Elle est même invariante par translation, ce qui montre bien que ce n'est pas cette propriété seule qui pose problème.

Ces exemples mettent donc en évidence le point essentiel : **la sous-famille de $\mathcal P(\mathbb R)$ sur laquelle une mesure peut être définie dépend des exigences qu'on lui impose**.

### 2. σ-algèbres : définition et premières propriétés

#### Définition

Soit Ω un ensemble quelconque. On note 𝒫(Ω) l'ensemble de toutes les parties de Ω.

**Définition.** Une **σ-algèbre** (ou **tribu**) sur Ω est une famille 𝒜 ⊂ 𝒫(Ω) qui vérifie :

1. Ω ∈ 𝒜 (l'ensemble « total » est mesurable)
2. Si A ∈ 𝒜, alors Aᶜ ∈ 𝒜 (stabilité par passage au complémentaire)
3. Si $(A_n)_{n \geq 1}$ est une suite d'éléments de 𝒜, alors $\bigcup_{n=1}^{\infty} A_n \in \mathcal{A}$ (stabilité par union dénombrable)

Le couple (Ω, 𝒜) s'appelle un **espace mesurable**. Les éléments de 𝒜 sont les ensembles sur lesquels une mesure pourra être définie — on les appelle les **ensembles mesurables**, ou en probabilités, les **événements**.

Attention au vocabulaire : « mesurable » ici veut dire **mesurable relativement à la tribu 𝒜**. Cela ne veut pas encore dire qu'une mesure m est déjà définie sur 𝒜, ni, a fortiori, qu'elle possède des propriétés géométriques particulières comme le prolongement de la longueur sur ℝ ou l'invariance par translation.

#### Mesure et espace mesuré

Une **mesure** sur un espace mesurable $(\Omega, \mathcal A)$ est une application

$$m : \mathcal A \to [0,+\infty]$$

telle que $m(\emptyset)=0$ et telle que $m$ soit σ-additive. Le triplet $(\Omega, \mathcal A, m)$ s'appelle alors un **espace mesuré**.

#### Conséquences immédiates

- ∅ ∈ 𝒜 (appliquer (2) à Ω : ∅ = Ωᶜ).
- Stabilité par **intersection dénombrable** : par les lois de De Morgan, $\bigcap_n A_n = \bigl(\bigcup_n A_n^c\bigr)^c$. Le complémentaire des $A_n$ est dans 𝒜 par (2), leur union par (3), le complémentaire de cette union par (2) à nouveau.
- Stabilité par **différence** : A \ B = A ∩ Bᶜ.
- Stabilité par union ou intersection **finies** (cas particulier du dénombrable, en complétant la suite par des ∅).

En résumé, une σ-algèbre est stable par toute opération ensembliste dénombrable.

#### Exemples

**Exemples extrêmes.**
- La plus petite tribu sur Ω : {∅, Ω}. On l'appelle la tribu **grossière**. Elle ne distingue rien.
- La plus grande tribu sur Ω : 𝒫(Ω). On l'appelle la tribu **discrète**. Elle distingue tout. En particulier, 𝒫(Ω) est toujours une σ-algèbre, quel que soit Ω.
- Toute σ-algèbre est comprise entre ces deux extrêmes : {∅, Ω} ⊂ 𝒜 ⊂ 𝒫(Ω).

Remarque: il n'y a pas de contradiction avec Vitali : lorsque Ω = ℝ, 𝒫(ℝ) est bien une σ-algèbre. On peut même définir sur 𝒫(ℝ) certaines mesures, comme les mesures de Dirac ou la mesure de comptage. Ce que Vitali montre, c'est qu'on ne peut pas y définir une mesure qui prolonge la longueur, soit invariante par translation et soit σ-additive.

**Exemple concret.** Ω = {1, 2, 3, 4} (un dé à 4 faces). On peut choisir la tribu 𝒜 = {∅, {1,2}, {3,4}, Ω}. Avec cette tribu, on peut distinguer « pair ou impair » (au sens 1,2 vs 3,4) mais pas les faces individuelles. Ajouter {1} à la tribu forcerait à y mettre aussi {1}ᶜ = {2,3,4}, puis {1} ∪ {3,4} = {1,3,4}, puis {1,3,4}ᶜ = {2}, etc. — la tribu s'enrichit par les axiomes.

#### Pourquoi dénombrable

**Pourquoi dénombrable et pas fini, ni quelconque ?** La question *pourquoi pas fini* a déjà été traitée : l'additivité finie est insuffisante pour contrôler les passages à la limite, comme le montre l'exemple de l'algèbre des parties finies ou cofinies. Il reste la question *pourquoi pas quelconque*.

Le dénombrable est le régime naturel de l'analyse : tous les raisonnements de passage à la limite — convergence monotone, limsup, liminf, Borel-Cantelli — reposent sur des opérations dénombrables (suites, séries). La stabilité par union dénombrable est donc suffisante pour garantir ces raisonnements, et exiger davantage serait sans contrepartie utile.

*Illustration sur $\mathbb R$.* On peut voir concrètement que la stabilité par union quelconque serait trop forte : tout singleton $\{x\}$ est dans la tribu borélienne (section 4), et avec des unions quelconques on pourrait former $\bigcup_{x \in A}\{x\} = A$ pour n'importe quel $A \subset \mathbb{R}$ — on retomberait sur $\mathcal{P}(\mathbb{R})$ entier, et l'on perdrait tout contrôle géométrique.

### 3. Tribu engendrée par une famille de parties

#### Idée générale

En pratique, on ne construit jamais une tribu en listant tous ses éléments (elle en a en général beaucoup trop — souvent autant que 𝒫(ℝ)). On part d'une famille « simple » d'ensembles et on laisse les axiomes faire le travail.

#### Définition

**Définition.** Soit ℰ ⊂ 𝒫(Ω) une famille quelconque de parties. La **tribu engendrée** par ℰ, notée σ(ℰ), est la plus petite σ-algèbre contenant ℰ :

$$\sigma(\mathcal{E}) = \bigcap \bigl\{ \mathcal{A} \subset \mathcal{P}(\Omega) : \mathcal{A} \text{ est une σ-algèbre et } \mathcal{E} \subset \mathcal{A} \bigr\}$$

Autrement dit, on prend l'intersection de toutes les σ-algèbres qui contiennent ℰ.

#### Pourquoi cela marche

**Pourquoi ça marche.**
- L'intersection est bien définie car il existe au moins une σ-algèbre contenant ℰ, à savoir 𝒫(Ω).
- Une intersection quelconque (même non dénombrable) de σ-algèbres est encore une σ-algèbre. Vérification : si Ω est dans chaque 𝒜ᵢ, il est dans leur intersection ; si A est dans toutes les 𝒜ᵢ, Aᶜ l'est aussi ; si chaque $A_n$ est dans toutes les 𝒜ᵢ, leur union l'est aussi.
- Donc σ(ℰ) est une σ-algèbre, et c'est la plus petite par construction (elle est incluse dans toute σ-algèbre contenant ℰ).

#### Intuition

**Ce que σ(ℰ) contient.** Intuitivement : tous les éléments de ℰ, leurs complémentaires, les unions dénombrables de tout cela, les complémentaires de ces unions, les unions de ces complémentaires, etc. — toutes les combinaisons dénombrables d'opérations ensemblistes appliquées aux éléments de ℰ. (La construction rigoureuse de cette hiérarchie est transfinite et n'est pas nécessaire en pratique.)

#### Propriété utile

**Propriété utile.** Si ℰ₁ ⊂ ℰ₂, alors σ(ℰ₁) ⊂ σ(ℰ₂). Plus les générateurs sont nombreux, plus la tribu engendrée est riche. Réciproquement, si ℰ₁ ⊂ σ(ℰ₂) et ℰ₂ ⊂ σ(ℰ₁), alors σ(ℰ₁) = σ(ℰ₂) : deux familles qui s'engendrent mutuellement donnent la même tribu.

### 4. Tribu borélienne sur ℝ et sur ℝⁿ

#### Définition

C'est la tribu la plus importante en pratique. Elle capture « tout ce qu'on rencontre en analyse » sans tomber dans les pathologies de Vitali.

**Définition.** La **tribu borélienne** de ℝ, notée ℬ(ℝ), est la tribu engendrée par les ouverts de ℝ :

$$\mathcal{B}(\mathbb{R}) = \sigma\bigl(\{O \subset \mathbb{R} : O \text{ ouvert}\}\bigr)$$

#### Contenu

**Ce qu'elle contient.** Les ouverts, les fermés (complémentaires d'ouverts), les intersections dénombrables d'ouverts (ensembles Gδ), les unions dénombrables de fermés (ensembles Fσ), et ainsi de suite en alternant. Les singletons {x} sont boréliens (comme intersections $\{x\} = \bigcap_n (x - 1/n, x + 1/n)$). Les intervalles de toute forme sont boréliens. Tous les ensembles qu'on manipule en analyse courante sont boréliens. (Construire un ensemble non borélien requiert l'axiome du choix, comme dans Vitali.)

#### Générateurs équivalents

**Générateurs équivalents.** Les familles suivantes engendrent toutes ℬ(ℝ) :

| Famille de générateurs | Pourquoi elle suffit |
|---|---|
| Ouverts de ℝ | Définition |
| Intervalles ouverts (a, b) | Tout ouvert de ℝ est union dénombrable d'intervalles ouverts (car ℚ est dense dans ℝ : pour chaque point d'un ouvert, on trouve un intervalle à bornes rationnelles contenu dans l'ouvert) |
| Demi-droites (−∞, t], t ∈ ℝ | (a, b) = ⋃ₙ ( (−∞, b − 1/n] \ (−∞, a] ), et réciproquement (−∞, t] = ⋂ₙ (−∞, t + 1/n) |
| Demi-droites (−∞, t), t ∈ ℝ | (−∞, t] = ⋂ₙ (−∞, t + 1/n), et (−∞, t) = ⋃ₙ (−∞, t − 1/n] |

#### Cas de $\mathbb{R}^n$

**Sur ℝⁿ.** La tribu borélienne ℬ(ℝⁿ) est engendrée par les ouverts de ℝⁿ. On peut aussi l'engendrer par les « pavés » $A_1 \times \cdots \times A_n$ où chaque $A_i \in \mathcal{B}(\mathbb{R})$ — on parle de **tribu produit** :

$$\mathcal{B}(\mathbb{R}^n) = \mathcal{B}(\mathbb{R}) \otimes \cdots \otimes \mathcal{B}(\mathbb{R})$$

Autrement dit, la tribu borélienne du produit est le produit des tribus boréliennes. (C'est un fait non trivial, qui repose sur le fait que ℝⁿ a une base dénombrable d'ouverts. Pour des espaces topologiques plus exotiques, l'égalité peut être fausse.)

### 5. Tribu engendrée par une application

#### Idée

C'est la notion clé pour les probabilités : elle formalise l'idée d'**information**.

#### Définition

**Définition.** Soient $(\Omega, \mathcal{A})$ et $(E, \mathcal{E})$ deux espaces mesurables. Une application $f : \Omega \to E$ est dite **mesurable** (ou $\mathcal{A}/\mathcal{E}$-mesurable) si

$$\forall B \in \mathcal{E},\quad f^{-1}(B) \in \mathcal{A}.$$

Autrement dit, la préimage de tout ensemble mesurable de l'espace d'arrivée est un ensemble mesurable de l'espace de départ.

**Définition.** Soit f : Ω → (E, ℰ) une application, où (E, ℰ) est un espace mesurable. La **tribu engendrée par f** est :

$$\sigma(f) = \{ f^{-1}(B) : B \in \mathcal{E} \} = f^{-1}(\mathcal{E})$$

Autrement dit, on « tire en arrière » par f tous les ensembles mesurables de E. Pour chaque ensemble mesurable B dans l'espace d'arrivée, on forme la préimage f⁻¹(B) = {ω ∈ Ω : f(ω) ∈ B} dans l'espace de départ.

#### Vérification

**Vérification que c'est une tribu.** f⁻¹(E) = Ω ✓. f⁻¹(B)ᶜ = f⁻¹(Bᶜ) ✓. f⁻¹(⋃ Bₙ) = ⋃ f⁻¹(Bₙ) ✓. (Les préimages commutent avec toutes les opérations ensemblistes.)

#### Interprétation

**Interprétation.** σ(f) est la plus petite σ-algèbre sur Ω qui rend f mesurable. Elle représente exactement **l'information que l'on obtient en observant f** : un sous-ensemble A de Ω appartient à σ(f) si et seulement si, connaissant la valeur de f(ω), on peut déterminer sans ambiguïté si ω ∈ A ou non.

#### Exemple

*Exemple.* Ω = {1,2,3,4,5,6} (un dé), f(ω) = ω mod 2 (pair ou impair). Alors σ(f) = {∅, {1,3,5}, {2,4,6}, Ω}. Observer f sépare pair/impair, mais pas les faces individuelles. L'événement {1,2} ∉ σ(f) : il n'est pas déterminable à partir de la parité seule.

#### Lemme de factorisation

**Lemme de factorisation (Doob).** Soit g : Ω → ℝ. Alors g est σ(f)-mesurable si et seulement s'il existe une fonction mesurable φ : E → ℝ telle que g = φ ∘ f.

En langue courante : **g est mesurable par rapport à σ(f) exactement quand g se factorise à travers f**, c'est-à-dire quand il existe $\varphi$ telle que $g(\omega) = \varphi(f(\omega))$ pour tout $\omega$. L'expression usuelle « $g$ est une fonction de $f$ » est un raccourci pour cette propriété : elle signifie que la valeur de $g$ en $\omega$ ne dépend de $\omega$ qu'à travers la valeur de $f(\omega)$. C'est intuitif — si l'information disponible est celle de f, les seules quantités qu'on peut calculer sont celles qui ne dépendent que de f.

Ce lemme est fondamental pour la suite : il donne un sens précis à l'expression « g ne dépend que de f », et c'est lui qui, en probabilités, fait le lien entre σ-algèbres et conditionnement.

#### Famille d'applications

**Tribu engendrée par une famille d'applications.** Si $(f_i)_{i \in I}$ est une famille d'applications $f_i : \Omega \to (E_i, \mathcal{E}_i)$, on pose :

$$\sigma\bigl((f_i)_{i \in I}\bigr) = \sigma\Bigl(\bigcup_{i \in I} f_i^{-1}(\mathcal{E}_i)\Bigr)$$

C'est la plus petite tribu rendant toutes les $f_i$ mesurables simultanément. Elle encode l'information conjointe de toutes les $f_i$ : un événement A ∈ σ((fᵢ)) est un événement qu'on peut déterminer en observant les valeurs de toutes les $f_i$.
