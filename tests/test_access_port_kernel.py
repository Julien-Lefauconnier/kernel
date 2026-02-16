# tests/test_access_port_kernel.py

from veramem_kernel.ports.access_port import decide_access
from veramem_kernel.access.access_context import AccessContext
from veramem_kernel.access.access_decision import AccessDecision
from veramem_kernel.access.access_policy import AccessPolicy


class AllowAllPolicy(AccessPolicy):
    def decide(self, *, subject, context: AccessContext) -> AccessDecision:
        return AccessDecision.ALLOW


class DenyAllPolicy(AccessPolicy):
    def decide(self, *, subject, context: AccessContext) -> AccessDecision:
        return AccessDecision.DENY


def test_access_port_allows():
    policy = AllowAllPolicy()
    ctx = AccessContext(user_id="user-1")

    decision = decide_access(
        policy=policy,
        subject="resource",
        context=ctx,
    )

    assert decision == AccessDecision.ALLOW


def test_access_port_denies():
    policy = DenyAllPolicy()
    ctx = AccessContext(user_id="user-1")

    decision = decide_access(
        policy=policy,
        subject="resource",
        context=ctx,
    )

    assert decision == AccessDecision.DENY
