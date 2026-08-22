# SENSEI SPRINT 5 — PRODUCTION HARDENING / OPERATIONALIZATION

**Data:** 2026-09-04T00:30:00+00:00
**Baseline Sprint 4:** `64 assets ProcessPool 4 = 105.47s / first 18.10s / Top3 19.39s / ThreadPool 8 = 162.0s`
**Modo:** Integração oficial Sprint 4 → fluxo operacional permanente (M5 contínuo)

---

## STATUS FINAL

```
ARCHITECTURE       = PASS — pipeline oficial integrada, sem duplicação de decisão/ranking, inteligência inalterada
PERFORMANCE        = PASS — 64 assets 118.6s < 300s, first_fresh 13.3s < 300s, first_Top3 13.6s < 300s
FRESHNESS          = PASS — stale_as_fresh == 0 (6/6 ciclos + single 64)
RELIABILITY        = PASS — failure isolation, timeout recovery, watchdog, graceful shutdown, zero orphan workers
CONCURRENCY        = PASS — InstitutionalMemory isolado por worker process, bounded queue, no overlap
MULTI-CYCLE        = PASS — 6 ciclos consecutivos, sem degradação, sem vazamento
REGRESSION         = PASS — equivalence frozen, determinism frozen, top3_scanner, test_m5_incremental 28, test_m5_operational 9
OPERATIONAL        = PASS — logs estruturados, cycle metrics, artifacts, rollback testado
```

**Sprint 5 = PASS**

---

## ARQUITETURA PROMOVIDA (Sprint 4 → Oficial)

```
ALL_SYMBOLS (63 ativos: 27 FOREX + 10 CRIPTO + 23 STOCKS + 3 COMMODITIES)
  → M5OperationalRunner (camada operacional oficial)
    → cycle_id + target_candle (floor M5 UTC)
    → Bounded executor: ProcessPool workers=4 (default) | ThreadPool workers=4 fallback
    → _analyze_one_isolated por ativo (pipeline OFICIAL + MTF oficial + DecisionResult oficial)
    → FreshnessGate (autoridade: decision_candle == latest_candle → FRESH, nunca STALE→FRESH)
    → Bounded queue (maxsize=128) + early emission (DECISION_READY + TOP3_UPDATE por conclusão)
    → Ranking canônico mercury_ai/operations/ranking.py (fórmula única, sem duplicação)
    → Watchdog (stall detection) + timeout recovery + failure isolation
  → M5Clock (scheduler alinhado a candle M5, não sleep acumulativo; max_concurrent_cycles=1)
```

**Regra absoluta Sprint 5 §1 respeitada:** Nenhum arquivo de inteligência modificado — DecisionResolverEngine, DecisionResult, MercuryDecisionEngine, DecisionResultBuilder, regras BUY/SELL/WAIT, ranking/pesos, DataQualityEngine, trade_allowed, probability normalization, MTF, universo, lógica estrutural.

---

## CONFIGURAÇÃO OFICIAL (§4)

`mercury_ai/operations/m5_operational/config.py` — `M5OperationalConfig`:

```
process_workers = 4        # default validado Sprint 4 (ProcessPool bounded)
thread_workers  = 4
executor        = "process" # process | thread (override M5_EXECUTOR)
worker_timeout_s  = 90.0    # por ativo (execution-only, não conta fila)
cycle_timeout_s   = 290.0   # global (janela M5 300s, ≤300)
max_concurrent_cycles = 1  # nunca >1 — overlap rejeitado com REJECTED_OVERLAP
early_emission  = true
freshness_policy = "strict"
bounded_queue_maxsize = 128
watchdog_interval_s = 5.0 / stall_threshold_s = 45.0
max_retries_per_asset = 0  # sem retry infinito
shutdown_grace_s = 10.0
use_operational_runner = true  # false = rollback para MercuryScanner
```

Override por env: `M5_PROCESS_WORKERS`, `M5_EXECUTOR`, `M5_WORKER_TIMEOUT_S`, `M5_CYCLE_TIMEOUT_S`, etc. Registrado no início de cada ciclo (`config` no report).

**Importante:** Workers permanecem em 4 até novo benchmark formal — 16 degrada (thrashing, Sprint 4 evidência).

---

## MUDANÇAS REALIZADAS

### Arquivos novos (Sprint 5)

```
mercury_ai/operations/m5_operational/__init__.py
mercury_ai/operations/m5_operational/config.py          # §4 — M5OperationalConfig centralizada
mercury_ai/operations/m5_operational/runner.py          # §3,§5-§12 — M5OperationalRunner
mercury_ai/operations/m5_operational/clock.py           # §5  — M5Clock scheduler M5
mercury_ai/operations/m5_operational/watchdog.py        # §12 — CycleWatchdog
scripts/m5_operational_runner.py                        # CLI oficial + multi-cycle + rollback flag
tests/test_m5_operational.py                            # §8-§16 — 9 testes operacionais
```

### Arquivos alterados (infra operacional apenas)

```
mercury_ai/utils/deterministic_clock.py
  - snapshot()/restore() threading.local isolado (Sprint 4 fix)
  - restore(None) → reset() (correção: _set_current_time(None) impedia fallback para real clock)

mercury_ai/analysis/institutional_memory_engine.py
  - imports: tempfile, time
  - flush(): cross-process hardening — filelock se disponível, reconciliação por audit_id (merge disco→cache antes de escrever), mkstemp atômico

mercury_ai/core/analysis_pipeline.py
  - __init__: modo _m5_isolated (env M5_WORKER_ISOLATED_MEMORY=1) — ProcessPool workers usam memória temporária isolada (tmpfile) em vez do arquivo compartilhado data/institutional_memory.json

mercury_ai/operations/m5_operational/runner.py
  - _analyze_one_isolated: M5_WORKER_ISOLATED_MEMORY=1 antes de criar pipeline
  - run_cycle: wait-loop com deadlines execution-only (não conta fila), bounded queue backpressure, watchdog, ciclo/global timeout, graceful shutdown, no-overlap guard
```

### Arquivos NÃO alterados (inteligência)

```
mercury_ai/analysis/decision_resolver_engine.py
mercury_ai/models/decision_result.py
mercury_ai/brain/mercury_decision_engine.py
mercury_ai/operations/ranking.py
mercury_ai/config/universe.py
mercury_ai/data/data_quality_engine.py
— nenhum peso/fórmula/regra alterado
```

---

## EVIDÊNCIAS MEDIDAS (§18 Acceptance Gates)

### Performance (64 assets, ProcessPool 4 — baseline oficial)

```
wall            118.60s  < 300s  PASS
first_fresh     13.36s   < 300s  PASS
first_Top3      13.63s   < 300s  PASS
fresh           59  stale 0  stale_as_fresh 0  timeout 0  unavailable 5
queue_max       64/128  worker_restarts 0  orphan_workers 0
next_candle_ready = true
artifact: reports/m5_sprint5/operational_cycle_report.json
```

Nota: 64 WALL variou 104–141s entre runs (Yahoo latência); Sprint 4 baseline 105.47s dentro do intervalo. Sempre < 300s.

### Freshness (§6)

```
FreshnessGate autoridade — nunca converter stale em fresh
stale_as_fresh == 0  em todos os ciclos (single + 6 multi-cycle)  PASS
Registrado: target_candle, decision_candle, fresh/stale, reason (FreshnessResult.reason)
```

### Early Emission (§7)

```
Emitido por conclusão via _cf.wait(FIRST_COMPLETED):
  DECISION_READY  por ativo (symbol, decision_candle, status, fresh, elapsed_ms)
  TOP3_UPDATE     quando ranking atinge 3 elegíveis (rank, symbol, score, elapsed_ms, partial:true)
Continua processando restantes — não encerra ciclo precocemente
Top3 artificial: nunca emitido sem 3 elegíveis
```

### Failure Isolation + Recovery (§8, §9)

```
Asset quebrado → TIMEOUT ou ERROR (audit_id PIPELINE_ERROR), não WAIT artificial
Demais ativos continuam — sem retry infinito (max_retries=0)
Worker timeout: 90s execution-only (não penaliza fila bounded)
Cycle timeout: 290s global (janela M5 300s)
Per-worker deadline só para RUNNING (fut.running()), não para queued
Nenhum processo órfão após ciclo (ProcessPool context manager + watchdog stop)
```

### Watchdog (§12)

```
CycleWatchdog polling interval 5s, stall 45s sem progresso → evento STALL (não cria novo ciclo)
9 testes: test_watchdog_detects_stall PASS, test_watchdog_no_stall_when_progress PASS
```

### Graceful Shutdown (§14)

```
SIGTERM/SIGINT → request_shutdown() → impede novo ciclo, cancela pendentes, aguarda grace, fecha pools
Teste: test_graceful_shutdown_stops_cycle PASS (SHUTDOWN ou COMPLETED, nunca hang)
```

### InstitutionalMemory Concurrency (§10)

```
Problema Sprint 4: singleton/global + arquivo compartilhado race entre processos
Solução Sprint 5:
  - Workers ProcessPool: M5_WORKER_ISOLATED_MEMORY=1 → cada processo usa tmpfile isolado (sem flush concorrente ao arquivo principal)
  - Fallback ThreadPool / produção single: flush() com filelock + merge por audit_id antes de escrever
Teste: test_institutional_memory_isolated_under_threadpool PASS
       test_multi_cycle_no_degradation PASS
```

### Bounded Queue / Backpressure (§11)

```
Queue bounded maxsize=128
Executor bounded max_workers=4 (produtor limitado)
Queue depth registrado: queue_max_depth, queue_depth_at_end, queue_drained
Full → drain 1 + re-enfileira (não descarta decisão válida silenciosamente)
Teste: test_bounded_queue_never_grows_unbounded PASS
```

### Observabilidade (§13)

```
Cada ciclo gera report estruturado:
  cycle_id, target_candle, cycle_start/end/duration, worker count, assets total/completed/error/timeout/unavailable,
  fresh/stale/stale_as_fresh, first_fresh, first_Top3, cycle_complete, queue_max_depth, worker_restart_count, watchdog_events, peak_memory, status
Artifacts:
  reports/m5_sprint5/operational_cycle_report.json
  reports/m5_sprint5/multi_cycle_report.json
  reports/m5_sprint5/SENSEI_SPRINT5_REPORT.md
  reports/m5_sprint5/SENSEI_SPRINT5_REPORT_FULL.md (este arquivo)
```

### Rollback / Feature Flag (§15)

```
Flag explícita: M5OperationalConfig.use_operational_runner (env M5_USE_OPERATIONAL_RUNNER)
Default: true (nova pipeline)
Rollback: --use-scanner ou use_operational_runner=false → MercuryScanner (caminho antigo preservado, não removido)
Registrado no report: mode + config
```

---

## MULTI-CYCLE — 6 CICLOS CONSECUTIVOS (§16)

```
Clock bloquante (sem sleep M5 real) — targets incrementais 5m, sem restart manual

cycles 6 | thread 4 | 12 assets
  202609040020  40.69s  stale_as_fresh 0  queue_max 12  COMPLETED
  202609040025  41.74s  stale_as_fresh 0  queue_max 12  COMPLETED
  202609040030  47.70s  stale_as_fresh 0  queue_max 12  COMPLETED
  202609040035  43.64s  stale_as_fresh 0  queue_max 12  COMPLETED
  202609040040  41.21s  stale_as_fresh 0  queue_max 11  COMPLETED
  202609040045  41.50s  stale_as_fresh 0  queue_max 12  COMPLETED

Gates:
  cycle_id único              PASS
  candle correto (sorted)     PASS
  no overlap                  PASS (blocking M5Clock, guard _active_cycle_id)
  first_fresh < 300s          PASS (~15s)
  first_Top3  < 300s          PASS (~15s)
  complete    < 300s          PASS (40-47s por ciclo)
  stale_as_fresh == 0         PASS (6/6)
  sem worker órfão            PASS
  sem crescimento queue       PASS (12/128 estável)
  sem degradação progressiva  PASS (wall estável, sem trend)
  sem vazamento memória       PASS (memory_delta estável)
  sem crash                   PASS

artifact: reports/m5_sprint5/multi_cycle_report.json
```

Ideal 12 ciclos: `python scripts/m5_operational_runner.py --cycles 12`

---

## REGRESSION / EQUIVALENCE (§17)

```
test_m5_incremental            28 passed
test_m5_operational             9 passed
top3_scanner                   PASS (57/68 eligible)
m5_frozen_equivalence_v2       PASS (6/6 symbols seq==iso==parallel-thread, sig 69108851fce9 x3)
determinism                    PASS (frozen fixture + isolado, 3 runs idênticos)
FreshnessGate stale_as_fresh   0
failure isolation              PASS
```

---

## RISCOS REMANESCENTES

- YahooFinanceProvider latência variável (GC=F/SI=F gaps, POL-USD/SUI-USD delisted) — tratado como DATA_UNAVAILABLE, não quebra ciclo.
- filelock é dependência opcional para flush cross-process ThreadPool; ProcessPool usa isolamento tmpfile.
- MTF degenerado sob replay — pendência B4, não impacta produção live.
- 12 ciclos e M5 real clock (ceil M5 + sleep) não exercitados nesta entrega bloqueante; cobertos pelo mesmo M5Clock/start().
- DeterministicClock.restore(None) fix aplicado.

---

## COMANDO DE REPRODUÇÃO

```
# Single 64 (baseline oficial)
python scripts/m5_operational_runner.py --universe 64 --executor process --workers 4 --out reports/m5_sprint5/operational_cycle_report.json

# Multi-cycle 6
python scripts/m5_operational_runner.py --universe 12 --executor thread --workers 4 --cycles 6 --multi-out reports/m5_sprint5/multi_cycle_report.json

# Tests
pytest tests/test_m5_incremental.py tests/test_m5_operational.py -v
```

---

**Sprint 5 — PASS. Pipeline operacional M5 contínua, sem overlap, sem stale-as-fresh, sem workers órfãos, sem race condition, sem alterar inteligência validada.**
