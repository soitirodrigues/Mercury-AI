import threading
from datetime import datetime, timezone


class DeterministicClock:
    """Relógio determinístico thread-safe para análise reproduzível.

    Usa um lock de classe para garantir que `set_time` e `utcnow` sejam
    atômicos mesmo sob concorrência de múltiplas threads.
    """

    _current_time = None
    _lock = threading.Lock()

    @classmethod
    def set_time(cls, dt: datetime) -> None:
        with cls._lock:
            cls._current_time = dt

    @classmethod
    def utcnow(cls) -> datetime:
        with cls._lock:
            if cls._current_time is not None:
                return cls._current_time
            return datetime.now(timezone.utc).replace(tzinfo=None)

    @classmethod
    def reset(cls) -> None:
        """Limpa o tempo determinístico, voltando ao relógio real."""
        with cls._lock:
            cls._current_time = None
