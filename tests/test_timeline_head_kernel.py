# tests/test_timeline_head_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_head import JournalHead


def test_head_is_constructible_and_immutable():
    now = datetime.now(timezone.utc)
    head = JournalHead(
        last_hash="0" * 64,
        last_timestamp=now,
        total_entries=12,
    )

    assert head.last_hash == "0" * 64
    assert head.last_timestamp == now
    assert head.total_entries == 12

    with pytest.raises(Exception):
        # frozen dataclass: must be immutable
        head.total_entries = 13  # type: ignore[misc]


def test_head_rejects_non_utc_timestamp():
    now_naive = datetime.utcnow()  # naive
    with pytest.raises(ValueError):
        JournalHead(last_hash="0" * 64, last_timestamp=now_naive, total_entries=1)

    # Explicit non-UTC timezone
    from datetime import timedelta
    non_utc = datetime(2020, 1, 1, tzinfo=timezone(timedelta(hours=2)))

    with pytest.raises(ValueError):
        JournalHead(last_hash="0" * 64, last_timestamp=non_utc, total_entries=1)



def test_head_rejects_invalid_hash_format():
    now = datetime.now(timezone.utc)

    with pytest.raises(ValueError):
        JournalHead(last_hash="abc", last_timestamp=now, total_entries=1)  # too short

    with pytest.raises(ValueError):
        JournalHead(last_hash=("g" * 64), last_timestamp=now, total_entries=1)  # not hex

    with pytest.raises(ValueError):
        JournalHead(last_hash=("0" * 63) + " ", last_timestamp=now, total_entries=1)  # not normalized


def test_head_empty_is_canonical():
    head = JournalHead.empty()
    assert head.total_entries == 0
    assert head.last_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert head.last_timestamp.tzinfo is not None
    assert head.last_timestamp.tzinfo.utcoffset(head.last_timestamp).total_seconds() == 0


def test_head_advance_is_deterministic():
    base = JournalHead.empty()
    t1 = datetime.fromtimestamp(1, tz=timezone.utc)
    t2 = datetime.fromtimestamp(2, tz=timezone.utc)

    h1 = base.advance(new_hash="1" * 64, new_timestamp=t1)
    h2 = h1.advance(new_hash="2" * 64, new_timestamp=t2)

    assert h1.total_entries == 1
    assert h1.last_hash == "1" * 64
    assert h1.last_timestamp == t1

    assert h2.total_entries == 2
    assert h2.last_hash == "2" * 64
    assert h2.last_timestamp == t2
