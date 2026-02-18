"""
AI Alignment Audit Example (generic).

This example demonstrates:
- append-only governance/audit journal
- deterministic recording of "alignment claims"
- traceable policy changes over time
- independent auditor verification via replay
- drift detection using immutable evidence

The scenario is intentionally domain-agnostic.

It can represent:
- AI oversight pipelines
- safety policy enforcement
- model governance and compliance
- regulated decision systems
- auditability of agentic workflows
- post-incident forensic analysis

Important note:
This example does NOT attempt to "prove alignment".
It shows how to make alignment-relevant evidence auditable,
deterministic, and replayable without relying on opaque internal state.
"""

import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List

from veramem_kernel.api.timeline import TimelineJournal
from veramem_kernel.journals.timeline.timeline_fork import fork_timeline
from veramem_kernel.journals.timeline.timeline_merge import merge_timelines


def stable_hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(obj: dict) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")


@dataclass(frozen=True)
class AlignmentClaim:
    """
    An "alignment claim" is a compact, auditable statement produced by a system.

    It intentionally avoids exposing internal reasoning.
    Instead, it records:
    - what policy was applied
    - what decision was made
    - what constraints were asserted
    - what evidence references were used (hashes / ids)
    """
    claim_id: str
    policy_id: str
    decision: str
    constraints: List[str]
    evidence_refs: List[str]  # hashes or stable identifiers
    timestamp_hint: str  # informational (not trusted as ordering)

    def to_bytes(self) -> bytes:
        obj = {
            "claim_id": self.claim_id,
            "policy_id": self.policy_id,
            "decision": self.decision,
            "constraints": self.constraints,
            "evidence_refs": self.evidence_refs,
            "timestamp_hint": self.timestamp_hint,
        }
        return canonical_json(obj)


@dataclass(frozen=True)
class PolicyUpdate:
    """
    Policy updates are also recorded as immutable facts.
    This supports:
    - traceability of governance changes
    - audit of policy evolution
    - deterministic reconstruction of what policy existed at any point in time
    """
    policy_id: str
    version: str
    change_summary: str
    owner: str

    def to_bytes(self) -> bytes:
        obj = {
            "policy_id": self.policy_id,
            "version": self.version,
            "change_summary": self.change_summary,
            "owner": self.owner,
        }
        return canonical_json(obj)


def print_timeline(title: str, timeline: TimelineJournal):
    print(f"\n{title}:")
    for entry in timeline.entries():
        decoded = entry.signal.payload.decode("utf-8")
        print("-", decoded)


def extract_claims(timeline: TimelineJournal) -> List[Dict]:
    claims = []
    for entry in timeline.entries():
        try:
            obj = json.loads(entry.signal.payload.decode("utf-8"))
        except Exception:
            continue
        if "claim_id" in obj and "policy_id" in obj and "decision" in obj:
            claims.append(obj)
    return claims


def auditor_check_for_drift(claims: List[Dict]) -> List[str]:
    """
    Extremely generic drift detection:
    - flags when the same constraint set starts producing different decisions
    - flags when policy_id changes unexpectedly
    """
    alerts = []
    seen = {}

    for c in claims:
        key = (
            tuple(c.get("constraints", [])),
            tuple(c.get("evidence_refs", [])),
        )
        decision = c.get("decision")
        policy_id = c.get("policy_id")

        if key not in seen:
            seen[key] = (decision, policy_id)
            continue

        prev_decision, prev_policy = seen[key]
        if decision != prev_decision:
            alerts.append(
                f"Decision drift detected for same constraints/evidence: "
                f"{prev_decision} -> {decision} (claim_id={c.get('claim_id')})"
            )
        if policy_id != prev_policy:
            alerts.append(
                f"Policy drift detected for same constraints/evidence: "
                f"{prev_policy} -> {policy_id} (claim_id={c.get('claim_id')})"
            )

    return alerts


def main():
    # --- System timeline: governance + claims ---
    system = TimelineJournal()

    # Baseline policy published
    p1 = PolicyUpdate(
        policy_id="safety-policy",
        version="1.0",
        change_summary="Baseline safety constraints and refusal rules",
        owner="governance-board",
    )
    system.append_bytes(domain="governance", payload=p1.to_bytes())

    # Evidence references (generic hashes)
    evidence_a = stable_hash(b"model-card-v1")
    evidence_b = stable_hash(b"safety-eval-suite-2026-01")
    evidence_c = stable_hash(b"incident-postmortem-xyz")

    # Alignment claims produced by the system
    c1 = AlignmentClaim(
        claim_id="claim-001",
        policy_id="safety-policy@1.0",
        decision="ALLOW",
        constraints=["no_illegal_actions", "no_self_harm", "no_privacy_violation"],
        evidence_refs=[evidence_a, evidence_b],
        timestamp_hint="t1",
    )
    system.append_bytes(domain="audit", payload=c1.to_bytes())

    c2 = AlignmentClaim(
        claim_id="claim-002",
        policy_id="safety-policy@1.0",
        decision="REFUSE",
        constraints=["no_illegal_actions", "no_self_harm", "no_privacy_violation"],
        evidence_refs=[evidence_a, evidence_c],
        timestamp_hint="t2",
    )
    system.append_bytes(domain="audit", payload=c2.to_bytes())

    print("System produced initial alignment claims under policy 1.0.")

    # --- Fork: new policy introduced in a separate branch ---
    branch = fork_timeline(system)

    p2 = PolicyUpdate(
        policy_id="safety-policy",
        version="1.1",
        change_summary="Tighten refusal rules after incident learnings",
        owner="governance-board",
    )
    branch.append_bytes(domain="governance", payload=p2.to_bytes())

    # Same constraints/evidence, but decision changes -> drift becomes visible & auditable
    c3 = AlignmentClaim(
        claim_id="claim-003",
        policy_id="safety-policy@1.1",
        decision="REFUSE",
        constraints=["no_illegal_actions", "no_self_harm", "no_privacy_violation"],
        evidence_refs=[evidence_a, evidence_b],
        timestamp_hint="t3",
    )
    branch.append_bytes(domain="audit", payload=c3.to_bytes())

    print("\nA policy update occurred in a branch (1.1), producing a different decision.")

    # --- Reconcile branch back into main (deterministic merge) ---
    merged = merge_timelines(system, branch)

    # --- Independent auditor reconstructs state deterministically ---
    auditor = TimelineJournal()
    for entry in merged.entries():
        auditor.append_signal(entry.signal)

    # Auditor replay
    claims = extract_claims(auditor)
    alerts = auditor_check_for_drift(claims)

    print_timeline("Merged immutable governance + audit log", merged)

    print("\nAuditor verification:")
    if merged.head() == auditor.head():
        print("- Deterministic replay verified (auditor matches system state).")
    else:
        print("- Replay mismatch detected (integrity failure).")

    print("\nDrift / alignment alerts:")
    if not alerts:
        print("- No drift detected.")
    else:
        for a in alerts:
            print("-", a)

    print("\nProperties demonstrated:")
    print("- Alignment-relevant evidence is recorded immutably")
    print("- Policy evolution is traceable and auditable")
    print("- Independent auditors can replay and verify deterministically")
    print("- Drift becomes detectable without access to internal reasoning")


if __name__ == "__main__":
    main()
