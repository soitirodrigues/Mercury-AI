import math
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional

from mercury_ai.models.evidence import Evidence
from mercury_ai.models.swing_analysis import Swing, SwingSequenceResult


class SwingEngine:
    """
    Motor institucional de estrutura de mercado Mercury AI.
    Compatível com padrão OHLCV:
    open, high, low, close, volume

    Detecta swings (pivots) institucionais usando janela de pivô e filtro ATR.
    Calcula força dinâmica do swing baseada em deslocamento ATR, volume relativo
    e distância do swing anterior. Gera evidências ricas para o motor de confluência.
    """

    def __init__(
        self,
        pivot_window: int = 5,
        atr_period: int = 14,
        atr_multiplier: float = 0.5
    ):
        if pivot_window < 1:
            raise ValueError(
                f"pivot_window must be >= 1, got {pivot_window}"
            )
        if atr_period < 1:
            raise ValueError(
                f"atr_period must be >= 1, got {atr_period}"
            )
        if atr_multiplier <= 0:
            raise ValueError(
                f"atr_multiplier must be > 0, got {atr_multiplier}"
            )

        self.pivot_window: int = pivot_window
        self.atr_period: int = atr_period
        self.atr_multiplier: float = atr_multiplier



    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        """
        Calcula o Average True Range (ATR) via EMA com alpha=1/atr_period.

        Retorna uma pd.Series indexada pelo mesmo índice de ``df``.
        O primeiro elemento (sem prev_close) usa high-low como TR fallback.
        """
        if df is None or df.empty:
            raise ValueError("calculate_atr: DataFrame vazio ou None")

        # Normalize column names to lowercase for case-insensitive access (work on a copy)
        df = df.copy()
        df.columns = [str(c).strip().lower() for c in df.columns]
        # Drop duplicate columns that may result from DataNormalizer adding both lowercase and uppercase
        df = df.loc[:, ~df.columns.duplicated()]

        required = {"high", "low", "close"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"calculate_atr: colunas obrigatórias ausentes: {missing}"
            )

        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)

        prev_close = close.shift(1)

        # True Range: para o primeiro candle (prev_close=NaN) usa high-low
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        # Garante que o primeiro candle tenha TR = high-low (não NaN)
        tr.iloc[0] = float(high.iloc[0] - low.iloc[0])

        atr = tr.ewm(
            alpha=1.0 / self.atr_period,
            adjust=False
        ).mean()

        return atr



    def _compute_swing_strength(
        self,
        atr_at_pivot: float,
        displacement: float,
        volume_at_pivot: float,
        avg_volume: float
    ) -> float:
        """
        Calcula força dinâmica do swing (0-100) baseada em:
        - Deslocamento relativo ao ATR (displacement / ATR)
        - Volume relativo à média (volume / avg_volume)
        Combina ambos os fatores ponderadamente.
        """
        # Fator de deslocamento: quanto maior o movimento relativo ao ATR, maior a força
        atr_ratio = displacement / atr_at_pivot if atr_at_pivot > 0 else 0.0
        # Normaliza: ATR ratio de 2.0+ é excepcional (força máxima)
        displacement_factor = min(atr_ratio / 2.0, 1.0) * 60.0

        # Fator de volume: volume acima da média aumenta a força
        vol_ratio = (
            volume_at_pivot / avg_volume
            if avg_volume > 0
            else 1.0
        )
        # Normaliza: volume 3x a média é excepcional
        volume_factor = min(max(vol_ratio - 1.0, 0.0) / 2.0, 1.0) * 40.0

        strength = displacement_factor + volume_factor
        # Garante range 0-100
        return float(max(0.0, min(100.0, strength)))

    def _compute_evidence_values(
        self,
        swing_strength: float,
        classification: str,
        is_high: bool
    ) -> Tuple[float, float, float]:
        """
        Calcula strength, confidence e weight dinâmicos para a Evidence.
        - strength: derivada da força do swing (escala 40-95)
        - confidence: maior para classificações mais decisivas (HH/LL vs HL/LH)
        - weight: maior para swings de maior força
        """
        # Strength: escala a swing_strength para o range 40-95
        strength = 40.0 + (swing_strength / 100.0) * 55.0

        # Confidence: HH e LL são mais decisivos que HL e LH
        if classification in ("HH", "LL"):
            confidence = 80.0 + (swing_strength / 100.0) * 15.0  # 80-95
        else:
            confidence = 65.0 + (swing_strength / 100.0) * 15.0  # 65-80

        # Weight: escala 10-30 baseado na força
        weight = 10.0 + (swing_strength / 100.0) * 20.0

        return float(strength), float(confidence), float(weight)

    def detect_swings(
        self,
        df: pd.DataFrame
    ) -> Tuple[List[Swing], List[Evidence]]:
        """
        Detecta swings (pivots) institucionais no DataFrame OHLCV.

        Retorna (swings, evidences) onde swings é a lista combinada de
        swing highs e swing lows ordenados por índice, e evidences é a
        lista de evidências correspondentes.
        """
        # ------------------------------------------------------------------
        # Input validation
        # ------------------------------------------------------------------
        if df is None or df.empty:
            raise ValueError("detect_swings: DataFrame vazio ou None")

        min_rows = 2 * self.pivot_window + 1
        if len(df) < min_rows:
            raise ValueError(
                f"detect_swings: DataFrame muito curto ({len(df)} rows), "
                f"mínimo necessário: {min_rows} (2*pivot_window+1)"
            )

        # Normalize column names to lowercase for case-insensitive access (work on a copy)
        df = df.copy()
        df.columns = [str(c).strip().lower() for c in df.columns]
        # Drop duplicate columns that may result from DataNormalizer adding both lowercase and uppercase
        df = df.loc[:, ~df.columns.duplicated()]

        required = {"high", "low"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"detect_swings: colunas obrigatórias ausentes: {missing}"
            )

        highs = df["high"].astype(float)
        lows = df["low"].astype(float)

        volume = (
            df["volume"].astype(float)
            if "volume" in df.columns
            else pd.Series(0.0, index=df.index, dtype=float)
        )

        atr = self.calculate_atr(df)

        # Média móvel de volume para referência relativa (janela = atr_period)
        vol_window = max(self.atr_period, self.pivot_window * 2)
        avg_volume_series = volume.rolling(
            window=min(vol_window, len(volume)),
            min_periods=1
        ).mean()

        confirmed_highs: List[Swing] = []
        confirmed_lows: List[Swing] = []
        evidences: List[Evidence] = []



        for i in range(
            self.pivot_window,
            len(df)-self.pivot_window
        ):



            # ======================
            # SWING HIGH
            # ======================

            if (
                all(
                    highs.iloc[i] >
                    highs.iloc[i-self.pivot_window:i]
                )
                and
                all(
                    highs.iloc[i] >
                    highs.iloc[i+1:i+self.pivot_window+1]
                )
            ):


                price = float(
                    highs.iloc[i]
                )


                if (
                    not confirmed_highs
                    or
                    abs(
                        confirmed_highs[-1].price
                        -
                        price
                    )
                    >
                    atr.iloc[i] *
                    self.atr_multiplier
                ):


                    classification = (
                        "HH"
                        if (
                            not confirmed_highs
                            or
                            price >
                            confirmed_highs[-1].price
                        )
                        else
                        "LH"
                    )

                    # Distância absoluta do swing high anterior
                    distance = (
                        abs(price - confirmed_highs[-1].price)
                        if confirmed_highs
                        else 0.0
                    )

                    # Deslocamento (displacement) relativo ao ATR
                    displacement = (
                        abs(price - confirmed_highs[-1].price)
                        if confirmed_highs
                        else float(atr.iloc[i])
                    )

                    avg_vol = (
                        float(avg_volume_series.iloc[i])
                        if avg_volume_series.iloc[i] > 0
                        else 1.0
                    )

                    swing_strength = self._compute_swing_strength(
                        atr_at_pivot=float(atr.iloc[i]),
                        displacement=displacement,
                        volume_at_pivot=float(volume.iloc[i]),
                        avg_volume=avg_vol
                    )

                    ev_strength, ev_confidence, ev_weight = (
                        self._compute_evidence_values(
                            swing_strength=swing_strength,
                            classification=classification,
                            is_high=True
                        )
                    )

                    swing = Swing(
                        "HIGH",
                        classification,
                        price,
                        str(df.index[i]),
                        i,
                        float(atr.iloc[i]),
                        swing_strength,
                        float(volume.iloc[i]),
                        True,
                        distance
                    )

                    confirmed_highs.append(swing)

                    evidences.append(
                        Evidence.create(
                            engine_name="SwingEngine",
                            evidence_name=f"New {classification}",
                            direction=(
                                "BULLISH"
                                if classification == "HH"
                                else "BEARISH"
                            ),
                            strength=ev_strength,
                            confidence=ev_confidence,
                            description=f"Swing High {classification} at price {price:.4f}",
                            weight=ev_weight,
                            metadata={
                                "swing_type": "HIGH",
                                "classification": classification,
                                "price": price,
                                "index": i,
                                "atr": float(atr.iloc[i]),
                                "swing_strength": swing_strength,
                                "distance_from_previous": distance,
                            }
                        )
                    )




            # ======================
            # SWING LOW
            # ======================


            if (
                all(
                    lows.iloc[i] <
                    lows.iloc[i-self.pivot_window:i]
                )
                and
                all(
                    lows.iloc[i] <
                    lows.iloc[i+1:i+self.pivot_window+1]
                )
            ):


                price = float(
                    lows.iloc[i]
                )


                if (
                    not confirmed_lows
                    or
                    abs(
                        confirmed_lows[-1].price
                        -
                        price
                    )
                    >
                    atr.iloc[i] *
                    self.atr_multiplier
                ):


                    classification = (
                        "HL"
                        if (
                            not confirmed_lows
                            or
                            price >
                            confirmed_lows[-1].price
                        )
                        else
                        "LL"
                    )

                    # Distância absoluta do swing low anterior
                    distance = (
                        abs(price - confirmed_lows[-1].price)
                        if confirmed_lows
                        else 0.0
                    )

                    # Deslocamento (displacement) relativo ao ATR
                    displacement = (
                        abs(price - confirmed_lows[-1].price)
                        if confirmed_lows
                        else float(atr.iloc[i])
                    )

                    avg_vol = (
                        float(avg_volume_series.iloc[i])
                        if avg_volume_series.iloc[i] > 0
                        else 1.0
                    )

                    swing_strength = self._compute_swing_strength(
                        atr_at_pivot=float(atr.iloc[i]),
                        displacement=displacement,
                        volume_at_pivot=float(volume.iloc[i]),
                        avg_volume=avg_vol
                    )

                    ev_strength, ev_confidence, ev_weight = (
                        self._compute_evidence_values(
                            swing_strength=swing_strength,
                            classification=classification,
                            is_high=False
                        )
                    )

                    swing = Swing(
                        "LOW",
                        classification,
                        price,
                        str(df.index[i]),
                        i,
                        float(atr.iloc[i]),
                        swing_strength,
                        float(volume.iloc[i]),
                        True,
                        distance
                    )

                    confirmed_lows.append(swing)

                    evidences.append(
                        Evidence.create(
                            engine_name="SwingEngine",
                            evidence_name=f"New {classification}",
                            direction=(
                                "BULLISH"
                                if classification == "HL"
                                else "BEARISH"
                            ),
                            strength=ev_strength,
                            confidence=ev_confidence,
                            description=f"Swing Low {classification} at price {price:.4f}",
                            weight=ev_weight,
                            metadata={
                                "swing_type": "LOW",
                                "classification": classification,
                                "price": price,
                                "index": i,
                                "atr": float(atr.iloc[i]),
                                "swing_strength": swing_strength,
                                "distance_from_previous": distance,
                            }
                        )
                    )



        return (
            confirmed_highs + confirmed_lows,
            evidences
        )



    def analyze_sequence(
        self,
        swings: List[Swing]
    ) -> SwingSequenceResult:
        """
        Analisa a sequência de swings para determinar direção de tendência,
        qualidade da sequência e confiança.

        - sequence_quality (0-100): mede a consistência direcional da sequência
          (proporção de swings alinhados à tendência dominante) ponderada
          pela força média dos swings.
        - sequence_confidence (0-100): mede a confiança na detecção da
          tendência, baseada na proporção de swings alinhados e na força média.
        """
        if not swings or len(swings) < 3:
            return SwingSequenceResult()

        sorted_swings = sorted(swings, key=lambda x: x.index)

        sequence = [s.classification for s in sorted_swings[-5:]]

        trend = "NEUTRAL"
        transition = False

        bullish_set = {"HH", "HL"}
        bearish_set = {"LL", "LH"}

        last_4 = sequence[-4:]

        if all(x in bullish_set for x in last_4):
            trend = "BULLISH"
        elif all(x in bearish_set for x in last_4):
            trend = "BEARISH"
        else:
            transition = True

        # ------------------------------------------------------------------
        # Cálculo dinâmico de sequence_quality e sequence_confidence
        # ------------------------------------------------------------------
        # Usa os swings da sequência (últimos 5) para calcular métricas
        seq_swings = sorted_swings[-len(sequence):]
        strengths = [s.strength for s in seq_swings]
        avg_strength = float(np.mean(strengths)) if strengths else 0.0

        # Conta swings alinhados à tendência detectada
        if trend == "BULLISH":
            aligned = sum(1 for c in sequence if c in bullish_set)
        elif trend == "BEARISH":
            aligned = sum(1 for c in sequence if c in bearish_set)
        else:
            # NEUTRAL: conta alinhamento majoritário
            bull_count = sum(1 for c in sequence if c in bullish_set)
            bear_count = sum(1 for c in sequence if c in bearish_set)
            aligned = max(bull_count, bear_count)

        alignment_ratio = aligned / len(sequence) if sequence else 0.0

        # sequence_quality: combina alinhamento direcional (70%) e força média (30%)
        sequence_quality = float(
            (alignment_ratio * 70.0) + ((avg_strength / 100.0) * 30.0)
        )
        sequence_quality = max(0.0, min(100.0, sequence_quality))

        # sequence_confidence: maior quando mais swings alinhados e maior força
        # Para tendências decisivas (BULLISH/BEARISH), confiança é maior
        if trend in ("BULLISH", "BEARISH"):
            sequence_confidence = float(
                (alignment_ratio * 60.0) + ((avg_strength / 100.0) * 40.0)
            )
        else:
            # Transição: confiança menor pois não há tendência clara
            sequence_confidence = float(
                (alignment_ratio * 40.0) + ((avg_strength / 100.0) * 30.0)
            )
        sequence_confidence = max(0.0, min(100.0, sequence_confidence))

        return SwingSequenceResult(
            current_swing=sorted_swings[-1],
            previous_swing=sorted_swings[-2],
            sequence=tuple(sequence),
            sequence_length=len(sequence),
            trend_direction=trend,
            trend_transition=transition,
            sequence_quality=sequence_quality,
            sequence_confidence=sequence_confidence
        )