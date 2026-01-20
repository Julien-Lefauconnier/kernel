# tests/test_timeline_reader_kernel.py

from datetime import datetime, timedelta

from kernel.journals.timeline.timeline_reader import TimelineReader
from kernel.journals.timeline.timeline_cursor import TimelineCursor
from kernel.journals.timeline.timeline_window import TimelineWindow
from kernel.journals.action.action_event import ActionEvent


def make_event(ts: datetime) -> ActionEvent:
    return ActionEvent(
        event_id=f"evt-{ts.isoformat()}",
        created_at=ts,
        user_ref="u1",
        place_ref="p1",
        intent="test",
    )


def test_reader_without_window_returns_all_events():
    now = datetime.utcnow()

    events = [
        make_event(now),
        make_event(now + timedelta(seconds=10)),
        make_event(now + timedelta(seconds=20)),
    ]

    reader = TimelineReader()
    result = reader.read(events=events)

    assert result == events

def test_reader_applies_after_cursor():
    now = datetime.utcnow()

    e1 = make_event(now)
    e2 = make_event(now + timedelta(seconds=10))
    e3 = make_event(now + timedelta(seconds=20))

    window = TimelineWindow(
        after=TimelineCursor(timestamp=now + timedelta(seconds=5))
    )

    reader = TimelineReader()
    result = reader.read(events=[e1, e2, e3], window=window)

    assert result == [e2, e3]

def test_reader_applies_before_cursor():
    now = datetime.utcnow()

    e1 = make_event(now)
    e2 = make_event(now + timedelta(seconds=10))
    e3 = make_event(now + timedelta(seconds=20))

    window = TimelineWindow(
        before=TimelineCursor(timestamp=now + timedelta(seconds=15))
    )

    reader = TimelineReader()
    result = reader.read(events=[e1, e2, e3], window=window)

    assert result == [e1, e2]

def test_reader_applies_after_and_before():
    now = datetime.utcnow()

    e1 = make_event(now)
    e2 = make_event(now + timedelta(seconds=10))
    e3 = make_event(now + timedelta(seconds=20))
    e4 = make_event(now + timedelta(seconds=30))

    window = TimelineWindow(
        after=TimelineCursor(timestamp=now + timedelta(seconds=5)),
        before=TimelineCursor(timestamp=now + timedelta(seconds=25)),
    )

    reader = TimelineReader()
    result = reader.read(events=[e1, e2, e3, e4], window=window)

    assert result == [e2, e3]

def test_reader_preserves_event_order():
    now = datetime.utcnow()

    e1 = make_event(now + timedelta(seconds=20))
    e2 = make_event(now)
    e3 = make_event(now + timedelta(seconds=10))

    events = [e1, e2, e3]

    reader = TimelineReader()
    result = reader.read(events=events)

    assert result == events

def test_reader_with_empty_events_returns_empty():
    reader = TimelineReader()
    result = reader.read(events=[])

    assert result == []

def test_reader_is_stateless():
    now = datetime.utcnow()

    e1 = make_event(now)
    e2 = make_event(now + timedelta(seconds=10))

    reader = TimelineReader()

    r1 = reader.read(events=[e1])
    r2 = reader.read(events=[e2])

    assert r1 == [e1]
    assert r2 == [e2]
