# kernel/journals/timeline/timeline_projector.py

"""
TimelineProjector is a PURE structural projection tool.

It:
- does not interpret events
- does not infer causality
- does not guarantee semantic ordering
- does not represent business truth

It is OPTIONAL.
Consumers MAY replace it with their own projector.
"""


from typing import Iterable, List, Any
import hashlib
from datetime import datetime

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent

from veramem_kernel.journals.action.action_event import ActionEvent
from veramem_kernel.journals.action.action_validation_event import ActionValidationEvent


def _timestamp(evt: Any) -> datetime:
    """
    Canonical timestamp extractor for kernel facts.
    """
    if isinstance(evt, ActionEvent):
        return evt.created_at
    if isinstance(evt, ActionValidationEvent):
        return evt.decided_at
    if isinstance(evt, KnowledgeEvent):
        return evt.created_at
    raise ValueError(f"Unsupported kernel event type: {type(evt)}")


def _stable_entry_id(evt: Any) -> str:
    """
    Deterministic ID derived from kernel facts.
    """
    if not hasattr(evt, "event_id"):
        raise ValueError("Kernel event missing event_id.")

    payload = (
        type(evt).__name__,
        evt.event_id,
    )
    return hashlib.sha256(str(payload).encode()).hexdigest()


def project_timeline(
    *,
    events: Iterable[Any],
) -> List[TimelineEntry]:
    """
    Deterministic and idempotent projection of kernel facts into timeline entries.

    Guarantees:
    - purity
    - determinism
    - idempotence
    - replay safety
    - order invariance
    """

    # ------------------------------------------------------------------
    # 1) Input normalization
    # ------------------------------------------------------------------

    # Deduplicate by kernel identity
    unique = {}
    for evt in events:
        event_id = getattr(evt, "event_id", None)
        if event_id is None:
            raise ValueError("Kernel events must expose a stable event_id.")
        unique[event_id] = evt

    # ------------------------------------------------------------------
    # 2) Stable canonical ordering
    # ------------------------------------------------------------------

    sorted_events = sorted(
        unique.values(),
        key=lambda e: (_timestamp(e), getattr(e, "event_id")),
    )

    # ------------------------------------------------------------------
    # 3) Projection
    # ------------------------------------------------------------------

    entries: List[TimelineEntry] = []

    for evt in sorted_events:

        if isinstance(evt, ActionEvent):
            entries.append(
                TimelineEntry(
                    entry_id=_stable_entry_id(evt),
                    created_at=evt.created_at,
                    type=TimelineEntryType.ACTION_PROPOSED,
                    title="An action was proposed",
                    description=None,
                    action_id=evt.action_ref,
                    place_id=evt.place_ref,
                    origin_ref="kernel",
                    nature=TimelineEntryNature.EVENT,
                )
            )

        elif isinstance(evt, ActionValidationEvent):
            entry_type = (
                TimelineEntryType.ACTION_VALIDATED
                if evt.decision == "ACCEPTED"
                else TimelineEntryType.ACTION_REFUSED
            )

            entries.append(
                TimelineEntry(
                    entry_id=_stable_entry_id(evt),
                    created_at=evt.decided_at,
                    type=entry_type,
                    title="Action accepted" if evt.decision == "ACCEPTED" else "Action refused",
                    description=None,
                    action_id=evt.action_ref,
                    place_id=evt.place_ref,
                    origin_ref="kernel",
                    nature=TimelineEntryNature.EVENT,
                )
            )

        elif isinstance(evt, KnowledgeEvent):
            entries.append(
                TimelineEntry(
                    entry_id=_stable_entry_id(evt),
                    created_at=evt.created_at,
                    type=TimelineEntryType.SYSTEM_NOTICE,
                    title="Knowledge state updated",
                    description=None,
                    action_id=None,
                    place_id=evt.place_ref,
                    origin_ref="kernel",
                    nature=TimelineEntryNature.STATE,
                )
            )

        else:
            raise ValueError(f"Unsupported kernel event type: {type(evt)}")

    return entries

