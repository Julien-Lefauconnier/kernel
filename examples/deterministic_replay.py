"""
Deterministic Replay Example (generic).

This example demonstrates:
- append-only history
- deterministic replay
- state reconstruction
- independent verification

The scenario is intentionally domain-agnostic.

It can represent:
- AI cognition replay
- distributed audit
- compliance verification
- forensic reconstruction
- safety-critical systems
- reproducible computation
"""

from veramem_kernel.api.timeline import TimelineJournal


def print_state(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- System execution ---
    system = TimelineJournal()

    system.append_bytes(domain="generic", payload=b"Event 1")
    system.append_bytes(domain="generic", payload=b"Event 2")
    system.append_bytes(domain="generic", payload=b"Event 3")

    print("System executed events.")
    print_state("Original system", system)

    # --- Export event log (generic representation) ---
    log = [entry for entry in system.entries()]

    # --- Independent verifier ---
    verifier = TimelineJournal()

    for entry in log:
        verifier.append_signal(entry.signal)

    print("\nVerifier reconstructed the state.")
    print_state("Verifier", verifier)

    # --- Determinism check ---
    if system.head() == verifier.head():
        print("\nDeterministic replay verified.")
    else:
        print("\nReplay mismatch detected.")


if __name__ == "__main__":
    main()
