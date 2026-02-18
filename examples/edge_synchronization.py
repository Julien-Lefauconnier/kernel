"""
Edge Synchronization Example (generic).

This example demonstrates:
- offline edge operation
- local append-only recording
- network partition tolerance
- delayed synchronization
- deterministic merge after reconnection
- resilience to intermittent connectivity

The scenario is intentionally domain-agnostic.

It can represent:
- IoT and sensor networks
- autonomous systems
- mobile or remote infrastructure
- field operations
- distributed monitoring
- edge AI cognition
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # ---------------------------------------------------------------
    # Initial shared state
    # ---------------------------------------------------------------
    central = TimelineJournal()

    central.append_bytes(
        domain="system",
        payload=b"Initial shared baseline",
    )

    print("Central baseline established.")

    # ---------------------------------------------------------------
    # Edge devices fork while connected
    # ---------------------------------------------------------------
    edge_a = fork_timeline(central)
    edge_b = fork_timeline(central)

    print("Edge devices synchronized and then disconnected.")

    # ---------------------------------------------------------------
    # Network partition (offline operation)
    # ---------------------------------------------------------------
    edge_a.append_bytes(
        domain="edge",
        payload=b"Edge A local observation",
    )

    edge_a.append_bytes(
        domain="edge",
        payload=b"Edge A anomaly detected",
    )

    edge_b.append_bytes(
        domain="edge",
        payload=b"Edge B routine monitoring",
    )

    print("Offline operations recorded independently.")

    print_timeline("Edge A (offline)", edge_a)
    print_timeline("Edge B (offline)", edge_b)

    # ---------------------------------------------------------------
    # Reconnection and synchronization
    # ---------------------------------------------------------------
    print("\nEdges reconnecting to central system...")

    merged = merge_timelines(edge_a, edge_b)

    print_timeline("Merged global state", merged)

    # ---------------------------------------------------------------
    # Deterministic verification
    # ---------------------------------------------------------------
    verifier = TimelineJournal()

    for entry in merged.entries():
        verifier.append_signal(entry.signal)

    if verifier.head() == merged.head():
        print("\nDeterministic synchronization verified.")
    else:
        print("\nSynchronization mismatch detected.")

    # ---------------------------------------------------------------
    # Traceability of distributed events
    # ---------------------------------------------------------------
    print("\nTraceability of distributed operations:")
    for entry in merged.entries():
        payload = entry.signal.payload.decode()
        if "Edge" in payload:
            print("-", payload)

    # ---------------------------------------------------------------
    # Key properties
    # ---------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Offline-first architecture")
    print("- Partition tolerance")
    print("- Deterministic reconciliation")
    print("- No central authority required")
    print("- Full traceability of edge activity")
    print("- Resilient distributed cognition")


if __name__ == "__main__":
    main()
