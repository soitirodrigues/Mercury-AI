#!/usr/bin/env python3
"""
SENSEI SPRINT 3 — FASE A — PROFILING FORENSE MTF
Mede separadamente por ativo:
A) download/data loading
B) M1 C) M5 D) M15 E) H1 F) H4
Dentro de cada timeframe: preparação, IndicatorEngine, cada engine, agregação, conversões/cópias

Também mede: n chamadas, DataFrames criados, tamanho, chamadas repetidas, wall, CPU

Gera reports/m5_mtf_optimization/mtf_profile.json e mtf_profile.txt
"""
from __future__ import annotations
import sys, time, json, traceback, os, hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter
import statistics

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "reports" / "m5_mtf_optimization"
OUT_DIR.mkdir(parents=True, exist_ok=True)
JSON_OUT = OUT_DIR / "mtf_profile.json"
TXT_OUT = OUT_DIR / "mtf_profile.txt"

TARGET_SYMBOLS = ["BTC-USD", "ETH-USD", "EURUSD=X", "USDJPY=X", "AUDNZD=X"]

# Attempt imports
from mercury_ai.config.timeframes import YFINANCE_INTERVALS
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.analysis.mtf_engine import MTFEngine
from mercury_ai.data.indicator_engine import IndicatorEngine
from mercury_ai.analysis.trend_analyzer import TrendAnalyzer
from mercury_ai.analysis.smart_money.liquidity_engine import LiquidityEngine
from mercury_ai.analysis.volatility_engine import VolatilityEngine
from mercury_ai.analysis.market_structure_intelligence_engine import MarketStructureIntelligenceEngine

import pandas as pd

def now_iso(): return datetime.now(timezone.utc).isoformat()

# Global counters
counters = Counter()
df_created = 0
df_sizes = []

original_df_copy = pd.DataFrame.copy
def counted_copy(self, deep=True):
    global df_created, df_sizes
    df_created += 1
    try:
        df_sizes.append(len(self))
    except: df_sizes.append(0)
    return original_df_copy(self, deep=deep)

# Patch
pd.DataFrame.copy = counted_copy

# Also track IndicatorEngine calls and repeated inputs via hash
indicator_calls = []
indicator_hashes = Counter()

# Instrument provider fetch
fetch_times = defaultdict(list)
engine_times = defaultdict(list)

def hash_df(df):
    if df is None or df.empty: return "empty"
    try:
        # use last close + len + first timestamp
        last_close = float(df["close"].iloc[-1]) if "close" in df.columns else float(df["Close"].iloc[-1])
        return f"len{len(df)}_close{last_close:.4f}"
    except:
        return f"len{len(df)}"

print("="*80)
print("SENSEI SPRINT 3 — MTF PROFILING FORENSE")
print(f"Started: {now_iso()}")
print(f"Targets: {TARGET_SYMBOLS}")
print("="*80)

provider = MercuryDataProvider()
market_service = MarketDataService(provider=provider)
mtf = MTFEngine(providers=[provider])

# For CPU time if available
try:
    import psutil
    HAS_PSUTIL=True
except: HAS_PSUTIL=False

per_asset = []
per_timeframe_agg = defaultdict(list)
overall_stage_times = defaultdict(list)
total_wall_per_asset = []
repeated_inputs = Counter()

for sym in TARGET_SYMBOLS:
    print(f"\n[{sym}] — profiling MTF ...")
    asset_record = {
        "symbol": sym,
        "timeframes": {},
        "total_wall_ms": 0,
        "total_cpu_ms": 0,
        "fetch_total_ms": 0,
        "compute_total_ms": 0,
        "dataframes_created": 0,
        "df_rows": {},
        "errors": [],
    }
    # Reset per-asset counters
    start_df_created = df_created
    # Wall overall for this asset MTF
    t_asset_start = time.perf_counter()
    cpu_start = time.process_time()
    # We will replicate MTF loop with granular timing instead of calling mtf.analyze directly,
    # to capture per-TF breakdown identical to production code path.
    # But also call real mtf.analyze for equivalence baseline comparison at end.
    fetch_total = 0
    compute_total = 0
    tf_records = {}
    # Use same timeframes as production
    timeframes = ["M1","M5","M15","H1","H4"]
    # Track hashes to detect repeated inputs
    seen_hashes = {}
    for tf in timeframes:
        interval = YFINANCE_INTERVALS[tf]
        rec = {
            "interval": interval,
            "fetch_ms": 0,
            "prep_ms": 0,
            "indicator_ms": 0,
            "trend_ms": 0,
            "structure_swings_ms": 0,
            "structure_evaluate_ms": 0,
            "liquidity_ms": 0,
            "volatility_ms": 0,
            "tagging_ms": 0,
            "total_tf_ms": 0,
            "rows": 0,
            "status": "pending",
            "dataframe_hash": "",
        }
        t_tf_start = time.perf_counter()
        # A) download/data loading
        t_fetch = time.perf_counter()
        df = None
        try:
            df = mtf.market_service.get_data(sym, interval=interval, period="1mo")
            rec["fetch_ms"] = (time.perf_counter() - t_fetch)*1000
            fetch_total += rec["fetch_ms"]
            fetch_times[tf].append(rec["fetch_ms"])
            if df is None or df.empty:
                rec["status"]="absent"
                rec["rows"]=0
                rec["total_tf_ms"]=(time.perf_counter()-t_tf_start)*1000
                tf_records[tf]=rec
                asset_record["errors"].append(f"{tf}: absent")
                continue
            if len(df) < 20:
                rec["status"]="rejected"
                rec["rows"]=len(df)
                rec["total_tf_ms"]=(time.perf_counter()-t_tf_start)*1000
                tf_records[tf]=rec
                continue
            rec["rows"]=len(df)
            rec["dataframe_hash"]=hash_df(df)
            # repeated check
            h=rec["dataframe_hash"]
            if h in seen_hashes:
                repeated_inputs[h]+=1
            seen_hashes[h]=seen_hashes.get(h,0)+1

            # preparação dos dados (normalização já feita em get_data, mas medimos cópia/lowercase)
            t_prep = time.perf_counter()
            # No extra prep beyond get_data normalization; measure tiny
            rec["prep_ms"]=(time.perf_counter()-t_prep)*1000

            # IndicatorEngine
            t_ind = time.perf_counter()
            indicator_data = mtf.indicators.calculate(df)
            rec["indicator_ms"]=(time.perf_counter()-t_ind)*1000
            indicator_calls.append((sym,tf))
            indicator_hashes[rec["dataframe_hash"]] += 1

            from mercury_ai.models.market_data import MarketData
            market = MarketData(symbol=sym, timeframe=tf, **indicator_data)

            # Trend
            t_trend = time.perf_counter()
            trend_evs = mtf.trend.analyze(market)
            rec["trend_ms"]=(time.perf_counter()-t_trend)*1000

            # Structure: swings + profile (note double detect_swings in production)
            t_sw = time.perf_counter()
            swings, _ = mtf.structure.swing_engine.detect_swings(df)
            rec["structure_swings_ms"]=(time.perf_counter()-t_sw)*1000

            t_eval = time.perf_counter()
            profile, str_evs = mtf.structure.evaluate(df)
            rec["structure_evaluate_ms"]=(time.perf_counter()-t_eval)*1000

            # Liquidity
            t_liq = time.perf_counter()
            liq_result = mtf.liquidity.analyze(df, swings, profile)
            liq_evs = liq_result.evidences
            rec["liquidity_ms"]=(time.perf_counter()-t_liq)*1000

            # Volatility
            t_vol = time.perf_counter()
            vol_evs = mtf.volatility.analyze(df, market).evidences
            rec["volatility_ms"]=(time.perf_counter()-t_vol)*1000

            # tagging / aggregation (replace)
            t_tag = time.perf_counter()
            from dataclasses import replace
            for evs in [trend_evs, liq_evs, vol_evs, str_evs]:
                for e in evs:
                    e2 = replace(e, engine_name=f"{tf} - {e.engine_name}")
                    e2 = replace(e2, timeframe=tf)
            rec["tagging_ms"]=(time.perf_counter()-t_tag)*1000

            rec["status"]="processed"
            rec["total_tf_ms"]=(time.perf_counter()-t_tf_start)*1000
            compute_total += rec["total_tf_ms"] - rec["fetch_ms"]
            # aggregate per TF times
            for k in ["indicator_ms","trend_ms","structure_swings_ms","structure_evaluate_ms","liquidity_ms","volatility_ms"]:
                engine_times[k].append(rec[k])
                per_timeframe_agg[tf].append(rec[k])

        except Exception as e:
            rec["status"]=f"error: {type(e).__name__}: {e}"
            rec["total_tf_ms"]=(time.perf_counter()-t_tf_start)*1000
            asset_record["errors"].append(f"{tf}: {e}")
            traceback.print_exc()
        tf_records[tf]=rec

    # Aggregation time (consensus) — approximated as tiny
    t_cons = time.perf_counter()
    # Build dummy consensus to measure
    try:
        # Call real MTF for consensus timing comparison
        t_real_start = time.perf_counter()
        evs_real, consensus_real = mtf.analyze(sym)
        t_real = (time.perf_counter()-t_real_start)*1000
        asset_record["real_mtf_wall_ms"]= round(t_real,2)
        asset_record["real_evidences"]= len(evs_real)
        asset_record["real_consensus"]= {
            "global_bias": consensus_real.global_bias,
            "alignment": consensus_real.alignment_score,
            "timeframe_status": consensus_real.timeframe_status
        }
    except Exception as e:
        asset_record["real_mtf_error"]= str(e)
        traceback.print_exc()

    total_wall = (time.perf_counter()-t_asset_start)*1000
    cpu_wall = (time.process_time()-cpu_start)*1000
    asset_record["timeframes"]=tf_records
    asset_record["total_wall_ms"]= round(total_wall,2)
    asset_record["total_cpu_ms"]= round(cpu_wall,2)
    asset_record["fetch_total_ms"]= round(fetch_total,2)
    asset_record["compute_total_ms"]= round(compute_total,2)
    asset_record["dataframes_created"]= df_created - start_df_created
    asset_record["df_rows"]= {tf: rec["rows"] for tf, rec in tf_records.items()}
    # overall share
    per_asset.append(asset_record)
    total_wall_per_asset.append(total_wall)
    per_timeframe_agg["__fetch__"].append(fetch_total)
    overall_stage_times["fetch"].append(fetch_total)
    overall_stage_times["compute"].append(compute_total)
    print(f"  -> total_wall={total_wall:.1f}ms fetch={fetch_total:.1f}ms compute={compute_total:.1f}ms df_created={asset_record['dataframes_created']} real_mtf={asset_record.get('real_mtf_wall_ms','?')}ms")

# Aggregate bottleneck ranking
stage_totals = {}
for tf in ["M1","M5","M15","H1","H4"]:
    # sum fetch + indicator etc across assets
    tot_fetch = sum(per_asset[i]["timeframes"][tf]["fetch_ms"] for i in range(len(per_asset)) if tf in per_asset[i]["timeframes"])
    tot_ind = sum(per_asset[i]["timeframes"][tf]["indicator_ms"] for i in range(len(per_asset)) if tf in per_asset[i]["timeframes"])
    tot_sw = sum(per_asset[i]["timeframes"][tf]["structure_swings_ms"] for i in range(len(per_asset)) if tf in per_asset[i]["timeframes"])
    tot_eval = sum(per_asset[i]["timeframes"][tf]["structure_evaluate_ms"] for i in range(len(per_asset)) if tf in per_asset[i]["timeframes"])
    tot_liq = sum(per_asset[i]["timeframes"][tf]["liquidity_ms"] for i in range(len(per_asset)) if tf in per_asset[i]["timeframes"])
    tot_vol = sum(per_asset[i]["timeframes"][tf]["volatility_ms"] for i in range(len(per_asset)) if tf in per_asset[i]["timeframes"])
    stage_totals[f"{tf}_fetch"] = tot_fetch
    stage_totals[f"{tf}_indicator"] = tot_ind
    stage_totals[f"{tf}_swings"] = tot_sw
    stage_totals[f"{tf}_structure"] = tot_eval
    stage_totals[f"{tf}_liquidity"] = tot_liq
    stage_totals[f"{tf}_volatility"] = tot_vol

ranked = sorted(stage_totals.items(), key=lambda x: x[1], reverse=True)

# Build json
profile = {
    "generated_at": now_iso(),
    "targets": TARGET_SYMBOLS,
    "per_asset": per_asset,
    "aggregate": {
        "total_wall_avg_ms": round(statistics.mean(total_wall_per_asset),2) if total_wall_per_asset else 0,
        "total_wall_p50_ms": round(statistics.median(total_wall_per_asset),2) if total_wall_per_asset else 0,
        "total_wall_p95_ms": round(sorted(total_wall_per_asset)[int(len(total_wall_per_asset)*0.95)] if total_wall_per_asset else 0,2),
        "fetch_avg_ms": round(statistics.mean([a["fetch_total_ms"] for a in per_asset]),2) if per_asset else 0,
        "compute_avg_ms": round(statistics.mean([a["compute_total_ms"] for a in per_asset]),2) if per_asset else 0,
        "df_created_total": df_created,
        "df_sizes_sample": df_sizes[:20],
        "stage_totals_ms": {k: round(v,2) for k,v in stage_totals.items()},
        "bottleneck_ranking": [{"stage": k, "total_ms": round(v,2), "share_pct": round(v/sum(stage_totals.values())*100,2) if sum(stage_totals.values()) else 0} for k,v in ranked],
        "repeated_inputs": dict(repeated_inputs),
        "indicator_hashes": dict(indicator_hashes),
        "fetch_times_by_tf": {tf: [round(x,2) for x in vals] for tf, vals in fetch_times.items()},
        "engine_times": {k: {"avg": round(statistics.mean(v),2) if v else 0, "p95": round(sorted(v)[int(len(v)*0.95)] if v else 0,2)} for k,v in engine_times.items()},
    },
    "observations": {
        "sequential_downloads": "MTFEngine.analyze loops 5 TFs sequentially -> 5 * yfinance downloads serialized",
        "double_swings": "Per TF, detect_swings called twice (once explicit, once inside structure.evaluate) -> ~2x swing cost",
        "df_copies": f"pd.DataFrame.copy called {df_created} times across {len(per_asset)} assets (avg {df_created/len(per_asset) if per_asset else 0:.1f}/asset)",
        "atr_recalc": "ATR recalc in SwingEngine.calculate_atr + IndicatorEngine.calculate + VolatilityEngine -> same series recomputed 3x per TF",
        "m5_overlap": "Main pipeline fetches M5 5d; MTF re-fetches M5 1mo but provider ignores period -> same data fetched twice (cache miss due to different period key)",
    }
}

# Write json
JSON_OUT.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nWrote {JSON_OUT}")

# Write txt human readable
lines = []
lines.append("="*80)
lines.append("SENSEI SPRINT 3 — MTF PROFILE (FORENSIC)")
lines.append(f"Generated: {profile['generated_at']}")
lines.append(f"Targets: {', '.join(TARGET_SYMBOLS)}")
lines.append("="*80)
lines.append("")
lines.append(f"TOTAL WALL AVG per asset (MTF only, instrumented): {profile['aggregate']['total_wall_avg_ms']:.1f} ms  p50={profile['aggregate']['total_wall_p50_ms']:.1f} p95={profile['aggregate']['total_wall_p95_ms']:.1f}")
lines.append(f"FETCH avg: {profile['aggregate']['fetch_avg_ms']:.1f} ms   COMPUTE avg: {profile['aggregate']['compute_avg_ms']:.1f} ms")
lines.append(f"DataFrames created total: {profile['aggregate']['df_created_total']} (avg {profile['aggregate']['df_created_total']/len(per_asset) if per_asset else 0:.1f}/asset)")
lines.append("")
lines.append("BOTTLENECK RANKING (accumulated ms across 5 assets):")
for i, b in enumerate(profile['aggregate']['bottleneck_ranking'],1):
    lines.append(f"  {i:2}. {b['stage']:20} {b['total_ms']:8.1f} ms  {b['share_pct']:5.1f}%")
lines.append("")
lines.append("PER-ASSET BREAKDOWN:")
for a in per_asset:
    lines.append(f"  {a['symbol']:12} wall={a['total_wall_ms']:7.1f}ms fetch={a['fetch_total_ms']:6.1f} compute={a['compute_total_ms']:6.1f} df={a['dataframes_created']} real_mtf={a.get('real_mtf_wall_ms','-')}ms rows={a['df_rows']}")
    for tf, rec in a['timeframes'].items():
        lines.append(f"    {tf} ({rec['interval']:3}) fetch={rec['fetch_ms']:6.1f} ind={rec['indicator_ms']:5.1f} sw={rec['structure_swings_ms']:5.1f} eval={rec['structure_evaluate_ms']:5.1f} liq={rec['liquidity_ms']:5.1f} vol={rec['volatility_ms']:5.1f} tot={rec['total_tf_ms']:6.1f} [{rec['status']}] rows={rec['rows']}")
lines.append("")
lines.append("OBSERVATIONS:")
for k,v in profile['observations'].items():
    lines.append(f"  - {k}: {v}")
lines.append("")
lines.append("REPEATED INPUTS (same df hash):")
for h,c in profile['aggregate']['repeated_inputs'].items():
    lines.append(f"  {h}: {c} repeats")
if not profile['aggregate']['repeated_inputs']:
    lines.append("  (none — each TF hash differs as expected)")
lines.append("")
lines.append("ENGINE TIME avgs (ms):")
for k,v in profile['aggregate']['engine_times'].items():
    lines.append(f"  {k:25} avg={v['avg']:6.2f} p95={v['p95']:6.2f}")

TXT_OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {TXT_OUT}")
# also print to stdout
print("\n".join(lines))
print("\nProfiler DONE.")
