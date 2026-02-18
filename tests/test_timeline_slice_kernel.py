# tests/test_timeline_slice_kernel.py

from datetime import datetime, timezone, timezone, timedelta
import pytest

from veramem_kernel.journals.timeline.timeline_slice import TimelineSlice
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType


def make_entry(ts):
    return TimelineEntry(
        entry_id=str(ts.timestamp()),
        created_at=ts,
        type=TimelineEntryType.ACTION_PROPOSED,
        title="test",
        description=None,
        action_id=None,
        place_id=None,
    )



def test_slice_creation():
    now = datetime.now(timezone.utc)
    entries = [make_entry(now)]

    slice_ = TimelineSlice(entries=entries)

    assert slice_.entries == tuple(entries)


def test_slice_is_immutable():
    now = datetime.now(timezone.utc)
    slice_ = TimelineSlice(entries=[make_entry(now)])

    with pytest.raises(AttributeError):
        slice_.entries.append("x")


def test_slice_can_have_cursors():
    now = datetime.now(timezone.utc)
    after = TimelineCursor(timestamp=now)

    slice_ = TimelineSlice(
        entries=[make_entry(now)],
        after=after,
    )

    assert slice_.after == after
    assert slice_.before is None


def test_slice_preserves_order():
    base = datetime(2025, 1, 1, 12, 0, 58, tzinfo=timezone.utc)  # seconde=58
    t1 = base
    t2 = base + timedelta(seconds=1)                            # seconde=59 → valide

    e1 = make_entry(t1)
    e2 = make_entry(t2)

    slice_ = TimelineSlice(entries=[e1, e2])

    assert slice_.entries[0] == e1
    assert slice_.entries[1] == e2


def test_empty_slice_allowed():
    slice_ = TimelineSlice(entries=[])

    assert slice_.entries == ()
