from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import pandas as pd


@dataclass(frozen=True)
class OrderBlockResult:
    """Resultado da análise de Order Block."""
    detected: bool
    direction: str  # "BULLISH" | "BEARISH" | "NONE"
    ob_type: str    # "BULLISH_OB" | "BEARISH_OB" | "NONE"
    price: float
    volume_strength: float
    confidence: int
    explanation: Tuple[str, ...]


class OrderBlockEngine:
    """
    Identifica Order Blocks institucionais.

    Um Order Block é a última vela de tendência oposta antes de um
    movimento impulsivo (displacement) com volume elevado.

    - Bullish OB: última vela bearish antes de impulso bullish.
    - Bearish OB: última vela bullish antes de impulso bearish.
    """

    #: Janela para média móvel de volume.
    _VOL_WINDOW = 20
    #: Fator mínimo de volume para caracterizar impulso.
    _VOL_MULTIPLIER = 1.5
    #: Número mínimo de candles para análise.
    _MIN_CANDLES = 20

    def analyze(self, df: pd.DataFrame) -> Optional[OrderBlockResult]:
        if df is None or len(df) < self._MIN_CANDLES:
            return None

        df = df.copy()
        df = df.reset_index(drop=True)
        df = df.loc[:, ~df.columns.duplicated()]

        # Garantir dados numéricos
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        required = {"Open", "High", "Low", "Close", "Volume"}
        if not required.issubset(df.columns):
            return None

        # Descartar linhas com NaN nas colunas essenciais
        df = df.dropna(subset=["Open", "High", "Low", "Close", "Volume"])
        if len(df) < self._MIN_CANDLES:
            return None

        volume = df["Volume"]
        vol_avg = volume.rolling(self._VOL_WINDOW).mean().iloc[-1]
        current_volume = volume.iloc[-1]

        if pd.isna(vol_avg) or vol_avg == 0:
            return None

        candle = df.iloc[-1]
        open_price = float(candle["Open"])
        close_price = float(candle["Close"])

        vol_strength = float(current_volume / vol_avg)
        is_impulse = current_volume > vol_avg * self._VOL_MULTIPLIER

        if not is_impulse:
            return None

        is_bullish_candle = close_price > open_price
        is_bearish_candle = close_price < open_price

        # ------------------------------------------------------------------
        # Bullish OB: vela atual é bullish (impulso de alta) → procurar
        # a última vela bearish antes deste impulso.
        # ------------------------------------------------------------------
        if is_bullish_candle:
            ob_index = self._find_last_opposite_candle(df, -1, bullish=False)
            if ob_index is not None:
                ob_candle = df.iloc[ob_index]
                ob_price = float(ob_candle["Low"])
                return OrderBlockResult(
                    detected=True,
                    direction="BULLISH",
                    ob_type="BULLISH_OB",
                    price=ob_price,
                    volume_strength=vol_strength,
                    confidence=self._calc_confidence(vol_strength),
                    explanation=(
                        f"Order Block Bullish detectado: última vela bearish "
                        f"antes de impulso de alta. Volume {vol_strength:.2f}x "
                        f"a média.",
                    ),
                )

        # ------------------------------------------------------------------
        # Bearish OB: vela atual é bearish (impulso de baixa) → procurar
        # a última vela bullish antes deste impulso.
        # ------------------------------------------------------------------
        if is_bearish_candle:
            ob_index = self._find_last_opposite_candle(df, -1, bullish=True)
            if ob_index is not None:
                ob_candle = df.iloc[ob_index]
                ob_price = float(ob_candle["High"])
                return OrderBlockResult(
                    detected=True,
                    direction="BEARISH",
                    ob_type="BEARISH_OB",
                    price=ob_price,
                    volume_strength=vol_strength,
                    confidence=self._calc_confidence(vol_strength),
                    explanation=(
                        f"Order Block Bearish detectado: última vela bullish "
                        f"antes de impulso de baixa. Volume {vol_strength:.2f}x "
                        f"a média.",
                    ),
                )

        return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _find_last_opposite_candle(
        df: pd.DataFrame,
        end_idx: int,
        bullish: bool,
    ) -> Optional[int]:
        """
        Encontra o índice da última vela de direção oposta antes de
        ``end_idx`` (exclusivo).

        Se ``bullish=True``, procura a última vela bullish (Close > Open).
        Se ``bullish=False``, procura a última vela bearish (Close < Open).
        """
        end = end_idx if end_idx >= 0 else len(df) + end_idx
        for i in range(end - 1, -1, -1):
            row = df.iloc[i]
            if bullish:
                if float(row["Close"]) > float(row["Open"]):
                    return i
            else:
                if float(row["Close"]) < float(row["Open"]):
                    return i
        return None

    @staticmethod
    def _calc_confidence(vol_strength: float) -> int:
        """
        Calcula confiança (0-100) com base na força do volume do impulso.
        """
        # 1.5x → 50, 2.0x → 70, 3.0x+ → 90
        if vol_strength >= 3.0:
            return 90
        if vol_strength >= 2.0:
            return 70
        if vol_strength >= 1.5:
            return 50
        return 0



        return None