# kernel/journals/knowledge/knowledge_journal.py


from typing import Iterable, List

from kernel.journals.knowledge.knowledge_event import KnowledgeEvent


class KnowledgeJournal:
    """
    Append-only kernel journal for knowledge events.
    No interpretation, no state derivation.
    """

    def __init__(self) -> None:
        self._events: List[KnowledgeEvent] = []

    def append(self, event: KnowledgeEvent) -> None:
        if not isinstance(event, KnowledgeEvent):
            raise TypeError("KnowledgeJournal only accepts KnowledgeEvent")

        self._events.append(event)

    def iter_events(self) -> Iterable[KnowledgeEvent]:
        return tuple(self._events)
