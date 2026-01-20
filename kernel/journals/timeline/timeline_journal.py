# kernel/kernel/journals/timeline/timeline_journal.py

from typing import List

from .timeline_entry import TimelineEntry
from kernel.invariants.timeline.timeline_invariants import (
    assert_entry_has_timestamp,
    assert_monotonic,
)


class TimelineJournal:
    """
    Append-only, fact-based timeline journal.

    This journal records *actual timeline facts* as they occur.
    It does NOT:
    - rebuild timelines
    - apply governance or policies
    - render views
    - infer meaning

    It is designed to be:
    - globally readable
    - test-resettable
    - audit-compatible
    """

    def __init__(self):
        self._entries: List[TimelineEntry] = []

    # ------------------------------------------------------------------
    # Write API
    # ------------------------------------------------------------------

    def append(self, entry: TimelineEntry) -> None:
        """
        Append a timeline entry to the journal.

        Timeline invariants are enforced at append time.
        """
        # 🔒 Local invariant (explicit)
        assert_entry_has_timestamp(entry)

        # 🔒 Global invariant (monotonic time)
        if self._entries:
            last = self._entries[-1]
            assert_monotonic(last, entry)

        self._entries.append(entry)


    # ------------------------------------------------------------------
    # Read API
    # ------------------------------------------------------------------

    def list_events(self) -> List[TimelineEntry]:
        """
        Return all recorded timeline entries.

        A defensive copy is returned to prevent external mutation.
        """
        return list(self._entries)

    # ------------------------------------------------------------------
    # Test / lifecycle helpers
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Clear all recorded entries.

        Intended for tests only.
        """
        self._entries.clear()


# ------------------------------------------------------------------
# Singleton (V1)
# ------------------------------------------------------------------

_DEFAULT_TIMELINE_JOURNAL = TimelineJournal()


def get_timeline_journal() -> TimelineJournal:
    """
    Return the global timeline journal instance.
    """
    return _DEFAULT_TIMELINE_JOURNAL


def list_timeline_events() -> List[TimelineEntry]:
    """
    Convenience function for audit / inspection layers.
    """
    return _DEFAULT_TIMELINE_JOURNAL.list_events()


def reset_timeline_journal() -> None:
    """
    Reset the global timeline journal (tests only).
    """
    _DEFAULT_TIMELINE_JOURNAL.reset()
