# kernel/ports/signal_port.py

from abc import ABC, abstractmethod
from typing import Iterable

from kernel.signals.signal import Signal


class SignalPort(ABC):
    """
    Kernel input port for signals.

    This port defines how raw signals enter the cognitive kernel.
    """

    @abstractmethod
    def emit(self, signal: Signal) -> None:
        """
        Inject a raw signal into the kernel.

        Implementations must:
        - not mutate the signal
        - not interpret the payload
        - not trigger side effects outside the kernel
        """
        raise NotImplementedError
