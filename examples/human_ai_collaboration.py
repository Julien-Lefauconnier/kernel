"""
Human–AI Collaboration Example (generic).

This example demonstrates:
- traceable collaboration between humans and AI
- immutable recording of decisions and reasoning steps
- explainability and accountability
- deterministic reconstruction of collaborative workflows
- auditability of human overrides
- safe co-pilot systems

The scenario is intentionally domain-agnostic.

It can represent:
- decision support systems
- medical or legal co-pilot
- regulated enterprise workflows
- AI governance and oversight
- human-in-the-loop safety systems
"""

from veramem_kernel.api.timeline import TimelineJournal


def print_timeline(name: str, timeline: TimelineJournal):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # ---------------------------------------------------------------
    # Collaborative system initialization
    # ---------------------------------------------------------------
    collaboration = TimelineJournal()

    collaboration.append_bytes(
        domain="system",
        payload=b"Human_AI collaboration session initialized",
    )

    print("Collaboration session started.")

    # ---------------------------------------------------------------
    # AI analysis phase
    # ---------------------------------------------------------------
    collaboration.append_bytes(
        domain="ai",
        payload=b"AI analyzed dataset and detected potential risk pattern",
    )

    collaboration.append_bytes(
        domain="ai",
        payload=b"AI proposed mitigation strategy A",
    )

    print("AI completed initial analysis.")

    # ---------------------------------------------------------------
    # Human review phase
    # ---------------------------------------------------------------
    collaboration.append_bytes(
        domain="human",
        payload=b"Human expert reviewed AI analysis",
    )

    collaboration.append_bytes(
        domain="human",
        payload=b"Human requested additional evidence",
    )

    collaboration.append_bytes(
        domain="ai",
        payload=b"AI provided supporting evidence",
    )

    print("Human–AI interaction recorded.")

    # ---------------------------------------------------------------
    # Human override scenario
    # ---------------------------------------------------------------
    collaboration.append_bytes(
        domain="human",
        payload=b"Human rejected mitigation strategy A",
    )

    collaboration.append_bytes(
        domain="human",
        payload=b"Human selected alternative strategy B",
    )

    print("Human override recorded.")

    # ---------------------------------------------------------------
    # Execution phase
    # ---------------------------------------------------------------
    collaboration.append_bytes(
        domain="system",
        payload=b"Strategy B executed",
    )

    collaboration.append_bytes(
        domain="system",
        payload=b"Outcome monitored",
    )

    print("Execution recorded.")

    print_timeline("Collaboration timeline", collaboration)

    # ---------------------------------------------------------------
    # Deterministic reconstruction
    # ---------------------------------------------------------------
    print("\n--- Deterministic reconstruction ---")

    replay = TimelineJournal()

    for entry in collaboration.entries():
        replay.append_signal(entry.signal)

    print_timeline("Reconstructed session", replay)

    if collaboration.head() == replay.head():
        print("\nDeterministic replay verified.")
    else:
        print("\nReplay mismatch detected.")

    # ---------------------------------------------------------------
    # Accountability and explainability
    # ---------------------------------------------------------------
    print("\n--- Explainability and accountability ---")

    ai_actions = []
    human_actions = []

    for entry in collaboration.entries():
        payload = entry.signal.payload.decode()

        if "AI" in payload:
            ai_actions.append(payload)
        if "Human" in payload:
            human_actions.append(payload)

    print("\nAI contributions:")
    for action in ai_actions:
        print("-", action)

    print("\nHuman decisions:")
    for action in human_actions:
        print("-", action)

    # ---------------------------------------------------------------
    # Audit perspective
    # ---------------------------------------------------------------
    print("\n--- Independent audit ---")

    auditor = TimelineJournal()

    for entry in collaboration.entries():
        auditor.append_signal(entry.signal)

    if auditor.head() == collaboration.head():
        print("Audit verified: collaboration trace is consistent.")
    else:
        print("Audit failure detected.")

    # ---------------------------------------------------------------
    # Key properties
    # ---------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Human–AI co-pilot traceability")
    print("- Override and accountability")
    print("- Deterministic replay")
    print("- Explainability by construction")
    print("- Audit-ready workflows")
    print("- Governance and compliance support")


if __name__ == "__main__":
    main()
