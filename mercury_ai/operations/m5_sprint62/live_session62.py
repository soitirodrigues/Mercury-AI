"""Sprint 6.2 — FULL LIVE_CLOCK CERTIFICATION / LONG SESSION (24 ciclos reais M5).

Nao altera inteligencia (Regra Zero). Layer exclusivo: observability, reporting,
watchdog, temporal integrity, recovery, orchestration.
"""
from __future__ import annotations

import json
import time
import uuid
import hashlib
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
from mercury_ai.operations.m5_sprint61.live_clock_integrity import (
    MeasurementMode,
    LiveClockCycleInput,
    classify_cycle,
    aggregate_live_clock,
)
from mercury_ai.operations.m5_sprint6.deadline import evaluate_deadline, aggregate_deadlines, percentile
from mercury_ai.operations.m5_sprint6.alerts import AlertSink

# Extend alert kinds for 6.2 if not present
try:
    from mercury_ai.operations.m5_sprint6 import alerts as _alerts_mod
    _alerts_mod.KINDS.add("CLOCK_INTEGRITY_FAIL")
except Exception:
    pass


@dataclass
class Sprint62Config:
    universe_n: int = 64
    executor: str = "process"  # Sprint 6.2 §4 exige process
    workers: Optional[int] = None  # baseline oficial (4)
    cycles: int = 24
    worker_timeout_s: float = 90.0
    cycle_timeout_s: float = 290.0
    measurement_mode: str = "LIVE_CLOCK"  # exclusivo


class Sprint62LiveSession:
    """Sessao longa 24 ciclos reais LIVE_CLOCK, max_concurrent=1, target derivado de UTC real."""

    def __init__(self, cfg: Optional[Sprint62Config] = None, m5_cfg: Optional[M5OperationalConfig] = None, strict: bool = True):
        self.cfg = cfg or Sprint62Config()
        if strict:
            if self.cfg.measurement_mode != "LIVE_CLOCK":
                raise ValueError("Sprint 6.2 exige measurement_mode=LIVE_CLOCK")
            if self.cfg.cycles != 24:
                raise ValueError("Sprint 6.2 exige cycles=24")
            if self.cfg.universe_n != 64:
                raise ValueError("Sprint 6.2 §4 exige universe=64")
            if self.cfg.executor != "process":
                raise ValueError("Sprint 6.2 §4 exige executor=process")
        self.m5_cfg = m5_cfg
        self.session_id = f"m5s62-{uuid.uuid4().hex[:8]}"
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
        # enforce baseline oficiais §4
        m5cfg = M5OperationalConfig(**kw)
        # garante max_concurrent 1
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
            # §2: clock_now_at_cycle_start capturado antes de derivar target
            # Se nao for primeiro ciclo, aguardar proxima fronteira real para nao duplicar e respeitar relogio real
            if idx > 0 and prev_target is not None:
                attempts = 0
                while attempts < 700:  # ~5min em polls 0.5s
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

            # §3 proibicao absoluta target futuro — runtime assertion
            if target_dt > clock_now_at_start:
                delta = (target_dt - clock_now_at_start).total_seconds()
                try:
                    self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target {target_dt.isoformat()} > clock_now {clock_now_at_start.isoformat()} delta {delta:.3f}s")
                except Exception:
                    # fallback se kind nao registrado
                    self.alerts.emit("STALE_DATA", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target future delta {delta:.3f}s")
                # ainda prosseguir mas sera NON_QUALIFYING pelo gate

            # Evitar duplicata §10: nunca duplicar target_candle
            if prev_target is not None and target_dt <= prev_target:
                nxt = ceil_m5(clock_now_at_start)
                wait_s = (nxt - clock_now_at_start).total_seconds() + 0.05
                if wait_s > 0:
                    time.sleep(wait_s)
                clock_now_at_start = datetime.now(timezone.utc)
                target_dt = floor_m5(clock_now_at_start)
                # re-validar apos ajuste
                if target_dt > clock_now_at_start:
                    delta = (target_dt - clock_now_at_start).total_seconds()
                    try:
                        self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL post-wait delta {delta:.3f}s")
                    except Exception:
                        pass
            prev_target = target_dt

            cycle_id = f"m5s62-live-{target_dt.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
            # runner.run_cycle executa pipeline real com dados reais
            r = runner.run_cycle(cycle_id=cycle_id, target_candle=target_dt)

            # Derivar timestamps §2
            try:
                cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))
            except Exception:
                cs_dt = clock_now_at_start
            try:
                ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None
            except Exception:
                ce_dt = None

            first_fresh_ms = r.get("first_fresh_decision_ms")
            first_top3_ms = r.get("first_top3_ms")
            complete_ms = r.get("cycle_complete_ms")

            # decision_ready = cycle_start + first_fresh_decision
            decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
            first_fresh_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
            first_top3_dt = (cs_dt + timedelta(milliseconds=float(first_top3_ms))) if first_top3_ms is not None else None
            cycle_complete_dt = ce_dt
            target_close_dt = target_dt
            next_start_dt = target_dt + timedelta(minutes=5)
            cycle_start_dt = cs_dt

            # Gate §2-§3 §6
            gate_input = LiveClockCycleInput(
                measurement_mode=mode,
                clock_now_at_cycle_start=clock_now_at_start,
                target_candle=target_dt,
                decision_ready=decision_ready_dt,
            )
            gate_rep = classify_cycle(gate_input)
            integrity_reports.append(gate_rep)

            # Freshness invariants §5: stale_as_fresh_total ==0, never convert ERROR→WAIT or STALE→FRESH
            # Runner ja garante via FreshnessGate; aqui apenas auditar
            if r.get("stale_as_fresh", 0) != 0:
                self.alerts.emit("FRESHNESS_VIOLATION", "CRITICAL", cycle_id, f"stale_as_fresh={r.get('stale_as_fresh')}")

            # §3 target futuro nunca PASS
            if gate_rep.target_is_future and gate_rep.next_candle_result == "QUALIFYING_PASS":
                # invariante violada — deve ser NON_QUALIFYING_FUTURE_TARGET, mas se chegou aqui é bug
                try:
                    self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", cycle_id, f"target_is_future but PASS — integrity bug target {gate_rep.target_candle} clock {gate_rep.clock_now_at_cycle_start}")
                except Exception:
                    pass

            # Deadline §6
            if gate_rep.next_candle_result == "QUALIFYING_FAIL":
                self.alerts.emit("DEADLINE_MISSED", "CRITICAL", cycle_id, f"QUALIFYING_FAIL margin={gate_rep.deadline_margin_s} latency={gate_rep.decision_latency_s}")
            elif gate_rep.next_candle_result.startswith("NON_QUALIFYING"):
                # nao mascarar; apenas WARN para visibilidade
                self.alerts.emit("STALE_DATA", "WARN", cycle_id, gate_rep.non_qualifying_reason or "non-qualifying")

            if r.get("watchdog_events"):
                for e in r["watchdog_events"]:
                    try:
                        self.alerts.emit("WATCHDOG_STALL", "WARN", cycle_id, str(e.get("message") or e), extra=e)
                    except Exception:
                        pass

            # Enriquecer ciclo com todos campos §2
            ec = dict(r)
            # normalizar campos canonicos §2
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
                "cycle_complete": cycle_complete_dt.isoformat() if cycle_complete_dt else r.get("cycle_end"),
                # derivadas
                "decision_latency_s": gate_rep.decision_latency_s,
                "deadline_margin_s": gate_rep.deadline_margin_s,
                "target_is_future": gate_rep.target_is_future,
                "decision_before_candle_close": gate_rep.decision_before_candle_close,
                "temporal_order_valid": gate_rep.temporal_order_valid,
                "live_clock_qualifying": gate_rep.live_clock_qualifying,
                "next_candle_result": gate_rep.next_candle_result,
                "non_qualifying_reason": gate_rep.non_qualifying_reason,
                "qualifying": gate_rep.live_clock_qualifying,  # alias
                "result": gate_rep.next_candle_result,
                # manter compat com legado
                "decision_latency": gate_rep.decision_latency_s,
                "deadline_margin": gate_rep.deadline_margin_s,
            })
            enriched.append(ec)

        self.end_wall = datetime.now(timezone.utc).isoformat()
        self.cycle_reports = enriched
        session_wall_s = time.perf_counter() - session_start_perf

        # Agregacoes
        gate_agg = aggregate_live_clock(integrity_reports)

        # Early emission stats §7
        def _collect(key):
            vals = []
            for c in enriched:
                v = c.get(key)
                if v is not None:
                    try:
                        vals.append(float(v) / 1000.0 if key.endswith("_ms") else float(v))
                    except Exception:
                        pass
            return vals

        first_fresh_s = [ (c["first_fresh_decision_ms"]/1000.0) for c in enriched if c.get("first_fresh_decision_ms") is not None ]
        first_top3_s = [ (c["first_top3_ms"]/1000.0) for c in enriched if c.get("first_top3_ms") is not None ]
        # decision latency & margin apenas de qualificaveis PASS (gate)
        lat_valid = [r.decision_latency_s for r in integrity_reports if r.next_candle_result == "QUALIFYING_PASS" and r.decision_latency_s is not None]
        mar_valid = [r.deadline_margin_s for r in integrity_reports if r.next_candle_result == "QUALIFYING_PASS" and r.deadline_margin_s is not None]
        # wall duration por ciclo
        wall_s = [c.get("cycle_duration_s") for c in enriched if c.get("cycle_duration_s") is not None]
        queue_maxes = [c.get("queue_max_depth", 0) for c in enriched]
        mem_vals = [c.get("peak_memory_mb") for c in enriched if c.get("peak_memory_mb") is not None]
        mem_deltas = [c.get("memory_delta_mb") for c in enriched if c.get("memory_delta_mb") is not None]

        orphan_total = sum(int(c.get("orphan_workers", 0) or 0) for c in enriched)
        watchdog_total = sum(len(c.get("watchdog_events") or []) for c in enriched)
        worker_restarts_total = sum(int(c.get("worker_restart_count", 0) or 0) for c in enriched)
        stale_as_fresh_total = sum(int(c.get("stale_as_fresh", 0) or 0) for c in enriched)

        # Performance drift §8: primeiros 4 vs ultimos 4
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

        # Duplicate target detection §10/§15
        targets = [c["target_candle"] for c in enriched]
        no_duplicate = len(targets) == len(set(targets))
        duplicate_targets = [t for t in set(targets) if targets.count(t) > 1]

        # All target <= clock check §3 §15
        all_target_le_clock = all(not c.get("target_is_future") or c.get("next_candle_result") != "QUALIFYING_PASS" for c in enriched)
        # stricter: nenhum target futuro em qualificavel
        future_count = sum(1 for c in enriched if c.get("target_is_future"))
        # honestly: fully compliant if future_count==0 for LIVE_CLOCK (should be 0)
        clock_integrity_ok = future_count == 0 and all(not c.get("target_is_future") for c in enriched)

        # Resource soak §9
        queue_max = max(queue_maxes) if queue_maxes else 0
        queue_bounded_ok = queue_max <= 128
        memory_initial = mem_vals[0] if mem_vals else None
        memory_peak = max(mem_vals) if mem_vals else None
        memory_final = mem_vals[-1] if mem_vals else None
        memory_delta = (memory_final - memory_initial) if memory_initial is not None and memory_final is not None else None
        # monotonic growth anormal: final > initial*2 ou crescimento > 50MB
        monotonic_anomaly = bool(memory_delta is not None and (memory_delta > 50 or (memory_initial and memory_final and memory_final > memory_initial * 2)))

        # Qualifying split §17 honestidade
        total_cycles = gate_agg["total_cycles"]
        qualifying_live_cycles = gate_agg["qualifying_live_cycles"]
        qualifying_pass = gate_agg["qualifying_pass"]
        qualifying_fail = gate_agg["qualifying_fail"]
        non_qualifying = gate_agg["non_qualifying_cycles"]

        # Determine certification §15 §16
        # FULL only if 24 qualifying pass ==24 etc
        is_full = (
            qualifying_live_cycles == 24
            and qualifying_pass == 24
            and qualifying_fail == 0
            and stale_as_fresh_total == 0
            and orphan_total == 0
            and no_duplicate
            and clock_integrity_ok
        )
        # determinism/regression will be injected externally; here mark pending
        status = "FULL LIVE_CLOCK CERTIFIED" if is_full else "NOT CERTIFIED"

        cycles_expected = self.cfg.cycles
        cycles_completed = len(enriched)
        cycles_failed = cycles_expected - cycles_completed if cycles_expected > cycles_completed else 0

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
            "cycles_failed": cycles_failed,
            "total_cycles": total_cycles,
            "qualifying_live_cycles": qualifying_live_cycles,
            "qualifying_pass": qualifying_pass,
            "qualifying_fail": qualifying_fail,
            "non_qualifying_cycles": non_qualifying,
            "next_candle_pass_rate": gate_agg.get("next_candle_pass_rate"),
            "live_clock_certification": gate_agg.get("certification"),
            "live_clock_agg": gate_agg,
            # Freshness §5
            "stale_as_fresh_total": stale_as_fresh_total,
            "freshness_ok": stale_as_fresh_total == 0,
            # Early emission §7
            "early_emission": {
                "first_fresh_s": fresh_stats,
                "first_top3_s": top3_stats,
                "decision_ready_latency_s": lat_stats,
                "cycle_complete_s": wall_stats,
            },
            "first_fresh_p50": fresh_stats.get("p50"),
            "first_fresh_p95": fresh_stats.get("p95"),
            "first_top3_p50": top3_stats.get("p50"),
            "first_top3_p95": top3_stats.get("p95"),
            "complete_p50": wall_stats.get("p50"),
            "complete_p95": wall_stats.get("p95"),
            # Performance drift §8
            "performance_drift": {
                "wall_duration_s": wall_stats,
                "decision_latency_s": lat_stats,
                "deadline_margin_s": mar_stats,
                "first_fresh_s": fresh_stats,
                "first_top3_s": top3_stats,
                "queue_depth": _slice_stats(queue_maxes),
                "memory_mb": _slice_stats(mem_vals) if mem_vals else {},
            },
            "deadline_margin_p50": mar_stats.get("p50"),
            "deadline_margin_p95": mar_stats.get("p95"),
            "deadline_margin_min": mar_stats.get("min"),
            "deadline_margin_max": mar_stats.get("max"),
            # Resource soak §9
            "resource_soak": {
                "orphan_workers": orphan_total,
                "queue_max_depth": queue_max,
                "queue_bounded_ok": queue_bounded_ok,
                "worker_restart_count": worker_restarts_total,
                "watchdog_events": watchdog_total,
                "memory_initial_mb": memory_initial,
                "memory_peak_mb": memory_peak,
                "memory_final_mb": memory_final,
                "memory_delta_mb": memory_delta,
                "monotonic_anomaly": monotonic_anomaly,
            },
            "orphan_workers": orphan_total,
            "queue_max": queue_max,
            "peak_memory_mb": memory_peak,
            "memory_initial_mb": memory_initial,
            "memory_final_mb": memory_final,
            "memory_delta_mb_last_first": memory_delta,
            "worker_restarts": worker_restarts_total,
            "watchdog_events": watchdog_total,
            # Temporal integrity §2-§3
            "temporal_integrity": {
                "all_target_le_clock": all_target_le_clock,
                "clock_integrity_ok": clock_integrity_ok,
                "future_target_count": future_count,
                "no_duplicate_target_candle": no_duplicate,
                "duplicate_targets": duplicate_targets,
                "min_deadline_margin_valid": mar_stats.get("min"),
                "min_latency_valid": lat_stats.get("min"),
                "max_latency_valid": lat_stats.get("max"),
            },
            "no_duplicate_target_candle": no_duplicate,
            "all_target_candle_le_clock": clock_integrity_ok,
            "min_deadline_margin_valid": mar_stats.get("min"),
            "min_latency_valid": lat_stats.get("min"),
            "max_latency_valid": lat_stats.get("max"),
            # Certification status §15-§16
            "full_live_clock_certified": is_full,
            "sprint62_status": status,
            # placeholders for determinism/regression §11-§12 (filled by runner)
            "determinism": "PENDING",
            "regression": "PENDING",
        }

        return {
            "session_id": self.session_id,
            "live_session_config": self.cfg.__dict__,
            "summary": summary,
            "cycles": enriched,
            "integrity_reports": [r.to_dict() for r in integrity_reports],
            "alerts": self.alerts.to_list(),
        }

    def write_artifacts(self, session: Dict[str, Any], out_dir: str = "reports/m5_sprint62") -> Dict[str, str]:
        base = Path(out_dir)
        base.mkdir(parents=True, exist_ok=True)
        # never overwrite previous: if base/live_clock_24cycles_report.json exists, move to subdir per session_id
        main_json = base / "live_clock_24cycles_report.json"
        main_md = base / "live_clock_24cycles_report.md"
        sensei = base / "SENSEI_SPRINT62_REPORT.md"
        session_id = session.get("session_id") or self.session_id
        paths: Dict[str, str] = {}
        # archive previous if exists
        if main_json.exists():
            try:
                prev = json.loads(main_json.read_text(encoding="utf-8"))
                prev_id = prev.get("session_id") or "prev"
                archive_dir = base / prev_id
                archive_dir.mkdir(parents=True, exist_ok=True)
                main_json.rename(archive_dir / "live_clock_24cycles_report.json")
                if main_md.exists():
                    main_md.rename(archive_dir / "live_clock_24cycles_report.md")
            except Exception:
                # fallback: rename by timestamp
                ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                try:
                    main_json.rename(base / f"live_clock_24cycles_report.{ts}.json")
                except Exception:
                    pass
        # write new
        main_json.write_text(json.dumps(session, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        paths["json"] = str(main_json)

        s = session["summary"]
        # Markdown with mandatory table §14
        lines: List[str] = []
        lines.append(f"# Sprint 6.2 — LIVE_CLOCK 24 CYCLES — {session_id}")
        lines.append("")
        lines.append(f"- Mode: LIVE_CLOCK  start {s.get('start')} → end {s.get('end')}  wall {s.get('session_wall_human')}")
        lines.append(f"- Config: universe {s.get('config',{}).get('universe_n')} executor {s.get('config',{}).get('executor')} cycles {s.get('config',{}).get('cycles')}")
        lines.append(f"- Qualifying: {s.get('qualifying_live_cycles')}/{s.get('total_cycles')}  pass {s.get('qualifying_pass')} fail {s.get('qualifying_fail')} nonq {s.get('non_qualifying_cycles')}  rate {s.get('next_candle_pass_rate')}")
        lines.append(f"- stale_as_fresh_total {s.get('stale_as_fresh_total')} orphan {s.get('orphan_workers')} duplicate_ok {s.get('no_duplicate_target_candle')} clock_integrity {s.get('all_target_candle_le_clock')}")
        lines.append(f"- Status: **{s.get('sprint62_status')}**  full_certified={s.get('full_live_clock_certified')}")
        lines.append("")
        # §14 mandatory table
        lines.append("| cycle | clock_start | target | close | decision_ready | next_start | latency | margin | qualifying | result |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for c in session["cycles"]:
            lines.append(f"| {c.get('cycle_index', c.get('cycle_id'))} | {c.get('clock_now_at_cycle_start')} | {c.get('target_candle')} | {c.get('target_candle_close')} | {c.get('decision_ready')} | {c.get('next_candle_start')} | {c.get('decision_latency_s')} | {c.get('deadline_margin_s')} | {c.get('live_clock_qualifying')} | {c.get('next_candle_result')} |")
        lines.append("")
        lines.append("## Early Emission §7")
        ee = s.get("early_emission", {})
        for k, v in ee.items():
            lines.append(f"- {k}: min {v.get('min')} p50 {v.get('p50')} p95 {v.get('p95')} max {v.get('max')} trend {v.get('trend')}")
        lines.append("")
        lines.append("## Performance Drift §8")
        pd_ = s.get("performance_drift", {})
        for k, v in pd_.items():
            lines.append(f"- {k}: first4_mean {v.get('first4_mean')} last4_mean {v.get('last4_mean')} drift {v.get('drift_last_minus_first')} trend {v.get('trend')} p50 {v.get('p50')} p95 {v.get('p95')} max {v.get('max')}")
        lines.append("")
        lines.append("## Resource Soak §9")
        rs = s.get("resource_soak", {})
        for k, v in rs.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
        lines.append("## Temporal Integrity §2-§3")
        ti = s.get("temporal_integrity", {})
        for k, v in ti.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
        if session.get("alerts"):
            lines.append("## Alerts")
            for a in session["alerts"]:
                lines.append(f"- {a['kind']} {a['severity']} cycle={a.get('cycle_id')} — {a.get('description')}")
            lines.append("")
        lines.append(f"Artifacts: `{paths['json']}`  session_id `{session_id}` (§13)")
        main_md.write_text("\n".join(lines), encoding="utf-8")
        paths["md"] = str(main_md)
        # SENSEI placeholder — runner will overwrite with full consolidated
        # ensure exists
        if not sensei.exists():
            sensei.write_text("\n".join(lines), encoding="utf-8")
            paths["sensei"] = str(sensei)
        else:
            paths["sensei"] = str(sensei)
        return paths
