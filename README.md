# Veramem Kernel
**A deterministic cognitive core for recording truth, enforcing invariants, and preserving temporal integrity.**

The Veramem Kernel is a minimal, sovereign foundation designed to make factual systems **auditable, deterministic, and composable by construction**.

It provides a formal substrate for building:
- trustworthy AI
- compliant cognitive systems
- distributed memory infrastructures
- long-term digital identity and knowledge preservation

[![CI](https://github.com/Julien-Lefauconnier/kernel/actions/workflows/ci.yml/badge.svg)](https://github.com/Julien-Lefauconnier/kernel/actions)
[![PyPI version](https://badge.fury.io/py/veramem-kernel.svg)](https://badge.fury.io/py/veramem-kernel)
[![Python versions](https://img.shields.io/pypi/pyversions/veramem-kernel.svg)](https://pypi.org/project/veramem-kernel/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Conformance](https://img.shields.io/badge/conformance-passed-brightgreen)](conformance/)

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

- **Append-only journals** — Immutable recording of facts across domains (observations, knowledge, signals, audits, constraints)
- **Monotonic timeline** — Single irreversible ordering with fork/reconciliation support
- **Signal lineage** — Provenance tracking, signal evolution, conflict resolution
- **Invariant enforcement** — Every write validated against formal invariants
- **Deterministic behavior** — Same inputs always produce the same outputs (no hidden randomness or side effects)

All operations are pure, auditable, and reproducible.

---

## What the Veramem Kernel is NOT

The kernel is intentionally minimal and incomplete. It does **NOT**:
- interpret signals or infer meaning
- apply business or policy logic
- resolve priorities or optimize outcomes
- provide orchestration or workflow engines
- expose user-facing APIs
- manage databases or storage
- trigger external side effects

These responsibilities belong outside the kernel. This strict separation is essential for **safety**, **auditability**, and **long-term reliability**.

---

## Architecture Boundaries

Veramem enforces a strong separation between layers:

- **Kernel (truth layer)** — Factual recording, temporal ordering, invariant enforcement, historical integrity
- **Application stack** — Projects facts, applies policies, orchestrates workflows, manages storage
- **Reflexive layer** — Governed explanations, compliance narratives (never influences kernel state)

Violating these boundaries compromises determinism and trust.

---

## Intended Usage

The Veramem Kernel is designed to be embedded in systems requiring strong guarantees.

Typical use cases:
- AI memory and cognitive architectures
- Compliance and governance systems
- Digital identity and long-term knowledge preservation
- Distributed coordination and consensus
- Reproducible research environments
- Regulated or high-trust infrastructures

---

## Installation

The kernel is published on [PyPI](https://pypi.org/project/veramem-kernel/):

```bash
# Core kernel (minimal, no crypto dependencies)
pip install veramem-kernel

# With Ed25519 support for distributed trust & attestation
pip install veramem-kernel[crypto]
```

Requires Python 3.10+.

---

## Quick Start

Run a minimal deterministic timeline:

```bash
python -m examples.basic_timeline
```

Explore more examples in the examples/ directory:

- distributed_timeline.py — Fork, divergence, deterministic merge
- explainable_ai_backbone.py — Governed explanations & audit trails
- long_term_memory.py — Epochs, snapshots, long-horizon reconstruction
- etc... (more than 15 examples)

---

### Core Guarantees

The kernel provides non-negotiable guarantees enforced by construction:

- Append-only truth
- Temporal integrity
- Determinism
- Invariant safety
- Reproducibility
- Auditability
- Strict separation of concerns
- Cryptographic integrity (HMAC-SHA256 baseline + Ed25519 via [crypto])

These properties are verified through extensive tests and conformance fixtures (included in the package).

---

## Conformance & Interoperability

Golden fixtures (deterministic test vectors) are included:

- Attestation (HMAC + Ed25519)
- Timeline delta, fork, merge, reconcile

Regenerate and verify in CI:

```bash
python conformance/generate_fixtures.py
git diff --exit-code conformance/fixtures/
```

See conformance/ for the full suite.

---

## Open Source Scope

This repository contains only the Veramem Kernel:

- deterministic core
- invariant enforcement
- signal lineage
- timeline integrity
- cryptographic primitives
- formal specifications and models

It does not include storage backends, orchestration layers, deployment systems, or hosted services.
License: Apache 2.0

---

## Research & Formal Foundations

Grounded in:

- formal invariant systems
- deterministic computation
- temporal consistency models
- distributed trust architectures
- zero-knowledge cognitive design

See protocol/, docs/, and formal/ directories.

---

## Contributing

We welcome contributions from:

- distributed systems engineers
- formal methods & cryptography researchers
- AI safety & governance experts

Please read:

CONTRIBUTING.md
MAINTAINERS.md (we welcome new maintainers!)
SECURITY.md
GOVERNANCE.md


Start with good first issues or help improve conformance tests!
The Veramem Kernel is built to outlive any single contributor.
Join us in creating a durable foundation for verifiable, trustworthy systems.