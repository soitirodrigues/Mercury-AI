"""Sprint 6.1 — LiveSession61 com certificacao honesta ACCELERATED vs LIVE_CLOCK.

Nao altera inteligencia. Usa M5OperationalRunner + ranking canonico + FreshnessGate.

Modos:
  ACCELERATED_SOAK — run_cycles_blocking rapido (target +=5m artificial), valido para
                     reliability/soak/concurrency, mas NON_QUALIFYING para LIVE_CLOCK.
  LIVE_CLOCK — ciclos ligados ao relogio UTC real: aguarda fronteira M5 real,
               captura clock_now, garante target <= clock_now, valida temporal order.

Invariantes §3 e classificacao via LiveClockIntegrityGate.
"""
from __future__ import annotations

import json, time, uuid, hashlib
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
from .live_clock_integrity import (
    MeasurementMode, LiveClockCycleInput, classify_cycle, aggregate_live_clock,
)
from mercury_ai.operations.m5_sprint6.deadline import evaluate_deadline, aggregate_deadlines, percentile
from mercury_ai.operations.m5_sprint6.alerts import AlertSink


@dataclass
class Sprint61Config:
    universe_n: int = 12
    executor: str = "thread"
    workers: Optional[int] = None
    cycles: int = 24
    worker_timeout_s: float = 90.0
    cycle_timeout_s: float = 290.0
    measurement_mode: str = "ACCELERATED_SOAK"  # ACCELERATED_SOAK | LIVE_CLOCK


class Sprint61LiveSession:
    def __init__(self, cfg: Optional[Sprint61Config] = None, m5_cfg: Optional[M5OperationalConfig] = None):
        self.cfg = cfg or Sprint61Config()
        # validate mode
        if self.cfg.measurement_mode not in ("ACCELERATED_SOAK", "LIVE_CLOCK"):
            raise ValueError("measurement_mode must be ACCELERATED_SOAK | LIVE_CLOCK")
        self.m5_cfg = m5_cfg
        self.session_id = f"m5s61-{uuid.uuid4().hex[:8]}"
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

    def _wait_for_next_boundary(self) -> datetime:
        """Aguarda proxima fronteira M5 real (poll 0.2s) e retorna clock_now apos fronteira."""
        while True:
            now = datetime.now(timezone.utc)
            nxt = ceil_m5(now)
            wait_s = (nxt - now).total_seconds()
            if wait_s <= 0.05:
                # ja estamos logo apos fronteira, retornar
                time.sleep(0.05)
                return datetime.now(timezone.utc)
            # sleep em chunks para nao bloquear shutdown indefinidamente
            # mas sprint61 nao tem shutdown externo aqui; simples sleep
            chunk = min(wait_s, 0.5)
            time.sleep(chunk)
            # loop recalcula nxt a partir do novo now (evita acumulo sleep(300) incorreto)

    def run(self) -> Dict[str, Any]:
        self.start_wall = datetime.now(timezone.utc).isoformat()
        runner = self._build_runner()
        assert self._clock is not None

        mode = MeasurementMode(self.cfg.measurement_mode)
        enriched: List[Dict[str, Any]] = []
        integrity_reports: List[Any] = []

        if mode == MeasurementMode.ACCELERATED_SOAK:
            # Caminho acelerado: sem espera real, target artificial +5m
            target_start = floor_m5(datetime.now(timezone.utc))
            reports = self._clock.run_cycles_blocking(count=self.cfg.cycles, target_start=target_start)
            for r in reports:
                # Para cada ciclo, precisamos de clock_now_at_cycle_start REAL (nao target)
                # Em modo acelerado, clock_now eh o cycle_start wall real, que sera < target para ciclos >0
                # Isso propositadamente gera NON_QUALIFYING_FUTURE_TARGET / ACCELERATED
                try:
                    cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))
                except Exception:
                    cs_dt = datetime.now(timezone.utc)
                try:
                    target_dt = datetime.fromisoformat(str(r.get("target_candle")).replace("Z", "+00:00"))
                except Exception:
                    target_dt = floor_m5(cs_dt)
                first_fresh_ms = r.get("first_fresh_decision_ms")
                decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
                # deadline legacy (para compatibilidade)
                dl = evaluate_deadline(target_dt, decision_ready_dt)
                # gate com modo acelerado
                gate_input = LiveClockCycleInput(
                    measurement_mode=mode,
                    clock_now_at_cycle_start=cs_dt,
                    target_candle=target_dt,
                    decision_ready=decision_ready_dt,
                )
                gate_rep = classify_cycle(gate_input)
                integrity_reports.append(gate_rep)
                # alertas honestos
                if gate_rep.next_candle_result == "NON_QUALIFYING_ACCELERATED":
                    self.alerts.emit("STALE_DATA", "WARN", r.get("cycle_id"), f"ACCELERATED_SOAK cycle non-qualifying for LIVE_CLOCK (target {gate_rep.target_candle})")
                # enriquecer
                ec = dict(r)
                ec.update({
                    "measurement_mode": gate_rep.measurement_mode,
                    "clock_now_at_cycle_start": gate_rep.clock_now_at_cycle_start,
                    "target_candle": gate_rep.target_candle,
                    "target_candle_close": gate_rep.target_candle_close,
                    "target_is_future": gate_rep.target_is_future,
                    "decision_ready": gate_rep.decision_ready,
                    "decision_before_candle_close": gate_rep.decision_before_candle_close,
                    "decision_latency_s": gate_rep.decision_latency_s,
                    "next_candle_start": gate_rep.next_candle_start,
                    "deadline_margin_s": gate_rep.deadline_margin_s,
                    "temporal_order_valid": gate_rep.temporal_order_valid,
                    "live_clock_qualifying": gate_rep.live_clock_qualifying,
                    "next_candle_result": gate_rep.next_candle_result,
                    "non_qualifying_reason": gate_rep.non_qualifying_reason,
                    "legacy_next_candle_ready": ("PASS" if dl.next_candle_ready is True else ("FAIL" if dl.next_candle_ready is False else "NON_QUALIFYING")),
                })
                # freshness alerts etc (reuse sprint6 logic)
                if r.get("stale_as_fresh", 0) != 0:
                    self.alerts.emit("FRESHNESS_VIOLATION", "CRITICAL", r.get("cycle_id"), f"stale_as_fresh={r.get('stale_as_fresh')}")
                enriched.append(ec)
        else:  # LIVE_CLOCK
            # Ciclos reais, um a um, sincronizados com UTC
            # Para evitar duplicar candle, esperamos fronteira antes de cada ciclo quando necessario
            prev_target: Optional[datetime] = None
            for idx in range(self.cfg.cycles):
                # Capturar clock_now no inicio do ciclo (antes de definir target)
                # Se nao for primeiro ciclo, aguardar proxima fronteira real para nao duplicar
                if idx > 0 and prev_target is not None:
                    # Esperar ate que floor_m5(clock_now) > prev_target
                    attempts = 0
                    while attempts < 600:  # max ~5min (600*0.5s)
                        now_probe = datetime.now(timezone.utc)
                        cand = floor_m5(now_probe)
                        if cand > prev_target:
                            break
                        nxt = ceil_m5(now_probe)
                        wait_s = (nxt - now_probe).total_seconds()
                        # Dorme ate proxima fronteira + pequena margem
                        sleep_for = min(max(wait_s + 0.05, 0.05), 1.0)
                        time.sleep(sleep_for)
                        attempts += 1
                    # fallback: se ainda nao avancou, forcar
                clock_now_at_start = datetime.now(timezone.utc)
                target_dt = floor_m5(clock_now_at_start)
                # Garantir nao futuro (por definicao floor <= now, entao ok)
                # mas se clock_now for exatamente na fronteira, floor==clock_now, ainda ok (target <= clock)
                # Evitar duplicata: se target == prev, esperar proxima
                if prev_target is not None and target_dt <= prev_target:
                    nxt = ceil_m5(clock_now_at_start)
                    wait_s = (nxt - clock_now_at_start).total_seconds() + 0.05
                    if wait_s > 0:
                        time.sleep(wait_s)
                    clock_now_at_start = datetime.now(timezone.utc)
                    target_dt = floor_m5(clock_now_at_start)
                prev_target = target_dt
                cycle_id = f"m5s61-live-{target_dt.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
                # Executar ciclo operacional real (pipeline real)
                r = runner.run_cycle(cycle_id=cycle_id, target_candle=target_dt)
                # decision_ready a partir de first_fresh
                try:
                    cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))
                except Exception:
                    cs_dt = clock_now_at_start
                first_fresh_ms = r.get("first_fresh_decision_ms")
                decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
                # Gate
                gate_input = LiveClockCycleInput(
                    measurement_mode=mode,
                    clock_now_at_cycle_start=clock_now_at_start,
                    target_candle=target_dt,
                    decision_ready=decision_ready_dt,
                )
                gate_rep = classify_cycle(gate_input)
                integrity_reports.append(gate_rep)
                ec = dict(r)
                ec.update({
                    "measurement_mode": gate_rep.measurement_mode,
                    "clock_now_at_cycle_start": gate_rep.clock_now_at_cycle_start,
                    "target_candle": gate_rep.target_candle,
                    "target_candle_close": gate_rep.target_candle_close,
                    "target_is_future": gate_rep.target_is_future,
                    "decision_ready": gate_rep.decision_ready,
                    "decision_before_candle_close": gate_rep.decision_before_candle_close,
                    "decision_latency_s": gate_rep.decision_latency_s,
                    "next_candle_start": gate_rep.next_candle_start,
                    "deadline_margin_s": gate_rep.deadline_margin_s,
                    "temporal_order_valid": gate_rep.temporal_order_valid,
                    "live_clock_qualifying": gate_rep.live_clock_qualifying,
                    "next_candle_result": gate_rep.next_candle_result,
                    "non_qualifying_reason": gate_rep.non_qualifying_reason,
                    "legacy_next_candle_ready": ("PASS" if evaluate_deadline(target_dt, decision_ready_dt).next_candle_ready is True else ("FAIL" if evaluate_deadline(target_dt, decision_ready_dt).next_candle_ready is False else "NON_QUALIFYING")),
                })
                if ec["next_candle_result"] == "QUALIFYING_FAIL":
                    self.alerts.emit("DEADLINE_MISSED", "CRITICAL", cycle_id, f"deadline missed margin={gate_rep.deadline_margin_s}")
                elif gate_rep.next_candle_result.startswith("NON_QUALIFYING"):
                    self.alerts.emit("STALE_DATA", "WARN", cycle_id, gate_rep.non_qualifying_reason or "non-qualifying")
                if r.get("stale_as_fresh", 0) != 0:
                    self.alerts.emit("FRESHNESS_VIOLATION", "CRITICAL", cycle_id, f"stale_as_fresh={r.get('stale_as_fresh')}")
                if r.get("watchdog_events"):
                    for e in r["watchdog_events"]:
                        self.alerts.emit("WATCHDOG_STALL", "WARN", cycle_id, str(e.get("message") or e), extra=e)
                enriched.append(ec)
                # Impedir overlap ja garantido por runner guard; mas tambem garantir nao iniciar proximo antes de terminar
                # (ja estamos sequencial)

        self.end_wall = datetime.now(timezone.utc).isoformat()
        self.cycle_reports = enriched

        # Agregacoes
        # Legacy deadline agg (para compatibilidade)
        legacy_results = []
        for ec in enriched:
            try:
                td = datetime.fromisoformat(str(ec["target_candle"]).replace("Z", "+00:00"))
            except Exception:
                td = floor_m5(datetime.now(timezone.utc))
            try:
                dr = datetime.fromisoformat(str(ec["decision_ready"]).replace("Z", "+00:00")) if ec.get("decision_ready") else None
            except Exception:
                dr = None
            legacy_results.append(evaluate_deadline(td, dr))
        legacy_agg = aggregate_deadlines(legacy_results)

        # Gate agg correto (§8)
        gate_objs = integrity_reports
        gate_agg = aggregate_live_clock(gate_objs)

        # Soak metrics
        mem_vals = [r.get("peak_memory_mb") for r in enriched if r.get("peak_memory_mb") is not None]
        mem_deltas = [r.get("memory_delta_mb") for r in enriched if r.get("memory_delta_mb") is not None]
        complete_s = [r.get("cycle_duration_s") for r in enriched if r.get("cycle_duration_s") is not None]
        first_fresh_s = [(r.get("first_fresh_decision_ms") or 0)/1000 for r in enriched if r.get("first_fresh_decision_ms") is not None]
        first_top3_s = [(r.get("first_top3_ms") or 0)/1000 for r in enriched if r.get("first_top3_ms") is not None]
        queue_maxes = [r.get("queue_max_depth", 0) for r in enriched]

        orphan_total = sum(int(r.get("orphan_workers", 0) or 0) for r in enriched)
        watchdog_total = sum(len(r.get("watchdog_events") or []) for r in enriched)
        worker_restarts_total = sum(int(r.get("worker_restart_count", 0) or 0) for r in enriched)
        stale_as_fresh_total = sum(int(r.get("stale_as_fresh", 0) or 0) for r in enriched)

        cycles_expected = self.cfg.cycles
        cycles_completed = sum(1 for r in enriched if r.get("cycle_status") in ("COMPLETED", "CYCLE_TIMEOUT", "SHUTDOWN"))
        cycles_failed = cycles_expected - cycles_completed

        summary: Dict[str, Any] = {
            "session_id": self.session_id,
            "measurement_mode": self.cfg.measurement_mode,
            "mode": self.cfg.measurement_mode,  # alias
            "start": self.start_wall,
            "end": self.end_wall,
            "config": self.cfg.__dict__,
            "m5_config": (self._runner.config.to_dict() if self._runner else {}),
            "formula": FORMULA,
            "cycles_expected": cycles_expected,
            "cycles_completed": cycles_completed,
            "cycles_failed": cycles_failed,
            # Legacy (enganação antiga) — manter para comparacao
            "legacy_next_candle_ready_pass_rate": legacy_agg.get("pass_rate"),
            "legacy_deadline_agg": legacy_agg,
            # Gate honesto §8
            "total_cycles": gate_agg["total_cycles"],
            "qualifying_live_cycles": gate_agg["qualifying_live_cycles"],
            "qualifying_pass": gate_agg["qualifying_pass"],
            "qualifying_fail": gate_agg["qualifying_fail"],
            "non_qualifying_cycles": gate_agg["non_qualifying_cycles"],
            "next_candle_pass_rate": gate_agg["next_candle_pass_rate"],
            "live_clock_certification": gate_agg["certification"] if self.cfg.measurement_mode == "LIVE_CLOCK" else "NON_QUALIFYING",
            "live_clock_agg": gate_agg,
            # Soak
            "freshness_pass_rate": (sum(1 for r in enriched if r.get("stale_as_fresh",0)==0)/len(enriched)) if enriched else None,
            "stale_as_fresh_total": stale_as_fresh_total,
            "first_fresh_p50": percentile(first_fresh_s, 50) if first_fresh_s else None,
            "first_fresh_p95": percentile(first_fresh_s, 95) if first_fresh_s else None,
            "first_top3_p50": percentile(first_top3_s, 50) if first_top3_s else None,
            "first_top3_p95": percentile(first_top3_s, 95) if first_top3_s else None,
            "complete_p50": percentile(complete_s, 50) if complete_s else None,
            "complete_p95": percentile(complete_s, 95) if complete_s else None,
            "deadline_margin_p50": gate_agg.get("min_deadline_margin_valid"),  # legacy compat
            "queue_max": max(queue_maxes) if queue_maxes else 0,
            "peak_memory_mb": max(mem_vals) if mem_vals else None,
            "memory_initial_mb": mem_vals[0] if mem_vals else None,
            "memory_final_mb": mem_vals[-1] if mem_vals else None,
            "memory_delta_mb_last_first": (mem_deltas[-1] - mem_deltas[0]) if len(mem_deltas) >=2 else None,
            "worker_restarts": worker_restarts_total,
            "watchdog_events": watchdog_total,
            "orphan_workers": orphan_total,
            "min_deadline_margin_valid": gate_agg.get("min_deadline_margin_valid"),
            "min_latency_valid": gate_agg.get("min_latency_valid"),
            "max_latency_valid": gate_agg.get("max_latency_valid"),
        }

        return {
            "session_id": self.session_id,
            "live_session_config": self.cfg.__dict__,
            "summary": summary,
            "cycles": enriched,
            "deadlines": [r.to_dict() for r in gate_objs],
            "alerts": self.alerts.to_list(),
        }

    def write_artifacts(self, session: Dict[str, Any], out_dir: str = "reports/m5_sprint61") -> Dict[str, str]:
        base = Path(out_dir)
        base.mkdir(parents=True, exist_ok=True)
        paths: Dict[str, str] = {}
        # nome depende do modo
        mode = session["summary"].get("measurement_mode") or self.cfg.measurement_mode
        suffix = "accelerated_soak" if mode == "ACCELERATED_SOAK" else "live_clock"
        p = base / f"{suffix}_report.json"
        p.write_text(json.dumps(session, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        paths["json"] = str(p)
        md = base / f"{suffix}_report.md"
        s = session["summary"]
        lines = [f"# Sprint 6.1 Report — {mode} — {session['session_id']}", ""]
        lines.append(f"- Mode: {mode}  start {s.get('start')} → end {s.get('end')}")
        lines.append(f"- Cycles: expected {s['cycles_expected']} completed {s['cycles_completed']}")
        lines.append(f"- Qualifying live: {s['qualifying_live_cycles']}/{s['total_cycles']}  pass {s['qualifying_pass']} fail {s['qualifying_fail']} non-qualifying {s['non_qualifying_cycles']}")
        lines.append(f"- Live clock certification: {s.get('live_clock_certification')}  pass_rate {s.get('next_candle_pass_rate')}")
        lines.append(f"- Legacy (misleading) pass_rate: {s.get('legacy_next_candle_ready_pass_rate')} (inclui futuros — NAO usar)")
        lines.append(f"- stale_as_fresh_total {s['stale_as_fresh_total']}  orphan {s['orphan_workers']}")
        lines.append("")
        lines.append("| cycle | target | clock_now | latency | margin | qualifying | result | fresh |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for c in session["cycles"]:
            lines.append(f"| {c['cycle_id']} | {c.get('target_candle')} | {c.get('clock_now_at_cycle_start')} | {c.get('decision_latency_s')} | {c.get('deadline_margin_s')} | {c.get('live_clock_qualifying')} | {c.get('next_candle_result')} | {c.get('fresh')} |")
        if session.get("alerts"):
            lines.append("")
            lines.append("## Alerts")
            for a in session["alerts"]:
                lines.append(f"- {a['kind']} {a['severity']} cycle={a.get('cycle_id')} — {a.get('description')}")
        md.write_text("\n".join(lines), encoding="utf-8")
        paths["md"] = str(md)
        return paths
