# Timeline — Journalisation factuelle, gouvernée et lisible (ZKCS / ARVIS)

Le module `timeline` définit **comment Veramem expose l’activité observable du système**
à des fins de **transparence, d’audit et de gouvernance humaine**,
**sans jamais exposer de raisonnement interne, de contenu utilisateur ou de données sensibles**.

Ce document décrit **l’état réel et actuel** de la Timeline tel qu’implémenté aujourd’hui, ainsi que son **cadre contractuel** a

---

## 🎯 Principe fondamental

> La Timeline n’explique pas comment le système pense.  
> Elle expose **ce qui est observable**, **quand**, et **sous quelle forme déclarative**.

La Timeline est :

- une **trace**, pas une explication,
- un **miroir factuel**, pas un narrateur,
- un **support de gouvernance**, pas un moteur de décision.

Toute narration, interprétation ou causalité est **hors de son périmètre**.

---

## 🧠 Rôle réel de la Timeline (état actuel)

La Timeline n’est plus un simple journal technique.

Elle constitue aujourd’hui :

- une **trace factuelle immuable** des événements observables,
- un **miroir déclaratif** d’états système et cognitifs (post-cognitifs),
- un **socle de gouvernance humaine** et d’audit,
- une **surface ZKCS vérifiable**, strictement non interprétative.

👉 La Timeline est **passive**, **non prescriptive**, mais **centrale** dans l’architecture Veramem.

---

## 🧩 Nature des entrées de Timeline

Chaque entrée de Timeline est :

- déclarative
- non exécutable
- non actionnable
- immuable
- indépendante du contenu utilisateur

La Timeline distingue explicitement deux **natures sémantiques**.

### 🔹 EVENT — Événement factuel

Un fait ponctuel observable, survenu à un instant précis.

Exemples :
- action proposée / validée / refusée
- accès ou modification d’un document
- feedback humain explicite

Un EVENT **décrit ce qui s’est produit**, sans en déduire causes ou conséquences.

---

### 🔹 STATE — État déclaratif

Un instantané lisible d’un état système ou cognitif.

Exemples :
- introspection système
- état de compréhension
- état de mémoire long terme
- présence d’une décision humaine (gouvernance)

Un STATE :
- n’implique aucune causalité
- ne déclenche aucune action
- ne prescrit aucun comportement

---

## ⏱️ Invariant temporel

Chaque entrée de Timeline :

- possède **obligatoirement** un timestamp
- est comparable chronologiquement
- peut être ordonnée de manière déterministe

📌 L’ordre temporel **n’implique aucune causalité**.

---

## 📐 Propriétés invariantes

### 1️⃣ Neutralité sémantique

La Timeline :
- ne juge pas
- ne recommande pas
- ne corrige pas
- n’explique pas

Elle **expose des faits et des états**, elle **n’interprète jamais**.

---

### 2️⃣ Zéro contenu utilisateur

Aucune entrée de Timeline ne contient :

- texte utilisateur
- prompts ou réponses générées
- fichiers
- embeddings
- raisonnements intermédiaires

Uniquement :
- des types déclaratifs
- des métadonnées minimales
- des états abstraits
- des références de traçabilité

---

### 3️⃣ Non-actionnabilité stricte

Une entrée de Timeline :

- ne déclenche aucune action
- ne modifie aucun état
- n’est jamais rejouée
- n’est jamais interprétée automatiquement

La Timeline est **passive par conception**.

---

## 🧭 Timeline canonique vs Timeline Views

la Timeline est explicitement **structurée en deux niveaux**.

### Timeline canonique (`/timeline`)

- exhaustive
- factuelle
- non filtrée
- orientée système
- **source unique de vérité**

Elle expose *tout ce qui est observable*.

---

### Timeline Views (`/timeline/views`)

- projections **déclaratives** de lecture
- filtrées par **rôle explicite**
- orientées audit, UI et gouvernance
- **post-cognitives par construction**

Les Views :
- ne modifient jamais la timeline canonique
- ne produisent aucune cognition
- n’interprètent jamais les données

👉 Voir `timeline/views/README.md` pour le contrat détaillé.

---

## 🧭 Rôles simultanés assumés

La Timeline remplit aujourd’hui plusieurs rôles **distincts mais non confondus** :

1️⃣ **Trace factuelle** — ce qui s’est produit  
2️⃣ **Awareness & lisibilité humaine** — ce qui est observable  
3️⃣ **Support de gouvernance** — ce qui peut être audité

👉 Ces rôles sont **explicitement séparés via les Timeline Views**.

---

## ⚖️ Gouvernance et accès

- la Timeline canonique est **interne**
- les Timeline Views sont **exposées via une gouvernance déclarative**
- l’accès dépend **uniquement du rôle de la view**, jamais de logique implicite

Aucune Timeline View :
- n’est utilisée comme entrée décisionnelle
- n’automatise une décision

---

## 🔐 Garanties Zero-Knowledge (ZKCS)

La Timeline garantit strictement :

- ❌ aucune chaîne de pensée
- ❌ aucun raisonnement sérialisé
- ❌ aucun contenu utilisateur
- ❌ aucune reconstruction implicite
- ❌ aucune inférence cachée

Chaque entrée est :
- autonome
- minimale
- explicite
- vérifiable

---

## 🏗️ Architecture réelle

Le module `timeline` fournit :

- des entrées immuables (`TimelineEntry`)
- une taxonomie déclarative (`TimelineEntryType`)
- un builder stateless (`TimelineBuilder`)
- des projections publiques (DTO)
- des résumés factuels (`TimelineSummary`)
- des **Timeline Views gouvernées** (`TimelineView`)

Il ne fournit :
- aucune logique métier
- aucune analyse
- aucune interprétation
- aucune narration

---

## 🚦 Phases couvertes

 — Clarification sémantique & invariants
 — Timeline Views (domaine)
 — API Timeline Views
 — Gouvernance d’accès

👉 L’ensemble est **implémenté, testé et verrouillé**.

---

## 🧠 Philosophie ARVIS

- Transparence ≠ exposition
- Traçabilité ≠ surveillance
- Gouvernance ≠ automatisation
- Lisibilité ≠ interprétation

La Timeline est un **miroir factuel gouvernable**, pas un narrateur.

> *Ce que Veramem fait est traçable.*  
> *Ce que Veramem pense reste privé.*



---

## 🔗 Relation avec les autres modules

### Cognition

La Timeline peut exposer :
- conflits cognitifs
- gaps de raisonnement
- intentions déclaratives
- états de connaissance ou d’incertitude

Elle ne :
- reproduit pas la cognition
- n’enregistre pas le raisonnement
- n’en déduit rien

---

### Action

La Timeline reflète :
- les actions proposées
- les décisions utilisateur
- les refus explicites

Elle ne :
- déclenche aucune action
- automatise aucune décision
- modifie aucun workflow

---

### Gouvernance & Control Center

La Timeline est une **source passive** pour :
- l’audit
- la gouvernance
- l’explicabilité
- la supervision humaine

Elle ne constitue **jamais une autorité décisionnelle**.

---

## 🔐 Garanties Zero-Knowledge (ZKCS)

La Timeline garantit strictement :

- ❌ aucune chaîne de pensée
- ❌ aucun raisonnement sérialisé
- ❌ aucun contenu utilisateur
- ❌ aucune reconstruction implicite
- ❌ aucune inférence cachée

Chaque entrée est :
- autonome
- minimale
- explicite
- vérifiable

---

## 🧭 Philosophie de conception (ARVIS)

- Transparence ≠ exposition
- Traçabilité ≠ surveillance
- Audit ≠ contrôle
- Historique ≠ mémoire sémantique
- Observation ≠ interprétation

La Timeline est **un miroir factuel**, pas un narrateur.

---

## 🚧 Portée actuelle

Le module fournit :

- des structures d’entrées immuables
- un builder stateless
- des règles d’ordonnancement
- une intégration passive avec cognition, action et gouvernance

Il ne fournit :

- aucune logique métier
- aucune analyse
- aucune interprétation
- aucune narration

---

## 🔮 Extensions futures (non engageantes)

Potentiels usages futurs :

- vues utilisateur dérivées
- résumés narratifs (hors Timeline)
- exports réglementaires
- audits multi-acteurs
- visualisations externes

Toute extension :
- est **hors du contrat Timeline**
- repose sur des couches supérieures
- ne modifie pas les invariants

---

## 🧠 Résumé

La Timeline est :

- la mémoire temporelle factuelle de Veramem
- la trace observable de son activité
- le socle de la transparence ZKCS
- un pilier de gouvernance ARVIS

Elle montre **ce qui est observable**,  
sans jamais révéler **ce qui est pensé**.

> *Ce que Veramem fait est traçable.  
> Ce que Veramem pense reste privé.*
