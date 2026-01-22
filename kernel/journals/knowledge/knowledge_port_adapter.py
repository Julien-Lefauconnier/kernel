# kernel/journals/knowledge/knowledge_port_adapter.py

from kernel.journals.knowledge.knowledge_journal import KnowledgeJournal
from kernel.ports.knowledge_port import KnowledgePort


class KnowledgeJournalAdapter(KnowledgePort):
    def __init__(self, journal: KnowledgeJournal):
        self._journal = journal

    def append(self, event):
        self._journal.append(event)
