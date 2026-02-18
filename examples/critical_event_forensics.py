"""
Critical Event Forensics Example (generic).

This example demonstrates:
- immutable event recording
- traceable system evolution
- deterministic replay after an incident
- root-cause reconstruction
- independent verification
- audit and accountability

The scenario is intentionally domain-agnostic.

It can represent:
- aviation or industrial accident analysis
- cybersecurity breach investigation
- financial system failure
- safety-critical infrastructure
- regulatory or compliance audits
- medical or clinical incident tracing

The goal is to show how Veramem enables:
- transparent and reliable forensic reconstruction
- reproducible system history
- trustless post-incident analysis
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline


def print_timeline(name: str, timeline: TimelineJournal):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # ------------------------------------------------------------------
    # Normal system operation
    # ------------------------------------------------------------------
    system = TimelineJournal()

    system.append_bytes(domain="system", payload=b"System initialized")
    system.append_bytes(domain="system", payload=b"Subsystem A online")
    system.append_bytes(domain="system", payload=b"Subsystem B online")

    print("System running normally.")

    # ------------------------------------------------------------------
    # Monitoring node replicates system state
    # ------------------------------------------------------------------
    monitoring_node = fork_timeline(system)

    print("Monitoring node synchronized.")

    # ------------------------------------------------------------------
    # Operational events
    # ------------------------------------------------------------------
    system.append_bytes(domain="system", payload=b"Sensor reading within tolerance")
    system.append_bytes(domain="system", payload=b"Control loop stable")

    monitoring_node.append_bytes(
        domain="monitoring",
        payload=b"Independent sensor verification OK"
    )

    print("System stable state recorded.")

    # ------------------------------------------------------------------
    # Incident occurs
    # ------------------------------------------------------------------
    system.append_bytes(domain="incident", payload=b"Unexpected anomaly detected")
    system.append_bytes(domain="incident", payload=b"Subsystem B failure")
    system.append_bytes(domain="incident", payload=b"Emergency shutdown triggered")

    monitoring_node.append_bytes(
        domain="monitoring",
        payload=b"Anomaly detected independently"
    )

    print("Critical incident recorded.")

    print_timeline("System", system)
    print_timeline("Monitoring", monitoring_node)

    # ------------------------------------------------------------------
    # Forensic reconstruction
    # ------------------------------------------------------------------
    print("\n--- Forensic Reconstruction ---")

    reconstruction = TimelineJournal()

    for entry in system.entries():
        reconstruction.append_signal(entry.signal)

    print_timeline("Reconstructed system state", reconstruction)

    # ------------------------------------------------------------------
    # Root cause analysis
    # ------------------------------------------------------------------
    print("\n--- Root Cause Analysis ---")

    root_events = [
        entry.signal.payload.decode()
        for entry in reconstruction.entries()
        if "failure" in entry.signal.payload.decode().lower()
        or "anomaly" in entry.signal.payload.decode().lower()
    ]

    for event in root_events:
        print("Potential root cause:", event)

    # ------------------------------------------------------------------
    # Independent audit
    # ------------------------------------------------------------------
    auditor = TimelineJournal()

    for entry in reconstruction.entries():
        auditor.append_signal(entry.signal)

    print("\n--- Independent Audit ---")

    if auditor.head() == reconstruction.head():
        print("Audit verified: deterministic reconstruction confirmed.")
    else:
        print("Mismatch detected: integrity compromised.")

    # ------------------------------------------------------------------
    # Key forensic properties
    # ------------------------------------------------------------------
    print("\nForensic properties demonstrated:")
    print("- Immutable event recording")
    print("- Deterministic replay")
    print("- Transparent incident traceability")
    print("- Independent auditability")
    print("- Root cause reconstruction")
    print("- Trustless verification of system history")


if __name__ == "__main__":
    main()
