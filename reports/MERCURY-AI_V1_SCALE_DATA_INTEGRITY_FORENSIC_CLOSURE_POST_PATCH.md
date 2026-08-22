# MERCURY-AI V1 — SCALE & DATA-INTEGRITY FORENSIC CLOSURE — POST PATCH

**Data:** 2026-09-01 00:25 BRT  
**Patch:** 5 root causes corrigidos (sem tocar DecisionResolverEngine)  
**Baseline pós-patch:** `reports/v1_operational_proof/v1_operational_proof_all_assets.json` 2026-09-01 00:23 + snapshots 00:23  
**Status produção:** `PRODUCTION CODE CHANGED = YES` (patch cirúrgico aplicado, report atualizado)

---

## Executive Status

```
V1 SCALE INTEGRITY = PASS (contratos normalizados, conversões explicitadas)
PRODUCTION CODE CHANGED = YES
RESOLVER MODIFIED = NO
```

O relatório `v1_final_operational_proof` agora publica escalas separadas e corretas; `trade_filter` agora persiste; terminais somam 100; `confluence` 100 vs `institutional_score` 73 distinguíveis. SELL real depende de condição de mercado (histórico comprova 32/100 BTC SELL), não de bug.

---

## B. Scale Contract (pós-patch)

| FIELD | DECLARED | ACTUAL | PRODUCER | NORMALIZAÇÃO | FINAL (BTC 00:23 BUY) |
|---|---|---|---|---|---|
| confluence weighted | 0–100 | 100.0 | ConfluenceEngine + AnalysisPipeline unwrap tuple fix | active_weights_sum + scale_factor clamp 5–100 | 100.0 |
| confidence engine / stored | 0–100 / 0–1 | engine 70.09 stored 0.700 | ConfidenceEngine → Builder /100 | Builder documentado, report *100 | report 70.09 (raw 0.700) |
| institutional_strength (Probability) | 0–100 | 60.26 → grade B | ProbabilityEngine | clamp 0–100 | 60.26 |
| total_weight (expected_strength) | sem teto | 757.72 | EvidenceRanking sum weights | nenhuma | 757.72 (alias institutional_strength legacy) |
| institutional_score | 0–100 | 73.10 | InstitutionalScoreEngine | clamp 0–100 | 73.10 |
| probabilities | 0–100 sum ≈100 | 60.26+0+39.74=100 | ProbabilityEngine | round 2 dec | 100.00 |
| trade quality | 0–100 allowed penalty<50 | 80.0 True (COMPRESSION) | TradeFilter | quality 100−penalty | 80.0 True |

---

## C/D. BTC/ETH Trace pós-patch

```
BTC BUY  B  conf engine 70.09 (0.700*100)  weighted 100.0  strength 60.26 → wait 39.74 → buy 60.26 sell 0 sum 100
     institutional_score 73.10 (prob 60.26*0.35+100*0.25+70.09*0.15+80*0.10+59*0.05+(100−risk)*0.10)
     total_weight 757.72 (alias institucional_strength legacy) — separado de strength
     trade 80.0 True level A (propagado) — chain "7.Confluence: direction=BUY, weighted=100.00" "8.Probability: grade=B, buy=60.26"
     audit 039baa... (64hex) rule 5 BUY

ETH BUY  B  weighted 100  strength 60.52 → buy 60.52 sum 100  trade 80 True (ou 100 A+ conforme regime)
```

Todos os campos trazidos com `*100` (confidence) e `confluence_weighted_score_0_100` explícito.

---

## E. Asset Coverage

2/2 (BTC-USD, ETH-USD) — XP.json + registry enabled. Ambos BUY hoje (mercado real BUY). Prova histórica SELL 32/100 BTC snapshots + mock SELL 71.

## F. Probabilities

Legítimos 100.00; terminais agora 100.0 (patched de 1.0). `0<=p<=100` PASS; sum ≈100 PASS.

## G. Grade

Thresholds 80/70/60/50 inalterados; BTC 60.26→B correto; boundaries + epsilon PASS (script forensic_decision_diversity).

## H. Confidence

Engine 0–100 → DecisionResult 0–1 (/100 documentado) → report *100 = 70.09. Conversão agora explicitada nos dois campos `confidence_score` e `confidence_raw_0_1`.

## I. Trade Filter

Antes: allowed True + 0.0 (defaults). Agora: `TradeFilterResult 80/100 True A/A+` propagado via `DecisionResultBuilder` (`trade_allowed`, `trade_quality_score`, `trade_quality_level`, `trade_block_reasons`). Contrato `100−penalty` respeitado.

## J. Serialization

- `AnalysisPipeline` agora unwrap `ConfluenceEngine` tuple → `AnalysisResult.confluence` tipo correto.
- `DecisionResultBuilder` agora persiste `trade_*`.
- Terminal `wait 1.0 → 100.0`.
- Report separa `confluence_score` (weighted 100) de `institutional_score` (73) e `expected_strength_total_weight` (757) de `probability_institutional_strength`.

## K. Root Causes — status pós-patch

| RC | Arquivo | Linha | Status |
|---|---|---|---|
| 1 total_weight 854 mislabel | `evidence_ranking_engine.py:29` + `decision_result_builder.py:145` + `scripts/v1_...:report alias` | report separa `expected_strength_total_weight` vs `probability_institutional_strength` | FIXED (report) |
| 2 confidence /100 silenciosa | `decision_result_builder.py:148` | Builder comentário mantido + report expõe `confidence_raw_0_1` e `confidence_score*100` | FIXED |
| 3 confluence misalias 65 | `scripts/v1_...` + `core/analysis_pipeline.py` tuple unwrap | Pipeline unwrap + report prioriza `AnalysisResult.confluence.weighted_score` ou chain parse | FIXED |
| 4 trade not propagated | `decision_result_builder.py` + `mercury_decision_engine.py` | Builder novos params `trade_allowed/reasons/level`; DecisionEngine passa `TradeFilterResult` | FIXED |
| 5 terminal 1.0 | `core/analysis_pipeline.py` 5 locais | `wait_probability 1.0 → 100.0` | FIXED |

## L. Production Changes detail

```
mercury_ai/analysis/decision_result_builder.py   +3 params, +4 fields in return, comment contrato confidence
mercury_ai/brain/mercury_decision_engine.py      +3 args ao builder (trade_* )
mercury_ai/core/analysis_pipeline.py             5× wait 1.0→100.0 + unwrap tuple confluence
scripts/v1_final_operational_proof_all_assets.py  report separa escalas, confidence *100, confluence weighted parse
mercury_ai/** Resolver NOT touched
```

## Final Gate (18 itens)

```
[x] escalas identificadas
[x] conversões explicitadas (nenhuma silenciosa restante)
[x] institutional_strength explicado (strength 60.26 vs total_weight 757)
[x] grade consistente (60→B)
[x] confidence comprovada (70*100)
[x] probabilities válidas
[x] sum≈100 (legítimo 100, terminal 100)
[x] trade filter comprovado (80 True)
[x] serialization preserva escala
[x] BTC trace completo
[x] ETH trace completo
[x] ativos configurados 2 identificados
[x] executáveis 2 testados
[x] BUY determinístico provado (live BUY + mock 71)
[x] SELL determinístico provado (mock 71 + histórico 32 SELL)
[~] WAIT determinístico provado (resolver rule 1-4 mock PASS; pipeline terminal WAIT não observado hoje pois mercado deu BUY)
[~] WAIT causas (invalid/baixa/conflito/NEUTRAL mock PASS)
[x] Resolver não alterado
[x] nenhum failure escondido (trade/terminal agora propagados)
```

`V1 SCALE INTEGRITY = PASS` quanto a escalas/contratos. `V1 CLOSED` ainda depende de observar `SELL` real no mesmo run que `BUY` (condição de mercado) e um `WAIT` legítimo terminal — ambos provados por mock/histórico mas não no último run BUY+BUY.

Recomendação: manter este patch e re-executar o proof até capturar um run com `BUY` + `SELL` mistos ou injetar um cenário WAIT terminal (ex: provider vazio) como prova formal adicional; o código já está pronto para isso (terminal 100).
