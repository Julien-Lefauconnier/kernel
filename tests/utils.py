# tests/utils.py

from datetime import datetime, timezone

from veramem_kernel.journals.action.action_event import ActionEvent

def fixed_now():
    return datetime(2020, 1, 1, tzinfo=timezone.utc)


def make_action(i: int) -> ActionEvent:
    return ActionEvent.create(
        user_ref="user",
        intent="TEST",
        extras={"i": i},
        created_at=fixed_now(),
    )