from typing import List
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_condition import MarketCondition

# Constantes de Limites (Magic Numbers eliminados)
ADX_THRESHOLD_STRONG = 25.0
ADX_THRESHOLD_MODERATE = 15.0

EMA_DISTANCE_GOOD = 0.005  # 0.5%
EMA_DISTANCE_TIGHT = 0.001  # 0.1%

class MarketConditionEngine:
    """
    Responsável pela análise técnica do contexto de mercado.
    Entrada: MarketData | Saída: MarketCondition
    """

    def analyze(self, market: MarketData) -> MarketCondition:
        evidences: List[str] = []
        
        trend = self._detect_trend(market)
        alignment_score = self._measure_ema_alignment(market)
        distance_score = self._measure_ema_distance(market, evidences)
        price_pos_score = self._analyze_price_position(market, trend, evidences)
        adx_score, adx_state = self._analyze_adx(market, evidences)
        
        strength = self._calculate_trend_strength(
            alignment_score, distance_score, price_pos_score, adx_score
        )
        
        state = self._detect_market_state(strength, adx_score)
        
        self._analyze_rsi(market, evidences)
        
        explanation = self._build_explanation(trend, state, evidences)

        return MarketCondition(
            trend=trend,
            trend_strength=strength,
            market_state=state,
            explanation=explanation
        )

    def _detect_trend(self, market: MarketData) -> str:
        """Determina a tendência baseada no alinhamento das médias."""
        if market.ema9 > market.ema21 > market.ema50:
            return "UPTREND"
        elif market.ema9 < market.ema21 < market.ema50:
            return "DOWNTREND"
        return "SIDEWAYS"

    def _measure_ema_alignment(self, market: MarketData) -> float:
        """Retorna score 100 se alinhado, 0 caso contrário."""
        if (market.ema9 > market.ema21 > market.ema50) or (market.ema9 < market.ema21 < market.ema50):
            return 100.0
        return 0.0

    def _measure_ema_distance(self, market: MarketData, evidences: List[str]) -> float:
        """Avalia espaçamento entre médias."""
        if market.ema21 == 0 or market.ema50 == 0:
            return 0.0
            
        diff1 = abs(market.ema9 - market.ema21) / market.ema21
        diff2 = abs(market.ema21 - market.ema50) / market.ema50
        avg_diff = (diff1 + diff2) / 2
        
        if avg_diff > EMA_DISTANCE_GOOD:
            evidences.append("EMAs bem espaçadas.")
            return 100.0
        elif avg_diff < EMA_DISTANCE_TIGHT:
            evidences.append("EMAs muito próximas (sem momentum).")
            return 20.0
        return 60.0

    def _measure_ema_slope(self, market: MarketData) -> str:
        """
        Documentação: Slope necessita histórico de candles.
        Como só recebemos snapshot, retorna FLAT.
        """
        return "FLAT"

    def _analyze_price_position(self, market: MarketData, trend: str, evidences: List[str]) -> float:
        """Analisa posição do preço em relação às médias."""
        if trend == "UPTREND":
            if market.close > market.ema9: 
                evidences.append("Preço acima da EMA9.")
                return 100.0
            return 50.0
        elif trend == "DOWNTREND":
            if market.close < market.ema9: 
                evidences.append("Preço abaixo da EMA9.")
                return 100.0
            return 50.0
        return 50.0

    def _analyze_adx(self, market: MarketData, evidences: List[str]) -> tuple[float, str]:
        """Analisa força do ADX."""
        adx = min(market.adx or 0.0, 100.0)
        if adx > ADX_THRESHOLD_STRONG:
            evidences.append(f"ADX indica tendência forte ({adx:.1f}).")
            return adx, "STRONG"
        elif adx > ADX_THRESHOLD_MODERATE:
            evidences.append(f"ADX indica tendência moderada ({adx:.1f}).")
            return adx, "MODERATE"
        evidences.append("ADX indica mercado fraco.")
        return adx, "WEAK"

    def _analyze_rsi(self, market: MarketData, evidences: List[str]) -> None:
        """Analisa RSI para contexto."""
        if market.rsi > 70:
            evidences.append("RSI sobrecomprado.")
        elif market.rsi < 30:
            evidences.append("RSI sobrevendido.")
        elif market.rsi > 50:
            evidences.append("RSI mostra força compradora.")
        else:
            evidences.append("RSI mostra força vendedora.")

    def _calculate_trend_strength(self, alignment, distance, price_pos, adx) -> float:
        return (alignment * 0.2) + (distance * 0.2) + (price_pos * 0.2) + (adx * 0.4)

    def _detect_market_state(self, strength: float, adx: float) -> str:
        if strength > 50 and adx > ADX_THRESHOLD_STRONG:
            return "TRENDING"
        elif strength > 25 or (ADX_THRESHOLD_MODERATE <= adx <= ADX_THRESHOLD_STRONG):
            return "TRANSITION"
        return "RANGING"

    def _build_explanation(self, trend, state, evidences) -> str:
        explanation = "\n".join([f"- {e}" for e in evidences])
        return f"Tendência: {trend} | Estado: {state}\nEvidências:\n{explanation}"
