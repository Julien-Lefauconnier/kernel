"""
Supply Chain Integrity Example (generic).

This example demonstrates:
- end-to-end traceability
- immutable provenance
- deterministic audit
- distributed participants
- tamper-evident history
- compliance and verification

The scenario is intentionally domain-agnostic.

It can represent:
- manufacturing and logistics
- pharmaceutical traceability
- food safety
- aerospace supply chains
- regulated industrial environments
- critical infrastructure verification
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
    # Step 1 — Raw material origin
    # -----------------------------------------------------------------
    origin = TimelineJournal()

    origin.append_bytes(
        domain="supply_chain",
        payload=b"Raw material extracted at certified source",
    )

    print("Origin recorded.")

    # -----------------------------------------------------------------
    # Step 2 — Manufacturing and processing nodes fork
    # -----------------------------------------------------------------
    manufacturer = fork_timeline(origin)
    processor = fork_timeline(origin)

    manufacturer.append_bytes(
        domain="manufacturing",
        payload=b"Material transformed into intermediate component",
    )

    processor.append_bytes(
        domain="processing",
        payload=b"Quality and safety inspection performed",
    )

    print("Manufacturing and inspection recorded.")

    print_timeline("Manufacturer", manufacturer)
    print_timeline("Processor", processor)

    # -----------------------------------------------------------------
    # Step 3 — Deterministic merge of records
    # -----------------------------------------------------------------
    combined = merge_timelines(manufacturer, processor)

    print("\nCombined traceability:")
    print_timeline("Combined", combined)

    # -----------------------------------------------------------------
    # Step 4 — Logistics and distribution
    # -----------------------------------------------------------------
    logistics = fork_timeline(combined)

    logistics.append_bytes(
        domain="logistics",
        payload=b"Secure transport with monitored conditions",
    )

    logistics.append_bytes(
        domain="logistics",
        payload=b"Delivery to distribution center",
    )

    print("\nLogistics recorded.")
    print_timeline("Logistics", logistics)

    # -----------------------------------------------------------------
    # Step 5 — Retail or deployment
    # -----------------------------------------------------------------
    deployment = fork_timeline(logistics)

    deployment.append_bytes(
        domain="deployment",
        payload=b"Final product assembled and validated",
    )

    deployment.append_bytes(
        domain="deployment",
        payload=b"Product delivered to end user",
    )

    print("\nDeployment recorded.")
    print_timeline("Deployment", deployment)

    # -----------------------------------------------------------------
    # Step 6 — Independent regulator audit
    # -----------------------------------------------------------------
    print("\nRegulatory audit...")

    regulator = TimelineJournal()

    for entry in deployment.entries():
        regulator.append_signal(entry.signal)

    if deployment.head() == regulator.head():
        print("Audit successful: traceability verified.")
    else:
        print("Audit failure: mismatch detected.")

    # -----------------------------------------------------------------
    # Step 7 — Provenance review
    # -----------------------------------------------------------------
    print("\nEnd-to-end provenance:")
    for entry in deployment.entries():
        print("-", entry.signal.payload.decode())

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- End-to-end traceability")
    print("- Tamper-evident history")
    print("- Deterministic verification")
    print("- Distributed participants")
    print("- Compliance-ready audit")
    print("- Supply chain transparency")


if __name__ == "__main__":
    main()
