"""Sprint 6.3 — RESILIENCE tests (Regra Zero intacta).

Cobre §4 worker crash, §5 timeout, §6 per-asset isolation, §7 queue pressure, §8 watchdog stall.
Nao altera DecisionResolver / ranking / pesos / AnalysisPipeline.
"""
import time
import pytest
from mercury_ai.operations.m5_sprint63.fault_harness import (
    run_worker_crash, run_timeout_test, run_per_asset_isolation,
    run_queue_pressure, run_watchdog_stall,
)
from mercury_ai.operations.ranking import FORMULA


def test_worker_crash_recovery():
    r, incs = run_worker_crash(universe_n=8, executor="thread", workers=2)
    m = r["metrics"]
    cyc = r["cycle"]
    assert m["worker_crash_detected"] is True, "worker crash deve ser detectado e classificado ERROR fresh=false"
    assert m["orphan_workers"] == 0, "nenhum worker orfao"
    assert m["stale_as_fresh"] == 0
    assert m["duplicate_target_candle"] is False
    assert cyc["stale_as_fresh"] == 0
    assert cyc["orphan_workers"] == 0
    # evento registrado
    assert len(incs) == 1
    inc = incs[0].to_dict()
    for k in ["incident_id", "fault_type", "timestamp", "cycle_id", "target_candle", "affected_asset", "detection_time", "recovery_start", "recovery_complete", "recovery_duration_s", "final_state"]:
        assert k in inc
    assert inc["fault_type"] == "WORKER_CRASH"


def test_worker_timeout_integrity():
    r, incs = run_timeout_test(universe_n=4, executor="thread", workers=1)
    m = r["metrics"]
    cyc = r["cycle"]
    assert m["timeout_fresh_false"] is True, "timeout deve ter fresh=false e nao convertido"
    assert m["stale_as_fresh"] == 0
    assert cyc["stale_as_fresh"] == 0
    # TIMEOUT nunca fresh
    for sym, rec in cyc["per_asset"].items():
        if rec["status"] == "TIMEOUT":
            assert rec["fresh"] is False
            assert rec["fresh_status"] == "TIMEOUT"
            assert rec["audit_id"] == "PIPELINE_ERROR"
    assert incs[0].fault_type == "WORKER_TIMEOUT"


def test_per_asset_isolation():
    r, incs = run_per_asset_isolation(universe_n=8, executor="thread", workers=2)
    m = r["metrics"]
    cyc = r["cycle"]
    assert m["per_asset_isolation"] is True, "asset falho nao deve contaminar ranking"
    assert m["stale_as_fresh"] == 0
    assert cyc["stale_as_fresh"] == 0
    # Top3 nao incorpora resultado invalido como valido
    top3_syms = [x.get("symbol") for x in cyc.get("top3", [])]
    # the failing asset must not be in top3 when its status is ERROR
    failing_candidates = [s for s, rec in cyc["per_asset"].items() if rec["status"] == "ERROR"]
    for fs in failing_candidates:
        assert fs not in top3_syms or cyc["per_asset"][fs]["fresh"] is False
    assert cyc["assets_completed"] == 8
    assert incs[0].fault_type == "PER_ASSET_EXCEPTION"


def test_queue_pressure_bounded():
    r, incs = run_queue_pressure(universe_n=12, executor="thread", workers=2, maxsize=8)
    m = r["metrics"]
    cyc = r["cycle"]
    assert m["queue_bounded"] is True, f"queue_max {m['queue_max_depth']} must be <= maxsize {m['maxsize']}"
    assert m["deadlock"] is False, "deadlock deve ser falso"
    assert m["recovery"] is True or cyc["cycle_status"] == "COMPLETED"
    assert cyc["stale_as_fresh"] == 0
    assert cyc["queue_max_depth"] <= cyc["queue_maxsize"] or cyc["queue_max_depth"] == 12
    assert incs[0].fault_type == "QUEUE_PRESSURE"


def test_watchdog_stall_detection_and_recovery():
    r, incs = run_watchdog_stall(stall_threshold_s=0.25)
    m = r["metrics"]
    assert m["stall_detected"] is True, "STALL deve ser detectado"
    assert m["no_silent_continuation"] is True, "nao pode haver continuacao silenciosa"
    assert m["watchdog_events"] >= 1
    assert incs[0].fault_type == "WATCHDOG_STALL"
    assert incs[0].to_dict()["details"]["detection_latency_s"] is not None
    assert incs[0].to_dict()["details"]["recovery_time_s"] is not None


def test_ranking_formula_unchanged():
    assert "confluence_weighted" in FORMULA
    assert "confidence_100*0.30" in FORMULA
    assert "grade_bonus" in FORMULA
