import threading
from datetime import datetime, timezone
from typing import Optional


class DeterministicClock:
    """Relógio determinístico thread-safe para análise reproduzível.

    Cada thread possui seu próprio estado de tempo via threading.local(),
    garantindo isolamento completo entre threads concurrentes.
    """

    _local = threading.local()

    @classmethod
    def _get_current_time(cls) -> Optional[datetime]:
        """Obtém o _current_time específico desta thread."""
        return getattr(cls._local, '_current_time', None)

    @classmethod
    def _set_current_time(cls, dt: datetime) -> None:
        """Define o _current_time específico desta thread."""
        cls._local._current_time = dt

    @classmethod
    def set_time(cls, dt: datetime) -> None:
        """Define o tempo determinístico para a thread corrente.

        A thread corrente passa a observar este tempo isoladamente
        das demais threads, até que seja chamado reset() ou restore().
        """
        cls._set_current_time(dt)

    @classmethod
    def utcnow(cls) -> datetime:
        """Retorna o tempo da thread corrente, ou o relógio real se não houver tempo definidio.

        Se a thread corrente tiver um _current_time definido (via set_time),
        retorna-o. Caso contrário, retorna o relógio real UTC.
        """
        current = cls._get_current_time()
        if current is not None:
            return current
        return datetime.now(timezone.utc).replace(tzinfo=None)

    @classmethod
    def reset(cls) -> None:
        """Limpa o tempo determinístico da thread corrente, voltando ao relógio real."""
        cls._local._current_time = None

    @classmethod
    def snapshot(cls) -> Optional[datetime]:
        """Captura o estado atual do relógio da thread corrente (None = relógio real).

        Usado para isolar o relógio durante operações determinísticas
        (ex.: replay histórico) e restaurar o estado anterior ao final,
        evitando contaminação temporal pós-replay.
        """
        return cls._get_current_time()

    @classmethod
    def restore(cls, state: Optional[datetime]) -> None:
        """Restaura um estado previamente capturado por snapshot() da thread corrente.

        Se state for None, o relógio volta ao comportamento normal (real).
        """
        cls._set_current_time(state)
