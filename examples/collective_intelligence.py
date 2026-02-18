"""
Collective Intelligence Example (generic).

This example demonstrates:
- decentralized contributions
- independent knowledge evolution
- divergence and hypothesis competition
- deterministic reconciliation
- traceable collective convergence

The scenario is intentionally domain-agnostic.

It can represent:
- multi-agent AI systems
- scientific collaboration
- swarm intelligence
- decentralized research
- collective decision-making
- distributed epistemic systems

The goal is to show how Veramem enables:
- transparent coordination without central authority
- auditable knowledge evolution
- reproducible collective reasoning
"""

import hashlib
from typing import List

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def stable_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def print_timeline(name: str, timeline: TimelineJournal):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # ------------------------------------------------------------------
    # Shared baseline: collective starting point
    # ------------------------------------------------------------------
    collective = TimelineJournal()

    shared_fact = collective.append_bytes(
        domain="collective",
        payload=b"Initial shared observation"
    )

    print("Collective baseline established.")

    # ------------------------------------------------------------------
    # Independent agents fork from shared state
    # ------------------------------------------------------------------
    agent_a = fork_timeline(collective)
    agent_b = fork_timeline(collective)
    agent_c = fork_timeline(collective)

    print("Agents A, B, and C started independent exploration.")

    # ------------------------------------------------------------------
    # Divergent hypotheses
    # ------------------------------------------------------------------
    agent_a.append_bytes(
        domain="collective",
        payload=b"Hypothesis A: explanation based on model X"
    )

    agent_b.append_bytes(
        domain="collective",
        payload=b"Hypothesis B: alternative interpretation using model Y"
    )

    agent_c.append_bytes(
        domain="collective",
        payload=b"Hypothesis C: data-driven explanation"
    )

    print("Agents generated competing hypotheses.")

    print_timeline("Agent A", agent_a)
    print_timeline("Agent B", agent_b)
    print_timeline("Agent C", agent_c)

    # ------------------------------------------------------------------
    # Iterative improvement and evidence gathering
    # ------------------------------------------------------------------
    evidence_a = stable_hash(b"dataset-1")
    evidence_b = stable_hash(b"dataset-2")

    agent_a.append_bytes(
        domain="collective",
        payload=f"Agent A supports hypothesis with evidence {evidence_a}".encode()
    )

    agent_b.append_bytes(
        domain="collective",
        payload=f"Agent B refines hypothesis using {evidence_b}".encode()
    )

    agent_c.append_bytes(
        domain="collective",
        payload=f"Agent C integrates both datasets {evidence_a} + {evidence_b}".encode()
    )

    print("\nAgents iteratively refined knowledge.")

    # ------------------------------------------------------------------
    # First deterministic merge (partial convergence)
    # ------------------------------------------------------------------
    merged_ab = merge_timelines(agent_a, agent_b)
    print("\nPartial convergence between A and B.")

    print_timeline("Merged A+B", merged_ab)

    # ------------------------------------------------------------------
    # Global reconciliation
    # ------------------------------------------------------------------
    global_state = merge_timelines(merged_ab, agent_c)

    print("\nGlobal deterministic reconciliation.")

    print_timeline("Global collective state", global_state)

    # ------------------------------------------------------------------
    # Independent verifier
    # ------------------------------------------------------------------
    verifier = TimelineJournal()
    for entry in global_state.entries():
        verifier.append_signal(entry.signal)

    print("\nIndependent verification:")

    if verifier.head() == global_state.head():
        print("- Deterministic collective convergence verified.")
    else:
        print("- Integrity mismatch detected.")

    # ------------------------------------------------------------------
    # Emergent properties
    # ------------------------------------------------------------------
    print("\nEmergent properties demonstrated:")
    print("- Decentralized collaboration without central coordination")
    print("- Competing hypotheses recorded immutably")
    print("- Transparent and auditable convergence")
    print("- Reproducible collective reasoning")
    print("- Traceable epistemic evolution")


if __name__ == "__main__":
    main()
