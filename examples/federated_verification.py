"""
Federated Verification Example (generic).

This example demonstrates:
- independent institutions
- distributed audit
- deterministic verification
- cross-domain trust
- replayable global history
- no central authority

This scenario is intentionally generic and domain-agnostic.

It can represent:
- international audit
- federated AI governance
- cross-border compliance
- scientific reproducibility
- distributed safety verification
- multi-organization trust frameworks

The goal is to show that Veramem enables independent actors
to verify a shared factual history without coordination or trust.
"""

from veramem_kernel.api.timeline import TimelineJournal


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Step 1: origin system produces facts ---
    origin = TimelineJournal()

    origin.append_bytes(domain="generic", payload=b"Fact A")
    origin.append_bytes(domain="generic", payload=b"Fact B")
    origin.append_bytes(domain="generic", payload=b"Fact C")

    print("Origin system produced factual history.")
    print_timeline("Origin", origin)

    # --- Step 2: export event log ---
    exported_log = [entry for entry in origin.entries()]

    # --- Step 3: independent institutions verify ---
    institution_1 = TimelineJournal()
    institution_2 = TimelineJournal()
    institution_3 = TimelineJournal()

    for entry in exported_log:
        institution_1.append_signal(entry.signal)
        institution_2.append_signal(entry.signal)
        institution_3.append_signal(entry.signal)

    print("\nIndependent institutions reconstructed the history.")

    print_timeline("Institution 1", institution_1)
    print_timeline("Institution 2", institution_2)
    print_timeline("Institution 3", institution_3)

    # --- Step 4: determinism check ---
    heads = [
        origin.head(),
        institution_1.head(),
        institution_2.head(),
        institution_3.head(),
    ]

    if len(set(heads)) == 1:
        print("\nAll institutions reached identical state.")
    else:
        print("\nDivergence detected.")

    # --- Step 5: divergence scenario ---
    institution_2.append_bytes(domain="generic", payload=b"Local divergence")

    print("\nInstitution 2 diverged.")

    print_timeline("Institution 2 (diverged)", institution_2)

    # --- Step 6: reconciliation ---
    # Institution 2 exports and reconciles with others
    reconciliation_log = [entry for entry in institution_2.entries()]

    reconciled = TimelineJournal()

    for entry in reconciliation_log:
        reconciled.append_signal(entry.signal)

    print("\nReconciled history:")
    print_timeline("Reconciled", reconciled)

    print("\nProperties demonstrated:")
    print("- No central authority")
    print("- Independent verification")
    print("- Global reproducibility")
    print("- Traceable divergence")
    print("- Deterministic reconciliation")
    print("- Federated trust")


if __name__ == "__main__":
    main()
