"""
Adaptive Policy System Example (generic).

This example demonstrates:
- evolving policies
- traceable governance
- auditable rule changes
- deterministic system behavior
- historical policy replay
- compliance and accountability

The scenario is intentionally domain-agnostic.

It can represent:
- AI governance and regulation
- financial compliance
- safety and security systems
- infrastructure governance
- regulated decision frameworks
- autonomous system supervision
"""

from veramem_kernel.api.timeline import TimelineJournal


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # ---------------------------------------------------------------
    # Initial system state
    # ---------------------------------------------------------------
    system = TimelineJournal()

    # Initial baseline policy
    system.append_bytes(
        domain="policy",
        payload=b"Policy v1: conservative threshold",
    )

    print("Initial policy defined.")

    # ---------------------------------------------------------------
    # System decisions under initial policy
    # ---------------------------------------------------------------
    system.append_bytes(
        domain="decision",
        payload=b"Decision: action rejected (threshold)",
    )

    print("Decisions recorded under policy v1.")

    print_timeline("System state after initial decisions", system)

    # ---------------------------------------------------------------
    # Policy evolution (adaptive governance)
    # ---------------------------------------------------------------
    print("\nPolicy review triggered.")

    system.append_bytes(
        domain="policy",
        payload=b"Policy v2: adaptive threshold",
    )

    system.append_bytes(
        domain="governance",
        payload=b"Justification: improved performance and safety",
    )

    print("Policy updated with traceable justification.")

    # ---------------------------------------------------------------
    # System continues with new policy
    # ---------------------------------------------------------------
    system.append_bytes(
        domain="decision",
        payload=b"Decision: action approved (adaptive)",
    )

    print_timeline("System state after policy evolution", system)

    # ---------------------------------------------------------------
    # Replay and audit
    # ---------------------------------------------------------------
    print("\nAuditor reconstructing policy evolution...")

    auditor = TimelineJournal()

    for entry in system.entries():
        auditor.append_signal(entry.signal)

    print_timeline("Auditor reconstructed state", auditor)

    if system.head() == auditor.head():
        print("\nDeterministic audit verified.")
    else:
        print("\nAudit mismatch detected.")

    # ---------------------------------------------------------------
    # Historical traceability
    # ---------------------------------------------------------------
    print("\nPolicy evolution history:")
    for entry in system.entries():
        payload = entry.signal.payload.decode()
        if "Policy" in payload:
            print("-", payload)

    print("\nGovernance trace:")
    for entry in system.entries():
        payload = entry.signal.payload.decode()
        if "Justification" in payload:
            print("-", payload)

    # ---------------------------------------------------------------
    # Key properties
    # ---------------------------------------------------------------
    print("\nProperties demonstrated:")
    print("- Auditable policy evolution")
    print("- Deterministic rule enforcement")
    print("- Historical accountability")
    print("- Replayable governance")
    print("- Traceable decisions")
    print("- Safe adaptive systems")


if __name__ == "__main__":
    main()
