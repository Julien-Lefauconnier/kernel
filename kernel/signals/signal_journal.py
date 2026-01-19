# kernel/signals/signal_journal.py

from typing import List

from kernel.signals.signal import Signal


class SignalJournal:
    """
    Append-only, kernel-level signal journal.

    This journal records raw signals as they are emitted or observed.
    It does NOT:
    - interpret signals
    - trigger behavior
    - route messages
    - apply policies

    It is designed to be:
    - globally readable
    - test-resettable
    - deterministic
    """

    def __init__(self):
        self._signals: List[Signal] = []

    # ------------------------------------------------------------------
    # Write API
    # ------------------------------------------------------------------

    def append(self, signal: Signal) -> None:
        """
        Append a signal to the journal.

        The signal must already respect Signal invariants.
        """
        self._signals.append(signal)

    # ------------------------------------------------------------------
    # Read API
    # ------------------------------------------------------------------

    def list_signals(self) -> List[Signal]:
        """
        Return all recorded signals.

        A defensive copy is returned to prevent external mutation.
        """
        return list(self._signals)

    # ------------------------------------------------------------------
    # Test / lifecycle helpers
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Clear all recorded signals.

        Intended for tests only.
        """
        self._signals.clear()


# ------------------------------------------------------------------
# Singleton (V1)
# ------------------------------------------------------------------

_DEFAULT_SIGNAL_JOURNAL = SignalJournal()


def get_signal_journal() -> SignalJournal:
    """
    Return the global signal journal instance.
    """
    return _DEFAULT_SIGNAL_JOURNAL


def list_signals() -> List[Signal]:
    """
    Convenience function for inspection layers.
    """
    return _DEFAULT_SIGNAL_JOURNAL.list_signals()


def reset_signal_journal() -> None:
    """
    Reset the global signal journal (tests only).
    """
    _DEFAULT_SIGNAL_JOURNAL.reset()
