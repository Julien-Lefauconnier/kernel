# tests/test_observation_port_kernel.py

import pytest
from datetime import datetime

from kernel.ports.observation_port import ObservationPort
from kernel.journals.observation.observation_event import ObservationEvent


class DummyObservationPort(ObservationPort):
    """
    Minimal in-memory implementation used only for kernel port tests.

    Kernel invariant: record() must exist and accept ObservationEvent.
    """

    def __init__(self):
        self.events: list[ObservationEvent] = []

    def record(self, event: ObservationEvent) -> None:
        self.events.append(event)


def test_observation_port_accepts_observation_event():
    """
    ObservationPort must accept append-only ObservationEvent records.
    """

    port = DummyObservationPort()

    event = ObservationEvent(
        user_id="user-1",
        source_type="normative",
        payload={"signal_type": "DISAGREE"},
        created_at=datetime.utcnow(),
    )

    port.record(event)

    assert len(port.events) == 1
    assert port.events[0] == event


def test_observation_port_is_append_only():
    """
    Port must not overwrite or deduplicate events.

    Same input twice → two stored events.
    """

    port = DummyObservationPort()

    e1 = ObservationEvent(
        user_id="user-1",
        source_type="normative",
        payload={"signal_type": "DISAGREE"},
        created_at=datetime.utcnow(),
    )

    e2 = ObservationEvent(
        user_id="user-1",
        source_type="normative",
        payload={"signal_type": "DISAGREE"},
        created_at=datetime.utcnow(),
    )

    port.record(e1)
    port.record(e2)

    assert len(port.events) == 2
    assert port.events[0] is not port.events[1]


def test_observation_port_has_minimal_contract():
    """
    Kernel contract: ObservationPort exposes only record().
    No inference, no list(), no delete(), no mutation.
    """

    assert hasattr(ObservationPort, "record")

    forbidden = ["delete", "update", "aggregate", "infer", "list"]

    for name in forbidden:
        assert not hasattr(ObservationPort, name)


def test_observation_writer_port_exists():
    from kernel.ports.observation_port import ObservationWriterPort

    assert ObservationWriterPort is not None


def test_observation_port_alias_exists():
    from kernel.ports.observation_port import ObservationPort
    assert ObservationPort is not None
