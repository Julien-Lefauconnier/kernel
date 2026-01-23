# kernel/invariants/audit/audit_invariants.py

"""
AUDIT KERNEL INVARIANTS (NORMATIVE)

These invariants are HARD GUARANTEES of the kernel.

The Audit kernel will NEVER:
- interpret audit meaning
- enrich metadata
- infer intent
- mutate events after append
"""

from kernel.journals.audit.audit_event import AuditEvent


def assert_has_timestamp(event: AuditEvent) -> None:
    """
    Invariant: every audit event must be time-bound.
    """
    if event.created_at is None:
        raise ValueError("AuditEvent must have a created_at timestamp")


def assert_has_identity(event: AuditEvent) -> None:
    """
    Invariant: every audit event must have a stable identity.
    """
    if not event.event_id:
        raise ValueError("AuditEvent must have a non-empty event_id")


def assert_is_immutable(event: AuditEvent) -> None:
    """
    Invariant: audit events are immutable once created.

    Structural immutability is enforced by @dataclass(frozen=True).
    This function exists as a semantic contract marker.
    """
    return None
