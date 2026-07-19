import time
import pandas as pd
from typing import List, Tuple, Optional
from mercury_ai.core.base_engine import BaseEngine, EngineResult
from mercury_ai.models.candlestick_analysis import CandlestickAnalysis
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_condition import MarketCondition
from mercury_ai.models.evidence import Evidence
from mercury_ai.analysis.evidence_query import EvidenceQuery

class CandlestickEngine(BaseEngine):
    """
    Analisa OHLC para identificar padrões profissionais de Price Action.
    """
    DOJI_BODY_LIMIT = 0.05
    HAMMER_WICK_RATIO = 2.0  
    STRONG_BODY_LIMIT = 0.60
    REJECTION_LIMIT = 0.60
    CONTINUATION_LIMIT = 0.70

    def analyze(self, df: pd.DataFrame, market: MarketData, trend_evidences: List[Evidence], mc: MarketCondition) -> Tuple[CandlestickAnalysis, EngineResult]:
        start_time = time.perf_counter()
        
        if len(df) < 2:
            exec_time = time.perf_counter() - start_time
            return CandlestickAnalysis(pattern="NONE", explanation="Dados insuficientes."), EngineResult(0.0, 0.0, (), ("Dados insuficientes",), exec_time)

        current = df.iloc[-1]
        previous = df.iloc[-2]
        evidences: List[str] = []

        # Métricas fundamentais
        body = abs(current['Close'] - current['Open'])
        range_total = current['High'] - current['Low']
        upper_wick = current['High'] - max(current['Open'], current['Close'])
        lower_wick = min(current['Open'], current['Close']) - current['Low']
        
        # Percentuais
        body_pct = (body / range_total) if range_total > 0 else 0
        upper_wick_pct = (upper_wick / range_total) if range_total > 0 else 0
        lower_wick_pct = (lower_wick / range_total) if range_total > 0 else 0
        
        # Padrões
        pattern = self._detect_pattern(current, body_pct, upper_wick_pct, lower_wick_pct, evidences)
        
        # Contexto
        context, context_score = self._detect_context(current, market, trend_evidences, mc, evidences)
        
        # Engulfing
        engulfing = self._detect_engulfing(current, previous)
        if engulfing:
            evidences.append(f"Padrão detectado: {engulfing}")
            
        # Rejeição e Continuação
        rejection = self._detect_rejection(upper_wick_pct, lower_wick_pct, evidences)
        continuation = self._detect_continuation(body_pct, upper_wick_pct, lower_wick_pct, evidences)
        
        explanation = "\n".join([f"- {e}" for e in evidences])

        # Final metrics
        exec_time = time.perf_counter() - start_time
        engine_result = EngineResult(
            score=context_score,
            confidence=85.0, # Simplified
            evidences=tuple(evidences),
            warnings=(),
            execution_time=exec_time
        )
        
        return CandlestickAnalysis(
            pattern=pattern,
            body_strength=body_pct * 100,
            upper_wick=upper_wick_pct * 100,
            lower_wick=lower_wick_pct * 100,
            rejection=rejection,
            engulfing=(engulfing is not None),
            continuation=continuation,
            explanation=explanation,
            context=context,
            context_score=context_score,
            evidences=evidences
        ), engine_result

    def _detect_context(self, current, market, trend_evidences, mc, evidences: List[str]) -> tuple[str, float]:
        is_uptrend = EvidenceQuery.is_uptrend(trend_evidences)
        is_downtrend = EvidenceQuery.is_downtrend(trend_evidences)
        
        if (is_uptrend and current['Close'] > market.ema9) or (is_downtrend and current['Close'] < market.ema9):
            evidences.append("Vela alinhada com a tendência principal.")
            return "TREND_CONTINUATION", 80.0
            
        if (is_uptrend and current['Close'] < market.ema21) or (is_downtrend and current['Close'] > market.ema21):
            evidences.append("Vela indicando possível pullback.")
            return "PULLBACK", 60.0
            
        return "UNCERTAIN", 30.0

    def _detect_pattern(self, c, body_pct, upper_pct, lower_pct, evidences) -> str:
        if body_pct < self.DOJI_BODY_LIMIT:
            evidences.append("Padrão: DOJI.")
            return "DOJI"
        
        if lower_pct > upper_pct * self.HAMMER_WICK_RATIO and body_pct < 0.3 and c['Close'] > c['Open']:
            evidences.append("Padrão: HAMMER.")
            return "HAMMER"
        
        if upper_pct > lower_pct * self.HAMMER_WICK_RATIO and body_pct < 0.3 and c['Close'] < c['Open']:
            evidences.append("Padrão: SHOOTING_STAR.")
            return "SHOOTING_STAR"
            
        if body_pct > self.STRONG_BODY_LIMIT:
            return "STRONG_BULL" if c['Close'] > c['Open'] else "STRONG_BEAR"
        
        evidences.append(f"Padrão: NONE.")
        return "NONE"

    def _detect_engulfing(self, c, p) -> Optional[str]:
        if p['Close'] < p['Open'] and c['Close'] > c['Open'] and c['Close'] > p['Open'] and c['Open'] < p['Close']:
            return "BULLISH_ENGULFING"
        if p['Close'] > p['Open'] and c['Close'] < c['Open'] and c['Close'] < p['Open'] and c['Open'] > p['Close']:
            return "BEARISH_ENGULFING"
        return None

    def _detect_rejection(self, upper, lower, evidences) -> bool:
        rejection = (upper > self.REJECTION_LIMIT) or (lower > self.REJECTION_LIMIT)
        if rejection:
            evidences.append("Alta rejeição detectada nos pavios.")
        return rejection

    def _detect_continuation(self, body, upper, lower, evidences) -> bool:
        is_strong = body > self.CONTINUATION_LIMIT and (upper < 0.2 and lower < 0.2)
        if is_strong:
            evidences.append("Alta probabilidade de continuidade.")
        return is_strong
