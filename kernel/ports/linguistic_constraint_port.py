# kernel/ports/linguistic_constraint_port.py

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Protocol, Optional

from kernel.journals.linguistic_constraint.linguistic_constraint_event import (
    LinguisticConstraintEvent,
)


class LinguisticConstraintWriterPort(Protocol):
    def record(self, event: LinguisticConstraintEvent) -> None: ...


class LinguisticConstraintReaderPort(Protocol):
    def list_for_user(
        self,
        *,
        user_id: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> Iterable[LinguisticConstraintEvent]: ...
