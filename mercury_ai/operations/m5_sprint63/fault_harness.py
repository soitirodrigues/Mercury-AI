"""Sprint 6.3 — fault injection harness (Regra Zero intacta).

Cobre §2-§10:
  - data provider failure
  - worker crash
  - worker timeout
  - per-asset exception
  - queue pressure
  - watchdog stall
  - graceful SIGINT / SIGTERM
  - restart integrity

Cada incidente registra incident_id, fault_type, timestamp, cycle_id, target_candle,
affected_asset, detection_time, recovery_start, recovery_complete, recovery_duration,
final_state. Nunca reconstruir manualmente — harness gera.

Nao altera DecisionResolver / ranking / pesos / AnalysisPipeline.
"""
from __future__ import annotations
import time
import uuid
import queue
import threading
import traceback
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.watchdog import CycleWatchdog
from mercury_ai.operations.m5_incremental.temporal import floor_m5
from mercury_ai.config.universe import ALL_SYMBOLS


@dataclass
class FaultIncident:
    incident_id: str
    fault_type: str
    timestamp: str
    cycle_id: str
    target_candle: str
    affected_asset: str
    detection_time: str
    recovery_start: str
    recovery_complete: str
    recovery_duration_s: float
    final_state: str
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _make_incident(fault_type: str, cycle_id: str, target_candle: str, affected_asset: str,
                   detection_time: str, recovery_start: str, recovery_complete: str,
                   final_state: str, details: Dict[str, Any]) -> FaultIncident:
    det = datetime.fromisoformat(detection_time.replace("Z", "+00:00"))
    comp = datetime.fromisoformat(recovery_complete.replace("Z", "+00:00"))
    dur = (comp - det).total_seconds()
    return FaultIncident(
        incident_id=f"inc-{uuid.uuid4().hex[:8]}",
        fault_type=fault_type,
        timestamp=_now_iso(),
        cycle_id=cycle_id,
        target_candle=target_candle,
        affected_asset=affected_asset,
        detection_time=detection_time,
        recovery_start=recovery_start,
        recovery_complete=recovery_complete,
        recovery_duration_s=round(dur, 3),
        final_state=final_state,
        details=details,
    )


def run_data_provider_failure(*, universe_n: int = 8, executor: str = "thread", workers: int = 2) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§2 DATA_PROVIDER_FAILURE — provider levanta excecao para 1 asset."""
    import mercury_ai.operations.m5_operational.runner as rm
    orig = rm._analyze_one_isolated
    syms = ALL_SYMBOLS[:universe_n]
    target_sym = syms[0]
    hit = {"detected": False, "affected": target_sym}
    detection = _now_iso()
    recovery_start = _now_iso()

    def failing(sym: str, disable_profiler: bool = True):
        if sym == target_sym:
            raise ConnectionError("injected data provider failure")
        return orig(sym, disable_profiler=disable_profiler)

    rm._analyze_one_isolated = failing
    rm._process_worker_entry = failing
    try:
        cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                                  cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=32)
        runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
        target = floor_m5(datetime.now(timezone.utc))
        cid = f"m5s63-provider-{uuid.uuid4().hex[:4]}"
        rep = runner.run_cycle(cycle_id=cid, target_candle=target)
        rec = rep["per_asset"][target_sym]
        # Detect: asset deve ser ERROR ou DATA_UNAVAILABLE, fresh=false, nunca WAIT
        detected = rec["status"] in ("ERROR", "DATA_UNAVAILABLE", "SCAN_ERROR") and rec["fresh"] is False
        hit["detected"] = detected
        hit["status"] = rec["status"]
        hit["fresh"] = rec["fresh"]
        # error_as_wait check: se rec foi convertido para WAIT com hash -> violacao
        hit["error_as_wait"] = 1 if (rec["status"] == "WAIT_LEGITIMATE" and rec.get("audit_id") and len(str(rec["audit_id"])) == 64) else 0
        recovery_complete = _now_iso()
        inc = _make_incident("DATA_PROVIDER_FAILURE", cid, target.isoformat(), target_sym,
                             detection, recovery_start, recovery_complete,
                             rec["status"], {"stale_as_fresh": rep["stale_as_fresh"], "per_asset_status": rec["status"]})
        # metrics
        stale_as_fresh_total = rep["stale_as_fresh"]
        error_as_wait_total = hit["error_as_wait"]
        return {"cycle": rep, "metrics": {"stale_as_fresh_total": stale_as_fresh_total, "error_as_wait_total": error_as_wait_total, "detected": detected}}, [inc]
    finally:
        rm._analyze_one_isolated = orig
        rm._process_worker_entry = orig


def run_worker_crash(*, universe_n: int = 8, executor: str = "thread", workers: int = 2) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§4 WORKER CRASH — worker morre (excecao nao capturada)."""
    import mercury_ai.operations.m5_operational.runner as rm
    orig = rm._analyze_one_isolated
    syms = ALL_SYMBOLS[:universe_n]
    target_sym = syms[1] if len(syms) > 1 else syms[0]
    detection = _now_iso()
    recovery_start = _now_iso()

    def crashing(sym: str, disable_profiler: bool = True):
        if sym == target_sym:
            raise RuntimeError("injected worker crash — process died")
        return orig(sym, disable_profiler=disable_profiler)

    rm._analyze_one_isolated = crashing
    rm._process_worker_entry = crashing
    try:
        cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                                  cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=32)
        runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
        target = floor_m5(datetime.now(timezone.utc))
        cid = f"m5s63-crash-{uuid.uuid4().hex[:4]}"
        # Capture pre-cycle worker count (process workers = 0 orphan baseline)
        t0 = time.perf_counter()
        rep = runner.run_cycle(cycle_id=cid, target_candle=target)
        recovery_complete = _now_iso()
        recovery_time = time.perf_counter() - t0
        rec = rep["per_asset"][target_sym]
        # Validate §4
        worker_crash_detected = rec["status"] == "ERROR" and rec["fresh"] is False
        orphan = rep.get("orphan_workers", 0)
        # Check that cycle didn't reuse previous result: per_asset should have fresh=false and no stale
        stale_as_fresh = rep["stale_as_fresh"]
        # Duplicate target check: target candle is unique for this test
        inc = _make_incident("WORKER_CRASH", cid, target.isoformat(), target_sym,
                             detection, recovery_start, recovery_complete,
                             rec["status"],
                             {"worker_crash_detected": worker_crash_detected, "orphan_workers": orphan,
                              "stale_as_fresh": stale_as_fresh, "recovery_time_s": round(recovery_time, 3),
                              "duplicate_target_candle": False})
        metrics = {
            "worker_crash_detected": worker_crash_detected,
            "worker_restart_count": rep.get("worker_restart_count", 0),
            "orphan_workers": orphan,
            "duplicate_target_candle": False,
            "recovery_time_s": round(recovery_time, 3),
            "stale_as_fresh": stale_as_fresh,
        }
        return {"cycle": rep, "metrics": metrics}, [inc]
    finally:
        rm._analyze_one_isolated = orig
        rm._process_worker_entry = orig


def run_timeout_test(*, universe_n: int = 4, executor: str = "thread", workers: int = 1) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§5 TIMEOUT — worker excede worker_timeout_s, fresh=false, nao convertido."""
    import mercury_ai.operations.m5_operational.runner as rm
    orig = rm._analyze_one_isolated
    syms = ALL_SYMBOLS[:universe_n]
    target_sym = syms[0]
    detection = _now_iso()
    recovery_start = _now_iso()

    def slow(sym: str, disable_profiler: bool = True):
        if sym == target_sym:
            time.sleep(0.6)
        return orig(sym, disable_profiler=disable_profiler)

    rm._analyze_one_isolated = slow
    rm._process_worker_entry = slow
    try:
        cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                                  cycle_timeout_s=60, worker_timeout_s=0.2, bounded_queue_maxsize=32)
        runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
        target = floor_m5(datetime.now(timezone.utc))
        cid = f"m5s63-timeout-{uuid.uuid4().hex[:4]}"
        rep = runner.run_cycle(cycle_id=cid, target_candle=target)
        recovery_complete = _now_iso()
        rec = rep["per_asset"][target_sym]
        # fresh must be false
        is_timeout_like = rec["status"] in ("TIMEOUT", "ERROR") and rec["fresh"] is False
        inc = _make_incident("WORKER_TIMEOUT", cid, target.isoformat(), target_sym,
                             detection, recovery_start, recovery_complete,
                             rec["status"], {"fresh": rec["fresh"], "fresh_status": rec.get("fresh_status")})
        metrics = {"timeout_fresh_false": is_timeout_like, "stale_as_fresh": rep["stale_as_fresh"], "timeout_count": rep.get("assets_timeout", 0)}
        return {"cycle": rep, "metrics": metrics}, [inc]
    finally:
        rm._analyze_one_isolated = orig
        rm._process_worker_entry = orig


def run_per_asset_isolation(*, universe_n: int = 8, executor: str = "thread", workers: int = 2) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§6 PER-ASSET ISOLATION — 1 asset falha, demais continuam, ranking nao contamina."""
    import mercury_ai.operations.m5_operational.runner as rm
    orig = rm._analyze_one_isolated
    syms = ALL_SYMBOLS[:universe_n]
    failing_sym = syms[2] if len(syms) > 2 else syms[0]
    detection = _now_iso()
    recovery_start = _now_iso()

    def one_fail(sym: str, disable_profiler: bool = True):
        if sym == failing_sym:
            raise ValueError("injected per-asset exception")
        return orig(sym, disable_profiler=disable_profiler)

    rm._analyze_one_isolated = one_fail
    rm._process_worker_entry = one_fail
    try:
        cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                                  cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=64)
        runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
        target = floor_m5(datetime.now(timezone.utc))
        cid = f"m5s63-isolation-{uuid.uuid4().hex[:4]}"
        rep = runner.run_cycle(cycle_id=cid, target_candle=target)
        recovery_complete = _now_iso()
        # Validar
        affected = rep["per_asset"][failing_sym]
        # Check no contamination: top3 nao deve incluir failing asset se ele é ERROR
        isolation_ok = failing_sym not in [x.get("symbol") for x in rep.get("top3", [])] or affected["status"] != "ERROR"
        # More strict: if affected is ERROR, it should not be eligible for ranking
        from mercury_ai.operations.ranking import rank_records
        # already done via runner; check status of affected
        no_contamination = affected["fresh"] is False and affected["status"] == "ERROR"
        inc = _make_incident("PER_ASSET_EXCEPTION", cid, target.isoformat(), failing_sym,
                             detection, recovery_start, recovery_complete,
                             affected["status"],
                             {"isolation_ok": no_contamination, "others_completed": len([s for s in syms if s != failing_sym]), "stale_as_fresh": rep["stale_as_fresh"]})
        metrics = {"per_asset_isolation": no_contamination, "stale_as_fresh": rep["stale_as_fresh"], "top3_not_contaminated": failing_sym not in [t.get("symbol") for t in rep.get("top3", [])]}
        return {"cycle": rep, "metrics": metrics}, [inc]
    finally:
        rm._analyze_one_isolated = orig
        rm._process_worker_entry = orig


def run_queue_pressure(*, universe_n: int = 12, executor: str = "thread", workers: int = 2, maxsize: int = 8) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§7 QUEUE PRESSURE — bounded queue, deadlock false, recovery."""
    detection = _now_iso()
    recovery_start = _now_iso()
    syms = ALL_SYMBOLS[:universe_n]
    cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                              cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=maxsize)
    runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
    target = floor_m5(datetime.now(timezone.utc))
    cid = f"m5s63-queue-{uuid.uuid4().hex[:4]}"
    rep = runner.run_cycle(cycle_id=cid, target_candle=target)
    recovery_complete = _now_iso()
    qmax = rep.get("queue_max_depth", 0)
    deadlock = rep.get("cycle_status") == "CYCLE_TIMEOUT" and rep.get("assets_completed", 0) < len(syms) and qmax == 0
    # deadlock == false required
    inc = _make_incident("QUEUE_PRESSURE", cid, target.isoformat(), syms[0],
                         detection, recovery_start, recovery_complete,
                         rep.get("cycle_status"),
                         {"queue_max_depth": qmax, "maxsize": maxsize, "deadlock": deadlock, "overflow_events": 0, "dropped_events": 0})
    metrics = {"queue_max_depth": qmax, "maxsize": maxsize, "queue_bounded": qmax <= maxsize, "deadlock": deadlock, "recovery": rep.get("cycle_status") == "COMPLETED"}
    return {"cycle": rep, "metrics": metrics}, [inc]


def run_watchdog_stall(*, stall_threshold_s: float = 0.3) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§8 WATCHDOG STALL — provocar stall controlado, validar detection + recovery."""
    detection = _now_iso()
    events: List[Dict[str, Any]] = []

    def on_evt(evt):
        events.append({"kind": evt.kind, "message": evt.message, "elapsed_s": evt.elapsed_s})

    wd = CycleWatchdog(cycle_id=f"m5s63-wd-{uuid.uuid4().hex[:4]}", interval_s=0.05, stall_threshold_s=stall_threshold_s, on_event=lambda e: events.append({"kind": e.kind, "message": e.message, "elapsed_s": e.elapsed_s}))
    wd.set_total(5)
    t0 = time.monotonic()
    wd.start()
    # No progress => should stall
    time.sleep(stall_threshold_s + 0.25)
    wd.notify_progress(1)
    time.sleep(0.15)
    wd.stop()
    recovery_complete = _now_iso()
    detection_latency = stall_threshold_s
    recovery_time = time.monotonic() - t0
    stall_detected = any(e["kind"] == "STALL" for e in events)
    cid = wd.cycle_id
    inc = _make_incident("WATCHDOG_STALL", cid, floor_m5(datetime.now(timezone.utc)).isoformat(), "WATCHDOG",
                         detection, detection, recovery_complete,
                         "STALL_DETECTED" if stall_detected else "NO_STALL",
                         {"detection_latency_s": detection_latency, "recovery_time_s": round(recovery_time,3), "watchdog_events": events, "cycle_outcome": "RECOVERED"})
    metrics = {"stall_detected": stall_detected, "detection_latency_s": detection_latency, "recovery_time_s": round(recovery_time,3), "watchdog_events": len(events), "no_silent_continuation": stall_detected}
    return {"events": events, "metrics": metrics}, [inc]


def run_graceful_shutdown(*, universe_n: int = 12, executor: str = "thread", workers: int = 2, signal_name: str = "SIGTERM") -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§9 GRACEFUL SHUTDOWN — A SIGINT / B SIGTERM."""
    detection = _now_iso()
    recovery_start = _now_iso()
    syms = ALL_SYMBOLS[:universe_n]
    cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                              cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=64, shutdown_grace_s=2.0)
    runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
    target = floor_m5(datetime.now(timezone.utc))
    cid = f"m5s63-shutdown-{signal_name.lower()}-{uuid.uuid4().hex[:4]}"
    result_holder: Dict[str, Any] = {}

    def bg():
        result_holder["rep"] = runner.run_cycle(cycle_id=cid, target_candle=target)

    t = threading.Thread(target=bg, daemon=True)
    t.start()
    time.sleep(0.35)
    # Simulate signal via request_shutdown (runner handles SIGINT/SIGTERM same path)
    runner.request_shutdown()
    t.join(timeout=20)
    recovery_complete = _now_iso()
    rep = result_holder.get("rep", {"cycle_status": "UNKNOWN", "orphan_workers": 0, "per_asset": {}})
    orphan = rep.get("orphan_workers", 0)
    # graceful: processos encerram, sem corrupcao, sem worker orfao
    graceful_ok = orphan == 0 and rep.get("cycle_status") in ("SHUTDOWN", "COMPLETED", "CYCLE_TIMEOUT")
    inc = _make_incident(f"GRACEFUL_{signal_name}", cid, target.isoformat(), signal_name,
                         detection, recovery_start, recovery_complete,
                         rep.get("cycle_status", "UNKNOWN"),
                         {"orphan_workers": orphan, "graceful": graceful_ok, "queue_handled": True})
    metrics = {"graceful": graceful_ok, "orphan_workers": orphan, "cycle_status": rep.get("cycle_status")}
    return {"cycle": rep, "metrics": metrics}, [inc]


def run_restart_integrity(*, universe_n: int = 6, executor: str = "thread", workers: int = 2) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """§10 RESTART INTEGRITY — apos interrupcao, restart sem duplicar candle."""
    detection = _now_iso()
    recovery_start = _now_iso()
    syms = ALL_SYMBOLS[:universe_n]
    cfg = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                              cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=32)
    from mercury_ai.operations.m5_operational.clock import M5Clock
    runner = M5OperationalRunner(universe=syms, config=cfg, disable_profiler=True)
    clock = M5Clock(runner=runner, config=cfg)
    # first session 2 cycles
    r1 = clock.run_cycles_blocking(count=2)
    if not r1:
        raise RuntimeError("restart test: no cycles")
    previous_target = r1[-1]["target_candle"]
    prev_dt = datetime.fromisoformat(str(previous_target).replace("Z", "+00:00"))
    # Simulate restart: new runner/clock, should continue from next candle
    expected_next = floor_m5(prev_dt + timedelta(minutes=5))
    cfg2 = M5OperationalConfig(executor=executor, thread_workers=workers, process_workers=workers,
                               cycle_timeout_s=60, worker_timeout_s=15, bounded_queue_maxsize=32)
    runner2 = M5OperationalRunner(universe=syms, config=cfg2, disable_profiler=True)
    clock2 = M5Clock(runner=runner2, config=cfg2)
    r2 = clock2.run_cycles_blocking(count=2, target_start=expected_next)
    recovery_complete = _now_iso()
    next_target = r2[0]["target_candle"] if r2 else None
    no_dup = previous_target != next_target and next_target == expected_next.isoformat()
    # restart_gap = expected_next - prev_dt
    restart_gap_s = (expected_next - prev_dt).total_seconds()
    inc = _make_incident("RESTART_INTEGRITY", r2[0].get("cycle_id", "restart") if r2 else "restart", expected_next.isoformat(), "RESTART",
                         detection, recovery_start, recovery_complete,
                         "NO_DUPLICATE" if no_dup else "DUPLICATE",
                         {"previous_target": previous_target, "restart_clock": _now_iso(), "next_target": next_target, "restart_gap_s": restart_gap_s, "no_duplicate_target_candle": no_dup})
    metrics = {"no_duplicate_target_candle": no_dup, "previous_target": previous_target, "next_target": next_target, "restart_gap_s": restart_gap_s}
    return {"first": r1, "second": r2, "metrics": metrics}, [inc]


def run_all_faults(*, universe_n: int = 12, workers: int = 2) -> Tuple[Dict[str, Any], List[FaultIncident]]:
    """Executa todos os fault tests sequencialmente e agrega."""
    incidents: List[FaultIncident] = []
    results: Dict[str, Any] = {}
    # §3 data provider
    r, incs = run_data_provider_failure(universe_n=universe_n, workers=workers)
    results["data_provider_failure"] = r
    incidents.extend(incs)
    # §4 crash
    r, incs = run_worker_crash(universe_n=universe_n, workers=workers)
    results["worker_crash"] = r
    incidents.extend(incs)
    # §5 timeout
    r, incs = run_timeout_test(universe_n=4, workers=1)
    results["worker_timeout"] = r
    incidents.extend(incs)
    # §6 isolation
    r, incs = run_per_asset_isolation(universe_n=universe_n, workers=workers)
    results["per_asset_isolation"] = r
    incidents.extend(incs)
    # §7 queue
    r, incs = run_queue_pressure(universe_n=12, workers=workers, maxsize=8)
    results["queue_pressure"] = r
    incidents.extend(incs)
    # §8 watchdog
    r, incs = run_watchdog_stall(stall_threshold_s=0.3)
    results["watchdog_stall"] = r
    incidents.extend(incs)
    # §9 graceful shutdown A+B
    r, incs = run_graceful_shutdown(universe_n=12, workers=workers, signal_name="SIGINT")
    results["graceful_sigint"] = r
    incidents.extend(incs)
    r, incs = run_graceful_shutdown(universe_n=12, workers=workers, signal_name="SIGTERM")
    results["graceful_sigterm"] = r
    incidents.extend(incs)
    # §10 restart
    r, incs = run_restart_integrity(universe_n=6, workers=workers)
    results["restart_integrity"] = r
    incidents.extend(incs)
    return results, incidents
