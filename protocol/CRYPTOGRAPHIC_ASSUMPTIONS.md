# Cryptographic Assumptions — Veramem

## 1. Purpose

This document defines the **cryptographic assumptions and security posture**
underlying the Veramem protocol.

The goal is to ensure:

- long-term integrity of memory,
- deterministic verification across implementations,
- resilience against adversarial manipulation,
- future cryptographic agility.

This document is normative unless stated otherwise.

---

## 2. Security Model

The Veramem protocol relies on:

- collision-resistant hash functions,
- secure message authentication and signatures,
- domain separation,
- deterministic canonical encoding,
- structural commitments rather than plaintext trust.

The protocol is designed to operate in:

- adversarial network environments,
- partially trusted ecosystems,
- zero-knowledge cognitive settings.

---

## 3. Hash Functions

### 3.1 Default

The reference implementation uses:

- **SHA-256**

for:

- timeline commitments,
- structural hashing,
- fork detection,
- snapshot identity.

### 3.2 Required Properties

Hash functions MUST provide:

- collision resistance,
- preimage resistance,
- second preimage resistance.

Weak or deprecated hash functions MUST NOT be used.

---

## 4. Message Authentication and Signatures

### 4.1 Default Mechanism

The baseline protocol supports:

- **HMAC-SHA256**

This is suitable for:

- constrained environments,
- embedded devices,
- symmetric trust models.

### 4.2 Implementation Requirements

Implementations MUST ensure:

- constant-time comparison,
- strict signature length validation,
- no implicit truncation,
- deterministic verification.

---

### 4.3 Asymmetric Signatures (Recommended)

For higher trust environments, implementations SHOULD support:

- **Ed25519**

This enables:

- multi-party verification,
- decentralized trust,
- hardware-backed identities,
- public auditability.

Future protocol profiles may require asymmetric signatures.

---

## 5. Cryptographic Agility

The protocol is designed to evolve without breaking existing data.

Possible upgrades include:

- SHA-256 → SHA-512, BLAKE3, or post-quantum hashes,
- HMAC → modern signature schemes,
- Ed25519 → post-quantum signature algorithms.

Migration MUST:

- preserve historical commitments,
- allow coexistence of multiple algorithms,
- avoid re-signing or rewriting history,
- maintain deterministic verification.

Algorithm identifiers MUST be explicit in the wire format.

---

## 6. Domain Separation

All cryptographic operations MUST use:

- explicit and stable domain separation.

This includes:

- commitments,
- signatures,
- attestation,
- encoding contexts.

This prevents:

- cross-protocol confusion,
- replay across layers,
- signature reuse attacks.

Domain strings are versioned and part of the canonical encoding.

---

## 7. Deterministic Encoding

All cryptographic operations depend on:

- canonical encoding,
- strict ordering,
- stable byte representation.

If two implementations produce different encodings,
they MUST reject the message.

Determinism is a core security property.

---

## 8. Randomness and Entropy

Secure randomness is required for:

- key generation,
- challenges,
- device identity,
- attestation freshness.

Implementations MUST use:

- cryptographically secure random number generators.

Weak or predictable randomness invalidates security guarantees.

---

## 9. Post-Quantum Considerations

The protocol is designed to support:

- post-quantum hash functions,
- post-quantum signatures,
- hybrid cryptographic models.

Backward compatibility is mandatory.

The timeline and commitments remain valid across upgrades.

---

## 10. Structural Trust and Zero-Knowledge Alignment

The Veramem protocol prioritizes:

- structural verification,
- commitment-based reasoning,
- minimal exposure of raw data.

Security does not depend on:

- plaintext inspection,
- semantic trust,
- centralized authorities.

This aligns with:

- Zero-Knowledge Cognitive Systems (ZKCS),
- long-term cognitive resilience.

---

## 11. Threat Model Assumptions

Security assumes:

- honest-but-fallible implementations,
- adversarial networks,
- compromised or malicious nodes,
- partial trust overlap.

The protocol aims to detect:

- tampering,
- rollback,
- replay,
- fork injection.

The protocol does not assume:

- trusted timestamps,
- trusted infrastructure,
- perfect network connectivity.

---

## 12. Non-Goals

This document does not define:

- encryption schemes,
- secure storage,
- hardware trust mechanisms,
- user identity models.

These are layered above the kernel.

---

## 13. Conclusion

The Veramem protocol relies on:

- conservative cryptographic design,
- deterministic encoding,
- explicit algorithm evolution,
- structural commitments.

This enables:

- long-term verifiable memory,
- resilient distributed cognition,
- safe evolution under uncertainty.
