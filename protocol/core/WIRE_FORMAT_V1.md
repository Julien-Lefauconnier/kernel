# Veramem Wire Format — Version 1

## 1. Purpose

This document defines the **canonical binary wire format** used by the Veramem protocol.

The wire format ensures:

* deterministic serialization,
* cryptographic stability,
* cross-language interoperability,
* long-term archival durability,
* signature reproducibility,
* domain separation.

This specification is normative for all Veramem implementations.

---

## 2. Design Principles

The Veramem wire format is designed to be:

* deterministic,
* unambiguous,
* implementation-independent,
* extensible,
* versioned,
* resistant to replay and ambiguity.

The format prioritizes:

* auditability,
* security,
* long-term compatibility.

---

## 3. Canonical Encoding Model

All protocol messages use a **canonical TLV encoding** with strict ordering and domain separation.

Each message is encoded as:

```
Message = Header || Domain || TLV Fields
```

Where:

* Header identifies the encoding version.
* Domain ensures structural separation.
* Fields are encoded using deterministic TLV.

---

## 4. Header Format

The first 4 bytes of any canonical message MUST be:

```
"VCE1"
```

This constant identifies:

* Veramem Canonical Encoding
* Version 1.

This prevents ambiguity and format confusion.

Future versions MUST use a different prefix.

---

## 5. Domain Separation

After the header, the domain is encoded as:

```
domain_length : 2 bytes (big-endian)
domain : ASCII bytes
```

The domain:

* uniquely identifies the message type,
* prevents cross-domain signature reuse,
* ensures cryptographic isolation.

Example:

```
veramem.timeline.entry.v1
veramem.device.attestation.bundle.v1
```

---

## 6. TLV Structure

Each field is encoded as:

```
tag : 2 bytes (big-endian)
length : 4 bytes (big-endian)
value : raw bytes
```

Properties:

* deterministic ordering,
* no implicit defaults,
* no optional tag reordering,
* strict parsing required.

Unknown tags MUST be rejected unless explicitly allowed.

---

## 7. Field Ordering

Fields MUST be ordered strictly by ascending tag value.

This ensures:

* byte-level determinism,
* identical signatures across implementations.

Non-canonical ordering MUST be rejected.

---

## 8. Root Message Versioning

All root protocol messages MUST include:

```
tag = 1 → wire protocol version
```

For version 1:

```
value = b"\x01"
```

This allows:

* backward compatibility,
* future protocol evolution.

Messages without this tag MUST be rejected.

---

## 9. Encoding Constraints

### 9.1 ASCII Fields

Certain fields MUST be ASCII-only:

* identifiers,
* algorithms,
* domain-bound metadata.

Control characters are forbidden.

---

### 9.2 UTF-8 Fields

Human-readable fields MUST use UTF-8.

---

### 9.3 Binary Fields

Cryptographic and opaque payloads use raw bytes.

---

## 10. Determinism Requirements

For any semantic structure:

> All compliant implementations MUST produce identical byte representations.

This includes:

* Python,
* Rust,
* Go,
* Java,
* WebAssembly.

Non-deterministic encoding is forbidden.

---

## 11. Cryptographic Stability

All commitments and signatures MUST be computed over:

* the canonical byte representation.

No alternative serialization is allowed.

---

## 12. Versioning and Extensibility

Forward compatibility is supported by:

* strict version tag,
* domain versioning,
* future tag allocation.

New versions MUST:

* use a new domain or wire version,
* preserve existing data.

---

## 13. Unknown Field Handling

For strict profiles:

* unknown tags MUST be rejected.

For extensible profiles:

* unknown tags MAY be accepted if explicitly allowed.

This behavior MUST be documented per message.

---

## 14. Security Properties

The wire format ensures:

* replay resistance (via domain binding),
* signature isolation,
* deterministic commitments,
* corruption detectability,
* cross-language reproducibility.

---

## 15. Example: Timeline Entry

Example domain:

```
veramem.timeline.entry.v1
```

Mandatory fields:

| Tag | Field         |
| --- | ------------- |
| 1   | wire version  |
| 2   | entry_id      |
| 3   | timestamp     |
| 4   | entry type    |
| 5   | title         |
| 10  | nature        |
| 11  | device_id     |
| 12  | lamport clock |

Optional:

| Tag | Field       |
| --- | ----------- |
| 6   | description |
| 7   | action_id   |
| 8   | place_id    |
| 9   | origin_ref  |

---

## 16. Device Identity Binding

Each entry includes:

* device fingerprint (SHA256),
* Lamport logical clock.

This supports:

* distributed ordering,
* causality modeling,
* fork resilience.

---

## 17. Parsing Rules

A compliant parser MUST:

1. Validate header.
2. Validate domain.
3. Validate version.
4. Validate field ordering.
5. Reject malformed or ambiguous messages.
6. Enforce strict type validation.

---

## 18. Error Handling

Decoding MUST fail if:

* domain mismatch,
* missing required fields,
* unsupported version,
* invalid encoding,
* malformed TLV,
* non-canonical ordering.

Fail-fast behavior is required.

---

## 19. Formal Properties

The wire format guarantees:

* determinism,
* immutability,
* replay safety,
* canonical commitment.

This supports:

* distributed cognition,
* zero-knowledge reasoning,
* long-term archival.

---

## 20. Alignment with ARVIS and ZKCS

This format enables:

* structural cognition,
* reasoning without plaintext,
* secure distributed memory.

It is compatible with:

* zero-knowledge architectures,
* privacy-preserving systems.

---

## 21. Future Work

Planned extensions:

* post-quantum cryptography,
* zero-knowledge commitments,
* selective disclosure,
* privacy-preserving attestations.

---

## 22. Compliance

An implementation is compliant if:

* it produces canonical encoding,
* it passes conformance tests,
* it preserves deterministic commitments.
