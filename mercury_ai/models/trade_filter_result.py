from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class TradeFilterResult:
    """
    Resultado imutável da avaliação do InstitutionalTradeFilterEngine.

    Substitui a tupla (bool, list[str], float, str) que era retornada
    anteriormente, eliminando ambiguidade e permitindo evolução futura
    sem quebrar consumidores.
    """

    allowed: bool
    """True se o trade passou pelo filtro institucional."""

    reasons: Tuple[str, ...] = field(default_factory=tuple)
    """Razões de bloqueio ou penalidade aplicadas."""

    quality_score: float = 0.0
    """Nota de qualidade do trade (0.0 - 100.0)."""

    quality_level: str = "N/A"
    """Classificação da qualidade (A+, A, B, C, D)."""