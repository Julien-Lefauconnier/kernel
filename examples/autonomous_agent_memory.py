"""
Autonomous Agent Memory Example (generic).

This example demonstrates:
- long-term memory for autonomous agents
- deterministic decision traceability
- auditability of agent evolution
- alignment and safety verification
- replayable cognitive history

The scenario is intentionally domain-agnostic.

It can represent:
- autonomous AI systems
- long-lived digital assistants
- robotic agents
- governance agents
- safety-critical autonomous decision systems
- aligned AI memory architectures

The goal is to show that Veramem enables safe, auditable,
and reproducible autonomous cognition.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal
from veramem_kernel.signals.lineage.signal_lineage_patch_builder import (
    build_signal_lineage_patch,
)
from veramem_kernel.signals.lineage.signal_lineage_patch_applier import (
    apply_signal_lineage_patch,
)


def print_agent_memory(name, timeline):
    print(f"\n{name} memory:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Autonomous agent runtime ---
    agent = TimelineJournal()

    print("Agent initialized with deterministic memory.")

    # Step 1 — perception
    observation = Signal(
        domain="agent",
        payload=b"Observation: environment contains obstacle"
    )
    agent.append(observation)

    # Step 2 — reasoning
    reasoning_v1 = Signal(
        domain="agent",
        payload=b"Reasoning: obstacle may block optimal path"
    )
    agent.append(reasoning_v1)

    # Step 3 — decision
    decision_v1 = Signal(
        domain="agent",
        payload=b"Decision: choose alternative route"
    )
    agent.append(decision_v1)

    # Step 4 — feedback
    feedback = Signal(
        domain="agent",
        payload=b"Feedback: route successful"
    )
    agent.append(feedback)

    # Step 5 — updated reasoning
    reasoning_v2 = Signal(
        domain="agent",
        payload=b"Updated reasoning: obstacle avoidance improves safety"
    )
    agent.append(reasoning_v2)

    # --- Lineage tracking of cognitive evolution ---
    lineage_state = {}

    patch = build_signal_lineage_patch(
        parents=[reasoning_v1.key],
        supersedes=reasoning_v1.key,
        child=reasoning_v2.key,
    )
    apply_signal_lineage_patch(patch, lineage_state)

    print("Agent cognitive evolution recorded.")

    print_agent_memory("Agent", agent)

    # --- Independent safety audit ---
    print("\nIndependent safety audit...")

    auditor = TimelineJournal()

    for entry in agent.entries():
        auditor.append_signal(entry.signal)

    print("Auditor reconstructed the agent history.")

    print_agent_memory("Auditor", auditor)

    # --- Deterministic verification ---
    if agent.head() == auditor.head():
        print("\nAgent memory verified.")
    else:
        print("\nVerification mismatch detected.")

    # --- Alignment traceability ---
    print("\nTraceable reasoning evolution:")
    print("Updated reasoning:", reasoning_v2.key)
    print("Supersedes:", reasoning_v1.key)


if __name__ == "__main__":
    main()
