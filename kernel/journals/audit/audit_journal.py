# kernel/journals/audit/audit_journal.py

from typing import Iterable, List

from kernel.journals.audit.audit_event import AuditEvent


class AuditJournal:
    """
    Append-only kernel journal for audit events.

    - No interpretation
    - No aggregation
    - No derivation
    """

    def __init__(self) -> None:
        self._events: List[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        if not isinstance(event, AuditEvent):
            raise TypeError("AuditJournal only accepts AuditEvent")

        self._events.append(event)

    def iter_events(self) -> Iterable[AuditEvent]:
        return tuple(self._events)
