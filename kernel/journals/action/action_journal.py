# kernel/journals/action/action_journal.py

from typing import List

from .action_event import ActionEvent


class ActionJournal:
    """
    Kernel Action Journal — append-only, declarative.

    Records the *fact* that an action decision occurred.

    ❌ No cognition
    ❌ No conflicts
    ❌ No presentation
    ❌ No policy

    ✔ Append-only
    ✔ Time-ordered
    ✔ Immutable events
    ✔ Zero-knowledge compatible
    """

    def __init__(self):
        self._events: List[ActionEvent] = []

    # -------------------------------------------------
    # Write API
    # -------------------------------------------------

    def append(self, event: ActionEvent) -> None:
        """
        Append a kernel ActionEvent.

        The event must already respect kernel invariants.
        """
        self._events.append(event)

    # -------------------------------------------------
    # Read API
    # -------------------------------------------------

    def list_events(self) -> List[ActionEvent]:
        """
        Return all recorded action events.

        Defensive copy to prevent mutation.
        """
        return list(self._events)

    # -------------------------------------------------
    # Test helpers
    # -------------------------------------------------

    def reset(self) -> None:
        """
        Clear all recorded events.

        Intended for tests only.
        """
        self._events.clear()


# -------------------------------------------------
# Singleton (V1)
# -------------------------------------------------

_DEFAULT_ACTION_JOURNAL = ActionJournal()


def get_action_journal() -> ActionJournal:
    """
    Return the global kernel ActionJournal.
    """
    return _DEFAULT_ACTION_JOURNAL


def list_action_events() -> List[ActionEvent]:
    """
    Convenience read helper (audit / debug).
    """
    return _DEFAULT_ACTION_JOURNAL.list_events()


def reset_action_journal() -> None:
    """
    Reset the global journal (tests only).
    """
    _DEFAULT_ACTION_JOURNAL.reset()
