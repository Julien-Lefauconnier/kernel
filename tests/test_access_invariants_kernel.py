# tests/test_access_invariants_kernel.py

import pytest

from kernel.access.access_context import AccessContext
from kernel.access.access_decision import AccessDecision
from kernel.invariants.access.access_invariants import (
    assert_valid_context,
    assert_valid_decision,
)


def test_valid_context_passes():
    ctx = AccessContext(user_id="user-1")
    assert_valid_context(ctx)


def test_missing_user_id_is_rejected():
    ctx = AccessContext(user_id="")

    with pytest.raises(ValueError):
        assert_valid_context(ctx)


def test_valid_decision_passes():
    assert_valid_decision(AccessDecision.ALLOW)
    assert_valid_decision(AccessDecision.DENY)
