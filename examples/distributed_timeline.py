"""
Distributed Timeline Example (generic).

This example demonstrates:
- independent nodes
- forked timelines
- divergence
- deterministic reconciliation
- traceable merge

This scenario is intentionally generic and domain-agnostic.

It can represent:
- distributed AI systems
- multi-agent cognition
- decentralized infrastructure
- audit and compliance
- edge synchronization
- collaborative knowledge systems

The goal is to show that Veramem enables safe and deterministic
distributed state evolution without central coordination.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # Node A (initial shared state)
    node_a = TimelineJournal()

    s1 = node_a.append_bytes(domain="generic", payload=b"Initial shared fact")
    print("Initial state created.")

    # Node B and Node C fork independently
    node_b = fork_timeline(node_a)
    node_c = fork_timeline(node_a)

    print("Nodes B and C forked from A.")

    # Divergence
    node_b.append_bytes(domain="generic", payload=b"Node B local update")
    node_c.append_bytes(domain="generic", payload=b"Node C local update")

    print("Nodes diverged.")

    print_timeline("Node B", node_b)
    print_timeline("Node C", node_c)

    # Merge back
    merged = merge_timelines(node_b, node_c)

    print("\nMerged state (deterministic):")
    print_timeline("Merged", merged)

    print("\nProperties demonstrated:")
    print("- No central authority required")
    print("- Deterministic merge")
    print("- Full traceability of divergence")
    print("- Replayable distributed history")


if __name__ == "__main__":
    main()
