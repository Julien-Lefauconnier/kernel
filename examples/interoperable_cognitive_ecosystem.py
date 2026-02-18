"""
Interoperable Cognitive Ecosystem Example (generic).

This example demonstrates:
- heterogeneous cognitive systems
- interoperability across vendors and domains
- shared trust and auditability
- portable memory and reasoning traces
- ecosystem-level coordination

The scenario is intentionally generic.

It can represent:
- multi-vendor AI ecosystems
- cloud + edge collaboration
- institutional interoperability
- cross-platform autonomous systems
- research + industry cognitive exchange
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
    # Step 1 — Shared interoperability backbone
    # -----------------------------------------------------------------
    backbone = TimelineJournal()

    backbone.append_bytes(
        domain="interop",
        payload=b"Common cognitive interoperability layer initialized",
    )

    backbone.append_bytes(
        domain="interop",
        payload=b"Shared invariants and encoding agreed",
    )

    print("Interoperability backbone created.")
    print_timeline("Backbone", backbone)

    # -----------------------------------------------------------------
    # Step 2 — Vendor A AI system
    # -----------------------------------------------------------------
    vendor_a = fork_timeline(backbone)

    vendor_a.append_bytes(
        domain="vendor_a",
        payload=b"Model A inference recorded",
    )

    vendor_a.append_bytes(
        domain="vendor_a",
        payload=b"Reasoning trace exported",
    )

    print("\nVendor A system.")
    print_timeline("Vendor A", vendor_a)

    # -----------------------------------------------------------------
    # Step 3 — Vendor B AI system
    # -----------------------------------------------------------------
    vendor_b = fork_timeline(backbone)

    vendor_b.append_bytes(
        domain="vendor_b",
        payload=b"Model B analysis recorded",
    )

    vendor_b.append_bytes(
        domain="vendor_b",
        payload=b"Confidence and calibration provided",
    )

    print("\nVendor B system.")
    print_timeline("Vendor B", vendor_b)

    # -----------------------------------------------------------------
    # Step 4 — Edge autonomous agents
    # -----------------------------------------------------------------
    edge = fork_timeline(vendor_a)

    edge.append_bytes(
        domain="edge",
        payload=b"Local environment observations",
    )

    edge.append_bytes(
        domain="edge",
        payload=b"Decision executed autonomously",
    )

    print("\nEdge agent execution.")
    print_timeline("Edge", edge)

    # -----------------------------------------------------------------
    # Step 5 — Institutional validation
    # -----------------------------------------------------------------
    governance = fork_timeline(vendor_b)

    governance.append_bytes(
        domain="governance",
        payload=b"Independent audit of vendor outputs",
    )

    governance.append_bytes(
        domain="governance",
        payload=b"Regulatory decision recorded",
    )

    print("\nInstitutional validation.")
    print_timeline("Governance", governance)

    # -----------------------------------------------------------------
    # Step 6 — Interoperable merge
    # -----------------------------------------------------------------
    merged = merge_timelines(edge, governance)

    print("\nMerged cognitive ecosystem state.")
    print_timeline("Merged", merged)

    # -----------------------------------------------------------------
    # Step 7 — Independent verification
    # -----------------------------------------------------------------
    print("\nIndependent ecosystem verification...")

    verifier = TimelineJournal()

    for entry in merged.entries():
        verifier.append_signal(entry.signal)

    if merged.head() == verifier.head():
        print("Ecosystem state verified.")
    else:
        print("Verification failed.")

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Cross-vendor interoperability")
    print("- Portable reasoning traces")
    print("- Auditable ecosystem-level cognition")
    print("- Cloud + edge + institutional collaboration")
    print("- Long-term trust across heterogeneous systems")


if __name__ == "__main__":
    main()
