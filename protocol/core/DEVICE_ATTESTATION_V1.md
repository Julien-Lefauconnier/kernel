# Veramem Device Attestation — Version 1

## 1. Purpose

This document defines the **device attestation protocol** of Veramem.

Device attestation provides a cryptographic proof that:

* a device possesses a valid signing capability,
* the device state is bound to a specific timeline commitment,
* the proof is fresh and resistant to replay,
* the proof can be verified across independent implementations.

This specification is normative for all compliant Veramem systems.

---

## 2. Design Objectives

The attestation protocol is designed to ensure:

* structural integrity,
* replay protection,
* timeline binding,
* cross-device trust negotiation,
* zero-knowledge compatibility,
* forward cryptographic agility.

The protocol prioritizes:

* safety over liveness,
* determinism,
* auditability.

---

## 3. High-Level Overview

The attestation protocol is a **challenge–response mechanism**.

It binds:

1. a device identity,
2. a timeline commitment,
3. a freshness challenge,
4. a cryptographic signature.

The resulting proof allows a verifier to confirm:

* the device controls a valid secret,
* the timeline state is authentic,
* the response is fresh.

---

## 4. Protocol Flow

### Step 1 — Challenge

A verifier generates a random challenge:

```
challenge : bytes
```

The challenge MUST be:

* cryptographically random,
* unpredictable,
* single-use.

---

### Step 2 — Commitment Binding

The device selects a timeline snapshot:

```
snapshot → commitment
```

The commitment binds the device state to:

* ordered history,
* structural integrity,
* append-only guarantees.

---

### Step 3 — Signed Commitment

The device signs the commitment using its signing key.

This produces:

```
SignedCommitment
```

This step ensures:

* device authenticity,
* structural state integrity.

---

### Step 4 — Attestation Response

The device generates the attestation response:

```
Attestation = Sign(
    SignedCommitment,
    ChallengeHash
)
```

The challenge is hashed to avoid length and structure ambiguity.

---

### Step 5 — Verification

The verifier checks:

1. signature validity,
2. commitment integrity,
3. challenge freshness,
4. replay resistance,
5. policy compliance.

---

## 5. Message Structure

All attestation messages MUST use the Veramem canonical wire format.

See:

```
WIRE_FORMAT_V1.md
```

---

## 6. Attestation Bundle

Domain:

```
veramem.device.attestation.bundle.v1
```

Mandatory fields:

| Tag | Field                   |
| --- | ----------------------- |
| 1   | SignedCommitment bundle |
| 2   | challenge_hash          |
| 3   | signature algorithm     |
| 4   | attestation signature   |

The attestation signature is computed over the canonical payload defined below.

---

## 7. Canonical Attestation Payload

The payload to be signed MUST be:

```
domain = veramem.device.attestation.v1
```

Fields:

| Tag | Field                          |
| --- | ------------------------------ |
| 1   | commitment signature algorithm |
| 2   | commitment signature           |
| 3   | challenge_hash                 |

This ensures:

* strict domain separation,
* no signature confusion,
* replay resistance.

---

## 8. Challenge Handling

The challenge MUST:

* be hashed with SHA-256,
* be verified during attestation validation.

Invariant:

```
sha256(challenge) == challenge_hash
```

Failure MUST reject the attestation.

---

## 9. Replay Protection

Replay resistance is ensured by:

* unique challenges,
* freshness policies,
* session binding.

A verifier MUST reject:

* reused challenges,
* stale attestations.

---

## 10. Cryptographic Requirements

### 10.1 Mandatory Algorithm (Profile V1)

The minimal compliant profile requires:

```
HMAC-SHA256
```

This profile supports:

* embedded devices,
* constrained environments,
* deterministic test vectors.

---

### 10.2 Future Profiles

Future profiles MAY support:

* Ed25519,
* ECDSA,
* post-quantum signatures,
* hardware-secured keys.

Algorithm negotiation is defined in future versions.

---

## 11. Determinism

Given identical inputs:

> All compliant implementations MUST produce identical attestation bytes.

This enables:

* cross-language reproducibility,
* conformance testing,
* archival verification.

---

## 12. Security Properties

The protocol guarantees:

### 12.1 Authenticity

The device controls the signing secret.

### 12.2 Integrity

The timeline commitment is cryptographically protected.

### 12.3 Freshness

Replay attacks are prevented.

### 12.4 Domain Isolation

Signatures cannot be reused in other contexts.

### 12.5 Structural Binding

The device state is tied to append-only memory.

---

## 13. Threat Model

The protocol defends against:

* replay attacks,
* forged commitments,
* signature substitution,
* domain confusion,
* challenge manipulation.

---

## 14. Zero-Knowledge Alignment

The protocol does not require:

* plaintext timeline data,
* payload disclosure.

Only commitments and signatures are exchanged.

This aligns with:

* Zero-Knowledge Cognitive Systems,
* privacy-preserving synchronization.

---

## 15. Trust Integration

Attestation feeds into:

* trust anchors,
* device lineage,
* behavioral consistency.

It supports:

* progressive trust evaluation,
* distributed identity,
* long-term memory governance.

See:

```
TIMELINE_TRUST_MODEL.md
```

---

## 16. Compliance Requirements

An implementation is compliant if it:

* uses canonical encoding,
* binds commitments correctly,
* validates challenge freshness,
* rejects replay,
* verifies signatures deterministically,
* passes conformance test vectors.

---

## 17. Error Handling

Verification MUST fail if:

* signature mismatch,
* invalid commitment,
* stale or reused challenge,
* unsupported algorithm,
* malformed canonical encoding.

Fail-fast behavior is required.

---

## 18. Conformance Test Vectors

Reference fixtures include:

* deterministic commitment,
* signed commitment,
* full attestation bundle.

All implementations MUST reproduce identical results.

---

## 19. Future Extensions

Future work includes:

* hardware attestation integration,
* TPM and secure enclave support,
* privacy-preserving attestations,
* unlinkable device proofs,
* zero-knowledge attestation.

---

## 20. Long-Term Vision

Device attestation provides the foundation for:

* resilient distributed cognition,
* secure memory inheritance,
* trusted personal AI,
* long-term digital identity.

It ensures that memory and cognition remain:

* verifiable,
* durable,
* transferable across generations.
