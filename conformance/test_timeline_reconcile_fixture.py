# conformance/test_timeline_reconcile_fixture.py

from pathlib import Path
from veramem_kernel.journals.timeline.timeline_reconcile import TimelineReconcileDecision, ReconcileDecisionKind

FIX = Path(__file__).parent / "fixtures" / "timeline_reconcile_v1.bin"

def test_timeline_reconcile_decision_v1_fixture_roundtrip():
    raw = FIX.read_bytes()
    d = TimelineReconcileDecision.from_bytes(raw)
    assert d.kind == ReconcileDecisionKind.KEEP_BOTH
    assert d.common_prefix_len == 5
