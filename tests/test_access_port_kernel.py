# tests/test_access_port_kernel.py

from kernel.ports.access_port import decide_access
from kernel.access.access_context import AccessContext
from kernel.access.access_decision import AccessDecision
from kernel.access.access_policy import AccessPolicy


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
