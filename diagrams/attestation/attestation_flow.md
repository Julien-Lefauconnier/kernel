# Device Attestation Flow

```mermaid
sequenceDiagram
participant Verifier
participant Device

Verifier->>Device: Challenge
Device->>Device: Build timeline snapshot
Device->>Device: Compute commitment
Device->>Device: Sign commitment

Device->>Verifier: Attestation bundle

Verifier->>Verifier: Verify signature
Verifier->>Verifier: Verify commitment
Verifier->>Verifier: Check freshness
```

---

## Security Properties

* Replay resistance.
* Commitment binding.
* Structural verification.

---

## Zero-Knowledge Alignment

The verifier does not need access to raw memory.
