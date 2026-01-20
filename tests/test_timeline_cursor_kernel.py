# tests/test_timeline_cursor_kernel.py

import pytest
from datetime import datetime, timedelta
from kernel.journals.timeline.timeline_cursor import TimelineCursor


def test_cursor_can_be_created_with_timestamp():
    ts = datetime.utcnow()

    cursor = TimelineCursor(timestamp=ts)

    assert cursor.timestamp == ts


def test_cursor_is_immutable():
    cursor = TimelineCursor(timestamp=datetime.utcnow())

    with pytest.raises(Exception):
        cursor.timestamp = datetime.utcnow()


def test_cursors_with_same_timestamp_are_equal():
    ts = datetime.utcnow()

    c1 = TimelineCursor(timestamp=ts)
    c2 = TimelineCursor(timestamp=ts)

    assert c1 == c2

def test_cursor_comparison_by_timestamp():
    t1 = datetime.utcnow()
    t2 = t1 + timedelta(seconds=10)

    c1 = TimelineCursor(timestamp=t1)
    c2 = TimelineCursor(timestamp=t2)

    assert c1 < c2
    assert c2 > c1


def test_cursors_can_be_sorted():
    now = datetime.utcnow()

    cursors = [
        TimelineCursor(timestamp=now + timedelta(seconds=5)),
        TimelineCursor(timestamp=now),
        TimelineCursor(timestamp=now + timedelta(seconds=10)),
    ]

    sorted_cursors = sorted(cursors)

    assert sorted_cursors[0].timestamp == now
    assert sorted_cursors[-1].timestamp == now + timedelta(seconds=10)


def test_cursor_can_be_serialized():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    cursor = TimelineCursor(timestamp=ts)

    payload = cursor.to_dict()

    assert payload == {
        "timestamp": ts.isoformat()
    }


def test_cursor_can_be_deserialized():
    ts = datetime(2024, 1, 1, 12, 0, 0)

    cursor = TimelineCursor.from_dict(
        {"timestamp": ts.isoformat()}
    )

    assert cursor.timestamp == ts


def test_cursor_comparison_with_other_type_fails():
    cursor = TimelineCursor(timestamp=datetime.utcnow())

    with pytest.raises(TypeError):
        _ = cursor < "not-a-cursor"