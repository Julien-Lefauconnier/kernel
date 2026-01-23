# kernel/journals/knowledge/__init__.py

from kernel.journals.knowledge.knowledge_journal import KnowledgeJournal

_knowledge_journal: KnowledgeJournal | None = None


def get_knowledge_journal() -> KnowledgeJournal:
    global _knowledge_journal
    if _knowledge_journal is None:
        _knowledge_journal = KnowledgeJournal()
    return _knowledge_journal
