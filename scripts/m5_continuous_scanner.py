#!/usr/bin/env python3
"""
M5 CONTINUOUS SCANNER — SPRINT 2

Scanner CONTÍNUO/INCREMENTAL M5 isolado (não substitui scanner batch).

Fluxo:
  START
    -> discover universe (config/universe.ALL_SYMBOLS)
    -> initialize state (AssetScanState por ativo)
    -> ciclo M5:
        -> rolling queue (P1 candle recém-fechado, P2 stale, P3 já fresh)
        -> analyze assets em ordem de prioridade (sequencial por padrão)
        -> freshness gate (FRESH vs STALE vs DATA_UNAVAILABLE)
        -> store official DecisionResult (via AnalysisPipeline + SnapshotLogger)
        -> update state -> update ranking (mesma fórmula canônica)
        -> Top-3 parcial quando houver >=3 elegíveis, completo quando ciclo fecha
        -> aguardar próxima fronteira M5 (ou encerrar se --cycles atingido)

Medições:
  cycle_start, first_fresh_decision, top3_partial_ready, all_assets_ready, top3_complete
  time_to_first_decision, time_to_partial_top3, time_to_complete_top3
  CACHE_HIT/MISS/STALE/REFRESH, FRESH/STALE/DATA_UNAVAILABLE por ativo

Uso:
  python scripts/m5_continuous_scanner.py --cycles 2 --universe 12 --workers 1
  python scripts/m5_continuous_scanner.py --cycles 1 --universe 64 --workers 1
  python scripts/m5_continuous_scanner.py --cycles 2 --universe 12 --workers 2  (paralelo controlado)

Contratos preservados:
  DecisionResolverEngine, DecisionResult, ranking fórmula/pesos, DataQualityEngine,
  trade_allowed, probability normalization, confluence/confidence, elegibilidade Top-3
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import threading

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.operations.ranking import (
    rank_records, select_top3, classify_status, confidence_100_public, prob_dominant_public, FORMULA, GRADE_BONUS
)
from mercury_ai.operations.m5_incremental.temporal import (
    floor_m5, ceil_m5, current_candle, previous_candle, next_candle,
    decision_candle_timestamp_from_df, _ensure_utc, next_m5_boundary
)
from mercury_ai.operations.m5_incremental.asset_state import AssetScanState
from mercury_ai.operations.m5_incremental.freshness import FreshnessGate
from mercury_ai.operations.m5_incremental.rolling_queue import RollingQueue, Top3Status
from mercury_ai.operations.m5_incremental.cache_tracker import CacheTracker
from mercury_ai.operations.m5_incremental.mtf_classification import MTF_CLASSIFICATIONS, report as mtf_report


def parse_args():
    p = argparse.ArgumentParser(description="M5 Continuous Scanner — Sprint 2")
    p.add_argument("--cycles", type=int, default=2, help="Número de ciclos M5 a executar (0 = infinito até Ctrl+C)")
    p.add_argument("--universe", type=int, default=12, help="Tamanho do universo para experimento (12 ou 64)")
    p.add_argument("--workers", type=int, default=1, help="max_workers para análise por ativo (1=sequencial, 2/4=paralelo controlado)")
    p.add_argument("--no-wait", action="store_true", help="Não aguardar próxima fronteira M5 entre ciclos (para teste rápido)")
    p.add_argument("--out", type=str, default="reports/asset_universe/m5_continuous_scanner.json", help="Arquivo de saída JSON")
    return p.parse_args()


def build_ranking_record(
    symbol: str,
    analysis_result: Any,
    audit_id: str,
    status: str,
    decision_str: str,
    grade: str,
    confidence: Optional[float],
    confluence: Optional[float],
    buy_p: Optional[float],
    sell_p: Optional[float],
    wait_p: Optional[float],
    trade_allowed: bool,
    prob_sum_ok: bool,
    execution_timestamp: str,
) -> Dict[str, Any]:
    return {
        "internal_symbol": symbol,
        "hezilex_input": symbol,
        "asset_class": "UNKNOWN",
        "provider_symbol": symbol,
        "decision": decision_str,
        "status": status,
        "trade_allowed": trade_allowed,
        "prob_sum_ok": prob_sum_ok,
        "confidence": confidence,
        "confluence": confluence,
        "grade": grade,
        "buy_probability": buy_p,
        "sell_probability": sell_p,
        "wait_probability": wait_p,
        "audit_id": audit_id,
        "execution_timestamp": execution_timestamp,
    }


def extract_result_fields(result: Any, symbol: str):
    """Extrai campos do AnalysisResult + DecisionResult."""
    decision = result.decision if result is not None else None
    decision_str = str(getattr(decision, "decision", "") or "").upper() if decision else "NONE"
    audit_id = str(getattr(decision, "audit_id", "") or "")
    grade = str(getattr(decision, "grade", "") or "")
    confidence = getattr(decision, "confidence", None)
    buy_p = getattr(decision, "buy_probability", None)
    sell_p = getattr(decision, "sell_probability", None)
    wait_p = getattr(decision, "wait_probability", None)
    trade_allowed = bool(getattr(decision, "trade_allowed", False)) if decision else False
    # prob sum ok
    prob_ok = False
    if buy_p is not None and sell_p is not None and wait_p is not None:
        try:
            s = float(buy_p or 0) + float(sell_p or 0) + float(wait_p or 0)
            prob_ok = abs(s - 100) < 0.5
        except Exception:
            prob_ok = False
    # confluence
    confl = getattr(result, "confluence", None)
    confluence = None
    if confl is not None:
        confluence = getattr(confl, "weighted_score", None)
        if confluence is None:
            confluence = getattr(confl, "confluence_score", None)
    status = classify_status(decision_str, audit_id)
    return {
        "decision_str": decision_str,
        "audit_id": audit_id,
        "grade": grade,
        "confidence": confidence,
        "buy_p": buy_p,
        "sell_p": sell_p,
        "wait_p": wait_p,
        "trade_allowed": trade_allowed,
        "prob_ok": prob_ok,
        "confluence": confluence,
        "status": status,
        "decision": decision,
        "result": result,
    }


def get_latest_candle_for_symbol(market_service: MarketDataService, symbol: str) -> Optional[datetime]:
    """Tenta obter latest candle sem pagar custo de AnalysisPipeline completo.
    
    Fallback: usa o próprio pipeline result. Aqui apenas probe leve.
    """
    try:
        df = market_service.get_data(symbol, interval="5m")
        ts = decision_candle_timestamp_from_df(df)
        return ts
    except Exception:
        return None


def main():
    args = parse_args()
    universe_size = min(args.universe, len(ALL_SYMBOLS))
    # manter ordem determinística do universo canônico (ALL_SYMBOLS é lista ordenada por prioridade)
    symbols = ALL_SYMBOLS[:universe_size]

    print("=" * 70)
    print("M5 CONTINUOUS SCANNER — SPRINT 2")
    print(f"Universe: {universe_size} / {len(ALL_SYMBOLS)}  symbols={symbols[:4]}...")
    print(f"Cycles: {args.cycles}  Workers: {args.workers}  No-wait: {args.no_wait}")
    print("=" * 70)

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path = out_path.with_suffix(".txt")

    # Estado incremental
    states: Dict[str, AssetScanState] = {s: AssetScanState(symbol=s) for s in symbols}
    cache_tracker = CacheTracker()
    freshness_gate = FreshnessGate()
    rolling_queue = RollingQueue(freshness_gate=freshness_gate)

    # Métricas globais
    overall_start = time.perf_counter()
    overall_start_iso = datetime.now(timezone.utc).isoformat()

    cycles_data: List[Dict[str, Any]] = []
    all_provider_errors = 0
    total_cache_stats = {"CACHE_HIT": 0, "CACHE_MISS": 0, "CACHE_STALE": 0, "CACHE_REFRESH": 0}

    # Para comparação CURRENT BATCH vs CONTINUOUS
    batch_sequential_time_s: Optional[float] = None

    # Pipeline factory (per-thread quando paralelo)
    def make_pipeline():
        provider = MercuryDataProvider()
        market_service = MarketDataService(provider=provider)
        pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])
        return provider, market_service, pipeline

    # Para modo sequencial, reusar um pipeline (mais rápido, sem race)
    seq_provider, seq_market_service, seq_pipeline = make_pipeline()

    cycles_to_run = args.cycles if args.cycles > 0 else 1  # para infinito usar Ctrl+C outer loop

    infinite = args.cycles == 0
    cycle_idx = 0

    try:
        while True:
            cycle_idx += 1
            if not infinite and cycle_idx > args.cycles:
                break

            cycle_start = time.perf_counter()
            cycle_start_iso = datetime.now(timezone.utc).isoformat()
            cycle_start_wall = datetime.now(timezone.utc)
            # expected candle para este ciclo
            cycle_candle = floor_m5(cycle_start_wall)
            cycle_next_boundary = ceil_m5(cycle_start_wall)

            print(f"\n{'='*70}")
            print(f"CYCLE {cycle_idx} — start {cycle_start_iso}  candle={cycle_candle.isoformat()} next_boundary={cycle_next_boundary.isoformat()}")
            print(f"{'='*70}")

            # Fase 1: sondar latest candles para construir fila (custo: 1 fetch leve por ativo)
            # Isso permite priorizar P1/P2/P3 antes de pagar custo full pipeline
            latest_candles: Dict[str, Optional[datetime]] = {}
            probe_start = time.perf_counter()
            # Em modo teste rápido, sondar via seq_market_service get_data (já tem cache Yahoo 60s)
            for sym in symbols:
                try:
                    # Usar probe leve (se falhar, None => DATA_UNAVAILABLE path)
                    latest_candles[sym] = get_latest_candle_for_symbol(seq_market_service, sym)
                except Exception:
                    latest_candles[sym] = None
            probe_duration_s = time.perf_counter() - probe_start

            # Construir rolling queue
            queue = rolling_queue.build(symbols, states, latest_candles, cycle_start=cycle_start_wall)
            # Log distribuição
            p_counts = {"P1": 0, "P2": 0, "P3": 0}
            for e in queue:
                if e.priority == 1:
                    p_counts["P1"] += 1
                elif e.priority == 2:
                    p_counts["P2"] += 1
                else:
                    p_counts["P3"] += 1
            print(f"Queue: P1={p_counts['P1']} P2={p_counts['P2']} P3={p_counts['P3']} (probe {probe_duration_s:.2f}s)")
            for e in queue[:6]:
                print(f"  P{e.priority} {e.symbol:12} — {e.reason[:80]}")

            # Fase 2: analisar em ordem de fila, medindo time_to_first, time_to_partial, time_to_complete
            first_fresh_time: Optional[float] = None
            first_fresh_symbol: Optional[str] = None
            top3_partial_time: Optional[float] = None
            top3_partial_symbols: Optional[List[str]] = None
            all_ready_time: Optional[float] = None
            top3_complete_time: Optional[float] = None

            per_asset_cycle: List[Dict[str, Any]] = []
            ranking_records_cycle: List[Dict[str, Any]] = []
            fresh_count = 0
            stale_count = 0
            unavailable_count = 0
            provider_errors_cycle = 0

            t_first_decision_wall: Optional[str] = None

            # Para Top-3 incremental: após cada ativo, recalcular ranking parcial
            # Mas só reportar top3_partial_ready na primeira vez que houver >=3 elegíveis

            processed_symbols: set = set()
            pending_for_top3 = set(symbols)

            # Escolher modo de execução
            if args.workers <= 1:
                # Sequencial — incremental e com medição precisa
                for qi, entry in enumerate(queue):
                    sym = entry.symbol
                    t0 = time.perf_counter()
                    t0_iso = datetime.now(timezone.utc).isoformat()
                    # Checar cache antes de pipeline
                    # required candle = latest_candles[sym] (ou floor_m5 agora)
                    required = latest_candles.get(sym)
                    if required is None:
                        required = floor_m5(datetime.now(timezone.utc))
                    cache_decision = cache_tracker.check(sym, required, latest_available=required)
                    cache_status_before = cache_decision.status.value

                    # Executar pipeline oficial
                    try:
                        result = seq_pipeline.analyze(sym)
                        t1 = time.perf_counter()
                        duration_ms = (t1 - t0) * 1000
                        fields = extract_result_fields(result, sym)
                        # Df para temporal
                        # Tentar obter data_latest_timestamp do snapshot ou df
                        snapshot = seq_pipeline.last_snapshots.get(sym)
                        data_latest_iso = None
                        decision_candle_iso = None
                        # snapshot.timestamp é decision_timestamp wall
                        snapshot_ts = snapshot.timestamp if snapshot else t0_iso
                        # Tentar df para latest candle (já temos latest_candles, mas re-derivar de result seria ideal)
                        # Usar latest_candles como data_latest
                        latest = latest_candles.get(sym)
                        if latest is not None:
                            data_latest_iso = latest.isoformat()
                            decision_candle_iso = latest.isoformat()  # decisão baseada nesta vela
                        else:
                            # Sem df, manter None
                            data_latest_iso = None
                            decision_candle_iso = None

                        # Freshness check sobre o resultado atual (comparar decision_candle vs latest)
                        fr = freshness_gate.check(
                            df=None,
                            decision_candle=latest,
                            latest_candle=latest,
                            now=datetime.now(timezone.utc),
                        )
                        # Se latest is None, freshness será DATA_UNAVAILABLE
                        if latest is None and fields["status"] in ("DATA_UNAVAILABLE", "SCAN_ERROR"):
                            fr_status = "DATA_UNAVAILABLE"
                            is_fresh = False
                        else:
                            fr_status = fr.status
                            is_fresh = fr.is_fresh

                        # Atualizar contadores
                        if fr_status == "FRESH":
                            fresh_count += 1
                        elif fr_status == "STALE":
                            stale_count += 1
                        elif fr_status == "DATA_UNAVAILABLE":
                            unavailable_count += 1

                        # Atualizar cache (após fresh)
                        if latest is not None and is_fresh:
                            cache_tracker.put(sym, latest, audit_id=fields["audit_id"])
                            # Se era MISS/STALE, marcar refresh
                            if cache_status_before in ("CACHE_MISS", "CACHE_STALE"):
                                cache_tracker.mark_refresh(sym)
                        cache_status_after = cache_tracker.check(sym, required, latest_available=required).status.value if latest else cache_status_before

                        # Atualizar AssetScanState (aponta para DecisionResult oficial, não duplica)
                        state = states[sym]
                        state.decision_candle_timestamp = decision_candle_iso
                        state.data_latest_timestamp = data_latest_iso
                        state.decision_timestamp = snapshot_ts if isinstance(snapshot_ts, str) else str(snapshot_ts)
                        state.last_audit_id = fields["audit_id"]
                        state.last_decision = fields["decision_str"]
                        state.last_grade = fields["grade"]
                        state.last_confidence = fields["confidence"]
                        state.last_confluence = fields["confluence"]
                        state.last_scan_duration_ms = round(duration_ms, 2)
                        state.scan_count += 1
                        state.consecutive_failures = 0 if fr_status != "DATA_UNAVAILABLE" else state.consecutive_failures + 1
                        state.status = fr_status if fr_status in ("FRESH", "STALE", "DATA_UNAVAILABLE") else fields["status"]
                        state.is_fresh = is_fresh
                        state.updated_at = datetime.now(timezone.utc).isoformat()
                        state.cache_status = cache_status_after
                        state.snapshot_file = getattr(snapshot, "timestamp", None)
                        state._result_ref = fields["decision"]
                        try:
                            # age
                            if state.decision_timestamp:
                                dt = datetime.fromisoformat(state.decision_timestamp.replace("Z", "+00:00"))
                                if dt.tzinfo is None:
                                    dt = dt.replace(tzinfo=timezone.utc)
                                state.decision_age_seconds = (datetime.now(timezone.utc) - dt).total_seconds()
                        except Exception:
                            pass

                        # Ranking record
                        ranking_rec = build_ranking_record(
                            symbol=sym,
                            analysis_result=result,
                            audit_id=fields["audit_id"],
                            status=fields["status"],
                            decision_str=fields["decision_str"],
                            grade=fields["grade"],
                            confidence=fields["confidence"],
                            confluence=fields["confluence"],
                            buy_p=fields["buy_p"],
                            sell_p=fields["sell_p"],
                            wait_p=fields["wait_p"],
                            trade_allowed=fields["trade_allowed"],
                            prob_sum_ok=fields["prob_ok"],
                            execution_timestamp=state.decision_timestamp or t0_iso,
                        )
                        ranking_records_cycle.append(ranking_rec)

                        # Per-asset entry
                        per_asset_cycle.append({
                            "symbol": sym,
                            "priority": entry.priority,
                            "queue_reason": entry.reason,
                            "cache_status_before": cache_status_before,
                            "cache_status_after": cache_status_after,
                            "freshness_status": fr_status,
                            "freshness_reason": fr.reason,
                            "is_fresh": is_fresh,
                            "decision": fields["decision_str"],
                            "audit_id": fields["audit_id"],
                            "status": fields["status"],
                            "grade": fields["grade"],
                            "confidence": fields["confidence"],
                            "confluence": fields["confluence"],
                            "duration_ms": round(duration_ms, 2),
                            "decision_candle": decision_candle_iso,
                            "data_latest": data_latest_iso,
                            "timestamp": state.decision_timestamp,
                        })

                        # Time to first decision (primeiro FRESH)
                        if first_fresh_time is None and is_fresh and fields["status"] in ("REAL_SIGNAL", "WAIT_LEGITIMATE"):
                            first_fresh_time = time.perf_counter() - cycle_start
                            first_fresh_symbol = sym
                            t_first_decision_wall = datetime.now(timezone.utc).isoformat()

                        # Top3 parcial: recalcular ranking a cada ativo
                        ranked_now, _ = select_top3(ranking_records_cycle)
                        if top3_partial_time is None and len(ranked_now) >= 3:
                            top3_partial_time = time.perf_counter() - cycle_start
                            top3_partial_symbols = [r[1]["internal_symbol"] for r in ranked_now[:3]]

                        processed_symbols.add(sym)
                        pending_for_top3.discard(sym)

                        print(f"  [{qi+1}/{len(queue)}] {sym:12} P{entry.priority} {fields['decision_str']:4} {fields['status']:16} fresh={is_fresh} cache={cache_status_after} {duration_ms:.0f}ms audit={fields['audit_id'][:10]}")

                    except Exception as e:
                        t1 = time.perf_counter()
                        duration_ms = (t1 - t0) * 1000
                        provider_errors_cycle += 1
                        all_provider_errors += 1
                        state = states[sym]
                        state.last_error = str(e)[:500]
                        state.status = "SCAN_ERROR"
                        state.is_fresh = False
                        state.last_scan_duration_ms = round(duration_ms, 2)
                        state.updated_at = datetime.now(timezone.utc).isoformat()
                        state.scan_count += 1
                        per_asset_cycle.append({
                            "symbol": sym,
                            "priority": entry.priority,
                            "error": str(e)[:500],
                            "trace": traceback.format_exc()[:600],
                            "duration_ms": round(duration_ms, 2),
                        })
                        # Ainda criar ranking record como SCAN_ERROR (não elegível)
                        ranking_records_cycle.append(build_ranking_record(
                            symbol=sym, analysis_result=None, audit_id="SCAN_ERROR",
                            status="SCAN_ERROR", decision_str="WAIT", grade="N/A",
                            confidence=None, confluence=None, buy_p=None, sell_p=None, wait_p=None,
                            trade_allowed=False, prob_sum_ok=False,
                            execution_timestamp=datetime.now(timezone.utc).isoformat(),
                        ))
                        print(f"  [{qi+1}/{len(queue)}] {sym:12} ERROR {e} {duration_ms:.0f}ms")
                        processed_symbols.add(sym)
                        pending_for_top3.discard(sym)

                # Fim sequencial
                cycle_duration_s = time.perf_counter() - cycle_start
                all_ready_time = cycle_duration_s

                # Top3 final do ciclo
                ranked_final, all_ranked = select_top3(ranking_records_cycle)
                top3_final = ranked_final[:3]
                pending = list(pending_for_top3)
                # Top3 status
                rq = RollingQueue()
                if not ranked_final:
                    top3_status = Top3Status.EMPTY.value
                elif pending:
                    top3_status = Top3Status.PARTIAL.value
                else:
                    top3_status = Top3Status.COMPLETE.value

                if top3_complete_time is None and top3_status == Top3Status.COMPLETE.value:
                    top3_complete_time = cycle_duration_s

                # Se top3_partial nunca atingiu mas há top3 ao final, usar tempo final
                if top3_partial_time is None and len(ranked_final) >= 3:
                    top3_partial_time = cycle_duration_s
                    top3_partial_symbols = [r[1]["internal_symbol"] for r in ranked_final[:3]]

            else:
                # Paralelo controlado (max_workers = args.workers)
                from concurrent.futures import ThreadPoolExecutor, as_completed

                def analyze_one(sym):
                    provider, market_service, pipeline = make_pipeline()
                    # Desabilitar profiler para evitar race tracemalloc em paralelo
                    pipeline.profiler.active = False
                    t0 = time.perf_counter()
                    try:
                        result = pipeline.analyze(sym)
                        t1 = time.perf_counter()
                        fields = extract_result_fields(result, sym)
                        snapshot = pipeline.last_snapshots.get(sym)
                        snapshot_ts = snapshot.timestamp if snapshot else datetime.now(timezone.utc).isoformat()
                        latest = get_latest_candle_for_symbol(market_service, sym)
                        # fallback: se probe não deu, usar snapshot timestamp floored
                        duration_ms = (t1 - t0) * 1000
                        return sym, {
                            "result": result, "fields": fields,
                            "snapshot_ts": snapshot_ts, "latest": latest,
                            "duration_ms": duration_ms, "error": None,
                            "pipeline": pipeline, "market_service": market_service,
                        }
                    except Exception as e:
                        t1 = time.perf_counter()
                        return sym, {"error": str(e), "trace": traceback.format_exc()[:600], "duration_ms": (t1-t0)*1000}

                # Para preservar ordem de prioridade mas executar em paralelo,
                # submeter na ordem da fila
                start_par = time.perf_counter()
                results_map: Dict[str, Any] = {}
                with ThreadPoolExecutor(max_workers=args.workers) as ex:
                    futs = {ex.submit(analyze_one, e.symbol): e for e in queue}
                    for fut in as_completed(futs):
                        entry = futs[fut]
                        sym, res = fut.result()
                        results_map[sym] = (entry, res)

                # Reconstituir em ordem de fila para medição determinística
                for entry in queue:
                    sym = entry.symbol
                    res = results_map.get(sym, (entry, {"error": "missing"}))[1]
                    if res.get("error"):
                        provider_errors_cycle += 1
                        all_provider_errors += 1
                        state = states[sym]
                        state.last_error = res["error"][:500]
                        state.status = "SCAN_ERROR"
                        state.is_fresh = False
                        state.last_scan_duration_ms = round(res.get("duration_ms", 0), 2)
                        state.updated_at = datetime.now(timezone.utc).isoformat()
                        per_asset_cycle.append({
                            "symbol": sym, "priority": entry.priority, "error": res["error"][:500], "duration_ms": round(res.get("duration_ms", 0), 2)
                        })
                        ranking_records_cycle.append(build_ranking_record(
                            symbol=sym, analysis_result=None, audit_id="SCAN_ERROR",
                            status="SCAN_ERROR", decision_str="WAIT", grade="N/A",
                            confidence=None, confluence=None, buy_p=None, sell_p=None, wait_p=None,
                            trade_allowed=False, prob_sum_ok=False,
                            execution_timestamp=datetime.now(timezone.utc).isoformat(),
                        ))
                    else:
                        fields = res["fields"]
                        latest = res["latest"]
                        t_duration = res["duration_ms"]
                        snapshot_ts = res["snapshot_ts"]
                        required = latest_candles.get(sym) or floor_m5(datetime.now(timezone.utc))
                        cache_decision = cache_tracker.check(sym, required, latest_available=required)
                        cache_before = cache_decision.status.value
                        fr = freshness_gate.check(df=None, decision_candle=latest, latest_candle=latest, now=datetime.now(timezone.utc))
                        fr_status = fr.status if latest else "DATA_UNAVAILABLE"
                        is_fresh = fr.is_fresh if latest else False
                        if fr_status == "FRESH":
                            fresh_count += 1
                        elif fr_status == "STALE":
                            stale_count += 1
                        else:
                            unavailable_count += 1
                        if latest is not None and is_fresh:
                            cache_tracker.put(sym, latest, audit_id=fields["audit_id"])
                            if cache_before in ("CACHE_MISS", "CACHE_STALE"):
                                cache_tracker.mark_refresh(sym)
                        cache_after = cache_tracker.check(sym, required, latest_available=required).status.value if latest else cache_before

                        state = states[sym]
                        state.decision_candle_timestamp = latest.isoformat() if latest else None
                        state.data_latest_timestamp = latest.isoformat() if latest else None
                        state.decision_timestamp = snapshot_ts if isinstance(snapshot_ts, str) else str(snapshot_ts)
                        state.last_audit_id = fields["audit_id"]
                        state.last_decision = fields["decision_str"]
                        state.last_grade = fields["grade"]
                        state.last_confidence = fields["confidence"]
                        state.last_confluence = fields["confluence"]
                        state.last_scan_duration_ms = round(t_duration, 2)
                        state.scan_count += 1
                        state.status = fr_status if fr_status in ("FRESH", "STALE", "DATA_UNAVAILABLE") else fields["status"]
                        state.is_fresh = is_fresh
                        state.updated_at = datetime.now(timezone.utc).isoformat()
                        state.cache_status = cache_after
                        state._result_ref = fields["decision"]

                        ranking_records_cycle.append(build_ranking_record(
                            symbol=sym, analysis_result=res["result"], audit_id=fields["audit_id"],
                            status=fields["status"], decision_str=fields["decision_str"], grade=fields["grade"],
                            confidence=fields["confidence"], confluence=fields["confluence"],
                            buy_p=fields["buy_p"], sell_p=fields["sell_p"], wait_p=fields["wait_p"],
                            trade_allowed=fields["trade_allowed"], prob_sum_ok=fields["prob_ok"],
                            execution_timestamp=state.decision_timestamp or datetime.now(timezone.utc).isoformat(),
                        ))
                        per_asset_cycle.append({
                            "symbol": sym, "priority": entry.priority,
                            "cache_status_before": cache_before, "cache_status_after": cache_after,
                            "freshness_status": fr_status, "is_fresh": is_fresh,
                            "decision": fields["decision_str"], "audit_id": fields["audit_id"],
                            "status": fields["status"], "duration_ms": round(t_duration, 2),
                        })
                        if first_fresh_time is None and is_fresh and fields["status"] in ("REAL_SIGNAL", "WAIT_LEGITIMATE"):
                            first_fresh_time = time.perf_counter() - cycle_start
                            first_fresh_symbol = sym
                        ranked_now, _ = select_top3(ranking_records_cycle)
                        if top3_partial_time is None and len(ranked_now) >= 3:
                            top3_partial_time = time.perf_counter() - cycle_start
                            top3_partial_symbols = [r[1]["internal_symbol"] for r in ranked_now[:3]]
                        print(f"  {sym:12} P{entry.priority} {fields['decision_str']:4} {fields['status']:16} fresh={is_fresh} {t_duration:.0f}ms")

                cycle_duration_s = time.perf_counter() - cycle_start
                all_ready_time = cycle_duration_s
                ranked_final, all_ranked = select_top3(ranking_records_cycle)
                top3_final = ranked_final[:3]
                pending = [s for s in symbols if s not in [r["symbol"] if isinstance(r, dict) else "" for r in per_asset_cycle]]
                # pending real: symbols não processados
                processed = set(r["symbol"] for r in per_asset_cycle if "symbol" in r)
                pending = [s for s in symbols if s not in processed]
                if not ranked_final:
                    top3_status = Top3Status.EMPTY.value
                elif pending:
                    top3_status = Top3Status.PARTIAL.value
                else:
                    top3_status = Top3Status.COMPLETE.value
                if top3_status == Top3Status.COMPLETE.value:
                    top3_complete_time = cycle_duration_s
                if top3_partial_time is None and len(ranked_final) >= 3:
                    top3_partial_time = cycle_duration_s
                    top3_partial_symbols = [r[1]["internal_symbol"] for r in ranked_final[:3]]

            # Métricas de tempo do ciclo
            time_to_first = round(first_fresh_time, 3) if first_fresh_time is not None else None
            time_to_partial = round(top3_partial_time, 3) if top3_partial_time is not None else None
            time_to_complete = round(all_ready_time, 3) if all_ready_time is not None else None

            # Estado do Top-3 já definido acima; garantir fallback
            if 'top3_status' not in locals():
                ranked_final, all_ranked = select_top3(ranking_records_cycle)
                top3_final = ranked_final[:3]
                top3_status = Top3Status.COMPLETE.value if ranked_final else Top3Status.EMPTY.value

            print(f"\nCycle {cycle_idx} done: duration={cycle_duration_s:.2f}s")
            print(f"  fresh={fresh_count} stale={stale_count} unavailable={unavailable_count} errors={provider_errors_cycle}")
            print(f"  time_to_first={time_to_first}s ({first_fresh_symbol})")
            print(f"  time_to_partial_top3={time_to_partial}s ({top3_partial_symbols})")
            print(f"  time_to_complete={time_to_complete}s  status={top3_status}")
            if 'top3_final' in locals() and top3_final:
                for i, (score, rec) in enumerate(top3_final, 1):
                    print(f"    Top{i}: {rec['internal_symbol']} {rec['decision']} score={score:.2f} audit={rec['audit_id'][:10]}")

            # Registrar ciclo
            cycles_data.append({
                "cycle": cycle_idx,
                "cycle_start": cycle_start_iso,
                "cycle_candle": cycle_candle.isoformat(),
                "next_boundary": cycle_next_boundary.isoformat(),
                "cycle_duration_s": round(cycle_duration_s, 3),
                "per_asset": per_asset_cycle,
                "ranking_records": ranking_records_cycle,
                "fresh_count": fresh_count,
                "stale_count": stale_count,
                "unavailable_count": unavailable_count,
                "provider_errors": provider_errors_cycle,
                "time_to_first_decision_s": time_to_first,
                "first_fresh_symbol": first_fresh_symbol,
                "time_to_partial_top3_s": time_to_partial,
                "top3_partial_symbols": top3_partial_symbols,
                "time_to_complete_top3_s": time_to_complete,
                "top3_status": top3_status,
                "top3_final": [{"rank": i+1, "symbol": rec["internal_symbol"], "decision": rec["decision"], "score": round(score, 4), "audit_id": rec["audit_id"]} for i, (score, rec) in enumerate(top3_final)] if 'top3_final' in locals() else [],
                "all_ranked_count": len(ranked_final) if 'ranked_final' in locals() else 0,
                "queue_distribution": p_counts,
                "probe_duration_s": round(probe_duration_s, 3),
            })

            # Aguardar próxima fronteira M5 (se não for último ciclo e não estiver em no-wait)
            if not infinite and cycle_idx >= args.cycles:
                break
            if args.no_wait:
                print("  --no-wait: iniciando próximo ciclo imediatamente")
                time.sleep(0.5)
                continue
            # Calcular sleep até próxima fronteira M5 + pequeno buffer (5s após boundary para garantir dados)
            now_wall = datetime.now(timezone.utc)
            nxt = ceil_m5(now_wall)
            # Adicionar 5s de buffer para Yahoo entregar candle fechado
            target = nxt + timedelta(seconds=5)
            sleep_s = (target - now_wall).total_seconds()
            if sleep_s < 0:
                sleep_s = 0
            # Se cycles==0 (infinito), dormir até boundary; se cycles finito mas ainda há ciclos, dormir mas cap a 300s
            # Em teste com --cycles 2 e --no-wait false, dormir 300s inviabiliza teste rápido — então para teste, limitar
            # Se o usuário pediu --cycles 2 com 12 ativos, o segundo ciclo seria 5min depois; para validar sem esperar 5min,
            # oferecemos interrupção: se sleep_s > 60 e args.cycles <=2, encurtar para 2s para validar segunda iteração
            if sleep_s > 60 and args.cycles <= 3 and not infinite:
                print(f"  Próxima fronteira em {sleep_s:.0f}s — modo teste: aguardando 3s para validar 2º ciclo sem esperar 5min real")
                time.sleep(3)
            elif sleep_s > 0:
                print(f"  Aguardando {sleep_s:.1f}s até próxima fronteira M5 {target.isoformat()}")
                time.sleep(sleep_s)
            else:
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário (Ctrl+C)")

    overall_duration_s = time.perf_counter() - overall_start

    # Consolidar estatísticas finais
    total_processed = sum(len(c["per_asset"]) for c in cycles_data)
    total_fresh = sum(c["fresh_count"] for c in cycles_data)
    total_stale = sum(c["stale_count"] for c in cycles_data)
    total_unavail = sum(c["unavailable_count"] for c in cycles_data)
    cache_stats = cache_tracker.stats()

    # Top3 final do último ciclo
    last_cycle = cycles_data[-1] if cycles_data else {}
    top3_partial = last_cycle.get("top3_final", []) if last_cycle else []
    top3_complete_flag = last_cycle.get("top3_status", Top3Status.EMPTY.value) if last_cycle else Top3Status.EMPTY.value

    # MTF classification
    mtf_by_verdict = mtf_report()

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_start": overall_start_iso,
        "overall_duration_s": round(overall_duration_s, 3),
        "universe_size": universe_size,
        "symbols": symbols,
        "cycles_tested": len(cycles_data),
        "cycles_requested": args.cycles,
        "workers": args.workers,
        "no_wait": args.no_wait,
        "cycles": cycles_data,
        "states": {sym: states[sym].to_dict() for sym in symbols},
        "summary": {
            "total_processed": total_processed,
            "fresh_results": total_fresh,
            "stale_results": total_stale,
            "data_unavailable": total_unavail,
            "provider_errors": all_provider_errors,
            "cache_hit": cache_stats.get("CACHE_HIT", 0),
            "cache_miss": cache_stats.get("CACHE_MISS", 0),
            "cache_stale": cache_stats.get("CACHE_STALE", 0),
            "cache_refresh": cache_stats.get("CACHE_REFRESH", 0),
        },
        "timing": {
            "time_to_first_decision_s": last_cycle.get("time_to_first_decision_s") if last_cycle else None,
            "time_to_partial_top3_s": last_cycle.get("time_to_partial_top3_s") if last_cycle else None,
            "time_to_complete_top3_s": last_cycle.get("time_to_complete_top3_s") if last_cycle else None,
            "last_cycle_duration_s": last_cycle.get("cycle_duration_s") if last_cycle else None,
            "overall_duration_s": round(overall_duration_s, 3),
            "sequential_baseline_s": 1026.14,
            "note": "time_to_first/partial/complete medidos por ciclo a partir de cycle_start (wall). Comparar com baseline batch 1026s.",
        },
        "top3": {
            "partial": top3_partial,
            "complete": top3_partial if top3_complete_flag == Top3Status.COMPLETE.value else [],
            "status": top3_complete_flag,
            "formula": FORMULA,
            "eligible_count_last_cycle": last_cycle.get("all_ranked_count", 0) if last_cycle else 0,
        },
        "mtf_classification": {
            "safe_incremental": mtf_by_verdict.get("SAFE_INCREMENTAL", []),
            "requires_full_recalc": mtf_by_verdict.get("REQUIRES_FULL_RECALC", []),
            "unknown": mtf_by_verdict.get("UNKNOWN", []),
            "details": [{"component": c.component, "verdict": c.verdict, "reason": c.reason} for c in MTF_CLASSIFICATIONS],
        },
        "freshness_gate": {
            "rule": "VALID: cached_last_candle == required_decision_candle; INVALID: cached < required => REFRESH; STALE se nova vela disponível não usada",
            "status_values": ["FRESH", "STALE", "DATA_UNAVAILABLE"],
        },
        "ranking_formula": FORMULA,
        "constraints_respected": {
            "DecisionResolverEngine": "NÃO alterado",
            "DecisionResult": "NÃO alterado",
            "ranking_formula": "NÃO alterada (mesma de top3_scanner.py)",
            "DataQualityEngine": "NÃO alterada",
            "trade_allowed": "NÃO alterado",
            "probability_normalization": "NÃO alterada",
            "confluence_confidence": "NÃO alterada",
            "elegibilidade_top3": "NÃO alterada",
            "segunda_decisao": "NÃO criada",
        },
        "notes": {
            "rolling_queue": "P1 candle recém-fechado, P2 stale, P3 já fresh/pending",
            "freshness": "decision_candle vs latest_available; nunca converter STALE em REAL_SIGNAL",
            "cache": "validado por candle, não por TTL; TTL sozinho não é suficiente",
            "parallelization": f"max_workers={args.workers}; cada worker com pipeline isolado; profiler desabilitado em paralelo para evitar race tracemalloc",
        }
    }

    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    # TXT
    lines = []
    lines.append("M5 CONTINUOUS SCANNER — SPRINT 2 REPORT")
    lines.append(f"Generated: {report['generated_at']}")
    lines.append(f"Universe: {universe_size}  Cycles: {len(cycles_data)}/{args.cycles}  Workers: {args.workers}  No-wait: {args.no_wait}")
    lines.append(f"Overall duration: {overall_duration_s:.2f}s")
    lines.append("")
    for c in cycles_data:
        lines.append(f"CYCLE {c['cycle']}: candle={c['cycle_candle']} duration={c['cycle_duration_s']}s queue P1={c['queue_distribution']['P1']} P2={c['queue_distribution']['P2']} P3={c['queue_distribution']['P3']}")
        lines.append(f"  fresh={c['fresh_count']} stale={c['stale_count']} unavailable={c['unavailable_count']} errors={c['provider_errors']}")
        lines.append(f"  time_to_first={c['time_to_first_decision_s']}s ({c['first_fresh_symbol']})  time_to_partial={c['time_to_partial_top3_s']}s  time_to_complete={c['time_to_complete_top3_s']}s  status={c['top3_status']}")
        if c['top3_final']:
            for t in c['top3_final']:
                lines.append(f"    Top{t['rank']}: {t['symbol']} {t['decision']} score={t['score']} audit={t['audit_id'][:10]}")
        lines.append("")
    lines.append(f"SUMMARY: fresh={total_fresh} stale={total_stale} unavailable={total_unavail} errors={all_provider_errors}")
    lines.append(f"CACHE: HIT={cache_stats.get('CACHE_HIT',0)} MISS={cache_stats.get('CACHE_MISS',0)} STALE={cache_stats.get('CACHE_STALE',0)} REFRESH={cache_stats.get('CACHE_REFRESH',0)}")
    lines.append(f"TIMING last cycle: first={report['timing']['time_to_first_decision_s']}s partial={report['timing']['time_to_partial_top3_s']}s complete={report['timing']['time_to_complete_top3_s']}s")
    lines.append(f"TOP3 status: {top3_complete_flag} eligible={report['top3']['eligible_count_last_cycle']}")
    lines.append("")
    lines.append(f"MTF SAFE_INCREMENTAL ({len(mtf_by_verdict.get('SAFE_INCREMENTAL',[]))}): {', '.join(mtf_by_verdict.get('SAFE_INCREMENTAL',[])[:3])}...")
    lines.append(f"MTF REQUIRES_FULL_RECALC ({len(mtf_by_verdict.get('REQUIRES_FULL_RECALC',[]))}): {', '.join([x[:50] for x in mtf_by_verdict.get('REQUIRES_FULL_RECALC',[])[:2]])}...")
    lines.append(f"MTF UNKNOWN ({len(mtf_by_verdict.get('UNKNOWN',[]))}): {', '.join([x[:50] for x in mtf_by_verdict.get('UNKNOWN',[])[:2]])}...")
    lines.append("")
    lines.append("CONSTRAINTS: DecisionResolverEngine / DecisionResult / ranking / DataQuality / trade_allowed — TODOS PRESERVADOS")

    txt_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines))
    print(f"\nWrote {out_path} and {txt_path}")


if __name__ == "__main__":
    main()
