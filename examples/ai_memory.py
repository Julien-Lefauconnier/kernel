"""
AI Memory Example.

This example demonstrates:
- append-only knowledge
- signal lineage
- deterministic replay
- traceable evolution of knowledge

This is a minimal illustration of a cognitive memory built on top of the Veramem Kernel.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal
from veramem_kernel.signals.lineage.signal_lineage_patch_builder import (
    build_signal_lineage_patch,
)
from veramem_kernel.signals.lineage.signal_lineage_patch_applier import (
    apply_signal_lineage_patch,
)


def main():
    timeline = TimelineJournal()

    # Step 1 — initial knowledge
    s1 = Signal(domain="knowledge", payload=b"The sky is blue")

    timeline.append(s1)

    print("Initial memory recorded.")

    # Step 2 — updated knowledge (traceable evolution)
    s2 = Signal(domain="knowledge", payload=b"The sky appears blue due to Rayleigh scattering")

    timeline.append(s2)

    # Create lineage between knowledge states
    patch = build_signal_lineage_patch(
        parents=[s1.key],
        supersedes=s1.key,
        child=s2.key,
    )

    lineage_state = {}
    apply_signal_lineage_patch(patch, lineage_state)

    print("Knowledge updated with traceability.")

    # Step 3 — replay memory
    print("\nDeterministic replay:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())

    # Step 4 — show lineage
    print("\nLineage:")
    print("Child:", s2.key)
    print("Supersedes:", s1.key)


if __name__ == "__main__":
    main()
