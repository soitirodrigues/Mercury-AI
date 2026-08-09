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

        close_2 = float(c2["Close"]) if "Close" in df.columns else high_2


        # FVG institucional
        # Bullish FVG: gap entre high_1 e low_3 (low_3 > high_1)
        # Bearish FVG: gap entre high_3 e low_1 (high_3 < low_1)

        bullish_fvg = low_3 > high_1

        bearish_fvg = high_3 < low_1


        filled = False
        gap_size = 0.0

        if bullish_fvg:
            # Gap está entre high_1 e low_3
            gap_size = low_3 - high_1
            # Fill: uma vela posterior penetra no gap.
            # Com apenas 3 velas, o FVG acaba de se formar e está aberto.
            # O fill só ocorreria se low_3 <= high_1, mas isso contradiz
            # a definição de bullish FVG (low_3 > high_1), logo sempre False.
            filled = low_3 <= high_1

        elif bearish_fvg:
            # Gap está entre high_3 e low_1
            gap_size = low_1 - high_3
            # Fill: uma vela posterior penetra no gap.
            # Com apenas 3 velas, o FVG acaba de se formar e está aberto.
            # O fill só ocorreria se high_3 >= low_1, mas isso contradiz
            # a definição de bearish FVG (high_3 < low_1), logo sempre False.
            filled = high_3 >= low_1



        evidences = []


        if bullish_fvg or bearish_fvg:

            direction = (
                "BULLISH"
                if bullish_fvg
                else "BEARISH"
            )

            # Calcular qualidade dinâmica baseada no tamanho do gap
            # e status de preenchimento
            # Gap aberto (não preenchido) = maior qualidade
            # Gap maior (relativo ao range) = maior qualidade
            candle_range = max(
                high_1 - low_1,
                high_2 - low_2,
                high_3 - low_3
            )
            if candle_range > 0:
                gap_ratio = min(gap_size / candle_range, 1.0)
            else:
                gap_ratio = 0.0

            # Qualidade base: gap aberto tem mais valor que preenchido
            base_quality = 0.8 if not filled else 0.4
            # Ajuste pelo tamanho relativo do gap
            fvg_quality = round(base_quality * (0.5 + 0.5 * gap_ratio), 2)
            fvg_quality = min(max(fvg_quality, 0.0), 1.0)

            # Confiança: gap aberto e maior = mais confiança
            confidence = round((0.6 + 0.4 * gap_ratio) if not filled else (0.3 + 0.2 * gap_ratio), 2)
            confidence = min(max(confidence, 0.0), 1.0)

            quality = fvg_quality

            # Strength e weight dinâmicos para Evidence
            strength = round(60.0 + 40.0 * gap_ratio, 1) if not filled else round(30.0 + 20.0 * gap_ratio, 1)
            weight = 60.0 if not filled else 30.0

            evidences.append(
                Evidence(
                    "FairValueGapEngine",
                    "FVG",
                    direction,
                    strength,
                    confidence * 100,
                    f"{direction} Fair Value Gap detectado (gap_size={gap_size:.4f}, filled={filled})",
                    weight
                )
            )

        else:
            fvg_quality = 0.0
            confidence = 0.0
            quality = 0.0


        metadata = {
            "gap_size": gap_size,
            "filled": filled,
            "candle_indices": {
                "c1": int(df.index[-3]) if len(df) >= 3 else None,
                "c2": int(df.index[-2]) if len(df) >= 2 else None,
                "c3": int(df.index[-1]) if len(df) >= 1 else None,
            },
        }


        return FairValueGapAnalysis(

            is_bullish_fvg=bool(bullish_fvg),

            is_bearish_fvg=bool(bearish_fvg),

            is_filled=bool(filled),

            is_open=not filled,

            fvg_quality=fvg_quality,

            confidence=confidence,

            quality=quality,

            evidences=tuple(evidences),

            metadata=metadata

        )