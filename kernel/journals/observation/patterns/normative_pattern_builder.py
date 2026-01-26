# kernel/journals/observation/patterns/normative_pattern_builder.py

import hashlib
from typing import Dict, Iterable, Tuple, List

from kernel.journals.observation.observation_event import ObservationEvent
from kernel.journals.observation.patterns.normative_pattern import NormativePattern


class NormativePatternBuilder:
    """
    Pure deterministic projection builder.

    Groups normative observation events.
    """

    @staticmethod
    def _make_id(user_id: str, signal_type: str) -> str:
        raw = f"{user_id}:normative:{signal_type}"
        return hashlib.sha256(raw.encode()).hexdigest()

    @classmethod
    def build(
        cls,
        *,
        events: Iterable[ObservationEvent],
    ) -> List[NormativePattern]:

        grouped: Dict[Tuple[str, str], List[ObservationEvent]] = {}

        for e in events:
            if e.source_type != "normative":
                continue

            signal_type = getattr(e.payload, "signal_type", None)
            if signal_type is None:
                continue

            grouped.setdefault((e.user_id, signal_type), []).append(e)

        patterns: List[NormativePattern] = []

        for (user_id, signal_type), items in grouped.items():
            items = sorted(items, key=lambda x: x.created_at)

            patterns.append(
                NormativePattern(
                    pattern_id=cls._make_id(user_id, signal_type),
                    user_id=user_id,
                    signal_type=signal_type,
                    occurrences=len(items),
                    first_seen_at=items[0].created_at,
                    last_seen_at=items[-1].created_at,
                    source_refs=[],
                )
            )

        return patterns
