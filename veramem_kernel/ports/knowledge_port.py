# kernel/ports/knowledge_port.py
"""
Knowledge Port — public kernel entrypoint.

This port is the ONLY supported way for external systems
(domain, adapters, integrations) to append knowledge events
to the kernel.

Rules:
- append-only
- no interpretation
- no enrichment
- kernel remains zero-knowledge
"""

from abc import ABC, abstractmethod

from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent
from veramem_kernel.journals.knowledge import get_knowledge_journal



class KnowledgePort(ABC):
    @abstractmethod
    def append(self, event: KnowledgeEvent) -> None:
        pass

def append_knowledge(event: KnowledgeEvent) -> None:
    """
    Append a KnowledgeEvent to the kernel knowledge journal.

    - No retries
    - No side effects
    - No error swallowing
    """
    if not isinstance(event, KnowledgeEvent):
        raise TypeError("append_knowledge expects a KnowledgeEvent")

    journal = get_knowledge_journal()
    journal.append(event)
