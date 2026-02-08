# Signal Lineage Contract

This document defines the normative contract governing Signal Lineage in the kernel.

A Signal Lineage expresses the structural and temporal relationships between canonical signals, without semantic interpretation.

A lineage is considered valid if and only if all invariants defined in this document are satisfied.

## 1. Definition

A Signal Lineage Node represents a canonical signal emission, optionally linked to:

- zero or more parent signals
- at most one superseded signal

Lineage information is declarative, immutable, and evaluated
against the timeline journal.

## 2. Structural Invariants

The following structural rules MUST be enforced:

- A signal MUST NOT list itself as a parent
- All parent signals MUST be registered in the Canonical Signal Registry
- If `supersedes` is defined:
  - the superseded signal MUST be registered
  - the superseded signal MUST be included in `parents`

## 3. Specification-Level Invariants

A signal MAY define `supersedes` only if its `CanonicalSignalSpec.supersession_allowed` flag is set to `True`

## 4. Temporal Invariants

All temporal invariants are evaluated against the timeline journal.

- All parent signals MUST have been emitted strictly before the child signal
- A superseded signal MUST have been emitted strictly before the superseding signal
- A superseded signal MUST have been emitted at least once

## 5. Graph Invariants

The signal lineage graph MUST be acyclic.

Cycles are forbidden in all forms, including:

- direct cycles
- indirect cycles
- long cycles
- cycles involving `supersedes`

Supersedes relationships are treated as parents for the purpose of cycle detection.

## 6. Validation

The normative reference for lineage validation is:

"assert_signal_lineage_invariants(node, known_nodes)"

If this function does not raise an error, the lineage is guaranteed to satisfy all invariants defined in this contract.

## 7. Guarantees

A valid Signal Lineage is guaranteed to be:

- structurally ordered (no semantic causality)
- temporally consistent
- acyclic
- replayable
- auditable
- fork-safe
- zero-knowledge compatible
- distributable without global state

## 8. Scope

This contract defines what must hold, not how it is implemented.

Any implementation respecting these invariants is considered Signal Lineage–compatible with this kernel.
