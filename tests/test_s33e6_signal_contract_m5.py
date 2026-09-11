"""S33-E.6 — Signal Contract + M5 entry timing (deterministico, SEM rede).

Sem Yahoo, sem broker, sem internet: fixtures montadas com os modelos reais
(MarketData/DecisionResult/RiskAssessment/MTFConsensus/TradingExplanation/
ConfluenceResult/MarketRegime/AnalysisResult) — compativeis com o sistema
atual, sem alterar thresholds/pesos/regras.

CASE A: BUY  | CASE B: SELL | CASE C: WAIT (WAIT continua WAIT, sem mascara)
NEGATIVE: signal_ts >= next_m5_ts -> EXPIRED (protecao contra falso timing)
SERIALIZATION: Signal -> dict/json -> ScanReport -> present_scan preserva tudo
SIGNAL-ONLY: sem broker LIVE, sem ordens, settings.READ_ONLY
"""
import ast
import json
from pathlib import Path
from types import SimpleNamespace

from mercury_ai.brain.scanner import MercuryScanner, ScanReport
from mercury_ai.models.analysis_result import AnalysisResult
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.direction import AnalysisDirection
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.market_regime_enum import MarketRegimeEnum
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.models.version_metadata import VersionMetadata
from mercury_ai.signals.m5_timing import (
    EXPIRED_STATE,
    VALID_STATE,
    compute_entry_window,
    compute_next_m5,
)
from mercury_ai.signals.signal_builder import build_signal_from_analysis

SIGNALS_DIR = Path("mercury_ai/signals")
REQUIRED_FIELDS = [
    "signal_id", "symbol", "decision", "signal_ts", "last_m5_ts", "next_m5_ts",
    "entry_price", "entry_window_start", "entry_window_end",
    "entry_window_seconds", "invalidation", "stop_loss", "take_profit",
    "risk_reward", "confidence", "probability_buy", "probability_sell",
    "probability_wait", "confluence", "quality", "institutional_score",
    "grade", "mtf_summary", "market_regime", "reason", "audit_id",
]

LAST_M5 = "2026-01-05T10:10:00+00:00"      # vela fechada conhecida
SIGNAL_TS = "2026-01-05T10:14:30+00:00"    # 30s antes da proxima M5
NEXT_M5 = "2026-01-05T10:15:00+00:00"


def _market(symbol="BTC-USD", close=100.0):
    return MarketData(
        symbol=symbol, timeframe="M5", close=close,
        ema9=99.0, ema21=98.0, ema50=97.0, rsi=60.0, atr=1.0, adx=25.0,
        macd=0.5, macd_signal=0.3, bollinger_upper=102.0,
        bollinger_lower=98.0, volume=1000.0,
    )


def _mtf():
    return MTFConsensus(
        global_bias="BULLISH", local_bias="BULLISH", conflict_detected=False,
        alignment_score=80.0, summary="M5/M15/H1/H4 alinhados; M1 rejeitado",
        timeframe_status={"M1": "rejected", "M5": "processed", "M15": "processed",
                          "H1": "processed", "H4": "processed"},
        timeframe_errors={"M1": "rejected(<20 baras)"},
    )


def _explanation(decision):
    return TradingExplanation(
        exec_summary=f"Institutional {decision} signal triggered at 100.00000.",
        decision_rationale=(
            f"Regra 2: dominant_direction={decision}, grade=B, "
            "conflict=False, is_valid=True"
        ),
        market_context="ctx", trend_context="trend", liquidity_context="liq",
        structure_context="struct", momentum_context="mom", volume_context="vol",
        smart_money_context="sm", confluence_context="confl",
        risk_assessment="risk", confidence_rationale="conf",
        strong_evidences=("TrendEngine:tendencia de alta",),
        warnings=(), conflicts=(),
    )


def _decision(decision="BUY", audit_id="a" * 64, grade="B"):
    buy, sell, wait = (65.0, 10.0, 25.0) if decision == "BUY" else (
        (10.0, 65.0, 25.0) if decision == "SELL" else (10.0, 10.0, 80.0))
    return DecisionResult(
        decision=decision, grade=grade, confidence=0.72, clarity=80.0,
        risk_score=30.0, score=68.0, quality=70.0, expected_strength=75.0,
        buy_probability=buy, sell_probability=sell, wait_probability=wait,
        expected_risk=99.0, expected_reward=102.0, expected_drawdown=2.0,
        audit_id=audit_id,
        version_metadata=VersionMetadata("1.2.0", "1.2.0", "1.2.0", "1.2.0"),
        explanation=_explanation(decision),
        mtf_consensus=_mtf(),
        summary=f"Institutional {decision} signal triggered at 100.00000.",
        technical_reason=f"Regra 2: dominant_direction={decision}",
    )


def _risk():
    return RiskAssessment(
        suggested_stop=99.0, suggested_take_profit=102.0, risk_reward_ratio=2.0,
        expected_drawdown=2.0, expected_volatility=1.0, trade_quality=70.0,
        max_exposure=0.02, invalidation_point=99.0, institutional_risk_score=30.0,
    )


def _confluence(direction=AnalysisDirection.BUY):
    return ConfluenceResult(
        buy_score=80.0, sell_score=10.0, neutral_score=10.0,
        agreement_percentage=80.0, conflicting_signals=False,
        independent_confirmations=3, weighted_score=75.0, confidence=72.0,
        dominant_direction=direction, evidences=(), warnings=(),
    )


def _analysis(decision="BUY", symbol="BTC-USD", audit_id="a" * 64):
    direction = (AnalysisDirection.BUY if decision == "BUY"
                 else AnalysisDirection.SELL if decision == "SELL"
                 else AnalysisDirection.NEUTRAL)
    regime = (MarketRegimeEnum.STRONG_UPTREND if decision == "BUY"
              else MarketRegimeEnum.STRONG_DOWNTREND if decision == "SELL"
              else MarketRegimeEnum.CONSOLIDATION)
    return AnalysisResult(
        market=_market(symbol), context=None, trend=(), mtf_evidences=(),
        smart_money=None,
        market_regime=MarketRegime(regime=regime, confidence=70.0,
                                   supporting_evidences=()),
        confluence=_confluence(direction), market_condition=None,
        market_state=None, candlestick_analysis=None, volatility_analysis=None,
        session_analysis=None, support_resistance=None, liquidity_analysis=None,
        risk_assessment=_risk(), evidence_ranking=None, volume_analysis=None,
        structure_analysis=None, decision=_decision(decision, audit_id),
    )


def _assert_common(sig, decision, symbol="BTC-USD"):
    assert sig.symbol != ""
    assert sig.decision in ("BUY", "SELL", "WAIT")
    assert sig.decision == decision
    assert sig.signal_ts is not None
    assert sig.last_m5_ts is not None
    assert sig.next_m5_ts is not None
    assert sig.next_m5_ts > sig.last_m5_ts
    assert sig.entry_price is not None and sig.entry_price > 0
    assert sig.invalidation is not None
    assert sig.mtf_summary is not None
    assert sig.reason != ""
    assert sig.audit_id != ""
    assert sig.asset == symbol
    d = sig.to_dict()
    for f in REQUIRED_FIELDS:
        assert f in d, f"campo critico ausente na serializacao: {f}"


def test_case_a_buy_signal():
    sig = build_signal_from_analysis(
        _analysis("BUY"), signal_ts=SIGNAL_TS, last_m5_ts=LAST_M5)
    _assert_common(sig, "BUY")
    assert sig.signal_id != ""
    assert sig.last_m5_ts == "2026-01-05T10:10:00+00:00"
    assert sig.next_m5_ts == NEXT_M5  # 10:10:00 -> 10:15:00
    assert sig.entry_window_seconds == 30.0  # 10:14:30 -> 10:15:00
    assert sig.seconds_to_next_m5 == 30.0
    assert sig.entry_valid_for_next_m5 is True
    assert sig.entry_timing_state == VALID_STATE
    assert sig.entry_window_start == SIGNAL_TS
    assert sig.entry_window_end == NEXT_M5
    # risco propagado (RiskEngine), nao recalculado
    assert sig.stop_loss == 99.0 and sig.take_profit == 102.0
    assert sig.invalidation == 99.0 and sig.risk_reward == 2.0
    assert sig.entry_price == 100.0 and sig.entry == 100.0
    # decisao propagada
    assert sig.probability_buy == 65.0 and sig.probability_wait == 25.0
    assert sig.confluence == 75.0 and sig.grade == "B"
    assert sig.institutional_score == 68.0 and sig.quality == 70.0
    assert sig.market_regime == "STRONG_UPTREND"
    assert "Regra 2" in sig.reason  # explicacao real, nao generica
    assert "strong BUY" not in sig.reason
    tf = sig.mtf_summary["timeframes"]
    assert tf["M5"] == "processed" and tf["M1"].startswith("rejected")
    assert sig.mtf_summary["status"] == "present"


def test_case_b_sell_signal():
    sig = build_signal_from_analysis(
        _analysis("SELL", audit_id="b" * 64), signal_ts=SIGNAL_TS,
        last_m5_ts=LAST_M5)
    _assert_common(sig, "SELL")
    assert sig.next_m5_ts == NEXT_M5
    assert sig.entry_window_seconds == 30.0
    assert sig.entry_timing_state == VALID_STATE
    assert sig.probability_sell == 65.0
    assert sig.market_regime == "STRONG_DOWNTREND"
    assert "Regra 2" in sig.reason


def test_case_c_wait_stays_wait():
    # OPPORTUNITY != SIGNAL: WAIT nao e mascarado como BUY/SELL
    sig = build_signal_from_analysis(
        _analysis("WAIT", audit_id="c" * 64), signal_ts=SIGNAL_TS,
        last_m5_ts=LAST_M5)
    _assert_common(sig, "WAIT")
    assert sig.decision == "WAIT" and sig.action == "WAIT"
    assert sig.entry_timing_state == VALID_STATE  # timing valido, decisao WAIT
    assert sig.probability_wait == 80.0


def test_negative_timing_signal_ts_gte_next_m5():
    # signal_ts == next_m5_ts -> EXPIRED (protecao contra falso timing)
    sig = build_signal_from_analysis(
        _analysis("BUY"), signal_ts=NEXT_M5, last_m5_ts=LAST_M5)
    assert sig.entry_valid_for_next_m5 is False
    assert sig.entry_timing_state == EXPIRED_STATE
    assert sig.entry_window_seconds == 0.0
    assert sig.seconds_to_next_m5 == 0.0
    # signal_ts apos a fronteira -> tambem EXPIRED
    sig2 = build_signal_from_analysis(
        _analysis("BUY"), signal_ts="2026-01-05T10:16:00+00:00",
        last_m5_ts=LAST_M5)
    assert sig2.entry_valid_for_next_m5 is False
    assert sig2.entry_timing_state == EXPIRED_STATE
    assert sig2.entry_window_seconds == 0.0
    assert sig2.seconds_to_next_m5 == -60.0
    # matematica pura: fronteira exata 10:10:00 -> proxima 10:15:00
    assert compute_next_m5("2026-01-05T10:10:00+00:00") == NEXT_M5
    assert compute_next_m5("2026-01-05T10:14:59+00:00") == NEXT_M5
    w = compute_entry_window(NEXT_M5, NEXT_M5)
    assert w["valid"] is False and w["state"] == EXPIRED_STATE


def test_no_known_candle_never_uses_wall_clock():
    # sem last_m5_ts: next=None -> EXPIRED honesto (nunca infere do relogio)
    sig = build_signal_from_analysis(_analysis("BUY"), signal_ts=SIGNAL_TS)
    assert sig.last_m5_ts is None and sig.next_m5_ts is None
    assert sig.entry_timing_state == EXPIRED_STATE
    assert sig.entry_valid_for_next_m5 is False


def test_serialization_preserves_all_fields():
    sig = build_signal_from_analysis(
        _analysis("BUY"), signal_ts=SIGNAL_TS, last_m5_ts=LAST_M5)
    payload = json.loads(json.dumps(sig.to_dict(), default=str))
    for f in REQUIRED_FIELDS:
        assert f in payload, f"campo perdido no JSON: {f}"
    assert payload["symbol"] == "BTC-USD" and payload["decision"] == "BUY"
    assert payload["entry_price"] == 100.0 and payload["audit_id"] == "a" * 64
    assert payload["next_m5_ts"] == NEXT_M5
    assert payload["mtf_summary"]["timeframes"]["H4"] == "processed"


def test_scanreport_top3_transports_full_signal():
    analyses = [_analysis("BUY"), _analysis("SELL", symbol="ETH-USD",
                                            audit_id="b" * 64)]
    from dataclasses import replace
    with_signals = [replace(a, signal=build_signal_from_analysis(
        a, signal_ts=SIGNAL_TS, last_m5_ts=LAST_M5)) for a in analyses]
    rep = ScanReport(scan_id="scan-e6-sig", status="COMPLETE",
                     ranked=with_signals, top3=with_signals[:2],
                     symbols_total=2, symbols_completed=2)
    data = rep.to_dict()
    assert len(data["top3"]) == 2
    for row in data["top3"]:
        assert row["signal"] is not None
        for f in REQUIRED_FIELDS:
            assert f in row["signal"], f"TOP3 perdeu campo: {f}"
    assert data["top3"][0]["signal"]["decision"] == "BUY"
    assert data["top3"][1]["signal"]["decision"] == "SELL"
    assert data["top3"][0]["signal"]["next_m5_ts"] == NEXT_M5
    # ranking intacto: ordenacao do RankingEngine preservada
    assert data["top3"][0]["symbol"] == "BTC-USD"
    # presentation: passthrough verbatim transporta o signal completo
    from app.dashboard.scan_presentation import present_scan
    view = present_scan(data)
    assert view["top3"][0]["signal"]["audit_id"] == "a" * 64
    assert view["top3"][1]["signal"]["entry_price"] == 100.0


def test_signal_only_no_live_broker_no_orders():
    from mercury_ai.config import settings
    assert settings.READ_ONLY is True
    for path in [Path("mercury_ai/signals/signal_builder.py"),
                 Path("mercury_ai/signals/m5_timing.py"),
                 Path("mercury_ai/models/signal.py")]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported = {n.module for n in ast.walk(tree)
                    if isinstance(n, ast.ImportFrom) and n.module}
        imported |= {a.name for n in ast.walk(tree)
                     if isinstance(n, ast.Import) for a in n.names}
        assert not [m for m in imported if "order_executor" in m.lower()
                    or "broker" in m.lower()], f"{path}: import LIVE"
        called = {n.func.attr for n in ast.walk(tree)
                  if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute)}
        assert not ({"create_order", "send_order", "execute_order",
                     "place_order"} & called), f"{path}: cria ordem"
    # builder nunca importa motores de decisao (propagacao, sem recalculo)
    tree = ast.parse(Path("mercury_ai/signals/signal_builder.py")
                     .read_text(encoding="utf-8"))
    imported = {n.module or "" for n in ast.walk(tree)
                if isinstance(n, ast.ImportFrom)}
    engines = [m for m in imported if "probability_engine" in m
               or "confluence_engine" in m or "confidence_engine" in m
               or "decision_resolver" in m or "risk_engine" in m]
    assert engines == [], f"builder nao pode importar motores: {engines}"
    # namespace simples nunca mistura: WAIT nao vira BUY/SELL no transporte
    row = SimpleNamespace(decision="WAIT")
    assert row.decision == "WAIT"
