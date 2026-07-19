"""
Helpers compartilhados para cálculos de confluência.

Funções puras usadas por ConfluenceEngine e ConfluenceScoreEngine
para evitar duplicação de lógica idêntica (detecção de conflito,
clamping, direção dominante).
"""

from mercury_ai.models.direction import AnalysisDirection


def has_conflict(bullish: float, bearish: float) -> bool:
    """Detecta conflito: ambos os lados têm contribuição positiva."""
    return bullish > 0.0 and bearish > 0.0


def clamp_score(value: float, floor: float = 0.0, ceiling: float = 100.0) -> float:
    """Clampa um valor entre floor e ceiling (inclusive)."""
    return max(floor, min(value, ceiling))


def dominant_direction(
    bullish: float,
    bearish: float,
    threshold: float = 1.2,
) -> AnalysisDirection:
    """
    Determina a direção dominante com threshold relativo.

    - Se bullish > bearish * threshold → BUY
    - Se bearish > bullish * threshold → SELL
    - Caso contrário → NEUTRAL
    """
    if bullish > bearish * threshold:
        return AnalysisDirection.BUY
    elif bearish > bullish * threshold:
        return AnalysisDirection.SELL
    else:
        return AnalysisDirection.NEUTRAL