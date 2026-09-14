"""Filtros institucionais M5 — observáveis puros (determinísticos, sem rede)."""
import pandas as pd

from mercury_ai.signals.m5_institutional_filters import (
    ADX_MIN_TREND,
    ADX_SPAN,
    ATR_CAP,
    BB_SPAN,
    BB_STD_MULT,
    EMA_SPAN,
    IDM_LOOKBACK,
    RSI_BUY_HI,
    RSI_BUY_LO,
    RSI_SELL_HI,
    RSI_SELL_LO,
    RSI_SPAN,
    SR_LOOKBACK,
    SR_PIVOT,
    TRIGGER_BODY_MIN,
    ZONE_LOOKBACK,
    adx_dmi,
    atr14,
    band_expansion,
    bollinger_bands,
    bollinger_pos,
    ema200_side,
    institutional_flags,
    reversal_candle,
    rsi14,
    rsi_adx_approved,
    rsi_value,
    smc_flags,
    sr_distance,
    trigger_aligned,
    trigger_body_ratio,
    trigger_range_atr,
)


def _df(rows):
    idx = pd.date_range("2026-09-14 14:00", periods=len(rows), freq="5min", tz="UTC")
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=idx)


def test_constants_documented():
    assert TRIGGER_BODY_MIN == 0.25
    assert ATR_CAP == 2.0
    assert EMA_SPAN == 200
    assert IDM_LOOKBACK == 5
    assert ZONE_LOOKBACK == 48
    # RSI+ADX audit-only (sem bloqueio)
    assert RSI_SPAN == 14
    assert ADX_SPAN == 14
    assert ADX_MIN_TREND == 20.0
    assert (RSI_BUY_LO, RSI_BUY_HI) == (50.0, 70.0)
    assert (RSI_SELL_LO, RSI_SELL_HI) == (30.0, 50.0)
    # Prompt-analise M5 audit-only (mesmo padrao, sem bloqueio)
    assert BB_SPAN == 20
    assert BB_STD_MULT == 2.0
    assert SR_LOOKBACK == 48
    assert SR_PIVOT == 3


def test_trigger_body_ratio():
    # corpo 0.8 / range 1.0 = 0.8
    df = _df([(100.0, 101.0, 100.0, 100.8)])
    assert trigger_body_ratio(df) == 0.8
    # range nulo -> None (nunca inventa)
    df2 = _df([(100.0, 100.0, 100.0, 100.0)])
    assert trigger_body_ratio(df2) is None
    # vazio -> None
    assert trigger_body_ratio(None) is None


def test_trigger_aligned():
    bull = _df([(100.0, 101.0, 99.5, 100.8)])
    bear = _df([(100.0, 101.0, 99.5, 99.6)])
    doji = _df([(100.0, 101.0, 99.5, 100.0)])
    assert trigger_aligned(bull, "BUY") is True
    assert trigger_aligned(bull, "SELL") is False
    assert trigger_aligned(bear, "SELL") is True
    assert trigger_aligned(bear, "BUY") is False
    assert trigger_aligned(doji, "BUY") is None
    assert trigger_aligned(bull, "WAIT") is None


def test_atr14_positive_and_short_df():
    rows = [(100 + i * 0.1, 100 + i * 0.1 + 0.5, 100 + i * 0.1 - 0.5, 100 + i * 0.1 + 0.05)
            for i in range(30)]
    assert atr14(_df(rows)) > 0
    assert atr14(_df(rows[:5])) is None  # <15 fechadas -> None honesto


def test_ema200_side_needs_200_rows():
    rows = [(100.0, 100.5, 99.5, 100.1)] * 50
    out = ema200_side(_df(rows), "BUY")
    assert out == {"aligned": None, "dist_atr": None}
    # tendência de alta longa: BUY alinhado
    n = 220
    base = [100 + i * 0.1 for i in range(n)]
    rows2 = [(b, b + 0.5, b - 0.5, b + 0.05) for b in base]
    out2 = ema200_side(_df(rows2), "BUY")
    assert out2["aligned"] is True
    assert ema200_side(_df(rows2), "SELL")["aligned"] is False


def test_institutional_flags_shape():
    rows = [(100 + i * 0.05, 100 + i * 0.05 + 0.4, 100 + i * 0.05 - 0.4, 100 + i * 0.05 + 0.1)
            for i in range(30)]
    flags = institutional_flags(_df(rows), "BUY")
    assert set(flags) == {"trigger_body_ratio", "trigger_aligned",
                          "trigger_range_atr", "ema200_aligned", "ema200_dist_atr",
                          "has_liquidity_sweep", "in_premium_discount_zone",
                          "has_fvg", "has_inducement",
                          "rsi", "adx", "plus_di", "minus_di", "rsi_adx_approved",
                          "bollinger_pos", "rsi_value", "reversal_candle",
                          "sr_distance", "band_expansion",
                          "bb_upper", "bb_middle", "bb_lower", "bb_bandwidth"}
    assert flags["trigger_body_ratio"] is not None
    assert flags["trigger_aligned"] in (True, False)
    assert flags["trigger_range_atr"] is not None
    assert flags["ema200_aligned"] is None  # <200 linhas: honesto
    # RSI+ADX observáveis (audit-only, nunca bloqueiam)
    assert flags["rsi"] is not None and 0.0 <= flags["rsi"] <= 100.0
    assert flags["adx"] is not None and flags["adx"] >= 0.0
    assert flags["plus_di"] is not None and flags["minus_di"] is not None
    assert flags["rsi_adx_approved"] in (True, False, None)
    # Prompt-analise audit-only (observaveis, sem bloqueio)
    assert flags["bollinger_pos"] in ("ABOVE_UPPER", "TOUCH_UPPER", "INSIDE",
                                        "TOUCH_LOWER", "BELOW_LOWER", None)
    assert flags["rsi_value"] is not None and 0.0 <= flags["rsi_value"] <= 100.0
    assert flags["reversal_candle"] in ("BULLISH_REVERSAL", "BEARISH_REVERSAL",
                                          "NONE", None)
    assert flags["sr_distance"] is None or flags["sr_distance"] >= 0.0
    assert flags["band_expansion"] in (True, False, None)
    assert flags["bb_upper"] is not None and flags["bb_lower"] is not None
    assert flags["bb_upper"] >= flags["bb_middle"] >= flags["bb_lower"]
    # trigger_range_atr respeita o teto documentado como referência
    assert isinstance(ATR_CAP, float)


def test_rsi_adx_observables_only():
    # df curto (<15): rsi/adx/dmi/approved = None honestos, sem exceção
    short = _df([(100.0, 100.5, 99.5, 100.1)] * 5)
    assert rsi14(short) is None
    assert adx_dmi(short) == {"adx": None, "plus_di": None, "minus_di": None}
    assert rsi_adx_approved(short, "BUY") is None
    assert rsi_adx_approved(short, "WAIT") is None
    # tendência de alta sustentada: BUY tende a aprovar, SELL a rejeitar
    n = 60
    base = [100 + i * 0.2 for i in range(n)]
    rows = [(b, b + 0.3, b - 0.3, b + 0.1) for b in base]
    df = _df(rows)
    rsi = rsi14(df)
    dmi = adx_dmi(df)
    assert rsi is not None and dmi["adx"] is not None
    assert dmi["plus_di"] > dmi["minus_di"]  # alta: comprador domina
    assert rsi_adx_approved(df, "BUY") in (True, False)  # observável, sem travar
    assert rsi_adx_approved(df, "SELL") is False  # DI contra: rejeita SELL
    assert rsi_adx_approved(df, "WAIT") is None  # sem direção: None honesto


def test_prompt_observables_audit_only():
    # df curto: Nones honestos, sem exceção, sem bloquear
    short = _df([(100.0, 100.5, 99.5, 100.1)] * 5)
    assert rsi_value(short) is None
    assert bollinger_bands(short) == {"middle": None, "upper": None,
                                      "lower": None, "bandwidth": None}
    assert bollinger_pos(short) is None
    assert band_expansion(short) is None
    assert reversal_candle(_df([(100.0, 100.5, 99.5, 100.1)])) is None  # <2: None honesto
    assert sr_distance(short) is None
    # reversão altista: martelo N (pavio inf >= 2x corpo) após queda N-1
    df_rev = _df([(100.0, 100.2, 99.6, 99.7),
                  (99.7, 99.9, 98.9, 99.8)])
    assert reversal_candle(df_rev) == "BULLISH_REVERSAL"
    # reversão baixista: shooting star N após alta N-1
    df_rev2 = _df([(99.0, 99.4, 98.8, 99.3),
                   (99.8, 100.6, 99.7, 99.75)])
    assert reversal_candle(df_rev2) == "BEARISH_REVERSAL"
    # doji: None honesto (sem direção inventada)
    df_doji = _df([(100.0, 100.5, 99.5, 100.2),
                   (100.2, 100.6, 99.8, 100.2)])
    assert reversal_candle(df_doji) is None
    # BB + expansão + S/R em tendência (60 fechadas)
    n = 60
    base = [100 + i * 0.2 for i in range(n)]
    rows = [(b, b + 0.3, b - 0.3, b + 0.1) for b in base]
    df = _df(rows)
    bb = bollinger_bands(df)
    assert bb["upper"] > bb["middle"] > bb["lower"] > 0
    assert bollinger_pos(df) in ("ABOVE_UPPER", "TOUCH_UPPER", "INSIDE",
                                 "TOUCH_LOWER", "BELOW_LOWER")
    assert band_expansion(df) in (True, False)
    assert rsi_value(df) == rsi14(df)  # alias nominal do prompt
    sr = sr_distance(df)
    assert sr is None or sr >= 0.0


def test_smc_flags_shape_and_short_df():
    # df curto (<15): Nones honestos, nunca exceção
    flags = smc_flags(_df([(100.0, 100.5, 99.5, 100.1)] * 5), "BUY")
    assert flags == {"has_liquidity_sweep": None, "in_premium_discount_zone": None,
                     "has_fvg": None, "has_inducement": None}
    # df suficiente: chaves booleanas ou None (zona pode ser None p/ WAIT)
    rows = [(100 + (i % 8) * 0.3, 100 + (i % 8) * 0.3 + 0.6, 100 + (i % 8) * 0.3 - 0.6,
             100 + (i % 8) * 0.3 + 0.1) for i in range(60)]
    flags2 = smc_flags(_df(rows), "BUY")
    assert set(flags2) == {"has_liquidity_sweep", "in_premium_discount_zone",
                           "has_fvg", "has_inducement"}
    for v in flags2.values():
        assert v in (True, False, None)
    # WAIT: sem direção => tudo None
    assert all(v is None for v in smc_flags(_df(rows), "WAIT").values())
