# Veramem Protocol Registry

## 1. Purpose

This registry defines globally reserved identifiers used in the Veramem protocol.

It prevents collisions across independent implementations and enables interoperability.

---

## 2. Domain Separation Registry

All canonical messages MUST use domain-separated identifiers.

### 2.1 Core Domains

| Domain                                  | Description             |
| --------------------------------------- | ----------------------- |
| `veramem.timeline.entry.v1`             | Timeline entry          |
| `veramem.timeline.commitment.v1`        | Timeline commitment     |
| `veramem.timeline.delta.v1`             | Delta synchronization   |
| `veramem.timeline.fork.v1`              | Fork proof              |
| `veramem.timeline.merge.v1`             | Merge result            |
| `veramem.timeline.reconcile.v1`         | Reconciliation decision |
| `veramem.timeline.signed_commitment.v1` | Signed commitment       |
| `veramem.device.attestation.v1`         | Device attestation      |
| `veramem.device.attestation.bundle.v1`  | Attestation bundle      |

Future domains MUST follow:

```
veramem.<layer>.<object>.vX
```

---

## 3. TLV Tag Registry

Tags MUST be deterministic and stable.

### 3.1 Root Message Version

| Tag | Meaning             |
| --- | ------------------- |
| 1   | Wire format version |

---

### 3.2 Timeline Entry

| Tag | Meaning          |
| --- | ---------------- |
| 2   | Entry ID         |
| 3   | Timestamp        |
| 4   | Type             |
| 5   | Title            |
| 6   | Description      |
| 7   | Action ID        |
| 8   | Place ID         |
| 9   | Origin reference |
| 10  | Nature           |
| 11  | Device ID        |
| 12  | Lamport clock    |

---

Additional registries MUST be appended here.

---

## 4. Algorithm Registry

### 4.1 Signature Algorithms

| Identifier    | Description              |
| ------------- | ------------------------ |
| `hmac-sha256` | Default symmetric signer |

Future additions:

* Ed25519
* PQC signatures.

---

### 4.2 Hash Functions

| Identifier | Description  |
| ---------- | ------------ |
| `sha256`   | Default hash |

---

## 5. Profiles

| Profile  | Description         |
| -------- | ------------------- |
| Minimal  | Encoding + timeline |
| Standard | Sync + attestation  |
| Advanced | Trust + hardware    |

---

## 6. Extension Policy

New identifiers MUST:

* be deterministic,
* avoid collisions,
* preserve backward compatibility.

---

## 7. Governance

This registry is maintained by the Veramem community.

Changes require:

* consensus,
* documentation,
* conformance updates.

---

## 8. IANA Considerations

Future versions may register:

* domains,
* algorithms,
* protocol parameters.

---

## 9. Conclusion

The registry ensures that independent implementations remain interoperable and secure.
