# Signal Lineage Graph

```mermaid
graph TD

S1[Signal A]
S2[Signal B]
S3[Derived Signal]
S4[Superseding Signal]

S1 --> S3
S2 --> S3
S3 --> S4
```

---

## Purpose

Signal lineage provides:

* traceable cognitive evolution,
* deterministic resolution,
* structural explainability.

---

## Key Properties

* Directed acyclic graph.
* Deterministic parent ordering.
* Non-destructive supersession.
* Stability under forks.
