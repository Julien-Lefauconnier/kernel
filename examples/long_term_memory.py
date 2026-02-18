"""
Long-Term Memory Example (generic).

This example demonstrates:
- long-term append-only memory
- temporal epochs and consolidation
- snapshotting and reconstruction
- deterministic replay over long horizons
- memory durability and historical integrity

This scenario is intentionally generic and domain-agnostic.

It can represent:
- AI long-term cognition
- human digital memory
- archival systems
- knowledge preservation infrastructures
- historical record keeping
- sovereign cognitive systems

The kernel ensures:
- no rewriting of the past
- deterministic reconstruction
- full traceability of memory evolution
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_snapshot import snapshot_timeline


def print_memory(title, timeline):
    print(f"\n{title}")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Phase 1: early memory ---
    memory = TimelineJournal()

    memory.append_bytes(domain="memory", payload=b"First experience recorded")
    memory.append_bytes(domain="memory", payload=b"Learning basic pattern")
    memory.append_bytes(domain="memory", payload=b"Initial knowledge consolidation")

    print("Phase 1 recorded.")

    # Snapshot epoch 1
    epoch_1 = snapshot_timeline(memory)
    print("\nEpoch 1 snapshot created.")

    # --- Phase 2: later evolution ---
    memory.append_bytes(domain="memory", payload=b"Advanced pattern recognition")
    memory.append_bytes(domain="memory", payload=b"Integration of new information")
    memory.append_bytes(domain="memory", payload=b"Contextual understanding improved")

    print("Phase 2 recorded.")

    epoch_2 = snapshot_timeline(memory)
    print("\nEpoch 2 snapshot created.")

    # --- Phase 3: mature system ---
    memory.append_bytes(domain="memory", payload=b"Long-term abstraction formation")
    memory.append_bytes(domain="memory", payload=b"Generalization across contexts")
    memory.append_bytes(domain="memory", payload=b"Strategic reasoning capability")

    print("Phase 3 recorded.")

    # --- Replay full memory ---
    print_memory("Full reconstructed memory", memory)

    # --- Independent archival node ---
    archive = TimelineJournal()

    # Load historical snapshots + new events
    for entry in epoch_1.entries():
        archive.append_signal(entry.signal)

    for entry in epoch_2.entries():
        archive.append_signal(entry.signal)

    for entry in memory.entries():
        archive.append_signal(entry.signal)

    print_memory("\nArchive reconstruction", archive)

    # --- Determinism check ---
    if archive.head() == memory.head():
        print("\nDeterministic reconstruction verified.")
    else:
        print("\nMismatch detected in long-term memory reconstruction.")

    print("\nProperties demonstrated:")
    print("- Memory is append-only and cannot be rewritten")
    print("- Historical epochs are preserved")
    print("- Snapshots allow scalable reconstruction")
    print("- Independent archival systems can verify memory")
    print("- Long-term consistency is guaranteed")


if __name__ == "__main__":
    main()
