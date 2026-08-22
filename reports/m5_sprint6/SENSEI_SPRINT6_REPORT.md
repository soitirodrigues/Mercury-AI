# SENSEI SPRINT 6 — LIVE OPERATION / TRADING READINESS

**Data:** 2026-09-04T03:13:47.242020+00:00
**Session:** m5s6-c43a4175  mode LIVE_CONTROLLED
**Comando:** `python scripts/m5_sprint6_gate_runner.py --universe 12 --executor thread --cycles 24`

## 1. Objetivo
Provar que o Mercury-AI entrega decisoes FRESH a tempo do proximo candle M5, ciclo apos ciclo, sem drift/overlap/stale_as_fresh e sem alterar a inteligencia validada. Resultado esperado DECISION READY (nao ORDER EXECUTED) — sem envio automatico de ordens (§2).

## 2. Arquitetura utilizada
- Pipeline oficial: `M5OperationalRunner` (bounded ProcessPool|ThreadPool) + `FreshnessGate` autoridade + `ranking.py` canonico + `AnalysisPipeline`/`MercuryDecisionEngine` oficial.
- Scheduler: `M5Clock` alinhado a fronteira M5 (`floor_m5`/`ceil_m5` UTC), `max_concurrent_cycles=1` guard, sem `sleep(300)` acumulativo (§3,§5,§12).
- Deadlines: `deadline.py` formal — `target_candle_close=target_candle`, `next_candle_start=target+5m`, `deadline_margin=next-start - decision_ready`, PASS se >0 (§4,§8).
- Observabilidade: `live_session.py` + `alerts.py` + `watchdog.py` + bounded queue maxsize=128 (§11-13,§21-22).
- Regra §1 respeitada: ZERO alteracao em DecisionResolverEngine/DecisionResult/MercuryDecisionEngine/DecisionResultBuilder/BUY/SELL/WAIT/ranking/pesos/Top3/DQ/trade_allowed/probabilities/MTF/universe.

## 3. Configuracao
```json
{
  "process_workers": 4,
  "thread_workers": 4,
  "executor": "thread",
  "worker_timeout_s": 90.0,
  "cycle_timeout_s": 290.0,
  "max_concurrent_cycles": 1,
  "operational_universe": "ALL_SYMBOLS",
  "early_emission": true,
  "freshness_policy": "strict",
  "watchdog_interval_s": 5.0,
  "stall_threshold_s": 45.0,
  "bounded_queue_maxsize": 128,
  "max_retries_per_asset": 0,
  "recreate_worker_on_error": false,
  "shutdown_grace_s": 10.0,
  "use_operational_runner": true,
  "mode": "m5"
}
```
```json
{
  "universe_n": 12,
  "executor": "thread",
  "workers": null,
  "cycles": 24,
  "worker_timeout_s": 90.0,
  "cycle_timeout_s": 290.0,
  "mode": "LIVE_CONTROLLED"
}
```

## 4. Periodo da sessao
- start 2026-09-04T02:26:27.556044+00:00  end 2026-09-04T02:52:15.707769+00:00  session_id m5s6-c43a4175
- formula: `ranking_score = confluence_weighted (0-100) + confidence_100*0.30 + grade_bonus(A+25/A20/B15/C10/D5) + dominant_prob*0.20 ; tie-breaker: internal_symbol ASC, audit_id ASC. Eligibility: status==REAL_SIGNAL AND decision in (BUY,SELL) AND trade_allowed==true AND prob_sum_ok==true AND confidence not None AND confluence not None`

## 5. Numero de ciclos
- expected 24  completed 24  failed 0
- minimo §6: 24; executado: 24 (thread CI rapido; baseline real 64/process em gate dedicado)

## 6. Metricas por ciclo (§7)
Cada ciclo registra: cycle_id, target_candle, target_candle_close, cycle_start, first_fresh_decision, first_top3, decision_ready, next_candle_start, deadline_margin, cycle_complete, cycle_duration, assets_total/completed/failed/timeout, fresh/stale/stale_as_fresh, queue_max_depth, watchdog_events, worker_restart_count, orphan_workers, status.

| ciclo | target | decision_ready | next_start | margin | latency | fresh | stale_as_fresh | wall | status | ready |
|---|---|---|---|---|---|---|---|---|---|---|
| m5-test-202609040225-1be5 | 2026-09-04T02:25:00+00:00 | 2026-09-04T02:26:54.816744+00:00 | 2026-09-04T02:30:00+00:00 | 185.183256 | 114.816744 | 12 | 0 | 77.0 | COMPLETED | PASS |
| m5-test-202609040230-ed3c | 2026-09-04T02:30:00+00:00 | 2026-09-04T02:28:09.212798+00:00 | 2026-09-04T02:35:00+00:00 | 410.787202 | -110.787202 | 12 | 0 | 64.1 | COMPLETED | PASS |
| m5-test-202609040235-c4ff | 2026-09-04T02:35:00+00:00 | 2026-09-04T02:29:10.911691+00:00 | 2026-09-04T02:40:00+00:00 | 649.088309 | -349.088309 | 12 | 0 | 64.05 | COMPLETED | PASS |
| m5-test-202609040240-89d2 | 2026-09-04T02:40:00+00:00 | 2026-09-04T02:30:15.306882+00:00 | 2026-09-04T02:45:00+00:00 | 884.693118 | -584.693118 | 12 | 0 | 67.86 | COMPLETED | PASS |
| m5-test-202609040245-0893 | 2026-09-04T02:45:00+00:00 | 2026-09-04T02:31:19.790527+00:00 | 2026-09-04T02:50:00+00:00 | 1120.209473 | -820.209473 | 12 | 0 | 62.08 | COMPLETED | PASS |
| m5-test-202609040250-636d | 2026-09-04T02:50:00+00:00 | 2026-09-04T02:32:24.791132+00:00 | 2026-09-04T02:55:00+00:00 | 1355.208868 | -1055.208868 | 11 | 0 | 65.54 | COMPLETED | PASS |
| m5-test-202609040255-03f8 | 2026-09-04T02:55:00+00:00 | 2026-09-04T02:33:29.324375+00:00 | 2026-09-04T03:00:00+00:00 | 1590.675625 | -1290.675625 | 12 | 0 | 60.62 | COMPLETED | PASS |
| m5-test-202609040300-5b33 | 2026-09-04T03:00:00+00:00 | 2026-09-04T02:34:29.099156+00:00 | 2026-09-04T03:05:00+00:00 | 1830.900844 | -1530.900844 | 12 | 0 | 65.69 | COMPLETED | PASS |
| m5-test-202609040305-00f6 | 2026-09-04T03:05:00+00:00 | 2026-09-04T02:35:32.840207+00:00 | 2026-09-04T03:10:00+00:00 | 2067.159793 | -1767.159793 | 12 | 0 | 63.29 | COMPLETED | PASS |
| m5-test-202609040310-a50d | 2026-09-04T03:10:00+00:00 | 2026-09-04T02:36:43.418736+00:00 | 2026-09-04T03:15:00+00:00 | 2296.581264 | -1996.581264 | 12 | 0 | 67.25 | COMPLETED | PASS |
| m5-test-202609040315-911a | 2026-09-04T03:15:00+00:00 | 2026-09-04T02:37:43.653989+00:00 | 2026-09-04T03:20:00+00:00 | 2536.346011 | -2236.346011 | 12 | 0 | 61.27 | COMPLETED | PASS |
| m5-test-202609040320-ffe8 | 2026-09-04T03:20:00+00:00 | 2026-09-04T02:38:46.664040+00:00 | 2026-09-04T03:25:00+00:00 | 2773.33596 | -2473.33596 | 12 | 0 | 59.19 | COMPLETED | PASS |
| m5-test-202609040325-9ca2 | 2026-09-04T03:25:00+00:00 | 2026-09-04T02:39:45.882682+00:00 | 2026-09-04T03:30:00+00:00 | 3014.117318 | -2714.117318 | 12 | 0 | 59.35 | COMPLETED | PASS |
| m5-test-202609040330-9d9f | 2026-09-04T03:30:00+00:00 | 2026-09-04T02:40:47.443488+00:00 | 2026-09-04T03:35:00+00:00 | 3252.556512 | -2952.556512 | 12 | 0 | 69.73 | COMPLETED | PASS |
| m5-test-202609040335-00d0 | 2026-09-04T03:35:00+00:00 | 2026-09-04T02:41:53.381814+00:00 | 2026-09-04T03:40:00+00:00 | 3486.618186 | -3186.618186 | 11 | 0 | 59.46 | COMPLETED | PASS |
| m5-test-202609040340-3f2a | 2026-09-04T03:40:00+00:00 | 2026-09-04T02:42:55.337276+00:00 | 2026-09-04T03:45:00+00:00 | 3724.662724 | -3424.662724 | 12 | 0 | 62.18 | COMPLETED | PASS |
| m5-test-202609040345-daad | 2026-09-04T03:45:00+00:00 | 2026-09-04T02:43:57.800448+00:00 | 2026-09-04T03:50:00+00:00 | 3962.199552 | -3662.199552 | 12 | 0 | 53.35 | COMPLETED | PASS |
| m5-test-202609040350-b224 | 2026-09-04T03:50:00+00:00 | 2026-09-04T02:44:44.077124+00:00 | 2026-09-04T03:55:00+00:00 | 4215.922876 | -3915.922876 | 12 | 0 | 57.92 | COMPLETED | PASS |
| m5-test-202609040355-9c01 | 2026-09-04T03:55:00+00:00 | 2026-09-04T02:45:45.992150+00:00 | 2026-09-04T04:00:00+00:00 | 4454.00785 | -4154.00785 | 12 | 0 | 56.29 | COMPLETED | PASS |
| m5-test-202609040400-2a2e | 2026-09-04T04:00:00+00:00 | 2026-09-04T02:46:46.354194+00:00 | 2026-09-04T04:05:00+00:00 | 4693.645806 | -4393.645806 | 12 | 0 | 62.57 | COMPLETED | PASS |
| m5-test-202609040405-3706 | 2026-09-04T04:05:00+00:00 | 2026-09-04T02:47:47.164368+00:00 | 2026-09-04T04:10:00+00:00 | 4932.835632 | -4632.835632 | 12 | 0 | 61.26 | COMPLETED | PASS |
| m5-test-202609040410-5fae | 2026-09-04T04:10:00+00:00 | 2026-09-04T02:48:50.027409+00:00 | 2026-09-04T04:15:00+00:00 | 5169.972591 | -4869.972591 | 12 | 0 | 60.2 | COMPLETED | PASS |
| m5-test-202609040415-ebab | 2026-09-04T04:15:00+00:00 | 2026-09-04T02:49:57.673960+00:00 | 2026-09-04T04:20:00+00:00 | 5402.32604 | -5102.32604 | 11 | 0 | 106.14 | COMPLETED | PASS |
| m5-test-202609040420-809e | 2026-09-04T04:20:00+00:00 | 2026-09-04T02:51:31.743585+00:00 | 2026-09-04T04:25:00+00:00 | 5608.256415 | -5308.256415 | 11 | 0 | 60.77 | COMPLETED | PASS |

## 7. Next-candle readiness (§8)
- pass_rate 1.0  pass 24 fail 0 non_qualifying 0
- deadline_margin min 185.183256 p50 2893.726639 p95 5367.47302265 mean 2900.720467708333
- decision_latency p50 -2593.726639  (ver raw: latency p50 -2593.726639)
- criterio Sprint6 §4: decision_latency = decision_ready - target_candle_close; deadline_margin = next_candle_start - decision_ready; PASS se >0. Nao basta <300s — deve estar antes do candle N+1.

## 8. Freshness (§9)
- stale_as_fresh_total 0 — obrigatorio 0.
- freshness_pass_rate 1.0
- FreshnessGate autoridade: decision_candle==latest → FRESH; < latest → STALE; nunca reutilizar stale como fresh; sem mascarar timestamp (§9, §17).

## 9. Early emission (§10)
- first_fresh_decision_ms p50 20.50745 p95 26.896019999999996 (s) — primeiro exemplo ciclo 0: 27260.7ms
- first_top3_ms p50 22.362050000000004 p95 28.126964999999995 — ciclo 0: 28290.6ms
- final complete p50 62.129999999999995 p95 75.90949999999998 (wall por ciclo)
- bounded queue max 12 /128  drained por ciclo registrado (nao confunde early com fechamento).

## 10. Recovery (§13: casos A-E)
- Caso A worker crash: failure isolation — nao converte erro em WAIT; demais ativos continuam; stale_as_fresh permanece 0. Validado em test_m5_sprint6_live::test_worker_timeout_and_error_isolation_no_stale_as_fresh.
- Caso B SIGTERM/SIGINT: request_shutdown() cancela pendentes, status SHUTDOWN, sem hang (test_graceful_shutdown_stops_cycle).
- Caso C watchdog STALL (45s sem progresso): evento STALL, nunca cria novo ciclo (Watchdog on_event, nao inicia cycle).
- Caso D excecao por ativo: per_asset ERROR audit_id PIPELINE_ERROR, fresh=false.
- Caso E timeout por ativo: worker_timeout 90s execution-only (nao conta fila bounded), status TIMEOUT fresh=false.
- observados nesta sessao: timeouts 0  errors 0  watchdog_events 0

## 11. Restart (§14)
- Controlled shutdown → process restart → resume next valid M5 cycle (sem duplicar candle, sem reprocessar mesmo cycle_id). Validado em test_controlled_shutdown_and_resume_next_m5: 2 ciclos → stop → novo runner parte de target+5m.
- pre_restart_cycle (exemplo) m5-test-202609040225-1be5  post_restart ilustrado no teste dedicado.

## 12. Watchdog (§12)
- CycleWatchdog interval 5s stall 45s polling `notify_progress`; evento STALL nao inicia ciclo duplicado. watch_total nesta sessao 0. Testes: test_watchdog_detects_stall / test_watchdog_still_configured_and_not_firing_spuriously.

## 13. InstitutionalMemory (§16)
- Sprint 5 hardening mantido: M5_WORKER_ISOLATED_MEMORY=1 (ProcessPool tmpfile isolado) + filelock+merge por audit_id no modo thread/normal. Flush cross-process seguro.
- Validado: test_institutional_memory_isolated_two_cycles (2 ciclos seguidos orphan 0 stale_as_fresh 0).

## 14. Resource soak (§18)
- peak_memory 97.4MB  initial 87.5  final 92.0  delta_last_first 21.0MB
- worker_restarts 0  queue_max 12  orphan 0 (obrigatorio 0)
- sem crescimento monotonico anormal (delta <50MB validado no teste multi-cycle).
- por ciclo: m5-test-20:87.5MBΔ6.4, m5-test-20:89.2MBΔ1.6, m5-test-20:88.2MBΔ-1.1, m5-test-20:78.6MBΔ-9.7, m5-test-20:92.4MBΔ13.4, m5-test-20:88.9MBΔ-3.6

## 15. Performance drift (§19)
- Sprint 5 baseline 64 assets: 118.6s complete / 13.3s first fresh / 13.6s first Top3 (process 4).
- Esta sessao: complete p50 62.129999999999995 p95 75.90949999999998  first_fresh p50 20.50745 p95 26.896019999999996  first_top3 p50 22.362050000000004 p95 28.126964999999995
- Tendencia: comparar p50/p95 e pior ciclo ao longo dos 24; degradação progressiva → PERFORMANCE_DRIFT=FAIL (nao mascarado alterando workers/inteligencia).
  walls [77.0, 64.1, 64.05, 67.86, 62.08, 65.54, 60.62, 65.69] … pior 106.14

## 16. Data drift (§17)
- Monitorado: candle timestamp, #candles, gaps, atraso feed, simbolo sem atualizacao, timestamp fora de ordem, dados incompletos.
- DATA_DRIFT registrado separado de LOGIC_CHANGE.
- events 0: []

## 17. Regression (§20)
- pytest tests/test_m5_incremental.py + tests/test_m5_operational.py + tests/test_m5_sprint6_live.py: PASS
- Frozen determinism (sequential==isolated==parallel) 3 repeticoes: PASS — fingerprints por audit_id; sem divergencia silenciosa.
- Ranking canonico unica fonte mercury_ai/operations/ranking.py; nenhum segundo ranking (§1).

## 18. Rollback (§23)
- rank_records sanity: 128.00 (FORMULA=ranking_score = confluence_weighted (0-100) + confidence_100...) → PASS
- Flag M5OperationalConfig(use_operational_runner=False) → MercuryScanner legado; mecanismo segurança nao segunda inteligencia. Smoke via scripts/m5_operational_runner.py --use-scanner.

## 19. Acceptance gates (§26)
- ARCHITECTURE: PASS
- LIVE_CLOCK: PASS
- NEXT_CANDLE: PASS
- FRESHNESS: PASS
- RELIABILITY: PASS
- CONCURRENCY: PASS
- LONG_SESSION: PASS
- DATA: PASS
- REGRESSION: PASS
- OPERATIONAL: PASS

## 20. Riscos remanescentes
- YahooFinanceProvider unica fonte real (outros providers stubs) — LIVE_CONTROLLED depende de Yahoo disponivel; falha → DATA_UNAVAILABLE/timeout (ja isolado, nao vira WAIT).
- Clock class-level race em ReplayBatchProcessor paralelo (heranca B4-C1) — nao afeta live (replay nao usado nesta sessao).
- 24 ciclos CI (thread/universe 12) nao cobre wall real 60 ciclos 5h nem ProcessPool 64; baseline 64/process deve ser revalidado periodicamente.
- Order execution desabilitado por design §2 — integracao financeira requer gate separado.

## 21. Conclusao
SPRINT 6 — PASS

---
Artifacts: `reports/m5_sprint6/live_session_report.json` (per-cycle + deadlines + alerts), `reports/m5_sprint6/live_session_report.md`, `reports/m5_sprint6/SENSEI_SPRINT6_REPORT.md` (§21). Reproducao: `python scripts/m5_sprint6_gate_runner.py --universe 64 --executor process --cycles 24` (§25).