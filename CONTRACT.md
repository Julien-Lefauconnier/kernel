# Veramem Kernel Contract

This document defines the explicit, non-negotiable guarantees provided by the Veramem Kernel.

It exists to:
- state what the kernel guarantees, without ambiguity
- define which behaviors are considered stable
- clarify what constitutes a breaking change
- prevent misuse or misinterpretation of the kernel’s role
- provide a durable reference for audits and long-term maintenance

This contract applies to the Veramem Kernel only.
It does not cover application stacks, integrations, or reflexive layers built on top of it.

Any behavior not explicitly guaranteed by this document must be considered unstable and subject to change.

## Scope of Guarantees

The guarantees defined in this contract apply exclusively to the following aspects of the Veramem Kernel:

- the semantic meaning of kernel-level facts
- the append-only nature of journals and timelines
- the enforcement of explicit invariants
- the determinism of kernel state transitions
- the authority of the kernel over temporal ordering
- the absence of interpretation, policy, or execution logic

These guarantees apply:
- regardless of deployment environment
- regardless of integration context
- regardless of application stack or consumer behavior

The contract does not guarantee:
- performance characteristics
- memory usage or storage efficiency
- backward compatibility beyond the guarantees explicitly stated
- stability of internal implementation details
- stability of test-only mechanisms

Only the externally observable behaviors described in this contract are considered stable.

## Non-Negotiable Invariants

The following invariants are absolute.
They apply at all times, under all circumstances, and across all integrations.

Any violation of these invariants constitutes a kernel contract breach.

### Immutability of Facts

All kernel-level facts are immutable.

Once a fact is recorded in a journal or timeline:
- it cannot be modified
- it cannot be deleted
- it cannot be reordered
- it cannot be replaced

The kernel provides no mechanism to alter historical facts at runtime.

### Append-Only Journals

All kernel journals are append-only.

Facts may only be added at the end of a journal.
Any attempt to insert, overwrite, or retroactively modify entries is forbidden.

Append operations either:
- succeed fully
- or fail without partial state change

### Temporal Monotonicity

The kernel enforces a single, strictly monotonic timeline.

Timeline entries must:
- contain an explicit timestamp
- be appended in non-decreasing temporal order

The kernel rejects any entry that violates temporal monotonicity.

### Deterministic State Evolution

Kernel state evolution is deterministic.

Given the same sequence of valid inputs:
- the kernel will always produce the same state
- the same journals
- the same timeline

No hidden randomness, implicit side effects, or external state may influence kernel behavior.

### Explicit Invariant Enforcement

All kernel writes are validated against explicit invariants at the time of insertion.

Invalid data is rejected at the boundary.
The kernel never attempts to:
- auto-correct invalid states
- infer missing information
- resolve inconsistencies internally

### No Interpretation or Policy

The kernel does not interpret facts.

It does not:
- infer meaning
- apply policy
- resolve conflicts
- prioritize outcomes
- execute decisions

Any system that performs interpretation, governance, or execution operates outside the kernel.

### No Side Effects

Kernel operations produce no side effects.

The kernel does not:
- perform I/O
- trigger callbacks
- emit events
- schedule tasks
- mutate external state

Its only effect is the deterministic evolution of its internal factual state.

## Test-Only Mechanisms

The Veramem Kernel includes limited mechanisms intended exclusively for isolated testing.

These mechanisms exist solely to:
- allow deterministic test execution
- ensure test independence
- validate invariants under controlled conditions

### Explicit Test Scope

Test-only mechanisms are:
- explicitly named
- explicitly documented
- explicitly excluded from runtime usage

They are not part of the kernel’s public runtime contract.

### No Runtime Availability

Test-only mechanisms must not be:
- reachable through runtime APIs
- accessible via integration layers
- callable by application code
- relied upon for system behavior

Any use of test-only mechanisms outside of isolated testing constitutes a contract violation.

### State Reset Semantics

Where provided, state reset mechanisms:
- clear in-memory kernel state
- do not alter invariant definitions
- do not bypass invariant enforcement
- do not mutate historical facts at runtime

They exist solely to restore a clean test environment.

### Non-Observability Guarantee

The presence or absence of test-only mechanisms must not:
- affect kernel behavior
- influence determinism
- alter factual recording
- leak into observable runtime state

Removing all test-only mechanisms must not change kernel semantics.

### No Backward Compatibility Guarantee

Test-only mechanisms are exempt from backward compatibility guarantees.

They may:
- change
- be renamed
- be restricted
- be removed

without constituting a breaking change to the kernel contract.

## Signal Lineage & Traceability

The Veramem Kernel provides first-class primitives for signal lineage and traceability.

Signal lineage is a structural property of the kernel.
It exists to preserve historical integrity, not to explain meaning.

### Lineage as Structural Truth

Every signal recorded by the kernel:
- has a stable identity
- belongs to an explicit lineage
- preserves its ancestry across transformations

Lineage relationships are:
- explicit
- immutable
- deterministic

They cannot be inferred, guessed, or retroactively constructed.

### No Semantic Interpretation

Signal lineage does not imply semantic causality.

The kernel does not:
- infer cause-effect relationships
- interpret signal meaning
- assign responsibility or intent
- construct narratives

Lineage only encodes factual relationships between signals.

### Deterministic Reconstruction

Given the full kernel state:
- signal lineage can be deterministically reconstructed
- no external context is required
- no hidden state is involved

Lineage reconstruction yields the same result across all environments.

### Closed World Constraint

The kernel enforces a closed world for signal lineage.

All lineage relationships must:
- reference existing kernel signals
- respect canonical signal definitions
- satisfy lineage invariants

The kernel rejects lineage that:
- references unknown signals
- violates canonical constraints
- introduces ambiguity

### Audit and Verification

Signal lineage enables:
- deterministic audit
- reproducible verification
- historical integrity checks

It does not provide:
- explanations
- justifications
- governance decisions
- user-facing narratives

Those concerns belong to external layers.

## Versioning & Compatibility

The Veramem Kernel follows a strict contract-first versioning policy.

Compatibility is defined exclusively by this contract.
Any behavior not explicitly guaranteed herein is subject to change.

### Contract Stability

The following elements are considered stable across compatible versions:
- the guarantees explicitly stated in this contract
- the non-negotiable invariants
- the observable behavior of kernel journals and timelines
- the semantics of signal lineage as defined by contract

As long as these elements hold, the kernel is considered compatible.

### Implementation Freedom

Internal implementation details are not part of the contract.

The kernel makes no guarantee regarding:
- internal data structures
- class layouts or method signatures
- module organization
- performance characteristics
- memory usage
- internal optimization strategies

These may change freely between versions without constituting a breaking change.

### Test-Only Mechanisms

Test-only mechanisms are explicitly excluded from compatibility guarantees.

They may:
- change
- be renamed
- be restricted
- be removed

without notice or version guarantees.

### Breaking Changes

A breaking change occurs only if:
- a contract guarantee is violated
- a non-negotiable invariant is weakened or removed
- observable kernel behavior deviates from the contract

Refactoring, reorganization, or optimization alone does not constitute a breaking change.

### Version Signaling

Kernel versions signal:
- contract compatibility
- invariant stability

They do not signal:
- feature completeness
- integration readiness
- application-level guarantees
