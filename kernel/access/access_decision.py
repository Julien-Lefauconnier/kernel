# kernel/access/access_decision.py

from enum import Enum


class AccessDecision(str, Enum):
    """
    Kernel-level access decision.
    """

    ALLOW = "allow"
    DENY = "deny"
