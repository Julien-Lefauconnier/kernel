# tests/test_timeline_window_kernel.py

from datetime import datetime, timedelta
import pytest

from kernel.journals.timeline.timeline_cursor import TimelineCursor
from kernel.journals.timeline.timeline_window import TimelineWindow

def test_window_can_be_created_empty():
    window = TimelineWindow()

    assert window.after is None
    assert window.before is None

def test_window_with_after_cursor():
    ts = datetime.utcnow()
    cursor = TimelineCursor(timestamp=ts)

    window = TimelineWindow(after=cursor)

    assert window.after == cursor
    assert window.before is None

def test_window_with_before_cursor():
    ts = datetime.utcnow()
    cursor = TimelineCursor(timestamp=ts)

    window = TimelineWindow(before=cursor)

    assert window.before == cursor
    assert window.after is None

def test_window_with_after_and_before():
    t1 = datetime.utcnow()
    t2 = t1 + timedelta(seconds=10)

    after = TimelineCursor(timestamp=t1)
    before = TimelineCursor(timestamp=t2)

    window = TimelineWindow(after=after, before=before)

    assert window.after == after
    assert window.before == before

def test_window_rejects_invalid_bounds():
    t1 = datetime.utcnow()
    t2 = t1 + timedelta(seconds=10)

    after = TimelineCursor(timestamp=t2)
    before = TimelineCursor(timestamp=t1)

    with pytest.raises(ValueError):
        TimelineWindow(after=after, before=before)

def test_window_is_immutable():
    cursor = TimelineCursor(timestamp=datetime.utcnow())
    window = TimelineWindow(after=cursor)

    with pytest.raises(Exception):
        window.after = None

def test_windows_with_same_bounds_are_equal():
    ts = datetime.utcnow()

    w1 = TimelineWindow(after=TimelineCursor(timestamp=ts))
    w2 = TimelineWindow(after=TimelineCursor(timestamp=ts))

    assert w1 == w2

def test_windows_with_different_bounds_are_not_equal():
    ts = datetime.utcnow()

    w1 = TimelineWindow(after=TimelineCursor(timestamp=ts))
    w2 = TimelineWindow(before=TimelineCursor(timestamp=ts))

    assert w1 != w2

def test_window_comparison_by_after_cursor():
    t1 = datetime.utcnow()
    t2 = t1 + timedelta(seconds=5)

    w1 = TimelineWindow(after=TimelineCursor(timestamp=t1))
    w2 = TimelineWindow(after=TimelineCursor(timestamp=t2))

    assert w1 < w2

def test_window_can_be_serialized_to_dict():
    ts = datetime.utcnow()
    cursor = TimelineCursor(timestamp=ts)

    window = TimelineWindow(after=cursor)

    data = window.to_dict()

    assert data["after"] == cursor.timestamp.isoformat()
    assert data["before"] is None
