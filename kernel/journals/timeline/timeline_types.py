# kernel/kernel/journals/timeline/timeline_types.py
from enum import Enum


class TimelineEntryType(str, Enum):
    """
    Declarative types for timeline entries.

    Timeline entry types are:
    - descriptive
    - non-executable
    - zero-knowledge compliant

    They classify *what kind of event* occurred,
    not *why* or *with what content*.
    """

    # --- Action lifecycle ---
    ACTION_PROPOSED = "action_proposed"
    ACTION_VALIDATED = "action_validated"
    ACTION_REFUSED = "action_refused"
    ACTION_BLOCKED = "action_blocked"

    # --- Cognitive / epistemic ---
    KNOWLEDGE_STATE = "knowledge_state"
    CONFLICT = "conflict"
    SYSTEM_NOTICE = "system_notice"
    REASONING_GAP = "reasoning_gap"
    REASONING_INTENT = "reasoning_intent"
    GOVERNANCE_NOTICE = "governance_notice"
    UNCERTAINTY_FRAME = "uncertainty_frame"
    UNDERSTANDING_STATE = "understanding_state"
    SELF_MODEL_NOTICE = "self_model_notice"
    INTROSPECTION_STATE = "introspection_state"
    MEMORY_LONG_STATE = "memory_long_state"

    # --- Linguistic observability ---
    LINGUISTIC_CONSTRAINT = "linguistic_constraint"

    # --- Human observability ---
    HUMAN_FEEDBACK = "human_feedback"

    # --- Document access & edits ---
    DOCUMENT_ACCESSED = "document_accessed"
    DOCUMENT_EDITED = "document_edited"

    # Lower number = higher cognitive priority
    @property
    def governance_priority(self) -> int:
        return {
            TimelineEntryType.REASONING_GAP: 10,
            TimelineEntryType.UNCERTAINTY_FRAME: 15,
            TimelineEntryType.REASONING_INTENT: 20,
            TimelineEntryType.GOVERNANCE_NOTICE: 30,
        }.get(self, 100)
