# Veramem Reference Implementation Guide

## 1. Purpose

This document provides guidance for implementing a conformant Veramem system.

Its goals are:

- ensure interoperability,
- preserve security guarantees,
- maintain deterministic behavior,
- facilitate independent implementations.

This guide is normative unless otherwise specified.

---

## 2. Implementation Philosophy

A Veramem implementation must prioritize:

1. Safety over performance,
2. Determinism over convenience,
3. Explicit failure over silent fallback,
4. Long-term stability over short-term optimization.

Implementations must never compromise security properties.

---

## 3. Conformance Requirements

An implementation is considered conformant if it:

- passes all official conformance tests,
- produces identical canonical outputs,
- enforces all invariants,
- rejects invalid or ambiguous inputs.

The reference test suite is located in:

`/conformance`.

---

## 4. Deterministic Behavior

All operations must be:

- deterministic,
- reproducible,
- platform-independent.

This includes:

- sorting,
- encoding,
- hashing,
- merge logic.

Floating-point arithmetic must not be used.

---

## 5. Canonical Encoding

Canonical encoding is mandatory.

Requirements:

- stable ordering,
- domain separation,
- binary encoding.

Implementations must:

- use canonical message formats,
- reject non-canonical inputs.

---

## 6. Timeline Implementation

The timeline must:

- be append-only,
- verify hashchains,
- detect forks,
- enforce invariants.

Snapshots must:

- be reproducible,
- match reference commitments.

---

## 7. Delta and Synchronization

Delta processing must:

- verify base snapshot,
- validate extension,
- reject rollback.

Synchronization must:

- converge only when safe,
- maintain stability otherwise.

---

## 8. Merge Behavior

Merge operations must:

- be deterministic,
- preserve causal ordering,
- reject unsafe merges.

Ambiguity must result in abstention.

---

## 9. Signal Lineage

Signal lineage must:

- detect cycles,
- preserve ancestry,
- enforce structural integrity.

Resolvers must:

- fail fast on incomplete graphs.

---

## 10. Device Attestation

Implementations must support:

- challenge-response,
- replay protection,
- deterministic validation.

Attestation verification must:

- be independent of transport.

---

## 11. Trust Anchors

Trust anchors must be:

- configurable,
- versioned,
- replaceable.

Implementations must:

- support multiple trust domains.

---

## 12. Cryptography

Mandatory:

- HMAC-SHA256,
- domain separation.

Optional:

- hardware-backed keys.

Future compatibility:

- post-quantum algorithms.

---

## 13. Error Handling

Errors must be:

- explicit,
- typed,
- non-ambiguous.

Silent recovery is prohibited.

---

## 14. Security Requirements

Implementations must:

- validate all inputs,
- enforce invariants,
- use constant-time comparisons.

---

## 15. Replay Protection

Replay protection must:

- bind challenges to commitments,
- track used challenges.

---

## 16. Fork Handling

Forks must:

- be detected,
- be preserved,
- not be silently merged.

---

## 17. Abstention

The system must:

- refuse unsafe operations,
- maintain stable divergence.

This is a core ARVIS property.

---

## 18. Storage Independence

The protocol must:

- be storage-agnostic.

Implementations may use:

- local storage,
- cloud storage,
- distributed storage.

---

## 19. Transport Independence

The protocol must:

- be transport-neutral.

Examples:

- HTTP,
- P2P,
- offline sync.

---

## 20. Testing Strategy

A conformant implementation must include:

- unit tests,
- adversarial tests,
- property-based tests.

---

## 21. Conformance Fixtures

Fixtures must:

- remain stable,
- be versioned.

---

## 22. Versioning

Implementations must:

- support version negotiation.

---

## 23. Migration

Migration must:

- preserve commitments,
- avoid history rewriting.

---

## 24. Logging and Observability

Implementations should:

- log failures,
- support auditing.

Sensitive data must never be logged.

---

## 25. Performance

Performance optimizations must:

- not change semantics,
- preserve determinism.

---

## 26. Resource Constraints

Implementations must:

- function in constrained environments.

---

## 27. Interoperability

Implementations must:

- exchange canonical structures,
- validate all incoming data.

---

## 28. Security Review

Security-sensitive changes must:

- undergo review,
- include test coverage.

---

## 29. Documentation

Implementations should document:

- invariants,
- assumptions,
- threat models.

---

## 30. Compliance Levels

Three levels are defined:

### Minimal
Core timeline + encoding.

### Standard
Full protocol support.

### Advanced
Hardware attestation + extended trust.

---

## 31. Open Source Recommendations

Recommended practices:

- reproducible builds,
- signed releases,
- public test coverage.

---

## 32. Governance

Changes must:

- maintain backward compatibility,
- avoid fragmentation.

---

## 33. Final Objective

The objective of this guide is:

> to enable a global ecosystem of interoperable and secure Veramem implementations.
