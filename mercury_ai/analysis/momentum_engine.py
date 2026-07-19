import pandas as pd
from typing import Optional
from mercury_ai.models.momentum_analysis import MomentumAnalysis
from mercury_ai.models.evidence import Evidence
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

class MomentumEngine:
    def __init__(self, executor: PipelineExecutor, profiler: Optional[PipelineProfiler] = None):
        self.executor = executor
        self.profiler = profiler

    def analyze(self, df: pd.DataFrame) -> MomentumAnalysis:
        return self.executor.execute("AnalyzeMomentum", self._analyze_logic, MomentumAnalysis, df)

    def _analyze_logic(self, df: pd.DataFrame) -> MomentumAnalysis:
        if len(df) < 30:
            return MomentumAnalysis()

        # Simplified Indicators
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = rsi.iloc[-1]
        
        roc = ((df['Close'].iloc[-1] - df['Close'].iloc[-10]) / df['Close'].iloc[-10]) * 100
        
        evidences = []
        if rsi_val > 70:
            evidences.append(Evidence("MomentumEngine", "Exhaustion", "BEARISH", 90.0, 80.0, "RSI Overbought", 50.0))
        elif rsi_val < 30:
            evidences.append(Evidence("MomentumEngine", "Exhaustion", "BULLISH", 90.0, 80.0, "RSI Oversold", 50.0))
            
        return MomentumAnalysis(
            rsi=float(rsi_val),
            roc=float(roc),
            confidence=0.7,
            quality=0.7,
            evidences=tuple(evidences)
        )
