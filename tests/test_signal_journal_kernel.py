# kernel/tests/test_signal_journal_kernel.py

from datetime import datetime, timedelta

from kernel.signals.signal import Signal
from kernel.signals.signal_journal import SignalJournal


def test_signal_journal_append_is_append_only():
    """
    Kernel invariant:
    SignalJournal must be append-only.
    """
    journal = SignalJournal()

    signal1 = Signal.unsafe(payload="first", origin="test")
    signal2 = Signal.unsafe(payload="second", origin="test")

    journal.append(signal1)
    journal.append(signal2)

    signals = journal.list_signals()

    assert len(signals) == 2
    assert signals[0] is signal1
    assert signals[1] is signal2


def test_signal_journal_preserves_insertion_order():
    """
    Kernel invariant:
    Signal insertion order must be preserved.
    """
    journal = SignalJournal()

    t0 = datetime.utcnow()
    t1 = t0 + timedelta(seconds=1)

    signal1 = Signal(
        signal_id="sig-1",
        timestamp=t0,
        payload="first",
        origin=None,
    )
    signal2 = Signal(
        signal_id="sig-2",
        timestamp=t1,
        payload="second",
        origin=None,
    )

    journal.append(signal1)
    journal.append(signal2)

    signals = journal.list_signals()

    assert [s.signal_id for s in signals] == ["sig-1", "sig-2"]


def test_signal_journal_can_be_reset_for_tests():
    """
    Kernel invariant:
    SignalJournal can be reset (tests only).
    """
    journal = SignalJournal()

    journal.append(Signal.unsafe(payload="x"))
    journal.append(Signal.unsafe(payload="y"))

    assert len(journal.list_signals()) == 2

    journal.reset()

    assert journal.list_signals() == []
