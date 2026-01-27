# tests/test_linguistic_constraint_port_kernel.py

from typing import Protocol

from kernel.ports.linguistic_constraint_port import (
    LinguisticConstraintWriterPort,
    LinguisticConstraintReaderPort,
)


def test_writer_port_is_protocol():
    assert isinstance(LinguisticConstraintWriterPort, type(Protocol))


def test_reader_port_is_protocol():
    assert isinstance(LinguisticConstraintReaderPort, type(Protocol))
