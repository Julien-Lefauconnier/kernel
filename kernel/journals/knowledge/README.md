# Knowledge Kernel

## Purpose
The Knowledge kernel defines **declarative knowledge events**.
It records *that a knowledge-related state existed at a given time*,
without ever encoding meaning, truth, or cognition.

This module is designed to be:
- MIT-licensed
- Domain-agnostic
- Zero-Knowledge Cognitive System (ZKCS) compliant
- Safely embeddable in any stack

---

## Core Concepts

### KnowledgeEvent
A `KnowledgeEvent` is a **pure declaration**:

- An event happened
- At a given time
- Related to knowledge

It **does not** contain:
- facts
- beliefs
- interpretations
- embeddings
- reasoning artifacts

```python
KnowledgeEvent.create(
    source="cognition",
    knowledge_type="cognitive_snapshot",
    user_ref="user-123",
)
```

---

## KnowledgeJournal

An append-only journal storing `KnowledgeEvent` instances.

### Guarantees
- append-only
- immutable events
- no mutation
- no inference
- no aggregation

### API
```python
journal.append(event)
journal.iter_events()
```

---

## Knowledge Port

The `knowledge_port` exposes a single safe entrypoint:

```python
append_knowledge(event)
```

It ensures:
- type safety
- isolation from consumers
- centralized write semantics

---

## Kernel Guarantees

The Knowledge kernel will **never**:
- interpret knowledge
- decide truth
- store content
- reason
- expose internal cognition

It only declares *existence*.

---

## Tests

Covered by unit tests:
- knowledge_event
- knowledge_journal
- knowledge_port

All invariants are enforced structurally.

---

## Relationship to Domain

Domains may:
- generate rich knowledge snapshots
- infer meaning
- reason

The kernel:
- records only that something existed

---

## License

MIT
