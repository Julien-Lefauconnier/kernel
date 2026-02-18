"""
Minimal example: append-only timeline.

This example demonstrates:
- deterministic ordering
- append-only facts
- replay capability
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal


def main():
    timeline = TimelineJournal()

    # Create signals
    s1 = Signal(domain="example", payload=b"event-1")
    s2 = Signal(domain="example", payload=b"event-2")

    # Append events
    timeline.append(s1)
    timeline.append(s2)

    # Replay
    for entry in timeline.entries():
        print(entry.signal.payload)


if __name__ == "__main__":
    main()
