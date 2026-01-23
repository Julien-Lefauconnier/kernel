# tests/test_access_context_kernel.py

import pytest
from kernel.access.access_context import AccessContext


def test_access_context_is_immutable():
    ctx = AccessContext(user_id="user-1", place_id="place-1")

    with pytest.raises(Exception):
        ctx.user_id = "other"


def test_access_context_accepts_optional_place():
    ctx = AccessContext(user_id="user-1")

    assert ctx.user_id == "user-1"
    assert ctx.place_id is None
