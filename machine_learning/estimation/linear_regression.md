# La régression linéaire : convergence de vues

> **Idée directrice.** La régression linéaire est suffisamment simple pour être résolue par une dizaine de méthodes différentes — et suffisamment riche pour que chacune révèle quelque chose que les autres cachent.

---

> **Espaces.** On travaille principalement avec deux espaces hermitiens munis du produit scalaire usuel, mais $\mathbb{C}^p$ y joue deux rôles distincts. D'une part, $\mathbb{C}^p$ est l'espace des covariables individuelles : chaque observation peut être identifiée à un vecteur de covariables dans cet espace. D'autre part, $\mathbb{C}^n$ est l'espace des variables indexées par les observations : c'est là que vivent $y$ et les colonnes de $X$. Enfin, le même espace vectoriel $\mathbb{C}^p$ intervient conceptuellement comme espace des paramètres, dans lequel vit $\beta$.

## 1. Projection orthogonale

On cherche la meilleure approximation de $y$ par un vecteur de la forme $X\beta$. Tout choix de $\beta \in \mathbb{C}^p$ produit une prédiction $X\beta$ dans le **sous-espace colonne**

$$\operatorname{col}(X) = \{ X\beta : \beta \in \mathbb{C}^p \} \subset \mathbb{C}^n.$$

La solution géométrique est de projeter orthogonalement $y$ sur $\operatorname{col}(X)$, ce qui entraine un résidu $e = y - X\hat\beta$ orthogonal à $\operatorname{col}(X)$ :

$$X^*(y - X\hat\beta) = 0 \quad\Longleftrightarrow\quad X^* X\,\hat\beta = X^* y.$$

Ces **équations normales** tirent leur nom précisément de cette condition. Quand $X$ est de rang plein, $X^* X$ est inversible et $\hat\beta = (X^* X)^{-1}X^* y$. La prédiction $\hat y = Py$ est donnée par le **projecteur orthogonal** $P = X(X^* X)^{-1}X^*$, hermitien et idempotent.

Ce cadre est purement géométrique : aucune hypothèse explicite sur le bruit. L'idempotence de $P$ n'est pas une propriété à vérifier mais une tautologie — projeter deux fois un point déjà dans $\operatorname{col}(X)$ ne le déplace pas.

L'hypothèse de rang plein n'est qu'une condition de confort : elle garantit que $X^* X$ est inversible, mais la projection sur $\operatorname{col}(X)$ existe et est unique quel que soit le rang. C'est le cadre SVD qui rend cela explicite : la pseudo-inverse $X^+ = V\Sigma^+ U^*$ fournit toujours un minimiseur des moindres carrés, et sélectionne, lorsque ce minimiseur n'est pas unique, celui de norme minimale.

## 2. Décomposition en valeurs singulières

La SVD ne répond pas seulement à la question du rang déficient — elle révèle la structure géométrique du problème dans toute sa généralité. Toute matrice $X \in \mathbb{C}^{n \times p}$ de rang $r$ admet une décomposition

$$X = U\Sigma V^*$$

où $U \in \mathbb{C}^{n \times n}$ et $V \in \mathbb{C}^{p \times p}$ sont unitaires, et $\Sigma \in \mathbb{R}^{n \times p}$ est diagonale avec des valeurs singulières $\sigma_1 \geq \cdots \geq \sigma_r > 0 = \sigma_{r+1} = \cdots$.

**Changement de base.** On pose $\tilde y = U^* y \in \mathbb{C}^n$ et $\tilde\beta = V^* \beta \in \mathbb{C}^p$. Les équations normales $X^* X\hat\beta = X^* y$ deviennent, dans ces nouvelles coordonnées,

$$\Sigma^* \Sigma\,\tilde\beta = \Sigma^* \tilde y.$$

Le problème est maintenant diagonal : pour chaque indice $i \leq r$, l'équation se réduit à $\sigma_i^2 \tilde\beta_i = \sigma_i \tilde y_i$, soit $\tilde\beta_i = \tilde y_i / \sigma_i$. Pour $i > r$, la $i$-ème équation est $0 = 0$ — aucune contrainte sur $\tilde\beta_i$. La solution de norme minimale impose $\tilde\beta_i = 0$ pour $i > r$.

**Retour dans la base originale.** On note $\Sigma^+$ la matrice $p \times n$ dont les entrées diagonales valent $1/\sigma_i$ pour $i \leq r$ et $0$ sinon. La solution de norme minimale est

$$\hat\beta = V\tilde\beta = V\Sigma^+ U^* y =: X^+ y$$

où $X^+ = V\Sigma^+ U^*$ est la **pseudo-inverse de Moore-Penrose** de $X$.

**Ce que la SVD rend visible.** La prédiction s'écrit d'abord

$$\hat y = X\hat\beta = XX^+ y = U\Sigma\Sigma^+ U^* y,$$

et n'est autre que la projection orthogonale de $y$ sur $\operatorname{col}(X)$ — ce que la section précédente posait comme point de départ devient ici un résultat. Plus précisément, $XX^+ = U\Sigma\Sigma^+U^*$ est hermitien, car $\Sigma\Sigma^+$ est réelle diagonale et $U$ est unitaire, et idempotent, car $(\Sigma\Sigma^+)^2 = \Sigma\Sigma^+$ : c'est bien le projecteur orthogonal sur $\operatorname{col}(X)$. La prédiction ne retient donc que les composantes de $\tilde y$ associées aux directions singulières non nulles.

La SVD expose également la sensibilité numérique du problème : une petite valeur singulière $\sigma_i \approx 0$ est amplifiée en $1/\sigma_i$ dans $X^+$, ce qui amplifie le bruit dans la direction correspondante. La régularisation de Ridge — remplacer $1/\sigma_i$ par $\sigma_i/(\sigma_i^2 + \lambda)$ — est exactement un filtrage spectral qui atténue ces directions instables.

## 3. Minimisation d'une fonction de perte

On se place cette fois dans l'espace des paramètres $\mathbb{C}^p$ et on pose le problème directement comme un problème d'optimisation : trouver $\beta$ qui minimise la fonction de perte

$$\mathcal{L}(\beta) = \|y - X\beta\|^2 = (y - X\beta)^*(y - X\beta).$$

$\mathcal{L}$ est une fonction réelle convexe, différentiable au sens de Wirtinger. En annulant le gradient par rapport à $\overline\beta$,

$$\nabla_{\overline\beta} \mathcal{L}(\beta) = -X^*(y - X\beta) = 0,$$

on retrouve exactement les équations normales $X^*X\hat\beta = X^*y$. Si $X$ n'est pas de rang plein, cette condition décrit plusieurs minimiseurs, et la pseudo-inverse sélectionne parmi eux celui de norme minimale. La solution géométrique de la section 1 et la solution analytique de l'optimisation coïncident — elles décrivent le même objet depuis deux espaces différents.

Ce cadre rend naturelle une modification : ajouter un terme de régularisation $\lambda\|\beta\|^2$ conduit au problème de **Ridge**,

$$\mathcal{L}_\lambda(\beta) = \|y - X\beta\|^2 + \lambda\|\beta\|^2, \qquad \lambda > 0,$$

dont la solution est $\hat\beta_\lambda = (X^*X + \lambda I)^{-1}X^*y$. Dans le cadre SVD, cela revient à remplacer chaque $1/\sigma_i$ par $\sigma_i/(\sigma_i^2 + \lambda)$ : un filtrage spectral qui atténue les directions de faible variance sans les annuler.

## 4. Maximum de vraisemblance

On note $Y$ le vecteur aléatoire et $y$ sa réalisation observée ; $X$ désigne la matrice de covariables, supposée déterministe.

On introduit un modèle probabiliste :

$$Y = X\beta + \varepsilon$$

où $\varepsilon$ désigne l'erreur complexe. Si $p_\varepsilon$ est sa densité, la vraisemblance est la densité de $Y$ évaluée en $y$, vue comme fonction des paramètres :

$$L(\beta, \sigma^2; y) = p_{Y\mid \beta,\sigma^2}(y) = p_\varepsilon(y - X\beta).$$

Dans le cas gaussien complexe circulaire $\varepsilon \sim \mathcal{CN}(0, \sigma^2 I_n)$, on a $Y \mid \beta \sim \mathcal{CN}(X\beta, \sigma^2 I_n)$ et

$$L(\beta, \sigma^2; y) = \frac{1}{(\pi\sigma^2)^n}\exp\!\left(-\frac{1}{\sigma^2}\|y - X\beta\|^2\right).$$

La log-vraisemblance s'écrit alors

$$\ell(\beta, \sigma^2) = -n\log(\pi\sigma^2) - \frac{1}{\sigma^2}\|y - X\beta\|^2.$$

À $\sigma^2$ fixé, maximiser $\ell$ en $\beta$ revient à minimiser $\|y - X\beta\|^2$ — on retrouve la fonction de perte de la section 3, et donc le même estimateur $\hat\beta = X^+y$.

Ce cadre révèle le lien général entre modèle d'erreur et fonction de perte.

**Distribution de l'erreur → fonction de perte.** On cherche à maximiser $p(y - X\beta) = p(\varepsilon)$ en $\beta$ pour $y$ fixé. Le log étant croissant, c'est équivalent à minimiser $-\log p(\varepsilon)$ — la fonction de perte canonique associée au modèle d'erreur. Toute fonction de perte qui n'en diffère que d'une constante additive définit le même estimateur et le même modèle d'erreur.

**Fonction de perte → distribution de l'erreur.** Réciproquement, toute fonction de perte suppose implicitement un modèle d'erreur : la densité $p(e) = Z^{-1}e^{-\mathcal{L}(e)}$, définie sous condition d'intégrabilité $Z = \int e^{-\mathcal{L}(e)}\,de < \infty$, à constante additive près. Cette densité n'est pas nécessairement celle du mécanisme générateur réel — c'est l'hypothèse probabiliste cachée derrière le choix de la perte.

Trois cas illustrent la correspondance :

- $-\log p(e) \propto \|e\|^2$ → gaussienne complexe circulaire $\mathcal{CN}(0, \sigma^2 I)$ — OLS
- $-\log p(e) \propto \|e\|_1$ → loi de type Laplace sur $\mathbb{C}^n$ — régression $\ell^1$
- $-\log p(e) \propto e^* \Sigma^{-1} e$ → gaussienne complexe corrélée $\mathcal{CN}(0, \Sigma)$ — GLS

Chaque fonction de perte est la signature d'un modèle d'erreur — explicite ou non.

## 5. Estimation MAP et régularisation

Dans le cadre fréquentiste de la section précédente, $\beta$ était un paramètre fixe inconnu. On adopte maintenant un point de vue bayésien : $\beta$ est une variable aléatoire, et on lui associe une distribution *a priori* $p(\beta)$ qui encode nos croyances avant d'observer les données.

Le théorème de Bayes donne le posterior :

$$p(\beta \mid y) \propto p(y \mid \beta) \cdot p(\beta).$$

L'estimateur MAP (Maximum A Posteriori) est le mode de ce posterior :

$$\hat\beta_{\text{MAP}} \in \arg\max_\beta \, p(\beta \mid y) = \arg\max_\beta \left[ \log p(y \mid \beta) + \log p(\beta) \right].$$

Maximiser le posterior revient donc à minimiser $-\log p(y \mid \beta) - \log p(\beta)$ — la log-vraisemblance négative à laquelle s'ajoute un terme $-\log p(\beta)$ qui pénalise les valeurs de $\beta$ peu probables sous le prior.

**Prior gaussien → Ridge.** On pose $\beta \sim \mathcal{CN}(0, \tau^2 I_p)$, ce qui donne $-\log p(\beta) = \frac{1}{\tau^2}\|\beta\|^2$ à constante près. Le problème MAP devient

$$\hat\beta_{\text{MAP}} \in \arg\min_\beta \left[ \frac{1}{\sigma^2}\|y - X\beta\|^2 + \frac{1}{\tau^2}\|\beta\|^2 \right],$$

soit exactement Ridge avec $\lambda = \sigma^2/\tau^2$. Le paramètre de régularisation n'est plus arbitraire — il est le rapport entre la variance du bruit et la variance du prior. Un grand $\lambda$ signifie qu'on fait davantage confiance au prior qu'aux données.

**Prior de type Laplace → Lasso.** On pose un prior $p(\beta) \propto e^{-\|\beta\|_1/b}$, ce qui donne $-\log p(\beta) = \frac{1}{b}\|\beta\|_1$ à constante près. Le problème MAP devient

$$\hat\beta_{\text{MAP}} \in \arg\min_\beta \left[ \frac{1}{\sigma^2}\|y - X\beta\|^2 + \frac{1}{b}\|\beta\|_1 \right],$$

soit exactement le Lasso. La parcimonie induite par la pénalisation $\ell^1$ n'est plus un artifice algorithmique — c'est la conséquence d'un prior qui concentre sa masse en zéro et admet des queues lourdes.

**Prior plat → OLS.** Sans information a priori sur $\beta$, on pose $p(\beta) \propto 1$ — un prior impropre, non normalisable, qui encode l'absence de préférence. On a alors $-\log p(\beta) = \text{cst}$, le terme de régularisation est nul, et le MAP se réduit à OLS.

On obtient ainsi une vue unifiée :

$$\hat\beta_{\text{MAP}} \in \arg\min_\beta \left[ \frac{1}{\sigma^2}\|y - X\beta\|^2 + \lambda\|\beta\|^q \right]$$

avec $q = 2$, $\lambda = \sigma^2/\tau^2$ pour Ridge ; $q = 1$, $\lambda = \sigma^2/b$ pour Lasso ; $\lambda = 0$ pour OLS. Le paramètre $\lambda$ est le curseur entre confiance aux données ($\lambda \to 0$) et confiance au prior ($\lambda \to \infty$, $\hat\beta \to 0$).

La structure est la même que dans la section 4, mais dans l'espace des paramètres : le choix du prior sur $\beta$ est équivalent au choix d'un terme de régularisation, à constante additive près sur $-\log p(\beta)$.

## 6. Optimalité : Gauss-Markov et Cramér-Rao

Les sections 1 à 4 ont construit l'estimateur des moindres carrés $\hat\beta = X^+y$, tandis que la section 5 a montré comment le point de vue bayésien le modifie de manière contrôlée par régularisation. Une question reste ouverte : dans quel sens statistique l'estimateur des moindres carrés est-il *bon* ? On suppose désormais que $X$ est de rang colonne plein, afin que $\beta$ soit identifiable ; si ce n'est pas le cas, les énoncés d'optimalité portent sur $X\beta$ ou sur une paramétrisation réduite, non sur $\beta$ lui-même.

**Gauss-Markov.** Sous les seules hypothèses $\mathbb{E}[\varepsilon] = 0$ et $\operatorname{Cov}(\varepsilon) = \sigma^2 I$ — sans aucune hypothèse sur la forme de la distribution — $\hat\beta = (X^*X)^{-1}X^*Y$ est le **meilleur estimateur linéaire non biaisé** (BLUE) : parmi tous les estimateurs de la forme $CY$ avec $CX = I_p$, il est celui de covariance minimale au sens matriciel,

$$\operatorname{Cov}(\hat\beta) \preceq \operatorname{Cov}(\tilde\beta)$$

pour tout estimateur linéaire non biaisé $\tilde\beta$. La gaussianité n'est pas nécessaire — seuls les deux premiers moments de $\varepsilon$ interviennent.

**Cramér-Rao.** Si on lève la contrainte de linéarité et qu'on considère les estimateurs non biaisés réguliers dans le modèle gaussien complexe circulaire, la borne de Cramér-Rao donne la covariance minimale atteignable :

$$\operatorname{Cov}(\hat\beta) \succeq \mathcal{I}(\beta)^{-1}$$

où, dans ce modèle, $\mathcal{I}(\beta) = \sigma^{-2}X^*X$ est la matrice d'information de Fisher, à convention près sur l'écriture réelle ou complexe de cette information. On a donc $\mathcal{I}(\beta)^{-1} = \sigma^2 (X^*X)^{-1}$, et l'estimateur des moindres carrés atteint cette borne — il est donc efficace au sens de Fisher.

La progression est nette : sans gaussianité, l'estimateur des moindres carrés est optimal dans la classe linéaire. Avec gaussianité complexe circulaire, il atteint la borne de Cramér-Rao et est donc efficace parmi les estimateurs non biaisés réguliers. L'hypothèse gaussienne ne change pas l'estimateur — elle élargit le théorème d'optimalité.

## Conclusion

Six cadres, un noyau commun. La projection orthogonale, la SVD, l'optimisation et le maximum de vraisemblance conduisent au même estimateur des moindres carrés $\hat\beta = X^+y$. La régularisation fréquentiste et l'estimation MAP partent du même problème central, mais le modifient de manière contrôlée en Ridge ou en Lasso. Chacun de ces cadres révèle une facette que les autres laissent dans l'ombre.

La géométrie donne l'existence et l'unicité de la projection. La SVD expose la structure spectrale et la sensibilité numérique. L'optimisation ouvre sur la régularisation. Le MLE révèle que toute fonction de perte est la signature implicite d'un modèle d'erreur. Le MAP montre que toute régularisation est l'expression d'un prior sur $\beta$. Gauss-Markov établit que l'estimateur des moindres carrés est optimal — dans la classe linéaire sans gaussianité, dans la classe générale avec gaussianité complexe circulaire et sous hypothèse d'identifiabilité.

Deux directions restent ouvertes. La régression linéaire est un cas particulier des méthodes à noyau — avec le noyau linéaire $k(x, x') = x^*x'$, le cadre RKHS retrouve $\hat\beta$ par le théorème de représentation, et ouvre sur les SVM et les processus gaussiens. C'est aussi le cas limite d'un réseau de neurones sans non-linéarité, où la descente de gradient converge vers $\hat\beta$ — ce qui relie la régression aux questions de convergence et d'optimisation non convexe du deep learning.

La régression linéaire n'est pas un modèle simple qu'on enseigne en introduction faute de mieux. C'est le point où toutes les grandes traditions des mathématiques appliquées se rejoignent — et l'endroit idéal pour comprendre ce que chacune apporte vraiment.

## Points à consolider

Cette note fonctionne comme carte conceptuelle — elle fixe les connexions entre cadres. Les points techniques suivants méritent un traitement plus approfondi pour verrouiller le tout.

**Calcul de Wirtinger.** La dérivation par rapport à $\overline\beta$ reste ici un geste formel. Il faut comprendre pourquoi ce choix est le bon en variables complexes, et vérifier rigoureusement que $\nabla_{\overline\beta}\|y - X\beta\|^2 = -X^*(y - X\beta)$.

**Gaussienne complexe circulaire.** La densité $\mathcal{CN}(0, \sigma^2 I)$ est utilisée sans que ses conventions soient discutées — facteurs $\pi$, rôle de la circularité, écriture de la matrice d'information de Fisher. Ces détails varient selon les sources et méritent d'être fixés une fois pour toutes.

**Rang déficient.** La note mentionne la pseudo-inverse mais ne distingue pas clairement deux objets : l'ensemble des minimiseurs des moindres carrés (qui peut être un sous-espace affine entier), et $X^+y$ comme choix particulier parmi eux — celui de norme minimale.

**Ridge et Lasso en complexe.** Ridge se transpose directement. Lasso est plus délicat :
$\|\beta\|_1 = \sum_i |\beta_i|$ pénalise les modules complexes et non séparément les parties
réelle et imaginaire. La pénalisation reste parcimonieuse, mais sa géométrie est différente
du cas réel : elle sélectionne ou annule des coefficients complexes entiers, avec une
invariance de phase qu'il faut comprendre proprement.

**Borne de Cramér-Rao complexe.** Selon qu'on travaille en variables complexes ou en coordonnées réelles équivalentes, les constantes et la forme de la matrice d'information changent — un point à traiter avec soin avant de conclure à l'efficacité de l'estimateur.