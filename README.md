# Veramem Kernel

The Veramem Kernel is a minimal, deterministic cognitive core designed to record facts, enforce invariants, and preserve temporal truth.

It provides:
- append-only journals for immutable facts
- a monotonic, irreversible timeline
- strict invariant enforcement
- signal lineage and traceability primitives

The kernel does not interpret data, apply policies, or produce user-facing views.
It records what happened, in which order, and under which constraints — nothing more.

Veramem Kernel is intentionally incomplete.
Its purpose is not to be a framework, an application runtime, or an orchestration layer, but a sovereign foundation upon which higher-level systems can safely be built.

## What the Veramem Kernel is NOT

The Veramem Kernel is not an application framework, a policy engine, or a cognitive interpreter.

It does NOT:
- interpret signals or infer meaning
- apply business rules or decision logic
- resolve conflicts or prioritize outcomes
- perform user-level filtering or personalization
- expose APIs, DTOs, or presentation models
- manage storage backends, databases, or transports
- trigger side effects or orchestrate workflows

Any system that applies interpretation, policy, rendering, or orchestration must live outside the kernel.

## Core Guarantees

The Veramem Kernel provides a small set of strict, non-negotiable guarantees.

These guarantees are enforced by construction and verified by tests.
They do not depend on usage patterns, configuration, or runtime environment.

### Append-only facts
All journals and timelines in the kernel are append-only.
Once a fact is recorded, it cannot be modified or removed at runtime.

### Temporal truth
The kernel enforces a single, monotonic timeline.
Events cannot be reordered, rewritten, or inserted retroactively.

### Determinism
Given the same sequence of inputs, the kernel will always produce the same state.
No hidden randomness, implicit side effects, or external dependencies are involved.

### Invariant enforcement
All kernel writes are validated against explicit invariants.
Invalid states are rejected at the boundary, not corrected later.

### Separation of concerns
The kernel produces facts and enforces constraints.
Interpretation, policy, projection, and orchestration are strictly external.

### Test/runtime separation
State reset mechanisms exist for isolated testing only.
They are explicitly marked and unavailable through the public runtime API.

## Architecture Boundaries

The Veramem Kernel is designed to operate as a sovereign core within a larger system.

It deliberately enforces strict boundaries between:
- the Kernel (truth and invariants)
- the Application Stack (projection and orchestration)
- the Reflexive Layer (governed explanation)

### Kernel
The kernel is the sole authority on factual truth and temporal ordering.
It records immutable facts, enforces invariants, and preserves historical integrity.

The kernel does not:
- interpret meaning
- apply policy
- render views
- manage infrastructure
- orchestrate behavior

### Application Stack
The application stack consumes kernel facts and builds usable systems on top of them.
It is responsible for:
- data projection and filtering
- policy enforcement
- storage and transport
- user-facing APIs and interfaces
- orchestration and workflow logic

### Reflexive Layer
The reflexive layer provides governed, post-cognitive explanations about what the system exposes and what it is capable of.

It operates strictly on kernel-produced facts and stack-level projections, without accessing raw data, internal reasoning, or execution logic.

The reflexive layer:
- produces deterministic, declarative explanations
- exposes explicit capabilities and limitations
- supports auditability and compliance
- never produces truth
- never executes actions

It exists outside the kernel and does not influence kernel state.

Violating these boundaries compromises determinism, auditability, and trust.

## Intended Usage & Non-Goals

The Veramem Kernel is intended to be embedded as a foundational component within larger systems that require strong guarantees around factual truth, temporal integrity, and auditability.

### Intended Usage

The kernel is designed to be used as:
- a canonical source of immutable facts
- a temporal authority for event ordering
- a foundation for audit, replay, and compliance
- a stable substrate for projection, interpretation, and explanation layers

Typical usage patterns include:
- feeding append-only journals from external systems
- enforcing invariants at the boundary of factual recording
- projecting kernel facts into application-specific views
- supporting deterministic replay and verification

The kernel can be embedded in:
- backend services
- cognitive systems
- governance or compliance frameworks
- research or experimental environments

### Non-Goals

The Veramem Kernel explicitly does NOT aim to:
- provide a complete application runtime
- replace databases or storage engines
- perform business logic or decision-making
- expose user-facing APIs or interfaces
- handle authentication, authorization, or access control
- manage infrastructure, networking, or persistence
- offer real-time reactivity or event-driven orchestration

If a feature requires interpretation, policy, execution, or presentation, it does not belong in the kernel.

## License

This project is licensed under the Apache License, Version 2.0.
