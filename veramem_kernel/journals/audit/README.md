# Audit Kernel — README

## Purpose

The **Audit Kernel** provides a minimal, append-only, immutable journal of auditable facts.

It exists to **declare that something happened**, nothing more.

The audit kernel is designed to be:
- portable
- dependency-free
- legally and technically safe
- usable outside of Veramem

It is licensed under **MIT** and intended for public use.

---

## What the Audit Kernel IS

- A **fact registry**
- A **structural memory**
- An **append-only log**
- A **compliance-friendly substrate**

Each `AuditEvent` declares:
- *when* something happened
- *what type* of event occurred
- *where it originated from*

---

## What the Audit Kernel is NOT

The audit kernel will **NEVER**:
- interpret events
- infer intent
- enrich metadata
- correlate events
- reorder events
- perform aggregation
- mutate events after creation

Any meaning belongs to **higher layers**.

---

## Core Components

### `AuditEvent`

```python
AuditEvent(
    event_id: str,
    created_at: datetime,
    source: str,
    source_id: str,
    event_type: str,
    metadata: Optional[Mapping[str, str]]
)
```

Properties:
- Immutable (`@dataclass(frozen=True)`)
- Opaque metadata
- Kernel-level primitive

Creation helper:
```python
AuditEvent.create(...)
```

---

### `AuditJournal`

```python
AuditJournal.append(event)
AuditJournal.iter_events()
```

Guarantees:
- Append-only
- In-order storage
- No mutation
- No interpretation

---

## Kernel Invariants

The following invariants are **hard guarantees**:

- Every audit event has a timestamp
- Every audit event has a stable identity
- Audit events are immutable
- Only `AuditEvent` instances are accepted

Violations raise **immediate errors**.

---

## Domain → Kernel Integration

The kernel is **not aware of domains**.

Typical integration uses a *shadow write* pattern:

```
Domain Event → Domain Adapter → AuditEvent → AuditJournal
```

Failures in the kernel **must never break domain behavior**.

---

## Zero-Knowledge Compliance

The audit kernel:
- stores no semantic payloads
- does not inspect metadata
- does not derive knowledge
- does not couple with cognition

This makes it compatible with:
- ZK architectures
- compliance logging
- legal audit trails
- regulated environments

---

## Extensibility

Consumers MAY:
- add their own adapters
- project audit events into views
- persist journals externally

Consumers MUST NOT:
- mutate kernel events
- overload kernel meaning
- bypass invariants

---

## Status

✅ Extracted from Veramem  
✅ Fully tested  
✅ Kernel-grade  
✅ Stable API surface  

---

## License

MIT License — free for use, modification, and distribution.
