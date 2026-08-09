from dataclasses import dataclass, field
from typing import Tuple
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME


@dataclass(frozen=True)
class Signal:
    """
    Representa a decisão final da Mercury AI.
    """

    asset: str

    action: str

    confidence: float

    score: float

    entry: float | None = None

    stop_loss: float | None = None

    take_profit: float | None = None

    timeframe: str = DEFAULT_TIMEFRAME

    strategy: str = ""

    evidences: Tuple[str, ...] = field(default_factory=tuple)

    explanation: str = ""