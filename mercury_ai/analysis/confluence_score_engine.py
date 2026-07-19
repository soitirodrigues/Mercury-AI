from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.confluence_score import ConfluenceScore
from mercury_ai.analysis.evidence_query import EvidenceQuery

# Pesos Centralizados (Migrados da ConfluenceEngine)
WEIGHTS = {
    "market_structure": 25,
    "trend": 20,
    "liquidity": 15,
    "support_resistance": 15,
    "volatility": 10,
    "market_condition": 10,
    "candlestick": 5,
}

class ConfluenceScoreEngine:
    """
    Motor central para cálculos determinísticos de confluência, score, e alinhamento.
    """

    def calculate(self, context: MarketContext) -> ConfluenceScore:
        bullish = 0.0
        bearish = 0.0
        conflicts = 0

        # Trend contribuição
        is_uptrend = EvidenceQuery.is_uptrend(context.trend)
        is_downtrend = EvidenceQuery.is_downtrend(context.trend)
        
        if is_uptrend:
            bullish += WEIGHTS["trend"]
        elif is_downtrend:
            bearish += WEIGHTS["trend"]

        # Smart Money contribuição
        if context.smart_money.structure.trend == "BULLISH":
            bullish += WEIGHTS["smart_money"]
        elif context.smart_money.structure.trend == "BEARISH":
            bearish += WEIGHTS["smart_money"]


        # Detecção de conflitos
        if bullish > 0 and bearish > 0:
            conflicts = 1

        # Cálculos determinísticos
        total_weight = sum(WEIGHTS.values())
        confluence_score = (max(bullish, bearish) / total_weight) * 100
        conflict_penalty = (conflicts * 20.0)
        clarity_score = min(max(confluence_score - conflict_penalty, 0), 100)
        
        return ConfluenceScore(
            confluence_score=confluence_score,
            clarity_score=clarity_score,
            bullish_score=bullish,
            bearish_score=bearish,
            conflict_penalty=conflict_penalty
        )
