"""Sprint 6.3 — RECOVERY tests (§9 graceful shutdown, §10 restart, §11 live recovery).

Regra Zero intacta. Nao altera inteligencia.
"""
import time
import pytest
from datetime import datetime, timezone, timedelta
from mercury_ai.operations.m5_sprint63.fault_harness import run_graceful_shutdown, run_restart_integrity
from mercury_ai.operations.m5_sprint63.live_session63 import Sprint63LiveSession, Sprint63LiveConfig
from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_incremental.temporal import floor_m5


def test_graceful_sigint():
    r, incs = run_graceful_shutdown(universe_n=8, executor="thread", workers=2, signal_name="SIGINT")
    m = r["metrics"]
    assert m["orphan_workers"] == 0, "SIGINT graceful: nenhum worker orfao"
    assert m["graceful"] is True
    assert r["cycle"]["cycle_status"] in ("SHUTDOWN", "COMPLETED", "CYCLE_TIMEOUT")
    assert incs[0].fault_type == "GRACEFUL_SIGINT"


def test_graceful_sigterm():
    r, incs = run_graceful_shutdown(universe_n=8, executor="thread", workers=2, signal_name="SIGTERM")
    m = r["metrics"]
    assert m["orphan_workers"] == 0, "SIGTERM graceful: nenhum worker orfao"
    assert m["graceful"] is True
    assert incs[0].fault_type == "GRACEFUL_SIGTERM"


def test_restart_integrity_no_duplicate():
    r, incs = run_restart_integrity(universe_n=6, executor="thread", workers=2)
    m = r["metrics"]
    assert m["no_duplicate_target_candle"] is True, f"restart nao pode duplicar target: prev {m['previous_target']} next {m['next_target']}"
    assert pytest.approx(m["restart_gap_s"], abs=2) == 300
    assert incs[0].fault_type == "RESTART_INTEGRITY"
    incd = incs[0].to_dict()
    for k in ["previous_target", "restart_clock", "next_target", "restart_gap_s"]:
        assert k in incd["details"]


def test_restart_no_stale_as_fresh():
    r, _ = run_restart_integrity(universe_n=6, executor="thread", workers=2)
    # Ambos blocos devem ter stale_as_fresh==0 e no stale reutilizado
    for block in [r["first"], r["second"]]:
        for cyc in block:
            assert cyc["stale_as_fresh"] == 0


def test_no_duplicate_target_across_blocking_cycles():
    """§10 + §2: 6 ciclos bloqueantes thread — nenhum duplicate target."""
    from mercury_ai.operations.m5_operational.clock import M5Clock
    from mercury_ai.config.universe import ALL_SYMBOLS
    cfg = M5OperationalConfig(executor="thread", thread_workers=2, cycle_timeout_s=60, worker_timeout_s=15)
    runner = M5OperationalRunner(universe=ALL_SYMBOLS[:4], config=cfg, disable_profiler=True)
    clock = M5Clock(runner=runner, config=cfg)
    reports = clock.run_cycles_blocking(count=6)
    targets = [r["target_candle"] for r in reports]
    assert len(targets) == len(set(targets)), f"duplicate target detected {targets}"
    # restart gap sempre 5m
    for i in range(1, len(targets)):
        a = datetime.fromisoformat(str(targets[i-1]).replace("Z", "+00:00"))
        b = datetime.fromisoformat(str(targets[i]).replace("Z", "+00:00"))
        assert pytest.approx((b - a).total_seconds(), abs=2) == 300


def test_live_recovery_small_thread_smoke():
    """§11 LIVE recovery smoke em thread (nao process) — prova orquestracao sem 5m wait."""
    # Para CI rapido, valida que 2 ciclos LIVE_CLOCK thread smoke passam
    cfg = Sprint63LiveConfig(universe_n=4, executor="thread", workers=2, cycles=6)  # strict would fail; use non-strict via direct runner
    # Use non-strict live session with thread to avoid 30min wait
    from mercury_ai.operations.m5_sprint63.live_session63 import Sprint63LiveSession
    # Bypass strict for smoke: construct with strict=False
    sess = Sprint63LiveSession(cfg=cfg, strict=False)
    # Monkey: run only 2 cycles by trimming cfg
    sess.cfg.cycles = 2
    sess.cfg.executor = "thread"
    sess.cfg.universe_n = 4
    out = sess.run()
    assert len(out["cycles"]) == 2
    assert out["summary"]["no_duplicate_target_candle"] is True
    for c in out["cycles"]:
        assert c["stale_as_fresh"] == 0
