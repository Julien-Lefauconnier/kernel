# Security Policy

Veramem is designed as a security-first, deterministic, and verifiable cognitive kernel.

Security is a foundational property of the system.  
We welcome responsible disclosure and collaboration with the security and cryptography community.

---

## 1. Supported Versions

At the moment, the latest stable release of Veramem is supported.

Security patches will be prioritized for:

- the latest release,
- critical vulnerabilities affecting protocol integrity.

Earlier versions may not receive fixes unless they impact core protocol safety.

---

## 2. Reporting a Vulnerability

If you believe you have found a security vulnerability, please do not open a public issue.

Instead, report it privately:

- Email: jlefauconnier@proton.me
- Subject: `[VERAMEM SECURITY]`

Include:

- a clear description,
- affected components,
- potential impact,
- proof-of-concept if available,
- reproducibility steps.

We aim to acknowledge reports within 72 hours.

---

## 3. Responsible Disclosure

We follow a coordinated disclosure process:

1. Report privately.
2. We validate and assess impact.
3. A fix is developed.
4. Coordinated disclosure timeline is agreed.
5. Public advisory is released.

Researchers will be credited unless anonymity is requested.

---

## 4. Scope of Security

Security applies to:

- protocol correctness,
- deterministic encoding,
- commitment integrity,
- signal lineage safety,
- distributed convergence,
- attestation and trust,
- replay resistance,
- adversarial resilience.

Out of scope:

- vulnerabilities in third-party infrastructure,
- unrelated application-level misuse.

---

## 5. Security Principles

Veramem follows these core principles:

### 5.1 Determinism
All protocol operations must be reproducible.

### 5.2 Verifiability
Every state must be auditable and cryptographically verifiable.

### 5.3 Minimal Trust
The system assumes adversarial environments.

### 5.4 Explicit State
Hidden or implicit state is avoided.

### 5.5 Zero-Knowledge Design
Sensitive data should never be exposed in plaintext when not required.

---

## 6. Threat Model

The kernel assumes:

- malicious participants,
- network adversaries,
- Byzantine environments,
- compromised devices,
- replay and rollback attacks,
- data tampering.

See:

- `security/KERNEL_THREAT_MODEL.md`

---

## 7. Cryptographic Design

Key properties:

- deterministic commitments,
- domain separation,
- replay protection,
- forward compatibility.

Cryptographic changes require:

- security analysis,
- formal justification,
- interoperability considerations.

---

## 8. Attestation and Trust

Device and node trust must:

- be explicit,
- be verifiable,
- resist replay,
- support distributed trust.

See:

- `security/DEVICE_ATTESTATION_MODEL.md`

---

## 9. Supply Chain Security

We aim to:

- minimize dependencies,
- ensure reproducible builds,
- prevent hidden behavior.

Future roadmap includes:

- signed releases,
- deterministic packaging,
- transparency logs.

---

## 10. Secure Development

The project encourages:

- adversarial testing,
- fuzzing,
- property-based testing,
- formal verification.

See:

- `VERAMEM_FORMAL_VERIFICATION_PLAN.md`

---

## 11. Hardening and Future Work

Planned improvements:

- side-channel analysis,
- memory safety strategies,
- cryptographic agility,
- distributed consensus safety,
- long-term post-quantum migration.

---

## 12. Ethical Use

Veramem is intended for:

- privacy-preserving systems,
- cognitive integrity,
- user autonomy.

It is not designed for:

- mass surveillance,
- coercive monitoring,
- opaque centralized control.

---

## 13. Legal

This security policy does not grant authorization to:

- access private infrastructure,
- perform denial-of-service attacks,
- violate applicable laws.

Researchers must respect applicable regulations.

---

## 14. Community

We believe security is a collaborative effort.

We welcome:

- academic researchers,
- cryptographers,
- distributed systems experts.

---

Thank you for helping make Veramem a secure and trustworthy system.
