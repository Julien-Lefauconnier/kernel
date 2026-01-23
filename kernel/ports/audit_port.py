# kernel/ports/audit_port.py

"""
Audit Port — public kernel entrypoint.

This port is the ONLY supported way for external systems
(domain, adapters, integrations) to append audit events
to the kernel.

Rules:
- append-only
- no interpretation
- no exception swallowing (handled by caller if needed)
"""

from kernel.journals.audit.audit_event import AuditEvent
from kernel.journals.audit import get_audit_journal


def append_audit(event: AuditEvent) -> None:
    """
    Append an AuditEvent to the kernel audit journal.

    This function is intentionally minimal:
    - no retries
    - no side effects
    - no error handling beyond type validation
    """
    if not isinstance(event, AuditEvent):
        raise TypeError("append_audit expects an AuditEvent")

    journal = get_audit_journal()
    journal.append(event)
