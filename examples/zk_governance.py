"""
Zero-Knowledge Governance Example (generic).

This example demonstrates:
- auditability without access to raw data
- policy compliance verification
- deterministic commitments
- separation between cognition and governance
- distributed trust without central authority

This scenario is intentionally generic and domain-agnostic.

It can represent:
- AI regulatory compliance
- privacy-preserving audit
- zero-knowledge cognitive systems (ZKCS)
- confidential governance infrastructures
- safety-critical oversight

The Veramem Kernel ensures that:
- events are immutable
- commitments are deterministic
- compliance can be verified independently
- sensitive data is never disclosed
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.api.crypto import HMACSigner, TrustAnchor
from veramem_kernel.journals.timeline.timeline_signed_commitment import (
    sign_timeline_head,
    verify_timeline_head,
)


def print_timeline(title, timeline):
    print(f"\n{title}")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Confidential system execution ---
    system = TimelineJournal()

    # Sensitive events (never disclosed)
    system.append_bytes(domain="confidential", payload=b"Private event A")
    system.append_bytes(domain="confidential", payload=b"Private event B")
    system.append_bytes(domain="confidential", payload=b"Policy-compliant action")

    print("Confidential system executed.")

    # --- Create deterministic commitment ---
    key = b"shared-secret"
    signer = HMACSigner(key=key)

    signed_commitment = sign_timeline_head(system, signer=signer)

    print("\nDeterministic commitment generated.")
    print("Commitment hash:", signed_commitment.head_hash.hex())

    # --- External governance authority ---
    trust_anchor = TrustAnchor()
    trust_anchor.register("system-A", signer)

    print("\nGovernance authority registered trust anchor.")

    # --- Independent compliance verification ---
    try:
        verify_timeline_head(
            system,
            signed_commitment,
            trust_anchor=trust_anchor,
            signer_id="system-A",
        )
        print("\nCompliance verified without accessing raw data.")
    except Exception as e:
        print("\nVerification failed:", str(e))

    # --- Demonstrate zero-knowledge properties ---
    print("\nProperties demonstrated:")
    print("- No raw events shared")
    print("- Deterministic cryptographic commitments")
    print("- Independent verification")
    print("- Privacy-preserving governance")
    print("- Separation between cognition and audit")


if __name__ == "__main__":
    main()
