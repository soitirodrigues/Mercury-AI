from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_data import MarketData
from typing import List

class TrendAnalyzer:
    """
    Analisa a tendência do mercado de forma granular.
    """

    def analyze(self, market: MarketData) -> List[Evidence]:
        evidences = []

        # EMA Alignment
        if market.ema9 > market.ema21 > market.ema50:
            evidences.append(Evidence("Trend", "EMA Alignment", "BULLISH", 90.0, 90.0, "EMA 9 > EMA 21 > EMA 50", 30.0))
        elif market.ema9 < market.ema21 < market.ema50:
            evidences.append(Evidence("Trend", "EMA Alignment", "BEARISH", 90.0, 90.0, "EMA 9 < EMA 21 < EMA 50", 30.0))

        # ADX Strength
        if market.adx >= 30:
            evidences.append(Evidence("Trend", "ADX Strength", "NEUTRAL", float(market.adx), 80.0, f"ADX: {market.adx}", 20.0))

        # Price Position
        if market.close > market.ema9:
            evidences.append(Evidence("Trend", "Price vs EMA9", "BULLISH", 80.0, 80.0, "Preço acima da EMA9", 10.0))
        else:
            evidences.append(Evidence("Trend", "Price vs EMA9", "BEARISH", 80.0, 80.0, "Preço abaixo da EMA9", 10.0))

        return evidences

