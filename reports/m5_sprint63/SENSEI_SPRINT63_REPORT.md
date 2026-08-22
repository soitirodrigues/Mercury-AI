# SENSEI SPRINT 6.3 — OPERATIONAL RESILIENCE & DATA INTEGRITY — m5s63-3f15e368

**Data:** 2026-09-05T00:37:13.065876+00:00
**Session:** m5s63-3f15e368  mode LIVE_CLOCK  baseline m5s62-41db6545 (24/24 QUALIFYING_PASS)
**Comando:** `python scripts/m5_sprint63_gate_runner.py --universe 64 --executor process --cycles 6 --mode live_clock`
**Quick:** False

## 1. Regra Zero — Inteligencia nao alterada
- Nenhuma alteracao em DecisionResolverEngine/DecisionResult/MercuryDecisionEngine/BUY/SELL/WAIT/probabilities/confidence/confluence/ranking/pesos/Top3/trade_allowed/DQ/MTF/universe logic/AnalysisPipeline/ranking.py
- Formula canonica: `ranking_score = confluence_weighted (0-100) + confidence_100*0.30 + grade_bonus(A+25/A20/B15/C10/D5) + dominant_prob*0.20 ; tie-breaker: internal_symbol ASC, audit_id ASC. Eligibility: status==REAL_SIGNAL AND decision in (BUY,SELL) AND trade_allowed==true AND prob_sum_ok==true AND confidence not None AND confluence not None`
- Verificacao: imports e testes sem mudanca; rollback smoke no gate (ver determinism).

## 2. Baseline congelada §1
- frozen determinism: PASS (sequential==isolated==parallel)
- baseline ref 6.2 session m5s62-41db6545 wall 114.4 min (1.91 h)

## 3. Fault Harness §2-§10
- incidents: 9
- stale_as_fresh_total: 0 (required 0)
- error_as_wait_total: 0 (required 0)
- orphan_workers (fault): 0 (required 0)
- restart no_duplicate: True (required true)

## 4. Live Recovery §11 (6 ciclos LIVE_CLOCK)
- cycles 6/6 qualifying 6 pass 6 fail 0 rate 1.0
- stale_as_fresh 0 orphan 0 no_duplicate True status LIVE_RECOVERY PASS
- wall 26.2 min (0.44 h) start 2026-09-04T23:35:19.609609+00:00 end 2026-09-05T00:01:34.250525+00:00

| cycle | clock_start | target | close | decision_ready | next_start | latency | margin | qualifying | result |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2026-09-04T23:35:19.609609+00:00 | 2026-09-04T23:35:00+00:00 | 2026-09-04T23:35:00+00:00 | 2026-09-04T23:35:33.914609+00:00 | 2026-09-04T23:40:00+00:00 | 33.914609 | 266.085391 | True | QUALIFYING_PASS |
| 1 | 2026-09-04T23:40:00.053269+00:00 | 2026-09-04T23:40:00+00:00 | 2026-09-04T23:40:00+00:00 | 2026-09-04T23:40:20.292234+00:00 | 2026-09-04T23:45:00+00:00 | 20.292234 | 279.707766 | True | QUALIFYING_PASS |
| 2 | 2026-09-04T23:45:00.008409+00:00 | 2026-09-04T23:45:00+00:00 | 2026-09-04T23:45:00+00:00 | 2026-09-04T23:45:18.142384+00:00 | 2026-09-04T23:50:00+00:00 | 18.142384 | 281.857616 | True | QUALIFYING_PASS |
| 3 | 2026-09-04T23:50:00.050236+00:00 | 2026-09-04T23:50:00+00:00 | 2026-09-04T23:50:00+00:00 | 2026-09-04T23:50:13.926454+00:00 | 2026-09-04T23:55:00+00:00 | 13.926454 | 286.073546 | True | QUALIFYING_PASS |
| 4 | 2026-09-04T23:55:00.051000+00:00 | 2026-09-04T23:55:00+00:00 | 2026-09-04T23:55:00+00:00 | 2026-09-04T23:55:13.408830+00:00 | 2026-09-05T00:00:00+00:00 | 13.40883 | 286.59117 | True | QUALIFYING_PASS |
| 5 | 2026-09-05T00:00:00.050639+00:00 | 2026-09-05T00:00:00+00:00 | 2026-09-05T00:00:00+00:00 | 2026-09-05T00:00:14.381956+00:00 | 2026-09-05T00:05:00+00:00 | 14.381956 | 285.618044 | True | QUALIFYING_PASS |

## 5. Observabilidade §12
- cada incidente possui incident_id/fault_type/timestamp/cycle_id/target_candle/affected_asset/detection_time/recovery_start/recovery_complete/recovery_duration/final_state (total 9)

## 6. Performance before/after §13

| Metrica | Baseline 6.2 | Pos-fault (6.3) |
|---|---|---|
| decision latency p50 | 13.1904285 | 16.26217 |
| deadline margin p50 | 286.8095715 | 283.73783000000003 |
| memory peak | 13.2 | 12.1 |
| orphan workers | 0 | 0 |
| stale as fresh | 0 | 0 |

## 7. Gates §16
- ARCHITECTURE: PASS
- BASELINE_INTEGRITY: PASS
- DATA_INTEGRITY: PASS
- WORKER_CRASH: PASS
- WORKER_TIMEOUT: PASS
- ASSET_ISOLATION: PASS
- QUEUE_PRESSURE: PASS
- WATCHDOG: PASS
- GRACEFUL_SHUTDOWN: PASS
- RESTART_INTEGRITY: PASS
- FRESHNESS: PASS
- CONCURRENCY: PASS
- RECOVERY: PASS
- LIVE_RECOVERY: PASS
- PERFORMANCE: PASS
- RESOURCE_SOAK: PASS
- DETERMINISM: PASS
- REGRESSION: PASS
- OPERATIONAL: PASS

## 8. Status final §17
**SPRINT 6.3 = OPERATIONAL RESILIENCE CERTIFIED**

## 9. Riscos remanescentes
- Broker/Yahoo disponibilidade (DATA_UNAVAILABLE -> NON_QUALIFYING).
- Clock skew host (NTP) — validar UTC.
- Sessao LIVE de 6 ciclos ~30min suscetivel a rede; recovery validado.
- Nao habilitar envio de ordens (Sprint 6.3 § entrega).

## 10. Artefatos §15
- fault: `reports\m5_sprint63\m5s63-3f15e368\fault_injection_report.json` / `reports\m5_sprint63\m5s63-3f15e368\fault_injection_report.md`
- recovery: `reports\m5_sprint63\m5s63-bae58cad\recovery_live_clock_report.json`
- sensei: `reports\m5_sprint63\m5s63-3f15e368\SENSEI_SPRINT63_REPORT.md` (canonico `reports\m5_sprint63\SENSEI_SPRINT63_REPORT.md`)
- session dir: `reports\m5_sprint63\m5s63-3f15e368`  session_id unico sem sobrescrever historico
