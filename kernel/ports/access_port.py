# kernel/ports/access_port.py

from typing import Any

from kernel.access.access_context import AccessContext
from kernel.access.access_decision import AccessDecision


def decide_access(
    *,
    policy,
    subject: Any,
    context: AccessContext,
) -> AccessDecision:
    """
    Kernel access decision port.

    The kernel does NOT provide implementations.
    """
    return policy.decide(subject=subject, context=context)
