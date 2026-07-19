import pandas as pd
from typing import Optional
from mercury_ai.models.volume_analysis import VolumeAnalysis
from mercury_ai.models.evidence import Evidence
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

class VolumeEngine:
    def __init__(self, executor: PipelineExecutor, profiler: Optional[PipelineProfiler] = None):
        self.executor = executor
        self.profiler = profiler

    def analyze(self, df: pd.DataFrame) -> VolumeAnalysis:
        return self.executor.execute("AnalyzeVolume", self._analyze_logic, VolumeAnalysis, df)

    def _analyze_logic(self, df: pd.DataFrame) -> VolumeAnalysis:
        if len(df) < 20:
            return VolumeAnalysis()

        vol_sma20 = df['Volume'].rolling(window=20).mean()
        curr_vol = df['Volume'].iloc[-1]
        prev_vol = df['Volume'].iloc[-2]
        sma20 = vol_sma20.iloc[-1]
        
        rel_vol = curr_vol / sma20 if sma20 > 0 else 1.0
        is_spike = rel_vol > 2.0
        
        trend = "NEUTRAL"
        if curr_vol > prev_vol:
            trend = "INCREASING"
        elif curr_vol < prev_vol:
            trend = "DECREASING"
            
        evidences = []
        if is_spike:
            evidences.append(Evidence("VolumeEngine", "Spike", "NEUTRAL", 90.0, 85.0, "Volume spike detected", 60.0))
            
        return VolumeAnalysis(
            relative_volume=float(rel_vol),
            is_volume_spike=bool(is_spike),
            volume_trend=trend,
            confidence=0.75,
            quality=0.75,
            evidences=tuple(evidences)
        )
