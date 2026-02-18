"""
Resilient Distributed Cognition Example (generic).

This example demonstrates:
- multi-agent cognition
- decentralized memory
- resilience to node failure
- fork and reconciliation
- deterministic recovery
- traceable distributed reasoning

The scenario is intentionally domain-agnostic.

It can represent:
- distributed AI systems
- autonomous agent coordination
- edge intelligence
- robotic swarms
- critical infrastructure control
- space or defense systems
- collaborative cognition networks

The goal is to show that Veramem enables resilient and auditable
distributed cognition without central coordination.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def print_timeline(name, timeline):
    print(f"\n{name} memory:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Shared initial knowledge ---
    core = TimelineJournal()

    core.append_bytes(domain="cognition", payload=b"Shared baseline model")
    core.append_bytes(domain="cognition", payload=b"Initial environment understanding")

    print("Baseline cognition established.")

    # --- Distributed agents fork ---
    agent_a = fork_timeline(core)
    agent_b = fork_timeline(core)
    agent_c = fork_timeline(core)

    print("Agents deployed and operating independently.")

    # --- Independent learning and reasoning ---
    agent_a.append_bytes(
        domain="cognition",
        payload=b"Agent A: local observation and update"
    )

    agent_b.append_bytes(
        domain="cognition",
        payload=b"Agent B: anomaly detection"
    )

    agent_c.append_bytes(
        domain="cognition",
        payload=b"Agent C: predictive inference"
    )

    print("Agents evolved independently.")

    print_timeline("Agent A", agent_a)
    print_timeline("Agent B", agent_b)
    print_timeline("Agent C", agent_c)

    # --- Node failure simulation ---
    print("\nAgent B failure simulated.")

    # Agent B becomes unavailable (no data loss, just unreachable)

    # --- Continued operation ---
    agent_a.append_bytes(
        domain="cognition",
        payload=b"Agent A: continued reasoning despite failure"
    )

    agent_c.append_bytes(
        domain="cognition",
        payload=b"Agent C: adaptation to degraded environment"
    )

    # --- Recovery and reintegration ---
    print("\nAgent B recovers and synchronizes.")

    # Assume Agent B reconnects later and syncs
    recovered = merge_timelines(agent_a, agent_c)

    # Now merge recovered state back into B
    agent_b = merge_timelines(agent_b, recovered)

    print_timeline("Recovered global cognition", agent_b)

    # --- Deterministic convergence ---
    print("\nProperties demonstrated:")
    print("- No central coordinator required")
    print("- System continues despite node failures")
    print("- Deterministic reconciliation")
    print("- Full traceability of distributed reasoning")
    print("- Auditable cognitive evolution")
    print("- Resilience and recovery")


if __name__ == "__main__":
    main()
