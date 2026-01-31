# tests/test_observation_long_builder_kernel.py

from kernel.journals.observation_long import ObservationLongBuilder


def test_builder_creates_valid_event():
    builder = ObservationLongBuilder(
        user_id="u1",
        source_type="governance",
        payload={"key": "value"},
    )

    event = builder.build()

    assert event.user_id == "u1"
    assert event.source_type == "governance"
    assert event.payload["key"] == "value"
    assert event.observed_at is not None
