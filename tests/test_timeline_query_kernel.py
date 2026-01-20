# tests/test_timeline_query_kernel.py

import pytest
from datetime import datetime, timedelta
from dataclasses import FrozenInstanceError

from kernel.journals.timeline.timeline_cursor import TimelineCursor
from kernel.journals.timeline.timeline_window import TimelineWindow
from kernel.journals.timeline.timeline_query import TimelineQuery


def test_query_can_be_created_with_defaults():
    q = TimelineQuery()

    assert q.window is None
    assert q.limit is None
    assert q.direction == "forward"


def test_query_accepts_window():
    now = datetime.utcnow()

    window = TimelineWindow(
        after=TimelineCursor(timestamp=now),
        before=TimelineCursor(timestamp=now + timedelta(seconds=10)),
    )

    q = TimelineQuery(window=window)

    assert q.window == window

def test_query_rejects_invalid_limit():
    with pytest.raises(ValueError):
        TimelineQuery(limit=0)

    with pytest.raises(ValueError):
        TimelineQuery(limit=-5)

def test_query_accepts_valid_directions():
    TimelineQuery(direction="forward")
    TimelineQuery(direction="backward")


def test_query_rejects_invalid_direction():
    with pytest.raises(ValueError):
        TimelineQuery(direction="sideways")

def test_query_is_immutable():
    q = TimelineQuery()

    with pytest.raises(FrozenInstanceError):
        q.limit = 10