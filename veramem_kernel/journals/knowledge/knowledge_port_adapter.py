# kernel/journals/knowledge/knowledge_port_adapter.py

from veramem_kernel.journals.knowledge.knowledge_journal import KnowledgeJournal
from veramem_kernel.ports.knowledge_port import KnowledgePort


class KnowledgeJournalAdapter(KnowledgePort):
    def __init__(self, journal: KnowledgeJournal):
        self._journal = journal

    def append(self, event):
        self._journal.append(event)
