"""
Regulated AI System Example (generic).

This example demonstrates:
- compliance and auditability by construction
- traceable decision pipelines
- deterministic replay for regulatory inspection
- explainable decision history
- alignment with safety and governance requirements

The scenario is intentionally domain-agnostic.

It can represent:
- AI systems under regulatory frameworks
- high-risk AI infrastructures
- financial or medical decision support
- public sector AI
- safety-critical automated decision systems
- compliance-driven cognitive architectures

The goal is to show that Veramem enables regulated AI
systems that are transparent, auditable, and reproducible.
"""

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.signals.signal import Signal
from veramem_kernel.signals.lineage.signal_lineage_patch_builder import (
    build_signal_lineage_patch,
)
from veramem_kernel.signals.lineage.signal_lineage_patch_applier import (
    apply_signal_lineage_patch,
)


def print_history(name, timeline):
    print(f"\n{name} decision history:")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def main():
    # --- Regulated AI system ---
    system = TimelineJournal()

    print("Regulated AI system initialized.")

    # Step 1 — data intake (traceable)
    data_event = Signal(
        domain="regulated_ai",
        payload=b"Input received: structured data"
    )
    system.append(data_event)

    # Step 2 — validation and constraint checks
    validation = Signal(
        domain="regulated_ai",
        payload=b"Validation: data integrity and constraints satisfied"
    )
    system.append(validation)

    # Step 3 — model inference (opaque outside, traceable outcome)
    inference_v1 = Signal(
        domain="regulated_ai",
        payload=b"Inference: decision score computed"
    )
    system.append(inference_v1)

    # Step 4 — human or governance oversight
    oversight = Signal(
        domain="regulated_ai",
        payload=b"Oversight: decision reviewed and approved"
    )
    system.append(oversight)

    # Step 5 — decision output
    decision = Signal(
        domain="regulated_ai",
        payload=b"Final decision issued"
    )
    system.append(decision)

    # Step 6 — model update (evolution traceability)
    inference_v2 = Signal(
        domain="regulated_ai",
        payload=b"Inference: updated decision policy after review"
    )
    system.append(inference_v2)

    # --- Traceability of model evolution ---
    lineage_state = {}

    patch = build_signal_lineage_patch(
        parents=[inference_v1.key],
        supersedes=inference_v1.key,
        child=inference_v2.key,
    )
    apply_signal_lineage_patch(patch, lineage_state)

    print("Model evolution recorded with traceability.")

    print_history("System", system)

    # --- Independent regulatory audit ---
    print("\nRegulatory audit reconstruction...")

    regulator = TimelineJournal()

    for entry in system.entries():
        regulator.append_signal(entry.signal)

    print("Regulator reconstructed the full decision pipeline.")

    print_history("Regulator", regulator)

    # --- Deterministic verification ---
    if system.head() == regulator.head():
        print("\nCompliance verification successful.")
    else:
        print("\nCompliance mismatch detected.")

    # --- Explainability and traceability ---
    print("\nTraceable model evolution:")
    print("Updated inference:", inference_v2.key)
    print("Supersedes:", inference_v1.key)


if __name__ == "__main__":
    main()
