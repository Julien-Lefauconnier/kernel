# veramem_kernel/journals/timeline/timeline_snapshot.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_hashchain import TimelineHashChain
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor



@dataclass(frozen=True)
class TimelineSnapshot:
    """
    Immutable, verifiable view of a timeline.

    This is the canonical kernel boundary for:
    - sync
    - audit
    - zero-knowledge proofs
    - distributed systems
    """

    entries: Tuple[TimelineEntry, ...]
    hashchain: TimelineHashChain

    @property
    def head(self) -> str | None:
        return self.hashchain.head

    @classmethod
    def build(
        cls,
        entries: Iterable[TimelineEntry],
    ) -> "TimelineSnapshot":
        entries_tuple = tuple(entries)
        chain = TimelineHashChain.build(entries_tuple)
        return cls(entries_tuple, chain)

    def verify(self) -> None:
        self.hashchain.verify(self.entries)

    def append(self, entry: TimelineEntry) -> "TimelineSnapshot":
        """
        Incremental deterministic extension of the snapshot.

        This allows:
        - streaming projection
        - distributed sync
        - O(1) append
        """

        new_entries = self.entries + (entry,)
        new_hashchain = self.hashchain.append(entry)

        return TimelineSnapshot(
            entries=new_entries,
            hashchain=new_hashchain,
        )
    
    def cursor(self) -> TimelineCursor:
        """
        Deterministic distributed cursor.
        """
        if not self.entries:
            return TimelineCursor(
                timestamp=datetime.fromtimestamp(0, timezone.utc),
                head=None,
                total_entries=0,
            )

        last = self.entries[-1]

        return TimelineCursor(
            timestamp=last.created_at,
            head=self.hashchain.head,
            total_entries=len(self.entries),
        )

