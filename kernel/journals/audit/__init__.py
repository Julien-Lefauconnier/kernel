# kernel/journals/audit/__init__.py

from kernel.journals.audit.audit_journal import AuditJournal

_audit_journal: AuditJournal | None = None


def get_audit_journal() -> AuditJournal:
    global _audit_journal
    if _audit_journal is None:
        _audit_journal = AuditJournal()
    return _audit_journal
