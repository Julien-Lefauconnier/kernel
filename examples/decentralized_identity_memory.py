"""
Decentralized Identity Memory Example (generic).

This example demonstrates:
- portable identity memory
- decentralized attestations
- sovereign long-term identity
- traceable evolution of identity claims
- auditability across independent verifiers
- resilience against central authority failures

The scenario is intentionally domain-agnostic.

It can represent:
- Self-Sovereign Identity (SSI)
- digital identity wallets
- decentralized credentials
- lifelong verifiable memory
- reputation and trust systems
- cross-border identity infrastructures

The goal is to show that Veramem enables identity systems
that are portable, auditable, and independent of centralized control.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal
from veramem_kernel.signals.lineage.signal_lineage_patch_builder import (
    build_signal_lineage_patch,
)
from veramem_kernel.signals.lineage.signal_lineage_patch_applier import (
    apply_signal_lineage_patch,
)


def print_identity(name, timeline):
    print(f"\n{name} identity memory:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Identity owner ---
    identity = TimelineJournal()

    print("Decentralized identity initialized.")

    # Step 1 — initial identity claim
    claim_v1 = Signal(
        domain="identity",
        payload=b"Identity claim: owner established"
    )
    identity.append(claim_v1)

    # Step 2 — decentralized attestation (issuer A)
    attestation_a = Signal(
        domain="identity",
        payload=b"Attestation: verified attribute by issuer A"
    )
    identity.append(attestation_a)

    # Step 3 — decentralized attestation (issuer B)
    attestation_b = Signal(
        domain="identity",
        payload=b"Attestation: verified credential by issuer B"
    )
    identity.append(attestation_b)

    # Step 4 — identity evolution
    claim_v2 = Signal(
        domain="identity",
        payload=b"Identity claim updated: new verified attributes"
    )
    identity.append(claim_v2)

    # --- Traceable identity evolution ---
    lineage_state = {}

    patch = build_signal_lineage_patch(
        parents=[claim_v1.key],
        supersedes=claim_v1.key,
        child=claim_v2.key,
    )
    apply_signal_lineage_patch(patch, lineage_state)

    print("Identity evolution recorded with traceability.")

    print_identity("Owner", identity)

    # --- Independent verifier ---
    print("\nIndependent verifier reconstructs identity...")

    verifier = TimelineJournal()

    for entry in identity.entries():
        verifier.append_signal(entry.signal)

    print_identity("Verifier", verifier)

    # --- Deterministic verification ---
    if identity.head() == verifier.head():
        print("\nIdentity verified deterministically.")
    else:
        print("\nVerification mismatch detected.")

    # --- Long-term resilience ---
    print("\nProperties demonstrated:")
    print("- Identity is portable and sovereign")
    print("- No central authority required")
    print("- Attestations remain auditable")
    print("- Evolution is traceable")
    print("- Independent verification is possible")


if __name__ == "__main__":
    main()
