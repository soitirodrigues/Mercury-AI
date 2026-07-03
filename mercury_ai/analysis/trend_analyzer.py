from dataclasses import dataclass

from mercury_ai.models.market_data import MarketData


@dataclass
class TrendAnalysis:
    trend: str
    confidence: int
    explanation: list[str]


class TrendAnalyzer:

    def analyze(self, market: MarketData) -> TrendAnalysis:

        score = 0
        reasons = []

        # Alinhamento das médias
        if market.ema9 > market.ema21 > market.ema50:
            score += 40
            reasons.append("EMA 9 > EMA 21 > EMA 50")

        elif market.ema9 < market.ema21 < market.ema50:
            score -= 40
            reasons.append("EMA 9 < EMA 21 < EMA 50")

        # ADX
        if market.adx >= 30:
            score += 20 if score > 0 else -20
            reasons.append("ADX acima de 30")

        elif market.adx >= 20:
            score += 10 if score > 0 else -10
            reasons.append("ADX entre 20 e 30")

        else:
            reasons.append("Mercado lateral")

        # Preço
        if market.close > market.ema9:
            score += 10
            reasons.append("Preço acima da EMA9")

        else:
            score -= 10
            reasons.append("Preço abaixo da EMA9")

        # Classificação
        if score >= 50:
            trend = "STRONG_UP"

        elif score >= 20:
            trend = "UP"

        elif score <= -50:
            trend = "STRONG_DOWN"

        elif score <= -20:
            trend = "DOWN"

        else:
            trend = "SIDEWAYS"

        confidence = min(abs(score), 100)

        return TrendAnalysis(
            trend=trend,
            confidence=confidence,
            explanation=reasons
        )