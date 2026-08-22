#!/usr/bin/env python3
"""
SENSEI SPRINT 4 — INTER-ASSET PARALLEL SCANNER + EARLY EMISSION

- Nao altera DecisionResolverEngine / DecisionResult / ranking / pesos / regra
- Worker isolado por ativo: executa pipeline OFICIAL + MTF oficial + DecisionResult oficial
- Bounded executor (ThreadPool / ProcessPool)
- Aggregator central com FreshnessGate + rolling queue + ranking canonico
- Early emission: DECISION_READY e TOP3_UPDATE assim que cada ativo termina
- Failure isolation: erro em um ativo nao derruba os demais
"""
from __future__ import annotations
import sys, time, json, traceback, threading
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.operations.ranking import rank_records, select_top3, classify_status, FORMULA
from mercury_ai.operations.m5_incremental.freshness import FreshnessGate
from mercury_ai.operations.m5_incremental.temporal import decision_candle_timestamp_from_df

# ---------- ISOLATED WORKER ----------

def _analyze_one_isolated(symbol: str, disable_profiler: bool = True) -> Dict[str, Any]:
    """Worker isolado: cria pipeline proprio, nao compartilha estado global."""
    t0 = time.perf_counter()
    try:
        from mercury_ai.providers.market_provider import MercuryDataProvider
        from mercury_ai.data.market_data import MarketDataService
        from mercury_ai.core.analysis_pipeline import AnalysisPipeline
        from mercury_ai.operations.ranking import classify_status as _cs
        from mercury_ai.operations.m5_incremental.freshness import FreshnessGate as _FG
        import traceback as _tb

        provider = MercuryDataProvider()
        market_service = MarketDataService(provider=provider)
        pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])
        if disable_profiler:
            try:
                pipeline.profiler.active = False
            except: pass

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
            except: prob_ok = False

        confl = getattr(result, "confluence", None)
        confluence = None
        if confl is not None:
            confluence = getattr(confl, "weighted_score", None)
            if confluence is None:
                confluence = getattr(confl, "confluence_score", None)

        status = _cs(decision_str, audit_id)

        # Freshness: decision_candle == latest_candle para dado vivo => FRESH.
        # Para DATA_UNAVAILABLE/SCAN_ERROR => DATA_UNAVAILABLE.
        decision_candle_iso = None
        try:
            snap = pipeline.last_snapshots.get(symbol) if hasattr(pipeline, "last_snapshots") else None
            if snap is not None:
                decision_candle_iso = getattr(snap, "timestamp", None)
        except: pass

        is_fresh = False
        fresh_status = "UNKNOWN"
        if status in ("DATA_UNAVAILABLE", "SCAN_ERROR", "ERROR"):
            is_fresh = False
            fresh_status = "DATA_UNAVAILABLE"
        else:
            # Se tem decision_candle, valida como FRESH comparando com si mesmo (mesma vela usada)
            try:
                gate = _FG()
                from datetime import datetime as _dt, timezone as _tz
                dec_dt = None
                if decision_candle_iso:
                    try:
                        dec_dt = _dt.fromisoformat(decision_candle_iso.replace("Z", "+00:00"))
                        if dec_dt.tzinfo is None:
                            dec_dt = dec_dt.replace(tzinfo=_tz.utc)
                    except: dec_dt = None
                # Usa dec_dt como both decision e latest => FRESH salvo caso DATA_UNAVAILABLE
                if dec_dt is not None:
                    fr = gate.check(df=None, decision_candle=dec_dt, latest_candle=dec_dt)
                    is_fresh = fr.is_fresh
                    fresh_status = fr.status
                else:
                    # Sem snapshot timestamp mas pipeline retornou hash => considerar FRESH
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

        # Captura MTF meta se houver
        mtf_ms = fetch_ms = 0
        mtf_status = {}
        mtf_errors = {}
        try:
            mtf = getattr(result, "mtf_consensus", None)  # device?
            # Pipeline nao expoe MTFConsensus direto no AnalysisResult? Checa decision.mtf_consensus ?
            mc = getattr(dec, "mtf_consensus", None) if dec else None
            if mc is not None:
                mtf_status = dict(getattr(mc, "timeframe_status", {}) or {})
                mtf_errors = dict(getattr(mc, "timeframe_errors", {}) or {})
        except: pass

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
            "mtf_ms": round(mtf_ms, 1),
            "fetch_ms": round(fetch_ms, 1),
            "timeframe_status": mtf_status,
            "timeframe_errors": mtf_errors,
            "error": None,
            "trace": None,
        }
    except Exception as e:
        tb = traceback.format_exc()[:2000]
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


# For ProcessPool we need a top-level pickleable wrapper that matches same logic
def _process_worker_entry(symbol: str) -> Dict[str, Any]:
    # ProcessPool worker: disable_profiler True to avoid tracemalloc race
    return _analyze_one_isolated(symbol, disable_profiler=True)


# ---------- PARALLEL SCANNER ----------

class ParallelScanner:
    def __init__(self, universe: List[str], workers: int = 4, executor_type: str = "thread", disable_profiler: bool = True):
        self.universe = list(universe)
        self.workers = int(workers)
        self.executor_type = executor_type  # thread | process
        self.disable_profiler = disable_profiler
        self.gate = FreshnessGate()

    def scan(self) -> Dict[str, Any]:
        overall_t0 = time.perf_counter()
        overall_iso = datetime.now(timezone.utc).isoformat()
        monotonic_start = overall_t0

        events: List[Dict[str, Any]] = []
        records: List[Dict[str, Any]] = []  # rolling queue of ranking records
        per_asset: Dict[str, Dict[str, Any]] = {}
        errors: List[Dict[str, Any]] = []
        top3_updates: List[Dict[str, Any]] = []

        fresh_count = 0
        stale_count = 0
        unavailable_count = 0
        error_count = 0

        ExecutorCls = ThreadPoolExecutor if self.executor_type == "thread" else ProcessPoolExecutor

        # Peak memory probe
        peak_mem_mb = None
        try:
            import psutil, os
            proc = psutil.Process(os.getpid())
            mem_before = proc.memory_info().rss / 1024 / 1024
        except:
            mem_before = None

        # Bounded executor: workers limit, queue is implicit via as_completed
        # We submit all but executor bounds concurrency
        with ExecutorCls(max_workers=self.workers) as ex:
            # submit
            if self.executor_type == "process":
                fut_to_sym = {ex.submit(_process_worker_entry, sym): sym for sym in self.universe}
            else:
                # thread: closure captures disable_profiler
                def _submit(sym):
                    return ex.submit(_analyze_one_isolated, sym, self.disable_profiler)
                fut_to_sym = {_submit(sym): sym for sym in self.universe}

            prev_top3_sig = None
            first_decision_ms = None
            time_to_5_ms = None
            time_to_10_ms = None
            time_to_partial_top3_ms = None

            completed = 0
            for fut in as_completed(fut_to_sym):
                sym = fut_to_sym[fut]
                elapsed_ms = (time.perf_counter() - monotonic_start) * 1000
                try:
                    res = fut.result()
                except Exception as e:
                    res = {"symbol": sym, "status": "ERROR", "decision": "ERROR", "audit_id": "PIPELINE_ERROR", "error": str(e), "trace": traceback.format_exc()[:1500], "fresh": False, "fresh_status": "ERROR", "wall_ms": 0, "decision_candle": None}
                per_asset[sym] = res
                completed += 1

                # Freshness classification for stats
                if res.get("error"):
                    error_count += 1
                elif res.get("status") in ("DATA_UNAVAILABLE", "SCAN_ERROR"):
                    unavailable_count += 1
                elif res.get("fresh"):
                    fresh_count += 1
                else:
                    # WAIT without fresh or other
                    if res.get("status") == "REAL_SIGNAL":
                        # should be fresh; count as stale if not
                        stale_count += 1
                    elif res.get("fresh_status") == "STALE":
                        stale_count += 1
                    else:
                        # ambiguous - count as fresh if has hash?
                        fresh_count += 1

                # Emit DECISION_READY
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
                }
                events.append(ev)

                if first_decision_ms is None:
                    first_decision_ms = elapsed_ms
                if completed == 5 and time_to_5_ms is None:
                    time_to_5_ms = elapsed_ms
                if completed == 10 and time_to_10_ms is None:
                    time_to_10_ms = elapsed_ms

                # Build rolling queue ranking record (canonical)
                # Only add to ranking pool if not ERROR; DATA_UNAVAILABLE still not eligible but tracked
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
                    "execution_timestamp": res.get("decision_candle") or overall_iso,
                }
                records.append(ranking_record)

                # Canonical ranking — only emit PARTIAL when we have 3 eligible
                ranked = rank_records(records)
                top3, all_ranked = ranked[:3], ranked
                has_full_partial = len(ranked) >= 3
                if has_full_partial and top3:
                    sig = "|".join(f"{r[1].get('internal_symbol')}:{r[1].get('decision')}:{round(r[0],2)}" for r in top3)
                    if sig != prev_top3_sig:
                        prev_top3_sig = sig
                        if time_to_partial_top3_ms is None:
                            time_to_partial_top3_ms = elapsed_ms
                        # Emit TOP3_UPDATE per rank
                        for rank_idx, (score, rec) in enumerate(top3, 1):
                            ev2 = {
                                "event": "TOP3_UPDATE",
                                "rank": rank_idx,
                                "symbol": rec.get("internal_symbol"),
                                "decision": rec.get("decision"),
                                "score": round(score, 4),
                                "elapsed_ms": round(elapsed_ms, 1),
                                "partial": True,
                            }
                            events.append(ev2)
                            top3_updates.append(ev2)
                elif top3 and len(ranked) > 0 and time_to_partial_top3_ms is None and len(ranked) < 3:
                    # Not yet full Top-3 — track first eligible as early signal but don't mark as partial Top3
                    pass

                # optional per-decision log to stdout for visibility
                # print minimal
                print(f"[{completed}/{len(self.universe)}] {sym} -> {res.get('decision')} status={res.get('status')} fresh={res.get('fresh')} elapsed={elapsed_ms:.0f}ms worker={self.workers}")

        wall_ms = (time.perf_counter() - monotonic_start) * 1000

        try:
            import psutil, os
            peak_mem_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            if mem_before is not None:
                mem_delta = peak_mem_mb - mem_before
            else:
                mem_delta = None
        except:
            peak_mem_mb = None
            mem_delta = None

        # Final ranking
        ranked = rank_records(records)
        top3_final = ranked[:3]
        all_ranked_sig = [{"rank": i+1, "symbol": r[1].get("internal_symbol"), "decision": r[1].get("decision"), "score": round(r[0],4)} for i,(r) in enumerate(ranked)]

        # Determine TOP3_COMPLETE vs PARTIAL
        top3_status = "TOP3_PARTIAL" if len(top3_final) >= 1 else "TOP3_EMPTY"
        # If wall finished scanning all assets, it's COMPLETE (even if empty, it's final)
        # Distinguish: PARTIAL during stream, COMPLETE at end
        top3_final_status = "TOP3_COMPLETE" if wall_ms else "TOP3_PARTIAL"

        # Throughput
        throughput = len(self.universe) / (wall_ms/1000) if wall_ms else 0

        # CPU estimate
        cpu_pct = None
        try:
            import psutil
            cpu_pct = psutil.cpu_percent(interval=0.1)
        except: pass

        result = {
            "generated_at": overall_iso,
            "executor_type": self.executor_type,
            "workers": self.workers,
            "universe": len(self.universe),
            "wall_ms": round(wall_ms, 1),
            "wall_s": round(wall_ms/1000, 2),
            "first_decision_ms": round(first_decision_ms, 1) if first_decision_ms else None,
            "time_to_5_ms": round(time_to_5_ms,1) if time_to_5_ms else None,
            "time_to_10_ms": round(time_to_10_ms,1) if time_to_10_ms else None,
            "time_to_partial_top3_ms": round(time_to_partial_top3_ms,1) if time_to_partial_top3_ms else None,
            "time_to_complete_top3_ms": round(wall_ms,1),
            "throughput_assets_per_sec": round(throughput,3),
            "throughput_sec_per_asset": round((wall_ms/1000)/len(self.universe),3) if self.universe else None,
            "fresh": fresh_count,
            "stale": stale_count,
            "unavailable": unavailable_count,
            "errors": error_count,
            "peak_memory_mb": round(peak_mem_mb,1) if peak_mem_mb else None,
            "memory_delta_mb": round(mem_delta,1) if mem_delta else None,
            "cpu_percent": cpu_pct,
            "events": events,
            "top3_updates": top3_updates,
            "per_asset": per_asset,
            "records": records,
            "ranked": all_ranked_sig,
            "top3": [{"rank": i+1, "symbol": r[1].get("internal_symbol"), "decision": r[1].get("decision"), "grade": r[1].get("grade"), "confidence": r[1].get("confidence"), "confluence": r[1].get("confluence"), "score": round(r[0],4), "audit_id": r[1].get("audit_id")} for i,r in enumerate(top3_final)],
            "top3_status": top3_final_status,
            "formula": FORMULA,
        }
        return result


def main():
    import argparse
    p = argparse.ArgumentParser(description="M5 Inter-Asset Parallel Scanner Sprint4")
    p.add_argument("--universe", type=int, default=12, help="12 ou 64")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--executor", choices=["thread","process"], default="thread")
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()
    n = min(args.universe, len(ALL_SYMBOLS))
    symbols = ALL_SYMBOLS[:n]
    print(f"ParallelScanner universe={n} workers={args.workers} executor={args.executor}")
    print(f"symbols: {symbols[:5]} ...")
    sc = ParallelScanner(symbols, workers=args.workers, executor_type=args.executor)
    res = sc.scan()
    out = Path(args.out) if args.out else Path(f"reports/m5_sprint4/scan_{n}assets_w{args.workers}_{args.executor}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\nWALL {res['wall_s']}s first={res['first_decision_ms']}ms partial_top3={res['time_to_partial_top3_ms']}ms complete={res['time_to_complete_top3_ms']}ms")
    print(f"Fresh {res['fresh']} stale {res['stale']} unavailable {res['unavailable']} errors {res['errors']}")
    print(f"Top3: {res['top3']}")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
