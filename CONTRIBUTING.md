# Contributing to Veramem

Thank you for your interest in contributing to Veramem.

This project aims to build a **deterministic, verifiable, and privacy-preserving memory kernel** designed for long-term memory systems and distributed trust.

Because Veramem is intended to become a **global open standard**, contributions must meet high requirements in terms of:

- correctness,
- determinism,
- security,
- formal rigor,
- interoperability.

---

## 1. Contribution Philosophy

Veramem follows a research-grade and security-first development model.

Key principles:

- Determinism over convenience.
- Security over performance.
- Formal invariants over informal assumptions.
- Simplicity over complexity.
- Explicitness over hidden behavior.

All contributions should align with these goals.

---

## 2. Types of Contributions

We welcome contributions in the following areas:

### 2.1 Protocol and Core Kernel
Examples:
- timeline model improvements,
- signal lineage formalization,
- synchronization and distributed correctness,
- attestation and trust.

This category requires strong review and formal justification.

---

### 2.2 Formal and Mathematical Models
Examples:
- invariant proofs,
- formal semantics,
- distributed convergence properties,
- adversarial analysis.

These contributions are highly valued.

---

### 2.3 Security
Examples:
- threat modeling,
- attack surface reduction,
- side-channel resilience,
- replay and tamper resistance.

Security contributions should be discussed before implementation.

---

### 2.4 Interoperability and Standards
Examples:
- protocol compatibility,
- reference vectors,
- conformance suites.

---

### 2.5 Testing and Verification
Examples:
- property-based tests,
- fuzzing,
- adversarial testing,
- deterministic replay.

---

### 2.6 Documentation
Examples:
- clarifying specifications,
- diagrams,
- architecture explanations.

Documentation quality is critical for adoption.

---

## 3. Contribution Workflow

### 3.1 Discuss before large changes

Before implementing significant changes:

- open a GitHub issue,
- describe the motivation,
- explain the security and determinism impact.

This avoids unnecessary work and preserves architectural coherence.

---

### 3.2 Fork and Branch

Create a feature branch:

```bash
git checkout -b feature/my-contribution
```

---

### 3.3 Write tests first (recommended)

All core logic must include:

- unit tests,
- invariant checks,
- deterministic behavior validation.

The kernel must remain reproducible.

---

## 3.4 Run the full test suite

```bash
pytest
pytest conformance/
```

All tests must pass.

---

## 3.5 Pull Request

Include:

- clear motivation,
- security considerations,
- formal implications,
- backward compatibility analysis.

---

### 4. Determinism and Reproducibility

The kernel must be deterministic across:

- environments,
- machines,
- time.

Avoid:

- non-deterministic ordering,
- system time dependencies,
- floating-point ambiguity,
- implicit randomness.

If randomness is required, it must be explicit and controlled.

---

### 5. Security Guidelines

Never introduce:

- implicit trust assumptions,
- hidden cryptographic state,
- side effects in verification paths.

Cryptographic changes must:

- include a threat model,
- justify algorithm choice,
- document attack resistance.

For vulnerability reports, see:

- `SECURITY.md`

---

### 6. Coding Standards

General rules:

- Explicit typing where possible,
- Minimal dependencies,
- Clear and readable code,
- No unnecessary abstraction.

We prioritize:

- clarity,
- auditability,
- long-term maintainability.

---

### 7. Backward Compatibility

Protocol-breaking changes require:

- versioning,
- migration strategy,
- interoperability considerations.

---

### 8. Formal Invariants

Any modification affecting:

- timelines,
- signal lineage,
- commitments,
- attestation,

must preserve or strengthen the formal invariants.

See:

- `protocol/TIMELINE_FORMAL_INVARIANTS.md`
- `protocol/SIGNAL_LINEAGE_FORMAL_INVARIANTS.md`

---

### 9. Conformance and Interoperability

Changes affecting protocol semantics must include:

- updated conformance fixtures,
- compatibility checks,
- deterministic encoding validation.

---

### 10. Ethical and Governance Considerations

Veramem is designed for:

- privacy,
- cognitive integrity,
- distributed trust.

Contributions that introduce:

- mass surveillance,
- centralized control,
- opaque systems,

will not be accepted.

---

### 11. License

By contributing, you agree that your work will be licensed under the project’s open-source license.

---

### 12. Research Contributions

We strongly encourage:

- academic collaboration,
- peer-reviewed validation,
- formal verification work.

See:

- `docs/research/VERAMEM_RESEARCH_ROADMAP.md`

---

### 13. Community

We aim to build a long-term, open, and neutral ecosystem.

Constructive discussions and respectful collaboration are essential.

---

Thank you for helping build the future of verifiable memory.