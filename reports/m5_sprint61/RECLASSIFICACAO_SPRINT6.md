# Reclassificação Sprint 6 — REQUIRES REVALIDATION

**Data:** 2026-09-04
**Motivo:** Sprint 6.1 identificou certificação LIVE_CLOCK enganosa.

## Preservação
Artefatos Sprint 6 em `reports/m5_sprint6/` são mantidos integralmente
(live_session_report.json, SENSEI_SPRINT6_REPORT.md, logs 24 ciclos).

## Reclassificação

| Aspecto | Sprint 6 Status Original | Reclassificação Sprint 6.1 |
|---|---|---|
| `LIVE_CLOCK` | PASS (100% next_candle_ready) | **REQUIRES REVALIDATION** |
| `NEXT_CANDLE_READY` | 100% PASS (24/24) | **NON_QUALIFYING** — medida sobre futuro |
| `OPERATIONAL HARDENING` | PASS | **PASS mantido** |
| `FRESHNESS` | PASS (stale_as_fresh 0) | **PASS mantido** |
| `CONCURRENCY` | PASS (no overlap, workers 4) | **PASS mantido** |
| `RECOVERY` | PASS | **PASS mantido** |
| `DETERMINISM` | PASS | **PASS mantido** |
| `REGRESSION` | PASS | **PASS mantido** |

## Causa (Sprint 6.1 §3)

Durante a sessão acelerada 24 ciclos (thread 12, ~25min wall), `target_candle`
avançou `+5m` por ciclo sem esperar fronteira real M5:

```
ciclo 0 target 02:25 decision 02:26:54  latency +114s PASS (único honesto)
ciclo 1 target 02:30 decision 02:28:09  latency -110s  margin 410s PASS (FUTURO)
ciclo 2 target 02:35 decision 02:29:10  latency -349s  margin 649s PASS (FUTURO)
...
ciclo23 target 04:20 decision 02:51:31  latency -5308s margin 5608s PASS (FUTURO)
```

`deadline.py:Sprint6` só checava `margin>0` (antes de N+1), sem validar
`target <= clock_now` nem `latency >=0`. Resultado: 23 ciclos com
`decision_ready < target_close` (impossível no relógio real) foram
contados como velocidade (`huge margin`). Taxa 100% não é prova LIVE_CLOCK.

## Correção Sprint 6.1

- Novos modos explícitos `ACCELERATED_SOAK` (Nunca certifica) vs `LIVE_CLOCK`
  (relogio real, invariantes §3, gate observacional).
- `LiveClockIntegrityGate` com estados
  QUALIFYING_PASS/FAIL vs NON_QUALIFYING_FUTURE_TARGET/ACCELERATED.
- Nova taxa: `qualifying_pass / (qualifying_pass+qualifying_fail)` — non-qualifying excluídos.
- Quando `qualifying==0` → `NOT_CERTIFIED` (nunca 100%).

## Próximos passos

- Sprint 6 permanece como prova de *operational hardening* acelerado.
- Certificação LIVE_CLOCK deve usar `scripts/m5_sprint61_gate_runner.py --mode live_clock`
  (aguarda fronteiras reais; 1 ciclo baseline 64/process já PASS — ver SENSEI 6.1).
- Long-session LIVE_CLOCK 24 ciclos reais (≈2h) ainda pendente para certificação completa;
  até lá, Sprint 6.1 = PASS WITH PARTIAL LIVE_CLOCK CERTIFICATION.
