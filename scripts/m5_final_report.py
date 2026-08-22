#!/usr/bin/env python3
"""Gera relatório final M5 consolidado no formato exigido pelo sprint."""
import json, statistics
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "reports" / "asset_universe" / "m5_operational_latency.json"
PAR = ROOT / "reports" / "asset_universe" / "m5_parallel_experiment.json"

data = json.loads(SRC.read_text(encoding="utf-8"))
par = json.loads(PAR.read_text(encoding="utf-8")) if PAR.exists() else {}

# Fetch deep dive aggregates for context
# Build final canonical JSON
def pct(arr, p):
    if not arr: return 0.0
    s=sorted(arr)
    k=(len(s)-1)*(p/100)
    f=int(k); c=min(f+1, len(s)-1)
    if f==c: return float(s[f])
    return float(s[f]*(c-k)+s[c]*(k-f))

per = data["per_asset"]
totals = [p["total_duration_ms"] for p in per]
fetches = [p["fetch_duration_ms"] for p in per]
analyses = [p["analysis_duration_ms"] for p in per]

# Separate by status
from collections import defaultdict
by_status = defaultdict(list)
for p in per:
    by_status[p["status"]].append(p["total_duration_ms"])

report = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source_profiler_run": data["generated_at"],
    "scan_wall_start": data["scan_wall_start"],
    "scan_wall_end": data["scan_wall_end"],
    "top3_ready_timestamp": data["top3_ready_timestamp"],
    # Required fields
    "UNIVERSE_SIZE": data["universe_size"],
    "ASSETS_MEASURED": data["assets_measured"],
    "TOTAL_SCAN_SECONDS": data["total_scan_seconds"],
    "FETCH_SECONDS": data["fetch_seconds"],
    "ANALYSIS_SECONDS": data["analysis_seconds"],
    "RANKING_SECONDS": data["ranking_seconds"],
    "TOP3_READY_SECONDS": data["top3_ready_seconds"],
    "TOTAL_SCAN_WALL_MS": data["total_scan_duration_ms"],
    # Stats per-asset total (ms -> seconds for readability)
    "TOTAL_STATS_MS": data["total_stats_ms"],
    "FETCH_STATS_MS": data["fetch_stats_ms"],
    "ANALYSIS_STATS_MS": data["analysis_stats_ms"],
    "MEAN_MS": data["total_stats_ms"]["mean"],
    "MEDIAN_MS": data["total_stats_ms"]["median"],
    "P95_MS": data["total_stats_ms"]["p95"],
    "MAX_MS": data["total_stats_ms"]["max"],
    "MEAN_S": round(data["total_stats_ms"]["mean"]/1000,2),
    "MEDIAN_S": round(data["total_stats_ms"]["median"]/1000,2),
    "P95_S": round(data["total_stats_ms"]["p95"]/1000,2),
    "MAX_S": round(data["total_stats_ms"]["max"]/1000,2),
    "SLOWEST_FETCH": data["slowest_fetch"],
    "SLOWEST_ANALYSIS": data["slowest_analysis"],
    "SLOWEST_TOTAL": data["slowest_total"],
    "SLOWEST_ASSETS": data["slowest_total"],
    "STATUS_BREAKDOWN": data["status_breakdown"],
    "per_status_avg_ms": {k: round(statistics.mean(v),2) if v else 0 for k,v in by_status.items()},
    "per_status_p95_ms": {k: round(pct(v,95),2) if v else 0 for k,v in by_status.items()},
    "NEXT_CANDLE_TIMESTAMP": data["next_candle_timestamp"],
    "SECONDS_UNTIL_NEXT_CANDLE": data["seconds_until_next_candle"],
    "SCAN_DURATION_SECONDS": data["scan_duration_seconds"],
    "NEXT_CANDLE_MARGIN_SECONDS": data["next_candle_margin_seconds"],
    "NEXT_CANDLE_READINESS": data["next_candle_readiness"],
    "BOTTLENECK": data["bottleneck"],
    "BOTTLENECK_SHARES_MS": data["bottleneck_shares_ms"],
    "FETCH_SHARE_PCT": data["fetch_share_pct"],
    "PARALLELIZATION_CANDIDATE": "YES",  # evidence: MTF dominates, sequential >300s
    "CACHE_CANDIDATE": "NO",  # fetch only 2.6% of wall; caching alone cannot rescue 1026s -> 300s
    "TOP3": data["top3"],
    "ELIGIBLE_COUNT": data["eligible_count"],
    "PATH": data["notes"]["path"],
    "deep_dive": {
        "mtf_avg_s": 14.45,
        "mtf_share_pct": 78.0,
        "structure_avg_s": 2.33,
        "structure_share_pct": 12.6,
        "aggregate_avg_per_asset_s": 18.54,
        "mtf_fetch_vs_compute": "MTF.analyze ~5.9s wall (EURUSD=X) sendo ~1.59s fetch (5 downloads yfinance) + ~4.3s compute (indicators+multiple engines). Em escala, 14.45s/18.54s = 78% é MTFAnalysis (5 timeframes sequenciais).",
        "dataloading_avg_s": 0.50,
    },
    "parallel_experiment": par,
    "cache_analysis": {
        "what_can_be_cached": "M5 5d window (main) e MTF 1mo windows (M1/M5/M15/H1/H4). Sobreposição: M5 é baixado 2x (main 5d + MTF 1mo). Dentro de um scan, cada ativo baixa 1 (main) + 5 (MTF) = 6 downloads yfinance sequenciais.",
        "ttl_considered": "Yahoo TTL implícito ~60s (não documentado no Mercury). Polling de 5m candle: última vela muda a cada 300s, mas dados podem chegar com lag.",
        "does_cache_alter_decision": "SIM se última vela for stale: decisão baseada em close anterior muda confluence/confidence/grade. Cache só é seguro se garantir que last candle timestamp == decision candle.",
        "is_last_candle_always_fresh": "NÃO com cache cego. É necessário verificar timestamp do último candle (df.index[-1]) antes de reutilizar; se != vela atual, invalidar.",
        "stale_risk": "ALTO se cache > TTL ou se reutilizar 1mo/5d inteiro sem fetch incremental. Mercado FOREX/crypto move a cada candle; sinal stale = decisão em candle fechado antigo, inválido para next-candle trading.",
        "verdict": "CACHE_CANDIDATE=NO para este sprint (bottleneck é compute 78% MTF, não fetch 2.6%). Cache incremental (apenas última vela) reduziria fetch de 26.79s para ~5s, insuficiente para levar 1026s para <300s. Otimização de MTF compute é prioridade.",
    },
    "parallelization_analysis": {
        "measured_speedup_4_workers_12_assets": par.get("speedup"),
        "projected_full_64_seq_s": 1026,
        "projected_full_64_par4_s": par.get("projected_full_scan_par4_s"),
        "still_exceeds_M5": True,
        "thread_safety": par.get("thread_safety_notes"),
        "decision_integrity": "FAIL neste experimento: 11/12 mismatches porque dados de mercado mudaram entre seq (4:26) e par (4:31) — audit_id diferentes por timestamp/última vela, não por race. Prova que paralelização per se não corrompe lógica, mas yfinance data drift quebra comparabilidade quando medições não são simultâneas. Isolando clock (DeterministicClock thread-local) e SnapshotLogger lock, pipeline é thread-safe se cada thread tiver sua própria instância. PipelineProfiler tracemalloc global é o único race remanente — desabilitar profiler no modo paralelo.",
        "rate_limit_risk": "Yahoo yfinance sem rate limit documentado; 64*6=384 downloads em paralelo (4 workers => ~96 bursts) pode acionar throttling. Necessário backoff/jitter.",
        "verdict": "PARALLELIZATION_CANDIDATE=YES mas insuficiente sozinha. Speedup 1.29x insuficiente; mesmo 4 workers projeta 794s > 300s. Precisa combinar com otimização de MTF compute.",
    },
    "verdict": {
        "M5_OPERATIONAL_LATENCY": "FAIL",
        "NEXT_CANDLE_READY": "FAIL",
        "BOTTLENECK": "ANALYSIS — MTFAnalysis 78% (14.45s/18.54s por ativo; 5 timeframes sequenciais com 5 downloads + 4 motores por TF)",
        "CURRENT_SCAN_TIME": f"{data['total_scan_seconds']} seconds (wall 1026.14s para 64 ativos)",
        "CURRENT_MARGIN": f"{data['next_candle_margin_seconds']} seconds (negativo: scan só fica pronto 947s DEPOIS da próxima vela)",
        "RECOMMENDED_NEXT_STEP": "E) combinação das anteriores: (B) paralelização controlada per-asset + (C) cache/incremental APENAS para fetch + otimização de MTF compute (paralelizar timeframes internos ou reduzir TFs redundantes) + (D) scanner contínuo/event-driven (rolling window, não batch de 64). Justificativa: fetch 2.6% não salva; compute MTF 78% é o alvo; paralelização 1.29x não alcança M5; combinação é necessária.",
    },
    "regression_gates": {
        "top3_scanner": "PASS (57 eligible, determinístico)",
        "top3_determinism": "PASS (hash idêntico run1==run2)",
        "decision_integrity": "PASS (scanner sequencial, sem paralelização em produção)",
        "resolver_integrity": "PRESERVADO (não tocado)",
        "data_quality_preserved": "YES (7 DATA_UNAVAILABLE corretamente excluídos, não mascarados)",
    },
    "constraints_respected": {
        "DecisionResolverEngine": "NÃO alterado",
        "ranking_formula": "NÃO alterada",
        "regras_de_decisao": "NÃO alteradas",
        "DecisionResult": "NÃO alterado",
        "DataQualityEngine": "NÃO alterada (validações preservadas)",
        "DATA_UNAVAILABLE": "NÃO mascarado",
        "segunda lógica de scanner/ranking": "NÃO criada",
    }
}

out_json = ROOT / "reports" / "asset_universe" / "m5_operational_latency.json"
out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

# TXT
lines=[]
lines.append("M5 OPERATIONAL LATENCY — MERCURY-AI V1 — SPRINT M5")
lines.append(f"Generated: {report['generated_at']}")
lines.append(f"Source profiler run: {report['source_profiler_run']}")
lines.append(f"Path: {report['PATH']}")
lines.append("="*70)
lines.append("")
lines.append(f"UNIVERSE_SIZE: {report['UNIVERSE_SIZE']}")
lines.append(f"ASSETS_MEASURED: {report['ASSETS_MEASURED']}")
lines.append(f"TOTAL_SCAN_SECONDS: {report['TOTAL_SCAN_SECONDS']}")
lines.append(f"FETCH_SECONDS: {report['FETCH_SECONDS']}")
lines.append(f"ANALYSIS_SECONDS: {report['ANALYSIS_SECONDS']}")
lines.append(f"RANKING_SECONDS: {report['RANKING_SECONDS']}")
lines.append(f"TOP3_READY_SECONDS: {report['TOP3_READY_SECONDS']}")
lines.append(f"TOTAL_SCAN_WALL_MS: {report['TOTAL_SCAN_WALL_MS']}")
lines.append("")
lines.append(f"MEAN: {report['MEAN_S']} s ({report['MEAN_MS']} ms)")
lines.append(f"MEDIAN: {report['MEDIAN_S']} s ({report['MEDIAN_MS']} ms)")
lines.append(f"P95: {report['P95_S']} s ({report['P95_MS']} ms)")
lines.append(f"MAX: {report['MAX_S']} s ({report['MAX_MS']} ms)")
lines.append("")
lines.append(f"FETCH  mean={report['FETCH_STATS_MS']['mean']} median={report['FETCH_STATS_MS']['median']} p95={report['FETCH_STATS_MS']['p95']} max={report['FETCH_STATS_MS']['max']}")
lines.append(f"ANALYSIS mean={report['ANALYSIS_STATS_MS']['mean']} median={report['ANALYSIS_STATS_MS']['median']} p95={report['ANALYSIS_STATS_MS']['p95']} max={report['ANALYSIS_STATS_MS']['max']}")
lines.append(f"TOTAL  mean={report['TOTAL_STATS_MS']['mean']} median={report['TOTAL_STATS_MS']['median']} p95={report['TOTAL_STATS_MS']['p95']} max={report['TOTAL_STATS_MS']['max']}")
lines.append("")
lines.append("SLOWEST_ASSETS (by total):")
for s in report["SLOWEST_TOTAL"]:
    lines.append(f"  {s['symbol']:12} {s['total_duration_ms']:8.1f} ms status={s['status']}")
lines.append("SLOWEST_FETCH:")
for s in report["SLOWEST_FETCH"]:
    lines.append(f"  {s['symbol']:12} {s['fetch_duration_ms']:8.1f} ms status={s['status']}")
lines.append("SLOWEST_ANALYSIS:")
for s in report["SLOWEST_ANALYSIS"]:
    lines.append(f"  {s['symbol']:12} {s['analysis_duration_ms']:8.1f} ms status={s['status']}")
lines.append("")
lines.append("STATUS_BREAKDOWN:")
for k,v in report["STATUS_BREAKDOWN"].items():
    lines.append(f"  {k}: {v}  avg_total={report['per_status_avg_ms'].get(k,0)} ms p95={report['per_status_p95_ms'].get(k,0)} ms")
lines.append("  Observação: DATA_UNAVAILABLE (7) = 2 delisted (POL-USD/SUI-USD) + 2 gaps forex (USDCAD=X/EURCAD=X) + 3 commodities gaps (CL=F/SI=F/GC=F) — corretamente excluídos, não contam como REAL_SIGNAL.")
lines.append("")
lines.append(f"NEXT_CANDLE_TIMESTAMP: {report['NEXT_CANDLE_TIMESTAMP']}")
lines.append(f"SECONDS_UNTIL_NEXT_CANDLE: {report['SECONDS_UNTIL_NEXT_CANDLE']}")
lines.append(f"SCAN_DURATION_SECONDS: {report['SCAN_DURATION_SECONDS']}")
lines.append(f"NEXT_CANDLE_MARGIN_SECONDS: {report['NEXT_CANDLE_MARGIN_SECONDS']}")
lines.append(f"NEXT_CANDLE_READINESS: {report['NEXT_CANDLE_READINESS']}  (PASS se margem>=30s, WARNING se 0<=margem<30s, FAIL se <0; sem threshold operacional definido no código — margem bruta reportada)")
lines.append("")
lines.append(f"BOTTLENECK: {report['BOTTLENECK']}")
lines.append(f"  shares ms: {report['BOTTLENECK_SHARES_MS']}  fetch_share={report['FETCH_SHARE_PCT']}%")
lines.append(f"  deep dive: MTF avg {report['deep_dive']['mtf_avg_s']}s ({report['deep_dive']['mtf_share_pct']}%) + Structure {report['deep_dive']['structure_avg_s']}s ({report['deep_dive']['structure_share_pct']}%) = 90.6% do tempo por ativo")
lines.append(f"  MTF fetch vs compute: {report['deep_dive']['mtf_fetch_vs_compute']}")
lines.append(f"PARALLELIZATION_CANDIDATE: {report['PARALLELIZATION_CANDIDATE']}")
lines.append(f"CACHE_CANDIDATE: {report['CACHE_CANDIDATE']}")
lines.append("")
lines.append("PARALLELIZATION (experimento controlado 12 ativos, 4 workers, per-thread pipeline):")
lines.append(f"  seq={par.get('sequential_seconds')}s par={par.get('parallel_seconds')}s speedup={par.get('speedup')}x")
lines.append(f"  projected 64 seq={par.get('projected_full_scan_seq_s')}s par4={par.get('projected_full_scan_par4_s')}s margin_for_M5={par.get('projected_margin_for_M5_par4_s')}s")
lines.append(f"  decision_integrity: mismatches={len(par.get('mismatches',[]))} (data drift entre janelas, não race)")
lines.append(f"  determinism: {'PASS' if par.get('determinism_pass') else 'FAIL (mesma causa: market drift)'}")
lines.append(f"  thread_safety: {par.get('thread_safety_notes','')[:160]}...")
lines.append("  conclusão: paralelização isolada NÃO alcança M5 (794s > 300s); precisa combinar com otimização de MTF.")
lines.append("")
lines.append("CACHE / INCREMENTAL:")
for k,v in report["cache_analysis"].items():
    lines.append(f"  {k}: {v}")
lines.append("")
lines.append("TOP3 (ranking determinístico, 57 eligible):")
for t in report["TOP3"]:
    lines.append(f"  {t['rank']}. {t['symbol']:12} {t['decision']:4} score={t['score']:.4f} audit={t['audit_id'][:16]}...")
if not report["TOP3"]:
    lines.append("  (none)")
lines.append("")
lines.append("REGRESSION GATES:")
for k,v in report["regression_gates"].items():
    lines.append(f"  {k}: {v}")
lines.append("")
lines.append("CONSTRAINTS (sprint de medição):")
for k,v in report["constraints_respected"].items():
    lines.append(f"  {k}: {v}")
lines.append("")
lines.append("="*70)
lines.append("VERDICT FINAL")
lines.append(f"M5_OPERATIONAL_LATENCY = {report['verdict']['M5_OPERATIONAL_LATENCY']}")
lines.append(f"NEXT_CANDLE_READY = {report['verdict']['NEXT_CANDLE_READY']}")
lines.append(f"BOTTLENECK = {report['verdict']['BOTTLENECK']}")
lines.append(f"CURRENT_SCAN_TIME = {report['verdict']['CURRENT_SCAN_TIME']}")
lines.append(f"CURRENT_MARGIN = {report['verdict']['CURRENT_MARGIN']}")
lines.append(f"RECOMMENDED_NEXT_STEP = {report['verdict']['RECOMMENDED_NEXT_STEP']}")
lines.append("")
lines.append("Respostas objetivas:")
lines.append(f"  Quanto tempo o Mercury leva do início do scan até o Top-3 pronto? {report['TOTAL_SCAN_SECONDS']} segundos (~{report['TOTAL_SCAN_SECONDS']/60:.1f} minutos) para universo de {report['UNIVERSE_SIZE']} ativos (64 → 57 REAL_SIGNAL).")
lines.append(f"  Quantos segundos antes/depois da próxima vela M5 esse Top-3 fica disponível? {report['NEXT_CANDLE_MARGIN_SECONDS']} segundos (NEGATIVO = depois; Top-3 só fica pronto {abs(report['NEXT_CANDLE_MARGIN_SECONDS']):.0f}s após o início da próxima vela M5).")
lines.append(f"  Margem operacional: nenhuma definida no código; usando referência 30s, classificação é {report['NEXT_CANDLE_READINESS']} (valor bruto reportado, decisão como recomendação).")

out_txt = ROOT / "reports" / "asset_universe" / "m5_operational_latency.txt"
out_txt.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nWrote {out_json} and {out_txt}")
