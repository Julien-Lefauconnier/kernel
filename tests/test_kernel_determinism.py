# tests/test_kernel_determinism.py

import inspect
from datetime import datetime, timezone

import pytest

from veramem_kernel.journals.timeline.timeline_projector import project_timeline
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor
from veramem_kernel.journals.action.action_event import ActionEvent
from tests.utils import make_action


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def fixed_now() -> datetime:
    return datetime(2000, 1, 1, tzinfo=timezone.utc)


def _build_action_event_kwargs(i: int) -> dict:
    """
    Build kwargs compatible with ActionEvent's current API.

    This is deliberately defensive: the kernel may rename fields
    (action_id vs id, action_type vs type, payload vs data, etc.).
    """
    desired = {
        "action_id": f"act-{i}",
        "id": f"act-{i}",
        "event_id": f"act-{i}",
        "created_at": fixed_now(),
        "timestamp": fixed_now(),
        "actor": "user",
        "action_type": "TEST",
        "type": "TEST",
        "payload": {"i": i},
        "data": {"i": i},
    }

    # If ActionEvent exposes a factory, prefer it.
    if hasattr(ActionEvent, "create") and callable(getattr(ActionEvent, "create")):
        sig = inspect.signature(ActionEvent.create)
        out = {}
        for name in sig.parameters.keys():
            if name in desired:
                out[name] = desired[name]
        return out

    # Otherwise, use constructor signature.
    sig = inspect.signature(ActionEvent)
    out = {}
    for name in sig.parameters.keys():
        if name in ("self",):
            continue
        if name in desired:
            out[name] = desired[name]
    return out


# ---------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------

def test_timeline_projection_is_deterministic():
    events = [make_action(i) for i in range(5)]

    e1 = project_timeline(events=events)
    e2 = project_timeline(events=events)

    assert e1 == e2


def test_projection_is_order_invariant():
    events1 = [make_action(i) for i in range(5)]
    events2 = list(reversed(events1))

    p1 = project_timeline(events=events1)
    p2 = project_timeline(events=events2)

    # Industrial kernel: projection must be canonical
    assert p1 == p2



def test_projection_does_not_mutate_input():
    events = [make_action(i) for i in range(3)]
    before = list(events)

    project_timeline(events=events)

    assert events == before


# ---------------------------------------------------------------------
# Cursor determinism
# ---------------------------------------------------------------------

def test_timeline_cursor_is_stable():
    t = fixed_now()
    c1 = TimelineCursor(t)
    c2 = TimelineCursor(t)

    assert c1 == c2
    assert hash(c1) == hash(c2)


# ---------------------------------------------------------------------
# Replay stability
# ---------------------------------------------------------------------

def test_replay_produces_identical_results():
    events = [make_action(i) for i in range(10)]

    first = project_timeline(events=events)
    second = project_timeline(events=list(events))

    assert first == second
