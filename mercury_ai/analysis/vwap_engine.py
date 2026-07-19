import pandas as pd
from typing import Optional
from mercury_ai.models.vwap_analysis import VWAPAnalysis
from mercury_ai.models.evidence import Evidence
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

class VWAPEngine:
    def __init__(self, executor: PipelineExecutor, profiler: Optional[PipelineProfiler] = None):
        self.executor = executor
        self.profiler = profiler

    def analyze(self, df: pd.DataFrame) -> VWAPAnalysis:
        return self.executor.execute("AnalyzeVWAP", self._analyze_logic, VWAPAnalysis, df)

    def _analyze_logic(self, df: pd.DataFrame) -> VWAPAnalysis:
        if len(df) < 1:
            return VWAPAnalysis()

        # Simplified VWAP: sum(price * volume) / sum(volume)
        # Assuming OHLCV dataframe
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        vwap = (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        vwap_val = vwap.iloc[-1]
        curr_price = df['Close'].iloc[-1]
        distance = (curr_price - vwap_val) / vwap_val
        
        bias = "NEUTRAL"
        if curr_price > vwap_val:
            bias = "BULLISH"
        elif curr_price < vwap_val:
            bias = "BEARISH"
            
        evidences = []
        if abs(distance) < 0.001:
            evidences.append(Evidence("VWAPEngine", "Acceptance", "NEUTRAL", 80.0, 70.0, "Price near VWAP", 50.0))
            
        return VWAPAnalysis(
            vwap=float(vwap_val),
            distance_to_vwap=float(distance),
            institutional_bias=bias,
            confidence=0.75,
            quality=0.75,
            evidences=tuple(evidences)
        )
