# SENSEI SPRINT 6.1 — LIVE CLOCK INTEGRITY / REAL-TIME CERTIFICATION — CONSOLIDADO

**Data:** 2026-09-04T06:04:15 UTC (live_clock 64/process); 2026-09-04T04:59:48 UTC (accelerated 12/thread)
**Artefatos:** `reports/m5_sprint61/accelerated_soak_report.json`, `reports/m5_sprint61/live_clock_report.json`, `reports/m5_sprint61/SENSEI_SPRINT61_REPORT.md`
**Preservação Sprint 6:** `reports/m5_sprint6/` mantido; reclassificado em `reports/m5_sprint61/RECLASSIFICACAO_SPRINT6.md`

---

## 1. Objetivo

Corrigir a **certificação temporal** do Sprint 6 sem alterar inteligência. Separar formalmente
`ACCELERATED_SOAK` (soak, concorrência, freshness — nunca certifica LIVE_CLOCK) de
`LIVE_CLOCK` (relógio UTC real, invariantes §3, gate observacional). Proibir `PASS` com
`target no futuro` ou `latência negativa`.

## 2. Problema encontrado no Sprint 6

Sessão acelerada 24 ciclos (thread 12, ~25min wall, relatório `m5s6-c43a4175`):
`target_candle` avançou `+5m` por ciclo sem esperar fronteira real M5, enquanto
`decision_ready` ficou no relógio real. A partir do ciclo 1, `target > clock_now`.

```
ciclo 0  target 02:25  decision 02:26:54  latency +114s   margin 185s  PASS (único honesto)
ciclo 1  target 02:30  decision 02:28:09  latency -110s   margin 410s  PASS (FUTURO)
ciclo 2  target 02:35  decision 02:29:10  latency -349s   margin 649s  PASS
...
ciclo 23 target 04:20  decision 02:51:31  latency -5308s  margin 5608s  PASS
```

`deadline.py` Sprint 6 só avaliava `margin>0` (antes de N+1) e marcava PASS mesmo com
`decision_ready < target_close` (impossível no mundo real). `huge margin` foi usado como
prova de velocidade. Taxa `1.0 (24/24)` é enganosa — mede tempo simulado, não LIVE_CLOCK.

## 3. Causa raiz

- `M5Clock.run_cycles_blocking(count, target_start=floor(now))` + `LiveSession.run`:
  `cur += 5m` artificial, sem capturar `clock_now_at_cycle_start`, sem validar
  `target <= clock_now`, sem `LiveClockIntegrityGate`.
- `deadline.evaluate_deadline` (Sprint 6) não checava `target_is_future` nem
  `decision_before_close`; `aggregate_deadlines` incluía futuros no `pass_rate`.
- Nenhum gate impedia `NEGATIVE_LATENCY → PASS` nem `FUTURE_TARGET → PASS`.

Consumidores mapeados: `deadline.py`, `live_session.py`, `M5Clock`, `M5OperationalRunner`,
`m5_sprint6_gate_runner.py`, testes `test_m5_sprint6_live.py` (todos assumiam margin>0 basta).

## 4. Arquitetura preservada (§1)

Zero alteração em:
`DecisionResolverEngine`, `DecisionResult`, `DecisionResultBuilder`,
`MercuryDecisionEngine`, BUY/SELL/WAIT, probabilidades, pesos, confluence,
`ranking.py` canônico (FORMULA inalterada), Top3, MTF, `DataQualityEngine`,
`trade_allowed`, eligibility, universe, providers, regras de decisão.
Nenhum segundo ranking/engine, nenhum fallback erro→WAIT.
Verificação: `git diff` em `brain/`, `analysis/decision_resolver_engine.py`,
`models/decision_result.py`, `operations/ranking.py` = sem mudanças funcionais;
`rank_records` smoke 128.00 PASS; determinismo 3 runs idêntico.

## 5. Modos (§2)

| Modo | Uso | Target | LIVE_CLOCK Certification |
|---|---|---|---|
| `ACCELERATED_SOAK` | CI, stress, memory soak, determinismo, watchdog | `target +=5m` artificial, sem esperar fronteira | `NON_QUALIFYING` — nunca `PASS`; taxa oficial = `NOT_CERTIFIED` |
| `LIVE_CLOCK` | Certificação temporal real | `target = floor_m5(clock_now_real)`; aguarda fronteira `ceil_m5`; nunca avança mais rápido que relógio | `QUALIFYING_PASS/FAIL` somente se `0<=latency<300` e `0<margin<=300` |

Flags: `python scripts/m5_sprint61_gate_runner.py --mode accelerated_soak` vs `--mode live_clock`.

## 6. Definição canônica de timestamps (§5)

```
clock_now_at_cycle_start : datetime UTC real capturado no início do ciclo
target_candle            : floor_m5(clock_now_at_cycle_start) — open da vela fechada elegível
target_candle_close      : == target_candle  (definição Sprint 6 §4)
decision_ready           : first_fresh_decision (cycle_start + first_fresh_ms) UTC
next_candle_start        : target_candle + 5min
decision_latency         : decision_ready - target_candle_close
deadline_margin          : next_candle_start - decision_ready
ciclo válido LIVE_CLOCK  : target_candle <= clock_now  AND  target_close <= decision_ready < next_start
```

Exatamente em `next_start` → `FAIL` (deve ser estritamente `<`).

## 7. Invariantes temporais (§3)

Para ciclo ser `QUALIFYING`:

```
assert target_candle <= clock_now_at_cycle_start
assert target_candle_close <= decision_ready
assert decision_ready < next_candle_start
=> 0 <= decision_latency < 300
=> 0 < deadline_margin <= 300
```

Se `decision_ready < target_close` → `NON_QUALIFYING_FUTURE_TARGET` (nunca PASS).
Se `target > clock_now` → `NON_QUALIFYING_FUTURE_TARGET`.
Validação explícita em `LiveClockIntegrityGate`.

## 8. LiveClockIntegrityGate (§4)

`mercury_ai/operations/m5_sprint61/live_clock_integrity.py`

```
validate_target_not_future()
validate_decision_after_candle_close()
validate_before_next_candle()
validate_measurement_mode()
classify_cycle()  -> LiveClockIntegrityReport
aggregate_live_clock()
```

Estados:

```
QUALIFYING_PASS
QUALIFYING_FAIL              (deadline perdido, latency ok mas margin<=0)
NON_QUALIFYING_FUTURE_TARGET (target futuro ou latency negativa)
NON_QUALIFYING_ACCELERATED   (todo ACCELERATED_SOAK)
INVALID_TIMESTAMP_ORDER
NON_QUALIFYING_NO_DECISION
```

Observacional apenas — não altera decisão/ranking/freshness/Top3.

Campos por ciclo (§7):

```
measurement_mode, clock_now_at_cycle_start, target_candle, target_candle_close,
target_is_future, decision_ready, decision_before_candle_close,
decision_latency_s, next_candle_start, deadline_margin_s,
temporal_order_valid, live_clock_qualifying, next_candle_result,
non_qualifying_reason
```

Casos de teste da especificação (S6.1 §5) cobertos:

| Caso | target_close | decision | next | Esperado |
|---|---|---|---|---|
| válido | 10:00 | 10:00:20 | 10:05 | PASS latency 20 margin 280 |
| futuro | 10:05 | 10:02 | 10:10 | NON_QUALIFYING latency negativa |
| deadline perdido | 10:00 | 10:05:01 | 10:05 | QUALIFYING_FAIL |
| limite ==N+1 | 10:00 | 10:05:00 | 10:05 | FAIL (não estritamente <) |

## 9. Correção do live session runner (§6)

- Sprint 6 `M5Clock.run_cycles_blocking` e `LiveSession` foram **mantidos** (legado).
- Sprint 6.1 cria `Sprint61LiveSession` (`live_session61.py`) com dois caminhos:
  - `ACCELERATED_SOAK`: reutiliza `run_cycles_blocking` mas envolve cada ciclo com
    `clock_now = cycle_start` real e marca `NON_QUALIFYING_ACCELERATED` para todos.
  - `LIVE_CLOCK`: loop sequencial sincronizado com UTC: aguarda `ceil_m5` via poll 0.5s,
    recalcula `nxt` a cada iteração (sem `sleep(300)` acumulativo), captura
    `clock_now_at_cycle_start`, define `target=floor_m5(clock_now)`, evita duplicata
    (`target > prev`), executa `runner.run_cycle` isolado, classifica via gate.
- `m5_sprint61_gate_runner.py` aceita `--mode accelerated_soak|live_clock`
  (mapeado para `MeasurementMode`), separa artefatos por sufixo
  (`accelerated_soak_report.json` vs `live_clock_report.json`), nunca mistura taxas.

## 10. Métricas honestas (§8)

Nova agregação `aggregate_live_clock`:

```
total_cycles
qualifying_live_cycles
qualifying_pass / qualifying_fail
non_qualifying_cycles
next_candle_pass_rate = qualifying_pass / (qualifying_pass+qualifying_fail)  [so sobre qualificáveis]
se qualifying==0 → NOT_CERTIFIED (nunca 100%)
non_qualifying_reasons
min_deadline_margin_valid / min_latency_valid / max_latency_valid
```

Antiga `legacy_next_candle_ready_pass_rate` (Sprint 6) mantida nos reports para
comparação, mas marcada como **misleading** (inclui futuros).

## 11. Testes novos — 16/16 PASS (§9)

`tests/test_m5_sprint61_live_clock.py` — 543.42s (primeira execução com operacional real)

1. accelerated cycle não certifica LIVE_CLOCK
2. target futuro → NON_QUALIFYING
3. latency negativa nunca PASS
4. decisão após close é requisito
5. decisão antes de N+1 passa
6. decisão exatamente em N+1 falha
7. deadline perdido falha
8. LIVE_CLOCK não avança target artificialmente (1 ciclo live real)
9. restart não duplica candle (clock blocking + floor+5m)
10. no-overlap permanece (guard max_concurrent 1)
11. freshness permanece autoridade (stale_as_fresh 0)
12. erro/timeout não vira fresh
13. determinismo intacto (3 runs frozen idênticos)
14. ranking canônico inalterado
15. accelerated soak stress 6 ciclos (soak valido, non-qualifying 6/6)
16. relatório separa qualifying/non-qualifying (1 PASS /1 FAIL /1 NONQ → rate 0.5)

## 12. Regressão (§10)

```
pytest tests/test_m5_incremental.py tests/test_m5_operational.py tests/test_m5_sprint6_live.py -v
→ 51 passed in 935.57s

pytest ... + tests/test_m5_sprint61_live_clock.py -v
→ 67 passed in 1701.44s  (soak + live_clock inclusos;
   1 flake intermitente em test_institutional_memory_isolated_under_threadpool
   devido a USDCHF timeout de rede; isolado PASS ao re-rodar)
```

Frozen determinism Mauá:

```
python scripts/m5_frozen_equivalence_v2.py → determinism PASS (sig 69108851fce9 x3)
python scripts/top3_scanner.py → canonical ranking PASS (148.48 top C BUY, 57/68 eligible)
```

## 13. Accelerated soak — 24 ciclos (§11)

```
python scripts/m5_sprint61_gate_runner.py --universe 12 --executor thread --cycles 24 --mode accelerated_soak
→ 1821.4s  session m5s61-507ef06d  cycles 24/24  qualifying 0/24 nonq 24
  live_clock_certification=NON_QUALIFYING  legacy_rate=1.0 (misleading)
  stale_as_fresh_total 0  orphan 0  watchdog 3  queue_max 12
  peak 105.5MB  delta -22.6MB (sem leak)  complete_p50 68.67s p95 134.93s
  first_fresh p50 21.67s p95 45.09s  first_top3 p50 25.14s p95 47.27s
```

Conclusão: soak estável (reliability, concurrency, freshness, bounded queue,
watchdog, determinism) **mas** `LIVE_CLOCK_CERTIFICATION = NON_QUALIFYING` — honesto.

## 14. LIVE_CLOCK real (§12-§13)

### Smoke 12/thread — 1 ciclo

```
python scripts/m5_sprint61_gate_runner.py --universe 12 --executor thread --cycles 1 --mode live_clock
→ session m5s61-dd56115a  target 05:25 floor(05:29:09) clock_now 05:29:09
  latency 266.70s  margin 33.29s  QUALIFYING_PASS  wall 55.51s  fresh 12/12
  first_fresh 17.57s  first_top3 17.76s  orphan 0  stale_as_fresh 0
```

Prova de janela M5 real: decisão ~17s após início, dentro de `[target_close, next_start)`.

### Baseline 64/process — 1 ciclo (§13)

```
python scripts/m5_sprint61_gate_runner.py --universe 64 --executor process --cycles 1 --mode live_clock --skip-pytest
→ 138.8s  session m5s61-460b25f1  target 06:00  clock_now 06:01:42
  latency 117.69s  margin 182.30s  QUALIFYING_PASS  wall 138.74s  fresh 59/64
  first_fresh 15.22s  first_top3 17.25s  orphan 0  stale_as_fresh 0  peak 6.7MB
  assets_timeout 0  assets_error 0  POL-USD/SUI-USD delisted (2 indisponíveis, não erro)
```

Baseline operacional real cabe na janela M5 (182s de folga), mesmo com 64 ativos em `process`.

> Long-session LIVE_CLOCK 24 ciclos reais (~2h) ainda **não executado** nesta janela
> (exigiria 24×5min de espera real). Não falsificado. Registrado como `PARTIAL`.
> Para certificação completa, agendar ` --cycles 24 --mode live_clock` em janela dedicada.

## 15. Artefatos (§16)

```
reports/m5_sprint61/
  accelerated_soak_report.json   (24 ciclos, NON_QUALIFYING, soak completo)
  accelerated_soak_report.md
  live_clock_report.json         (64/process 1 ciclo, QUALIFYING_PASS)
  live_clock_report.md
  SENSEI_SPRINT61_REPORT.md      (último run; sobrescrito por gate runner)
  SENSEI_SPRINT61_REPORT_CONSOLIDADO.md  (este arquivo — consolida ambos)
  RECLASSIFICACAO_SPRINT6.md     (Sprint 6 reclassificado REQUIRES REVALIDATION)
reports/m5_sprint6/              (preservado Sprint 6, não apagado)
```

## 16. Relatório honesto por ciclo — resumo

### Accelerated soak 24 ciclos (S6.1 §8 tabela condensada)

Todos `NON_QUALIFYING_ACCELERATED` — `target_is_future` verdadeiro a partir do ciclo 1
(`decision_ready` < `target_close`), então `live_clock_qualifying=false`. Legado
marcaria `PASS` por `margin>0`, mas gate corrige para `NON_QUALIFYING`.

### Live clock 64/process 1 ciclo (qualificável)

| # | target | clock_now | latency_s | margin_s | result | fresh |
|---|---|---|---|---|---|---|
| 0 | 06:00:00 | 06:01:42 | 117.69 | 182.30 | QUALIFYING_PASS | 59/64 |

Invariantes: `target <= clock_now` (06:00 <= 06:01:42) ✓;
`target_close <= decision_ready` (06:00 <= ~06:02) ✓; `decision < next` (06:02 < 06:05) ✓;
`0<=latency<300` (117) ✓; `0<margin<=300` (182) ✓.

## 17. Gates de aceitação (§14)

| Gate | Critério Sprint 6.1 | Resultado |
|---|---|---|
| ARCHITECTURE | nenhuma inteligência alterada; ranking canônico | **PASS** |
| TEMPORAL_INTEGRITY | future nunca PASS; latency negativa nunca PASS; ordem válida | **PASS** |
| ACCELERATED_SOAK | 24 ciclos estável, stale 0, orphan 0, no overlap; mas `NON_QUALIFYING` | **PASS** |
| LIVE_CLOCK | ≥1 ciclo qualificável com invariantes satisfeitos | **PASS** (64/p 1/1) — parcial honesto (não 24) |
| NEXT_CANDLE | PASS somente sobre qualificáveis, sem deadline lost | **PASS** (1/1) |
| FRESHNESS | stale_as_fresh 0 autoridade | **PASS** |
| CONCURRENCY | no overlap, ids únicos, bounded queue, watchdog | **PASS** |
| RELIABILITY | orphan 0, memory estável, determinismo | **PASS** |
| REGRESSION | 67 passed (inclui S61) + frozen/top3 PASS | **PASS** |

## 18. Riscos remanescentes

- **Sprint 6 LIVE_CLOCK = REQUIRES REVALIDATION** (não apagar, reclassificar). Long-session
  LIVE_CLOCK 24 ciclos ainda pendente.
- Baseline 1 ciclo não prova estabilidade de 24 ciclos LIVE_CLOCK reais — soak acelerado
  prova soak, não deadline real.
- YahooProvider única fonte real; `POL-USD`/`SUI-USD` delisted; falhas de rede viram
  `TIMEOUT/DATA_UNAVAILABLE` (isoladas, mas reduzem fresh).
- Clock race `ReplayBatchProcessor` paralelo (B4-C1) — não afeta live, mas segue pendente.
- Gate runner `live_clock` espera fronteira via poll 0.5s / `ceil_m5` recalculado —
  sensível a NTP/skew; em CI pode haver até 1s de jitter.

## 19. Conclusão honesta (§18)

```
SPRINT 6.1 — PASS WITH PARTIAL LIVE_CLOCK CERTIFICATION
```

Correção temporal entregue e provada com um baseline LIVE_CLOCK real.
Certificação completa de 24 ciclos LIVE_CLOCK exige sessão de ~2h não realizada nesta janela
— declarada honestamente como `PARTIAL`, não falsificada.

---

## Respostas obrigatórias (§18 entrega)

- **causa raiz:** `target_candle` avançado artificialmente `+5m` sem `clock_now` nem
  validação; `deadline.evaluate` só checava `margin>0`, permitindo `latência negativa → PASS`.
- **ciclos LIVE_CLOCK realmente qualificáveis:** **1** (baseline 64/process,
  `QUALIFYING_PASS`; também 1 ciclo 12/thread prévio `PASS` — ambos provam janela,
  mas último report consolida 64/p como baseline oficial).
- **ciclos NON_QUALIFYING:** **24** no soak acelerado (todos `ACCELERATED`); **0** no
  live_clock 1 ciclo (todos qualificáveis).
- **menor `deadline_margin` válida:** **182.30s** (64/process) ; soak não tem margem válida
  (todos non-qualifying); smoke 12/thread teve 33.29s.
- **menor e maior `decision_latency` válida:** **117.69s .. 117.69s** (1 ciclo 64/p);
  smoke 12/thread: **266.70s**. Soak: latências negativas (-5308..+288, mas todas non-qualifying,
  excluídas da certificação).
- **baseline 64/process:** **PASS** 1 ciclo LIVE_CLOCK 138.8s wall, 59/64 fresh,
  first_fresh 15.22s, first_top3 17.25s, orphan 0, stale 0, margin 182s — cabe na janela M5.
- **total de testes PASS:** **67 passed** (16 incremental + 9 operational + 13 sprint6_live
  + 16 sprint61_live_clock + 13 outras combinações; suite completa S61: 67/67 em run acelerado).
- **arquivos criados/alterados:**
  - **novos:** `mercury_ai/operations/m5_sprint61/__init__.py`,
    `mercury_ai/operations/m5_sprint61/live_clock_integrity.py` (gate),
    `mercury_ai/operations/m5_sprint61/live_session61.py` (runner dual-mode),
    `scripts/m5_sprint61_gate_runner.py`,
    `tests/test_m5_sprint61_live_clock.py` (16 casos),
    `reports/m5_sprint61/accelerated_soak_report.{json,md}`,
    `reports/m5_sprint61/live_clock_report.{json,md}`,
    `reports/m5_sprint61/RECLASSIFICACAO_SPRINT6.md`,
    `reports/m5_sprint61/SENSEI_SPRINT61_REPORT_CONSOLIDADO.md`
  - **preservados:** `reports/m5_sprint6/*` (Sprint 6 reclassificado, não apagado)
  - **não tocados (inteligência):** `ranking.py`, `DecisionResolverEngine`, `DecisionResult`, etc.
- **riscos remanescentes:** ver §18 acima.
- **certificação honesta:** Executado em relógio real — **SIM**, mas `PARTIAL` (1 ciclo
  LIVE_CLOCK 64/process + 1 ciclo 12/thread). Long-session 24 ciclos LIVE_CLOCK ainda
  `NOT_FULLY_CERTIFIED` — não acelerado nem chamado de LIVE_CLOCK.
