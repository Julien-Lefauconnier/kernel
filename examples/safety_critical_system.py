"""
Safety-Critical System Example (generic).

This example demonstrates:
- traceable decision history
- deterministic replay
- auditability
- incident reconstruction
- accountability
- immutable event recording

This scenario is intentionally generic and domain-agnostic.

It can represent:
- aviation control
- medical decision systems
- autonomous robotics
- nuclear monitoring
- industrial safety
- critical infrastructure

The goal is to show that Veramem enables trustworthy
and auditable operation in safety-critical environments.
"""

from veramem_kernel.api.timeline import TimelineJournal


def print_history(timeline):
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Step 1: system initialization ---
    system = TimelineJournal()

    system.append_bytes(domain="generic", payload=b"System initialized")
    system.append_bytes(domain="generic", payload=b"Sensor calibration complete")

    print("System started.")

    # --- Step 2: normal operation ---
    system.append_bytes(domain="generic", payload=b"Sensor reading: nominal")
    system.append_bytes(domain="generic", payload=b"Automated control action executed")

    print("\nNormal operation recorded.")

    # --- Step 3: anomaly detection ---
    system.append_bytes(domain="generic", payload=b"Sensor anomaly detected")
    system.append_bytes(domain="generic", payload=b"Fallback procedure activated")

    print("\nAnomaly handled.")

    # --- Step 4: critical incident ---
    system.append_bytes(domain="generic", payload=b"Critical threshold reached")
    system.append_bytes(domain="generic", payload=b"Emergency shutdown triggered")

    print("\nCritical event recorded.")

    # --- Step 5: export for investigation ---
    incident_log = [entry for entry in system.entries()]

    # --- Step 6: independent audit ---
    auditor = TimelineJournal()

    for entry in incident_log:
        auditor.append_signal(entry.signal)

    print("\nIndependent auditor reconstructed the system history.")

    # --- Step 7: replay for forensic analysis ---
    print("\nForensic replay:")
    print_history(auditor)

    # --- Step 8: deterministic verification ---
    if system.head() == auditor.head():
        print("\nAudit verified: system history is consistent.")
    else:
        print("\nMismatch detected: investigation required.")

    print("\nProperties demonstrated:")
    print("- Immutable operational history")
    print("- Incident traceability")
    print("- Independent verification")
    print("- Deterministic replay")
    print("- Accountability")
    print("- Safety and compliance support")


if __name__ == "__main__":
    main()
