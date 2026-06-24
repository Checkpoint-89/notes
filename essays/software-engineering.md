# Manifesto for Intelligible Software Engineering

Un bon logiciel n'est pas seulement un système qui fonctionne.
C'est un système dont le comportement est intelligible et le reste quand il change.

Un système bien conçu ne dit pas seulement ce qu'il fait.
Il délimite un domaine admissible : les états valides, les comportements acceptables et les violations à détecter.

Les invariants ne sont pas des détails d'implémentation.
Les règles métier, les contrats d'interface, la cohérence des données et les contraintes techniques sont les points d'appui du système.
Ils doivent être identifiés, nommés et préservés.

Une abstraction juste ne cache pas le désordre : elle le supprime parce que le problème a été réellement compris.

La complexité essentielle appartient au problème : il faut l'encadrer.
La complexité accidentelle vient de nos choix : il faut l'éliminer.

Un module qui ne peut pas être compris ou testé isolément a une frontière mal dessinée.
Les dépendances doivent être nécessaires, explicites et limitées.

Quand le langage du code, du métier et de la documentation diverge, le modèle se fragilise.

Les patterns servent à ne pas réinventer ce qui a déjà été résolu.
Un choix de design est un trade-off, pas une vérité.

Un bon design rend le changement local, compréhensible et vérifiable.
Un mauvais design diffuse les effets d'une modification bien au-delà de son intention.

Le but n'est pas de produire plus vite à tout prix.
Le but est de construire des systèmes que l'on peut comprendre, discuter, corriger et faire évoluer sans perdre leur sens.
