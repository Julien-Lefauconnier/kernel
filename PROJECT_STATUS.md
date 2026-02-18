# Veramem — Project Status and Scope

## 1. Purpose

This document defines the current stability and maturity level of the Veramem Kernel and Protocol.

It is intended to help:

* implementers,
* auditors,
* contributors,
* future maintainers,

understand which components are stable and which may evolve.

This ensures long-term continuity and safe ecosystem growth.

---

## 2. Stability Philosophy

Veramem follows a **safety-first and stability-first approach**.

Changes to stable components must:

* preserve backward compatibility,
* maintain determinism,
* pass all conformance tests.

Experimental components may evolve.

---

## 3. Stable Components (Normative)

The following elements are considered **stable and production-grade**:

### 3.1 Canonical Encoding

* TLV-based deterministic encoding.
* Domain separation.
* Byte-level reproducibility.

Defined in:

* `WIRE_FORMAT_V1.md`

This format MUST remain stable.

---

### 3.2 Timeline Commitments

* Hashchain structure.
* Snapshot identity.
* Deterministic head computation.

Defined in:

* Timeline model specifications.

---

### 3.3 Delta Synchronization

* Append-only extension.
* Base match validation.
* Replay protection.

---

### 3.4 Fork Detection and Classification

* Deterministic prefix detection.
* Stable divergence.

---

### 3.5 Safe Merge Model

* Deterministic ordering.
* Non-destructive convergence.
* Abstention when unsafe.

---

### 3.6 Device Attestation V1

* Commitment binding.
* Challenge-response.
* Replay protection.

---

## 4. Experimental Components

The following areas may evolve:

* Trust weighting and reputation.
* Probabilistic or adaptive merging.
* Governance overlays.
* Multi-anchor trust graphs.
* Secure gossip strategies.
* Zero-knowledge advanced features.

These changes MUST NOT break stable protocol layers.

---

## 5. Compatibility Guarantees

Stable layers guarantee:

* Deterministic behavior.
* Canonical encoding stability.
* Commitment reproducibility.
* Cross-language interoperability.

Any breaking change MUST introduce a new protocol version.

---

## 6. Conformance

An implementation is considered compliant if:

* it passes the official conformance suite,
* it produces identical commitments,
* it respects canonical encoding.

---

## 7. Long-Term Vision

The Veramem protocol is designed for:

* decades or centuries of operation,
* intergenerational knowledge continuity,
* resilient distributed cognition.

---

## 8. Maintenance and Governance

This document should be updated when:

* new protocol versions are released,
* components become stable or deprecated.

---

## 9. Scope

This document does not define:

* governance policy,
* trust authority,
* application semantics.

These belong to higher layers.

---

## 10. Conclusion

Veramem prioritizes:

> stability, determinism, safety, and resilience.

This ensures that the protocol can evolve while preserving historical continuity and interoperability.
