"""
Multi-Agent Coordination Example (generic).

This example demonstrates:
- distributed autonomous agents
- shared deterministic memory
- coordination without central authority
- conflict traceability
- reproducible collective behavior
- auditable decision history

The scenario is intentionally domain-agnostic.

It can represent:
- robotics and swarm systems
- autonomous vehicles
- distributed AI systems
- cooperative decision-making
- decentralized infrastructures
- collective optimization
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
    # Shared initial state
    # -----------------------------------------------------------------
    shared = TimelineJournal()

    shared.append_bytes(
        domain="coordination",
        payload=b"Initial shared mission",
    )

    print("Initial coordination state created.")

    # -----------------------------------------------------------------
    # Autonomous agents fork independently
    # -----------------------------------------------------------------
    agent_a = fork_timeline(shared)
    agent_b = fork_timeline(shared)
    agent_c = fork_timeline(shared)

    print("Agents forked from shared memory.")

    # -----------------------------------------------------------------
    # Agents perform local observations and decisions
    # -----------------------------------------------------------------
    agent_a.append_bytes(
        domain="observation",
        payload=b"Agent A detected condition X",
    )
    agent_a.append_bytes(
        domain="decision",
        payload=b"Agent A proposes action Alpha",
    )

    agent_b.append_bytes(
        domain="observation",
        payload=b"Agent B detected condition Y",
    )
    agent_b.append_bytes(
        domain="decision",
        payload=b"Agent B proposes action Beta",
    )

    agent_c.append_bytes(
        domain="observation",
        payload=b"Agent C detected conflicting signal",
    )
    agent_c.append_bytes(
        domain="decision",
        payload=b"Agent C proposes action Alpha",
    )

    print("Agents produced local decisions.")

    print_timeline("Agent A", agent_a)
    print_timeline("Agent B", agent_b)
    print_timeline("Agent C", agent_c)

    # -----------------------------------------------------------------
    # Deterministic merge of agent knowledge
    # -----------------------------------------------------------------
    merged_ab = merge_timelines(agent_a, agent_b)
    merged_all = merge_timelines(merged_ab, agent_c)

    print("\nMerged collective state:")
    print_timeline("Collective", merged_all)

    # -----------------------------------------------------------------
    # Conflict traceability
    # -----------------------------------------------------------------
    print("\nConflict traceability:")
    for entry in merged_all.entries():
        payload = entry.signal.payload.decode()
        if "proposes" in payload:
            print("-", payload)

    # -----------------------------------------------------------------
    # Independent verifier
    # -----------------------------------------------------------------
    print("\nIndependent coordination verifier...")

    verifier = TimelineJournal()

    for entry in merged_all.entries():
        verifier.append_signal(entry.signal)

    if merged_all.head() == verifier.head():
        print("Deterministic coordination verified.")
    else:
        print("Mismatch detected.")

    # -----------------------------------------------------------------
    # Key properties
    # -----------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Autonomous agents coordination")
    print("- No central authority required")
    print("- Deterministic merge of knowledge")
    print("- Full decision traceability")
    print("- Conflict transparency")
    print("- Reproducible collective behavior")


if __name__ == "__main__":
    main()
