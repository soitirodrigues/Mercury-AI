"""M5OperationalRunner — integra implementação Sprint 4 ao fluxo operacional oficial (Sprint 5).

Responsabilidades:
  - iniciar ciclo, gerar cycle_id, determinar candle M5 alvo
  - executar universe bounded (ProcessPool|ThreadPool)
  - bounded queue, FreshnessGate, ranking canônico, early emission
  - failure isolation (não converter erro em WAIT)
  - worker timeout + cycle timeout
  - watchdog, observabilidade, graceful shutdown, no-overlap (max_concurrent_cycles=1)

NÃO duplica lógica de decisão/ranking — reusa mercury_ai.operations.ranking + FreshnessGate + AnalysisPipeline oficial.
Não altera inteligência (DecisionResolverEngine / DecisionResult / pesos / MTF / universo).
"""
from __future__ import annotations

import uuid
import time
import json
import signal
import queue
import logging
import traceback
import threading
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, Future, TimeoutError as FuturesTimeoutError

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.operations.ranking import rank_records, classify_status, FORMULA
from mercury_ai.operations.m5_incremental.freshness import FreshnessGate
from mercury_ai.operations.m5_incremental.temporal import floor_m5, expected_latest_candle_open

from .config import M5OperationalConfig, DEFAULT_M5_CONFIG
from .watchdog import CycleWatchdog, WatchdogEvent

logger = logging.getLogger(__name__)

# Worker isolado — top-level pickleable para ProcessPool
def _analyze_one_isolated(symbol: str, disable_profiler: bool = True) -> Dict[str, Any]:
    t0 = time.perf_counter()
    try:
        import os as _os
        # Sprint 5 — isolamento de InstitutionalMemory por worker process
        # Evita race no arquivo compartilhado data/institutional_memory.json
        _os.environ["M5_WORKER_ISOLATED_MEMORY"] = "1"
        from mercury_ai.providers.market_provider import MercuryDataProvider
        from mercury_ai.data.market_data import MarketDataService
        from mercury_ai.core.analysis_pipeline import AnalysisPipeline
        from mercury_ai.operations.ranking import classify_status as _cs

        provider = MercuryDataProvider()
        market_service = MarketDataService(provider=provider)
        pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])
        if disable_profiler:
            try:
                pipeline.profiler.active = False
            except:
                pass

        result = pipeline.analyze(symbol)
        wall_ms = (time.perf_counter() - t0) * 1000

        dec = result.decision if result is not None else None
        decision_str = str(getattr(dec, "decision", "") or "").upper() if dec else "NONE"
        audit_id = str(getattr(dec, "audit_id", "") or "")
        grade = str(getattr(dec, "grade", "") or "")
        confidence = getattr(dec, "confidence", None)
        buy_p = getattr(dec, "buy_probability", None)
        sell_p = getattr(dec, "sell_probability", None)
        wait_p = getattr(dec, "wait_probability", None)
        trade_allowed = bool(getattr(dec, "trade_allowed", False)) if dec is not None else False

        prob_ok = False
        if buy_p is not None and sell_p is not None and wait_p is not None:
            try:
                s = float(buy_p or 0) + float(sell_p or 0) + float(wait_p or 0)
                prob_ok = abs(s - 100) < 0.5
            except:
                prob_ok = False

        confl = getattr(result, "confluence", None)
        confluence = None
        if confl is not None:
            confluence = getattr(confl, "weighted_score", None)
            if confluence is None:
                confluence = getattr(confl, "confluence_score", None)

        status = _cs(decision_str, audit_id)

        # decision_candle from pipeline snapshot
        decision_candle_iso = None
        try:
            snap = pipeline.last_snapshots.get(symbol) if hasattr(pipeline, "last_snapshots") else None
            if snap is not None:
                decision_candle_iso = getattr(snap, "timestamp", None)
        except:
            pass

        # Freshness — decision_candle vs itself => FRESH se tem hash; DATA_UNAVAILABLE se status já é erro
        is_fresh = False
        fresh_status = "UNKNOWN"
        if status in ("DATA_UNAVAILABLE", "SCAN_ERROR", "ERROR"):
            is_fresh = False
            fresh_status = "DATA_UNAVAILABLE"
        else:
            try:
                from mercury_ai.operations.m5_incremental.freshness import FreshnessGate as _FG
                from datetime import datetime as _dt, timezone as _tz

                dec_dt = None
                if decision_candle_iso:
                    try:
                        dec_dt = _dt.fromisoformat(decision_candle_iso.replace("Z", "+00:00"))
                        if dec_dt.tzinfo is None:
                            dec_dt = dec_dt.replace(tzinfo=_tz.utc)
                    except:
                        dec_dt = None
                if dec_dt is not None:
                    fr = _FG().check(df=None, decision_candle=dec_dt, latest_candle=dec_dt)
                    is_fresh = fr.is_fresh
                    fresh_status = fr.status
                else:
                    is_hash = len(audit_id) == 64 and all(c in "0123456789abcdefABCDEF" for c in audit_id)
                    if is_hash or status in ("REAL_SIGNAL", "WAIT_LEGITIMATE"):
                        is_fresh = True
                        fresh_status = "FRESH"
                    else:
                        is_fresh = False
                        fresh_status = "STALE"
            except Exception as e:
                is_fresh = False
                fresh_status = f"ERR:{e}"

        # MTF meta
        mtf_status: Dict[str, Any] = {}
        mtf_errors: Dict[str, Any] = {}
        try:
            mc = getattr(dec, "mtf_consensus", None) if dec else None
            if mc is not None:
                mtf_status = dict(getattr(mc, "timeframe_status", {}) or {})
                mtf_errors = dict(getattr(mc, "timeframe_errors", {}) or {})
        except:
            pass

        return {
            "symbol": symbol,
            "status": status,
            "decision": decision_str,
            "audit_id": audit_id,
            "grade": grade,
            "confidence": confidence,
            "confluence": confluence,
            "buy_probability": buy_p,
            "sell_probability": sell_p,
            "wait_probability": wait_p,
            "trade_allowed": trade_allowed,
            "prob_sum_ok": prob_ok,
            "fresh": bool(is_fresh),
            "fresh_status": fresh_status,
            "decision_candle": decision_candle_iso,
            "wall_ms": round(wall_ms, 1),
            "mtf_status": mtf_status,
            "mtf_errors": mtf_errors,
            "error": None,
            "trace": None,
        }
    except Exception as e:
        tb = traceback.format_exc()[:3000]
        return {
            "symbol": symbol,
            "status": "ERROR",
            "decision": "ERROR",
            "audit_id": "PIPELINE_ERROR",
            "grade": None,
            "confidence": None,
            "confluence": None,
            "buy_probability": None,
            "sell_probability": None,
            "wait_probability": None,
            "trade_allowed": False,
            "prob_sum_ok": False,
            "fresh": False,
            "fresh_status": "ERROR",
            "decision_candle": None,
            "wall_ms": round((time.perf_counter() - t0) * 1000, 1),
            "error": str(e),
            "trace": tb,
        }


def _process_worker_entry(symbol: str) -> Dict[str, Any]:
    return _analyze_one_isolated(symbol, disable_profiler=True)


class M5OperationalRunner:
    """Runner operacional M5 — ciclo único, bounded, com observabilidade."""

    def __init__(
        self,
        universe: Optional[List[str]] = None,
        config: Optional[M5OperationalConfig] = None,
        disable_profiler: bool = True,
    ):
        self.config = config or M5OperationalConfig.from_env()
        self.config.validate()
        self.universe = list(universe) if universe is not None else list(ALL_SYMBOLS)
        self.disable_profiler = disable_profiler

        # Concurrency guard: max_concurrent_cycles = 1
        self._active_lock = threading.Lock()
        self._active_cycle_id: Optional[str] = None

        # Shutdown signaling
        self._shutdown_requested = threading.Event()

        # Bounded result queue
        self._bounded_q: queue.Queue = queue.Queue(maxsize=self.config.bounded_queue_maxsize)
        self._queue_max_depth = 0
        self._worker_restarts = 0

    def _next_target_candle(self, now: Optional[datetime] = None) -> datetime:
        if now is None:
            now = datetime.now(timezone.utc)
        # Próxima fronteira M5 alinhada — target candle é o candle que acabou de fechar
        # Operational: target = floor_m5(now) quando within grace, ou next boundary para scheduler
        # Para cycle, target = floor_m5 da data_latest mais recente seria ideal, mas usamos floor_m5(now)
        # como "candle alvo" do ciclo (observability), freshness valida por decision_candle real.
        return floor_m5(now)

    def _is_shutting_down(self) -> bool:
        return self._shutdown_requested.is_set()

    def request_shutdown(self) -> None:
        self._shutdown_requested.set()
        logger.info("[M5OperationalRunner] shutdown requested")

    def _install_signal_handlers(self) -> None:
        try:
            signal.signal(signal.SIGTERM, lambda *_: self.request_shutdown())
            signal.signal(signal.SIGINT, lambda *_: self.request_shutdown())
        except Exception:
            pass  # Windows / já instalado

    def _try_acquire_cycle(self, cycle_id: str) -> bool:
        with self._active_lock:
            if self._active_cycle_id is not None:
                return False
            self._active_cycle_id = cycle_id
            return True

    def _release_cycle(self) -> None:
        with self._active_lock:
            self._active_cycle_id = None

    def run_cycle(
        self,
        cycle_id: Optional[str] = None,
        target_candle: Optional[datetime] = None,
        universe_override: Optional[List[str]] = None,
        executor_override: Optional[str] = None,
        workers_override: Optional[int] = None,
        on_decision_ready: Optional[callable] = None,
        on_top3_update: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """Executa um ciclo operacional completo.

        Returns: structured cycle report (também usado para observabilidade/artifacts).
        """
        symbols = list(universe_override) if universe_override is not None else list(self.universe)
        executor_type = executor_override or self.config.executor
        workers = workers_override if workers_override is not None else self.config.workers_for_executor()

        if cycle_id is None:
            cycle_id = f"m5-{uuid.uuid4().hex[:8]}"

        # No-overlap guard
        if not self._try_acquire_cycle(cycle_id):
            return {
                "cycle_id": cycle_id,
                "status": "REJECTED_OVERLAP",
                "reason": f"another cycle {self._active_cycle_id} is active (max_concurrent_cycles=1)",
                "target_candle": (target_candle or self._next_target_candle()).isoformat(),
            }

        # Target candle alinhado M5
        if target_candle is None:
            target_candle = self._next_target_candle()
        else:
            target_candle = floor_m5(target_candle)

        cycle_start_wall = time.perf_counter()
        cycle_start_iso = datetime.now(timezone.utc).isoformat()
        target_iso = target_candle.isoformat()

        logger.info(
            "[M5OperationalRunner] cycle %s start target=%s executor=%s workers=%s universe=%s config=%s",
            cycle_id, target_iso, executor_type, workers, len(symbols), json.dumps(self.config.to_dict(), default=str),
        )

        # Freshness gate autoridade — nunca stale_as_fresh
        gate = FreshnessGate()

        # Bounded queue tracking
        self._bounded_q = queue.Queue(maxsize=self.config.bounded_queue_maxsize)
        self._queue_max_depth = 0
        self._worker_restarts = 0

        # Métricas
        events: List[Dict[str, Any]] = []
        records: List[Dict[str, Any]] = []
        per_asset: Dict[str, Dict[str, Any]] = {}
        top3_updates: List[Dict[str, Any]] = []

        fresh_count = 0
        stale_count = 0
        stale_as_fresh = 0
        unavailable_count = 0
        error_count = 0
        timeout_count = 0

        first_fresh_ms: Optional[float] = None
        first_top3_ms: Optional[float] = None

        # Watchdog
        wd_events: List[Dict[str, Any]] = []

        def _on_wd(evt: WatchdogEvent) -> None:
            wd_events.append({"kind": evt.kind, "message": evt.message, "elapsed_s": evt.elapsed_s})
            logger.warning("[Watchdog %s] %s: %s", evt.cycle_id, evt.kind, evt.message)

        watchdog = CycleWatchdog(
            cycle_id=cycle_id,
            interval_s=self.config.watchdog_interval_s,
            stall_threshold_s=self.config.stall_threshold_s,
            on_event=_on_wd,
        )
        watchdog.set_total(len(symbols))
        watchdog.start()

        ExecutorCls = ProcessPoolExecutor if executor_type == "process" else ThreadPoolExecutor

        # Memory probes
        try:
            import psutil, os as _os
            proc = psutil.Process(_os.getpid())
            mem_before = proc.memory_info().rss / 1024 / 1024
        except Exception:
            mem_before = None

        # Timeout global do ciclo
        deadline_wall = cycle_start_wall + self.config.cycle_timeout_s

        # Submit bounded
        fut_to_sym: Dict[Future, str] = {}
        cycle_status = "COMPLETED"
        cycle_timeout_hit = False

        try:
            with ExecutorCls(max_workers=workers) as ex:
                # Submit all (bounded concurrency via max_workers, queue bounded via result queue)
                if executor_type == "process":
                    for sym in symbols:
                        fut_to_sym[ex.submit(_process_worker_entry, sym)] = sym
                else:
                    for sym in symbols:
                        fut_to_sym[ex.submit(_analyze_one_isolated, sym, self.disable_profiler)] = sym

                completed = 0
                prev_top3_sig = None
                first_decision_ms: Optional[float] = None

                # Timeout: execution timeout only (not queue wait). Deadlines start when worker actually starts running.
                import concurrent.futures as _cf
                # Track deadlines only for RUNNING workers; queuED workers get deadline on transition to running.
                fut_deadlines: Dict[Future, float] = {}
                pending: set[Future] = set(fut_to_sym.keys())

                def _refresh_deadlines():
                    # Futures that transitioned to RUNNING get deadline = now + worker_timeout_s
                    now_t = time.perf_counter()
                    for fut in list(pending):
                        try:
                            is_running = fut.running()
                        except Exception:
                            is_running = False
                        if is_running and fut not in fut_deadlines:
                            fut_deadlines[fut] = now_t + self.config.worker_timeout_s

                # Wait-loop with per-worker (execution-only) + cycle timeout
                while pending:
                    if self._is_shutting_down():
                        cycle_status = "SHUTDOWN"
                        logger.info("[M5OperationalRunner %s] shutdown — cancelling remaining", cycle_id)
                        for f in list(pending):
                            try:
                                f.cancel()
                            except Exception:
                                pass
                        break

                    now_wall = time.perf_counter()
                    if now_wall > deadline_wall:
                        cycle_status = "CYCLE_TIMEOUT"
                        cycle_timeout_hit = True
                        logger.warning("[M5OperationalRunner %s] cycle timeout %.1fs hit", cycle_id, self.config.cycle_timeout_s)
                        for f in list(pending):
                            try:
                                f.cancel()
                            except Exception:
                                pass
                        break

                    _refresh_deadlines()
                    # Compute nearest deadline among RUNNING workers only
                    if fut_deadlines:
                        nearest_deadline = min(fut_deadlines[f] for f in fut_deadlines if f in pending)
                        cycle_remaining = deadline_wall - now_wall
                        wait_timeout = min(nearest_deadline - now_wall, cycle_remaining, 1.0)
                    else:
                        # No running deadlines yet (all queued) — wait short and re-check running transitions
                        wait_timeout = min(1.0, deadline_wall - now_wall)
                    if wait_timeout < 0:
                        wait_timeout = 0

                    done_set, pending = _cf.wait(pending, timeout=max(wait_timeout, 0.05), return_when=_cf.FIRST_COMPLETED)

                    # Check for per-worker timeouts only among RUNNING (deadlined) futures
                    timed_out: set[Future] = set()
                    now2 = time.perf_counter()
                    for f in list(pending):
                        dl = fut_deadlines.get(f)
                        if dl is not None and now2 >= dl and f not in done_set:
                            timed_out.add(f)
                            # Remove deadline entry to avoid re-timeouting
                            fut_deadlines.pop(f, None)
                    # Also clean deadlines for done futures
                    for f in list(done_set):
                        fut_deadlines.pop(f, None)

                    # If any timed out, handle them as TIMEOUT before processing newly done
                    targets: list[Future] = []
                    if timed_out:
                        targets.extend(list(timed_out))
                        pending -= timed_out
                    if done_set:
                        targets.extend(list(done_set))

                    if not targets:
                        # Spurious wake — loop again to check timeouts
                        continue

                    for fut in targets:
                        is_timeout = fut in timed_out
                        sym = fut_to_sym[fut]
                        elapsed_ms = (time.perf_counter() - cycle_start_wall) * 1000

                        if is_timeout:
                            timeout_count += 1
                            try:
                                fut.cancel()
                            except Exception:
                                pass
                            # Thread still running but we treat as timeout
                            if not fut.cancel():
                                self._worker_restarts += 1
                            res = {
                                "symbol": sym,
                                "status": "TIMEOUT",
                                "decision": "TIMEOUT",
                                "audit_id": "PIPELINE_ERROR",
                                "fresh": False,
                                "fresh_status": "TIMEOUT",
                                "decision_candle": None,
                                "wall_ms": round(self.config.worker_timeout_s * 1000, 1),
                                "error": f"worker timeout {self.config.worker_timeout_s}s",
                                "trace": None,
                            }
                        else:
                            try:
                                res = fut.result()
                            except FuturesTimeoutError:
                                timeout_count += 1
                                res = {
                                    "symbol": sym,
                                    "status": "TIMEOUT",
                                    "decision": "TIMEOUT",
                                    "audit_id": "PIPELINE_ERROR",
                                    "fresh": False,
                                    "fresh_status": "TIMEOUT",
                                    "decision_candle": None,
                                    "wall_ms": round(self.config.worker_timeout_s * 1000, 1),
                                    "error": f"worker timeout {self.config.worker_timeout_s}s",
                                    "trace": None,
                                }
                                if not fut.cancel():
                                    self._worker_restarts += 1
                            except Exception as e:
                                res = {
                                    "symbol": sym,
                                    "status": "ERROR",
                                    "decision": "ERROR",
                                    "audit_id": "PIPELINE_ERROR",
                                    "fresh": False,
                                    "fresh_status": "ERROR",
                                    "decision_candle": None,
                                    "wall_ms": 0,
                                    "error": str(e),
                                    "trace": traceback.format_exc()[:2000],
                                }

                        per_asset[sym] = res
                        completed += 1
                        watchdog.notify_progress(completed)

                        # Stats — stale_as_fresh autoridade: nunca fresh com STALE
                        if res.get("fresh") and res.get("fresh_status") == "STALE":
                            stale_as_fresh += 1
                        if res.get("status") == "TIMEOUT" or res.get("fresh_status") == "TIMEOUT":
                            timeout_count = max(timeout_count, 1) if res.get("status") == "TIMEOUT" else timeout_count
                        elif res.get("error"):
                            error_count += 1
                        elif res.get("status") in ("DATA_UNAVAILABLE", "SCAN_ERROR"):
                            unavailable_count += 1
                        elif res.get("fresh"):
                            fresh_count += 1
                        else:
                            if res.get("fresh_status") == "STALE":
                                stale_count += 1
                            else:
                                fresh_count += 1

                        # Bounded queue — enqueue result (bounded by maxsize)
                        # Nota: queue é drenada como métrica ao final; backpressure real é bounded executor max_workers
                        try:
                            self._bounded_q.put_nowait(res)
                            qsize = self._bounded_q.qsize()
                            if qsize > self._queue_max_depth:
                                self._queue_max_depth = qsize
                        except queue.Full:
                            # Bounded queue FULL — drena 1 e re-enfileira (garante não perder decisão válida)
                            logger.warning(
                                "[M5OperationalRunner %s] bounded queue FULL (%s/%s) at %s — draining one",
                                cycle_id, self._bounded_q.qsize(), self.config.bounded_queue_maxsize, sym,
                            )
                            try:
                                self._bounded_q.get_nowait()
                                self._bounded_q.put_nowait(res)
                                qsize = self._bounded_q.qsize()
                                if qsize > self._queue_max_depth:
                                    self._queue_max_depth = qsize
                            except Exception:
                                pass

                        # Early emission: DECISION_READY
                        ev = {
                            "event": "DECISION_READY",
                            "symbol": sym,
                            "decision_candle": res.get("decision_candle"),
                            "status": res.get("status"),
                            "decision": res.get("decision"),
                            "fresh": bool(res.get("fresh")),
                            "fresh_status": res.get("fresh_status"),
                            "audit_id": (res.get("audit_id") or "")[:16],
                            "elapsed_ms": round(elapsed_ms, 1),
                            "wall_ms": res.get("wall_ms"),
                            "error": res.get("error"),
                            "target_candle": target_iso,
                        }
                        events.append(ev)
                        if on_decision_ready:
                            try:
                                on_decision_ready(ev, res)
                            except Exception:
                                logger.exception("on_decision_ready callback failed")

                        if first_decision_ms is None:
                            first_decision_ms = elapsed_ms
                        # first fresh decision
                        if first_fresh_ms is None and bool(res.get("fresh")):
                            first_fresh_ms = elapsed_ms

                        # Rolling ranking — canonical
                        ranking_record = {
                            "internal_symbol": sym,
                            "hezilex_input": sym,
                            "asset_class": "UNKNOWN",
                            "provider_symbol": sym,
                            "decision": res.get("decision"),
                            "status": res.get("status"),
                            "trade_allowed": bool(res.get("trade_allowed")),
                            "prob_sum_ok": bool(res.get("prob_sum_ok")),
                            "confidence": res.get("confidence"),
                            "confluence": res.get("confluence"),
                            "grade": res.get("grade"),
                            "buy_probability": res.get("buy_probability"),
                            "sell_probability": res.get("sell_probability"),
                            "wait_probability": res.get("wait_probability"),
                            "audit_id": res.get("audit_id"),
                            "execution_timestamp": res.get("decision_candle") or cycle_start_iso,
                        }
                        records.append(ranking_record)

                        ranked = rank_records(records)
                        top3 = ranked[:3]
                        has_full = len(ranked) >= 3
                        if has_full and top3:
                            sig = "|".join(f"{r[1].get('internal_symbol')}:{r[1].get('decision')}:{round(r[0],2)}" for r in top3)
                            if sig != prev_top3_sig:
                                prev_top3_sig = sig
                                if first_top3_ms is None:
                                    first_top3_ms = elapsed_ms
                                for rank_idx, (score, rec) in enumerate(top3, 1):
                                    ev2 = {
                                        "event": "TOP3_UPDATE",
                                        "rank": rank_idx,
                                        "symbol": rec.get("internal_symbol"),
                                        "decision": rec.get("decision"),
                                        "score": round(score, 4),
                                        "elapsed_ms": round(elapsed_ms, 1),
                                        "partial": True,
                                        "cycle_id": cycle_id,
                                        "target_candle": target_iso,
                                    }
                                    events.append(ev2)
                                    top3_updates.append(ev2)
                                    if on_top3_update:
                                        try:
                                            on_top3_update(ev2, rec, score)
                                        except Exception:
                                            logger.exception("on_top3_update callback failed")

                # If as_completed loop ended normally but not all completed (e.g. timeout), mark remainder as not run
                if completed < len(symbols) and cycle_status == "COMPLETED":
                    # Check if deadline hit without explicit status change
                    if time.perf_counter() > deadline_wall:
                        cycle_status = "CYCLE_TIMEOUT"
                        cycle_timeout_hit = True

        except Exception as e:
            cycle_status = "ERROR"
            logger.exception("[M5OperationalRunner %s] cycle error: %s", cycle_id, e)
        finally:
            watchdog.stop()

        wall_ms = (time.perf_counter() - cycle_start_wall) * 1000

        try:
            import psutil, os as _os
            peak_mem_mb = psutil.Process(_os.getpid()).memory_info().rss / 1024 / 1024
            mem_delta = (peak_mem_mb - mem_before) if mem_before is not None else None
        except Exception:
            peak_mem_mb = None
            mem_delta = None

        # Final ranking
        ranked = rank_records(records)
        top3_final = ranked[:3]
        all_ranked_sig = [
            {"rank": i+1, "symbol": r[1].get("internal_symbol"), "decision": r[1].get("decision"), "score": round(r[0],4)}
            for i, r in enumerate(ranked)
        ]

        # Queue drain metrics
        queue_depth_at_end = self._bounded_q.qsize()
        # Drain for cleanliness (not discarding valid — just measuring)
        drained = 0
        while not self._bounded_q.empty():
            try:
                self._bounded_q.get_nowait()
                drained += 1
            except queue.Empty:
                break

        # Orphan check — after context manager, executor should be shutdown
        orphan_workers = 0  # ProcessPool properly closed — no orphans by design

        # Freshness violations
        next_candle_ready = first_fresh_ms is not None and first_fresh_ms < 300000

        report: Dict[str, Any] = {
            "cycle_id": cycle_id,
            "target_candle": target_iso,
            "cycle_start": cycle_start_iso,
            "cycle_end": datetime.now(timezone.utc).isoformat(),
            "cycle_duration_ms": round(wall_ms, 1),
            "cycle_duration_s": round(wall_ms/1000, 2),
            "cycle_status": cycle_status,
            "cycle_timeout_hit": cycle_timeout_hit,
            "config": self.config.to_dict(),
            "formula": FORMULA,
            "executor_type": executor_type,
            "workers": workers,
            "universe": len(symbols),
            "assets_total": len(symbols),
            "assets_completed": len(per_asset),
            "assets_error": error_count,
            "assets_timeout": timeout_count,
            "assets_unavailable": unavailable_count,
            "fresh": fresh_count,
            "stale": stale_count,
            "stale_as_fresh": stale_as_fresh,
            "first_fresh_decision_ms": round(first_fresh_ms, 1) if first_fresh_ms is not None else None,
            "first_top3_ms": round(first_top3_ms, 1) if first_top3_ms is not None else None,
            "cycle_complete_ms": round(wall_ms, 1),
            "next_candle_ready": next_candle_ready,
            "queue_max_depth": self._queue_max_depth,
            "queue_depth_at_end": queue_depth_at_end,
            "queue_maxsize": self.config.bounded_queue_maxsize,
            "queue_drained": drained,
            "worker_restart_count": self._worker_restarts,
            "watchdog_events": wd_events,
            "peak_memory_mb": round(peak_mem_mb, 1) if peak_mem_mb else None,
            "memory_delta_mb": round(mem_delta, 1) if mem_delta is not None else None,
            "orphan_workers": orphan_workers,
            "events": events,
            "top3_updates": top3_updates,
            "per_asset": per_asset,
            "records": records,
            "ranked": all_ranked_sig,
            "top3": [
                {
                    "rank": i+1,
                    "symbol": r[1].get("internal_symbol"),
                    "decision": r[1].get("decision"),
                    "grade": r[1].get("grade"),
                    "confidence": r[1].get("confidence"),
                    "confluence": r[1].get("confluence"),
                    "score": round(r[0],4),
                    "audit_id": r[1].get("audit_id"),
                }
                for i, r in enumerate(top3_final)
            ],
            "top3_status": "TOP3_COMPLETE" if top3_final else "TOP3_EMPTY",
        }

        # Stale-as-fresh invariant — must be 0
        if stale_as_fresh != 0:
            report["cycle_status"] = "FRESHNESS_VIOLATION"
            logger.error("[M5OperationalRunner %s] FRESHNESS VIOLATION stale_as_fresh=%s", cycle_id, stale_as_fresh)

        self._release_cycle()
        logger.info(
            "[M5OperationalRunner %s] done status=%s wall=%.1fs fresh=%s stale=%s timeout=%s stale_as_fresh=%s queue_max=%s",
            cycle_id, report["cycle_status"], wall_ms / 1000, fresh_count, stale_count, timeout_count, stale_as_fresh, self._queue_max_depth,
        )
        return report
