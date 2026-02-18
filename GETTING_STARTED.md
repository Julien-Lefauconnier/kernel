# Getting Started with Veramem

This guide provides a minimal and structured introduction to the Veramem kernel.

It is intended for:
- engineers integrating Veramem,
- researchers evaluating the system,
- contributors exploring the architecture.

For full protocol and security specifications, see the `protocol/` and `security/` directories.

---

## 1. What is Veramem?

Veramem is a distributed, deterministic, and formally specified memory kernel designed for:

- long-term cognitive systems,
- verifiable AI memory,
- privacy-preserving knowledge systems,
- distributed trust and auditability.

The kernel provides:

- deterministic event journaling,
- cryptographic commitments,
- timeline integrity,
- signal lineage tracking,
- device and trust attestation,
- formal invariants.

The system is designed under:

- Zero-Knowledge Cognitive System (ZKCS) principles,
- ARVIS architecture (Adaptive Resilient Vigilant Intelligence System).

---

## 2. Core concepts

Before using Veramem, it is important to understand its main abstractions:

### Timeline
A cryptographically verifiable ordered log of events.

### Signals
Structured knowledge representations with canonical forms.

### Lineage
Formal evolution of signals through deterministic transformations.

### Attestation
Trust anchors and device identity verification.

### Determinism
All operations are reproducible and verifiable.

More details:
- `protocol/VERAMEM_PROTOCOL_SPEC.md`
- `protocol/TIMELINE_FORMAL_INVARIANTS.md`
- `protocol/SIGNAL_LINEAGE_FORMAL_INVARIANTS.md`

---

## 3. Installation

### Requirements

- Python 3.10+
- pip

### Install locally

```bash
pip install -e .
```
Or:

pip install veramem_kernel

---

## 4. Run the test suite

The test suite validates formal invariants, determinism, and security properties.

``pytest``

The conformance suite ensures protocol interoperability:

``pytest conformance/``

---

## 5. Minimal example

from veramem_kernel.api import timeline, signals

# Create timeline
t = timeline.TimelineJournal()

# Create signal
s = signals.Signal(...)

# Append event
t.append(s)

# Compute commitment
head = t.head_commitment()``

This example is simplified. See the reference implementation guide:

- `VERAMEM_REFERENCE_IMPLEMENTATION_GUIDE.md`

---

## 6. Security model

Veramem is designed for adversarial environments.

Key properties:

- tamper-evident logs,
- replay resistance,
- formal invariants,
 -zero-knowledge compatibility.

See:

- `security/KERNEL_THREAT_MODEL.md`
- `security/VERAMEM_SECURITY_ARCHITECTURE.md`

---

## 7. Interoperability

The protocol supports:

- distributed nodes,
- heterogeneous implementations,
- deterministic synchronization.

See:

- `protocol/VERAMEM_INTEROPERABILITY_SPEC.md`

---

## 8. Contributing

Please read:

- `CONTRIBUTING.md`

---

## 9. Research and roadmap

The long-term research direction is described in:

- `docs/research/VERAMEM_RESEARCH_ROADMAP.md`

---

## 10. Community and governance

Veramem aims to become an open and neutral standard.

See:

- `governance/VERAMEM_TRUST_AND_GOVERNANCE.md`
- `governance/VERAMEM_STANDARDIZATION_PATH.md`