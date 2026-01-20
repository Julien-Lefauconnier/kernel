# kernel/journals/timeline/timeline_projector.py

from typing import Iterable, List, Any
from uuid import uuid4
from datetime import datetime

from kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from kernel.journals.timeline.timeline_types import TimelineEntryType
from kernel.journals.knowledge.knowledge_event import KnowledgeEvent

from kernel.journals.action.action_event import ActionEvent
from kernel.journals.action.action_validation_event import ActionValidationEvent


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



def project_timeline(
    *,
    events: Iterable[Any],
) -> List[TimelineEntry]:
    """
    Deterministic projection of kernel facts into timeline entries.

    - Pure function
    - No side effects
    - No inference
    - Zero-knowledge compliant
    """

    entries: List[TimelineEntry] = []

    # 1) Sort facts by their canonical timestamp
    sorted_events = sorted(events, key=_timestamp)

    # 2) Project facts → timeline entries
    for evt in sorted_events:
        
        # -------------------------
        # Action proposed
        # -------------------------
        if isinstance(evt, ActionEvent):
            entries.append(
                TimelineEntry(
                    entry_id=str(uuid4()),
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

        # -------------------------
        # Action validation
        # -------------------------
        elif isinstance(evt, ActionValidationEvent):
            entry_type = (
                TimelineEntryType.ACTION_VALIDATED
                if evt.decision == "ACCEPTED"
                else TimelineEntryType.ACTION_REFUSED
            )

            entries.append(
                TimelineEntry(
                    entry_id=str(uuid4()),
                    created_at=evt.decided_at,
                    type=entry_type,
                    title=(
                        "Action accepted"
                        if evt.decision == "ACCEPTED"
                        else "Action refused"
                    ),
                    description=None,
                    action_id=evt.action_ref,
                    place_id=evt.place_ref,
                    origin_ref="kernel",
                    nature=TimelineEntryNature.EVENT,
                )
            )
        
        # -------------------------
        # Knowledge state (STATE)
        # -------------------------
        elif isinstance(evt, KnowledgeEvent):
            entries.append(
                TimelineEntry(
                    entry_id=str(uuid4()),
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
