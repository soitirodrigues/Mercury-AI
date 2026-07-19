from datetime import datetime, timezone

class DeterministicClock:
    _current_time = None

    @classmethod
    def set_time(cls, dt: datetime):
        cls._current_time = dt

    @classmethod
    def utcnow(cls) -> datetime:
        if cls._current_time:
            return cls._current_time
        return datetime.now(timezone.utc).replace(tzinfo=None)
