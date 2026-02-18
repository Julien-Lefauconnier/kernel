# Veramem Kernel

**A deterministic cognitive core for recording truth, enforcing invariants, and preserving temporal integrity.**

The Veramem Kernel is a minimal, sovereign foundation designed to make factual systems **auditable, deterministic, and composable by construction**.

It provides a formal substrate for building:
- trustworthy AI
- compliant cognitive systems
- distributed memory infrastructures
- long-term digital identity and knowledge preservation

---

## Why Veramem?

Modern software and AI systems suffer from fundamental weaknesses:
- mutable state
- hidden side effects
- temporal ambiguity
- unverifiable reasoning
- weak auditability
- opaque decision pipelines

These limitations make systems fragile, unsafe, and difficult to trust.

The Veramem Kernel addresses these problems by enforcing:
- immutable factual recording
- strict temporal ordering
- invariant validation at write time
- deterministic replay and verification
- traceable signal lineage

It does not try to interpret the world.  
It guarantees that **what is recorded is stable, ordered, and verifiable**.

---

## Core Capabilities

The kernel provides a small and strictly defined set of primitives:

### Append-only journals
Immutable recording of facts across domains such as:
- observations
- knowledge
- signals
- audits
- constraints

Facts cannot be modified or removed at runtime.

### Monotonic timeline
A single, irreversible ordering of events ensures:
- temporal integrity
- reproducible replay
- causal traceability
- fork and reconciliation support

### Signal lineage
Built-in primitives for:
- provenance tracking
- evolution of signals
- conflict resolution frameworks
- explainable historical state

### Invariant enforcement
Every write is validated against explicit formal invariants.  
Invalid states are rejected immediately.

### Deterministic behavior
Given the same inputs, the kernel always produces the same outputs.

No hidden randomness.  
No implicit side effects.

---

## What the Veramem Kernel is NOT

The kernel is intentionally minimal and incomplete.

It does NOT:
- interpret signals or infer meaning
- apply business or policy logic
- resolve priorities or optimize outcomes
- provide orchestration or workflow engines
- expose user-facing APIs
- manage databases or storage
- trigger external side effects
- perform filtering or personalization

These responsibilities belong outside the kernel.

This strict separation is essential for:
- safety
- auditability
- long-term reliability

---

## Architecture Boundaries

Veramem enforces a strong separation between layers.

### Kernel (truth layer)

The kernel is the sole authority for:
- factual recording
- temporal ordering
- invariant enforcement
- historical integrity

It never interprets or executes.

### Application stack

The application stack:
- projects kernel facts
- applies policies
- orchestrates workflows
- builds interfaces
- manages storage and infrastructure

### Reflexive layer

The reflexive layer produces:
- governed explanations
- compliance narratives
- declarative system capabilities

It operates strictly on projected facts and never influences kernel state.

Violating these boundaries compromises determinism and trust.

---

## Intended Usage

The Veramem Kernel is designed to be embedded in systems requiring strong guarantees.

Typical use cases:
- AI memory and cognitive architectures
- compliance and governance systems
- digital identity and long-term knowledge
- distributed coordination and consensus
- reproducible research environments
- regulated or high-trust infrastructures

---

## Installation

The kernel is published on PyPI:

```bash
pip install veramem-kernel
```
### Optional cryptography

For distributed trust and Ed25519 support:

```bash
pip install veramem-kernel[crypto]
```

---

## Quick Start

Run a minimal deterministic timeline:

```bash
python examples/basic_timeline.py
```

---

## Examples

The repository contains a growing collection of generic and domain-agnostic examples demonstrating the guarantees of the Veramem Kernel.

These examples illustrate:

- deterministic timelines
- distributed state evolution
- auditable AI memory
- replay and verification
- identity and attestation
- conflict traceability
- Explainable AI Backbone
- Long-Term Memory
- Zero-knowledge Governance

See the `examples/` directory for runnable demonstrations.

---

## Core Guarantees

The kernel provides a small set of non-negotiable guarantees:

- Append-only truth
- Temporal integrity
- Determinism
- Invariant safety
- Reproducibility
- Auditability
- Separation concerns
- Cryptographic integrity (HMAC-SHA256 baseline + Ed25519 for distributed trust)

These properties are enforced by construction and verified through extensive tests.

---
## Badges

[![CI](https://github.com/Julien-Lefauconnier/kernel/actions/workflows/ci.yml/badge.svg)](https://github.com/Julien-Lefauconnier/kernel/actions)
[![PyPI](https://img.shields.io/pypi/v/veramem-kernel)](https://pypi.org/project/veramem-kernel/)
[![Python](https://img.shields.io/pypi/pyversions/veramem-kernel)](https://pypi.org/project/veramem-kernel/)
[![Conformance](https://img.shields.io/badge/conformance-passed-brightgreen)](conformance/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](LICENSE)

The kernel is published on PyPI (current: v1.0.2):

---

## Open Source Scope

This repository contains only the Veramem Kernel.

It includes:

- the deterministic cognitive core
- invariant enforcement
- signal lineage
- timeline integrity
- cryptographic primitives
- formal specifications and models

It does not include:

- storage backends
- orchestration layers
- deployment systems
- hosted or commercial services

These belong to separate components of the Veramem ecosystem.

---

## Research & Formal Foundations

The kernel is grounded in:

- formal invariant systems
- deterministic computation
- temporal consistency models
- distributed trust architectures
- zero-knowledge cognitive design

See the protocol/ and docs/ directories for specifications.

---

## Contributing

We welcome contributions from:

- distributed systems engineers
- formal methods researchers
- cryptographers
- AI safety and governance experts

Please read:

- CONTRIBUTING.md
- MAINTAINERS.md (we welcome new maintainers!)
- SECURITY.md
- GOVERNANCE.md

---

## License

This project is licensed under the Apache License, Version 2.0.