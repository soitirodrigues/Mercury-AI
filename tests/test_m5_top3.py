"""Testes M5 Top-3 (puros, deterministicos, sem rede)."""
import pandas as pd
import numpy as np

from mercury_ai.analysis.institutional_confirmation import (
    closed_df, atr14, detect_liquidity_sweep, detect_displacement,
    detect_fvg, score_setup,
)
from mercury_ai.signals.top3_selector import select_top3
from mercury_ai.signals.m5_alerts import alert_state
from mercury_ai.signals.m5_timing import compute_next_m5, compute_entry_window
from mercury_ai.signals.forward_bias import forward_bias
from mercury_ai.signals.entry_time import (
    countdown_s,
    enrich_top3_oportunidades,
    format_br,
    next_entry_utc,
)
from mercury_ai.data.indicator_engine import IndicatorEngine


def _df(n=60, seed=7):
    rng = np.random.default_rng(seed)
    base = 100 + np.cumsum(rng.normal(0, 0.2, n))
    idx = pd.date_range("2026-09-13 14:00", periods=n, freq="5min", tz="UTC")
    return pd.DataFrame({
        "Open": base, "High": base + 0.3, "Low": base - 0.3,
        "Close": base + 0.05, "Volume": 1000 + np.arange(n) * 5,
    }, index=idx)


def test_closed_excludes_forming():
    df = _df()
    cl = closed_df(df)
    assert len(cl) == len(df) - 1
    assert cl.index[-1] < df.index[-1]


def test_atr_positive():
    assert atr14(closed_df(_df())) > 0


def test_detectors_return_shape():
    cl = closed_df(_df())
    a = atr14(cl)
    for fn in (detect_liquidity_sweep, detect_displacement, detect_fvg):
        r = fn(cl, a)
        assert "detected" in r and "direction" in r


def test_score_gate():
    s = score_setup({"detected": True, "direction": "BULLISH"},
                    {"detected": True, "direction": "BULLISH"},
                    True, True, True, True)
    assert s["score"] == 100.0 and s["pass_gate"] is True
    s2 = score_setup({"detected": False, "direction": "NONE"},
                     {"detected": False, "direction": "NONE"},
                     False, False, False, False)
    assert s2["score"] == 0.0 and s2["pass_gate"] is False


def test_top3_filters_and_caps():
    def e(sym, dec, score, state="VALID", rr=2.5):
        return {"symbol": sym, "decision": dec, "score": score,
                "confidence": 70,
                "signal": {"symbol": sym, "decision": dec, "entry_timing_state": state,
                           "risk_reward": rr, "score": score, "confidence": 70, "confluence": 70}}
    rep = {"top3": [e("A", "BUY", 90), e("B", "SELL", 85), e("C", "BUY", 80),
                    e("D", "BUY", 75), e("W", "WAIT", 99), e("X", "BUY", 95, "EXPIRED"),
                    e("Y", "BUY", 95, "VALID", 1.5), e("Z", "BUY", 60)],
           "ranked": []}
    top3 = select_top3(rep)
    assert len(top3) == 3
    assert [t["symbol"] for t in top3] == ["A", "B", "C"]
    assert all(t["decision"] in ("BUY", "SELL") for t in top3)


def test_alert_window():
    assert alert_state(70.0)["state"] == "EMIT"
    assert alert_state(70.0)["in_window"] is True
    assert alert_state(200.0)["state"] == "WAIT"
    assert alert_state(-5.0)["state"] == "EXPIRED"


def test_timing_strict_ceil():
    nxt = compute_next_m5("2026-09-13T14:30:00+00:00")
    assert nxt == "2026-09-13T14:35:00+00:00"
    w = compute_entry_window("2026-09-13T14:33:50+00:00", nxt)
    assert w["valid"] is True and w["state"] == "VALID"
    w2 = compute_entry_window(nxt, nxt)
    assert w2["valid"] is False and w2["state"] == "EXPIRED"


def test_entry_time_next_m5():
    # Caso do print: sinal 02:52:22 -> entrada 02:55:00Z
    assert next_entry_utc(signal_ts="2026-09-13T02:52:22.061200+00:00") == "2026-09-13T02:55:00+00:00"
    assert next_entry_utc(signal_ts="2026-09-13T02:55:00+00:00") == "2026-09-13T03:00:00+00:00"
    assert next_entry_utc() is None
    assert format_br("2026-09-13T02:55:00+00:00") == "13/09 02:55:00 UTC"
    assert format_br(None) == "--"


def test_enrich_top3_oportunidades():
    ops = [
        {"symbol": "LTC-USD", "decision": "BUY", "score": 72.99,
         "signal_ts": "2026-09-13T02:52:22+00:00"},
        {"symbol": "XRP-USD", "decision": "BUY", "score": 72.93,
         "signal": {"signal_ts": "2026-09-13T02:52:22+00:00"}},
    ]
    out = enrich_top3_oportunidades(ops)
    assert out[0]["entrada_sugerida_utc"] == "2026-09-13T02:55:00+00:00"
    assert out[0]["entrada_sugerida_br"] == "13/09 02:55:00 UTC"
    assert out[1]["entrada_sugerida_utc"] == "2026-09-13T02:55:00+00:00"
    # verbatim: originais intactos
    assert out[0]["symbol"] == "LTC-USD" and out[0]["score"] == 72.99


def _risk_ctx(price, atr, trend, bull_n=3, bear_n=1):
    from mercury_ai.models.market_data import MarketData
    from mercury_ai.models.market_structure import MarketStructure
    from mercury_ai.models.smart_money import SmartMoneyAnalysis
    from mercury_ai.models.market_context import MarketContext
    from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
    from mercury_ai.models.evidence import Evidence
    mkt = MarketData(symbol="T", timeframe="M5", close=price, ema9=price,
                     ema21=price, ema50=price, rsi=50.0, atr=atr, adx=25.0,
                     macd=0.0, macd_signal=0.0, bollinger_upper=price,
                     bollinger_lower=price, volume=1000.0)
    evs = tuple([Evidence("E", f"b{i}", "BULLISH", 70.0, 70.0, "d", 10.0) for i in range(bull_n)] +
                [Evidence("E", f"s{i}", "BEARISH", 70.0, 70.0, "d", 10.0) for i in range(bear_n)])
    ctx = MarketContext(market=mkt, trend=[], price_action=None,
                        support_resistance=None,
                        smart_money=SmartMoneyAnalysis(structure=MarketStructure(trend=trend)),
                        market_state=None, liquidity=None, market_regime=None,
                        mtf_consensus=None, risk_assessment=None)
    return ctx, MarketEvidenceBundle(evidences=evs, timestamp="t", asset="T", timeframe="M5")


def test_f1_risk_side_by_evidence():
    # F1: estrutura BULLISH mas evidências BEARISH -> stop ACIMA (lado SELL)
    from mercury_ai.analysis.risk_engine import RiskEngine
    ctx, bundle = _risk_ctx(100.0, 1.0, "BULLISH", bull_n=1, bear_n=4)
    ra = RiskEngine().assess(ctx, bundle)
    assert ra.suggested_stop > 100.0 and ra.suggested_take_profit < 100.0
    assert ra.risk_reward_ratio == 2.0


def test_f2_ob_carries_direction():
    # F2: OB nunca NEUTRAL (testa OrderBlockEngine direto, sem liquidez)
    from mercury_ai.analysis.smart_money.order_block_engine import OrderBlockEngine
    n = 30
    idx = pd.date_range("2026-09-13 14:00", periods=n, freq="5min", tz="UTC")
    base = 100 + np.arange(n) * 0.5
    df = pd.DataFrame({"Open": base, "High": base + 0.5, "Low": base - 0.3,
                       "Close": base + 0.4, "Volume": 3000,
                       "open": base, "high": base + 0.5, "low": base - 0.3,
                       "close": base + 0.4, "volume": 3000}, index=idx)
    ob = OrderBlockEngine().analyze(df)
    if ob is not None:
        assert ob.direction in ("BULLISH", "BEARISH")


def test_f3_fvg_ignores_spread_noise():
    # F3: micro-gap de spread não é FVG
    from mercury_ai.analysis.fair_value_gap_engine import FairValueGapEngine
    from mercury_ai.core.pipeline_executor import PipelineExecutor
    idx = pd.date_range("2026-09-13 14:00", periods=5, freq="5min", tz="UTC")
    df = pd.DataFrame({"Open": [100, 100, 100.00001, 100, 100],
                       "High": [101, 101, 101.00001, 101, 101],
                       "Low": [99, 99, 99.00001, 99, 99],
                       "Close": [100.5, 100.5, 100.50001, 100.5, 100.5]},
                      index=idx)
    res = FairValueGapEngine(PipelineExecutor()).analyze(df)
    assert not res.is_bullish_fvg and not res.is_bearish_fvg


def test_f4_adx_real_trend():
    # F4: ADX de Wilder detecta tendência (antes sempre 0.0)
    n = 60
    idx = pd.date_range("2026-09-13 14:00", periods=n, freq="5min", tz="UTC")
    base = 100 + np.arange(n) * 0.5
    df = pd.DataFrame({"open": base, "high": base + 0.4, "low": base - 0.2,
                       "close": base + 0.3, "volume": 1000}, index=idx)
    adx = IndicatorEngine().calculate(df)["adx"]
    assert adx > 20.0


def test_f7_top3_requires_forward_confirmed():
    # F7: WEAK/EXPIRED nunca entra no Top-3
    def e(sym, fwd):
        return {"symbol": sym, "decision": "BUY", "score": 95, "confidence": 90,
                "signal": {"symbol": sym, "decision": "BUY", "entry_timing_state": "VALID",
                           "forward_state": fwd, "risk_reward": 2.5, "score": 95,
                           "confidence": 90, "confluence": 90}}
    rep = {"top3": [e("A", "WEAK"), e("B", "EXPIRED"), e("C", "CONFIRMED")], "ranked": []}
    top3 = select_top3(rep)
    assert [t["symbol"] for t in top3] == ["C"]


def test_forward_bias_states():
    n = 30
    idx = pd.date_range("2026-09-13 14:00", periods=n, freq="5min", tz="UTC")
    base = 100 + np.arange(n) * 0.3
    df = pd.DataFrame({"Open": base, "High": base + 0.4, "Low": base - 0.2,
                       "Close": base + 0.25, "Volume": 1000}, index=idx)
    assert forward_bias(df, "BUY")["state"] == "CONFIRMED"
    assert forward_bias(df, "SELL")["state"] == "EXPIRED"
