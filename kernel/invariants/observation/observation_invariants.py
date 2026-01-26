# kernel/invariants/observation/observation_invariants.py

from kernel.journals.observation.observation_event import ObservationEvent


class ObservationInvariants:
    """
    Kernel-level invariants for observation events.

    Observation is append-only factual truth.
    """

    @staticmethod
    def is_valid(event: ObservationEvent) -> bool:
        return (
            bool(event.user_id)
            and bool(event.source_type)
            and event.created_at is not None
        )

    @staticmethod
    def assert_valid(event: ObservationEvent) -> None:
        if not ObservationInvariants.is_valid(event):
            raise ValueError(
                f"Invalid ObservationEvent: {event}"
            )
