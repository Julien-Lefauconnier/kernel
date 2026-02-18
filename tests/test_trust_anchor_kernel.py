# tests/test_trust_anchor_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.common.trust_anchor import TrustAnchor, RollbackDetected
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


def _cursor(entries: int, head: str | None = None) -> TimelineCursor:
    return TimelineCursor(
        timestamp=datetime.fromtimestamp(100, tz=timezone.utc),
        head=head,
        total_entries=entries,
    )


def test_anchor_initial_accepts_any():
    anchor = TrustAnchor()

    c = _cursor(5, "a" * 64)
    anchor.verify(c)


def test_anchor_advances():
    anchor = TrustAnchor()

    c1 = _cursor(5, "a" * 64)
    anchor = anchor.advance(c1)

    c2 = _cursor(10, "b" * 64)
    anchor = anchor.advance(c2)

    assert anchor.best == c2


def test_anchor_rejects_rollback_height():
    anchor = TrustAnchor(best=_cursor(10, "a" * 64))

    with pytest.raises(RollbackDetected):
        anchor.verify(_cursor(5, "b" * 64))


def test_anchor_rejects_conflicting_same_height():
    anchor = TrustAnchor(best=_cursor(10, "a" * 64))

    with pytest.raises(RollbackDetected):
        anchor.verify(_cursor(10, "b" * 64))


def test_anchor_allows_same_cursor():
    c = _cursor(10, "a" * 64)
    anchor = TrustAnchor(best=c)

    anchor.verify(c)
