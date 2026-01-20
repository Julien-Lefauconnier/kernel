# tests/test_timeline_projector_kernel.py

from datetime import datetime, timedelta

from kernel.journals.timeline.timeline_projector import project_timeline
from kernel.journals.timeline.timeline_types import TimelineEntryType

from kernel.journals.action.action_event import ActionEvent
from kernel.journals.action.action_validation_event import ActionValidationEvent
from kernel.journals.knowledge.knowledge_event import KnowledgeEvent



def make_action(
    *,
    event_id="a1",
    created_at=None,
):
    return ActionEvent(
        event_id=event_id,
        created_at=created_at or datetime.utcnow(),
        user_ref="u1",
        place_ref="p1",
        action_ref="act-1",
        intent="remember",
    )


def make_validation(
    *,
    event_id="v1",
    decision="ACCEPTED",
    decided_at=None,
):
    return ActionValidationEvent(
        event_id=event_id,
        action_ref="act-1",
        user_ref="u1",
        place_ref="p1",
        decision=decision,
        decided_at=decided_at or datetime.utcnow(),
    )


# -------------------------------------------------
# Basic behavior
# -------------------------------------------------

def test_project_empty_timeline():
    entries = project_timeline(events=[])
    assert entries == []


def test_action_event_projects_to_timeline():
    action = make_action()

    entries = project_timeline(events=[action])

    assert len(entries) == 1
    entry = entries[0]

    assert entry.type == TimelineEntryType.ACTION_PROPOSED
    assert entry.created_at == action.created_at
    assert entry.place_id == action.place_ref
    assert entry.action_id == action.action_ref


def test_validation_event_projects_to_validated():
    validation = make_validation(decision="ACCEPTED")

    entries = project_timeline(events=[validation])

    assert len(entries) == 1
    entry = entries[0]

    assert entry.type == TimelineEntryType.ACTION_VALIDATED
    assert entry.created_at == validation.decided_at


def test_validation_event_projects_to_refused():
    validation = make_validation(decision="REFUSED")

    entries = project_timeline(events=[validation])

    assert entries[0].type == TimelineEntryType.ACTION_REFUSED


# -------------------------------------------------
# Ordering
# -------------------------------------------------

def test_timeline_is_sorted_by_time():
    t0 = datetime.utcnow()
    t1 = t0 + timedelta(seconds=5)

    action = make_action(created_at=t0)
    validation = make_validation(decided_at=t1)

    entries = project_timeline(events=[validation, action])

    assert len(entries) == 2
    assert entries[0].created_at == t0
    assert entries[1].created_at == t1
    assert entries[0].type == TimelineEntryType.ACTION_PROPOSED
    assert entries[1].type in {
        TimelineEntryType.ACTION_VALIDATED,
        TimelineEntryType.ACTION_REFUSED,
    }


# -------------------------------------------------
# Purity
# -------------------------------------------------

def test_projector_is_pure_function():
    action = make_action()
    events = [action]

    entries1 = project_timeline(events=events)
    entries2 = project_timeline(events=events)

    assert entries1 != entries2  # different ids
    assert [e.type for e in entries1] == [e.type for e in entries2]
    assert [e.created_at for e in entries1] == [e.created_at for e in entries2]


# -----------------------
# Test knowledge
# -----------------------

def make_knowledge(*, created_at=None):
    return KnowledgeEvent.create(
        source="cognition",
        knowledge_type="state",
        user_ref="u1",
        place_ref="p1",
        created_at=created_at,
    )


def test_knowledge_event_projects_to_state_entry():
    evt = make_knowledge()

    entries = project_timeline(events=[evt])

    assert len(entries) == 1
    entry = entries[0]

    assert entry.nature.name == "STATE"
    assert entry.type == TimelineEntryType.SYSTEM_NOTICE
    assert entry.created_at == evt.created_at
    assert entry.place_id == "p1"
    assert entry.title == "Knowledge state updated"
