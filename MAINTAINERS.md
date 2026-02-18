# Veramem Kernel — Maintainers

This document lists the current maintainers and governance roles of the Veramem Kernel project.

The goal of this file is to ensure transparency, continuity, and resilience of the project over time.

---

## 1. Current Maintainers

### Core Maintainer

**Julien Lefauconnier**  
Founder and initial author of the Veramem Kernel. 
He does not intend to maintain it indefinitly, the community is welcomed to take over.

Responsibilities:
- Architectural direction
- Review of critical changes
- Security-sensitive decisions
- Invariant and protocol integrity

Contact:
- See SECURITY.md for responsible disclosure and security-related contact.

---

## 2. Future Maintainers

The Veramem project is designed to become a **community-driven open standard**.

We actively welcome:
- Researchers in distributed systems, cryptography, and AI safety
- Open source contributors
- Protocol and infrastructure engineers
- Formal methods and verification experts

If you are interested in becoming a maintainer, please:
1. Start contributing through issues or pull requests.
2. Participate in design discussions.
3. Demonstrate long-term commitment to the project.

Maintainers are selected based on:
- Technical competence
- Alignment with the project philosophy (determinism, safety, abstention)
- Security awareness
- Constructive collaboration.

---

## 3. Maintainer Responsibilities

Maintainers are responsible for:

- Preserving protocol invariants and safety guarantees.
- Reviewing pull requests affecting:
  - canonical encoding,
  - timeline integrity,
  - signal lineage,
  - attestation and trust.
- Ensuring deterministic and reproducible behavior.
- Avoiding unsafe or ambiguous protocol changes.
- Maintaining backward compatibility.

Security-sensitive areas require **multi-review before merging**.

---

## 4. Decision Model

The project follows a **conservative governance model**:

- Safety over speed.
- Determinism over convenience.
- Stability over feature growth.

For critical protocol changes:
- Consensus among maintainers is required.
- If consensus cannot be reached, the change is rejected.

Abstention is considered a valid governance outcome.

---

## 5. Security and Responsible Disclosure

All security vulnerabilities must be reported according to the process described in:

SECURITY.md


Maintainers must:
- Coordinate disclosure,
- Ensure timely response,
- Prioritize user safety.

---

## 6. Conflict Resolution

In case of disagreement:

1. Technical discussion is preferred.
2. Formal reasoning and invariants take precedence.
3. If necessary, the conservative option is selected.

The project favors:
- correctness,
- long-term resilience,
- auditability.

---

## 7. Community Governance Evolution

As adoption grows, governance may evolve to include:

- A Technical Steering Committee (TSC),
- Multiple independent maintainers,
- Cryptography and formal verification reviewers,
- External advisory contributors.

The long-term objective is:

> A decentralized, resilient, and transparent governance model.

---

## 8. Maintainer Availability

Maintainers are volunteers and may not respond immediately.

If a maintainer becomes inactive:
- The community is encouraged to step in.
- New maintainers may be nominated through open discussion.

---

## 9. Becoming a Maintainer

To be considered for maintainership:

- Demonstrate sustained, high-quality contributions.
- Show deep understanding of the protocol.
- Uphold the project’s safety-first philosophy.

There is no fixed timeline. Trust is built progressively.

---

## 10. Final Note

The Veramem Kernel is designed to outlive any single individual.

Its long-term resilience depends on:
- openness,
- strong invariants,
- distributed stewardship.

We welcome contributors committed to these principles.
