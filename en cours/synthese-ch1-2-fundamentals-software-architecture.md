# Synthèse — Chapitres 1-2, *Fundamentals of Software Architecture* (Richards & Ford)

## 0) Chaîne de conception (itérative)

(a) caractéristiques + (b) composants logiques (entités, workflows) → (c) style d'architecture → (d) décisions architecturales, avec boucle possible de (c) vers (b) si un workflow s'avère incompatible avec les caractéristiques visées.

## 1) Critères de décision architecturale

- caractère **stratégique vs. tactique**
- **effort de changement**
- **importance des trade-offs**

## 2) Les trois lois de l'architecture logicielle

| Loi | Énoncé | Portée |
|---|---|---|
| **Loi 1** | Tout est trade-off | Il n'y a pas de solution architecturale supérieure dans l'absolu, seulement des compromis à peser selon le contexte |
| **Loi 2** | *Why* > *how* | Face à une architecture existante, comprendre son fonctionnement est relativement mécanique ; comprendre pourquoi elle a été construite ainsi est le vrai défi — d'où l'intérêt de documenter les décisions (ADR, chapitre 21) |
| **Loi 3** | Spectre, pas binaire | Les décisions architecturales se situent rarement entre deux options nettes ; elles occupent un continuum entre deux extrêmes |

## 3) Connaissance breadth-first

L'architecte doit privilégier une connaissance **large** plutôt que **profonde** — contrairement au développeur, qui vise l'expertise verticale.

## 4) Rester technique par la pratique

Sans se placer sur le chemin critique de l'équipe de développement : bugs, features secondaires, outillage pour l'équipe, POC pouvant enrichir la bibliothèque de modèles de l'organisation
