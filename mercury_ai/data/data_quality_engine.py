import pandas as pd
from typing import Tuple


class DataQualityEngine:
    """
    Motor institucional de validação de qualidade de dados.
    """

    def validate(self, df: pd.DataFrame) -> Tuple[bool, float, str]:

        if df.empty:
            return False, 0.0, "Empty DataFrame"

        # Detectar timestamps inválidos (NaT) antes de qualquer coisa
        if df.index.isna().any():
            return False, 0.0, "Invalid timestamps (NaT) detected"


        if df.isnull().values.any():
            return False, 0.1, "NaN values detected"


        if df.index.duplicated().any():
            return False, 0.2, "Duplicate timestamps"


        required_columns = [
            "open",
            "high",
            "low",
            "close"
        ]


        missing = [
            c for c in required_columns
            if c not in df.columns
        ]


        if missing:
            return False, 0.0, f"Missing columns: {missing}"


        if (df[required_columns] < 0).any().any():
            return False, 0.1, "Negative price data"


        if "volume" in df.columns:

            if (df["volume"] < 0).any():
                return False, 0.3, "Negative volume"


        if (df["low"] > df["high"]).any():
            return False, 0.1, "Invalid candle"


        # Temporal gap classification:
        # Distingue gaps reais de dados de períodos legítimos sem negociação
        # ou artefatos de agregação de dados (ex: Yahoo Finance crypto candles
        # com gap ~45min na fronteira UTC midnight).
        #
        # CLASSIFICAÇÃO DE CADA GAP:
        #   - < 2x expected_interval  → NORMAL (variação típica)
        #   - 2x a 3x interval       → MINOR_SKIP ( candle perdido tolerável)
        #   - > 3x interval, cruza   → EXPECTED_NON_TRADING (artefato de
        #     dia UTC, ex: gap crypto 45min)
        #   - > 3x interval, NÃO     → UNEXPECTED_DATA_GAP (dados perdidos
        #     cruza dia UTC            realmente faltando)
        #
        # Apenas UNEXPECTED_DATA_GAP causa rejeição. EXPECTED_NON_TRADING e
        # MINOR_SKIP degradam o score mas permitem análise.
        if len(df) > 1:
            time_diffs = df.index.to_series().diff().dropna()
            if len(time_diffs) > 0:
                expected_interval = time_diffs.median()
                if expected_interval > pd.Timedelta(0):
                    gaps = time_diffs[time_diffs > expected_interval * 3]
                    unexpected_gaps = []
                    for idx, gap_size in gaps.items():
                        # Verifica se o gap cruza uma fronteira de dia UTC
                        prev_idx = time_diffs.index[time_diffs.index.get_loc(idx) - 1]
                        crosses_day = prev_idx.day != idx.day
                        if gap_size > expected_interval * 3 and not crosses_day:
                            unexpected_gaps.append((idx, gap_size))

                    if unexpected_gaps:
                        return False, 0.4, "Temporal gaps detected (unexpected data loss)"
                    # Gaps classificados como EXPECTED_NON_TRADING ou MINOR_SKIP:
                    # degrada score, mas permite análise (não mascara erro real)
                    if len(gaps) > 0:
                        return True, 0.8, "Temporal gaps detected (non-trading / data artifact, allowed)"


        if len(df) > 10:

            std = df["close"].std()

            if std > 0:

                z_scores = (
                    df["close"] -
                    df["close"].mean()
                ) / std


                if (z_scores.abs() > 5).any():
                    return False, 0.5, "Extreme price outliers"


        return True, 1.0, "Data quality pass"