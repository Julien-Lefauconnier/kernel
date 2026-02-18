"""
Explainable AI Backbone Example (generic).

This example demonstrates:
- immutable observation recording
- traceable decision history
- governed, deterministic explanations
- replay and independent verification
- separation of concerns (kernel vs. policy vs. explanation)

This scenario is intentionally generic and domain-agnostic.

It can represent:
- AI assistant recommendations
- compliance-oriented decision systems
- regulated scoring pipelines
- safety governance layers
- audit-ready AI products

Important:
The kernel does NOT "reason" or "decide".
It records facts, ordering, and constraints.

A higher layer (outside the kernel) can compute a decision,
then record both the decision and a governed explanation back into the kernel.
"""

from dataclasses import dataclass
from typing import List, Tuple

from veramem_kernel.api.timeline import TimelineJournal


# ---------------------------
# External (non-kernel) logic
# ---------------------------

@dataclass(frozen=True)
class DecisionResult:
    decision: str
    reasons: List[str]
    constraints: List[str]


def external_decision_engine(observations: List[str], constraints: List[str]) -> DecisionResult:
    """
    A deliberately simple, deterministic "decision" function.

    This is NOT part of the kernel.
    It simulates an application-layer decision engine that:
    - reads facts (observations)
    - reads constraints (rules/requirements)
    - produces a decision + reasons
    """
    # Deterministic rule: if any observation contains "risk:high", we recommend "BLOCK"
    # Otherwise "ALLOW".
    risk_high = any("risk:high" in o for o in observations)

    if risk_high:
        decision = "BLOCK"
        reasons = [
            "Observed high risk signal",
            "Constraints require conservative outcome under high risk",
        ]
    else:
        decision = "ALLOW"
        reasons = [
            "No high risk signal observed",
            "Constraints allow normal operation under nominal conditions",
        ]

    return DecisionResult(decision=decision, reasons=reasons, constraints=constraints)


def governed_explanation(decision: DecisionResult, evidence: List[str]) -> str:
    """
    A governed explanation is declarative and bounded.

    - It references recorded facts.
    - It states limitations explicitly.
    - It does not claim access to hidden reasoning or raw data.
    """
    lines = []
    lines.append("EXPLANATION (governed):")
    lines.append(f"- Decision: {decision.decision}")
    lines.append("- Evidence used (recorded facts):")
    for e in evidence:
        lines.append(f"  - {e}")
    lines.append("- Constraints applied (recorded constraints):")
    for c in decision.constraints:
        lines.append(f"  - {c}")
    lines.append("- Limitations:")
    lines.append("  - This explanation is derived only from recorded facts and declared constraints.")
    lines.append("  - No private model reasoning, hidden features, or external context was used.")
    return "\n".join(lines)


# ---------------------------
# Kernel-backed timeline
# ---------------------------

def print_history(title: str, timeline: TimelineJournal) -> None:
    print(f"\n{title}")
    for entry in timeline.entries():
        print("-", entry.signal.payload.decode())


def extract_domain_payloads(timeline: TimelineJournal, domain: str) -> List[str]:
    out = []
    for entry in timeline.entries():
        if entry.signal.domain == domain:
            out.append(entry.signal.payload.decode())
    return out


def main():
    # --- Step 1: record facts & constraints immutably ---
    kernel = TimelineJournal()

    kernel.append_bytes(domain="observation", payload=b"input:request_id=REQ-001")
    kernel.append_bytes(domain="observation", payload=b"signal:risk=low")
    kernel.append_bytes(domain="observation", payload=b"context:region=generic")
    kernel.append_bytes(domain="constraint", payload=b"rule:if risk=high => BLOCK")
    kernel.append_bytes(domain="constraint", payload=b"rule:explanations must be evidence-bounded")

    print("Recorded observations + constraints into the kernel.")

    # --- Step 2: external layer reads kernel facts (projection outside kernel) ---
    observations = extract_domain_payloads(kernel, "observation")
    constraints = extract_domain_payloads(kernel, "constraint")

    # --- Step 3: external decision engine produces decision deterministically ---
    decision = external_decision_engine(observations, constraints)

    # Record the decision as a fact (still no policy engine inside kernel)
    kernel.append_bytes(domain="decision", payload=f"decision:{decision.decision}".encode())

    # --- Step 4: external reflexive layer produces governed explanation ---
    explanation = governed_explanation(decision, evidence=observations)
    kernel.append_bytes(domain="explanation", payload=explanation.encode())

    print("\nDecision + governed explanation recorded.")

    # --- Step 5: export log for independent verification ---
    log = [entry for entry in kernel.entries()]

    verifier = TimelineJournal()
    for entry in log:
        verifier.append_signal(entry.signal)

    # --- Step 6: replay + verification ---
    print_history("Replayed history (verifier):", verifier)

    if kernel.head() == verifier.head():
        print("\nDeterministic verification: OK (same head).")
    else:
        print("\nDeterministic verification: FAILED (mismatch).")

    print("\nProperties demonstrated:")
    print("- Observations are immutable facts")
    print("- Constraints are explicit and recorded")
    print("- Decisions are recorded as facts (not hidden)")
    print("- Explanations are governed and evidence-bounded")
    print("- Full replay and independent verification")


if __name__ == "__main__":
    main()
