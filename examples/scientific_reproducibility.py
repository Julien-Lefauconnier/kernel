"""
Scientific Reproducibility Example (generic).

This example demonstrates:
- immutable experiment recording
- deterministic replay of scientific workflows
- traceable evolution of hypotheses
- auditable validation of results

The scenario is intentionally domain-agnostic.

It can represent:
- AI model training
- medical research
- physics experiments
- data science pipelines
- benchmark verification
- reproducible academic publications

The goal is to show that Veramem enables long-term,
verifiable, and replayable scientific knowledge.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal
from veramem_kernel.signals.lineage.signal_lineage_patch_builder import (
    build_signal_lineage_patch,
)
from veramem_kernel.signals.lineage.signal_lineage_patch_applier import (
    apply_signal_lineage_patch,
)


def print_experiment(timeline):
    print("\nRecorded experiment history:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Research lab system ---
    lab = TimelineJournal()

    print("Recording experiment...")

    # Step 1 — initial hypothesis
    hypothesis_v1 = Signal(
        domain="science",
        payload=b"Hypothesis: Method A improves performance"
    )
    lab.append(hypothesis_v1)

    # Step 2 — experiment run
    experiment_1 = Signal(
        domain="science",
        payload=b"Experiment 1: Dataset X, configuration alpha"
    )
    lab.append(experiment_1)

    # Step 3 — results
    result_1 = Signal(
        domain="science",
        payload=b"Result: 12% improvement observed"
    )
    lab.append(result_1)

    # Step 4 — revised hypothesis
    hypothesis_v2 = Signal(
        domain="science",
        payload=b"Hypothesis updated: Method A with parameter tuning"
    )
    lab.append(hypothesis_v2)

    # --- Lineage tracking of hypothesis evolution ---
    lineage_state = {}

    patch = build_signal_lineage_patch(
        parents=[hypothesis_v1.key],
        supersedes=hypothesis_v1.key,
        child=hypothesis_v2.key,
    )
    apply_signal_lineage_patch(patch, lineage_state)

    print("Experiment and hypothesis evolution recorded.")

    print_experiment(lab)

    # --- Independent verifier ---
    print("\nIndependent reproducibility verification...")

    verifier = TimelineJournal()

    for entry in lab.entries():
        verifier.append_signal(entry.signal)

    print("Verifier reconstructed the experiment.")

    print_experiment(verifier)

    # --- Deterministic verification ---
    if lab.head() == verifier.head():
        print("\nReproducibility verified.")
    else:
        print("\nMismatch detected.")

    # --- Traceability ---
    print("\nTraceable evolution of scientific knowledge:")
    print("Updated hypothesis:", hypothesis_v2.key)
    print("Supersedes:", hypothesis_v1.key)


if __name__ == "__main__":
    main()
