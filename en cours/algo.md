# Méthode de résolution de problèmes algorithmiques

*Protocole dérivé d'une session de travail sur un problème de type "Path Existence Queries" (graphe implicite + requêtes de plus court chemin). L'objectif n'est pas la solution de ce problème, mais les patterns de réflexion réutilisables.*

## Principe directeur

La reconnaissance de patterns est centrale parce que **chaque pattern compresse de la complexité validée par ailleurs** — c'est le rôle des théorèmes en mathématiques, et le mécanisme du chunking chez les maîtres d'échecs (Chase & Simon) : un codage court pour les régularités du domaine. Mais la compression n'est *lossless* que si deux conditions sont remplies :

1. **Le pattern voyage avec son interface** : ses conditions d'applicabilité en font partie intégrante. Le pattern matching superficiel (reconnaître la forme sans vérifier les hypothèses) est le mode d'échec principal.
2. **Le pattern est décompressible** : pouvoir le redériver au besoin (méthode Feynman). Un pattern qu'on ne peut pas reconstruire est un pointeur vers une mémoire qu'on ne possède pas — le jour où le problème dévie du cas canonique, on ne peut pas l'adapter.

## Le protocole (dans l'ordre)

### 1. Contraintes → budget de complexité

Lire les bornes de l'énoncé **avant** de chercher une reformulation, et estimer la complexité de l'approche naïve *contre ces bornes*. Nommer explicitement le facteur qui explose (ex. le produit `n · q ≈ 10^10`), pas juste sentir que "ça explose".

Le budget ainsi obtenu (ex. précalcul `O(n log n)` + `O(log n)` par requête) **filtre** les reformulations candidates à l'étape suivante : inutile d'explorer des pistes incompatibles avec le budget.

### 2. Reformulation → structure cachée

Chercher si le problème se reformule dans un contexte plus simple où des patterns de résolution connus apparaissent. Question systématique : *quelle est la structure qui rend ce problème plus facile qu'il n'en a l'air ?*

Réflexes types :
- Graphe implicite défini par une condition numérique (seuil, parité, divisibilité) → **est-ce que trier révèle une structure ?** (ex. composantes connexes → intervalles contigus après tri)
- "Existe-t-il un chemin ?" → connectivité → Union-Find. "Chemin minimal ?" → il faut compter, autre famille d'outils.
- Nommer la réduction explicitement ("c'est Jump Game II") : cela importe d'un coup toute la connaissance associée (algorithme, preuve, pièges).

### 3. Vérifier l'interface de chaque pattern

Pour chaque pattern invoqué, connaître ses conditions d'applicabilité et **les vérifier, pas les supposer**.

Exemples d'interfaces :
- Glouton "saut maximal" (Jump Game II) : valide seulement si la portée atteignable est *monotone* en la position de départ. Un glouton sans propriété de domination identifiée est un pari, pas un algorithme.
- Binary lifting : le saut élémentaire doit être une **fonction déterministe de la position seule** (requête-indépendant). Les paramètres spécifiques à la requête se réintroduisent au moment de la composition.

### 4. Sémantique des variables

Pour chaque variable, expliciter son rôle dans l'algorithme abstrait : fixe ou mobile ? état ou borne ? requête-dépendante ou précalculable ?

- Si une variable "bouge" alors que son rôle est fixe → du code est en trop (ex. une fonction qui "recalcule" une cible qui n'a pas à changer).
- Cette étape trouve le **code en trop** (défauts de conception), là où les cas limites (étape 5) trouvent les **bugs** (défauts de comportement).
- Quand une pièce de code résiste à la compréhension, remonter au rôle sémantique plutôt que raisonner ligne à ligne.

### 5. Cas limites → exemples adverses minimaux

Pour chaque boucle, identifier les cas limites et les **dérouler à la main** sur des exemples construits exprès (3 éléments suffisent presque toujours). Classes de bugs récurrentes à tester systématiquement :

| Classe | Exemple adverse | Symptôme typique |
|---|---|---|
| Mapping ambigu (doublons) | Deux nœuds de même valeur | `.index()` sur valeurs → collision ; utiliser des **permutations d'indices** (bijections par construction) |
| Invariants d'entrée non garantis | Requête inversée `(r, l)` | Boucle qui suppose `l ≤ r` sans que rien ne le garantisse ; le fix (swap) doit être *justifié* (ex. graphe non orienté) |
| Mises à jour couplées | `l = f(l,r); r = g(l,r)` | Le second appel utilise le `l` déjà modifié |
| Recherche binaire qui stagne | `r == l+1` | `i = (l+r)//2 = l` puis `l = i` → boucle infinie ; pattern robuste : candidat mémorisé séparément + progression stricte (`lo = i+1`) |
| Condition au seuil | `target == sorted_nums[i]` exactement | `<` vs `<=` : tester l'égalité exacte |
| Requête identité | `query[0] == query[1]` | Vérifier que la réponse attendue (souvent 0) tombe naturellement |

### 6. Accélération par précalcul

Quand la boucle correcte est trop lente : si l'opération itérée est une fonction déterministe de la position seule, précalculer ses itérées par puissances de 2 :

$$\text{up}[k][i] = \text{up}[k-1]\big[\text{up}[k-1][i]\big]$$

et composer n'importe quel nombre de sauts en $O(\log n)$. Même machinerie que le LCA par binary lifting ou l'exponentiation rapide : **transformer une itération linéaire en composition logarithmique, au prix d'un précalcul $O(n \log n)$**.

Le diagnostic du besoin d'accélération passe par un **cas adversarial construit exprès** (ex. `maxDiff` minimal + valeurs espacées + requête traversant tout le tableau → `O(n)` itérations par requête).

## Checklist condensée

1. **Budget** : bornes de l'énoncé → complexité cible, *avant* de coder. Nommer le facteur qui explose.
2. **Structure** : la relation entre entités cache-t-elle un ordre qui simplifie (tri → intervalles) ?
3. **Réduction nommée** : identifier le problème connu sous-jacent, *et vérifier l'hypothèse qui rend sa solution valide*.
4. **Rôles sémantiques** : fixe/mobile, état/borne, précalculable/requête-dépendant. Une variable au rôle flou = code suspect.
5. **Bijections, pas valeurs** : tout mapping indice ↔ position passe par des permutations, jamais par `.index()` sur des valeurs.
6. **Exemples adverses minimaux** : un cas de 3 éléments par classe de bug (doublons, égalité au seuil, `r == l+1`, requête inversée, requête identité).
7. **Précalcul logarithmique** : itération d'une fonction déterministe de la position → binary lifting.