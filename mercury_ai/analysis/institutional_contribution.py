from dataclasses import dataclass


@dataclass(frozen=True)
class InstitutionalContribution:
    """
    Contribuição individual de uma engine para a decisão institucional.

    Cada instância representa o peso e a influência de uma engine
    específica no cálculo de confluência que levou à decisão final.

    Attributes:
        engine_name: Nome da engine (ex: 'trend', 'market_structure')
        weight: Peso institucional canônico da engine (0-20)
        raw_score: Score bruto da evidência (0-100)
        weighted_score: Score ponderado = (raw_score/100) * weight
        direction: Direção da evidência (BULLISH, BEARISH, NEUTRAL)
        confidence: Confiança da evidência (0-100)
        explanation: Descrição textual da contribuição
    """
    engine_name: str
    weight: float
    raw_score: float
    weighted_score: float
    direction: str
    confidence: float
    explanation: str