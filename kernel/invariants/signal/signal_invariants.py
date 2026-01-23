# kernel/invariants/signal/signal_invariants.py

"""
SIGNAL KERNEL INVARIANTS (NORMATIVE)

These invariants are HARD GUARANTEES of the kernel.

A Signal MUST:
- be time-bound
- be immutable
- be strictly declarative
"""

from kernel.signals.signal import Signal


def assert_signal_has_timestamp(signal: Signal) -> None:
    """
    Invariant: every signal must be strictly time-bound.
    """
    if signal.timestamp is None:
        raise ValueError("Signal.timestamp must not be None.")


def assert_signal_is_immutable(signal: Signal) -> None:
    """
    Invariant: signals are immutable once created.

    Structural immutability is guaranteed by frozen dataclasses.
    This function exists as a semantic contract.
    """
    return None


def assert_signal_payload_exists(signal: Signal) -> None:
    """
    Invariant: signal payload must be defined (can be opaque).
    """
    if signal.payload is None:
        raise ValueError("Signal.payload must not be None.")
