# Signal Kernel

## Purpose
Signals are the lowest-level, strictly declarative facts entering or leaving the kernel.

They represent raw observations with:
- no interpretation
- no policy
- no behavior
- no routing logic

Signals are immutable and time-bound.

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
