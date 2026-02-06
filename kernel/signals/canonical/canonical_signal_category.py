# kernel/signals/canonical/canonical_signal_category.py

from enum import Enum


class CanonicalSignalCategory(str, Enum):
    COGNITIVE_STATE = "cognitive_state"
    TEMPORAL_STATE = "temporal_state"
    KNOWLEDGE_STATE = "knowledge_state"
    ACCESS_STATE = "access_state"
    GOVERNANCE_STATE = "governance_state"
    OBSERVATION_STATE = "observation_state"
