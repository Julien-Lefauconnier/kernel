# kernel/ports/knowledge_port.py

from typing import Protocol
from kernel.journals.knowledge.knowledge_event import KnowledgeEvent


class KnowledgePort(Protocol):
    def append(self, event: KnowledgeEvent) -> None: ...
