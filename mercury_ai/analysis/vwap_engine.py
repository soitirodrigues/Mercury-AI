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
        vol_cumsum = df['Volume'].cumsum()
        # Guard against division by zero when all volumes are 0
        vol_cumsum_safe = vol_cumsum.replace(0, 1e-10)
        vwap = (typical_price * df['Volume']).cumsum() / vol_cumsum_safe

        vwap_val = vwap.iloc[-1]
        curr_price = df['Close'].iloc[-1]
        # Guard against division by zero if vwap_val is 0
        distance = (curr_price - vwap_val) / vwap_val if vwap_val != 0 else 0.0

        bias = "NEUTRAL"
        if curr_price > vwap_val:
            bias = "BULLISH"
        elif curr_price < vwap_val:
            bias = "BEARISH"

        # Acceptance: price within 0.5% of VWAP (standard SMC threshold)
        is_accepted = abs(distance) < 0.005
        # Rejection: price more than 2% away from VWAP
        is_rejected = abs(distance) > 0.02
        # Mean reversion: price was far and is coming back toward VWAP
        is_mean_reversion = False
        if len(vwap) >= 3:
            prev_distance = (df['Close'].iloc[-2] - vwap.iloc[-2]) / vwap.iloc[-2] if vwap.iloc[-2] != 0 else 0.0
            if abs(prev_distance) > abs(distance) and abs(prev_distance) > 0.01:
                is_mean_reversion = True

        evidences = []
        if is_accepted:
            evidences.append(Evidence("VWAPEngine", "VWAP_Acceptance", "NEUTRAL", 80.0, 70.0,
                                     "Price near VWAP — institutional acceptance zone", 50.0))
        if is_rejected:
            direction = "BEARISH" if curr_price > vwap_val else "BULLISH"
            evidences.append(Evidence("VWAPEngine", "VWAP_Rejection", direction, 75.0, 65.0,
                                     f"Price {abs(distance)*100:.1f}% from VWAP — rejection zone", 45.0))
        if bias != "NEUTRAL" and not is_accepted:
            evidences.append(Evidence("VWAPEngine", "VWAP_Bias", bias, 60.0, 60.0,
                                     f"Institutional bias {bias} — price {'above' if bias == 'BULLISH' else 'below'} VWAP", 40.0))
        if is_mean_reversion:
            evidences.append(Evidence("VWAPEngine", "Mean_Reversion", bias, 65.0, 60.0,
                                     "Price reverting toward VWAP — mean reversion signal", 35.0))

        # Adaptive confidence based on data quality and distance
        confidence = 0.75
        if len(df) >= 20:
            confidence = 0.85
        elif len(df) < 5:
            confidence = 0.50

        # Quality: higher when price is near VWAP (clearer signal)
        quality = 0.90 if is_accepted else (0.60 if is_rejected else 0.75)

        return VWAPAnalysis(
            vwap=float(vwap_val),
            distance_to_vwap=float(distance),
            is_accepted=is_accepted,
            is_rejected=is_rejected,
            is_mean_reversion=is_mean_reversion,
            institutional_bias=bias,
            confidence=confidence,
            quality=quality,
            evidences=tuple(evidences)
        )
