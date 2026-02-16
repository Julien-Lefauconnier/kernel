# kernel/access/access_policy.py

from abc import ABC, abstractmethod
from typing import Any

from veramem_kernel.access.access_decision import AccessDecision
from veramem_kernel.access.access_context import AccessContext


class AccessPolicy(ABC):
    """
    Kernel access policy interface.

    Implementations live OUTSIDE the kernel.
    """

    @abstractmethod
    def decide(
        self,
        *,
        subject: Any,
        context: AccessContext,
    ) -> AccessDecision:
        ...
