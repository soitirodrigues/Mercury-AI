"""Sprint 6.1 — LIVE CLOCK INTEGRITY tests (§9: 16 casos obrigatorios).

Nao altera inteligencia.
"""
from datetime import datetime, timezone, timedelta
import pytest

from mercury_ai.operations.m5_incremental.temporal import floor_m5
from mercury_ai.operations.m5_sprint61.live_clock_integrity import (
    MeasurementMode, LiveClockCycleInput, classify_cycle, aggregate_live_clock,
    validate_target_not_future, validate_decision_after_candle_close, validate_before_next_candle,
)
from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_sprint61.live_session61 import Sprint61LiveSession, Sprint61Config
from mercury_ai.config.universe import ALL_SYMBOLS


def _iso(s: str):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# 1 — accelerated nao certifica
def test_accelerated_never_qualifying():
    clock = datetime(2026, 9, 3, 10, 2, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)  # futuro em relacao a clock
    ready = datetime(2026, 9, 3, 10, 5, 20, tzinfo=timezone.utc)
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.ACCELERATED_SOAK, clock, target, ready))
    assert rep.live_clock_qualifying is False
    assert rep.next_candle_result == "NON_QUALIFYING_ACCELERATED"
    assert rep.target_is_future is True  # mesmo futuro, continua accelerated


# 2 — target futuro vira NON_QUALIFYING_FUTURE_TARGET
def test_future_target_non_qualifying():
    clock = datetime(2026, 9, 3, 10, 2, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    ready = datetime(2026, 9, 3, 10, 5, 30, tzinfo=timezone.utc)
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready))
    assert rep.live_clock_qualifying is False
    assert rep.next_candle_result == "NON_QUALIFYING_FUTURE_TARGET"


# 3 — latency negativa nunca PASS
def test_negative_latency_never_pass():
    clock = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    ready = datetime(2026, 9, 3, 10, 4, 0, tzinfo=timezone.utc)  # antes do close
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready))
    assert rep.decision_latency_s < 0
    assert rep.next_candle_result == "NON_QUALIFYING_FUTURE_TARGET"
    assert rep.live_clock_qualifying is False


# 4 — decisao apos close requisito
def test_decision_after_close_requirement():
    clock = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    ready_ok = datetime(2026, 9, 3, 10, 5, 20, tzinfo=timezone.utc)
    ready_bad = datetime(2026, 9, 3, 10, 4, 59, tzinfo=timezone.utc)
    assert validate_decision_after_candle_close(ready_ok, target) is True
    assert validate_decision_after_candle_close(ready_bad, target) is False
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready_ok))
    assert rep.next_candle_result == "QUALIFYING_PASS"
    rep2 = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready_bad))
    assert rep2.next_candle_result == "NON_QUALIFYING_FUTURE_TARGET"


# 5 — decisao antes de N+1 passa
def test_before_next_pass():
    clock = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    ready = datetime(2026, 9, 3, 10, 9, 59, tzinfo=timezone.utc)
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready))
    assert rep.next_candle_result == "QUALIFYING_PASS"
    assert rep.deadline_margin_s == pytest.approx(1, abs=0.5)


# 6 — exatamente em N+1 falha
def test_exactly_at_next_fails():
    clock = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    ready = datetime(2026, 9, 3, 10, 10, 0, tzinfo=timezone.utc)  # == next
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready))
    assert rep.next_candle_result == "QUALIFYING_FAIL"
    assert rep.live_clock_qualifying is True  # qualificavel mas FAIL
    assert rep.deadline_margin_s == pytest.approx(0, abs=0.1)


# 7 — deadline perdido falha
def test_deadline_missed_fail():
    clock = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    target = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    ready = datetime(2026, 9, 3, 10, 10, 1, tzinfo=timezone.utc)
    rep = classify_cycle(LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, target, ready))
    assert rep.next_candle_result == "QUALIFYING_FAIL"
    assert rep.deadline_margin_s < 0


# 8 — LIVE_CLOCK nao avanca target artificialmente (live session prova)
def test_live_clock_no_artificial_advance():
    # Sessao LIVE_CLOCK real com 1 ciclo apenas (nao espera 5m se ja houver fronteira)
    cfg = Sprint61Config(universe_n=4, executor="thread", workers=2, cycles=1, measurement_mode="LIVE_CLOCK")
    sess = Sprint61LiveSession(cfg=cfg)
    out = sess.run()
    assert len(out["cycles"]) == 1
    c = out["cycles"][0]
    # target <= clock_now
    assert c["target_is_future"] is False
    # live_clock_qualifying deve ser True se houve fresh, ou False apenas se sem decisao (nao futuro)
    assert c["measurement_mode"] == "LIVE_CLOCK"
    assert c["next_candle_result"] != "NON_QUALIFYING_FUTURE_TARGET" or c["live_clock_qualifying"] is False


# 9 — restart nao duplica candle (live clock floor vs prev)
def test_restart_no_duplicate():
    from mercury_ai.operations.m5_operational.clock import M5Clock
    m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=m5cfg, disable_profiler=True)
    clock = M5Clock(runner=runner, config=m5cfg)
    r1 = clock.run_cycles_blocking(count=2)
    pre = [x["target_candle"] for x in r1]
    last = datetime.fromisoformat(str(pre[-1]).replace("Z", "+00:00"))
    expected_next = floor_m5(last) + timedelta(minutes=5)
    m5cfg2 = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner2 = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=m5cfg2, disable_profiler=True)
    clock2 = M5Clock(runner=runner2, config=m5cfg2)
    r2 = clock2.run_cycles_blocking(count=2, target_start=expected_next)
    assert r2[0]["target_candle"] == expected_next.isoformat()
    assert r2[0]["target_candle"] not in pre


# 10 — no-overlap permanece
def test_no_overlap_guard():
    m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=m5cfg, disable_profiler=True)
    ok = runner._try_acquire_cycle("held")
    assert ok
    rep = runner.run_cycle(cycle_id="second")
    assert rep.get("status") == "REJECTED_OVERLAP"
    runner._release_cycle()


# 11 — freshness autoridade
def test_freshness_authority():
    cfg = Sprint61Config(universe_n=6, executor="thread", workers=2, cycles=4, measurement_mode="ACCELERATED_SOAK")
    sess = Sprint61LiveSession(cfg=cfg)
    out = sess.run()
    for c in out["cycles"]:
        assert c["stale_as_fresh"] == 0
    assert out["summary"]["stale_as_fresh_total"] == 0


# 12 — erro/timeout nao vira fresh
def test_error_timeout_not_fresh():
    import mercury_ai.operations.m5_operational.runner as rm
    orig = rm._analyze_one_isolated
    syms = ALL_SYMBOLS[:3]

    def flaky(sym, disable_profiler=True):
        if sym == syms[1]:
            raise RuntimeError("injected")
        return orig(sym, disable_profiler=disable_profiler)

    rm._analyze_one_isolated = flaky
    rm._process_worker_entry = flaky
    try:
        m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
        runner = M5OperationalRunner(universe=syms, config=m5cfg, disable_profiler=True)
        rep = runner.run_cycle(cycle_id="err-fresh-s61")
        assert rep["stale_as_fresh"] == 0
        assert rep["per_asset"][syms[1]]["fresh"] is False
    finally:
        rm._analyze_one_isolated = orig
        rm._process_worker_entry = orig


# 13 — determinismo intacto
def test_determinism_intact():
    import tempfile, os, hashlib
    import pandas as pd, numpy as np
    from mercury_ai.data.market_data import MarketDataService
    from mercury_ai.core.analysis_pipeline import AnalysisPipeline
    frozen = {}
    syms = ALL_SYMBOLS[:3]
    for sym in syms:
        for iv in ["1m", "5m", "15m", "1h", "4h"]:
            key = f"{sym}|{iv}"
            seed = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
            rs = np.random.RandomState(seed)
            n_map = {"1m": 600, "5m": 500, "15m": 120, "1h": 60, "4h": 30}
            n = n_map.get(iv, 100)
            base = 100
            closes = base + np.cumsum(rs.randn(n) * base * 0.002)
            highs = closes + np.abs(rs.randn(n) * base * 0.001)
            lows = closes - np.abs(rs.randn(n) * base * 0.001)
            opens = closes + rs.randn(n) * base * 0.0003
            vols = np.abs(rs.randn(n) * 1000) + 500
            idx = pd.date_range("2025-06-01", periods=n, freq={"1m": "1min", "5m": "5min", "15m": "15min", "1h": "1h", "4h": "4h"}[iv], tz="UTC")
            frozen[key] = pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes, "volume": vols}, index=idx)

    class Fp:
        def check_health(self): return True
        def is_available(self): return True
        def supports_symbol(self, s): return True
        def best_provider(self, s): return self
        def get_data(self, symbol, interval="5m", period="5d"): return frozen[f"{symbol}|{interval}"].copy()

    def one():
        sigs = []
        for s in syms:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json"); tmp.write(b"[]"); tmp.close()
            fp = Fp(); ms = MarketDataService(provider=fp)
            pipe = AnalysisPipeline(market_service=ms, providers=[fp], institutional_memory_path=tmp.name)
            pipe.mtf_engine.market_service = ms; pipe.profiler.active = False
            r = pipe.analyze(s); dec = r.decision
            confl = getattr(r, "confluence", None)
            c = getattr(confl, "weighted_score", None) if confl else None
            if c is None and confl: c = getattr(confl, "confluence_score", None)
            sigs.append((s, str(dec.decision), str(dec.grade), round(float(dec.confidence), 6), round(float(c or 0), 2)))
            os.unlink(tmp.name)
        return tuple(sigs)

    a, b, c = one(), one(), one()
    assert a == b == c


# 14 — ranking canonico
def test_ranking_canonical():
    from mercury_ai.operations.ranking import rank_records, FORMULA
    assert "confluence_weighted" in FORMULA
    recs = [{"internal_symbol": "A", "decision": "BUY", "status": "REAL_SIGNAL", "trade_allowed": True, "prob_sum_ok": True, "confidence": 0.7, "confluence": 80, "grade": "B", "buy_probability": 60, "sell_probability": 0, "wait_probability": 40, "audit_id": "a"*64}]
    assert len(rank_records(recs)) == 1


# 15 — accelerated soak funciona para stress
def test_accelerated_soak_stress():
    cfg = Sprint61Config(universe_n=12, executor="thread", workers=4, cycles=6, measurement_mode="ACCELERATED_SOAK")
    sess = Sprint61LiveSession(cfg=cfg)
    out = sess.run()
    assert out["summary"]["total_cycles"] == 6
    assert out["summary"]["stale_as_fresh_total"] == 0
    assert out["summary"]["orphan_workers"] == 0
    # todos NON_QUALIFYING para live (mas soak valido)
    assert out["summary"]["non_qualifying_cycles"] == 6
    assert out["summary"]["live_clock_certification"] == "NON_QUALIFYING"


# 16 — relatorio separa qualifying / non-qualifying
def test_report_separates_qualifying():
    clock = datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
    inputs = [
        LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc), datetime(2026, 9, 3, 10, 5, 20, tzinfo=timezone.utc)),  # PASS
        LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc), datetime(2026, 9, 3, 10, 10, 1, tzinfo=timezone.utc)),  # FAIL
        LiveClockCycleInput(MeasurementMode.LIVE_CLOCK, clock, datetime(2026, 9, 3, 10, 10, tzinfo=timezone.utc), datetime(2026, 9, 3, 10, 5, 30, tzinfo=timezone.utc)),  # future NONQ
    ]
    reps = [classify_cycle(i) for i in inputs]
    agg = aggregate_live_clock(reps)
    assert agg["total_cycles"] == 3
    assert agg["qualifying_live_cycles"] == 2
    assert agg["qualifying_pass"] == 1
    assert agg["qualifying_fail"] == 1
    assert agg["non_qualifying_cycles"] == 1
    assert agg["next_candle_pass_rate"] == pytest.approx(0.5)
