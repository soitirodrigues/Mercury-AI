from typing import Optional
import pandas as pd
from mercury_ai.models.price_action_analysis import PriceActionAnalysis
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

class PriceActionEngine:
    def __init__(self, executor: PipelineExecutor, profiler: Optional[PipelineProfiler] = None):
        self.executor = executor
        self.profiler = profiler

    def analyze(self, df: pd.DataFrame) -> PriceActionAnalysis:
        """
        Analyzes price action patterns and returns PriceActionAnalysis.
        """
        return self.executor.execute("AnalyzePriceAction", self._analyze_logic, PriceActionAnalysis, df)

    def _analyze_logic(self, df: pd.DataFrame) -> PriceActionAnalysis:
        # Simplified pattern detection
        # Need at least 2 candles for most patterns
        if len(df) < 2:
            return PriceActionAnalysis()

        curr = df.iloc[-1]
        prev = df.iloc[-2]

        # Strong/Weak
        body_size = abs(curr['Close'] - curr['Open'])
        total_size = curr['High'] - curr['Low']
        is_strong_candle = body_size / total_size > 0.7 if total_size > 0 else False
        is_weak_candle = body_size / total_size < 0.3 if total_size > 0 else False
        
        # Pin Bar
        is_pin_bar = (body_size / total_size < 0.2) and \
                     ((curr['High'] - max(curr['Open'], curr['Close'])) / total_size > 0.5 or \
                      (min(curr['Open'], curr['Close']) - curr['Low']) / total_size > 0.5)

        # Inside/Outside Bar
        is_inside_bar = (curr['High'] < prev['High']) and (curr['Low'] > prev['Low'])
        is_outside_bar = (curr['High'] > prev['High']) and (curr['Low'] < prev['Low'])

        prev_is_bearish = prev['Close'] < prev['Open']
        curr_is_bullish = curr['Close'] > curr['Open']
        is_bullish_engulfing = prev_is_bearish and curr_is_bullish and (curr['Close'] >= prev['Open']) and (curr['Open'] <= prev['Close'])
        
        prev_is_bullish = prev['Close'] > prev['Open']
        curr_is_bearish = curr['Close'] < curr['Open']
        is_bearish_engulfing = prev_is_bullish and curr_is_bearish and (curr['Close'] <= prev['Open']) and (curr['Open'] >= prev['Close'])
        
        is_engulfing = is_bullish_engulfing or is_bearish_engulfing
        
        return PriceActionAnalysis(
            is_strong_candle=bool(is_strong_candle),
            is_weak_candle=bool(is_weak_candle),
            is_pin_bar=bool(is_pin_bar),
            is_inside_bar=bool(is_inside_bar),
            is_outside_bar=bool(is_outside_bar),
            is_engulfing=bool(is_engulfing),
            confidence=0.5,
            quality=0.5
        )
