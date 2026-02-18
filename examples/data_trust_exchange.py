"""
Data Trust Exchange Example (generic).

This example demonstrates:
- trusted data exchange between organizations
- immutable audit trails
- provenance and lineage
- verifiable sharing
- independent verification
- regulatory and compliance workflows

The scenario is intentionally domain-agnostic.

It can represent:
- healthcare data sharing
- financial reporting
- regulated research
- inter-organizational AI training
- confidential industrial collaboration
- secure public-private data exchange
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # -----------------------------------------------------------------
    # Step 1 — Organization A produces data
    # -----------------------------------------------------------------
    org_a = TimelineJournal()

    org_a.append_bytes(
        domain="data_production",
        payload=b"Dataset created under controlled conditions",
    )

    org_a.append_bytes(
        domain="data_production",
        payload=b"Data validated and quality checked",
    )

    print("Organization A produced trusted data.")
    print_timeline("Org A", org_a)

    # -----------------------------------------------------------------
    # Step 2 — Data sharing agreement
    # -----------------------------------------------------------------
    agreement = fork_timeline(org_a)

    agreement.append_bytes(
        domain="governance",
        payload=b"Data sharing agreement signed between Org A and Org B",
    )

    agreement.append_bytes(
        domain="governance",
        payload=b"Access rights and obligations defined",
    )

    print("\nData sharing agreement recorded.")
    print_timeline("Agreement", agreement)

    # -----------------------------------------------------------------
    # Step 3 — Secure transfer to Organization B
    # -----------------------------------------------------------------
    org_b = fork_timeline(agreement)

    org_b.append_bytes(
        domain="data_transfer",
        payload=b"Dataset securely transferred to Organization B",
    )

    org_b.append_bytes(
        domain="data_transfer",
        payload=b"Integrity verified after transfer",
    )

    print("\nOrganization B received and verified the data.")
    print_timeline("Org B", org_b)

    # -----------------------------------------------------------------
    # Step 4 — Derived data or analysis
    # -----------------------------------------------------------------
    derived = fork_timeline(org_b)

    derived.append_bytes(
        domain="analysis",
        payload=b"Derived model or report generated",
    )

    derived.append_bytes(
        domain="analysis",
        payload=b"Traceable link to original dataset maintained",
    )

    print("\nDerived knowledge recorded.")
    print_timeline("Derived", derived)

    # -----------------------------------------------------------------
    # Step 5 — Independent regulator or auditor
    # -----------------------------------------------------------------
    print("\nIndependent audit...")

    auditor = TimelineJournal()

    for entry in derived.entries():
        auditor.append_signal(entry.signal)

    if derived.head() == auditor.head():
        print("Audit successful: exchange and usage verified.")
    else:
        print("Audit failure: inconsistency detected.")

    # -----------------------------------------------------------------
    # Step 6 — Deterministic merge for shared trust
    # -----------------------------------------------------------------
    shared = merge_timelines(org_a, derived)

    print("\nShared trust state:")
    print_timeline("Shared", shared)

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Trusted inter-organizational exchange")
    print("- Immutable provenance")
    print("- Deterministic verification")
    print("- Compliance and governance")
    print("- Transparent lineage")
    print("- Auditable collaboration")


if __name__ == "__main__":
    main()
