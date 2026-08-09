import pandas as pd
import numpy as np
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
        # Fix: prevent division by zero in RS calculation
        loss = loss.replace(0, 1e-10)
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = rsi.iloc[-1]

        # Fix: handle NaN rsi_val from insufficient rolling data
        if pd.isna(rsi_val):
            return MomentumAnalysis()

        roc = ((df['Close'].iloc[-1] - df['Close'].iloc[-10]) / df['Close'].iloc[-10]) * 100

        # Fix: add basic MACD calculation (fields exist in MomentumAnalysis model)
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        macd_signal = macd.ewm(span=9, adjust=False).mean()
        macd_val = float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else 0.0
        macd_signal_val = float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else 0.0

        evidences = []
        is_exhaustion = False
        if rsi_val > 70:
            is_exhaustion = True
            evidences.append(Evidence("MomentumEngine", "Exhaustion", "BEARISH", 90.0, 80.0, "RSI Overbought", 50.0))
        elif rsi_val < 30:
            is_exhaustion = True
            evidences.append(Evidence("MomentumEngine", "Exhaustion", "BULLISH", 90.0, 80.0, "RSI Oversold", 50.0))

        # Fix: detect divergence — price makes higher high but MACD makes lower high
        if len(df) >= 40:
            price_recent_high = df['High'].iloc[-20:].max()
            price_prev_high = df['High'].iloc[-40:-20].max()
            macd_recent_high = macd.iloc[-20:].max()
            macd_prev_high = macd.iloc[-40:-20].max()
            if price_recent_high > price_prev_high and macd_recent_high < macd_prev_high:
                evidences.append(Evidence("MomentumEngine", "Divergence", "BEARISH", 75.0, 70.0, "Bearish divergence: price HH but MACD LH", 45.0))

        return MomentumAnalysis(
            rsi=float(rsi_val),
            macd=macd_val,
            macd_signal=macd_signal_val,
            roc=float(roc),
            is_exhaustion=is_exhaustion,
            is_divergence=len(evidences) > 0 and any(e.evidence_name == "Divergence" for e in evidences),
            confidence=0.7,
            quality=0.7,
            evidences=tuple(evidences)
        )
