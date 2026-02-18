"""
Conflict Traceability Example (generic).

This example demonstrates:
- divergent knowledge states
- absence of overwrite
- traceable conflicts
- coexistence of competing truths
- deterministic historical reconstruction

This scenario is intentionally domain-agnostic.

It can represent:
- AI model disagreements
- regulatory audit
- scientific hypothesis evolution
- multi-agent cognition
- forensic investigations
- distributed decision systems
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def print_timeline(name, timeline):
    print(f"\n{name}:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Shared initial knowledge ---
    base = TimelineJournal()

    base.append_bytes(domain="generic", payload=b"Initial observation")

    print("Shared initial state created.")

    # --- Independent analysis ---
    analyst_a = fork_timeline(base)
    analyst_b = fork_timeline(base)

    print("Two independent agents started analysis.")

    # Diverging interpretations
    analyst_a.append_bytes(
        domain="generic",
        payload=b"Hypothesis A: cause = environmental factor",
    )

    analyst_b.append_bytes(
        domain="generic",
        payload=b"Hypothesis B: cause = system failure",
    )

    print("Agents produced conflicting conclusions.")

    print_timeline("Analyst A", analyst_a)
    print_timeline("Analyst B", analyst_b)

    # --- Deterministic merge ---
    merged = merge_timelines(analyst_a, analyst_b)

    print("\nMerged timeline with full traceability:")
    print_timeline("Merged", merged)

    print("\nProperties demonstrated:")
    print("- No truth overwrite")
    print("- Conflicts remain visible")
    print("- Historical accountability preserved")
    print("- External resolution possible")
    print("- Deterministic reconstruction")


if __name__ == "__main__":
    main()
