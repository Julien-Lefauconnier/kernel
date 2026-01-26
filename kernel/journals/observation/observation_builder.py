# kernel/journals/observation/observation_builder.py

from datetime import datetime

from kernel.journals.observation.observation_event import ObservationEvent


class ObservationBuilder:
    """
    Kernel invariant builder.

    Converts domain signals into append-only ObservationEvents.

    SINGLE SOURCE OF TRUTH.
    """

    @staticmethod
    def from_normative_signal(signal) -> ObservationEvent:
        return ObservationEvent(
            user_id=signal.user_id,
            source_type="normative",
            payload={
                "bundle_id": signal.bundle_id,
                "signal_type": signal.signal_type,
                "message": signal.message,
                "source": signal.source,
            },
            created_at=signal.created_at or datetime.utcnow(),
        )
