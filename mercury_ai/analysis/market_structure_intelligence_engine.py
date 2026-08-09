from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pandas as pd

from mercury_ai.analysis.swing_engine import SwingEngine
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.models.swing_analysis import Swing


class MarketStructureIntelligenceEngine:
    """
    Motor institucional avançado para análise de estrutura de mercado.

    Construído sobre o ``SwingEngine``, este motor detecta Break of Structure
    (BOS), Change of Character (CHoCH), Market Structure Shift (MSS), mede
    impulsos vs. correções, identifica displacement institucional e calcula
    zonas de Premium/Discount/OTE — tudo com valores dinâmicos baseados em
    evidência quantitativa real, nunca hard-coded.
    """

    # ------------------------------------------------------------------ #
    #  Constantes calibráveis                                             #
    # ------------------------------------------------------------------ #

    #: Janela móvel padrão para médias de volume e body
    _ROLLING_WINDOW: int = 20

    #: Múltiplo de body médio para classificar displacement (2× = forte)
    _DISPLACEMENT_BODY_MULT: float = 2.0

    #: Múltiplo de volume médio para confirmar displacement
    _DISPLACEMENT_VOL_MULT: float = 1.0

    #: Peso base para evidência de Displacement
    _DISPLACEMENT_WEIGHT_BASE: float = 40.0

    #: Peso base para evidência de OTE
    _OTE_WEIGHT_BASE: float = 30.0

    #: Peso base para evidência de BOS
    _BOS_WEIGHT_BASE: float = 35.0

    #: Peso base para evidência de CHoCH
    _CHOCH_WEIGHT_BASE: float = 45.0

    #: Peso base para evidência de MSS
    _MSS_WEIGHT_BASE: float = 50.0

    # ------------------------------------------------------------------ #
    #  Construtor                                                         #
    # ------------------------------------------------------------------ #

    def __init__(self) -> None:
        self.swing_engine = SwingEngine()

    # ------------------------------------------------------------------ #
    #  API pública                                                        #
    # ------------------------------------------------------------------ #

    def evaluate(
        self,
        df: pd.DataFrame,
        avg_volume: pd.Series | None = None,
        avg_body: pd.Series | None = None,
    ) -> Tuple[MarketStructureProfile, List[Evidence]]:
        """Avalia a estrutura de mercado e retorna perfil + evidências."""

        # ------------------------------------------------------------------
        #  0. Validação de entrada
        # ------------------------------------------------------------------
        if df is None or df.empty:
            return MarketStructureProfile(), []

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"df deve ser um pandas.DataFrame, recebeu {type(df).__name__}"
            )

        required_cols = {"open", "high", "low", "close", "volume"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(
                f"DataFrame não contém colunas obrigatórias: {sorted(missing)}"
            )

        # ------------------------------------------------------------------
        #  1. Normalização de colunas (cópia — não muta o input)
        # ------------------------------------------------------------------
        df = df.copy()
        df.columns = [str(c).strip().lower() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        if len(df) < 3:
            return MarketStructureProfile(), []

        # ------------------------------------------------------------------
        #  2. Detectar swings e sequência
        # ------------------------------------------------------------------
        swings, evidences = self.swing_engine.detect_swings(df)

        if len(swings) < 2:
            return MarketStructureProfile(), evidences

        sequence_result = self.swing_engine.analyze_sequence(swings)

        # ------------------------------------------------------------------
        #  3. Detectar BOS / CHoCH / MSS
        # ------------------------------------------------------------------
        (
            bos,
            choch,
            mss,
            break_price,
            break_strength,
            break_timestamp,
            structure_evidences,
        ) = self._detect_structure_breaks(swings, df)

        evidences.extend(structure_evidences)

        # ------------------------------------------------------------------
        #  4. Impulsos vs. Correções (baseado em classificação, não em paridade de índice)
        # ------------------------------------------------------------------
        impulses, corrections = self._split_impulses_corrections(swings)

        avg_impulse = (
            sum(impulses) / len(impulses) if impulses else 0.0
        )
        avg_correction = (
            sum(corrections) / len(corrections) if corrections else 0.0
        )

        # ------------------------------------------------------------------
        #  5. Displacement institucional
        # ------------------------------------------------------------------
        last_candle = df.iloc[-1]

        body = abs(float(last_candle["close"]) - float(last_candle["open"]))

        if avg_volume is not None:
            avg_vol = float(avg_volume.iloc[-1])
        else:
            avg_vol = float(
                df["volume"]
                .rolling(self._ROLLING_WINDOW)
                .mean()
                .iloc[-1]
            )

        if avg_body is not None:
            avg_bdy = float(avg_body.iloc[-1])
        else:
            avg_bdy = float(
                (df["close"] - df["open"])
                .abs()
                .rolling(self._ROLLING_WINDOW)
                .mean()
                .iloc[-1]
            )

        displacement = (
            body > (avg_bdy * self._DISPLACEMENT_BODY_MULT)
            and float(last_candle["volume"]) > (avg_vol * self._DISPLACEMENT_VOL_MULT)
        )

        direction = "NEUTRAL"

        if displacement:
            if float(last_candle["close"]) > float(last_candle["open"]):
                direction = "BULLISH"
            else:
                direction = "BEARISH"

            # Strength dinâmico: ratio body/avg_body escalado 50-95
            body_ratio = body / avg_bdy if avg_bdy > 0 else 0.0
            vol_ratio = (
                float(last_candle["volume"]) / avg_vol if avg_vol > 0 else 0.0
            )
            disp_strength = self._clamp(
                50.0 + (body_ratio - self._DISPLACEMENT_BODY_MULT) * 15.0,
                50.0,
                95.0,
            )
            disp_confidence = self._clamp(
                70.0 + min(vol_ratio, 3.0) * 8.0,
                70.0,
                95.0,
            )
            disp_weight = self._DISPLACEMENT_WEIGHT_BASE

            evidences.append(
                Evidence.create(
                    engine_name="StructureEngine",
                    evidence_name=f"{direction} Displacement",
                    direction=direction,
                    strength=disp_strength,
                    confidence=disp_confidence,
                    description=(
                        f"Displacement {direction} detectado — "
                        f"body {body_ratio:.2f}× avg, "
                        f"volume {vol_ratio:.2f}× avg"
                    ),
                    weight=disp_weight,
                    metadata={
                        "body_ratio": body_ratio,
                        "volume_ratio": vol_ratio,
                        "body": body,
                        "avg_body": avg_bdy,
                    },
                )
            )

        # ------------------------------------------------------------------
        #  6. Premium / Discount / OTE
        # ------------------------------------------------------------------
        equilibrium = 0.0
        premium = 0.0
        discount = 0.0
        ote = 0.0

        if (
            sequence_result.current_swing is not None
            and sequence_result.previous_swing is not None
        ):
            high = max(
                sequence_result.current_swing.price,
                sequence_result.previous_swing.price,
            )
            low = min(
                sequence_result.current_swing.price,
                sequence_result.previous_swing.price,
            )
            rng = high - low

            if rng > 0:
                equilibrium = low + (rng * 0.5)
                premium = high - (rng * 0.21)
                discount = low + (rng * 0.21)
                ote = low + (rng * 0.705)

                # Determinar direção da zona OTE
                if sequence_result.current_swing is not None:
                    if sequence_result.current_swing.type == "HIGH":
                        ote_direction = "BEARISH"
                    elif sequence_result.current_swing.type == "LOW":
                        ote_direction = "BULLISH"
                    else:
                        ote_direction = "NEUTRAL"
                else:
                    ote_direction = "NEUTRAL"

                ote_strength = self._clamp(
                    60.0 + sequence_result.sequence_confidence * 0.35,
                    60.0,
                    95.0,
                )
                ote_confidence = self._clamp(
                    70.0 + sequence_result.sequence_quality * 0.25,
                    70.0,
                    95.0,
                )

                evidences.append(
                    Evidence.create(
                        engine_name="StructureEngine",
                        evidence_name="OTE",
                        direction=ote_direction,
                        strength=ote_strength,
                        confidence=ote_confidence,
                        description=(
                            f"OTE em {ote:.5f} | "
                            f"Equilibrium {equilibrium:.5f} | "
                            f"Premium {premium:.5f} | "
                            f"Discount {discount:.5f}"
                        ),
                        weight=self._OTE_WEIGHT_BASE,
                        metadata={
                            "ote": ote,
                            "equilibrium": equilibrium,
                            "premium": premium,
                            "discount": discount,
                            "range": rng,
                        },
                    )
                )

        # ------------------------------------------------------------------
        #  7. Contagem HH / HL / LH / LL
        # ------------------------------------------------------------------
        hh = sum(1 for s in swings if s.classification == "HH")
        hl = sum(1 for s in swings if s.classification == "HL")
        lh = sum(1 for s in swings if s.classification == "LH")
        ll = sum(1 for s in swings if s.classification == "LL")

        # ------------------------------------------------------------------
        #  8. Construir perfil
        # ------------------------------------------------------------------
        displacement_strength = (
            float(body / avg_bdy) if avg_bdy > 0 else 0.0
        )

        profile = MarketStructureProfile(
            classification=sequence_result.trend_direction,
            trend_strength=sequence_result.sequence_confidence,
            hh_count=hh,
            hl_count=hl,
            lh_count=lh,
            ll_count=ll,
            confidence_score=sequence_result.sequence_confidence,
            current_swing=sequence_result.current_swing,
            previous_swing=sequence_result.previous_swing,
            current_sequence=sequence_result.sequence,
            bos=bos,
            choch=choch,
            mss=mss,
            break_strength=break_strength,
            break_price=break_price,
            break_timestamp=break_timestamp,
            impulse_strength=float(avg_impulse),
            correction_strength=float(avg_correction),
            displacement=displacement,
            displacement_strength=displacement_strength,
            displacement_direction=direction,
            premium_zone=float(premium),
            discount_zone=float(discount),
            equilibrium=float(equilibrium),
            ote=float(ote),
        )

        return profile, evidences

    # ------------------------------------------------------------------ #
    #  Métodos privados auxiliares                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _clamp(value: float, lo: float, hi: float) -> float:
        """Limita ``value`` ao intervalo [lo, hi]."""
        return max(lo, min(hi, value))

    def _detect_structure_breaks(
        self,
        swings: List[Swing],
        df: pd.DataFrame,
    ) -> Tuple[bool, bool, bool, float, float, str, List[Evidence]]:
        """
        Detecta BOS, CHoCH e MSS a partir da sequência de swings e preço atual.

        - **BOS** (Break of Structure): preço atual rompe o swing high/low
          anterior na direção da tendência confirmada.
        - **CHoCH** (Change of Character): preço atual rompe na direção oposta
          à tendência anterior, indicando potencial reversão.
        - **MSS** (Market Structure Shift): CHoCH confirmado por um novo swing
          na direção oposta (shift completo de estrutura).

        Returns:
            Tuple ``(bos, choch, mss, break_price, break_strength,
            break_timestamp, evidences)``
        """
        bos = False
        choch = False
        mss = False
        break_price = 0.0
        break_strength = 0.0
        break_timestamp = ""
        structure_evidences: List[Evidence] = []

        if len(swings) < 3:
            return (
                bos,
                choch,
                mss,
                break_price,
                break_strength,
                break_timestamp,
                structure_evidences,
            )

        # Último preço e timestamp do candle atual
        current_price = float(df.iloc[-1]["close"])
        current_ts = str(df.iloc[-1].get("timestamp", df.index[-1]))

        # Determinar tendência anterior a partir dos últimos 4 swings
        recent = swings[-4:] if len(swings) >= 4 else swings
        prev_trend = self._infer_trend_from_swings(recent[:-1] if len(recent) > 1 else recent)

        # Encontrar último swing high e último swing low confirmados
        last_high: Swing | None = None
        last_low: Swing | None = None
        for s in reversed(swings):
            if last_high is None and s.type == "HIGH":
                last_high = s
            if last_low is None and s.type == "LOW":
                last_low = s
            if last_high is not None and last_low is not None:
                break

        # --- BOS: rompimento na direção da tendência ---
        if prev_trend == "BULLISH" and last_high is not None:
            if current_price > last_high.price:
                bos = True
                break_price = float(last_high.price)
                break_strength = self._clamp(
                    ((current_price - last_high.price) / last_high.price) * 10000.0,
                    10.0,
                    95.0,
                )
                break_timestamp = current_ts
        elif prev_trend == "BEARISH" and last_low is not None:
            if current_price < last_low.price:
                bos = True
                break_price = float(last_low.price)
                break_strength = self._clamp(
                    ((last_low.price - current_price) / last_low.price) * 10000.0,
                    10.0,
                    95.0,
                )
                break_timestamp = current_ts

        # --- CHoCH: rompimento na direção oposta à tendência ---
        if prev_trend == "BULLISH" and last_low is not None:
            if current_price < last_low.price:
                choch = True
                break_price = float(last_low.price)
                break_strength = self._clamp(
                    ((last_low.price - current_price) / last_low.price) * 10000.0,
                    15.0,
                    95.0,
                )
                break_timestamp = current_ts
        elif prev_trend == "BEARISH" and last_high is not None:
            if current_price > last_high.price:
                choch = True
                break_price = float(last_high.price)
                break_strength = self._clamp(
                    ((current_price - last_high.price) / last_high.price) * 10000.0,
                    15.0,
                    95.0,
                )
                break_timestamp = current_ts

        # --- MSS: CHoCH + novo swing confirmado na direção oposta ---
        if choch and len(swings) >= 2:
            last_swing = swings[-1]
            if prev_trend == "BULLISH" and last_swing.type == "HIGH":
                # CHoCH bearish confirmado por novo swing high (lower high)
                mss = True
            elif prev_trend == "BEARISH" and last_swing.type == "LOW":
                # CHoCH bullish confirmado por novo swing low (higher low)
                mss = True

        # --- Evidências de BOS / CHoCH / MSS ---
        if bos:
            bos_direction = "BULLISH" if prev_trend == "BULLISH" else "BEARISH"
            self._append_structure_evidence(
                evidences=structure_evidences,
                name="BOS",
                direction=bos_direction,
                strength=break_strength,
                confidence=self._clamp(break_strength + 5.0, 70.0, 95.0),
                weight=self._BOS_WEIGHT_BASE,
                break_price=break_price,
                current_price=current_price,
            )

        if choch:
            choch_direction = "BEARISH" if prev_trend == "BULLISH" else "BULLISH"
            self._append_structure_evidence(
                evidences=structure_evidences,
                name="CHoCH",
                direction=choch_direction,
                strength=break_strength,
                confidence=self._clamp(break_strength + 10.0, 75.0, 95.0),
                weight=self._CHOCH_WEIGHT_BASE,
                break_price=break_price,
                current_price=current_price,
            )

        if mss:
            mss_direction = "BEARISH" if prev_trend == "BULLISH" else "BULLISH"
            self._append_structure_evidence(
                evidences=structure_evidences,
                name="MSS",
                direction=mss_direction,
                strength=break_strength,
                confidence=self._clamp(break_strength + 15.0, 80.0, 95.0),
                weight=self._MSS_WEIGHT_BASE,
                break_price=break_price,
                current_price=current_price,
            )

        return (
            bos,
            choch,
            mss,
            break_price,
            break_strength,
            break_timestamp,
            structure_evidences,
        )

    def _append_structure_evidence(
        self,
        evidences: List[Evidence] | None,
        name: str,
        direction: str,
        strength: float,
        confidence: float,
        weight: float,
        break_price: float,
        current_price: float,
    ) -> None:
        """Cria e anexa evidência de estrutura (BOS/CHoCH/MSS)."""
        if evidences is None:
            return
        evidences.append(
            Evidence.create(
                engine_name="StructureEngine",
                evidence_name=name,
                direction=direction,
                strength=strength,
                confidence=confidence,
                description=(
                    f"{name} detectado — "
                    f"break {break_price:.5f}, "
                    f"preço atual {current_price:.5f}"
                ),
                weight=weight,
                metadata={
                    "break_price": break_price,
                    "current_price": current_price,
                },
            )
        )

    @staticmethod
    def _infer_trend_from_swings(swings: List[Swing]) -> str:
        """
        Infere direção de tendência a partir de uma lista de swings.

        - HH + HL → BULLISH
        - LH + LL → BEARISH
        - misto  → NEUTRAL
        """
        if not swings:
            return "NEUTRAL"

        bullish = 0
        bearish = 0
        for s in swings:
            if s.classification in ("HH", "HL"):
                bullish += 1
            elif s.classification in ("LH", "LL"):
                bearish += 1

        if bullish > bearish:
            return "BULLISH"
        if bearish > bullish:
            return "BEARISH"
        return "NEUTRAL"

    @staticmethod
    def _split_impulses_corrections(
        swings: List[Swing],
    ) -> Tuple[List[float], List[float]]:
        """
        Classifica distâncias entre swings em impulsos vs. correções.

        Em tendência bullish: HH→HL (correção), HL→HH (impulso).
        Em tendência bearish: LH→LL (impulso), LL→LH (correção).

        Heurística: se o swing de destino é HH ou LL → impulso (continuação
        da tendência). Se HL ou LH → correção (retracement).
        """
        impulses: List[float] = []
        corrections: List[float] = []

        for i in range(1, len(swings)):
            dist = abs(swings[i].price - swings[i - 1].price)
            cls = swings[i].classification
            if cls in ("HH", "LL"):
                impulses.append(dist)
            elif cls in ("HL", "LH"):
                corrections.append(dist)
            else:
                # Classificação desconhecida — assume correção conservadora
                corrections.append(dist)

        return impulses, corrections