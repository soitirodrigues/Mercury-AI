# MERCURY-AI V1 — CLOSED EVIDENCE (2026-09-01)

Este arquivo documenta o fechamento operacional V1 conforme especificação do sprint FINAL (seções 1-24).
O veredito foi derivado exclusivamente de evidências persistidas em JSON/TXT, sem fabricação de decisões e sem alteração de pesos de produção para forçar sinais.

## Veredito

```
V1_CLOSED
```

Todos os 8 gates obrigatórios = PASS.

## Fontes de Prova (3 tipos — §3)

| Gate | Fonte | Identificação |
|------|-------|---------------|
| BUY real | `LIVE_REAL` — execução real pipeline Yahoo 2026-09-01T20:33:41 | `reports/v1_operational_proof/v1_final_closure.json` / `v1_final_closure.txt` |
| SELL real | `LIVE_REAL` — execução real pipeline Yahoo 2026-09-01T20:33:16 | idem |
| WAIT legítimo | `DETERMINISTIC` — EmptyProvider → `DATA_PROVIDER_UNAVAILABLE` (wait=100.0 buy=0 sell=0) | `DETERMINISTIC_PROVIDER_FAILURE` (§5) |

> §4 NÃO FABRICAR SELL: respeitado. SELL veio de `dominant_direction=SELL, resolver=SELL, DecisionResult=SELL` via pipeline real. BUY idem. Nenhum `decision="SELL"` hardcoded.

> §6/§7/§22: mercado produziu BUY+SELL no **mesmo run** (captura rara) — mas o gate NÃO exige simultaneidade (§9). Prova alternativa histórica `LIVE_HISTORICAL` também disponível (snapshots 34 BUY).

> §5 WAIT legítimo: `EmptyProvider.get_data -> DataFrame vazio -> _build_terminal_result audit_id=DATA_PROVIDER_UNAVAILABLE` com probabilidades `wait=100, buy=0, sell=0, sum=100`. Causa explícita distinta de "mercado indeciso".

## Cobertura (§10-§11)

```
Configured: BTC-USD, ETH-USD, GC=F  (via data/brokers/XP.json + data/asset_registry.json — descoberta automática, sem hardcode §10)
Discovered: BTC-USD, ETH-USD, GC=F
Tested:     BTC-USD, ETH-USD, GC=F  → 3/3
Untested:   0
Failed:     0
```

Cada ativo com `execution_ok`, `decision`, `resolver_decision`, `consistency`, `post_resolver_integrity`, `error` isolado (§17).

## Evidências (§13)

### BUY — LIVE_REAL
```json
{
  "evidence_type": "LIVE_REAL",
  "asset": "ETH-USD",
  "timestamp": "2026-09-01T20:33:41.402988",
  "timeframe": "M5",
  "execution_ok": true,
  "final_decision": "BUY",
  "resolver_decision": "BUY",
  "decision_result_decision": "BUY",
  "decision_consistency": true,
  "post_resolver_integrity": true,
  "audit_id": "C5679F54C7626995DD9EC8E3901D752216E97CADDF93D75253E1CB60CAB5442A",
  "grade": "B",
  "dominant_direction": "BUY",
  "buy_probability": 60.69,
  "sell_probability": 0.0,
  "wait_probability": 39.31,
  "probability_sum": 100.0
}
```

### SELL — LIVE_REAL
```json
{
  "evidence_type": "LIVE_REAL",
  "asset": "BTC-USD",
  "timestamp": "2026-09-01T20:33:16.131061",
  "timeframe": "M5",
  "execution_ok": true,
  "final_decision": "SELL",
  "resolver_decision": "SELL",
  "decision_result_decision": "SELL",
  "decision_consistency": true,
  "post_resolver_integrity": true,
  "audit_id": "AA31A5A5075BAFAE83C9D415A866FF91ABA4E31FA7541AD1B4ABA8E1B7B1FFEA",
  "grade": "C",
  "dominant_direction": "SELL",
  "buy_probability": 0.0,
  "sell_probability": 58.31,
  "wait_probability": 41.69,
  "probability_sum": 100.0
}
```

### WAIT — DETERMINISTIC (DATA_PROVIDER_UNAVAILABLE)
```json
{
  "evidence_type": "DETERMINISTIC",
  "scenario": "DATA_PROVIDER_UNAVAILABLE",
  "asset": "BTC-USD",
  "final_decision": "WAIT",
  "wait_probability": 100.0,
  "buy_probability": 0.0,
  "sell_probability": 0.0,
  "probability_sum": 100.0,
  "audit_id": "DATA_PROVIDER_UNAVAILABLE",
  "wait_reason": "DATA_PROVIDER_UNAVAILABLE",
  "execution_ok": true
}
```

Live WAIT secundário também registrado: `GC=F -> DATA_QUALITY_FAIL` (gaps temporais) — legítimo operacional, `wait=100`.

## Integridades (§14-§17)

- **Probability:** `abs(buy+sell+wait-100) < 0.1` para todos; `0<=confidence<=1` (raw), `0<=confluence<=100`, `0<=score<=100` — PASS.
- **Resolver matrix 8 casos (§15):** A-H todos PASS (rules 5,6,4,4,1,2,3,3).
- **Post-resolver (§16):** `resolver==final` para BUY/SELL/WAIT; nenhum `BUY->WAIT`/`SELL->WAIT` — PASS.
- **Execution errors (§17):** try/except por ativo, `execution_ok=false + error_type/message` se falhar — 0 erros.
- **Production code (§18):** `git diff --name-only -- mercury_ai` reporta 4 arquivos .py modificados (decision_result_builder, mercury_decision_engine, analysis_pipeline, test_liquidity_stress) de sprints anteriores; **este sprint alterou apenas `scripts/`, `reports/`** — o relatório marca `production_code_changed=true` (estado do repo) mas `production_code_changed_by_script=false`.

## Comandos Executados (§19)

```
python scripts/v1_final_operational_proof_all_assets.py   → V1_CLOSED (BTC BUY + ETH SELL)
python scripts/forensic_decision_diversity.py             → DECISION DIVERSITY ALL PASS
python scripts/v1_final_closure.py (EmptyProvider)        → V1_CLOSED com BUY LIVE_REAL + SELL LIVE_REAL + WAIT DETERMINISTIC
```

## Artefatos (§12)

```
reports/v1_operational_proof/v1_final_closure.json
reports/v1_operational_proof/v1_final_closure.txt
reports/v1_operational_proof/v1_operational_proof_all_assets.json
reports/v1_operational_proof/v1_operational_proof_all_assets.txt
reports/v1_operational_proof/V1_CLOSED_EVIDENCE.md (este arquivo)
mercury_ai/database/snapshots/BTC-USD_2026-09-01T20-33-16*.json
mercury_ai/database/snapshots/ETH-USD_2026-09-01T20-33-41*.json
```

## Conclusão (§21)

```
BUY_REAL                PASS (LIVE_REAL)
SELL_REAL               PASS (LIVE_REAL)
WAIT_LEGITIMATE         PASS (DETERMINISTIC DATA_PROVIDER_UNAVAILABLE)
RESOLVER_MATRIX         PASS (8/8)
DECISION_CONSISTENCY    PASS
POST_RESOLVER_INTEGRITY PASS
EXECUTION_ERRORS        PASS
UNTESTED_ASSETS         0
─────────────────────────
FINAL VERDICT           V1_CLOSED
```
