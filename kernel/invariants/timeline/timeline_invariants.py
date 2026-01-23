# kernel/invariants/timeline/timeline_invariants.py

"""
TIMELINE KERNEL INVARIANTS (NORMATIVE)

These invariants are HARD GUARANTEES of the kernel.
Any consumer relying on this kernel may assume they are always true.

The kernel will NEVER:
- infer intent
- reorder events semantically
- enrich entries with meaning
- mutate entries after append
"""

from kernel.journals.timeline.timeline_entry import TimelineEntry


def assert_entry_has_timestamp(entry: TimelineEntry) -> None:
    """
    Invariant: every timeline entry must be strictly time-bound.
    """
    if entry.created_at is None:
        raise ValueError(
            "TimelineEntry must have a non-null created_at timestamp."
        )


def assert_monotonic(previous: TimelineEntry, current: TimelineEntry) -> None:
    """
    Invariant: timeline entries must be appended in non-decreasing
    temporal order.

    current.created_at must be >= previous.created_at
    """
    if current.created_at < previous.created_at:
        raise ValueError(
            "Timeline invariant violation: non-monotonic append "
            f"(previous={previous.created_at}, current={current.created_at})."
        )


def assert_immutable(entry: TimelineEntry) -> None:
    """
    Invariant: timeline entries are immutable once created.

    This invariant is guaranteed structurally by frozen dataclasses,
    but kept here as a semantic contract reference.
    """
    # Structural immutability is enforced by @dataclass(frozen=True)
    # This function exists for contract completeness.
    return None
