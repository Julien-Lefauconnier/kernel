# Signal Kernel

## Purpose
Signals are the lowest-level, strictly declarative facts entering or leaving the kernel.

They represent raw observations with:
- no interpretation
- no policy
- no behavior
- no routing logic

Signals are immutable and time-bound.

## Canonical Signals (Closed World)

The kernel enforces a **closed-world canonical signal registry**.

All `CanonicalSignal` instances MUST:
- reference a registered `CanonicalSignalKey`
- comply with a declared `CanonicalSignalSpec`

This guarantees:
- deterministic interpretation
- cross-system interoperability
- strict validation at construction time

### Domain Separation

Canonical signals are grouped by domains:

| Domain            | Category             | Origin    |
|------------------|----------------------|-----------|
| Timeline         | `TEMPORAL_STATE`     | `timeline`|
| Decision (ARVIS) | `DECISION_STATE`     | `arvis`   |
| Risk (ARVIS)     | `RISK_STATE`         | `arvis`   |
| Validation       | `VALIDATION_STATE`   | `arvis`   |

### Cognitive Vocabulary (ARVIS)

The kernel now embeds a **universal cognitive vocabulary**:

#### Decision
- `decision_emitted`
- `decision_actionable`
- `decision_memory_related`
- `decision_meta`
- `decision_informational`

#### Risk
- `uncertainty_detected`
- `conflict_detected`
- `instability_detected`
- `early_warning_detected`

#### Validation (Gate)
- `gate_allow`
- `gate_require_confirmation`
- `gate_abstain`
- `projection_valid`
- `projection_invalid`

These signals enable interoperability with cognitive systems such as **ARVIS**.


## Core Concepts

### Signal
A Signal is a frozen data structure representing an observation.

Guaranteed invariants:
- `timestamp` is always defined
- signal is immutable
- signal carries no semantics

### SignalJournal
Append-only in-memory journal for signals.

It:
- records signals as-is
- never interprets them
- is globally readable
- can be reset for tests

### Unsafe constructor
`Signal.unsafe()` exists ONLY for:
- tests
- adapters
- external bridges

It does NOT bypass invariants.

## Kernel Guarantees
The kernel will NEVER:
- infer intent from signals
- mutate signals
- drop timestamps
- reorder signals semantically

## Intended Usage
Signals feed higher layers (audit, knowledge, timeline) without coupling.

## License
MIT
