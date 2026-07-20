# veramem_kernel/kernel/journals/timeline/timeline_journal.py

from typing import List
from threading import Lock
from datetime import datetime, timezone, timedelta

from .timeline_entry import TimelineEntry
from veramem_kernel.invariants.timeline.timeline_invariants import (
    assert_entry_has_timestamp,
    assert_monotonic,
)

MAX_DRIFT = timedelta(seconds=30)

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
        self._entry_ids: set[str] = set()
        self._lock = Lock()
        self._lamport = 0
        self._device_id = "0" * 64

    # ------------------------------------------------------------------
    # Write API
    # ------------------------------------------------------------------

    def append(self, entry: TimelineEntry) -> None:
        """
        Append a timeline entry to the journal.

        Timeline invariants are enforced at append time.
        """
        with self._lock:
            # 🔒 Local invariant (explicit)
            assert_entry_has_timestamp(entry)

            now = datetime.now(timezone.utc)
            if entry.created_at > now + MAX_DRIFT:
                raise ValueError("Timeline entry timestamp too far in the future.")

            # 🔒 Global invariant (monotonic time)
            if self._entries:
                last = self._entries[-1]
                # Local audit invariant only (not required for distributed causal order)
                assert_monotonic(last, entry)

            if entry.entry_id in self._entry_ids:
                raise ValueError("Duplicate timeline entry_id detected.")
            
            # Assign Lamport deterministically
            lamport = max(self._lamport + 1, entry.lamport)
            self._lamport = lamport

            # enforce device ownership
            if entry.device_id != self._device_id:
                raise ValueError("device_id mismatch for local journal")

            # rebuild immutable entry
            entry = TimelineEntry(
                entry_id=entry.entry_id,
                created_at=entry.created_at,
                type=entry.type,
                title=entry.title,
                description=entry.description,
                action_id=entry.action_id,
                place_id=entry.place_id,
                origin_ref=entry.origin_ref,
                nature=entry.nature,
                device_id=self._device_id,
                lamport=lamport,
            )

            self._entry_ids.add(entry.entry_id)
            self._entries.append(entry)


    # ------------------------------------------------------------------
    # Read API
    # ------------------------------------------------------------------

    def list_events(self) -> List[TimelineEntry]:
        """
        Return all recorded timeline entries.

        A defensive copy is returned to prevent external mutation.
        """
        with self._lock:
            return list(self._entries)

    # ------------------------------------------------------------------
    # Test / lifecycle helpers
    # ------------------------------------------------------------------

    def _reset_for_tests(self) -> None:
        """
        TEST-ONLY METHOD.
        Clears all recorded timeline entries.
        MUST NOT be used in production code.
        """
        with self._lock:
            self._entries.clear()
            self._entry_ids.clear()


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
    _DEFAULT_TIMELINE_JOURNAL._reset_for_tests()
