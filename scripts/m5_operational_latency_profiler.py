#!/usr/bin/env python3
"""
M5 OPERATIONAL LATENCY PROFILER — SPRINT M5
Mede tempo real do pipeline M5 até Top-3 pronto (sem alterar lógica de produção).
Caminho: MarketDataService -> Provider(YahooAdapter) -> AnalysisPipeline.analyze() -> DecisionResult -> ranking -> Top-3
"""
from __future__ import annotations
import json
import sys
import time
import traceback
import statistics
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def next_m5_boundary(now: datetime) -> datetime:
    # Ceiling to next 5-minute mark in UTC
    # Truncate seconds/microseconds, then add delta
    minute = now.minute
    remainder = minute % 5
    if remainder == 0 and now.second == 0 and now.microsecond == 0:
        # Exactly on boundary -> next is +5min
        nxt = now.replace(second=0, microsecond=0) + timedelta(minutes=5)
    else:
        # Next boundary
        add = (5 - remainder) % 5
        # If remainder !=0, add; if remainder==0 but seconds>0, add 5
        if remainder == 0:
            add = 5
        nxt = now.replace(second=0, microsecond=0) + timedelta(minutes=add)
        # If we are at e.g. 10:03:15, remainder 3, add 2 -> 10:05:00 correct
        # If we are at 10:05:12, remainder 0 add 5 -> 10:10:00 correct
    return nxt

def percentile(data, p):
    if not data:
        return 0.0
    s = sorted(data)
    k = (len(s)-1) * (p/100)
    f = int(k)
    c = min(f+1, len(s)-1)
    if f == c:
        return float(s[f])
    d0 = s[f] * (c - k)
    d1 = s[c] * (k - f)
    return float(d0 + d1)

def classify_status(decision, audit_id):
    audit = str(audit_id) if audit_id else ""
    dec_str = str(getattr(decision, "decision", "") or "").upper() if decision else ""
    is_hash = len(audit)==64 and all(ch in "0123456789abcdefABCDEF" for ch in audit)
    if audit == "DATA_PROVIDER_UNAVAILABLE":
        return "DATA_UNAVAILABLE"
    if audit == "PIPELINE_ERROR":
        return "SCAN_ERROR"
    if audit in ("DATA_QUALITY_FAIL","INSUFFICIENT_DATA","MARKET_CLOSED"):
        return "DATA_UNAVAILABLE"
    if dec_str in ("BUY","SELL") and is_hash:
        return "REAL_SIGNAL"
    if dec_str == "WAIT" and is_hash:
        return "WAIT_LEGITIMATE"
    if dec_str == "WAIT":
        return "WAIT_LEGITIMATE" if audit not in ("DATA_PROVIDER_UNAVAILABLE","PIPELINE_ERROR","DATA_QUALITY_FAIL","INSUFFICIENT_DATA","MARKET_CLOSED") else "DATA_UNAVAILABLE"
    return "ERROR"

# --- Setup ---
print("="*70)
print("M5 OPERATIONAL LATENCY PROFILER")
print(f"Started: {now_iso()}")
print(f"Universe size: {len(ALL_SYMBOLS)}")
print(f"Symbols: {ALL_SYMBOLS[:5]} ...")
print("="*70)

provider = MercuryDataProvider()
market_service = MarketDataService(provider=provider)
pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])

# Global timing
scan_wall_start = time.perf_counter()
scan_wall_start_iso = now_iso()

per_asset = []
fetch_times = []
analysis_times = []
total_times = []

# Maps for ranking later
records_for_ranking = []

for idx, sym in enumerate(ALL_SYMBOLS, 1):
    print(f"\n[{idx}/{len(ALL_SYMBOLS)}] {sym} ...", flush=True)
    # --- FETCH isolated probe ---
    fetch_start = time.perf_counter()
    fetch_start_iso = now_iso()
    fetch_duration_ms = 0
    df_probe = None
    fetch_error = None
    try:
        df_probe = market_service.get_data(sym, interval="5m")
        fetch_end = time.perf_counter()
        fetch_duration_ms = (fetch_end - fetch_start) * 1000
        probe_rows = 0 if df_probe is None else len(df_probe)
        print(f"  fetch: {fetch_duration_ms:.1f} ms rows={probe_rows}", flush=True)
    except Exception as e:
        fetch_end = time.perf_counter()
        fetch_duration_ms = (fetch_end - fetch_start) * 1000
        fetch_error = str(e)
        print(f"  fetch ERROR: {e} ({fetch_duration_ms:.1f} ms)", flush=True)

    # --- FULL PIPELINE (includes its own fetch) ---
    analysis_start = time.perf_counter()
    analysis_start_iso = now_iso()
    total_duration_ms = 0
    analysis_duration_ms = 0
    fetch_internal_ms = 0
    decision = None
    audit_id = ""
    status = "UNKNOWN"
    error = fetch_error
    grade = None
    confidence = None
    confluence = None
    buy_p = sell_p = wait_p = None
    decision_str = None

    try:
        # Time the pipeline call itself
        pipe_start = time.perf_counter()
        result = pipeline.analyze(sym)
        pipe_end = time.perf_counter()
        total_duration_ms = (pipe_end - pipe_start) * 1000
        decision = result.decision if result else None
        decision_str = str(getattr(decision, "decision", "") or "").upper() if decision else "NONE"
        audit_id = str(getattr(decision, "audit_id", "") or "")
        grade = str(getattr(decision, "grade", "") or "")
        confidence = getattr(decision, "confidence", None)
        buy_p = getattr(decision, "buy_probability", None)
        sell_p = getattr(decision, "sell_probability", None)
        wait_p = getattr(decision, "wait_probability", None)
        # confluence from result
        confl = getattr(result, "confluence", None)
        if confl is not None:
            confluence = getattr(confl, "weighted_score", None)
        status = classify_status(decision, audit_id)

        # Try to extract internal fetch time from profiler
        try:
            prof_summary = pipeline.profiler.summary()
            # prof_summary.stages is tuple of StageProfile
            for st in prof_summary.stages:
                if st.name == "DataLoading":
                    fetch_internal_ms = st.duration * 1000
                    break
        except Exception:
            fetch_internal_ms = 0

        # analysis_duration = total - internal_fetch (if available), else total - probe fetch
        if fetch_internal_ms > 0:
            analysis_duration_ms = max(0, total_duration_ms - fetch_internal_ms)
        else:
            # fallback: subtract probe fetch
            analysis_duration_ms = max(0, total_duration_ms - fetch_duration_ms)

        decision_ready_iso = now_iso()
        print(f"  pipeline: total={total_duration_ms:.1f} ms (fetch_internal={fetch_internal_ms:.1f} analysis={analysis_duration_ms:.1f}) -> {decision_str} audit={audit_id[:12]} status={status}", flush=True)

    except Exception as e:
        pipe_end = time.perf_counter()
        total_duration_ms = (pipe_end - pipe_start) * 1000 if 'pipe_start' in locals() else 0
        analysis_duration_ms = total_duration_ms
        error = str(e) + " | " + traceback.format_exc()[:500]
        status = "SCAN_ERROR"
        decision_ready_iso = now_iso()
        print(f"  pipeline ERROR: {e} total={total_duration_ms:.1f} ms", flush=True)

    fetch_times.append(fetch_duration_ms)
    analysis_times.append(analysis_duration_ms)
    total_times.append(total_duration_ms)

    # For ranking: need same structure as m5_full_scan records
    # Build minimal record for later ranking
    per_asset.append({
        "symbol": sym,
        "status": status,
        "fetch_start": fetch_start_iso,
        "fetch_duration_ms": round(fetch_duration_ms, 2),
        "fetch_internal_ms": round(fetch_internal_ms, 2),
        "analysis_duration_ms": round(analysis_duration_ms, 2),
        "total_duration_ms": round(total_duration_ms, 2),
        "decision": decision_str,
        "audit_id": audit_id,
        "grade": grade,
        "confidence": confidence,
        "confluence": confluence,
        "buy_probability": buy_p,
        "sell_probability": sell_p,
        "wait_probability": wait_p,
        "error": error,
        "decision_ready": decision_ready_iso,
    })

    # For ranking eligibility: replicate top3_scanner eligibility
    # Need fields: status, decision, trade_allowed, prob_sum_ok, confidence, confluence
    trade_allowed = bool(getattr(decision, "trade_allowed", False)) if decision else False
    # prob sum
    prob_ok = False
    if buy_p is not None and sell_p is not None and wait_p is not None:
        s = float(buy_p or 0) + float(sell_p or 0) + float(wait_p or 0)
        prob_ok = abs(s - 100) < 0.5
    records_for_ranking.append({
        "internal_symbol": sym,
        "decision": decision_str,
        "status": status,
        "trade_allowed": trade_allowed,
        "prob_sum_ok": prob_ok,
        "confidence": confidence,
        "confluence": confluence,
        "grade": grade,
        "buy_probability": buy_p,
        "sell_probability": sell_p,
        "wait_probability": wait_p,
        "audit_id": audit_id,
        "execution_timestamp": decision_ready_iso,
        "total_duration_ms": total_duration_ms,
    })

scan_wall_end = time.perf_counter()
scan_wall_end_iso = now_iso()
total_scan_duration_ms = (scan_wall_end - scan_wall_start) * 1000

# --- RANKING ---
ranking_start = time.perf_counter()
# Use same formula as top3_scanner.py
GRADE_BONUS = {"A+":25,"A":20,"B":15,"C":10,"D":5,"N/A":0, None:0}
def prob_dominant(r):
    if r["decision"]=="BUY": return float(r["buy_probability"] or 0)
    if r["decision"]=="SELL": return float(r["sell_probability"] or 0)
    return 0.0
def confidence_100(r):
    c=r.get("confidence")
    if c is None: return 0.0
    if 0 < c <= 1.1:
        return c*100
    return c

eligible=[]
for r in records_for_ranking:
    if r.get("status")!="REAL_SIGNAL": continue
    if r.get("decision") not in ("BUY","SELL"): continue
    if not r.get("trade_allowed"): continue
    if not r.get("prob_sum_ok"): continue
    if r.get("confidence") is None: continue
    if r.get("confluence") is None: continue
    c100 = confidence_100(r)
    confl = float(r["confluence"] or 0)
    grade = r.get("grade")
    gbon = GRADE_BONUS.get(grade, 0)
    if gbon==0 and grade:
        gbon = GRADE_BONUS.get(str(grade).upper(), 0)
    pdom = prob_dominant(r)
    score = confl + c100*0.30 + gbon + pdom*0.20
    eligible.append((score, r))
eligible.sort(key=lambda x: (-x[0], x[1]["internal_symbol"], x[1]["audit_id"]))
top3 = eligible[:3]
ranking_end = time.perf_counter()
ranking_duration_ms = (ranking_end - ranking_start) * 1000
top3_ready_timestamp = now_iso()
top3_ready_perf = time.perf_counter()

# --- NEXT CANDLE ---
now_utc = datetime.now(timezone.utc)
next_candle = next_m5_boundary(now_utc)
seconds_until_next_candle = (next_candle - now_utc).total_seconds()
scan_duration_seconds = total_scan_duration_ms / 1000
next_candle_margin_seconds = seconds_until_next_candle - scan_duration_seconds

# Classification (no invented threshold; use raw)
if next_candle_margin_seconds < 0:
    readiness = "FAIL"
elif next_candle_margin_seconds < 30:
    readiness = "WARNING"
else:
    readiness = "PASS"

# --- STATS ---
def stats(arr):
    if not arr:
        return {"mean":0,"median":0,"p95":0,"max":0,"min":0,"sum":0}
    return {
        "mean": round(statistics.mean(arr),2),
        "median": round(statistics.median(arr),2),
        "p95": round(percentile(arr,95),2),
        "max": round(max(arr),2),
        "min": round(min(arr),2),
        "sum": round(sum(arr),2),
    }

fetch_stats = stats(fetch_times)
analysis_stats = stats(analysis_times)
total_stats = stats(total_times)

# Slowest
slowest_fetch = sorted(per_asset, key=lambda x: x["fetch_duration_ms"], reverse=True)[:5]
slowest_analysis = sorted(per_asset, key=lambda x: x["analysis_duration_ms"], reverse=True)[:5]
slowest_total = sorted(per_asset, key=lambda x: x["total_duration_ms"], reverse=True)[:5]

# Status breakdown
from collections import Counter
status_counts = Counter([p["status"] for p in per_asset])

# Bottleneck
fetch_sum = sum(fetch_times)
analysis_sum = sum(analysis_times)
ranking_ms = ranking_duration_ms
# Compare shares
shares = {"FETCH": fetch_sum, "ANALYSIS": analysis_sum, "RANKING": ranking_ms}
bottleneck = max(shares, key=lambda k: shares[k])

# Parallelization & cache candidates (evidence-based)
# Parallel candidates if sequential scan > 30s and fetch is dominant
parallel_candidate = "YES" if total_scan_duration_ms > 30000 and bottleneck in ("FETCH","ANALYSIS") else "NO"
# Cache candidate: if fetch is large share (>40% of total) and MTF does redundant fetches
fetch_share_pct = (fetch_sum / total_scan_duration_ms * 100) if total_scan_duration_ms else 0
cache_candidate = "YES" if fetch_share_pct > 30 else "NO"

# Assemble report
report = {
    "generated_at": now_iso(),
    "scan_wall_start": scan_wall_start_iso,
    "scan_wall_end": scan_wall_end_iso,
    "top3_ready_timestamp": top3_ready_timestamp,
    "universe_size": len(ALL_SYMBOLS),
    "assets_measured": len(per_asset),
    "total_scan_duration_ms": round(total_scan_duration_ms,2),
    "total_scan_seconds": round(total_scan_duration_ms/1000,2),
    "fetch_seconds": round(fetch_sum/1000,2),
    "analysis_seconds": round(analysis_sum/1000,2),
    "ranking_duration_ms": round(ranking_duration_ms,2),
    "ranking_seconds": round(ranking_duration_ms/1000,2),
    "top3_ready_seconds": round((top3_ready_perf - scan_wall_start)/1000,2) if 'top3_ready_perf' in locals() else round(total_scan_duration_ms/1000,2),
    "per_asset": per_asset,
    "fetch_stats_ms": fetch_stats,
    "analysis_stats_ms": analysis_stats,
    "total_stats_ms": total_stats,
    "slowest_fetch": [{"symbol": s["symbol"], "fetch_duration_ms": s["fetch_duration_ms"], "status": s["status"]} for s in slowest_fetch],
    "slowest_analysis": [{"symbol": s["symbol"], "analysis_duration_ms": s["analysis_duration_ms"], "status": s["status"]} for s in slowest_analysis],
    "slowest_total": [{"symbol": s["symbol"], "total_duration_ms": s["total_duration_ms"], "status": s["status"]} for s in slowest_total],
    "status_breakdown": dict(status_counts),
    "next_candle_timestamp": next_candle.isoformat(),
    "now_utc": now_utc.isoformat(),
    "seconds_until_next_candle": round(seconds_until_next_candle,2),
    "scan_duration_seconds": round(scan_duration_seconds,2),
    "next_candle_margin_seconds": round(next_candle_margin_seconds,2),
    "next_candle_readiness": readiness,
    "bottleneck": bottleneck,
    "bottleneck_shares_ms": {k: round(v,2) for k,v in shares.items()},
    "fetch_share_pct": round(fetch_share_pct,2),
    "parallelization_candidate": parallel_candidate,
    "cache_candidate": cache_candidate,
    "top3": [{"rank": i+1, "symbol": r["internal_symbol"], "decision": r["decision"], "score": round(sc,4), "audit_id": r["audit_id"]} for i,(sc,r) in enumerate(top3)],
    "eligible_count": len(eligible),
    "notes": {
        "path": "MarketDataService(provider=YahooAdapter) -> AnalysisPipeline.analyze() -> DecisionResult -> ranking -> Top-3",
        "production_logic_untouched": True,
        "fetch_probe": "isolated MarketDataService.get_data call per symbol (yfinance download 5m 5d)",
        "total_per_asset": "AnalysisPipeline.analyze() wall time (includes internal fetch + analysis + persistence)",
        "analysis_duration": "total - internal DataLoading stage (from PipelineProfiler) when available",
        "readiness_thresholds": "FAIL if margin<0, WARNING if 0<=margin<30s, PASS if >=30s (operational margin not defined in code — reported as recommendation)",
    }
}

OUT_JSON = ROOT / "reports" / "asset_universe" / "m5_operational_latency.json"
OUT_TXT = ROOT / "reports" / "asset_universe" / "m5_operational_latency.txt"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

# TXT
lines=[]
lines.append("M5 OPERATIONAL LATENCY — MERCURY-AI V1")
lines.append(f"Generated: {report['generated_at']}")
lines.append(f"Path: {report['notes']['path']}")
lines.append("")
lines.append(f"UNIVERSE_SIZE: {report['universe_size']}")
lines.append(f"ASSETS_MEASURED: {report['assets_measured']}")
lines.append(f"TOTAL_SCAN_SECONDS: {report['total_scan_seconds']}")
lines.append(f"FETCH_SECONDS: {report['fetch_seconds']} (sum of per-asset probe fetches)")
lines.append(f"ANALYSIS_SECONDS: {report['analysis_seconds']} (sum of per-asset analysis)")
lines.append(f"RANKING_SECONDS: {report['ranking_seconds']}")
lines.append(f"TOP3_READY_SECONDS: {report['top3_ready_seconds']} (wall clock start->top3)")
lines.append(f"WALL_TOTAL_MS: {report['total_scan_duration_ms']}")
lines.append("")
lines.append(f"FETCH  mean={fetch_stats['mean']} median={fetch_stats['median']} p95={fetch_stats['p95']} max={fetch_stats['max']} min={fetch_stats['min']}")
lines.append(f"ANALYSIS mean={analysis_stats['mean']} median={analysis_stats['median']} p95={analysis_stats['p95']} max={analysis_stats['max']}")
lines.append(f"TOTAL  mean={total_stats['mean']} median={total_stats['median']} p95={total_stats['p95']} max={total_stats['max']}")
lines.append("")
lines.append("STATUS_BREAKDOWN:")
for k,v in status_counts.items():
    lines.append(f"  {k}: {v}")
lines.append("")
lines.append("SLOWEST_FETCH:")
for s in report["slowest_fetch"]:
    lines.append(f"  {s['symbol']}: {s['fetch_duration_ms']} ms status={s['status']}")
lines.append("SLOWEST_ANALYSIS:")
for s in report["slowest_analysis"]:
    lines.append(f"  {s['symbol']}: {s['analysis_duration_ms']} ms status={s['status']}")
lines.append("SLOWEST_TOTAL:")
for s in report["slowest_total"]:
    lines.append(f"  {s['symbol']}: {s['total_duration_ms']} ms status={s['status']}")
lines.append("")
lines.append(f"NEXT_CANDLE_TIMESTAMP: {report['next_candle_timestamp']}")
lines.append(f"NOW_UTC: {report['now_utc']}")
lines.append(f"SECONDS_UNTIL_NEXT_CANDLE: {report['seconds_until_next_candle']}")
lines.append(f"SCAN_DURATION_SECONDS: {report['scan_duration_seconds']}")
lines.append(f"NEXT_CANDLE_MARGIN_SECONDS: {report['next_candle_margin_seconds']}")
lines.append(f"NEXT_CANDLE_READINESS: {report['next_candle_readiness']}")
lines.append("")
lines.append(f"BOTTLENECK: {report['bottleneck']} shares={report['bottleneck_shares_ms']} fetch_share={report['fetch_share_pct']}%")
lines.append(f"PARALLELIZATION_CANDIDATE: {report['parallelization_candidate']}")
lines.append(f"CACHE_CANDIDATE: {report['cache_candidate']}")
lines.append("")
lines.append(f"TOP3 eligible={report['eligible_count']}:")
for t in report["top3"]:
    lines.append(f"  {t['rank']}. {t['symbol']} {t['decision']} score={t['score']} audit={t['audit_id'][:16]}...")
if not report["top3"]:
    lines.append("  (none — no REAL_SIGNAL eligible)")
lines.append("")
lines.append("PER-ASSET (symbol fetch_ms analysis_ms total_ms status decision):")
for p in per_asset:
    lines.append(f"  {p['symbol']:12} fetch={p['fetch_duration_ms']:7.1f} analysis={p['analysis_duration_ms']:7.1f} total={p['total_duration_ms']:7.1f} {p['status']:16} {p['decision']:5} audit={p['audit_id'][:12]}")
OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
print("\n" + "\n".join(lines))
print(f"\nWrote {OUT_JSON} and {OUT_TXT}")
