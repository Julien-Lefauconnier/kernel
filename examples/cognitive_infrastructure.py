"""
Cognitive Infrastructure Example (generic).

This example demonstrates:
- a shared cognitive backbone
- humans, AI systems, and institutions interacting
- immutable knowledge evolution
- distributed cognition
- traceable decision processes
- long-term collective memory

The scenario is intentionally generic and domain-agnostic.

It can represent:
- global knowledge systems
- collaborative scientific reasoning
- multi-agent cognitive ecosystems
- institutional decision memory
- trustworthy AI infrastructures
- long-term civilization-scale cognition
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
    # Step 1 — Shared cognitive foundation
    # -----------------------------------------------------------------
    global_memory = TimelineJournal()

    global_memory.append_bytes(
        domain="foundation",
        payload=b"Shared cognitive infrastructure initialized",
    )

    global_memory.append_bytes(
        domain="foundation",
        payload=b"Common invariants and trust anchors established",
    )

    print("Global cognitive infrastructure created.")
    print_timeline("Global Memory", global_memory)

    # -----------------------------------------------------------------
    # Step 2 — Human contribution
    # -----------------------------------------------------------------
    human_node = fork_timeline(global_memory)

    human_node.append_bytes(
        domain="human_input",
        payload=b"Expert observation recorded",
    )

    human_node.append_bytes(
        domain="human_input",
        payload=b"Hypothesis proposed",
    )

    print("\nHuman knowledge contribution.")
    print_timeline("Human Node", human_node)

    # -----------------------------------------------------------------
    # Step 3 — AI system reasoning
    # -----------------------------------------------------------------
    ai_node = fork_timeline(human_node)

    ai_node.append_bytes(
        domain="ai_reasoning",
        payload=b"Model inference generated",
    )

    ai_node.append_bytes(
        domain="ai_reasoning",
        payload=b"Confidence and uncertainty quantified",
    )

    print("\nAI reasoning recorded.")
    print_timeline("AI Node", ai_node)

    # -----------------------------------------------------------------
    # Step 4 — Institutional validation
    # -----------------------------------------------------------------
    institution = fork_timeline(ai_node)

    institution.append_bytes(
        domain="governance",
        payload=b"Inference reviewed by regulatory body",
    )

    institution.append_bytes(
        domain="governance",
        payload=b"Decision approved and recorded",
    )

    print("\nInstitutional validation.")
    print_timeline("Institution", institution)

    # -----------------------------------------------------------------
    # Step 5 — Knowledge evolution
    # -----------------------------------------------------------------
    future = fork_timeline(institution)

    future.append_bytes(
        domain="evolution",
        payload=b"New evidence integrated",
    )

    future.append_bytes(
        domain="evolution",
        payload=b"Decision updated transparently",
    )

    print("\nKnowledge evolved over time.")
    print_timeline("Future", future)

    # -----------------------------------------------------------------
    # Step 6 — Independent verification
    # -----------------------------------------------------------------
    print("\nIndependent verification...")

    verifier = TimelineJournal()

    for entry in future.entries():
        verifier.append_signal(entry.signal)

    if future.head() == verifier.head():
        print("Cognitive process verified.")
    else:
        print("Verification failed.")

    # -----------------------------------------------------------------
    # Step 7 — Shared global state
    # -----------------------------------------------------------------
    global_state = merge_timelines(global_memory, future)

    print("\nGlobal cognitive state:")
    print_timeline("Global State", global_state)

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Human + AI collaboration")
    print("- Institutional oversight")
    print("- Immutable cognitive trace")
    print("- Transparent knowledge evolution")
    print("- Distributed cognition")
    print("- Long-term collective memory")
    print("- Auditable decision pipelines")


if __name__ == "__main__":
    main()
