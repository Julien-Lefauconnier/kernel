# conformance/test_timeline_merge_fixture.py

from pathlib import Path
from veramem_kernel.journals.timeline.timeline_merge import TimelineMergeResult, TimelineMergeKind

FIX = Path(__file__).parent / "fixtures" / "timeline_merge_v1.bin"

def test_timeline_merge_v1_fixture_roundtrip():
    raw = FIX.read_bytes()
    res = TimelineMergeResult.from_bytes(raw)
    assert res.kind == TimelineMergeKind.MERGED
    assert res.merged is not None
    assert len(res.merged.entries) == 11  # 5 prefix + 3 + 3
