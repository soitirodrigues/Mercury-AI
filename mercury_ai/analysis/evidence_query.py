from typing import List
from mercury_ai.models.evidence import Evidence

class EvidenceQuery:
    """
    Camada institucional de consulta de evidências.
    Desacopla as engines da estrutura interna das evidências.
    """

    @staticmethod
    def get_trend_direction(evidences: List[Evidence]) -> str:
        """
        Consulta a direção da tendência baseada nas evidências disponíveis.
        Retorna 'BULLISH', 'BEARISH' ou 'NEUTRAL'.
        """
        # Regra de negócio preservada: Baseada no alinhamento das médias
        for e in evidences:
            if e.engine_name in ("Trend", "TrendEngine") and e.evidence_name == "EMA Alignment":
                return e.direction
        return "NEUTRAL"

    @staticmethod
    def is_uptrend(evidences: List[Evidence]) -> bool:
        return EvidenceQuery.get_trend_direction(evidences) == "BULLISH"

    @staticmethod
    def is_downtrend(evidences: List[Evidence]) -> bool:
        return EvidenceQuery.get_trend_direction(evidences) == "BEARISH"

    @staticmethod
    def has_strong_trend(evidences: List[Evidence]) -> bool:
        """
        Determina se a tendência é considerada forte.
        Regra: Alguma evidência de tendência possui força (strength) >= 80.
        """
        for e in evidences:
            if e.engine_name in ("Trend", "TrendEngine") and e.strength >= 80:
                return True
        return False
