# kernel/journals/observation/patterns/normative_pattern.py

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class NormativePattern:
    """
    Deterministic longitudinal pattern projection.

    Derived from observation events.
    Never canonical state.
    """

    pattern_id: str
    user_id: str
    signal_type: str

    occurrences: int
    first_seen_at: datetime
    last_seen_at: datetime

    source_refs: List[str]
