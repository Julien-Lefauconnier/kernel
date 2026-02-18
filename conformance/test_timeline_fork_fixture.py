# conformance/test_timeline_fork_fixture.py

from pathlib import Path
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork, TimelineForkKind

FIX = Path(__file__).parent / "fixtures" / "timeline_fork_v1.bin"

def test_timeline_fork_v1_fixture_roundtrip():
    raw = FIX.read_bytes()
    fork = TimelineFork.from_bytes(raw)
    fork.assert_consistent()
    assert fork.kind == TimelineForkKind.FORK
    assert fork.common_prefix_len == 5
