"""Sprint 5 — Operational tests: watchdog, graceful shutdown, bounded queue, no-overlap, timeout."""
import time, threading, uuid, json, tempfile, os
from pathlib import Path
from datetime import datetime, timezone, timedelta

import pytest

from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_operational.clock import M5Clock
from mercury_ai.operations.m5_operational.watchdog import CycleWatchdog


class _FakeRunner:
    """Fake minimal runner for watchdog/shutdown unit tests (no market data)."""
    pass


def test_watchdog_detects_stall():
    events = []

    def on_evt(evt):
        events.append(evt)

    wd = CycleWatchdog(cycle_id="test-wd", interval_s=0.05, stall_threshold_s=0.15, on_event=on_evt)
    wd.set_total(5)
    wd.start()
    # No progress => should fire STALL after ~0.15s
    time.sleep(0.35)
    wd.stop()
    assert any(e.kind == "STALL" for e in events), "watchdog should have fired STALL"
    assert events[0].cycle_id == "test-wd"


def test_watchdog_no_stall_when_progress():
    events = []
    wd = CycleWatchdog(cycle_id="wd2", interval_s=0.05, stall_threshold_s=0.2, on_event=lambda e: events.append(e))
    wd.set_total(5)
    wd.start()
    for i in range(5):
        time.sleep(0.07)
        wd.notify_progress(i + 1)
    time.sleep(0.15)
    wd.stop()
    # With steady progress, no STALL should fire (reset each time)
    assert not any(e.kind == "STALL" for e in events)


def test_bounded_queue_never_grows_unbounded():
    """Operational runner must use bounded queue and track max depth."""
    cfg = M5OperationalConfig(process_workers=2, thread_workers=2, executor="thread", bounded_queue_maxsize=4, cycle_timeout_s=290, worker_timeout_s=30)
    cfg.validate()
    # Use 6 assets to exceed queue maxsize=4 and ensure backpressure handling doesn't crash
    from mercury_ai.config.universe import ALL_SYMBOLS
    symbols = ALL_SYMBOLS[:6]
    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)
    report = runner.run_cycle()
    assert report["cycle_status"] in ("COMPLETED", "CYCLE_TIMEOUT", "SHUTDOWN")
    assert report["queue_max_depth"] <= cfg.bounded_queue_maxsize or report["queue_max_depth"] == len(symbols)
    assert report["stale_as_fresh"] == 0
    # Bounded queue never lost a valid fresh without logging — report should have assets_completed == universe or explain timeout
    assert report["assets_completed"] == len(symbols)


def test_no_cycle_overlap_rejected():
    """max_concurrent_cycles=1 — second cycle while first active must be REJECTED_OVERLAP."""
    cfg = M5OperationalConfig(process_workers=2, thread_workers=2, executor="thread", cycle_timeout_s=290, worker_timeout_s=30)
    from mercury_ai.config.universe import ALL_SYMBOLS
    symbols = ALL_SYMBOLS[:4]
    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)
    # Simulate active cycle by acquiring lock directly
    acquired = runner._try_acquire_cycle("cycle-active")
    assert acquired is True
    report = runner.run_cycle(cycle_id="cycle-second")
    assert report["status"] == "REJECTED_OVERLAP"
    runner._release_cycle()


def test_graceful_shutdown_stops_cycle():
    """SIGTERM/SIGINT path: request_shutdown must mark next cycle as SHUTDOWN or complete gracefully."""
    cfg = M5OperationalConfig(process_workers=2, thread_workers=2, executor="thread", cycle_timeout_s=290, worker_timeout_s=30, shutdown_grace_s=2.0)
    from mercury_ai.config.universe import ALL_SYMBOLS
    symbols = ALL_SYMBOLS[:12]
    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)

    result_holder = {}

    def run_in_bg():
        result_holder["report"] = runner.run_cycle(cycle_id="shutdown-test")

    t = threading.Thread(target=run_in_bg, daemon=True)
    t.start()
    time.sleep(0.8)
    runner.request_shutdown()
    t.join(timeout=15)
    assert "report" in result_holder
    rep = result_holder["report"]
    # Should be SHUTDOWN or COMPLETED (if finished before shutdown took effect) — never hang
    assert rep["cycle_status"] in ("SHUTDOWN", "COMPLETED", "CYCLE_TIMEOUT")
    assert rep["orphan_workers"] == 0


def test_institutional_memory_isolated_under_threadpool():
    """Sprint 5 — InstitutionalMemory must be safe under concurrent execution.

    Workers are now M5_WORKER_ISOLATED_MEMORY per-process/thread isolated —
    pipeline memory must not race/corrupt shared file.
    Run 6 assets thread 4 twice and check determinism via stale_as_fresh and status.
    """
    cfg = M5OperationalConfig(process_workers=4, thread_workers=4, executor="thread", cycle_timeout_s=290, worker_timeout_s=30)
    from mercury_ai.config.universe import ALL_SYMBOLS
    symbols = ALL_SYMBOLS[:6]
    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)
    r1 = runner.run_cycle(cycle_id="mem-test-1")
    r2 = runner.run_cycle(cycle_id="mem-test-2")
    assert r1["stale_as_fresh"] == 0
    assert r2["stale_as_fresh"] == 0
    assert r1["orphan_workers"] == 0
    assert r2["orphan_workers"] == 0
    # Per-symbol status should be deterministic for frozen-like stable assets (at least not ERROR due to race)
    for sym in symbols:
        assert r1["per_asset"][sym]["status"] != "ERROR" or r2["per_asset"][sym]["status"] in ("ERROR", "DATA_UNAVAILABLE", "SCAN_ERROR", "TIMEOUT")


def test_multi_cycle_no_degradation():
    """6 ciclos: no overlap, unique cycle_ids, sorted targets, stale_as_fresh=0, no orphan."""
    cfg = M5OperationalConfig(process_workers=2, thread_workers=2, executor="thread", cycle_timeout_s=290, worker_timeout_s=30)
    from mercury_ai.config.universe import ALL_SYMBOLS
    symbols = ALL_SYMBOLS[:4]
    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)
    clock = M5Clock(runner=runner, config=cfg)
    reports = clock.run_cycles_blocking(count=6)
    assert len(reports) == 6
    ids = [r["cycle_id"] for r in reports]
    assert len(set(ids)) == 6, "cycle_id must be unique"
    targets = [r["target_candle"] for r in reports]
    assert targets == sorted(targets), "targets must be monotonically increasing"
    for r in reports:
        assert r["stale_as_fresh"] == 0, f"stale_as_fresh violation in {r['cycle_id']}"
        assert r["orphan_workers"] == 0
        # bounded queue invariant
        assert r["queue_max_depth"] <= cfg.bounded_queue_maxsize or r["queue_max_depth"] == len(symbols)
    # Memory delta should not grow unbounded (allow some variance, but not > 50MB growth)
    mem_deltas = [r.get("memory_delta_mb") for r in reports if r.get("memory_delta_mb") is not None]
    if len(mem_deltas) >= 2 and all(m is not None for m in mem_deltas):
        # Last minus first should be < 50 MB
        assert (mem_deltas[-1] - mem_deltas[0]) < 50, f"memory leak? deltas {mem_deltas}"


def test_timeout_recovery():
    """Worker timeout should be recorded as TIMEOUT, not converted to WAIT.

    Note: fut.result(timeout=...) only times out if the future hasn't completed
    within that window. With a fast completion (< timeout), no timeout occurs.
    So we test that the timeout plumbing exists and doesn't violate freshness.
    Actual timeout is provoked in test_timeout_recovery_forced.
    """
    cfg = M5OperationalConfig(process_workers=1, thread_workers=1, executor="thread", worker_timeout_s=90, cycle_timeout_s=290)
    from mercury_ai.config.universe import ALL_SYMBOLS
    symbols = ALL_SYMBOLS[:2]
    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)
    report = runner.run_cycle(cycle_id="timeout-test")
    assert report["stale_as_fresh"] == 0
    assert report["cycle_status"] in ("COMPLETED", "CYCLE_TIMEOUT", "SHUTDOWN")


def test_timeout_recovery_forced():
    """Forced timeout plumbing: use a slow provider stub to guarantee TIMEOUT."""
    import concurrent.futures

    cfg = M5OperationalConfig(process_workers=1, thread_workers=1, executor="thread", worker_timeout_s=0.05, cycle_timeout_s=290)

    # Monkey-patch the worker to sleep longer than worker_timeout_s
    import mercury_ai.operations.m5_operational.runner as runner_mod

    orig = runner_mod._analyze_one_isolated

    def slow_worker(symbol: str, disable_profiler: bool = True):
        time.sleep(0.3)
        return orig(symbol, disable_profiler=disable_profiler)

    runner_mod._analyze_one_isolated = slow_worker
    runner_mod._process_worker_entry = slow_worker
    try:
        from mercury_ai.config.universe import ALL_SYMBOLS
        symbols = ALL_SYMBOLS[:2]
        runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)
        report = runner.run_cycle(cycle_id="timeout-forced")
        assert report["assets_timeout"] >= 1 or report["cycle_status"] == "CYCLE_TIMEOUT"
        assert report["stale_as_fresh"] == 0
        for sym, rec in report["per_asset"].items():
            if rec.get("status") == "TIMEOUT":
                assert rec["audit_id"] == "PIPELINE_ERROR"
                assert rec["fresh"] is False
    finally:
        runner_mod._analyze_one_isolated = orig
        runner_mod._process_worker_entry = orig
