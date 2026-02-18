# tests/test_timeline_cursor_kernel.py

import pytest
from datetime import datetime, timezone, timedelta, timezone
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


def test_cursor_can_be_created_with_timestamp():
    ts = datetime.now(timezone.utc)

    cursor = TimelineCursor(timestamp=ts)

    assert cursor.timestamp == ts


def test_cursor_is_immutable():
    cursor = TimelineCursor(timestamp=datetime.now(timezone.utc))

    with pytest.raises(Exception):
        cursor.timestamp = datetime.now(timezone.utc)


def test_cursors_with_same_timestamp_are_equal():
    ts = datetime.now(timezone.utc)

    c1 = TimelineCursor(timestamp=ts)
    c2 = TimelineCursor(timestamp=ts)

    assert c1 == c2

def test_cursor_comparison_not_supported():
    now = datetime.now(timezone.utc)
    c1 = TimelineCursor(timestamp=now)
    c2 = TimelineCursor(timestamp=now)

    with pytest.raises(TypeError):
        _ = c1 < c2

    with pytest.raises(TypeError):
        sorted([c1, c2])


def test_cursor_can_be_serialized():
    ts = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    cursor = TimelineCursor(timestamp=ts)

    payload = cursor.to_dict()

    assert payload == {
        "timestamp": ts.isoformat()
    }


def test_cursor_can_be_deserialized():
    ts = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    cursor = TimelineCursor.from_dict(
        {"timestamp": ts.isoformat()}
    )

    assert cursor.timestamp == ts


def test_cursor_comparison_with_other_type_fails():
    cursor = TimelineCursor(timestamp=datetime.now(timezone.utc))

    with pytest.raises(TypeError):
        _ = cursor < "not-a-cursor"

def test_cursor_now_factory():
    before = datetime.now(timezone.utc)

    cursor = TimelineCursor.now()

    after = datetime.now(timezone.utc)

    assert isinstance(cursor, TimelineCursor)
    assert before <= cursor.timestamp <= after