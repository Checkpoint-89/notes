# Lemme de factorisation de Doob — Démonstration

## Énoncé

Soient $f : \Omega \to (E, \mathcal{E})$ une application et $g : \Omega \to \mathbb{R}$. Alors $g$ est $\sigma(f)$-mesurable si et seulement s'il existe $\varphi : (E, \mathcal{E}) \to (\mathbb{R}, \mathcal{B}(\mathbb{R}))$ mesurable telle que $g = \varphi \circ f$.

## Sens facile (⟸)

Si $g = \varphi \circ f$, alors pour tout $B \in \mathcal{B}(\mathbb{R})$ :

$$g^{-1}(B) = (\varphi \circ f)^{-1}(B) = f^{-1}(\varphi^{-1}(B)).$$

Comme $\varphi$ est mesurable, $\varphi^{-1}(B) \in \mathcal{E}$, donc $f^{-1}(\varphi^{-1}(B)) \in \sigma(f)$. Ainsi $g$ est $\sigma(f)$-mesurable.

## Sens difficile (⟹) — La machine standard

On suppose $g$ mesurable par rapport à $\sigma(f)$ et on construit $\varphi$.

La structure de la preuve est la suivante : on traite d'abord les fonctions les plus simples (indicatrices), puis on remonte par linéarité et par passage à la limite croissante. C'est la **machine standard** — elle réapparaît dans toute la théorie de la mesure (théorèmes de transfert, Fubini, etc.).

### Étape 1 — Indicatrices

Soit $g = \mathbf{1}_A$ avec $A \in \sigma(f)$. Par définition de $\sigma(f) = f^{-1}(\mathcal{E})$, il existe $B \in \mathcal{E}$ tel que $A = f^{-1}(B)$. Alors :

$$g(\omega) = \mathbf{1}_A(\omega) = \mathbf{1}_B(f(\omega)) = (\mathbf{1}_B \circ f)(\omega).$$

On pose $\varphi = \mathbf{1}_B \in \mathcal{E}$.

### Étape 2 — Fonctions étagées positives

Soit $g = \sum_{i=1}^n a_i \mathbf{1}_{A_i} \geq 0$ où les $A_i = g^{-1}(\{a_i\}) \in \sigma(f)$ forment une partition de $\Omega$. Chaque $A_i = f^{-1}(B_i)$ pour un certain $B_i \in \mathcal{E}$.

Les $A_i$ étant disjoints, si $y \in B_i \cap B_j$ pour $i \neq j$, alors $f^{-1}(\{y\}) \subset A_i \cap A_j = \emptyset$, donc $y \notin f(\Omega)$. On peut rendre les $B_i$ disjoints sans changer leurs préimages : poser $B_i' = B_i \setminus \bigcup_{j < i} B_j$ donne $f^{-1}(B_i') = A_i$ et les $B_i'$ sont dans $\mathcal{E}$, disjoints.

On pose $\varphi = \sum_{i=1}^n a_i \mathbf{1}_{B_i'}$, qui vérifie $g = \varphi \circ f$.

### Étape 3 — Fonctions positives quelconques

Soit $g \geq 0$ mesurable par rapport à $\sigma(f)$. Toute fonction mesurable positive est limite croissante de fonctions étagées positives ; on choisit $(g_n)$ avec $g_n \uparrow g$, chaque $g_n$ étant $\sigma(f)$-mesurable.

Par l'étape 2, il existe $\varphi_n$ mesurable telle que $g_n = \varphi_n \circ f$. On pose :

$$\varphi(y) = \limsup_{n \to \infty} \varphi_n(y).$$

La $\limsup$ d'une suite de fonctions mesurables est mesurable, donc $\varphi$ est $\mathcal{E}$-mesurable. Pour tout $\omega$ :

$$(\varphi \circ f)(\omega) = \limsup_n \varphi_n(f(\omega)) = \limsup_n g_n(\omega) = g(\omega)$$

puisque la suite $g_n(\omega) \uparrow g(\omega)$ converge.

### Étape 4 — Cas général

Décomposer $g = g^+ - g^-$ où $g^+ = \max(g,0)$ et $g^- = \max(-g,0)$ sont $\sigma(f)$-mesurables positives. Par l'étape 3, $g^+ = \varphi^+ \circ f$ et $g^- = \varphi^- \circ f$. On pose $\varphi = \varphi^+ - \varphi^-$.

## Observation clé — Compatibilité avec les fibres

La preuve révèle une structure fondamentale : $g$ est $\sigma(f)$-mesurable **si et seulement si** $g$ est constante sur les fibres de $f$, c'est-à-dire :

$$f(\omega_1) = f(\omega_2) \implies g(\omega_1) = g(\omega_2).$$

C'est exactement la condition pour qu'il existe une fonction $\varphi$ quelconque telle que $g = \varphi \circ f$. L'apport du lemme est que la mesurabilité de $g$ entraîne celle de $\varphi$.

Intuitivement : $f$ partitionne $\Omega$ en fibres $f^{-1}(\{y\})$. Une quantité $g$ est « calculable à partir de $f$ » exactement quand elle ne distingue pas les points d'une même fibre.

## La machine standard en résumé

La même structure en quatre étapes — indicatrices → étagées → positives → général — sert à démontrer quasi-systématiquement les résultats intégraux :

| Résultat | Ce qu'on vérifie d'abord |
|---|---|
| Lemme de Doob | $g = \mathbf{1}_A$, $A \in \sigma(f)$ |
| Théorème de transfert $\int g \, d(f_*\mu) = \int g \circ f \, d\mu$ | $g = \mathbf{1}_B$, $B \in \mathcal{E}$ |
| Théorème de Fubini | $g = \mathbf{1}_{A \times B}$, $A \in \mathcal{A}$, $B \in \mathcal{B}$ |

Le fil conducteur est toujours le même : vérifier la propriété sur une famille génératrice simple, stabilité par linéarité (étagées), puis par passage à la limite monotone (Beppo-Levi) pour couvrir toutes les fonctions mesurables positives, puis signe pour le cas général.
