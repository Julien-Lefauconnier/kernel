# kernel/journals/linguistic_constraint/linguistic_constraint_journal.py

from __future__ import annotations

from datetime import datetime
from typing import List, Protocol, Optional

from .linguistic_constraint_event import LinguisticConstraintEvent


class LinguisticConstraintJournal(Protocol):
    def append(self, event: LinguisticConstraintEvent) -> None: ...

    def list_for_user(
        self,
        *,
        user_id: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> List[LinguisticConstraintEvent]: ...
