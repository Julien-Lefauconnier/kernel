# kernel/journals/action/action_validation_journal.py

from typing import List

from .action_validation_event import ActionValidationEvent


class ActionValidationJournal:
    """
    Kernel Action Validation Journal — append-only, declarative.

    Records immutable user validation facts.

    ✔ Append-only
    ✔ Time-ordered
    ✔ Replayable
    ✔ Audit-compatible
    """

    def __init__(self):
        self._events: List[ActionValidationEvent] = []

    # -------------------------------------------------
    # Write API
    # -------------------------------------------------

    def append(self, event: ActionValidationEvent) -> None:
        """
        Append a kernel ActionValidationEvent.
        """
        self._events.append(event)

    # -------------------------------------------------
    # Read API
    # -------------------------------------------------

    def list_events(self) -> List[ActionValidationEvent]:
        """
        Return all validation events (defensive copy).
        """
        return list(self._events)

    # -------------------------------------------------
    # Test helpers
    # -------------------------------------------------

    def reset(self) -> None:
        """
        Clear all events (tests only).
        """
        self._events.clear()


# -------------------------------------------------
# Singleton (V1)
# -------------------------------------------------

_DEFAULT_ACTION_VALIDATION_JOURNAL = ActionValidationJournal()


def get_action_validation_journal() -> ActionValidationJournal:
    return _DEFAULT_ACTION_VALIDATION_JOURNAL


def list_action_validation_events() -> List[ActionValidationEvent]:
    return _DEFAULT_ACTION_VALIDATION_JOURNAL.list_events()


def reset_action_validation_journal() -> None:
    _DEFAULT_ACTION_VALIDATION_JOURNAL.reset()
