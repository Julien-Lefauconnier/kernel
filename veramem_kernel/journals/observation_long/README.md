# Observation Long Journal (Kernel)

Observation Long is the kernel subsystem for immutable longitudinal traces.

## Contract

- Append-only truth
- Declarative payload only
- Payload must be JSON-safe (`Mapping[str, Any]`)
- No inference
- No aggregation
- No projection inside kernel

## Purpose

ObservationLong captures durable traces such as:

- governance snapshots
- cognitive exposure markers
- normative longitudinal signals

Kernel does not interpret them.

Domain projections are external.

## Guarantees

- deterministic replay
- auditable event history
- ZKCS compatible
- ARVIS compliant
