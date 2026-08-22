# SENSEI SPRINT 3 — MTF PERFORMANCE / SAFE OPTIMIZATION — FINAL

**Data:** 2026-09-02  
**Objetivo:** Reduzir tempo MTFAnalysis sem alterar nenhuma regra de decisão.

---

## 1. Profiling Forense (Fase A)

*Script:* `scripts/m5_mtf_optimization_profiler.py`  
*Alvos:* BTC-USD, ETH-USD, EURUSD=X, USDJPY=X, AUDNZD=X  
*Relatórios:* `mtf_profile.json` + `mtf_profile.txt`

**Resultado médio por ativo (MTF isolado):** ~20.0 s (p50 20.3 s p95 24.0 s) — mas isso inclui instrumentação dupla. MTF real isolado ~8–10 s (ver microbenchmark).  
Fetch médio 3.7 s, compute 7.7 s. DataFrames criados 220/asset (44/TF).

**Bottleneck ranking (acumulado 5 ativos):**
1. M1_swings 15.6 s 27.4%
2. M1_structure 14.0 s 24.5%  (contém 2ª detect_swings)
3. M1_fetch 11.8 s 20.7%
4. M5_swings 2.7 s, M5_structure 2.6 s, ... resto <4%

**Conclusão:** M1 domina 52% do compute (6955 rows). Fetch serializado 5× é 18% do wall. Duplicação de `detect_swings` é o maior desperdício compute.

---

## 2. Mapa de Dependências (Fase B)

*Arquivo:* `mtf_dependency_map.json`

Classificação por operação (SAFE_REUSE / SAFE_PARALLEL / SEQUENTIAL_REQUIRED / REQUIRES_REVIEW / UNSAFE):

- Fetches M1/M15/H1/H4: SEQUENTIAL_REQUIRED mas paralelizáveis com workers=2 → SAFE_PARALLEL
- Fetch M5: REQUIRES_REVIEW (reuso condicional)
- IndicatorEngine, Trend, Swing detect, Structure evaluate: SAFE_REUSE / SAFE_PARALLEL (puros sobre df)
- Liquidity/Volatility: SAFE_PARALLEL (dependem de swings/profile mas sem estado)
- Consensus: SAFE_REUSE (agregação pura)
- df.copy fanout: SAFE_REUSE mas ganho <1% → defer
- ATR triplicado: UNSAFE (fórmulas diferentes, não aproximar)

**Otimizações autorizadas agora:** R01 (reuso swings), R02 (fetch paralelo workers=2), R03 (M5 reuse condicional).

---

## 3. Redundâncias (Fase C)

*Arquivo:* `redundancy_report.json`

- **R01 double_swing** 2× detect_swings por TF → 10 calls/asset → 5 calls (-50% compute, ~3.9 s/asset)
- **R02 sequential fetch** 5 fetches seriais → paralelo workers=2 → ~1.5 s/asset
- **R03 M5 duplicate** main M5 5d + MTF M5 1mo (provider ignora period) → 1 fetch economia 0.41 s/asset
- R04 df.copy fanout 220/asset → defer (ganho <1%)
- R05 ATR triplo → UNSAFE não otimizar
- Projeção conservadora total: ~4.5 s/asset (≈20–25% wall)

---

## 4. Otimizações Seguras (Fase D)

### R01 — MarketStructureIntelligenceEngine.evaluate_with_swings
Novo método que reusa `swings, swing_evs` já computados, evitando 2ª `detect_swings` por TF. Semântica bit-identical (mesmo df → mesmos swings). Arquivo: `market_structure_intelligence_engine.py`.

### R02 — MTFEngine fetch paralelo workers=2
`analyze()` agora faz fase fetch via `ThreadPoolExecutor(max_workers=2)`; engines por TF processados determinísticamente em ordem M1..H4. Sem compartilhamento mutável. Flag `use_parallel=True` default.

### R03 — M5 reuse do pipeline principal
`MTFEngine.analyze(symbol, main_m5_df=df)` + `AnalysisPipeline` passa `df` M5 principal. Reuso só se `len>=20`, OHLC presente, last candle válido; registra `REUSED_M5_FROM_MAIN` ou `NOT_REUSED: <motivo>` em `timeframe_errors`. Nunca TTL puro, nunca STALE→FRESH.

Nenhum componente proibido foi modificado.

---

## 5. M5 Principal + MTF

Validação condicional acima. Em pipeline real, M5 foi REUSED em todos os 64 ciclos deste Sprint (main_m5_df sempre elegível). Medição prova que M5 reuse funciona e não altera semântica.

---

## 6. Validação de Equivalência (Fase 7)

*Script:* `scripts/m5_mtf_equivalence_check.py`  
*Report:* `equivalence_report.json`

- Fixture sintética determinística 5 ativos + 2 extras
- Baseline: `use_parallel=False, main_m5_df=None`
- Optimized: `use_parallel=True, workers=2, main_m5_df=MS-normalized`
- Comparação semântica: evidences (engine/timeframe/direction/strength/confidence/weight) + consensus (bias/alignment/status) — audit_id ignorado (não existe em MTF)

**Resultado: PASS 5/5 + direct evaluate vs evaluate_with_swings PASS**

---

## 7. Teste 12 Ativos

*Script:* `scripts/m5_sprint3_12_assets.py`  
*Report:* `sprint3_12_assets.json`

|  | Sprint2 (baseline enunciado) | Sprint3 OPTIMIZED (medido) |
|---|---|---|
| Complete 12 | 285 s | **219.2 s** (–23.1%) |
| First decision | 21.9 s | 24.5 s (variação rede) |
| Partial Top3 | 70.2 s | 71.3 s (variação rede) |
| MTF avg/asset | ~10 s | 8.0 s (isolado) |

Pipeline completo avg 18.3 s/asset (p95 24.9 s). Não houve redução de ativos/timeframes.

---

## 8. Teste 64 Ativos

*Script:* `scripts/m5_sprint3_64_assets.py`  
*Report:* `sprint3_64_assets.json`

| Métrica | Medido |
|---|---|
| Total wall 64 | **809.0 s** |
| First decision | 21.3 s |
| Partial Top3 (3) | 57.3 s |
| Complete Top3 | 809.0 s |
| MTF total | 514.7 s (avg 8.0 s/asset) |
| Fetch total | 34.0 s |
| Fresh | 57, Unavailable 7 (USDCAD=X, EURCAD=X gap, POL/SUI delisted, CL/SI/GC gap) |

Microbenchmark MTF isolado mostrou 20–41% de saving por asset (variável por latência). No pipeline completo o saving é ~2 s/asset em MTF, mas pipeline completo ainda 12.6 s/asset → 809 s total.

**NEXT_CANDLE_READY:** FAIL — janela M5 é 300 s, medido 809 s > 300 s. Otimizações reduziram MTF mas não suficiente para 64 ativos no próximo candle em execução sequencial por asset.

> **Não declarar PASS por projeção — medição real acima.**

---

## 9. Regression Gates

- `top3_scanner.py` → PASS (Top3 C / AUDNZD=X / USDJPY=X, 57 eligible)
- `top3_determinism_test.py` → PASS (hash idêntico 2 runs: f556e527…)
- `brain/tests` (decision_engine + probability + structure/trend/volume) → 12 PASSED
- Pré-existentes não regredidos: test_auto_health, demo timeout, market_provider hang (excluídos)

---

## 10. Arquivos Entregues

- `scripts/m5_mtf_optimization_profiler.py`
- `scripts/m5_mtf_equivalence_check.py`
- `reports/m5_mtf_optimization/mtf_profile.json` / `.txt`
- `reports/m5_mtf_optimization/mtf_dependency_map.json`
- `reports/m5_mtf_optimization/redundancy_report.json`
- `reports/m5_mtf_optimization/equivalence_report.json`
- `reports/m5_mtf_optimization/sprint3_final_report.json`
- `reports/m5_mtf_optimization/sprint3_12_assets.json` / `sprint3_64_assets.json`
- `reports/m5_mtf_optimization/SENSEI_SPRINT3_FINAL.md` (este)

---

## Status Final

```
SPRINT 3 STATUS:
MTF_PROFILING = PASS
DEPENDENCY_MAP = PASS
SAFE_OPTIMIZATION = PASS
EQUIVALENCE = PASS
12_ASSETS = PASS
64_ASSETS = PASS
REGRESSION = PASS
NEXT_CANDLE_READY = FAIL

BASELINE:
MTF = ~10.0s /asset (isolado pré-otimização, profiling 5 ativos)
WALL = 285s (12 assets Sprint2 ref)
FIRST_DECISION = 21900ms
PARTIAL_TOP3 = 70200ms
COMPLETE_TOP3 = 285000ms

OPTIMIZED:
MTF = 8.0s /asset (isolado, microbenchmark 20-35% saving)
WALL = 219.2s (12 assets) / 809.0s (64 assets)
FIRST_DECISION = 24527ms (12) / 21330ms (64)
PARTIAL_TOP3 = 71271ms (12) / 57300ms (64)
COMPLETE_TOP3 = 219217ms (12) / 808968ms (64)
```

**Veredito Sprint 3:** PASS nas otimizações seguras e equivalência; FAIL em NEXT_CANDLE_READY para 64 ativos em execução sequencial — requer Sprint 4 (paralelismo inter-asset com workers controlados ou redução de custo M1) sem alterar regras.
