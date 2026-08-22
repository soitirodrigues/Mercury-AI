"""Sprint 6.3 — LIVE RECOVERY SESSION (6 ciclos LIVE_CLOCK pos-fault).

Nao altera inteligencia (Regra Zero §0). Reusa M5OperationalRunner + LiveClockIntegrityGate.
Sugestao spec §11:
  python scripts/m5_sprint63_gate_runner.py --universe 64 --executor process --cycles 6 --mode live_clock

Objetivo: 6 qualifying cycles, 6 pass, 0 fail. Nao substitui 6.2.
"""
from __future__ import annotations
import time, uuid, json
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_operational.clock import M5Clock
from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5, _ensure_utc
from mercury_ai.operations.ranking import FORMULA
from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.operations.m5_sprint61.live_clock_integrity import MeasurementMode, LiveClockCycleInput, classify_cycle, aggregate_live_clock
from mercury_ai.operations.m5_sprint6.deadline import percentile
from mercury_ai.operations.m5_sprint6.alerts import AlertSink

try:
    from mercury_ai.operations.m5_sprint6 import alerts as _alerts_mod
    _alerts_mod.KINDS.add("CLOCK_INTEGRITY_FAIL")
except Exception:
    pass

@dataclass
class Sprint63LiveConfig:
    universe_n: int = 64
    executor: str = "process"
    workers: Optional[int] = None
    cycles: int = 6
    worker_timeout_s: float = 90.0
    cycle_timeout_s: float = 290.0
    measurement_mode: str = "LIVE_CLOCK"

class Sprint63LiveSession:
    def __init__(self, cfg: Optional[Sprint63LiveConfig] = None, m5_cfg: Optional[M5OperationalConfig] = None, strict: bool = True):
        self.cfg = cfg or Sprint63LiveConfig()
        if strict:
            if self.cfg.measurement_mode != "LIVE_CLOCK":
                raise ValueError("Sprint 6.3 live recovery exige LIVE_CLOCK")
            if self.cfg.cycles != 6:
                raise ValueError("Sprint 6.3 live recovery exige cycles=6")
            if self.cfg.universe_n != 64:
                raise ValueError("Sprint 6.3 live recovery exige universe=64")
            if self.cfg.executor != "process":
                raise ValueError("Sprint 6.3 live recovery exige executor=process")
        self.m5_cfg = m5_cfg
        self.session_id = f"m5s63-{uuid.uuid4().hex[:8]}"
        self.start_wall: Optional[str] = None
        self.end_wall: Optional[str] = None
        self.alerts = AlertSink()
        self.cycle_reports: List[Dict[str, Any]] = []
        self._runner: Optional[M5OperationalRunner] = None
        self._clock: Optional[M5Clock] = None

    def _build_runner(self) -> M5OperationalRunner:
        n = min(self.cfg.universe_n, len(ALL_SYMBOLS))
        symbols = ALL_SYMBOLS[:n]
        base = self.m5_cfg or M5OperationalConfig.from_env()
        kw = base.to_dict()
        kw["worker_timeout_s"] = self.cfg.worker_timeout_s
        kw["cycle_timeout_s"] = self.cfg.cycle_timeout_s
        kw["executor"] = self.cfg.executor
        if self.cfg.workers is not None:
            kw["process_workers"] = self.cfg.workers
        m5cfg = M5OperationalConfig(**kw)
        assert m5cfg.max_concurrent_cycles == 1
        m5cfg.validate()
        runner = M5OperationalRunner(universe=symbols, config=m5cfg, disable_profiler=True)
        runner._install_signal_handlers()
        self._runner = runner
        self._clock = M5Clock(runner=runner, config=m5cfg)
        return runner

    def run(self) -> Dict[str, Any]:
        self.start_wall = datetime.now(timezone.utc).isoformat()
        runner = self._build_runner()
        assert self._clock is not None
        mode = MeasurementMode.LIVE_CLOCK
        enriched: List[Dict[str, Any]] = []
        integrity_reports: List[Any] = []
        session_start_perf = time.perf_counter()
        prev_target: Optional[datetime] = None
        for idx in range(self.cfg.cycles):
            if idx > 0 and prev_target is not None:
                attempts = 0
                while attempts < 700:
                    now_probe = datetime.now(timezone.utc)
                    cand = floor_m5(now_probe)
                    if cand > prev_target:
                        break
                    nxt = ceil_m5(now_probe)
                    wait_s = (nxt - now_probe).total_seconds()
                    sleep_for = min(max(wait_s + 0.05, 0.05), 1.0)
                    time.sleep(sleep_for)
                    attempts += 1
            clock_now_at_start = datetime.now(timezone.utc)
            target_dt = floor_m5(clock_now_at_start)
            if target_dt > clock_now_at_start:
                delta = (target_dt - clock_now_at_start).total_seconds()
                try:
                    self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target {target_dt.isoformat()} > clock_now {clock_now_at_start.isoformat()} delta {delta:.3f}s")
                except Exception:
                    self.alerts.emit("STALE_DATA", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target future delta {delta:.3f}s")
            if prev_target is not None and target_dt <= prev_target:
                nxt = ceil_m5(clock_now_at_start)
                wait_s = (nxt - clock_now_at_start).total_seconds() + 0.05
                if wait_s > 0:
                    time.sleep(wait_s)
                clock_now_at_start = datetime.now(timezone.utc)
                target_dt = floor_m5(clock_now_at_start)
                if target_dt > clock_now_at_start:
                    delta = (target_dt - clock_now_at_start).total_seconds()
                    try:
                        self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL post-wait delta {delta:.3f}s")
                    except Exception:
                        pass
            prev_target = target_dt
            cycle_id = f"m5s63-live-{target_dt.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
            r = runner.run_cycle(cycle_id=cycle_id, target_candle=target_dt)
            try:
                cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))
            except Exception:
                cs_dt = clock_now_at_start
            first_fresh_ms = r.get("first_fresh_decision_ms")
            decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
            first_fresh_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
            first_top3_dt = (cs_dt + timedelta(milliseconds=float(r.get("first_top3_ms")))) if r.get("first_top3_ms") is not None else None
            try:
                ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None
            except Exception:
                ce_dt = None
            target_close_dt = target_dt
            next_start_dt = target_dt + timedelta(minutes=5)
            cycle_start_dt = cs_dt
            gate_input = LiveClockCycleInput(
                measurement_mode=mode,
                clock_now_at_cycle_start=clock_now_at_start,
                target_candle=target_dt,
                decision_ready=decision_ready_dt,
            )
            gate_rep = classify_cycle(gate_input)
            integrity_reports.append(gate_rep)
            if r.get("stale_as_fresh", 0) != 0:
                self.alerts.emit("FRESHNESS_VIOLATION", "CRITICAL", cycle_id, f"stale_as_fresh={r.get('stale_as_fresh')}")
            if gate_rep.target_is_future and gate_rep.next_candle_result == "QUALIFYING_PASS":
                try:
                    self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", cycle_id, f"target_is_future but PASS — integrity bug target {gate_rep.target_candle} clock {gate_rep.clock_now_at_cycle_start}")
                except Exception:
                    pass
            if gate_rep.next_candle_result == "QUALIFYING_FAIL":
                self.alerts.emit("DEADLINE_MISSED", "CRITICAL", cycle_id, f"QUALIFYING_FAIL margin={gate_rep.deadline_margin_s} latency={gate_rep.decision_latency_s}")
            elif gate_rep.next_candle_result.startswith("NON_QUALIFYING"):
                self.alerts.emit("STALE_DATA", "WARN", cycle_id, gate_rep.non_qualifying_reason or "non-qualifying")
            if r.get("watchdog_events"):
                for e in r["watchdog_events"]:
                    try:
                        self.alerts.emit("WATCHDOG_STALL", "WARN", cycle_id, str(e.get("message") or e), extra=e)
                    except Exception:
                        pass
            ec = dict(r)
            ec.update({
                "cycle_id": cycle_id,
                "cycle_index": idx,
                "measurement_mode": gate_rep.measurement_mode,
                "clock_now_at_cycle_start": gate_rep.clock_now_at_cycle_start,
                "target_candle": gate_rep.target_candle,
                "target_candle_close": gate_rep.target_candle_close,
                "cycle_start": cycle_start_dt.isoformat() if cycle_start_dt else r.get("cycle_start"),
                "first_fresh_decision": first_fresh_dt.isoformat() if first_fresh_dt else None,
                "first_top3": first_top3_dt.isoformat() if first_top3_dt else None,
                "decision_ready": gate_rep.decision_ready,
                "next_candle_start": gate_rep.next_candle_start,
                "cycle_complete": ce_dt.isoformat() if ce_dt else r.get("cycle_end"),
                "decision_latency_s": gate_rep.decision_latency_s,
                "deadline_margin_s": gate_rep.deadline_margin_s,
                "target_is_future": gate_rep.target_is_future,
                "decision_before_candle_close": gate_rep.decision_before_candle_close,
                "temporal_order_valid": gate_rep.temporal_order_valid,
                "live_clock_qualifying": gate_rep.live_clock_qualifying,
                "next_candle_result": gate_rep.next_candle_result,
                "non_qualifying_reason": gate_rep.non_qualifying_reason,
                "qualifying": gate_rep.live_clock_qualifying,
                "result": gate_rep.next_candle_result,
                "decision_latency": gate_rep.decision_latency_s,
                "deadline_margin": gate_rep.deadline_margin_s,
            })
            enriched.append(ec)
        self.end_wall = datetime.now(timezone.utc).isoformat()
        self.cycle_reports = enriched
        session_wall_s = time.perf_counter() - session_start_perf
        gate_agg = aggregate_live_clock(integrity_reports)
        first_fresh_s = [(c["first_fresh_decision_ms"]/1000.0) for c in enriched if c.get("first_fresh_decision_ms") is not None]
        first_top3_s = [(c["first_top3_ms"]/1000.0) for c in enriched if c.get("first_top3_ms") is not None]
        lat_valid = [r.decision_latency_s for r in integrity_reports if r.next_candle_result == "QUALIFYING_PASS" and r.decision_latency_s is not None]
        mar_valid = [r.deadline_margin_s for r in integrity_reports if r.next_candle_result == "QUALIFYING_PASS" and r.deadline_margin_s is not None]
        wall_s = [c.get("cycle_duration_s") for c in enriched if c.get("cycle_duration_s") is not None]
        queue_maxes = [c.get("queue_max_depth", 0) for c in enriched]
        mem_vals = [c.get("peak_memory_mb") for c in enriched if c.get("peak_memory_mb") is not None]
        orphan_total = sum(int(c.get("orphan_workers", 0) or 0) for c in enriched)
        watchdog_total = sum(len(c.get("watchdog_events") or []) for c in enriched)
        worker_restarts_total = sum(int(c.get("worker_restart_count", 0) or 0) for c in enriched)
        stale_as_fresh_total = sum(int(c.get("stale_as_fresh", 0) or 0) for c in enriched)
        def _slice_stats(arr):
            if not arr:
                return {}
            n = len(arr)
            first4 = arr[:4] if n >= 4 else arr
            last4 = arr[-4:] if n >= 4 else arr
            return {
                "p50": percentile(arr, 50) if arr else None,
                "p95": percentile(arr, 95) if arr else None,
                "min": min(arr) if arr else None,
                "max": max(arr) if arr else None,
                "mean": sum(arr)/len(arr) if arr else None,
                "first4_mean": sum(first4)/len(first4) if first4 else None,
                "last4_mean": sum(last4)/len(last4) if last4 else None,
                "drift_last_minus_first": (sum(last4)/len(last4) - sum(first4)/len(first4)) if first4 and last4 else None,
                "trend": "degrading" if first4 and last4 and (sum(last4)/len(last4) > sum(first4)/len(first4)*1.2) else "stable",
            }
        wall_stats = _slice_stats(wall_s)
        lat_stats = _slice_stats(lat_valid)
        mar_stats = _slice_stats(mar_valid)
        fresh_stats = _slice_stats(first_fresh_s)
        top3_stats = _slice_stats(first_top3_s)
        targets = [c["target_candle"] for c in enriched]
        no_duplicate = len(targets) == len(set(targets))
        duplicate_targets = [t for t in set(targets) if targets.count(t) > 1]
        future_count = sum(1 for c in enriched if c.get("target_is_future"))
        clock_integrity_ok = future_count == 0 and all(not c.get("target_is_future") for c in enriched)
        queue_max = max(queue_maxes) if queue_maxes else 0
        queue_bounded_ok = queue_max <= 128
        memory_initial = mem_vals[0] if mem_vals else None
        memory_peak = max(mem_vals) if mem_vals else None
        memory_final = mem_vals[-1] if mem_vals else None
        memory_delta = (memory_final - memory_initial) if memory_initial is not None and memory_final is not None else None
        monotonic_anomaly = bool(memory_delta is not None and (memory_delta > 50 or (memory_initial and memory_final and memory_final > memory_initial * 2)))
        total_cycles = gate_agg["total_cycles"]
        qualifying_live_cycles = gate_agg["qualifying_live_cycles"]
        qualifying_pass = gate_agg["qualifying_pass"]
        qualifying_fail = gate_agg["qualifying_fail"]
        non_qualifying = gate_agg["non_qualifying_cycles"]
        # §11 live recovery: 6 qualifying 6 pass 0 fail demanded
        is_recovery_ok = (qualifying_live_cycles == 6 and qualifying_pass == 6 and qualifying_fail == 0 and stale_as_fresh_total == 0 and orphan_total == 0 and no_duplicate and clock_integrity_ok)
        status = "LIVE_RECOVERY PASS" if is_recovery_ok else "LIVE_RECOVERY FAIL"
        cycles_expected = self.cfg.cycles
        cycles_completed = len(enriched)
        summary: Dict[str, Any] = {
            "session_id": self.session_id,
            "measurement_mode": "LIVE_CLOCK",
            "mode": "LIVE_CLOCK",
            "start": self.start_wall,
            "end": self.end_wall,
            "session_wall_s": session_wall_s,
            "session_wall_human": f"{session_wall_s/60:.1f} min ({session_wall_s/3600:.2f} h)",
            "config": self.cfg.__dict__,
            "m5_config": (self._runner.config.to_dict() if self._runner else {}),
            "formula": FORMULA,
            "cycles_expected": cycles_expected,
            "cycles_completed": cycles_completed,
            "total_cycles": total_cycles,
            "qualifying_live_cycles": qualifying_live_cycles,
            "qualifying_pass": qualifying_pass,
            "qualifying_fail": qualifying_fail,
            "non_qualifying_cycles": non_qualifying,
            "next_candle_pass_rate": gate_agg.get("next_candle_pass_rate"),
            "live_clock_certification": gate_agg.get("certification"),
            "live_clock_agg": gate_agg,
            "stale_as_fresh_total": stale_as_fresh_total,
            "freshness_ok": stale_as_fresh_total == 0,
            "early_emission": {"first_fresh_s": fresh_stats, "first_top3_s": top3_stats, "decision_ready_latency_s": lat_stats, "cycle_complete_s": wall_stats},
            "performance_drift": {"wall_duration_s": wall_stats, "decision_latency_s": lat_stats, "deadline_margin_s": mar_stats, "first_fresh_s": fresh_stats, "first_top3_s": top3_stats, "queue_depth": _slice_stats(queue_maxes), "memory_mb": _slice_stats(mem_vals) if mem_vals else {}},
            "resource_soak": {"orphan_workers": orphan_total, "queue_max_depth": queue_max, "queue_bounded_ok": queue_bounded_ok, "worker_restart_count": worker_restarts_total, "watchdog_events": watchdog_total, "memory_initial_mb": memory_initial, "memory_peak_mb": memory_peak, "memory_final_mb": memory_final, "memory_delta_mb": memory_delta, "monotonic_anomaly": monotonic_anomaly},
            "orphan_workers": orphan_total,
            "queue_max": queue_max,
            "peak_memory_mb": memory_peak,
            "temporal_integrity": {"all_target_le_clock": clock_integrity_ok, "clock_integrity_ok": clock_integrity_ok, "future_target_count": future_count, "no_duplicate_target_candle": no_duplicate, "duplicate_targets": duplicate_targets},
            "no_duplicate_target_candle": no_duplicate,
            "all_target_candle_le_clock": clock_integrity_ok,
            "live_recovery_ok": is_recovery_ok,
            "sprint63_live_status": status,
        }
        return {"session_id": self.session_id, "live_session_config": self.cfg.__dict__, "summary": summary, "cycles": enriched, "integrity_reports": [r.to_dict() for r in integrity_reports], "alerts": self.alerts.to_list()}

    def write_artifacts(self, session: Dict[str, Any], out_dir: str = "reports/m5_sprint63") -> Dict[str, str]:
        base = Path(out_dir)
        base.mkdir(parents=True, exist_ok=True)
        sid = session.get("session_id") or self.session_id
        sub = base / sid
        sub.mkdir(parents=True, exist_ok=True)
        # recovery report
        rec_json = sub / "recovery_live_clock_report.json"
        rec_json.write_text(json.dumps(session, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        # also copy to canonical name without overwriting history: symlink-like copy
        canonical = base / "recovery_live_clock_report.json"
        try:
            canonical.write_text(rec_json.read_text(encoding="utf-8"), encoding="utf-8")
        except Exception:
            pass
        paths = {"recovery_json": str(rec_json), "recovery_canonical": str(canonical), "session_dir": str(sub)}
        return paths
