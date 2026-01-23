# tests/test_access_decision_kernel.py

from kernel.access.access_decision import AccessDecision


def test_access_decision_enum_values():
    assert AccessDecision.ALLOW.value == "allow"
    assert AccessDecision.DENY.value == "deny"


def test_access_decision_is_str_enum():
    assert isinstance(AccessDecision.ALLOW.value, str)
