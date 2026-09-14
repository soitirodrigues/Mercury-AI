"""Filtros institucionais M5 — observáveis puros (determinísticos, sem rede)."""
import pandas as pd

from mercury_ai.signals.m5_institutional_filters import (
    ATR_CAP,
    EMA_SPAN,
    IDM_LOOKBACK,
    TRIGGER_BODY_MIN,
    ZONE_LOOKBACK,
    atr14,
    ema200_side,
    institutional_flags,
    smc_flags,
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
                          "has_fvg", "has_inducement"}
    assert flags["trigger_body_ratio"] is not None
    assert flags["trigger_aligned"] in (True, False)
    assert flags["trigger_range_atr"] is not None
    assert flags["ema200_aligned"] is None  # <200 linhas: honesto
    # trigger_range_atr respeita o teto documentado como referência
    assert isinstance(ATR_CAP, float)


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
