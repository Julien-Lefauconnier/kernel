# kernel/ports/timeline_port.py

from abc import ABC, abstractmethod
from typing import Iterable

from kernel.journals.timeline.timeline_entry import TimelineEntry


class TimelinePort(ABC):
    """
    Kernel output port for timeline observation.

    This port defines how external systems observe
    kernel-level timeline facts.
    """

    @abstractmethod
    def list_entries(self) -> Iterable[TimelineEntry]:
        """
        Return all known timeline entries.

        Implementations must:
        - preserve entry immutability
        - not reorder or filter facts
        """
        raise NotImplementedError
