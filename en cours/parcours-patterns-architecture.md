# Parcours "Patterns d'Architecture" — version révisée

Parcours construit autour des leçons *Software Architecture Monday* de Mark Richards (developertoarchitect.com/lessons), révisé après vérification partielle sur le site.

**Légende :**
- ✓ = numéro et titre confirmés sur le site (index consulté, à jour jusqu'à la leçon 214, décembre 2025)
- ? = plausible mais non confirmé — vérifier le titre exact sur la page avant de cocher
- Les leçons ≥ 215 datent de 2026 et n'ont pas pu être confirmées : traiter les titres comme indicatifs.

---

## Colonne vertébrale recommandée (changement par rapport à la v1)

Les vidéos de 10 minutes donnent la largeur, pas la profondeur. Texte principal suggéré, du même auteur :

1. **_Software Architecture Patterns_, 2e éd.** (Mark Richards, O'Reilly, 2022) — court, couvre les styles majeurs avec trade-offs systématisés. À lire en premier ; il remplace avantageusement le bloc 1 comme source primaire.
2. **_Fundamentals of Software Architecture_, 2e éd.** (Richards & Ford, O'Reilly, avril 2025) — la référence complète, si tu veux aller au fond.

Les leçons vidéo deviennent alors des **compléments ciblés par pattern** : après un chapitre, regarde la leçon correspondante pour l'angle "terrain" de Richards.

---

## 0. Cadrage

- [ ] **Leçon 6** — Classifying Architecture Patterns ?

## 1. Styles d'architecture majeurs

Série existante sur le site, mais numéros exacts non confirmés — vérifier sur la page catégorie avant usage. Couvert intégralement par *Software Architecture Patterns* 2e éd.

- [ ] **Leçon 158** — Layered Architecture ?
- [ ] **Leçon 159** — Modular Monolith Architecture ?
- [ ] **Leçon 160** — Microkernel Architecture ?
- [ ] **Leçon 161** — Agility and Monolithic Architectures ?
- [ ] **Leçon 162** — Microservices Architecture ?
- [ ] **Leçon 163** — Service-Based Architecture ?
- [ ] **Leçon 164** — Service-Oriented Architecture (SOA) ?
- [ ] **Leçon 165** — Event-Driven Architecture ?
- [ ] **Leçon 166** — Space-Based Architecture ?
- [ ] **Leçon 196** — Modularity and Architectural Styles ?

## 2. Patterns d'intégration classiques

- [ ] **Leçon 19** — File Transfer ?
- [ ] **Leçon 20** — Shared Database ?
- [ ] **Leçon 21** — RPC ?
- [ ] **Leçon 22** — Messaging ?
- [ ] **Leçon 39** — ESB (Enterprise Service Bus) ?
- [ ] **Leçon 40** — Common Integration Patterns ?

## 3. Patterns tactiques microservices

- [ ] **Leçon 43** — Microservices Orchestration Pattern ?
- [ ] **Leçon 44** — Microservices Aggregation Pattern ?
- [ ] **Leçon 45** — Microservices Gateway Pattern ?
- [ ] **Leçon 46** — Reactive Architecture Patterns Introduction ✓
- [ ] **Leçon 47** — Channel Monitoring Pattern ✓
- [ ] **Leçon 48** — Thread Delegate Pattern ✓

## 4. Patterns nommés isolés (ordre chronologique)

- [ ] **Leçon 27** — Circuit Breaker Pattern ✓
- [ ] **Leçon 28** — Service Design Patterns ?
- [ ] **Leçon 35** — Watch Notification Pattern ✓
- [ ] **Leçon 53** — Distributed Transactions Using Sagas ✓ *(ajout : confirmée sur le site, très pertinente pour les patterns distribués)*
- [ ] **Leçon 56** — The Ambulance Pattern ?
- [ ] **Leçon 72** — Multi-Broker Pattern ?
- [ ] **Leçon 81** — Workflow Event Pattern ?
- [ ] **Leçon 148** — Compensating Updates ?
- [ ] **Leçon 171** — Producer Control Flow Pattern ?
- [ ] **Leçon 175** — Events vs. Messages ✓ *(ajout : confirmée, distinction fondamentale pour tout le bloc event-driven)*
- [ ] **Leçon 176** — Compensating Updates (révision) ?
- [ ] **Leçon 178** — Multi-Broker Pattern (révision) ?
- [ ] **Leçon 197** — Communication Patterns ?
- [ ] **Leçons 215-219** — titres non vérifiables (2026) : consulter la page pour les leçons récentes ?

## 5. Anti-patterns (en dernier)

- [ ] **Leçon 74** — Elephant Migration AntiPattern ?
- [ ] **Leçon 113** — Cart Before The Horse Anti-Pattern ?
- [ ] **Leçon 117** — Accidental Complexity AntiPattern ?
- [ ] **Leçon 130** — The Frozen Caveman AntiPattern ?
- [ ] **Leçon 132** — Architecture by Implication AntiPattern ?
- [ ] **Leçon 133** — Stovepipe Architecture AntiPattern ?
- [ ] **Leçon 146** — The Out-of-Context Scorecard AntiPattern ?
- [ ] **Leçon 155** — The Infinity Architecture AntiPattern ?
- [ ] **Leçon 198** — The Swarm of Gnats Event AntiPattern ?
- [ ] **Leçon 214** — Microservice All The Things Pitfall ✓

---

## Méthode de travail

1. Lire d'abord le chapitre correspondant dans *Software Architecture Patterns* (styles) ou aborder le pattern via la vidéo (patterns tactiques/isolés).
2. Après chaque leçon, noter en 3-5 lignes : problème résolu, trade-off principal, exemple déjà croisé.
3. Ne pas sauter les paires original/révision (72→178, 148→176) : elles montrent l'évolution de la pensée de Richards.
4. À la première visite de la page, corriger les numéros marqués "?" directement dans ce fichier.

*Note de fiabilité : les fetchs directs de la page ayant échoué lors de la construction de la v1, une partie des numéros provient de mémoire de modèle et non de la page elle-même. Les six leçons marquées ✓ ont été confirmées par recherche web ; le reste est à valider par toi à la première consultation. Rythme de publication : hebdomadaire à l'origine (2018), ~mensuel aujourd'hui.*
