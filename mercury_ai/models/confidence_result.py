from dataclasses import dataclass


@dataclass(frozen=True)
class ConfidenceResult:
    """
    Resultado completo do Confidence Engine.

    Todos os fatores utilizados no cálculo final permanecem
    disponíveis para auditoria institucional.
    """

    # Score bruto do engine (0-100)
    confidence_score: float

    # Score calibrado com memória institucional (0-100)
    final_confidence: float

    # Nota A/B/C/D
    confidence_grade: str

    # Alta confiança?
    is_high: bool

    # ===========================
    # Auditoria
    # ===========================

    average_quality: float

    consensus_score: float

    market_score: float

    confirmation_count: int