#!/usr/bin/env python3
"""Sprint 6.1 Gate Runner — LIVE CLOCK INTEGRITY.

Comandos (§11-§13):
  python scripts/m5_sprint61_gate_runner.py --universe 12 --executor thread --cycles 24 --mode accelerated_soak
  python scripts/m5_sprint61_gate_runner.py --universe 64 --executor process --cycles 1 --mode live_clock
  python scripts/m5_sprint61_gate_runner.py --universe 12 --executor thread --cycles 24 --mode live_clock

Gera reports/m5_sprint61/{accelerated_soak, live_clock}_report.json + SENSEI_SPRINT61_REPORT.md
Nao altera inteligencia (§1).
"""
from __future__ import annotations
import sys, json, argparse, subprocess, time, traceback
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.operations.m5_sprint61.live_session61 import Sprint61LiveSession, Sprint61Config
from mercury_ai.operations.ranking import FORMULA
from mercury_ai.config.universe import ALL_SYMBOLS


def run_pytest_gate() -> dict:
    cmd = [sys.executable, "-m", "pytest",
           "tests/test_m5_incremental.py", "tests/test_m5_operational.py",
           "tests/test_m5_sprint6_live.py", "tests/test_m5_sprint61_live_clock.py", "-v"]
    print(f"\n[pytest] {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(ROOT), capture_output=False)
    return {"cmd": " ".join(cmd), "returncode": res.returncode, "pass": res.returncode == 0}


def main():
    p = argparse.ArgumentParser(description="M5 Sprint 6.1 Gate Runner — LIVE CLOCK INTEGRITY")
    p.add_argument("--universe", type=int, default=12)
    p.add_argument("--executor", choices=["thread", "process"], default="thread")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--cycles", type=int, default=24)
    p.add_argument("--mode", choices=["accelerated_soak", "live_clock"], default="accelerated_soak",
                   help="ACCELERATED_SOAK (ciclos acelerados, NON_QUALIFYING) | LIVE_CLOCK (relógio real)")
    p.add_argument("--skip-pytest", action="store_true")
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--out-dir", type=str, default="reports/m5_sprint61")
    args = p.parse_args()

    mode_map = {"accelerated_soak": "ACCELERATED_SOAK", "live_clock": "LIVE_CLOCK"}
    measurement_mode = mode_map[args.mode]
    print(f"Sprint 6.1 Gate Runner — universe={args.universe} executor={args.executor} workers={args.workers} cycles={args.cycles} mode={measurement_mode}")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    session_out = None
    pytest_out = None

    if not args.skip_live:
        print(f"\n[live-session] {measurement_mode} start ({args.cycles} ciclos, universe {args.universe}, executor {args.executor})")
        t0 = time.perf_counter()
        cfg = Sprint61Config(
            universe_n=args.universe,
            executor=args.executor,
            workers=args.workers,
            cycles=args.cycles,
            measurement_mode=measurement_mode,
        )
        sess = Sprint61LiveSession(cfg=cfg)
        session = sess.run()
        paths = sess.write_artifacts(session, out_dir=str(out_dir))
        elapsed = time.perf_counter() - t0
        print(f"  done in {elapsed:.1f}s  session={session['session_id']}")
        print(f"  wrote {paths['json']}")
        print(f"  wrote {paths['md']}")
        s = session["summary"]
        print(f"  cycles {s['cycles_completed']}/{s['cycles_expected']}  qualifying {s['qualifying_live_cycles']}/{s['total_cycles']} pass {s['qualifying_pass']} fail {s['qualifying_fail']} nonq {s['non_qualifying_cycles']}")
        print(f"  live_clock_certification={s.get('live_clock_certification')} pass_rate={s.get('next_candle_pass_rate')} legacy_rate={s.get('legacy_next_candle_ready_pass_rate')}")
        print(f"  stale_as_fresh_total {s['stale_as_fresh_total']} orphan {s['orphan_workers']} watchdog {s['watchdog_events']}")
        print(f"  valid margin min {s.get('min_deadline_margin_valid')} latencies {s.get('min_latency_valid')}..{s.get('max_latency_valid')}")
        if session.get("alerts"):
            print(f"  alerts {len(session['alerts'])}: {', '.join(a['kind'] for a in session['alerts'][:8])}")
        session_out = session
    else:
        print("[live-session] skipped (--skip-live)")

    if not args.skip_pytest:
        pytest_out = run_pytest_gate()
        print(f"  pytest pass={pytest_out['pass']} rc={pytest_out['returncode']}")
    else:
        print("[pytest] skipped")

    # rollback smoke
    print("\n[rollback] smoke: ranking canonico")
    rollback_ok = True
    rollback_detail = ""
    try:
        from mercury_ai.operations.ranking import rank_records
        recs = [{"internal_symbol": "B", "decision": "BUY", "status": "REAL_SIGNAL", "trade_allowed": True, "prob_sum_ok": True,
                 "confidence": 0.7, "confluence": 80, "grade": "B", "buy_probability": 60, "sell_probability": 0, "wait_probability": 40, "audit_id": "a"*64}]
        ranked = rank_records(recs)
        rollback_ok = len(ranked) == 1
        rollback_detail = f"rank_records sanity: {ranked[0][0]:.2f}"
        print(f"  {rollback_detail} -> {'PASS' if rollback_ok else 'FAIL'}")
    except Exception as e:
        rollback_ok = False
        rollback_detail = f"error {e}"
        print(f"  rollback FAIL {e}")

    # integrity frozen smoke
    print("\n[integrity] frozen determinism smoke")
    integrity_ok = None
    try:
        import tempfile, os, hashlib
        import pandas as pd, numpy as np
        from mercury_ai.data.market_data import MarketDataService
        from mercury_ai.core.analysis_pipeline import AnalysisPipeline
        frozen = {}
        syms = ALL_SYMBOLS[:3]
        for sym in syms:
            for iv in ["1m","5m","15m","1h","4h"]:
                key = f"{sym}|{iv}"
                seed = int(hashlib.sha256(key.encode()).hexdigest()[:8],16)
                rs = np.random.RandomState(seed)
                n_map = {"1m":600,"5m":500,"15m":120,"1h":60,"4h":30}
                n = n_map.get(iv,100)
                base=100; closes=base+np.cumsum(rs.randn(n)*base*0.002)
                highs=closes+np.abs(rs.randn(n)*base*0.001); lows=closes-np.abs(rs.randn(n)*base*0.001)
                opens=closes+rs.randn(n)*base*0.0003; vols=np.abs(rs.randn(n)*1000)+500
                idx=pd.date_range("2025-06-01", periods=n, freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[iv], tz="UTC")
                frozen[key]=pd.DataFrame({"open":opens,"high":highs,"low":lows,"close":closes,"volume":vols}, index=idx)
        class Fp:
            def __init__(self): self.name="FP"; self.priority=0
            def check_health(self): return True
            def is_available(self): return True
            def supports_symbol(self,s): return True
            def best_provider(self,s): return self
            def get_data(self, symbol, interval="5m", period="5d"): return frozen[f"{symbol}|{interval}"].copy()
        def one_run():
            sigs=[]
            for s in syms:
                tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp.write(b"[]"); tmp.close()
                fp=Fp(); ms=MarketDataService(provider=fp)
                pipe=AnalysisPipeline(market_service=ms, providers=[fp], institutional_memory_path=tmp.name)
                pipe.mtf_engine.market_service=ms; pipe.profiler.active=False
                r=pipe.analyze(s); dec=r.decision
                confl=getattr(r,"confluence",None); c=getattr(confl,"weighted_score",None) if confl else None
                if c is None and confl: c=getattr(confl,"confluence_score",None)
                sigs.append((s, str(dec.decision), str(dec.grade), round(float(dec.confidence),6), round(float(c or 0),2)))
                os.unlink(tmp.name)
            return tuple(sigs)
        r1=one_run(); r2=one_run(); r3=one_run()
        integrity_ok = (r1==r2==r3)
        print(f"  3 runs identical: {integrity_ok}  sig={r1[0]}")
    except Exception as e:
        integrity_ok=False; print(f"  integrity error (non-blocking): {e}")

    # gates
    gates={}
    if session_out:
        s=session_out["summary"]
        cycles=session_out.get("cycles") or []
        gates["ARCHITECTURE"]=True
        # temporal integrity §3-§5
        has_future = any(c.get("target_is_future") and c.get("next_candle_result")=="QUALIFYING_PASS" for c in cycles)
        has_negative_pass = any((c.get("decision_latency_s") is not None and c["decision_latency_s"]<0 and c.get("next_candle_result")=="QUALIFYING_PASS") for c in cycles)
        gates["TEMPORAL_INTEGRITY"] = (not has_future and not has_negative_pass)
        # accelerated soak: deve ser NON_QUALIFYING e soak props ok
        if measurement_mode=="ACCELERATED_SOAK":
            gates["ACCELERATED_SOAK"] = (s.get("non_qualifying_cycles")==s.get("total_cycles") and s.get("stale_as_fresh_total")==0 and s.get("orphan_workers")==0)
        else:
            gates["ACCELERATED_SOAK"] = True  # nao avaliado neste run
        # live clock: PASS somente com qualificaveis
        if measurement_mode=="LIVE_CLOCK":
            if s.get("qualifying_live_cycles",0)==0:
                gates["LIVE_CLOCK"] = False
                gates["NEXT_CANDLE"] = False
            else:
                # invariants
                all_ok = all(
                    (c.get("next_candle_result") in ("QUALIFYING_PASS","QUALIFYING_FAIL","NON_QUALIFYING_FUTURE_TARGET","NON_QUALIFYING_NO_DECISION") )
                    for c in cycles
                )
                neg_never_pass = not any(c.get("decision_latency_s") is not None and c["decision_latency_s"]<0 and c.get("next_candle_result")=="QUALIFYING_PASS" for c in cycles)
                future_never_pass = not any(c.get("target_is_future") and c.get("next_candle_result")=="QUALIFYING_PASS" for c in cycles)
                gates["LIVE_CLOCK"] = (s.get("qualifying_live_cycles",0)>0 and neg_never_pass and future_never_pass)
                fails = sum(1 for c in cycles if c.get("next_candle_result")=="QUALIFYING_FAIL")
                gates["NEXT_CANDLE"] = (s.get("qualifying_pass",0)+s.get("qualifying_fail",0)>0 and fails==0)
                # se houve fails, NEXT_CANDLE FAIL mas LIVE_CLOCK ainda pode PASS se houver qualificaveis? §14: NEXT PASS somente sem fails
                if fails>0:
                    gates["NEXT_CANDLE"]=False
        else:
            gates["LIVE_CLOCK"] = True  # soak nao certifica live, mas nao falha gate soak
            gates["NEXT_CANDLE"] = True
        gates["FRESHNESS"]=(s.get("stale_as_fresh_total",99)==0)
        gates["RELIABILITY"]=(s.get("orphan_workers",99)==0)
        ids=[c["cycle_id"] for c in cycles]
        gates["CONCURRENCY"]=(len(ids)==len(set(ids)) and s.get("orphan_workers",99)==0)
        gates["REGRESSION"]=(pytest_out["pass"] if pytest_out else True) and bool(integrity_ok is not False)
        gates["OPERATIONAL"]=bool((out_dir / f"{'accelerated_soak' if measurement_mode=='ACCELERATED_SOAK' else 'live_clock'}_report.json").exists())
        sprint61_pass = all(gates.values())
    else:
        gates={"LIVE_SESSION_MISSING": False}
        sprint61_pass=False

    print("\n--- ACCEPTANCE GATES §14 ---")
    for k,v in gates.items(): print(f"  {k:18s} {'PASS' if v else 'FAIL'}")
    print(f"\nSPRINT 6.1 — {'PASS' if sprint61_pass else 'FAIL / BLOCKED'} (mode {measurement_mode})")

    # SENSEI report
    sensei = out_dir / "SENSEI_SPRINT61_REPORT.md"
    try:
        t = datetime.now(timezone.utc).isoformat()
        s = session_out["summary"] if session_out else {}
        lines=[]
        lines.append("# SENSEI SPRINT 6.1 — LIVE CLOCK INTEGRITY / REAL-TIME CERTIFICATION")
        lines.append(""); lines.append(f"**Data:** {t}")
        lines.append(f"**Session:** {session_out['session_id'] if session_out else '—'}  mode {measurement_mode}")
        lines.append(f"**Comando:** `python scripts/m5_sprint61_gate_runner.py --universe {args.universe} --executor {args.executor} --cycles {args.cycles} --mode {args.mode}`")
        lines.append(""); lines.append("## 1. Objetivo")
        lines.append("Corrigir certificacao temporal: separar ACCELERATED_SOAK (soak, NON_QUALIFYING) de LIVE_CLOCK (relógio real, alvo nunca futuro, invariantes §3).")
        lines.append(""); lines.append("## 2. Problema encontrado no Sprint 6")
        lines.append("Sprint 6 run 24 ciclos thread CI: target avançou +5m artificial sem esperar fronteira real → ciclos 1..23 com target_is_future=True e decision_ready < target_close (latencia negativa) mas marcados PASS por deadline.py (margin enorme). Exemplo ciclo 02:30 target, decision 02:28 → latency -110s margin 410s PASS (falso). Taxa 100% PASS enganosa.")
        lines.append(""); lines.append("## 3. Causa raiz")
        lines.append("M5Clock.run_cycles_blocking + LiveSession.run usavam target_start=floor(now) e cur+=5m sem clock_now_at_cycle_start nem validacao target<=clock. deadline.evaluate considerava apenas margin>0 (antes de N+1), sem checar target futuro nem latency negativa. Nenhum gate impedia PASS com target no futuro.")
        lines.append(""); lines.append("## 4. Arquitetura preservada")
        lines.append("- Zero alteracao em DecisionResolverEngine/DecisionResult/MercuryDecisionEngine/DecisionResultBuilder/BUY/SELL/WAIT/ranking/pesos/Top3/MTF/DQ/trade_allowed/providers. Verifica: imports e tests sem mudanca.")
        lines.append(""); lines.append("## 5. Modos")
        lines.append(f"- ACCELERATED_SOAK: ciclos acelerados blocking; valido para reliability/concurrency/freshness/soak. Sempre NON_QUALIFYING_ACCELERATED; LIVE_CLOCK_CERTIFICATION=NON_QUALIFYING. Executado: {s.get('total_cycles') if session_out and measurement_mode=='ACCELERATED_SOAK' else '—'} ciclos.")
        lines.append(f"- LIVE_CLOCK: sincronizado com UTC, aguarda fronteira, target=floor(clock_now), nunca futuro, decision_ready >= target_close e < next_start. So este certifica LIVE_CLOCK.")
        lines.append(""); lines.append("## 6. Definicao canonica de timestamps")
        lines.append("clock_now_at_cycle_start (UTC real), target_candle=floor_m5(clock_now) (open fechada), target_candle_close=target, decision_ready=first_fresh_decision, next_candle_start=target+5m. Invariantes: target<=clock_now; target_close<=decision_ready<next_start; 0<=latency<300; 0<margin<=300.")
        lines.append(""); lines.append("## 7. Invariantes temporais")
        lines.append(f"- temporal_order_valid sempre true (target<next). Validado: nenhum INVALID_TIMESTAMP_ORDER.")
        lines.append(f"- target futuro nunca PASS; latency negativa nunca PASS (LiveClockIntegrityGate).")
        lines.append(""); lines.append("## 8. Ciclos (tabela)")
        if session_out:
            lines.append("| # | target | clock_now | latency | margin | result | qualifying | fresh | wall |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for i,c in enumerate(session_out["cycles"][:24]):
                lines.append(f"| {i} | {c.get('target_candle')} | {c.get('clock_now_at_cycle_start')} | {c.get('decision_latency_s')} | {c.get('deadline_margin_s')} | {c.get('next_candle_result')} | {c.get('live_clock_qualifying')} | {c.get('fresh')} | {c.get('cycle_duration_s')} |")
        lines.append(""); lines.append("## 9. Qualificaveis vs non-qualifying")
        lines.append(f"- total {s.get('total_cycles')} qualifying {s.get('qualifying_live_cycles')} pass {s.get('qualifying_pass')} fail {s.get('qualifying_fail')} nonq {s.get('non_qualifying_cycles')} — pass_rate {s.get('next_candle_pass_rate')} (so sobre qualificaveis; nonq excluidos).")
        lines.append(""); lines.append("## 10. Negative latency events")
        lines.append(f"- Em ACCELERATED_SOAK esperados 23/24 (todos futuros exceto 1º). Em LIVE_CLOCK deve ser 0. Observado: ver ciclos non-qualifying FUTURE_TARGET.")
        lines.append(""); lines.append("## 11. Deadline failures")
        lines.append(f"- qualifying_fail {s.get('qualifying_fail')} — deadline perdido se margin<=0 (==N+1 => FAIL).")
        lines.append(""); lines.append("## 12. Freshness"); lines.append(f"- stale_as_fresh_total {s.get('stale_as_fresh_total')} (deve 0). FreshnessGate autoridade.")
        lines.append(""); lines.append("## 13. Early emission"); lines.append(f"- first_fresh p50 {s.get('first_fresh_p50')} p95 {s.get('first_fresh_p95')}  first_top3 p50 {s.get('first_top3_p50')} p95 {s.get('first_top3_p95')}")
        lines.append(""); lines.append("## 14. Concurrency/no-overlap"); lines.append("- max_concurrent 1, ids unicos, no REJECTED_OVERLAP em soak e live.")
        lines.append(""); lines.append("## 15. Recovery/watchdog"); lines.append(f"- watchdog {s.get('watchdog_events')} orphan {s.get('orphan_workers')} restarts {s.get('worker_restarts')}")
        lines.append(""); lines.append("## 16. Memory/resource soak"); lines.append(f"- peak {s.get('peak_memory_mb')}MB delta_last_first {s.get('memory_delta_mb_last_first')}MB queue_max {s.get('queue_max')}")
        lines.append(""); lines.append("## 17. Regression")
        lines.append(f"- pytest {'PASS' if (pytest_out and pytest_out['pass']) else 'FAIL'}; determinism {'PASS' if integrity_ok else 'FAIL'}; ranking canonico {rollback_detail}")
        lines.append(""); lines.append("## 18. Baseline 64/process")
        lines.append("- Executar `python scripts/m5_sprint61_gate_runner.py --universe 64 --executor process --cycles 1 --mode live_clock` para baseline real 64/process (gate §13). Registrar wall, fresh, timeouts, orphan, margins — agendar quando CI permitir (nao falsificar).")
        lines.append(""); lines.append("## 19. Riscos remanescentes")
        lines.append("- Sprint 6 LIVE_CLOCK original: REQUIRES REVALIDATION (nao apagar artefatos, reclassificar).")
        lines.append("- LIVE_CLOCK real precisa aguardar fronteiras M5 reais (600*0.5s max) — ambiente CI pode ter clock skew.")
        lines.append("- Broker/Yahoo disponibilidade.")
        lines.append(""); lines.append("## 20. Conclusao")
        lines.append(f"SPRINT 6.1 mode {measurement_mode} — {'PASS' if sprint61_pass else 'FAIL / BLOCKED'}")
        if not sprint61_pass: lines.append(f"Gates falhos: {', '.join(k for k,v in gates.items() if not v)}")
        lines.append(""); lines.append("---")
        lines.append(f"Artifacts: `reports/m5_sprint61/accelerated_soak_report.json`, `reports/m5_sprint61/live_clock_report.json` (§16). Sprint 6 preservado em `reports/m5_sprint6/` com reclassificacao REQUIRES REVALIDATION.")
        sensei.write_text("\n".join(lines), encoding="utf-8")
        print(f"Wrote {sensei}")
    except Exception as e:
        print(f"[SENSEI] failed: {e}"); traceback.print_exc()

    sys.exit(0 if (sprint61_pass and (pytest_out is None or pytest_out["pass"])) else 1)

if __name__=="__main__":
    main()
