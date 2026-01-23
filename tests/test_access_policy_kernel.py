# tests/test_access_policy_kernel.py

import pytest
from kernel.access.access_policy import AccessPolicy
from kernel.access.access_context import AccessContext
from kernel.access.access_decision import AccessDecision


class DummyPolicy(AccessPolicy):
    def decide(self, *, subject, context: AccessContext) -> AccessDecision:
        return AccessDecision.ALLOW


def test_access_policy_can_be_implemented():
    policy = DummyPolicy()
    ctx = AccessContext(user_id="user-1")

    decision = policy.decide(subject="anything", context=ctx)

    assert decision == AccessDecision.ALLOW


def test_access_policy_is_abstract():
    with pytest.raises(TypeError):
        AccessPolicy()  # type: ignore
