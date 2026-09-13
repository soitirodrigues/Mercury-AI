import pandas as pd
import numpy as np


class IndicatorEngine:
    """
    Motor de indicadores técnicos do Mercury AI.
    Trabalha com padrão OHLCV:
    open, high, low, close, volume
    """


    def calculate(self, df: pd.DataFrame):

        data = df.copy()

        # Handle empty DataFrame - return default values matching MarketData fields
        if data.empty:
            return {
                "close": 0.0,
                "ema9": 0.0,
                "ema21": 0.0,
                "ema50": 0.0,
                "rsi": 50.0,
                "atr": 0.0,
                "adx": 0.0,
                "macd": 0.0,
                "macd_signal": 0.0,
                "bollinger_upper": 0.0,
                "bollinger_lower": 0.0,
                "volume": 0.0,
            }


        close = data["close"]
        high = data["high"]
        low = data["low"]
        volume = data["volume"]


        # EMA

        ema9 = (
            close
            .ewm(span=9)
            .mean()
        )

        ema21 = (
            close
            .ewm(span=21)
            .mean()
        )

        ema50 = (
            close
            .ewm(span=50)
            .mean()
        )


        # RSI 14

        delta = close.diff()

        gain = (
            delta
            .clip(lower=0)
            .rolling(14)
            .mean()
        )

        loss = (
            -delta
            .clip(upper=0)
            .rolling(14)
            .mean()
        )


        rs = gain / loss

        rsi = (
            100 -
            (100 / (1 + rs))
        )


        # ATR

        tr1 = high - low

        tr2 = abs(high - close.shift())

        tr3 = abs(low - close.shift())


        true_range = pd.concat(
            [
                tr1,
                tr2,
                tr3
            ],
            axis=1
        ).max(axis=1)


        atr = (
            true_range
            .rolling(14)
            .mean()
        )


        # ADX-14 Wilder (F4: antes zerado — regime nunca detectava tendência).
        # +DM/-DM suavizados por Wilder, DX médio 14 períodos. Sem upload de
        # pesos: cálculo determinístico puro sobre high/low/close.
        up_move = high.diff()
        down_move = (-low.diff()).clip(lower=0)
        up_move = up_move.clip(lower=0)
        plus_dm = pd.Series(np.where((up_move > down_move), up_move, 0.0), index=data.index)
        minus_dm = pd.Series(np.where((down_move > up_move), down_move, 0.0), index=data.index)
        atr_w = true_range.ewm(alpha=1.0 / 14, adjust=False).mean()
        plus_di = 100.0 * (plus_dm.ewm(alpha=1.0 / 14, adjust=False).mean() / atr_w.replace(0, np.nan))
        minus_di = 100.0 * (minus_dm.ewm(alpha=1.0 / 14, adjust=False).mean() / atr_w.replace(0, np.nan))
        dx = (100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)).fillna(0.0)
        adx = dx.ewm(alpha=1.0 / 14, adjust=False).mean().fillna(0.0)



        # MACD

        ema12 = close.ewm(span=12).mean()

        ema26 = close.ewm(span=26).mean()


        macd = ema12 - ema26

        macd_signal = (
            macd
            .ewm(span=9)
            .mean()
        )


        # Bollinger Bands

        middle = (
            close
            .rolling(14)
            .mean()
        )


        std = (
            close
            .rolling(14)
            .std()
        )


        bollinger_upper = middle + (2 * std)

        bollinger_lower = middle - (2 * std)



        return {

            "close": float(close.iloc[-1]),

            "ema9": float(ema9.iloc[-1]),

            "ema21": float(ema21.iloc[-1]),

            "ema50": float(ema50.iloc[-1]),

            "rsi": float(rsi.iloc[-1]),

            "atr": float(atr.iloc[-1]),

            "adx": float(adx.iloc[-1]),

            "macd": float(macd.iloc[-1]),

            "macd_signal": float(macd_signal.iloc[-1]),

            "bollinger_upper": float(bollinger_upper.iloc[-1]),

            "bollinger_lower": float(bollinger_lower.iloc[-1]),

            "volume": float(
                data["volume"].iloc[-1]
                if "volume" in data.columns
                else 0
            )
        }