# Inégalités fondamentales sur un espace vectoriel normé

> **Idée directrice.** Les inégalités de Young, Hölder, Minkowski et Cauchy-Schwarz forment une chaîne logique : chacune découle de la précédente. La brique de base est une inégalité sur $\mathbb{R}_+$ (Young). Le passage aux vecteurs se fait via la valeur absolue $|\cdot|$, qui ramène tout calcul à $\mathbb{R}_+$.

## I. Structure minimale d'un espace normé

Soit $\mathbb{K}$ un corps muni d'une valeur absolue $|\cdot| : \mathbb{K} \to \mathbb{R}_+$, et $E$ un espace vectoriel sur $\mathbb{K}$ muni d'une norme $\|\cdot\|$.

**Inégalité triangulaire.**

$$\|x + y\| \leq \|x\| + \|y\|$$

**Homogénéité.**

$$\|\lambda x\| = |\lambda| \cdot \|x\|, \quad \lambda \in \mathbb{K}$$

**Norme duale.** Pour toute forme linéaire continue $\varphi : E \to \mathbb{K}$ :

$$\|\varphi\|_* = \sup_{\|x\| \leq 1} |\varphi(x)|$$

et pour tout $x \in E$ :

$$|\varphi(x)| \leq \|\varphi\|_* \cdot \|x\|$$

Les deux expressions sont équivalentes par homogénéité de $\varphi$.  
La constante $\|\varphi\|_*$ est finie si et seulement si $\varphi$ est continue (pour une application linéaire, continuité équivaut à être bornée sur la boule unité). En dimension finie, toute forme linéaire est automatiquement continue ; en dimension infinie, il existe des formes linéaires discontinues.

## II. Inégalité de Young (brique de base sur $\mathbb{R}_+$)

Pour $a, b \in \mathbb{R}_+$ et $p, q > 1$ avec $\frac{1}{p} + \frac{1}{q} = 1$ :

$$ab \leq \frac{a^p}{p} + \frac{b^q}{q}$$

C'est une inégalité purement réelle : elle repose sur la convexité de l'exponentielle (cas d'égalité de la concavité du logarithme). Les vecteurs n'interviennent pas encore.

## III. Passage aux vecteurs dans $\mathbb{K}^n$ (spécifique à $\ell_p$)

Les trois résultats de cette section — Hölder, dualité $\ell_p/\ell_q$, Minkowski — utilisent la structure spécifique des normes $\ell_p$ (les sommes $\sum |x_k|^p$). Ils se généralisent à $L^p(\Omega, \mu)$ en remplaçant $\sum$ par $\int$.

Pour $a = (a_k), x = (x_k) \in \mathbb{K}^n$, on travaille avec $|a_k|, |x_k| \in \mathbb{R}_+$. Toute l'analyse vit dans $\mathbb{R}_+$ via la valeur absolue.

### Inégalité de Hölder

Pour $a, x \in \mathbb{K}^n$ et $p, q > 1$ avec $\frac{1}{p} + \frac{1}{q} = 1$ :

$$\left|\sum_{k=1}^n a_k x_k\right| \leq \|a\|_q \cdot \|x\|_p$$

où $\|x\|_p = \left(\sum |x_k|^p\right)^{1/p}$.

La preuve applique Young à chaque paire $(|a_k|, |x_k|)$ après normalisation par $\|a\|_q$ et $\|x\|_p$.

### Dualité $\ell_p / \ell_q$

Pour la forme linéaire $\varphi(x) = \sum a_k x_k$ :

$$\|\varphi\|_* = \|a\|_q$$

Conséquence directe de Hölder : l'inégalité $|\varphi(x)| \leq \|a\|_q \|x\|_p$ donne $\|\varphi\|_* \leq \|a\|_q$, et l'égalité est atteinte pour $x_k = |a_k|^{q-1} \bar{a}_k / |a_k|$ (amplitude qui réalise l'égalité dans Young, phase qui aligne $a_k x_k$ sur $\mathbb{R}_+$).

### Inégalité de Minkowski

Pour $x, y \in \mathbb{K}^n$ et $p \geq 1$ :

$$\|x + y\|_p \leq \|x\|_p + \|y\|_p$$

C'est l'inégalité triangulaire pour $\|\cdot\|_p$ — elle garantit que $\|\cdot\|_p$ est une norme. La preuve repose sur Hölder.

## IV. Cas particulier : produit scalaire ($p = 2$)

Pour $\mathbb{K} = \mathbb{R}$ ou $\mathbb{C}$, avec le produit scalaire $\langle x, y \rangle = \sum \bar{x}_k y_k$ :

**Inégalité de Cauchy-Schwarz.**

$$|\langle x, y \rangle| \leq \|x\|_2 \cdot \|y\|_2$$

C'est le cas $p = q = 2$ de Hölder. Mais Cauchy-Schwarz admet aussi une preuve directe, valable dans tout espace préhilbertien (pas seulement $\ell_2$) : le discriminant du polynôme $t \mapsto \|x + ty\|^2 \geq 0$ donne l'inégalité sans passer par Hölder. Dans ce cas, la dualité $\ell_p / \ell_q$ devient l'auto-dualité $\ell_2 / \ell_2$ : le théorème de Riesz.

## Chaîne logique

$$\text{Young } (\mathbb{R}_+) \;\Rightarrow\; \text{Hölder } (\mathbb{K}^n \text{ via } |\cdot|) \;\Rightarrow\; \text{Dualité } \ell_p/\ell_q \;\Rightarrow\; \text{Minkowski (norme)}$$

Les vecteurs vivent dans $\mathbb{K}$, mais toute l'analyse passe par $\mathbb{R}_+$ via la valeur absolue.
