"""replay_isolation — helpers de isolamento temporal para S7.1.

Documenta e encapsula a dependência crítica do isolamento via
threading.local do DeterministicClock.

NENHUMA semântica de DeterministicClock é alterada aqui; apenas
helpers de conveniência e um context manager para uso em replay
e em testes paralelos.

Zona B — POSSÍVEL IMPACTO mas sem mudança de semântica.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Generator

from mercury_ai.utils.deterministic_clock import DeterministicClock


def is_isolation_active() -> bool:
    """Retorna True se a thread corrente está com clock congelado."""
    return DeterministicClock.is_frozen() if hasattr(DeterministicClock, "is_frozen") else (
        DeterministicClock.snapshot() is not None
    )


@contextmanager
def isolated_clock(frozen_time: Optional[datetime] = None) -> Generator[None, None, None]:
    """Context manager que isola o DeterministicClock da thread corrente.

    Captura snapshot na entrada e restaura em finally, garantindo
    NORMAL→REPLAY→NORMAL sem contaminação mesmo sob exceção.

    Args:
        frozen_time: Se fornecido, congela o clock neste instante durante
            o contexto; se None, apenas isola mas mantém wall-clock.

    Yields:
        None
    """
    state = DeterministicClock.snapshot()
    if frozen_time is not None:
        DeterministicClock.set_time(frozen_time)
    try:
        yield
    finally:
        DeterministicClock.restore(state)


@contextmanager
def frozen_clock_at(candle_time: datetime) -> Generator[None, None, None]:
    """Atalho explícito para congelar no candle_time e restaurar."""
    state = DeterministicClock.snapshot()
    DeterministicClock.set_time(candle_time)
    try:
        yield
    finally:
        DeterministicClock.restore(state)
