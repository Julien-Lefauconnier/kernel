# kernel/signals/lineage/signal_lineage_errors.py

class SignalLineageError(Exception):
    """
    Base class for all signal lineage related errors.
    """


class SignalLineageInvariantViolation(SignalLineageError):
    """
    Raised when a signal lineage invariant is violated.
    """


class SignalLineageResolutionError(SignalLineageError):
    """
    Raised when signal lineage resolution fails due to
    missing, inconsistent, or incomplete lineage data.
    """
