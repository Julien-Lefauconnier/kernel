# veramem_kernel/journals/knowledge/knowledge_journal.py

from __future__ import annotations

from typing import Iterable, List
from threading import Lock
from datetime import datetime, timezone, timedelta

from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent

MAX_DRIFT = timedelta(minutes=5)


class KnowledgeJournal:
    """
    Append-only kernel journal for knowledge events.
    No interpretation, no state derivation.
    """

    def __init__(self) -> None:
        self._events: List[KnowledgeEvent] = []
        self._event_ids: set[str] = set()
        self._lock = Lock()

    def append(self, event: KnowledgeEvent) -> None:
        if not isinstance(event, KnowledgeEvent):
            raise TypeError("KnowledgeJournal only accepts KnowledgeEvent")

        with self._lock:
            now = datetime.now(timezone.utc)
            if event.created_at > now + MAX_DRIFT:
                raise ValueError("KnowledgeEvent.created_at too far in the future.")

            if self._events:
                last = self._events[-1]
                if event.created_at < last.created_at:
                    raise ValueError("KnowledgeJournal requires monotonic timestamps.")

            if event.event_id in self._event_ids:
                raise ValueError("Duplicate KnowledgeEvent.event_id detected.")

            self._event_ids.add(event.event_id)
            self._events.append(event)

    def iter_events(self) -> Iterable[KnowledgeEvent]:
        with self._lock:
            return tuple(self._events)

    def _reset_for_tests(self) -> None:
        with self._lock:
            self._events.clear()
            self._event_ids.clear()

# ------------------------------------------------------------------
# Global registry (kernel-safe singleton)
# ------------------------------------------------------------------

from typing import Optional

_GLOBAL_KNOWLEDGE_JOURNAL: Optional[KnowledgeJournal] = None


def get_knowledge_journal() -> KnowledgeJournal:
    global _GLOBAL_KNOWLEDGE_JOURNAL
    if _GLOBAL_KNOWLEDGE_JOURNAL is None:
        _GLOBAL_KNOWLEDGE_JOURNAL = KnowledgeJournal()
    return _GLOBAL_KNOWLEDGE_JOURNAL


def reset_knowledge_journal() -> None:
    journal = get_knowledge_journal()
    journal._reset_for_tests()


