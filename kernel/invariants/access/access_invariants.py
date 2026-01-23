# kernel/invariants/access/access_invariants.py

from kernel.access.access_context import AccessContext
from kernel.access.access_decision import AccessDecision


def assert_valid_context(context: AccessContext) -> None:
    if not context.user_id:
        raise ValueError("AccessContext.user_id must be defined.")


def assert_valid_decision(decision: AccessDecision) -> None:
    if decision not in (AccessDecision.ALLOW, AccessDecision.DENY):
        raise ValueError("Invalid AccessDecision value.")
