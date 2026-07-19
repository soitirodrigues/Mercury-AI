import pandas as pd
from typing import Optional

from mercury_ai.models.fair_value_gap_analysis import FairValueGapAnalysis
from mercury_ai.models.evidence import Evidence
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler


class FairValueGapEngine:

    def __init__(
        self,
        executor: PipelineExecutor,
        profiler: Optional[PipelineProfiler] = None
    ):
        self.executor = executor
        self.profiler = profiler


    def analyze(
        self,
        df: pd.DataFrame
    ) -> FairValueGapAnalysis:

        return self.executor.execute(
            "AnalyzeFVG",
            self._analyze_logic,
            FairValueGapAnalysis,
            df
        )


    def _analyze_logic(
        self,
        df: pd.DataFrame
    ) -> FairValueGapAnalysis:


        if df is None or len(df) < 3:
            return FairValueGapAnalysis()


        # Garantir índice limpo
        df = df.copy()

        df = df.reset_index(drop=True)


        # Garantir números
        for col in [
            "Open",
            "High",
            "Low",
            "Close"
        ]:

            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )


        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]


        high_1 = float(c1["High"])
        low_1 = float(c1["Low"])

        high_3 = float(c3["High"])
        low_3 = float(c3["Low"])

        high_2 = float(c2["High"])
        low_2 = float(c2["Low"])



        # FVG institucional

        bullish_fvg = low_3 > high_1

        bearish_fvg = high_3 < low_1



        filled = False


        if bullish_fvg:

            filled = low_3 <= high_2


        elif bearish_fvg:

            filled = high_3 >= low_2



        evidences = []


        if bullish_fvg or bearish_fvg:

            direction = (
                "BULLISH"
                if bullish_fvg
                else "BEARISH"
            )


            evidences.append(
                Evidence(
                    "FairValueGapEngine",
                    "FVG",
                    direction,
                    80.0,
                    70.0,
                    f"{direction} Fair Value Gap detectado",
                    50.0
                )
            )



        return FairValueGapAnalysis(

            is_bullish_fvg=bool(bullish_fvg),

            is_bearish_fvg=bool(bearish_fvg),

            is_filled=bool(filled),

            is_open=not filled,

            fvg_quality=0.7,

            confidence=0.7,

            quality=0.7,

            evidences=tuple(evidences)

        )