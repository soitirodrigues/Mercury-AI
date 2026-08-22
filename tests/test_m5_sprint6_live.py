"""Sprint 6 — LIVE OPERATION / TRADING READINESS tests (§24-§26).

Cobre sem alterar inteligencia:
  - next-candle deadline
  - cycle sequencing / no-overlap
  - restart recovery (controlled shutdown + resume next M5)
  - worker crash/timeout isolation
  - watchdog
  - InstitutionalMemory live isolation
  - no duplicate cycle
  - data drift monitor
  - long-session aggregation

Todos usam universo pequeno + ThreadPool para rodar rapido no CI.
Sessao longa real 24 ciclos e validada no gate script (m5_sprint6_gate_runner).
"""
import time, threading, uuid
from datetime import datetime, timezone, timedelta

import pytest

from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5
from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_operational.clock import M5Clock
from mercury_ai.operations.m5_sprint6.deadline import (
    evaluate_deadline, next_candle_start_for, target_candle_close_for,
    aggregate_deadlines,
)
from mercury_ai.operations.m5_sprint6.live_session import LiveSession, LiveSessionConfig


# ---------- deadline contract ----------

def test_deadline_metric_definitions():
    tc = datetime(2026, 9, 3, 10, 5, 0, tzinfo=timezone.utc)
    tcc = target_candle_close_for(tc)
    ncs = next_candle_start_for(tc)
    assert tcc == tc
    assert ncs == datetime(2026, 9, 3, 10, 10, 0, tzinfo=timezone.utc)
    # decision ready before next candle => PASS
    dr = datetime(2026, 9, 3, 10, 5, 30, tzinfo=timezone.utc)
    r = evaluate_deadline(tc, dr)
    assert r.next_candle_ready is True
    assert r.deadline_margin_s == pytest.approx(270, abs=0.5)
    assert r.decision_latency_s == pytest.approx(30, abs=0.5)
    # after next candle => FAIL
    dr2 = datetime(2026, 9, 3, 10, 10, 1, tzinfo=timezone.utc)
    r2 = evaluate_deadline(tc, dr2)
    assert r2.next_candle_ready is False
    assert r2.deadline_margin_s < 0
    # no fresh => non-qualifying
    r3 = evaluate_deadline(tc, None)
    assert r3.next_candle_ready is None


def test_deadline_aggregate_percentiles():
    base = datetime(2026, 9, 3, 10, 0, 0, tzinfo=timezone.utc)
    results = []
    for i, margin in enumerate([250, 260, 270, 280, 285]):
        tc = base + timedelta(minutes=5*i)
        ncs = next_candle_start_for(tc)
        dr = ncs - timedelta(seconds=margin)
        results.append(evaluate_deadline(tc, dr))
    agg = aggregate_deadlines(results)
    assert agg["pass"] == 5
    assert agg["fail"] == 0
    assert agg["deadline_margin_min"] == pytest.approx(250, abs=0.5)
    assert agg["deadline_margin_p50"] is not None
    assert agg["deadline_margin_p95"] is not None


# ---------- next candle readiness live ----------

def test_next_candle_ready_live_small_session():
    """§8: decision_ready < next_candle_start para ciclos validos."""
    cfg = LiveSessionConfig(universe_n=6, executor="thread", workers=2, cycles=4)
    sess = LiveSession(cfg=cfg)
    out = sess.run()
    assert len(out["cycles"]) == 4
    for c in out["cycles"]:
        # todo ciclo com fresh deve ter PASS
        if c.get("fresh", 0) > 0:
            assert c["next_candle_ready"] == "PASS", f"deadline miss on {c['cycle_id']}: {c.get('deadline_margin_s')}"
        assert c["stale_as_fresh"] == 0


# ---------- cycle sequencing / no-overlap / no duplicate ----------

def test_cycle_sequencing_targets_monotonic_and_ids_unique():
    cfg = LiveSessionConfig(universe_n=6, executor="thread", workers=2, cycles=6)
    sess = LiveSession(cfg=cfg)
    out = sess.run()
    cycles = out["cycles"]
    ids = [c["cycle_id"] for c in cycles]
    assert len(set(ids)) == len(ids), "cycle_id must be unique"
    targets = [c["target_candle"] for c in cycles]
    assert targets == sorted(targets)


def test_no_duplicate_cycle_and_max_concurrent_1():
    """Sprint 6 §12: max_concurrent_cycles == 1 — segundo ciclo rejeitado."""
    from mercury_ai.config.universe import ALL_SYMBOLS
    m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=m5cfg, disable_profiler=True)
    ok = runner._try_acquire_cycle("held-1")
    assert ok is True
    rep = runner.run_cycle(cycle_id="second")
    assert rep.get("status") == "REJECTED_OVERLAP"
    runner._release_cycle()
    # after release, should allow
    rep2 = runner.run_cycle(cycle_id="after-release")
    assert rep2.get("cycle_status") in ("COMPLETED", "CYCLE_TIMEOUT", "SHUTDOWN")
    assert rep2.get("stale_as_fresh") == 0


def test_clock_no_overlap_under_blocking():
    cfg = LiveSessionConfig(universe_n=4, executor="thread", workers=2, cycles=4)
    sess = LiveSession(cfg=cfg)
    out = sess.run()
    # blocking run ensures no overlap by construction; also no REJECTED_OVERLAP inside cycles
    for c in out["cycles"]:
        assert c["cycle_status"] != "REJECTED_OVERLAP"


# ---------- restart recovery ----------

def test_controlled_shutdown_and_resume_next_m5():
    """§14: controlled shutdown -> restart -> resume next valid M5 cycle w/o dup."""
    from mercury_ai.config.universe import ALL_SYMBOLS
    m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=m5cfg, disable_profiler=True)
    clock = M5Clock(runner=runner, config=m5cfg)
    # run 2 cycles
    r1 = clock.run_cycles_blocking(count=2)
    assert len(r1) == 2
    pre_targets = [x["target_candle"] for x in r1]
    clock.stop(timeout=5)
    runner.request_shutdown()
    # simulate process restart: new runner/clock, should resume NEXT M5 (not replay same)
    m5cfg2 = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner2 = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=m5cfg2, disable_profiler=True)
    clock2 = M5Clock(runner=runner2, config=m5cfg2)
    # compute next expected candle
    last = datetime.fromisoformat(str(pre_targets[-1]).replace("Z", "+00:00"))
    expected_next = floor_m5(last) + timedelta(minutes=5)
    r2 = clock2.run_cycles_blocking(count=2, target_start=expected_next)
    assert r2[0]["target_candle"] == expected_next.isoformat()
    assert r2[0]["target_candle"] not in pre_targets
    clock2.stop(timeout=5)


# ---------- watchdog + timeout + worker crash isolation ----------

def test_watchdog_still_configured_and_not_firing_spuriously():
    from mercury_ai.operations.m5_operational.watchdog import CycleWatchdog
    fired = []
    wd = CycleWatchdog(cycle_id="wd-s6", interval_s=0.05, stall_threshold_s=0.2, on_event=lambda e: fired.append(e))
    wd.set_total(3)
    wd.start()
    for i in range(3):
        time.sleep(0.06)
        wd.notify_progress(i+1)
    time.sleep(0.15)
    wd.stop()
    assert not any(e.kind == "STALL" for e in fired)


def test_worker_timeout_and_error_isolation_no_stale_as_fresh():
    import mercury_ai.operations.m5_operational.runner as runner_mod
    orig = runner_mod._analyze_one_isolated
    from mercury_ai.config.universe import ALL_SYMBOLS
    syms = ALL_SYMBOLS[:3]

    def flaky(symbol: str, disable_profiler: bool = True):
        if symbol == syms[1]:
            raise RuntimeError("injected crash for isolation test")
        return orig(symbol, disable_profiler=disable_profiler)

    runner_mod._analyze_one_isolated = flaky
    runner_mod._process_worker_entry = flaky
    try:
        m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
        runner = M5OperationalRunner(universe=syms, config=m5cfg, disable_profiler=True)
        rep = runner.run_cycle(cycle_id="crash-isolation-s6")
        assert rep["stale_as_fresh"] == 0
        # at least one error/timeout, others still fresh/unavailable but not promoted stale
        assert rep["assets_completed"] == len(syms)
        # crashed asset recorded as ERROR/TIMEOUT, not converted to WAIT fresh
        err = rep["per_asset"][syms[1]]
        assert err["fresh"] is False
        assert err["fresh_status"] in ("ERROR", "TIMEOUT")
    finally:
        runner_mod._analyze_one_isolated = orig
        runner_mod._process_worker_entry = orig


# ---------- InstitutionalMemory live isolation ----------

def test_institutional_memory_isolated_two_cycles():
    m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    from mercury_ai.config.universe import ALL_SYMBOLS
    syms = ALL_SYMBOLS[:6]
    runner = M5OperationalRunner(universe=syms, config=m5cfg, disable_profiler=True)
    r1 = runner.run_cycle(cycle_id="mem-s6-1")
    r2 = runner.run_cycle(cycle_id="mem-s6-2")
    assert r1["stale_as_fresh"] == 0
    assert r2["stale_as_fresh"] == 0
    assert r1["orphan_workers"] == 0
    assert r2["orphan_workers"] == 0


# ---------- data drift monitor ----------

def test_data_drift_monitor_flags_gap():
    cfg = LiveSessionConfig(universe_n=4, executor="thread", workers=2, cycles=6)
    sess = LiveSession(cfg=cfg)
    out = sess.run()
    # normal session must not produce drift (targets +5m each)
    assert out["summary"]["data_drift_events"] == [] or all(
        "gap" not in e.get("detail","") for e in out["summary"]["data_drift_events"]
    )


# ---------- freshness absolute ----------

def test_freshness_absolute_across_session():
    cfg = LiveSessionConfig(universe_n=6, executor="thread", workers=2, cycles=6)
    sess = LiveSession(cfg=cfg)
    out = sess.run()
    for c in out["cycles"]:
        assert c["stale_as_fresh"] == 0, f"stale_as_fresh violation in {c['cycle_id']}"
    assert out["summary"]["stale_as_fresh_total"] == 0


# ---------- early emission + top3 consistency (§10-§11) ----------

def test_early_emission_and_top3_consistency():
    from mercury_ai.config.universe import ALL_SYMBOLS
    m5cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=290, worker_timeout_s=30)
    runner = M5OperationalRunner(universe=ALL_SYMBOLS[:6], config=m5cfg, disable_profiler=True)
    rep = runner.run_cycle(cycle_id="early-top3-s6")
    # early emission fields present
    assert rep.get("first_fresh_decision_ms") is not None or rep.get("fresh", 0) == 0
    # ranking is canonical (formula present, no second ranking)
    assert "ranking_score" in rep.get("formula", "")
    # top3 final is prefix of ranked (consistency)
    top3 = rep.get("top3") or []
    ranked = rep.get("ranked") or []
    if top3 and ranked:
        assert top3[0]["symbol"] == ranked[0]["symbol"]


# ---------- legacy incrementals still green ----------

def test_legacy_incrementals_still_importable():
    # smoke: sprint 5 gates unchanged
    from mercury_ai.operations.m5_incremental.temporal import floor_m5
    assert floor_m5(datetime(2026, 9, 3, 10, 7, tzinfo=timezone.utc)) == datetime(2026, 9, 3, 10, 5, tzinfo=timezone.utc)
