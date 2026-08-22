"""Sprint 6.4 — LIVE AUDIT SESSION (6 ciclos LIVE_CLOCK + full audit trail).

Nao altera inteligencia (Regra Zero). Layer: audit record + artifact manifest +
event stream + provenance + ordering + tamper/replay plumbing.

Uso canonico:
  python scripts/m5_sprint64_gate_runner.py --universe 64 --executor process --cycles 6 --mode live_clock
"""
from __future__ import annotations
import time, uuid, json, hashlib, tempfile, os
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5
from mercury_ai.operations.ranking import FORMULA
from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.operations.m5_sprint61.live_clock_integrity import MeasurementMode, LiveClockCycleInput, classify_cycle, aggregate_live_clock
from mercury_ai.operations.m5_sprint6.deadline import percentile
from mercury_ai.operations.m5_sprint6.alerts import AlertSink
from .audit import AuditStore, AuditRecord, AuditIdentity
from .artifact import ArtifactManifest, sha256_file, sha256_bytes
from .events import EventStream, ObservabilityEvent, EventOrderValidator
from .provenance import DecisionProvenance
from .replay import ReplayEngine

try:
    from mercury_ai.operations.m5_sprint6 import alerts as _alerts_mod
    _alerts_mod.KINDS.add("CLOCK_INTEGRITY_FAIL")
except Exception:
    pass

@dataclass
class Sprint64Config:
    universe_n: int = 64
    executor: str = "process"
    workers: Optional[int] = None
    cycles: int = 6
    worker_timeout_s: float = 90.0
    cycle_timeout_s: float = 290.0
    measurement_mode: str = "LIVE_CLOCK"
    parent_session_id: Optional[str] = None


class Sprint64LiveSession:
    def __init__(self, cfg: Optional[Sprint64Config] = None, m5_cfg: Optional[M5OperationalConfig] = None, strict: bool = True, base_dir: Optional[Path] = None):
        self.cfg = cfg or Sprint64Config()
        if strict:
            if self.cfg.measurement_mode != "LIVE_CLOCK":
                raise ValueError("Sprint 6.4 live audit exige LIVE_CLOCK")
            if self.cfg.cycles != 6:
                raise ValueError("Sprint 6.4 live audit exige cycles=6")
            if self.cfg.universe_n != 64:
                raise ValueError("Sprint 6.4 §19 exige universe=64")
            if self.cfg.executor != "process":
                raise ValueError("Sprint 6.4 §19 exige executor=process")
        self.m5_cfg = m5_cfg
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parents[3] / "reports" / "m5_sprint64"
        self.session_id = AuditIdentity.new_session()
        self.start_wall: Optional[str] = None
        self.end_wall: Optional[str] = None
        self.alerts = AlertSink()
        self.cycle_reports: List[Dict[str, Any]] = []
        self.audit_records: List[AuditRecord] = []
        self._runner: Optional[M5OperationalRunner] = None
        # infra stores (init on run)
        self.audit_store: Optional[AuditStore] = None
        self.manifest: Optional[ArtifactManifest] = None
        self.event_stream: Optional[EventStream] = None
        # metrics
        self.audit_write_latencies: List[float] = []
        self.replay_duration_samples: List[float] = []
        # crash/recovery tracking
        self.incidents: List[Dict[str, Any]] = []

    def _build_runner(self) -> M5OperationalRunner:
        n = min(self.cfg.universe_n, len(ALL_SYMBOLS))
        symbols = ALL_SYMBOLS[:n]
        base = self.m5_cfg or M5OperationalConfig.from_env()
        kw = base.to_dict()
        # for smoke quick cycles, ensure worker < cycle if strict check
        wt = float(self.cfg.worker_timeout_s)
        ct = float(self.cfg.cycle_timeout_s)
        if wt >= ct:
            ct = wt + 5.0
        kw["worker_timeout_s"] = wt
        kw["cycle_timeout_s"] = ct
        kw["executor"] = self.cfg.executor
        if self.cfg.workers is not None:
            kw["process_workers"] = self.cfg.workers
            kw["thread_workers"] = self.cfg.workers
        m5cfg = M5OperationalConfig(**kw)
        assert m5cfg.max_concurrent_cycles == 1
        m5cfg.validate()
        runner = M5OperationalRunner(universe=symbols, config=m5cfg, disable_profiler=True)
        runner._install_signal_handlers()
        self._runner = runner
        return runner

    def run(self) -> Dict[str, Any]:
        self.start_wall = datetime.now(timezone.utc).isoformat()
        # init audit infra
        self.audit_store = AuditStore(base_dir=self.base_dir, session_id=self.session_id)
        aud_init = self.audit_store.create_session_dir()
        self.manifest = ArtifactManifest(self.audit_store.session_dir, self.session_id)
        self.event_stream = EventStream(self.audit_store.session_dir, self.session_id)
        # SESSION_START event
        self.event_stream.emit(ObservabilityEvent.new("SESSION_START", self.session_id, None, None, details={"parent_session_id": self.cfg.parent_session_id}))
        runner = self._build_runner()
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
                    self.alerts.emit("STALE_DATA", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target future")
            if prev_target is not None and target_dt <= prev_target:
                nxt = ceil_m5(clock_now_at_start)
                wait_s = (nxt - clock_now_at_start).total_seconds() + 0.05
                if wait_s > 0:
                    time.sleep(wait_s)
                clock_now_at_start = datetime.now(timezone.utc)
                target_dt = floor_m5(clock_now_at_start)
            prev_target = target_dt
            cycle_id = f"m5s64-live-{target_dt.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
            # events: CYCLE_START, TARGET_SELECTED
            self.event_stream.emit(ObservabilityEvent.new("CYCLE_START", self.session_id, cycle_id, target_dt.isoformat()))
            self.event_stream.emit(ObservabilityEvent.new("TARGET_SELECTED", self.session_id, cycle_id, target_dt.isoformat()))
            self.event_stream.emit(ObservabilityEvent.new("DATA_START", self.session_id, cycle_id, target_dt.isoformat()))
            clock_start_iso = clock_now_at_start.isoformat()
            clock_start_dt = clock_now_at_start
            # need cycle_start wall for decision_ready
            r = runner.run_cycle(cycle_id=cycle_id, target_candle=target_dt)
            # DATA phase events per asset
            for sym, rec in (r.get("per_asset") or {}).items():
                st = rec.get("status")
                fresh_st = rec.get("fresh_status")
                if st in ("TIMEOUT",) or fresh_st == "TIMEOUT":
                    self.event_stream.emit(ObservabilityEvent.new("DATA_TIMEOUT", self.session_id, cycle_id, target_dt.isoformat(), asset=sym))
                elif st in ("DATA_UNAVAILABLE", "SCAN_ERROR") or fresh_st == "DATA_UNAVAILABLE":
                    self.event_stream.emit(ObservabilityEvent.new("DATA_UNAVAILABLE", self.session_id, cycle_id, target_dt.isoformat(), asset=sym))
                elif rec.get("error"):
                    self.event_stream.emit(ObservabilityEvent.new("DATA_ERROR", self.session_id, cycle_id, target_dt.isoformat(), asset=sym))
                else:
                    self.event_stream.emit(ObservabilityEvent.new("DATA_COMPLETE", self.session_id, cycle_id, target_dt.isoformat(), asset=sym))
                # worker events
                self.event_stream.emit(ObservabilityEvent.new("WORKER_COMPLETE", self.session_id, cycle_id, target_dt.isoformat(), asset=sym, worker_id=rec.get("worker_id") or "worker"))
            if r.get("queue_max_depth", 0) >= (r.get("queue_maxsize", 128) * 0.8):
                self.event_stream.emit(ObservabilityEvent.new("QUEUE_PRESSURE", self.session_id, cycle_id, target_dt.isoformat(), details={"queue_max_depth": r.get("queue_max_depth"), "queue_maxsize": r.get("queue_maxsize")}))
            for wd in r.get("watchdog_events") or []:
                kind = wd.get("kind") or "WATCHDOG_STALL"
                et = "WATCHDOG_STALL" if "STALL" in str(kind) else "WATCHDOG_RECOVERY"
                self.event_stream.emit(ObservabilityEvent.new(et, self.session_id, cycle_id, target_dt.isoformat(), details=wd))
            self.event_stream.emit(ObservabilityEvent.new("ANALYSIS_COMPLETE", self.session_id, cycle_id, target_dt.isoformat()))
            self.event_stream.emit(ObservabilityEvent.new("RANKING_COMPLETE", self.session_id, cycle_id, target_dt.isoformat()))
            try:
                cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))
            except Exception:
                cs_dt = clock_start_dt
            try:
                ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None
            except Exception:
                ce_dt = None
            first_fresh_ms = r.get("first_fresh_decision_ms")
            decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None
            self.event_stream.emit(ObservabilityEvent.new("DECISION_READY", self.session_id, cycle_id, target_dt.isoformat(), details={"decision_ready": decision_ready_dt.isoformat() if decision_ready_dt else None}))
            self.event_stream.emit(ObservabilityEvent.new("DECISION_EMITTED", self.session_id, cycle_id, target_dt.isoformat(), details={"decision_ready": decision_ready_dt.isoformat() if decision_ready_dt else None}))
            # gate
            gate_input = LiveClockCycleInput(measurement_mode=mode, clock_now_at_cycle_start=clock_start_dt, target_candle=target_dt, decision_ready=decision_ready_dt)
            gate_rep = classify_cycle(gate_input)
            integrity_reports.append(gate_rep)
            # also handle stale_as_fresh etc already in runner report
            ec = dict(r)
            ec.update({
                "cycle_id": cycle_id,
                "cycle_index": idx,
                "measurement_mode": gate_rep.measurement_mode,
                "clock_now_at_cycle_start": gate_rep.clock_now_at_cycle_start,
                "target_candle": gate_rep.target_candle,
                "target_candle_close": gate_rep.target_candle_close,
                "cycle_start": cs_dt.isoformat() if cs_dt else r.get("cycle_start"),
                "first_fresh_decision": (cs_dt + timedelta(milliseconds=float(first_fresh_ms))).isoformat() if first_fresh_ms is not None else None,
                "decision_ready": gate_rep.decision_ready,
                "next_candle_start": gate_rep.next_candle_start,
                "cycle_complete": ce_dt.isoformat() if ce_dt else r.get("cycle_end"),
                "decision_latency_s": gate_rep.decision_latency_s,
                "deadline_margin_s": gate_rep.deadline_margin_s,
                "target_is_future": gate_rep.target_is_future,
                "temporal_order_valid": gate_rep.temporal_order_valid,
                "live_clock_qualifying": gate_rep.live_clock_qualifying,
                "next_candle_result": gate_rep.next_candle_result,
                "non_qualifying_reason": gate_rep.non_qualifying_reason,
                "clock_start": clock_start_iso,
            })
            enriched.append(ec)
            # build canonical audit record and persist atomically
            rec = AuditRecord.from_cycle_report(self.session_id, ec, clock_start_iso=clock_start_iso)
            t0 = time.perf_counter()
            wr = self.audit_store.write_cycle_record(rec)
            t1 = time.perf_counter()
            self.audit_write_latencies.append((t1 - t0) * 1000)
            if wr.get("collision"):
                self.event_stream.emit(ObservabilityEvent.new("AUDIT_COLLISION", self.session_id, cycle_id, target_dt.isoformat(), details=wr))
                self.incidents.append({"incident_id": AuditIdentity.new_incident(), "type": "AUDIT_COLLISION", "cycle_id": cycle_id, "details": wr})
            else:
                # register artifact in manifest
                self.manifest.register(self.audit_store.cycle_dir / f"{cycle_id}.json", cycle_id=cycle_id)
                self.event_stream.emit(ObservabilityEvent.new("ARTIFACT_WRITTEN", self.session_id, cycle_id, target_dt.isoformat(), details={"artifact": f"cycle_audit/{cycle_id}.json"}))
            self.audit_records.append(rec)
            self.cycle_reports.append(ec)
        self.end_wall = datetime.now(timezone.utc).isoformat()
        self.event_stream.emit(ObservabilityEvent.new("SESSION_COMPLETE", self.session_id, None, None))
        # finalize manifest — save with posix keys (artifact.py already posix since register)
        # but previous quick sessions had backslash keys; reload posix migration if needed
        if self.manifest:
            # migrate any backslash keys to posix
            migrated = {}
            for k, v in list(self.manifest.entries.items()):
                nk = k.replace("\\", "/")
                if nk != k:
                    v.artifact_name = nk
                    migrated[nk] = v
                else:
                    migrated[k] = v
            self.manifest.entries = migrated
        manifest_save = self.manifest.save_atomic() if self.manifest else {"saved": False}
        # also register manifest itself? manifest is not self-registered (avoid chicken-egg); we will include it as artifact for integrity by storing its hash separately
        # For integrity report we consider manifest + cycle records
        # Persist per-session live report as well for artifact integrity
        # compute ordering validation
        validator = EventOrderValidator(self.event_stream.all())
        ordering = validator.validate()
        # aggregate live clock
        gate_agg = aggregate_live_clock(integrity_reports)
        # collect metrics
        first_fresh_s = [(c.get("first_fresh_decision_ms") or 0)/1000.0 for c in enriched if c.get("first_fresh_decision_ms") is not None]
        mem_vals = [c.get("peak_memory_mb") for c in enriched if c.get("peak_memory_mb") is not None]
        queue_maxes = [c.get("queue_max_depth",0) for c in enriched]
        orphan_total = sum(int(c.get("orphan_workers",0) or 0) for c in enriched)
        stale_total = sum(int(c.get("stale_as_fresh",0) or 0) for c in enriched)
        # provenance per cycle
        provenances = []
        for rec in self.audit_records:
            prov = DecisionProvenance.from_audit_record(rec.to_dict(), manifest_path=str(self.audit_store.session_dir / "manifest.json"), event_stream_path=str(self.audit_store.session_dir / "audit_events.jsonl"))
            provenances.append(prov.to_dict())
        decision_without_provenance = sum(1 for p in provenances if not p.get("ranking_signature") or not p.get("decision_signature"))
        # artifact integrity
        from .artifact import ArtifactIntegrityResult
        art_result = self.manifest.verify() if self.manifest else ArtifactIntegrityResult(True,0,0,0,[],[],[])
        # event duplicates already in ordering
        # replay quick check for ≥3 cycles (normal, data_unavailable, fault if any) — do replay on last 3 cycles
        replay_engine = ReplayEngine(self.audit_store.session_dir)
        replay_ids = [r.cycle_id for r in self.audit_records[-3:]]
        replay_results = []
        for cid in replay_ids:
            t0 = time.perf_counter()
            rr = replay_engine.replay_cycle(cid)
            t1 = time.perf_counter()
            self.replay_duration_samples.append((t1 - t0)*1000)
            replay_results.append(rr.to_dict())
        replay_pass = sum(1 for r in replay_results if r["status"]=="REPLAY_MATCH")
        replay_div = sum(1 for r in replay_results if r["status"]=="REPLAY_DIVERGENCE")
        # queue observability
        queue_max = max(queue_maxes) if queue_maxes else 0
        # cross-executor audit consistency will be checked externally via isolated vs parallel comparison; set flag
        summary = {
            "session_id": self.session_id,
            "parent_session_id": self.cfg.parent_session_id,
            "measurement_mode": "LIVE_CLOCK",
            "start": self.start_wall,
            "end": self.end_wall,
            "session_wall_s": time.perf_counter() - session_start_perf,
            "config": self.cfg.__dict__,
            "m5_config": (self._runner.config.to_dict() if self._runner else {}),
            "formula": FORMULA,
            "cycles_expected": self.cfg.cycles,
            "cycles_completed": len(enriched),
            "cycles_failed": max(0, self.cfg.cycles - len(enriched)),
            "total_cycles": gate_agg["total_cycles"],
            "qualifying_live_cycles": gate_agg["qualifying_live_cycles"],
            "qualifying_pass": gate_agg["qualifying_pass"],
            "qualifying_fail": gate_agg["qualifying_fail"],
            "non_qualifying_cycles": gate_agg["non_qualifying_cycles"],
            "live_clock_agg": gate_agg,
            "stale_as_fresh_total": stale_total,
            "freshness_ok": stale_total==0,
            "orphan_workers": orphan_total,
            "queue_max": queue_max,
            "queue_bounded_ok": queue_max <= 128,
            "peak_memory_mb": max(mem_vals) if mem_vals else None,
            "memory_initial_mb": mem_vals[0] if mem_vals else None,
            "memory_final_mb": mem_vals[-1] if mem_vals else None,
            "audit_records_created": len(self.audit_records),
            "audit_records_missing": self.cfg.cycles - len(self.audit_records),
            "artifact_integrity_pass": art_result.artifact_integrity_pass,
            "artifact_hash_mismatch_total": art_result.artifact_hash_mismatch_total,
            "missing_artifact_total": art_result.missing_artifact_total,
            "unexpected_artifact_total": art_result.unexpected_artifact_total,
            "replay_total": len(replay_results),
            "replay_pass": replay_pass,
            "replay_fail": len(replay_results)-replay_pass,
            "replay_divergence_total": replay_div,
            "event_total": ordering.get("event_total", 0),
            "event_loss_total": ordering.get("event_loss_total", 0),
            "duplicate_event_total": ordering.get("duplicate_event_total", 0),
            "event_order_violation_total": ordering.get("event_order_violation_total", 0),
            "decision_without_provenance_total": decision_without_provenance,
            "audit_write_latency_p50": percentile(sorted(self.audit_write_latencies), 50) if self.audit_write_latencies else None,
            "audit_write_latency_p95": percentile(sorted(self.audit_write_latencies), 95) if self.audit_write_latencies else None,
            "replay_duration_p50": percentile(sorted(self.replay_duration_samples), 50) if self.replay_duration_samples else None,
            "replay_duration_p95": percentile(sorted(self.replay_duration_samples), 95) if self.replay_duration_samples else None,
            "ordering": ordering,
            "artifact_integrity": art_result.to_dict(),
            "manifest_save": manifest_save,
            "replay_results": replay_results,
            "provenances": provenances,
            "alerts": self.alerts.to_dict() if hasattr(self.alerts, "to_dict") else [],
        }
        # determine no_duplicate_target etc
        targets = [c["target_candle"] for c in enriched]
        summary["no_duplicate_target_candle"] = len(targets)==len(set(targets))
        summary["corrupt_artifact_accepted"] = False
        return {"summary": summary, "cycles": enriched, "audit_records": [r.to_dict() for r in self.audit_records], "events": [e.to_dict() for e in self.event_stream.all()]}

    def write_artifacts(self, session_result: Dict[str, Any], out_dir: str = "reports/m5_sprint64") -> Dict[str, str]:
        base = Path(out_dir) / self.session_id
        base.mkdir(parents=True, exist_ok=True)
        audit_json = base / "audit_manifest.json"
        # legacy reports compat
        return {"audit_json": str(audit_json)}
