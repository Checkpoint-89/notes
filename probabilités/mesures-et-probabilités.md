# Probabilités

## II. Mesures et probabilités

**Vue d'ensemble.** Ce chapitre formalise la notion de mesure, esquissée au chapitre I, en cinq étapes.

1. On définit rigoureusement ce qu'est une mesure positive sur un espace mesurable $(\Omega, \mathcal A)$ : une application $m : \mathcal A \to [0,+\infty]$ vérifiant $m(\emptyset) = 0$ et la σ-additivité. On en déduit les propriétés de base — monotonie, σ-sous-additivité, continuité monotone — qui sont les outils de travail quotidiens du calcul des mesures.
2. La mesure de Lebesgue sur $\mathbb R$ est l'exemple central : c'est la mesure qui prolonge la longueur des intervalles à toute la tribu borélienne $\mathcal B(\mathbb R)$, tout en restant σ-additive et invariante par translation. Le théorème de Carathéodory garantit l'existence et l'unicité d'un tel prolongement. On en profite pour distinguer la tribu de Lebesgue de la tribu borélienne et pour introduire les ensembles de mesure nulle.
3. Une probabilité est simplement une mesure de masse totale 1. Les axiomes de Kolmogorov ne sont rien d'autre que la σ-additivité appliquée à ce cadre. On retrouve les règles de calcul classiques — complémentaire, union, inclusion-exclusion — comme conséquences immédiates des propriétés générales des mesures. On introduit la probabilité conditionnelle et la formule de Bayes.
4. Étant donné deux mesures $\mu$ et $\nu$ sur le même espace, on peut se demander si $\mu$ est « exprimable » en fonction de $\nu$. La continuité absolue ($\mu \ll \nu$) et le théorème de Radon-Nikodym formalisent cette idée : sous des hypothèses raisonnables, $\mu$ s'écrit comme l'intégrale d'une densité par rapport à $\nu$.
5. Pour travailler sur des espaces produits $\Omega_1 \times \Omega_2$, on construit la mesure produit, qui permet de mesurer des « pavés » $A_1 \times A_2$ par le produit $m_1(A_1) \cdot m_2(A_2)$. Le théorème de Fubini-Tonelli permet alors de calculer les intégrales sur un espace produit par itération.

### 1. Mesures positives : définition et propriétés

#### Définition

Le chapitre I a introduit la notion d'espace mesurable $(\Omega, \mathcal A)$ et motivé la σ-additivité. On peut maintenant formaliser.

**Définition.** Soit $(\Omega, \mathcal A)$ un espace mesurable. Une **mesure positive** (ou simplement **mesure**) sur $(\Omega, \mathcal A)$ est une application

$$m : \mathcal A \to [0, +\infty]$$

vérifiant :

1. $m(\emptyset) = 0$
2. **σ-additivité.** Pour toute suite $(A_n)_{n \geq 1}$ d'éléments de $\mathcal A$ **deux à deux disjoints**,

$$m\Bigl(\bigcup_{n=1}^{\infty} A_n\Bigr) = \sum_{n=1}^{\infty} m(A_n).$$

Le triplet $(\Omega, \mathcal A, m)$ s'appelle un **espace mesuré**.

*Remarque.* La σ-additivité entraîne l'additivité finie (poser $A_n = \emptyset$ pour $n$ assez grand). La réciproque est fausse, comme on l'a vu au chapitre I avec l'exemple des parties finies ou cofinies de $\mathbb N$.

#### Vocabulaire

- $m$ est **finie** si $m(\Omega) < \infty$.
- $m$ est **σ-finie** s'il existe une suite $(E_n)$ d'éléments de $\mathcal A$ telle que $\Omega = \bigcup_n E_n$ et $m(E_n) < \infty$ pour tout $n$. Autrement dit, on peut découper $\Omega$ en morceaux de mesure finie. C'est une hypothèse technique fréquente, vérifiée dans la plupart des situations concrètes.

*Exemples.* La mesure de Lebesgue sur $(\mathbb R, \mathcal B(\mathbb R))$ est σ-finie (prendre $E_n = [-n, n]$) mais pas finie. Toute probabilité est finie (donc σ-finie). La mesure de comptage sur $(\mathbb R, \mathcal P(\mathbb R))$ n'est pas σ-finie : tout ensemble de mesure finie est fini, et $\mathbb R$ n'est pas union dénombrable d'ensembles finis.

#### Propriétés fondamentales

Les propriétés suivantes découlent directement de la définition. Soit $m$ une mesure sur $(\Omega, \mathcal A)$.

**1. Monotonie.** Si $A \subset B$, alors $m(A) \leq m(B)$.

*Preuve.* $B = A \cup (B \setminus A)$, union disjointe. Par additivité, $m(B) = m(A) + m(B \setminus A) \geq m(A)$. ∎

**2. Différence.** Si $A \subset B$ et $m(A) < \infty$, alors $m(B \setminus A) = m(B) - m(A)$.

*Preuve.* Même décomposition. On peut soustraire $m(A)$ car il est fini. ∎

**3. σ-sous-additivité.** Pour toute suite $(A_n)$ (pas nécessairement disjointe),

$$m\Bigl(\bigcup_{n=1}^{\infty} A_n\Bigr) \leq \sum_{n=1}^{\infty} m(A_n).$$

*Preuve.* On pose $B_1 = A_1$ et $B_n = A_n \setminus \bigcup_{k < n} A_k$ pour $n \geq 2$. Les $B_n$ sont disjoints, de même union que les $A_n$, et $B_n \subset A_n$, donc $m(B_n) \leq m(A_n)$. Par σ-additivité appliquée aux $B_n$, puis monotonie :

$$m\Bigl(\bigcup_n A_n\Bigr) = \sum_n m(B_n) \leq \sum_n m(A_n). \quad ∎$$

**4. Continuité monotone croissante (par en bas).** Si $A_1 \subset A_2 \subset \cdots$ (on note $A_n \uparrow A$ avec $A = \bigcup_n A_n$), alors

$$m(A) = \lim_{n \to \infty} m(A_n).$$

*Preuve.* On pose $B_1 = A_1$ et $B_n = A_n \setminus A_{n-1}$ pour $n \geq 2$. Les $B_n$ sont disjoints et $\bigcup_n B_n = A$. Par σ-additivité,

$$m(A) = \sum_{n=1}^{\infty} m(B_n) = \lim_{N \to \infty} \sum_{n=1}^{N} m(B_n) = \lim_{N \to \infty} m(A_N)$$

la dernière égalité venant de l'additivité finie appliquée à $A_N = B_1 \cup \cdots \cup B_N$. ∎

**5. Continuité monotone décroissante (par en haut).** Si $A_1 \supset A_2 \supset \cdots$ et **$m(A_1) < \infty$** (on note $A_n \downarrow A$ avec $A = \bigcap_n A_n$), alors

$$m(A) = \lim_{n \to \infty} m(A_n).$$

*Preuve.* On applique la continuité croissante aux complémentaires relatifs $A_1 \setminus A_n \uparrow A_1 \setminus A$. On obtient $m(A_1 \setminus A_n) \to m(A_1 \setminus A)$, soit $m(A_1) - m(A_n) \to m(A_1) - m(A)$. La soustraction est licite car $m(A_1) < \infty$. ∎

*Remarque.* L'hypothèse $m(A_1) < \infty$ est indispensable : on a vu au chapitre I que sans elle, on peut avoir $A_n \downarrow \emptyset$ et $m(A_n) = 1$ pour tout $n$.

#### Exemples de mesures

Des mesures ont déjà été rencontrées au chapitre I. On les rassemble ici, avec quelques compléments.

- **Mesure de Dirac** $\delta_{x_0}$ en un point $x_0 \in \Omega$ : $\delta_{x_0}(A) = \mathbf{1}_{x_0 \in A}$. C'est une mesure finie sur $(\Omega, \mathcal A)$ pour toute tribu $\mathcal A$ telle que $\{x_0\} \in \mathcal A$. On a $\delta_{x_0}(\Omega) = 1$, c'est donc une probabilité.

- **Mesure de comptage** $\#$ : $\#(A) = |A|$ si $A$ est fini, $+\infty$ sinon. Mesure sur $(\Omega, \mathcal P(\Omega))$ pour tout $\Omega$.

- **Mesure nulle** : $m(A) = 0$ pour tout $A$. C'est la plus petite mesure possible. Elle est σ-additive de façon triviale.

- **Combinaison linéaire.** Si $m_1, m_2$ sont des mesures sur $(\Omega, \mathcal A)$ et $\alpha, \beta \geq 0$, alors $\alpha m_1 + \beta m_2$ est une mesure. Plus généralement, pour une suite de mesures $(m_n)$ et de coefficients $(\alpha_n) \subset [0,+\infty)$, la somme $m = \sum_n \alpha_n m_n$ est une mesure (la σ-additivité se transmet car on peut intervertir deux sommes de termes positifs).

*Exemple.* Toute combinaison $\sum_{i} \alpha_i \delta_{x_i}$ avec $\alpha_i \geq 0$ est une mesure. Si de plus $\sum_i \alpha_i = 1$, c'est une probabilité. On retrouve ainsi les lois discrètes.

### 2. Mesure de Lebesgue sur ℝ

#### Objectif

L'objectif est de construire la mesure qui résout le problème de la mesure posé au chapitre I — dans le cadre restreint de la tribu borélienne. Concrètement, on cherche une mesure $\lambda$ sur $(\mathbb R, \mathcal B(\mathbb R))$ qui :

- prolonge la longueur : $\lambda([a,b]) = b - a$ ;
- soit invariante par translation : $\lambda(A + t) = \lambda(A)$ ;
- soit σ-additive (c'est dans la définition de mesure).

Le théorème de Vitali nous dit que ces trois propriétés sont incompatibles sur $\mathcal P(\mathbb R)$, mais le passage à $\mathcal B(\mathbb R)$ rend la construction possible.

#### Le théorème de Carathéodory (idée)

La construction repose sur un résultat général : le **théorème d'extension de Carathéodory**. L'idée est la suivante.

On part d'une « pré-mesure » définie sur une famille simple d'ensembles — ici, la longueur sur les intervalles. On l'étend d'abord en une **mesure extérieure** $\lambda^*$ définie sur toutes les parties de $\mathbb R$ :

$$\lambda^*(A) = \inf \Bigl\{ \sum_{n=1}^{\infty} (b_n - a_n) : A \subset \bigcup_{n=1}^{\infty} (a_n, b_n) \Bigr\}$$

On recouvre $A$ par des intervalles ouverts et on prend la borne inférieure des sommes des longueurs de ces recouvrements. Cette mesure extérieure est définie sur $\mathcal P(\mathbb R)$ tout entier, mais elle n'est pas σ-additive en général (seulement σ-sous-additive). Le théorème de Carathéodory identifie alors une σ-algèbre — la tribu de Lebesgue $\mathcal L$ — sur laquelle $\lambda^*$ est σ-additive. La restriction de $\lambda^*$ à $\mathcal L$ est la **mesure de Lebesgue**.

#### Énoncé

**Théorème (existence et unicité).** Il existe une unique mesure $\lambda$ sur $(\mathbb R, \mathcal B(\mathbb R))$ telle que $\lambda([a,b]) = b - a$ pour tout intervalle $[a,b]$.

L'unicité vient du fait que les intervalles engendrent $\mathcal B(\mathbb R)$ et forment un système « suffisamment stable » (un π-système). Le lemme de classe monotone (ou le théorème d'unicité des mesures) garantit qu'une mesure σ-finie est entièrement déterminée par ses valeurs sur un π-système qui engendre la tribu.

#### Tribu de Lebesgue vs tribu borélienne

La construction de Carathéodory produit en fait une tribu $\mathcal L$ plus grande que $\mathcal B(\mathbb R)$ :

$$\mathcal B(\mathbb R) \subsetneq \mathcal L \subsetneq \mathcal P(\mathbb R).$$

La tribu de Lebesgue $\mathcal L$ contient $\mathcal B(\mathbb R)$ et tous les sous-ensembles d'ensembles de mesure nulle (on dit qu'elle est **complète**). La tribu borélienne, elle, n'est pas complète.

*Exemple.* L'ensemble de Cantor $C$ est borélien (c'est un fermé) et vérifie $\lambda(C) = 0$. Or $C$ a la puissance du continu : il contient autant de points que $\mathbb R$. Tout sous-ensemble de $C$ est Lebesgue-mesurable (de mesure nulle), mais il en existe qui ne sont pas boréliens. Cela fournit un exemple d'ensemble Lebesgue-mesurable non borélien.

En pratique, la distinction importe rarement : on travaille presque toujours sur $\mathcal B(\mathbb R)$, et les ensembles qu'on rencontre sont boréliens.

#### Propriétés de la mesure de Lebesgue

**1. Invariance par translation.** $\lambda(A + t) = \lambda(A)$ pour tout borélien $A$ et tout $t \in \mathbb R$. C'est la propriété géométrique fondamentale, celle-là même qui posait problème sur $\mathcal P(\mathbb R)$.

**2. Comportement par changement d'échelle.** $\lambda(\alpha A) = |\alpha| \lambda(A)$ pour tout $\alpha \in \mathbb R$, où $\alpha A = \{\alpha x : x \in A\}$. Dilater un ensemble par un facteur $\alpha$ multiplie sa mesure par $|\alpha|$.

**3. Tout dénombrable est négligeable.** Si $A$ est dénombrable, $\lambda(A) = 0$. En effet, $A = \bigcup_n \{a_n\}$ et $\lambda(\{a_n\}) = 0$ pour tout $n$. En particulier, $\lambda(\mathbb Q) = 0$ : les rationnels, bien que denses dans $\mathbb R$, ont une mesure nulle.

**4. Tout ouvert non vide a une mesure strictement positive.** Un ouvert non vide contient un intervalle $(a,b)$ avec $a < b$, donc sa mesure est au moins $b - a > 0$.

**5. σ-finitude.** $\lambda$ est σ-finie : $\mathbb R = \bigcup_{n \geq 1} [-n, n]$ et $\lambda([-n,n]) = 2n < \infty$.

#### Ensembles de mesure nulle et ensembles négligeables

**Définition.** Un ensemble $A$ est **négligeable** (pour la mesure $m$) si $m(A) = 0$.Un ensemble est **$m$-négligeable** s'il est contenu dans un ensemble mesurable de mesure nulle.

Les propriétés « qui sont vraies sauf sur un ensemble négligeable » jouent un rôle central en théorie de la mesure. On dit qu'une propriété est vraie **presque partout** (abrégé p.p., ou **presque sûrement** en probabilités, abrégé p.s.) si l'ensemble des points où elle est fausse est négligeable.

*Propriétés des ensembles négligeables.* Toute partie d'un ensemble négligeable est négligeable (dans la tribu de Lebesgue ; pas nécessairement dans $\mathcal B(\mathbb R)$ — c'est la question de la complétude). Toute union dénombrable d'ensembles négligeables est négligeable (par σ-sous-additivité).

### 3. Probabilités : axiomes de Kolmogorov

#### D'une mesure à une probabilité

Une probabilité est une mesure de masse totale 1. C'est un cas particulier de la théorie générale, mais c'est le cas le plus important pour ce cours.

**Définition.** Soit $(\Omega, \mathcal A)$ un espace mesurable. Une **probabilité** sur $(\Omega, \mathcal A)$ est une mesure $P : \mathcal A \to [0, 1]$ telle que $P(\Omega) = 1$.

Le triplet $(\Omega, \mathcal A, P)$ s'appelle un **espace probabilisé** (ou espace de probabilité). Les éléments de $\Omega$ s'appellent les **issues** (ou résultats, ou états du monde), les éléments de $\mathcal A$ les **événements**, et $P(A)$ la **probabilité de l'événement** $A$.

#### Les axiomes de Kolmogorov

La définition ci-dessus constitue, en substance, les axiomes posés par Kolmogorov en 1933. Pour les rendre explicites :

**Axiomes.** Un espace de probabilité est un triplet $(\Omega, \mathcal A, P)$ où :

1. $\Omega$ est un ensemble non vide (l'univers) ;
2. $\mathcal A$ est une σ-algèbre sur $\Omega$ (les événements) ;
3. $P : \mathcal A \to [0,1]$ est une application vérifiant :
   - $P(\Omega) = 1$ (normalisation),
   - pour toute suite $(A_n)$ d'événements deux à deux disjoints, $P\bigl(\bigcup_n A_n\bigr) = \sum_n P(A_n)$ (σ-additivité).

L'axiomatisation de Kolmogorov fonde les probabilités sur la théorie de la mesure. C'est l'analogue, pour les probabilités, de ce qu'a fait Euclide pour la géométrie : un petit nombre de principes à partir desquels tout le reste se déduit.

#### Propriétés élémentaires

Toutes les propriétés des mesures (section 1) s'appliquent. On les reformule dans le langage probabiliste.

**1. Complémentaire.** $P(A^c) = 1 - P(A)$.

*Preuve.* $\Omega = A \cup A^c$, union disjointe. Par additivité, $1 = P(A) + P(A^c)$. ∎

**2. Monotonie.** Si $A \subset B$, alors $P(A) \leq P(B)$.

**3. Sous-additivité (union bound).** $P(A \cup B) \leq P(A) + P(B)$. Plus généralement, pour toute suite,

$$P\Bigl(\bigcup_{n} A_n\Bigr) \leq \sum_n P(A_n).$$

**4. Formule d'inclusion-exclusion.** Pour deux événements :

$$P(A \cup B) = P(A) + P(B) - P(A \cap B).$$

Pour $n$ événements :

$$P\Bigl(\bigcup_{i=1}^n A_i\Bigr) = \sum_i P(A_i) - \sum_{i < j} P(A_i \cap A_j) + \sum_{i < j < k} P(A_i \cap A_j \cap A_k) - \cdots + (-1)^{n+1} P(A_1 \cap \cdots \cap A_n).$$

**5. Continuité.** Si $A_n \uparrow A$, alors $P(A_n) \to P(A)$. Si $A_n \downarrow A$, alors $P(A_n) \to P(A)$. (L'hypothèse $m(A_1) < \infty$ de la continuité décroissante est automatiquement vérifiée car $P(A_1) \leq 1$.)

#### Exemples d'espaces probabilisés

**Espaces finis.** $\Omega = \{\omega_1, \dots, \omega_n\}$, $\mathcal A = \mathcal P(\Omega)$, $P$ définie par des poids $p_i = P(\{\omega_i\})$ avec $p_i \geq 0$ et $\sum_i p_i = 1$. Si tous les poids sont égaux ($p_i = 1/n$), on parle de **probabilité uniforme**.

**Espaces dénombrables.** $\Omega = \mathbb N$, $\mathcal A = \mathcal P(\mathbb N)$, $P(\{n\}) = p_n$ avec $\sum_n p_n = 1$. C'est le cadre des lois discrètes (Bernoulli, binomiale, Poisson, géométrique, etc.).

**Espaces continus.** $\Omega = \mathbb R$ (ou un sous-ensemble), $\mathcal A = \mathcal B(\mathbb R)$, $P$ définie par une densité $f \geq 0$ avec $\int_{\mathbb R} f \, d\lambda = 1$ :

$$P(A) = \int_A f(x) \, dx.$$

C'est le cadre des lois continues (uniforme, exponentielle, gaussienne, etc.). La notion de densité sera précisée à la section 4.

#### Probabilité conditionnelle

**Définition.** Soit $B$ un événement avec $P(B) > 0$. La **probabilité conditionnelle** de $A$ sachant $B$ est

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}.$$

Pour $B$ fixé, l'application $A \mapsto P(A \mid B)$ est une probabilité sur $(\Omega, \mathcal A)$. Intuitivement, on restreint l'univers à $B$ et on renormalise.

**Formule des probabilités totales.** Si $(B_n)_{n \geq 1}$ est une partition de $\Omega$ en événements de probabilité strictement positive (i.e. $B_n$ deux à deux disjoints, $\bigcup_n B_n = \Omega$, $P(B_n) > 0$), alors pour tout événement $A$ :

$$P(A) = \sum_{n=1}^{\infty} P(A \mid B_n) P(B_n).$$

*Preuve.* $A = \bigcup_n (A \cap B_n)$, union disjointe. Par σ-additivité, $P(A) = \sum_n P(A \cap B_n) = \sum_n P(A \mid B_n) P(B_n)$. ∎

**Formule de Bayes.** Sous les mêmes hypothèses, pour tout $k$ :

$$P(B_k \mid A) = \frac{P(A \mid B_k) P(B_k)}{\sum_n P(A \mid B_n) P(B_n)}.$$

*Preuve.* Appliquer la définition de $P(B_k \mid A) = P(A \cap B_k) / P(A)$, puis exprimer le numérateur et le dénominateur. ∎

La formule de Bayes « inverse » le conditionnement : connaissant les probabilités des causes $B_k$ et les vraisemblances $P(A \mid B_k)$ de l'observation $A$ sous chaque cause, on en déduit les probabilités révisées $P(B_k \mid A)$ des causes à la lumière de l'observation.

### 4. Densité et mesure absolument continue

#### Motivation

On rencontre souvent des probabilités sur $(\mathbb R, \mathcal B(\mathbb R))$ décrites par une fonction $f \geq 0$ avec $\int f \, d\lambda = 1$ : on pose $P(A) = \int_A f \, d\lambda$. La fonction $f$ est la **densité** de $P$ par rapport à la mesure de Lebesgue. On veut comprendre quand un tel $f$ existe, et dans quel cadre général.

#### Mesure absolument continue

**Définition.** Soient $\mu$ et $\nu$ deux mesures sur $(\Omega, \mathcal A)$. On dit que $\mu$ est **absolument continue** par rapport à $\nu$, et on écrit $\mu \ll \nu$, si

$$\forall A \in \mathcal A, \quad \nu(A) = 0 \implies \mu(A) = 0.$$

Autrement dit, $\mu$ ne charge pas les ensembles $\nu$-négligeables : tout ce qui est invisible pour $\nu$ l'est aussi pour $\mu$.

*Exemples.*

- Si $P(A) = \int_A f \, d\lambda$ pour une densité $f \geq 0$, alors $P \ll \lambda$. En effet, si $\lambda(A) = 0$, l'intégrale de $f$ sur $A$ est nulle.
- La mesure de Dirac $\delta_0$ n'est pas absolument continue par rapport à $\lambda$ : $\lambda(\{0\}) = 0$ mais $\delta_0(\{0\}) = 1$.
- $\lambda$ n'est pas absolument continue par rapport à $\delta_0$ : $\delta_0(\{0\}^c) = 0$ mais $\lambda(\{0\}^c) = +\infty$.

#### Le théorème de Radon-Nikodym

**Théorème (Radon-Nikodym).** Soient $\mu$ et $\nu$ deux mesures σ-finies sur $(\Omega, \mathcal A)$, avec $\mu \ll \nu$. Alors il existe une fonction mesurable $f : \Omega \to [0, +\infty)$ telle que

$$\forall A \in \mathcal A, \quad \mu(A) = \int_A f \, d\nu.$$

La fonction $f$ est unique $\nu$-presque partout. On l'appelle la **dérivée de Radon-Nikodym** (ou **densité**) de $\mu$ par rapport à $\nu$, et on la note $\frac{d\mu}{d\nu}$.

La preuve complète sera possible après le chapitre III (Intégration). On admet ici l'énoncé.

*Remarques.*

- L'hypothèse de σ-finitude est essentielle : sans elle, le théorème est faux.
- La notation $\frac{d\mu}{d\nu}$ est suggestive : elle se comporte comme une « dérivée » au sens où $d\mu = f \, d\nu$, et les règles de chaîne s'appliquent. Si $\mu \ll \nu \ll \rho$, alors $\frac{d\mu}{d\rho} = \frac{d\mu}{d\nu} \cdot \frac{d\nu}{d\rho}$ (presque partout).
- En probabilités, la densité d'une loi est toujours relative à une mesure de référence (le plus souvent la mesure de Lebesgue). Dire qu'une variable aléatoire « a une densité » signifie que sa loi est absolument continue par rapport à $\lambda$.

#### Mesures singulières

**Définition.** Deux mesures $\mu$ et $\nu$ sur $(\Omega, \mathcal A)$ sont **mutuellement singulières**, noté $\mu \perp \nu$, s'il existe $A \in \mathcal A$ tel que $\mu(A) = 0$ et $\nu(A^c) = 0$. Autrement dit, elles « vivent » sur des ensembles disjoints.

*Exemple.* $\delta_0 \perp \lambda$ : prendre $A = \{0\}^c$. On a $\delta_0(A) = 0$ et $\lambda(A^c) = \lambda(\{0\}) = 0$.

**Décomposition de Lebesgue.** Toute mesure σ-finie $\mu$ se décompose de façon unique en $\mu = \mu_{ac} + \mu_s$ où $\mu_{ac} \ll \nu$ et $\mu_s \perp \nu$. C'est la « partie absolument continue » et la « partie singulière » de $\mu$ par rapport à $\nu$.

### 5. Mesures produit et théorème de Fubini

#### Motivation

On veut mesurer des ensembles dans un espace produit $\Omega_1 \times \Omega_2$. Par exemple, pour deux lancers de dé indépendants, l'espace est $\{1,\dots,6\}^2$ ; pour un point aléatoire dans le plan, c'est $\mathbb R^2$. La question est : comment construire une mesure sur le produit à partir des mesures sur les facteurs ?

#### Tribu produit

Au chapitre I, on a vu que $\mathcal B(\mathbb R^n) = \mathcal B(\mathbb R)^{\otimes n}$. On généralise.

**Définition.** Soient $(\Omega_1, \mathcal A_1)$ et $(\Omega_2, \mathcal A_2)$ deux espaces mesurables. La **tribu produit** est

$$\mathcal A_1 \otimes \mathcal A_2 = \sigma\bigl(\{A_1 \times A_2 : A_1 \in \mathcal A_1, \, A_2 \in \mathcal A_2\}\bigr).$$

C'est la tribu engendrée par les « rectangles mesurables ». L'espace mesurable produit est $(\Omega_1 \times \Omega_2, \, \mathcal A_1 \otimes \mathcal A_2)$.

#### Mesure produit

**Théorème (existence et unicité de la mesure produit).** Soient $(Ω_1, \mathcal A_1, m_1)$ et $(\Omega_2, \mathcal A_2, m_2)$ deux espaces mesurés σ-finis. Il existe une unique mesure $m_1 \otimes m_2$ sur $(\Omega_1 \times \Omega_2, \, \mathcal A_1 \otimes \mathcal A_2)$ telle que

$$\forall A_1 \in \mathcal A_1, \, \forall A_2 \in \mathcal A_2, \quad (m_1 \otimes m_2)(A_1 \times A_2) = m_1(A_1) \cdot m_2(A_2).$$

L'unicité repose, comme pour la mesure de Lebesgue, sur le fait que les rectangles mesurables forment un π-système qui engendre la tribu produit, et le théorème d'unicité des mesures s'applique (les mesures étant σ-finies).

*Exemple.* La mesure de Lebesgue sur $\mathbb R^2$ est $\lambda \otimes \lambda$ : l'aire d'un rectangle $[a,b] \times [c,d]$ est $(b-a)(d-c) = \lambda([a,b]) \cdot \lambda([c,d])$.

#### Le théorème de Fubini-Tonelli

C'est l'outil qui permet de calculer les intégrales doubles par intégrales itérées.

**Théorème (Tonelli).** Soient $(Ω_1, \mathcal A_1, m_1)$ et $(\Omega_2, \mathcal A_2, m_2)$ deux espaces mesurés σ-finis, et $f : \Omega_1 \times \Omega_2 \to [0, +\infty]$ une fonction mesurable positive. Alors :

$$\int_{\Omega_1 \times \Omega_2} f \, d(m_1 \otimes m_2) = \int_{\Omega_1} \Bigl(\int_{\Omega_2} f(\omega_1, \omega_2) \, dm_2(\omega_2)\Bigr) dm_1(\omega_1) = \int_{\Omega_2} \Bigl(\int_{\Omega_1} f(\omega_1, \omega_2) \, dm_1(\omega_1)\Bigr) dm_2(\omega_2).$$

Les trois quantités sont égales (éventuellement infinies). Aucune hypothèse d'intégrabilité n'est nécessaire : pour les fonctions positives, on peut toujours intervertir les intégrales.

**Théorème (Fubini).** Si de plus $f$ est intégrable (i.e. $\int |f| \, d(m_1 \otimes m_2) < \infty$), alors les trois intégrales ci-dessus sont finies et égales.

*Usage pratique.* Pour calculer $\int f \, d(m_1 \otimes m_2)$ :

1. Si $f \geq 0$ : appliquer directement Tonelli, l'interversion est toujours licite.
2. Si $f$ change de signe : vérifier d'abord que $\int |f| < \infty$ (en appliquant Tonelli à $|f|$), puis appliquer Fubini.

Le piège classique est d'intervertir les intégrales pour une fonction qui n'est pas de signe constant et qui n'est pas intégrable : on peut alors obtenir des résultats différents selon l'ordre d'intégration.
