# Timeline Kernel

## Purpose

The **Timeline Kernel** provides a **pure, deterministic, zero-knowledge timeline projection layer**.
It is designed to be **portable, auditable, and reusable** across systems.

The kernel exposes **no business logic**, **no inference**, and **no interpretation**.
It only guarantees **structural and temporal correctness**.

---

## Core Principles

The Timeline Kernel:

- ❌ Does **not** infer intent
- ❌ Does **not** interpret meaning
- ❌ Does **not** enrich or mutate events
- ❌ Does **not** assume domain semantics

It **only**:
- ✅ Preserves temporal ordering
- ✅ Projects kernel facts into timeline entries
- ✅ Enforces hard invariants
- ✅ Remains deterministic and stateless

---

## Architecture Overview

```
kernel/
├── invariants/
│   └── timeline/
│       └── timeline_invariants.py
├── journals/
│   └── timeline/
│       ├── timeline_entry.py
│       ├── timeline_journal.py
│       ├── timeline_reader.py
│       ├── timeline_projector.py
│       ├── timeline_query.py
│       ├── timeline_slice.py
│       ├── timeline_summary.py
│       ├── timeline_view.py
│       └── ...
├── ports/
│   └── timeline_port.py
└── tests/
    └── test_timeline_*_kernel.py
```

---

## Timeline Invariants (Hard Guarantees)

Defined in `timeline_invariants.py`:

1. **Timestamp Presence**
   - Every `TimelineEntry` MUST have a non-null timestamp.

2. **Monotonic Append**
   - Timeline entries MUST be appended in non-decreasing temporal order.

3. **Immutability**
   - Entries are immutable once created (structurally enforced).

These invariants are **normative guarantees** of the kernel.

---

## TimelineProjector

### What it is

A **pure projection utility** that converts kernel facts into timeline entries.

- Stateless
- Deterministic
- Optional
- Replaceable by consumers

### What it does

- Accepts **unordered kernel events**
- Sorts them by canonical timestamp
- Emits `TimelineEntry` objects

### What it does NOT do

- ❌ Infer causality
- ❌ Enforce business semantics
- ❌ Modify input events
- ❌ Persist data

---

## Supported Kernel Events

The default projector supports:

- `ActionEvent`
- `ActionValidationEvent`
- `KnowledgeEvent`

Each event is mapped to a **structural timeline entry** only.

---

## Determinism & Zero-Knowledge

Given the same input events:

- Output is **always identical**
- No external state is accessed
- No hidden knowledge is introduced

This makes the Timeline Kernel:
- Auditable
- Replayable
- Safe for distributed systems

---

## Testing Strategy

The kernel includes **exhaustive tests** validating:

- Sorting behavior
- Cursor logic
- Query slicing
- View building
- Invariant enforcement
- Reader & projector behavior

All tests must pass for any kernel release.

---

## Usage Contract

The Timeline Kernel guarantees:

- Structural correctness
- Temporal ordering
- No semantic coupling

Consumers are responsible for:
- Interpretation
- Presentation
- Business meaning
- UI / UX concerns

---

## Status

✅ **Timeline Kernel: COMPLETE & STABLE**

Future kernel extractions (Audit, Knowledge, Signals) will follow the same model.

---

## License

MIT — free to use, modify, and embed.
