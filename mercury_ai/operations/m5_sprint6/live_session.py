"""Sprint 6 — LiveSession orchestrator: 24+ ciclos M5, observabilidade, drift, soak.

Nao altera inteligencia. Usa M5OperationalRunner + M5Clock + temporal canonico.
Modo LIVE_CONTROLLED: dados reais, pipeline real, scheduler real, universe operacional,
nenhuma ordem enviada, decisoes persistidas, watchdog ativo, rollback disponivel.

Gera agregados Sprint 6 §21 e artefatos §21 + deadline formal §4.
"""
from __future__ import annotations

import json, os, time, uuid, hashlib, threading, traceback, queue
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_operational.clock import M5Clock
from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5, _ensure_utc
from mercury_ai.operations.ranking import FORMULA
from mercury_ai.config.universe import ALL_SYMBOLS

from .deadline import (
    evaluate_deadline, target_candle_close_for, next_candle_start_for,
    aggregate_deadlines, deadline_margin_s, decision_latency_s,
)
from .alerts import AlertSink


def _parse_cycle_wall(cycle_report: Dict[str, Any]) -> Optional[datetime]:
    # cycle reports tem cycle_start/cycle_end ISO wall (nao decision_ready)
    # decision_ready = cycle_start + first_fresh_decision_ms
    try:
        cs = cycle_report.get("cycle_start")
        if not cs:
            return None
        base = datetime.fromisoformat(str(cs).replace("Z", "+00:00"))
        # Use fresh timing quando disponivel; senao cycle_end
        ms = cycle_report.get("first_fresh_decision_ms")
        if ms is not None:
            return base + timedelta(milliseconds=float(ms))
        # fallback: cycle_end (completo)
        ce = cycle_report.get("cycle_end")
        if ce:
            return datetime.fromisoformat(str(ce).replace("Z", "+00:00"))
        return base
    except Exception:
        return None


def _hash_ranked(ranked: List[Dict[str, Any]]) -> str:
    """Fingerprint deterministico do ranking (sem inteligencia alterada)."""
    payload = json.dumps(ranked, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class LiveSessionConfig:
    universe_n: int = 12
    executor: str = "thread"  # thread para tests CI rapidos; process para baseline real
    workers: Optional[int] = None
    cycles: int = 24
    worker_timeout_s: float = 90.0
    cycle_timeout_s: float = 290.0
    mode: str = "LIVE_CONTROLLED"  # Sprint 6 §5


class LiveSession:
    """Executa sessao longa validando todos os gates Sprint 6."""

    def __init__(self, cfg: Optional[LiveSessionConfig] = None, m5_cfg: Optional[M5OperationalConfig] = None):
        self.cfg = cfg or LiveSessionConfig()
        self.m5_cfg = m5_cfg
        self.session_id = f"m5s6-{uuid.uuid4().hex[:8]}"
        self.start_wall: Optional[str] = None
        self.end_wall: Optional[str] = None
        self.alerts = AlertSink()
        self.cycle_reports: List[Dict[str, Any]] = []
        self.deadline_results: List[Dict[str, Any]] = []
        self._runner: Optional[M5OperationalRunner] = None
        self._clock: Optional[M5Clock] = None

    def _build_runner(self) -> M5OperationalRunner:
        n = min(self.cfg.universe_n, len(ALL_SYMBOLS))
        symbols = ALL_SYMBOLS[:n]
        base = self.m5_cfg or M5OperationalConfig.from_env()
        # override por LiveSessionConfig
        kw = base.to_dict()
        kw["worker_timeout_s"] = self.cfg.worker_timeout_s
        kw["cycle_timeout_s"] = self.cfg.cycle_timeout_s
        if self.cfg.executor:
            kw["executor"] = self.cfg.executor
        if self.cfg.workers is not None:
            if kw["executor"] == "process":
                kw["process_workers"] = self.cfg.workers
            else:
                kw["thread_workers"] = self.cfg.workers
        m5cfg = M5OperationalConfig(**kw)
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
        # 24 ciclos consecutivos simulados (blocking) — sem sleep M5 real, mas com
        # target_candle incremental de 5m e no-overlap garantido. Prova live clock
        # scheduling separado em teste dedicado (test_live_clock_alignment).
        target_start = floor_m5(datetime.now(timezone.utc))
        reports = self._clock.run_cycles_blocking(count=self.cfg.cycles, target_start=target_start)
        self.cycle_reports = reports

        # Avaliar cada ciclo para Sprint 6 §7 fields + deadline §4/§8
        enriched: List[Dict[str, Any]] = []
        for r in reports:
            # per-cycle fields exigidos Sprint 6 §7
            cycle_id = r.get("cycle_id")
            target_iso = r.get("target_candle")
            try:
                target_dt = datetime.fromisoformat(str(target_iso).replace("Z", "+00:00"))
            except Exception:
                target_dt = floor_m5(datetime.now(timezone.utc))
            tcc = target_candle_close_for(target_dt)
            ncs = next_candle_start_for(target_dt)
            # decision timestamps
            try:
                cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))
            except Exception:
                cs_dt = datetime.now(timezone.utc)
            try:
                ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None
            except Exception:
                ce_dt = None
            first_fresh_ms = r.get("first_fresh_decision_ms")
            first_top3_ms = r.get("first_top3_ms")
            complete_ms = r.get("cycle_complete_ms")
            # decision_ready_timestamp / next_candle_start / deadline_margin / decision_latency
            decision_ready_dt: Optional[datetime] = None
            if first_fresh_ms is not None:
                decision_ready_dt = cs_dt + timedelta(milliseconds=float(first_fresh_ms))
            elif ce_dt is not None:
                # sem fresh qualificavel — usar completo mas marcar nao-qualificavel
                decision_ready_dt = None  # para evaluate_deadline marcar non-qualifying
                # ainda registrar complete para observabilidade
            deadline = evaluate_deadline(target_dt, decision_ready_dt)
            # cycle_complete / cycle_duration
            cycle_duration_s = r.get("cycle_duration_s")
            # queue_max_depth, watchdog, orphan, status
            status = r.get("cycle_status")
            # alertas por ciclo
            if r.get("stale_as_fresh", 0) != 0:
                self.alerts.emit("FRESHNESS_VIOLATION", "CRITICAL", cycle_id,
                                 f"stale_as_fresh={r.get('stale_as_fresh')} (Sprint6 §9 bloqueante)",
                                 recovery_action="investigar pipeline; nao mascarar timestamp")
            if deadline.next_candle_ready is False:
                self.alerts.emit("DEADLINE_MISSED", "CRITICAL", cycle_id,
                                 f"deadline missed margin={deadline.deadline_margin_s:.2f}s target={target_iso}",
                                 extra={"deadline_margin_s": deadline.deadline_margin_s, "decision_latency_s": deadline.decision_latency_s})
            elif deadline.next_candle_ready is None:
                self.alerts.emit("STALE_DATA", "WARN", cycle_id,
                                 f"sem fresh para deadline (fresh={r.get('fresh')} stale={r.get('stale')} unavailable={r.get('assets_unavailable')})")
            if r.get("watchdog_events"):
                for e in r["watchdog_events"]:
                    self.alerts.emit("WATCHDOG_STALL", "WARN", cycle_id, str(e.get("message") or e), extra=e)
            if r.get("assets_timeout", 0) > 0:
                self.alerts.emit("WORKER_TIMEOUT", "WARN", cycle_id, f"timeouts={r.get('assets_timeout')}", extra={"per_asset_timeout": [k for k,v in r.get("per_asset",{}).items() if v.get("status")=="TIMEOUT"]})
            if r.get("cycle_status") == "CYCLE_TIMEOUT":
                self.alerts.emit("CYCLE_TIMEOUT", "WARN", cycle_id, f"cycle wall {cycle_duration_s}s hit {r.get('config',{}).get('cycle_timeout_s')}s")
            if r.get("queue_max_depth", 0) >= r.get("queue_maxsize", 128):
                self.alerts.emit("BOUNDED_QUEUE_FULL", "WARN", cycle_id, f"queue_max {r.get('queue_max_depth')}/{r.get('queue_maxsize')}")
            if any(v.get("status")=="ERROR" for v in r.get("per_asset", {}).values()):
                errs = [k for k,v in r.get("per_asset",{}).items() if v.get("status")=="ERROR"]
                self.alerts.emit("WORKER_CRASH", "WARN", cycle_id, f"errors={errs[:6]}")

            enriched_cycle = dict(r)  # copy
            # Sprint 6 §7 canonical per-cycle fields (aliases normalizados)
            enriched_cycle["target_candle_close"] = tcc.isoformat()
            enriched_cycle["cycle_start_wall"] = r.get("cycle_start")
            enriched_cycle["cycle_end_wall"] = r.get("cycle_end")
            enriched_cycle["first_fresh_decision"] = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))).isoformat() if first_fresh_ms is not None else None
            enriched_cycle["first_top3"] = (cs_dt + timedelta(milliseconds=float(first_top3_ms))).isoformat() if first_top3_ms is not None else None
            enriched_cycle["decision_ready"] = decision_ready_dt.isoformat() if decision_ready_dt else None
            enriched_cycle["next_candle_start"] = ncs.isoformat()
            enriched_cycle["decision_latency_s"] = deadline.decision_latency_s
            enriched_cycle["deadline_margin_s"] = deadline.deadline_margin_s
            enriched_cycle["next_candle_ready"] = ("PASS" if deadline.next_candle_ready is True else ("FAIL" if deadline.next_candle_ready is False else "NON_QUALIFYING"))
            enriched_cycle["cycle_complete"] = ce_dt.isoformat() if ce_dt else None
            enriched_cycle["cycle_duration"] = cycle_duration_s
            # legacy runner fields ja presentes: assets_total/completed/failed/timeout, fresh/stale/stale_as_fresh, queue_max_depth, watchdog_events, worker_restart_count, orphan_workers, status
            enriched_cycle["deadline_reason"] = deadline.reason
            enriched.append(enriched_cycle)
            self.deadline_results.append({
                "cycle_id": cycle_id,
                "target_candle": target_iso,
                "deadline": {
                    "target_candle_close": tcc.isoformat(),
                    "next_candle_start": ncs.isoformat(),
                    "decision_ready": decision_ready_dt.isoformat() if decision_ready_dt else None,
                    "decision_latency_s": deadline.decision_latency_s,
                    "deadline_margin_s": deadline.deadline_margin_s,
                    "next_candle_ready": enriched_cycle["next_candle_ready"],
                    "reason": deadline.reason,
                }
            })

        self.end_wall = datetime.now(timezone.utc).isoformat()

        # Soak / performance drift (§18 §19) — medido sobre reports enriquecidos
        mem_vals = [r.get("peak_memory_mb") for r in enriched if r.get("peak_memory_mb") is not None]
        mem_deltas = [r.get("memory_delta_mb") for r in enriched if r.get("memory_delta_mb") is not None]
        complete_s = [r.get("cycle_duration_s") for r in enriched if r.get("cycle_duration_s") is not None]
        first_fresh_s = [ (r.get("first_fresh_decision_ms") or 0)/1000 for r in enriched if r.get("first_fresh_decision_ms") is not None]
        first_top3_s = [ (r.get("first_top3_ms") or 0)/1000 for r in enriched if r.get("first_top3_ms") is not None]
        queue_maxes = [r.get("queue_max_depth", 0) for r in enriched]
        from .deadline import percentile
        agg = aggregate_deadlines([evaluate_deadline(
            datetime.fromisoformat(str(r["target_candle"]).replace("Z","+00:00")),
            (datetime.fromisoformat(str(r["cycle_start"]).replace("Z","+00:00")) + timedelta(milliseconds=float(r["first_fresh_decision_ms"]))) if r.get("first_fresh_decision_ms") is not None else None
        ) for r in enriched])

        orphan_total = sum(int(r.get("orphan_workers", 0) or 0) for r in enriched)
        watchdog_total = sum(len(r.get("watchdog_events") or []) for r in enriched)
        worker_restarts_total = sum(int(r.get("worker_restart_count", 0) or 0) for r in enriched)
        stale_as_fresh_total = sum(int(r.get("stale_as_fresh", 0) or 0) for r in enriched)

        # Data drift monitor (§17) — detecta mudanca de candle/data entre ciclos
        data_drift_events: List[Dict[str, Any]] = []
        for idx in range(1, len(enriched)):
            prev = enriched[idx-1]
            cur = enriched[idx]
            # target deve avancar exatamente 5m
            try:
                pt = datetime.fromisoformat(str(prev["target_candle"]).replace("Z","+00:00"))
                ct2 = datetime.fromisoformat(str(cur["target_candle"]).replace("Z","+00:00"))
                delta = (ct2 - pt).total_seconds()
                if abs(delta - 300) > 1:
                    data_drift_events.append({"cycle_id": cur["cycle_id"], "kind": "DATA_DRIFT", "detail": f"target gap {delta}s != 300s", "prev": prev["target_candle"], "cur": cur["target_candle"]})
            except Exception:
                pass

        # Observabilidade §21 — visao agregada
        cycles_expected = self.cfg.cycles
        cycles_completed = sum(1 for r in enriched if r.get("cycle_status") in ("COMPLETED", "CYCLE_TIMEOUT", "SHUTDOWN"))
        cycles_failed = cycles_expected - cycles_completed
        # Pass rates sobre ciclos qualificaveis
        pass_rate = agg.get("pass_rate")
        freshness_pass_rate = (sum(1 for r in enriched if r.get("stale_as_fresh",0)==0) / len(enriched)) if enriched else None

        summary: Dict[str, Any] = {
            "session_id": self.session_id,
            "mode": self.cfg.mode,
            "start": self.start_wall,
            "end": self.end_wall,
            "config": self.cfg.__dict__,
            "m5_config": (self._runner.config.to_dict() if self._runner else {}),
            "formula": FORMULA,
            "cycles_expected": cycles_expected,
            "cycles_completed": cycles_completed,
            "cycles_failed": cycles_failed,
            "cycles_recovered": 0,  # Sprint 6 §14 recovery §21 (nenhum auto-retry; SHUTDOWN/timeout ja contado)
            "next_candle_ready_pass_rate": pass_rate,
            "freshness_pass_rate": freshness_pass_rate,
            "stale_as_fresh_total": stale_as_fresh_total,
            "first_fresh_p50": percentile(first_fresh_s, 50) if first_fresh_s else None,
            "first_fresh_p95": percentile(first_fresh_s, 95) if first_fresh_s else None,
            "first_top3_p50": percentile(first_top3_s, 50) if first_top3_s else None,
            "first_top3_p95": percentile(first_top3_s, 95) if first_top3_s else None,
            "complete_p50": percentile(complete_s, 50) if complete_s else None,
            "complete_p95": percentile(complete_s, 95) if complete_s else None,
            "deadline_margin_p50": agg.get("deadline_margin_p50"),
            "deadline_margin_p95": agg.get("deadline_margin_p95"),
            "deadline_margin_min": agg.get("deadline_margin_min"),
            "deadline_margin_max": agg.get("deadline_margin_max"),
            "deadline_margin_mean": agg.get("deadline_margin_mean"),
            "queue_max": max(queue_maxes) if queue_maxes else 0,
            "peak_memory_mb": max(mem_vals) if mem_vals else None,
            "memory_initial_mb": mem_vals[0] if mem_vals else None,
            "memory_final_mb": mem_vals[-1] if mem_vals else None,
            "memory_delta_mb_last_first": (mem_deltas[-1] - mem_deltas[0]) if len(mem_deltas) >= 2 else None,
            "worker_restarts": worker_restarts_total,
            "watchdog_events": watchdog_total,
            "orphan_workers": orphan_total,
            "deadline_agg": agg,
            "data_drift_events": data_drift_events,
        }

        return {
            "session_id": self.session_id,
            "live_session_config": self.cfg.__dict__,
            "summary": summary,
            "cycles": enriched,
            "deadlines": self.deadline_results,
            "alerts": self.alerts.to_list(),
        }

    def write_artifacts(self, session: Dict[str, Any], out_dir: str = "reports/m5_sprint6") -> Dict[str, str]:
        base = Path(out_dir)
        base.mkdir(parents=True, exist_ok=True)
        paths: Dict[str, str] = {}
        p = base / "live_session_report.json"
        p.write_text(json.dumps(session, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        paths["json"] = str(p)
        # md sintetico §21
        md = base / "live_session_report.md"
        s = session["summary"]
        lines = [f"# Live Session Report — {session['session_id']}", ""]
        lines.append(f"- Mode: {s.get('mode')}  start {s.get('start')} → end {s.get('end')}")
        lines.append(f"- Cycles: expected {s['cycles_expected']} completed {s['cycles_completed']} failed {s['cycles_failed']}")
        lines.append(f"- next_candle_ready pass_rate: {s['next_candle_ready_pass_rate']}  freshness_pass_rate {s['freshness_pass_rate']}  stale_as_fresh_total {s['stale_as_fresh_total']}")
        lines.append(f"- first_fresh p50 {s['first_fresh_p50']} p95 {s['first_fresh_p95']}  first_top3 p50 {s['first_top3_p50']} p95 {s['first_top3_p95']}")
        lines.append(f"- complete p50 {s['complete_p50']} p95 {s['complete_p95']}  deadline_margin min {s['deadline_margin_min']} p50 {s['deadline_margin_p50']} p95 {s['deadline_margin_p95']}")
        lines.append(f"- queue_max {s['queue_max']}  peak_memory {s['peak_memory_mb']}  orphan {s['orphan_workers']}  watchdog {s['watchdog_events']}")
        # per-cycle table
        lines.append("")
        lines.append("| cycle | target | ready | margin | fresh | stale_as_fresh | wall | status |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for c in session["cycles"]:
            lines.append(f"| {c['cycle_id']} | {c['target_candle']} | {c.get('next_candle_ready')} | {c.get('deadline_margin_s')} | {c.get('fresh')} | {c.get('stale_as_fresh')} | {c.get('cycle_duration_s')} | {c.get('cycle_status')} |")
        if session.get("alerts"):
            lines.append("")
            lines.append("## Alerts")
            for a in session["alerts"]:
                lines.append(f"- {a['kind']} {a['severity']} cycle={a.get('cycle_id')} — {a.get('description')}")
        md.write_text("\n".join(lines), encoding="utf-8")
        paths["md"] = str(md)
        return paths
