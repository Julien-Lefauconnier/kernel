# kernel/tests/test_action_event_kernel.py

from datetime import datetime, timezone
import pytest

from veramem_kernel.journals.action.action_event import ActionEvent


def test_action_event_is_immutable():
    evt = ActionEvent(
        event_id="e1",
        created_at=datetime.now(timezone.utc),
        action_ref="memory.store",
        mode="assisted",
    )

    with pytest.raises(Exception):
        evt.mode = "manual"


def test_action_event_requires_created_at():
    with pytest.raises(ValueError):
        ActionEvent(
            event_id="e2",
            created_at=None,  # type: ignore
        )


def test_action_event_accepts_opaque_metadata():
    evt = ActionEvent(
        event_id="e3",
        created_at=datetime.now(timezone.utc),
        extras={"hash": "abc123", "debug": True},
    )

    assert evt.extras["hash"] == "abc123"
