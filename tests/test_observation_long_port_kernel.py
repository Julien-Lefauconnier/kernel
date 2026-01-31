# tests/test_observation_long_port_kernel.py

from kernel.ports.observation_long_port import (
    ObservationLongReaderPort,
    ObservationLongWriterPort,
)


def test_observation_long_ports_exist():
    assert ObservationLongReaderPort is not None
    assert ObservationLongWriterPort is not None
