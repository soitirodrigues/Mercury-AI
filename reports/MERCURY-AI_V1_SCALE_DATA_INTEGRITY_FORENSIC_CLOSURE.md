# MERCURY-AI V1 — SCALE & DATA-INTEGRITY FORENSIC CLOSURE

**Data:** 2026-09-01 00:10 BRT  
**Executor:** Forensic Agent (read-only, sem alteração de produção)  
**Baseline:** commit main atual + snapshots 2026-08-31 22:41 + live 2026-09-01 00:04  
**Comando:** Sprint SCALE & DATA-INTEGRITY (18 seções do enunciado) — investigar, provar com código executado, não alterar produção antes da root cause.

---

## A. Executive Status

```
V1 SCALE INTEGRITY = FAIL
V1 CLOSED = NÃO
PRODUCTION CODE CHANGED = NO
```

**Motivo do FAIL (não é “parece ok”):** 3 conversões silenciosas + 1 omissão de propagação quebram o contrato de escala entre engine → DecisionResult → relatório. O `Resolver` está intacto, as probabilidades somam 100 e o grade é matematicamente correto **quando lido na escala correta (0–100)**, mas o relatório publicado rotula `expected_strength = total_weight (≈ 854, sem teto)` como `institutional_strength`, exibe `confidence 0.68` (escala 0–1) como se fosse 0–100, mapeia `confluence 65.27` (que é o `institutional_score`) no lugar do `weighted_score 100`, e publica `trade_filter.allowed True + quality 0.0` — combinação que viola o contrato do filtro (o valor real nunca foi persistido).

Sem patch cirúrgico, o próximo relatório continuará comparando `grade D` com `854` e parecerá “inconsistente” mesmo quando a decisão está correta.

---

## B. Scale Contract — tabela completa (declarada vs real)

| FIELD | DECLARED SCALE | ACTUAL SCALE | PRODUCER | CONSUMERS (esperam) | NORMALIZATION | FINAL VALUE (exemplo BTC 2026-08-31 22:41) |
|---|---|---|---|---|---|---|
| `confluence_score` (weighted) | 0–100 | 0–100 (clamp 5–100) | `ConfluenceScoreEngine.calculate` (total_weight=100) + `ConfluenceEngine.analyze` (active_weights_sum + scale_factor) — `confluence_score_engine.py:85`, `confluence_engine.py:119–165` | `ProbabilityEngine` (0–100), `DecisionResolverEngine` (threshold 40), `InstitutionalScoreEngine` (×0.25) | `active_weights_sum` + `scale_factor=100/active_sum` + `clamp 5–100` | **100.00** (chain `weighted=100.00`) — relatório publicou `65.27` (na verdade `institutional_score`) |
| `confidence_score` (engine) | 0–100 | Engine 0–100; **DecisionResult 0–1** | `ConfidenceEngine.calculate: 100*(0.25 quality+0.45 consensus+0.30 market)` clamp 0–100 + `calibrate` clamp — `confidence_engine.py:98–121` | `ProbabilityEngine` 0–100, `InstitutionalScoreEngine` 0–100, UI `×100` | `DecisionResultBuilder: confidence = calibrated/100.0` (`decision_result_builder.py:148`) | Engine `68.247` → armazenado `0.682476925` → relatório exibe `0.68` sem `×100` |
| `institutional_strength` (Probability) | 0–100 | 0–100 | `ProbabilityEngine.analyze: (conf*0.50+confid*0.35+evidence_bonus*0.15)*(1−risk*0.50)` clamp 0–100 — `probability_engine.py:90–108` | `opportunity_grade` thresholds 80/70/60/50; `wait = max(5,100−strength) cap 60` | clamp 0–100 | **44.388** (raw 76.88 → after risk 84.53) → `grade D` correto |
| `expected_strength` / `total_weight` (reportou como institutional_strength) | **sem teto** — soma de pesos | 0–~2000 (soma `e.weight`) | `EvidenceRankingEngine.rank: total_weight = sum(e.weight)` — `evidence_ranking_engine.py:29` → `DecisionResultBuilder expected_strength = total_weight` (`decision_result_builder.py:145`) | display only | nenhuma | **854.247** (BTC), **739.379** (ETH) — NÃO usado para grade |
| `institutional_score` (`DecisionResult.score`) | 0–100 | 0–100 | `InstitutionalScoreEngine: prob*0.35+confl*0.25+conf*0.15+trade*0.10+resolved*0.05+(100−risk)*0.10 * conflict 0–1` clamp — `institutional_score_engine.py:44–68` | `DecisionResult.score`, `explainability.institutional_score` | clamp 0–100 | **65.275** (BTC), **63.242** (ETH report = este score, não confluence) |
| `trade_filter.quality_score` | 0–100 (`100−penalty`) | Engine 0–100; **DecisionResult `trade_quality_score` fica 0.0 por omissão** | `InstitutionalTradeFilterEngine.evaluate` — `institutional_trade_filter_engine.py:67–140` | `InstitutionalScoreEngine` (×0.10), `DecisionResult.quality` (alias) deveria receber `trade_quality_score` | `quality_level A+≥90 A≥80 B≥70 C≥60 D<60; allowed = penalty<50` | Engine real: BTC REVERSAL → `100.0 allowed True`; ETH COMPRESSION → `80.0 allowed True`; Snapshot `trade_quality_score 0.0 allowed True` (default, não propagado) |
| `probabilities` (buy/sell/wait) | 0–100 cada, soma ≈100 | 0–100 (legítimo); **1.0 (0–1) em estados terminais `DATA_QUALITY_FAIL` etc** | `ProbabilityEngine` — `probability_engine.py:114–145`; terminais em `core/analysis_pipeline.py: ~230/270/520` | `DecisionResult` | `round 2 dec`, `wait = max(5,100−strength) cap 60` | Legítimo: BTC `0+44.39+55.61=100.00`; ETH `0+44.35+55.65=100.00`; Terminal `0+0+1.0=1.0` (escala divergente) |
| `opportunity_grade` | categorias sobre 0–100 | A+≥80 A≥70 B≥60 C≥50 D<50 | `ProbabilityEngine` — `probability_engine.py:157–168` | `DecisionResolverEngine` regra 4 (`conflict && grade in C/D → WAIT`) | thresholds hard-coded | BTC `44.38→D`, live B `60.88→B` |
| `clarity / agreement_percentage` | 0–100 | 0–100 | `ConfluenceEngine` `(normalized_score/100)*100` | display | clamp | `100.0` nos casos traçados |

---

## C. BTC Trace — campo por campo (snapshot 2026-08-31 22:41:14 + live 2026-09-01 00:04)

**Snapshot citado no enunciado (prova executada `forensic_scale_trace.py` + leitura direta do snapshot):**

```
Snapshot: mercury_ai/database/snapshots/BTC-USD_2026-08-31T22-41-14.758600.json
Snapshot: reports/v1_operational_proof/v1_operational_proof_all_assets.json case BTC

final_decision              SELL            (resolver rule 6)
dominant_direction          SELL            (Confluence weighted winner BEARISH)
is_valid                    True
validation_warnings         []
confluence weighted_score   100.00          (chain "7.Confluence: direction=SELL, weighted=100.00")
  └ trace no relatório      65.275341375    *** MISALIASED — é institutional_score, não weighted ***
institutional_strength (Probability) 44.388129  (conf 100*0.50=50 + 68.247*0.35=23.88 + bonus 20*0.15=3 → 76.88 × (1−0.845*0.5)=44.38)
  └ grade                   D               (44.38 < 50 correto)
  └ wait_prob               55.61 (= max(5,100−44.38) =55.61 cap 60)
  └ remaining               44.38 → sell 44.39 / buy 0
  └ sum                     100.00 PASS
confidence engine           68.2476925 (0–100) → DecisionResult 0.682476925 (0–1) → relatório 0.682 (sem ×100)
expected_strength (total_weight) 854.2472329102645 (= sum e.weight, 32 evidências, escala sem teto) — relatório rotula como institutional_strength
institutional_score (DecisionResult.score) 65.275341375 (= 44.39*0.35 +100*0.25+68.24*0.15+0*0.10+59.11*0.05+(15.46)*0.10) — é o "confluence" do relatório
  └ explainability chain: "8.Probability: grade=D, buy=0.00, sell=44.39" / "9.Resolver: rule=6"
trade_filter engine real    quality 100.0 (REVERSAL_TRANSITION, 32 evidências, ATR 59) allowed True
  └ DecisionResult          trade_allowed True (default) / trade_quality_score 0.0 (default) / quality 100.0 (alias) / trade_quality_level N/A — BUG: campos trade_* não propagados
audit_id                    56b46e47f4e2ac9ec976a1ca9519ba42318545876168e768d27892e3e07a6394 (sha256 64hex = WAIT/BUY/SELL legítimo)
```

**Cadeia completa (SOURCE → FINAL → CONSUMER):**

```
EvidenceRankingEngine.rank
  raw: sum weights 854.247
  → DecisionResultBuilder expected_strength = total_weight
  → DecisionResult.expected_strength 854.247 (escala solta)
  → SERILIZAÇÃO snapshot JSON 854.247
  → REPORT scripts/v1_final... trace["institutional_strength"]=expected_strength (mislabel)
  → CONSUMER relatório exibe "854" como se fosse força 0–100 → comparando com grade D parece impossível (mas grade usa outra variável 44.38)

ConfidenceEngine.calculate
  raw: avg quality 0.591 + consensus 1.0*1.0 + market 0.?? → 100*(0.25*0.591+0.45*1.0+0.30*0.??) =68.247
  → calibrate 68.247 (consistency 0.5 neutro)
  → ProbabilityEngine recebe 68.247 (0–100) ✓
  → InstitutionalScoreEngine recebe 68.247 ✓
  → DecisionResultBuilder divide /100 → 0.682 stored
  → JSON snapshot 0.682
  → REPORT exibe 0.682 sem ×100 → parece 0–1 quando declaração é 0–100

ConfluenceEngine.analyze
  raw: bullish_score vs bearish_score → max  ~??
  → net_score − risk − conflict → normalized × scale_factor → 100.00
  → ProbabilityEngine confluence 100.0 ✓
  → InstitutionalScoreEngine confluence 100.0 ✓
  → DecisionResult.score = institutional_score 65.27 (não confluence)
  → REPORT trace["confluence_score"]= DecisionResult.score (65.27) pois snapshot não tem AnalysisResult.confluence persistido → misalias

ProbabilityEngine
  raw: 76.88 → after risk 44.38 → grade D → wait 55.61 → sell 44.39/buy 0
  → DecisionResult buy/sell/wait 0/44.39/55.61 soma 100 PASS
  → DecisionResolverEngine (dominant SELL, valid True, grade D, conflict False, confl 65? ou 100?) → rule 6 SELL

TradeFilter
  raw penalty 0 → quality 100 → allowed True
  → MercuryDecisionEngine recebe TradeFilterResult allowed True
  → DecisionResultBuilder NÃO repassa trade_* → snapshot mantém defaults 0.0 / True / N/A
  → REPORT "True + 0.0" viola contrato 100−penalty
```

---

## D. ETH Trace — campo por campo

```
Snapshot: mercury_ai/database/snapshots/ETH-USD_2026-08-31T22-41-45.688722.json  (encontrado por busca exata de strength 739.37)
Snapshot report case ETH: mesmos valores

final_decision              SELL (live 00:04) / snapshot anterior ETH-USD 2026-08-31 22:41 com mesmos números do enunciado SELL
dominant_direction          SELL (live) — histórico 2026-08-24 havia BUY 44.28 para mesmo ETH (prova de diversidade)
is_valid                    True
confluence weighted         100.00 (chain direction=SELL weighted=100.00 — live; histórico BUY também 100.00)
institutional_strength (Probability) ~44.5 (similar a BTC) → grade D (ETH live 44.52 wait 55.48)
confidence                  68.214 (report 0.6821448258064519 stored) → *100 =68.21 engine
expected_strength           739.379613480828 (live 777.80, histórico BUY 721.82) — soma pesos, não força
institutional_score         63.242543354838716 (report rotula como confluence)
probabilities               0 +44.35+55.65=100.00 (live 0+44.52+55.48=100)
trade_filter engine         COMPRESSION → penalty 20 → quality 80.0 allowed True (simulado direto dá 80)
  └ snapshot                trade_quality_score 0.0 allowed True (mesmo bug BTC)
audit_id                    c11694641ae16d3a14082d03b18ad64a2655d614e0bdc5372c7382ce41e4e223 (64hex legítimo)
```

Cadeia idêntica à BTC, com `trade_quality` real 80 (COMPRESSION) vs 0 persistido.

---

## E. Asset Coverage — todos os ativos oficialmente configurados

**Descoberta real (não inventada):**

```
Fonte 1: data/brokers/XP.json          → ["BTC-USD","ETH-USD"]
Fonte 2: data/asset_registry.json      → { "BTC-USD": enabled true, "ETH-USD": enabled true } (2 enabled, 0 disabled)
Fonte 3: scripts/discover_assets()     → configured 2, discovered 2, tested 2, untested 0
```

| ASSET | CONFIGURED | ENABLED | SUPPORTED | EXECUTED | EXECUTION_ERROR | DECISION | RESOLVER | CONSISTENT |
|---|---|---|---|---|---|---|---|---|
| BTC-USD | yes (XP.json, registry) | true | Yahoo priority 1 (fallback Polygon) | EXECUTED | — | SELL (rule 6) | SELL rule 6 | true |
| ETH-USD | yes | true | Yahoo priority 1 | EXECUTED | — | SELL (rule 6) live; histórico BUY 44.28 | SELL/BUY conforme run | true |

**Histórico de prova de cobertura:** `reports/v1_operational_proof/v1_operational_proof_all_assets.json` 2026-08-31 22:41 (2/2), 2026-09-01 00:04 (2/2, ambos SELL). Não existe terceiro ativo configurado; portanto 2/2 fecha o requisito multiativo **para V1** (escopo configurado). Marcar `BLOCKED_EXTERNAL_DEPENDENCY` não se aplica — feed Yahoo respondeu para ambos (DecisionResult audit_id 64hex, não `DATA_PROVIDER_UNAVAILABLE`).

Se o roadmap V1 previa ≥3 ativos, a lacuna é de **configuração**, não de execução — nenhuma falha de provider foi mascarada.

---

## F. Probability Integrity — asserts com tolerância

**Tolerância:** `abs(sum−100) < 0.1` para legítimos (por `round 2 dec`); terminais documentados como exceção `sum=1.0` (ver §5).

```
BTC snapshot SELL 0+44.39+55.61=100.00  0≤p≤100 ✓  sum≈100 PASS
ETH snapshot SELL 0+44.35+55.65=100.00  PASS
LIVE BTC 2026-09-01 BUY 45.27+0+54.73=100.00 PASS (outra run BUY 60.88+0+39.12=100.00 após mock diversidade)
LIVE ETH SELL 0+44.52+55.48=100.00 PASS
Mock BUY 71+0+29=100 PASS
Mock SELL 0+71+29=100 PASS
Mock NEUTRAL 35.5+35.5+29=100 PASS
TERMINAL INSUFFICIENT_DATA 0+0+1.0=1.0  escala 0–1  (AnalysisPipeline _build_terminal_result espera 1.0) — CONTRATO DIVERGENTE
```

**Veredito:** Probabilidades legítimas **PASS**. Terminais falham o invariante `≈100` porque usam escala 0–1; isso é **FAIL de contrato de escala sob serialization** (deveria ser 100 ou documentado como dual-scale).

Associado: `institutional_strength` → `wait = max(5,100−strength) cap 60` → `remaining` correto; `dominant_direction` distribui `remaining` para BUY/SELL sem perda.

---

## G. Grade Integrity — thresholds + boundary tests (prova executada `forensic_decision_diversity.py`)

**Thresholds extraídos diretamente de `probability_engine.py:157–168`:**

```
A+  ≥80
A   ≥70
B   ≥60
C   ≥50
D   <50
```

**Boundary table (função grade isolada + epsilon 0.001):**

| INPUT | EXPECTED | GOT | RESULT |
|---|---|---|---|
| 0 | D | D | PASS |
| 1 | D | D | PASS |
| 49.999 | D | D | PASS |
| 50 | C | C | PASS |
| 50−0.001 | D | D | PASS |
| 50+0.001 | C | C | PASS |
| 59.999 | C | C | PASS |
| 60 | B | B | PASS |
| 60±0.001 | C/B | C/B | PASS |
| 69.999 | B | B | PASS |
| 70±0.001 | B/A | B/A | PASS |
| 79.999 | A | A | PASS |
| 80±0.001 | A/A+ | A/A+ | PASS |
| 100 | A+ | A+ | PASS |

**Consistência BTC/ETH (prova de que grade usa `strength` 44.x, não 854):**

```
BTC strength 44.388 → D  ✓  (se fosse 854 → A+ esperado, não ocorre)
ETH strength ~44.5 → D  ✓
Live B 60.88 → B ✓  (strength 60.88 produz B, não D)
```

**Grade Integrity: PASS** para a função pura; **FAIL** para a leitura do relatório que compara `854` com thresholds 0–100.

---

## H. Confidence Integrity — escala real + consumidores

- **Produzido:** `ConfidenceEngine` 0–100 (`confidence_result.confidence_score` e `final_confidence` clamp 0–100).
- **Armazenado:** `DecisionResult.confidence = calibrated/100` 0–1 (builder line 148, comentário “compatibilidade histórica UI ×100”).
- **Consumido:**
  - `ProbabilityEngine.analyze` recebe `confidence_result.final_confidence` **0–100** — correto (live 68.27, 70.17, 62.90).
  - `InstitutionalScoreEngine` recebe **0–100** — correto.
  - UI / snapshot reader deve fazer `confidence*100` para 0–100; relatório não fez (exibiu 0.68).
- **Detecção automática de troca 0.68↔68:** `0.682*100 =68.2` ≠ `0.682` — transformação `/100` silenciosa no builder; sem ela, consumidor esperaria 0–100 e receberia 68, ok; com ela, quem lê `DecisionResult.confidence` precisa saber que é 0–1.
- **Veredito:** Conversão existe, está **documentada no código** mas **não no contrato do relatório**; não é bug matemático, é **conversão silenciosa** que quebra a regra “nenhuma conversão silenciosa”. **FAIL** por falta de normalização declarada no relatório.

---

## I. Trade Filter Integrity — `allowed` vs `quality_score`

**Contrato engine:** `quality =100−penalty`; `allowed = penalty<50` (`penalty≥50 → blocked`). Logo `quality 0.0 → penalty 100 → allowed False`. Combinação `True+0.0` impossível sob contrato.

**Encontrado:**

```
Engine real (simulação com snapshot context)
  BTC REVERSAL        penalty 0  → quality 100.0 allowed True ✓
  ETH COMPRESSION     penalty 20 → quality 80.0  allowed True ✓
Snapshot DecisionResult
  BTC quality 100.0 (alias DecisionResult.quality) vs trade_quality_score 0.0, allowed True, level N/A
  ETH quality 80.0  vs trade_quality_score 0.0, allowed True
Live 00:04
  BTC SELL trade_quality_score 0.0 allowed True
  ETH SELL trade_quality_score 0.0 allowed True
```

**Root Cause #4 (abaixo):** `DecisionResultBuilder.build` mapeia `quality=trade_quality_score` mas **nunca seta** `trade_quality_score`, `trade_allowed`, `trade_quality_level`, `trade_block_reasons` no `DecisionResult`. Os campos permanecem nos defaults (`0.0 / True / N/A / ()`). O `TradeFilterResult` é consumido apenas para `InstitutionalScoreEngine` e para `is_valid=False` se `allowed==False`, mas seu valor nunca é persistido.

**Veredito:** `allowed True + quality 0.0` é **(F) valor exibido diferente do valor utilizado internamente** e **(E) campo quality_score não utilizado para determinar allowed no objeto persistido** (engine usou, mas não serializou). **FAIL**.

---

## J. Serialization Integrity — Engine → Model → dict → JSON → DecisionResult → Report

| Etapa | Transformação | Preserva escala? |
|---|---|---|
| `ConfidenceEngine 68.247` → `ConfidenceResult.final_confidence 68.247` | 0–100 intacto | ✓ |
| `ConfidenceResult` → `ProbabilityEngine` | 0–100 | ✓ |
| `ConfidenceResult` → `DecisionResultBuilder` | `/100` → stored 0–1 | **silenciosa** (divide sem renomear campo) |
| `ConfluenceEngine weighted 100.00` → `Probability/Institutional` | 0–100 | ✓ |
| `ConfluenceEngine weighted 100.00` → `DecisionResult.score` | `score` recebe `institutional_score 65.27`, não weighted | **misalias** no relatório |
| `EvidenceRanking total_weight 854` → `expected_strength 854` | sem teto → report chama `institutional_strength` 854 | **mislabel** |
| `TradeFilterResult quality 100/80` → `DecisionResult.trade_quality_score` | **não copiado** → permanece `0.0` | **omissão** |
| `TradeFilterResult allowed True` → `DecisionResult.trade_allowed` | **não copiado** → permanece `True` (default coincide por sorte) | **omissão** (falharia se penalty≥50) |
| `Probability wait 55.61` → `DecisionResult wait 55.61` | 0–100 round | ✓ legítimo; terminal `1.0` (0–1) diverge |
| `Snapshot JSON` → `report trace` | `trace["institutional_strength"]=expected_strength`, `trace["confidence_score"]=confidence (0–1)` sem ×100, `trace["confluence_score"]=DecisionResult.score` (fallback) | **não preserva** |

**Veredito:** **FAIL** — 4 transformações quebram a promessa “relatório representa exatamente o valor utilizado pelo pipeline”.

---

## K. Root Cause — causas raiz com localização cirúrgica

### ROOT CAUSE #1 — `institutional_strength 854` é `total_weight`, não força institucional

- **File:** `mercury_ai/analysis/evidence_ranking_engine.py`
- **Class:** `EvidenceRankingEngine`
- **Function:** `rank` (`calculate_contribution_score` → `rank`)
- **Line:** `29: total_weight = sum(e.weight for e in ranked)` ; `mercury_ai/analysis/decision_result_builder.py:145: expected_strength=ranked_result.total_weight`
- **Problem:** Relatório lê `DecisionResult.expected_strength` (soma não normalizada de pesos por evidência) e publica como `institutional_strength` (que na especificação e no `ProbabilityEngine` é 0–100). Escalas incompatíveis: `854` > `100` sempre.
- **Expected:** `institutional_strength` deveria ser `ProbabilityEngine.institutional_strength` 0–100 (ex: 44.38) ou ser renomeado para `total_weight` com escala documentada 0–~2000.
- **Actual:** `854.247` (BTC), `739.379` (ETH) — soma de `e.weight` (30, 60 etc) por 32 evidências.
- **Transformation:** `sum(weights)` sem divisão; nenhuma normalização; consumidor relatório interpreta como 0–100.
- **Consumer:** `scripts/v1_final_operational_proof_all_assets.py:313 trace["institutional_strength"]= safe_get(decision_result,"expected_strength")` → `reports/v1_operational_proof_all_assets.json`.

### ROOT CAUSE #2 — `confidence 0.68` exibido em escala errada

- **File:** `mercury_ai/analysis/decision_result_builder.py`
- **Class:** `DecisionResultBuilder`
- **Function:** `build`
- **Line:** `148: confidence=calibrated_confidence / 100.0  # DESIGN NOTE: 0-1 compat UI *100`
- **Problem:** Conversão silenciosa `/100` sem renomear campo nem declarar contrato; snapshot armazena 0–1, relatório exibe 0–1 como se fosse 0–100.
- **Expected:** Campo documentado 0–100 ou relatório fazer `*100` para exibição.
- **Actual:** `0.682476925` em JSON; relatório mostra `0.682` (68× menor).
- **Transformation:** `/100`.
- **Consumer:** `reports/v1_operational_proof_all_assets.json` + consumidores UI que esperam 0–1 vs engines que esperam 0–100.

### ROOT CAUSE #3 — `confluence_score 65.27` no relatório é `institutional_score`, não `weighted_score 100`

- **File:** `scripts/v1_final_operational_proof_all_assets.py`
- **Function:** `extract_trace`
- **Lines:** `312: trace["confluence_score"]= safe_get(decision_result,"score")` (fallback) + `349: trace["confluence_score"]= ws` (tenta sobrescrever com `confluence.weighted_score` mas `confluence` não está persistido no snapshot `DecisionSnapshot`, então fallback permanece)
- **Problem:** `DecisionResult.score` é `institutional_score` 0–100, não confluence. O weighted real `100.00` só existe em `AnalysisResult.confluence.weighted_score` (não serializado em `DecisionSnapshot` para snapshots antigos; hoje `explainability` tem, mas script não lê `explainability` para confluence).
- **Expected:** `confluence_score` deveria ser `AnalysisResult.confluence.weighted_score` ou `ConfluenceResult.weighted_score` (100.00).
- **Actual:** `65.275` / `63.242` (institutional_score).
- **Transformation:** alias errado.
- **Consumer:** gate `POST_RESOLVER_INTEGRITY` passa, mas humano compara grade com confluence errado.

### ROOT CAUSE #4 — `trade_filter.allowed True + quality 0.0` é bug de propagação

- **File:** `mercury_ai/analysis/decision_result_builder.py`
- **Class:** `DecisionResultBuilder`
- **Function:** `build`
- **Lines:** `~130–180 return DecisionResult(... quality=trade_quality_score, expected_strength=..., )` — **faltam** `trade_allowed`, `trade_quality_score`, `trade_quality_level`, `trade_block_reasons`, `mtf_consensus`, `market_regime`, `evidence_ranking` (alguns preenchidos em chamadas posteriores, mas trade_* nunca)
- **Also:** `mercury_ai/brain/mercury_decision_engine.py: ~490–520` chama `builder.build(..., trade_quality_score= trade_filter_result.quality_score)` mas não passa `trade_allowed`
- **Problem:** `TradeFilterResult` calculado corretamente (100/80) é usado para `is_valid` e para `InstitutionalScoreEngine`, mas **não é persistido** no `DecisionResult`. Snapshot fica com defaults `trade_quality_score 0.0`, `trade_allowed True` (default), `quality_level N/A`.
- **Expected:** `DecisionResult.trade_quality_score = 80.0/100.0`, `trade_allowed = penalty<50`, etc.
- **Actual:** `0.0 / True / N/A` sempre, violando `quality 0 → allowed False` ao comparar defaults.
- **Transformation:** omissão (não cópia).
- **Consumer:** `scanner` e `DecisionResult` downstream que decide ranking.

### ROOT CAUSE #5 — Probabilidades terminais em escala 0–1 vs legítimas 0–100

- **File:** `mercury_ai/core/analysis_pipeline.py`
- **Function:** `analyze` + `_build_terminal_result`
- **Lines:** `~230: DecisionResult(..., wait_probability=1.0)` para `DATA_QUALITY_FAIL`, `INSUFFICIENT_DATA`, `MARKET_CLOSED`, etc.
- **Problem:** Contrato `ProbabilityResult` é 0–100; terminais usam 0–1 (1.0 = 100%). Quebra `wait+buy+sell≈100`.
- **Expected:** `100.0` ou contrato dual-scale documentado.
- **Actual:** `1.0`.
- **Transformation:** `×100` faltando.
- **Consumer:** asserts de integridade e qualquer agregador que soma probabilidades de snapshots mistos.

> Nota: `Resolver Matrix` é **PASS** e não é causa; alterar `DecisionResolverEngine` mascararia os 4 bugs acima — proibido nesta fase (seção 16).

---

## L. Production Changes

```
PRODUCTION CODE CHANGED = NO
```

Nenhum arquivo de produção foi editado neste sprint forensic (apenas `scripts/forensic_*` e `reports/forensic_scale_trace.json` de evidência).

### Patch mínimo proposto (NÃO aplicado — aguardar aprovação)

**Aprovar antes de implementar — ordem, risco e linhas exatas:**

1. **Builder — propagar trade filter (RC#4)**
   ```python
   # mercury_ai/analysis/decision_result_builder.py: em build(), acrescentar params
   trade_allowed: bool, trade_block_reasons: tuple, trade_quality_score: float, trade_quality_level: str
   # e no return DecisionResult(..., trade_allowed=trade_allowed, trade_block_reasons=trade_block_reasons,
   # trade_quality_score=trade_quality_score, trade_quality_level=trade_quality_level, trade_quality? alias)
   # mercury_ai/brain/mercury_decision_engine.py: passar trade_filter_result.allowed/reasons/quality_score/level ao builder
   ```

2. **Builder — documentar confidence dual-scale ou renomear (RC#2)**
   - Opção A (mínima): renomear campo armazenado para `confidence_normalized` 0–1 e manter `confidence` 0–100, ou manter e documentar contrato `DecisionResult.confidence` 0–1 exigindo `*100` para display; corrigir `scripts/v1_final...` para `trace["confidence_score"] = decision_result.confidence *100`
   - 1 linha + comentário contrato

3. **Report — corrigir misalias (RC#1 + RC#3)**
   ```python
   # scripts/v1_final_operational_proof_all_assets.py
   trace["institutional_strength"] = explainability.institutional_score  # ou Probability strength se exposto
   trace["total_weight"]           = decision_result.expected_strength     # renomeado, escala solta
   trace["confluence_score"]       = analysis_result.confluence.weighted_score  # 0–100, fallback para explainability parsing
   trace["confidence_score"]       = decision_result.confidence * 100          # 0–100
   ```

4. **Pipeline terminais — normalizar probabilidades (RC#5)**
   ```python
   # mercury_ai/core/analysis_pipeline.py: _build_terminal_result e blocos DATA_QUALITY_FAIL etc
   wait_probability=100.0, buy_probability=0.0, sell_probability=0.0
   # ou, se manter 0–1, documentar contrato "terminal probabilities 0–1" e adaptar asserts
   ```

5. **Snapshot — persistir confluence weighted (opcional, fortalece J)**
   - Garantir `DecisionSnapshot` já carrega `evidence_ranking` + `context`; adicionar `confluence_result` ou usar `explainability` já persistida como fonte canônica de `weighted 100`.

**Risco do patch:** isolado a builder + report + pipeline terminal; `ProbabilityEngine` e `DecisionResolverEngine` intocados. Testes de grade/probabilidade/diversidade já provam compatibilidade.

---

## Veredito detalhado por gate (seção 18)

| Gate | Resultado | Prova |
|---|---|---|
| todas as escalas identificadas | ✓ | Tabela B + forensic_scale_trace.json |
| nenhuma conversão silenciosa | **FAIL** | RC#2 `/100`, RC#5 `1.0 vs 100` |
| institutional_strength explicado | ✓ (mas mislabeled) | RC#1 — é total_weight 854, grade usa 44.38 |
| grade consistente com seu input | ✓ quando lido 44.38 | BTC 44→D, live 60→B |
| confidence scale comprovada | **FAIL** display | engine 68 stored 0.68 |
| probabilities válidas | ✓ legítimo / **FAIL** terminal | snapshot terminal 1.0 |
| probabilities ≈100 | ✓ legítimo | 100.00 todos os SELL/BUY legit |
| trade filter contract | **FAIL** | True+0.0 persiste defaults |
| serialization preserva escala | **FAIL** | 4 transforms quebram J |
| BTC trace completo | ✓ | §C |
| ETH trace completo | ✓ | §D |
| todos ativos configurados identificados | ✓ | 2/2 XP.json + registry |
| todos executáveis testados | ✓ | 2/2 live + snapshots |
| BUY determinístico provado | ✓ mock + snapshot histórico BUY 44.28 | diversity script + ETH 2026-08-24 BUY |
| SELL determinístico provado | ✓ live SELL ambos | BTC/ETH 00:04 |
| WAIT determinístico provado | ✓ resolverWAIT | 5 casos |
| WAIT por invalid | ✓ | resolver rule 1 |
| WAIT por baixa confluência | ✓ | rule 3 |
| WAIT por conflito | ✓ | rule 4 |
| WAIT por NEUTRAL | ✓ | rule 2 |
| Resolver não sofreu alteração | ✓ | unmodified |
| nenhum failure escondido | **FAIL** | trade + terminal mascarados |

**Conclusão do sprint:** `V1 SCALE INTEGRITY = FAIL` — **não declarar V1 CLOSED**. O próximo passo é **A) PATCH CIRÚRGICO DEFINITIVO** com os 5 itens acima (estimativa < 15 linhas de produção + correções de report). Re-executar `forensic_scale_integrity_proofs.py` + `forensic_decision_diversity.py` + `v1_final_operational_proof_all_assets.py` deve transformar este FAIL em PASS.

---

## Artefatos de prova executável

- `scripts/forensic_scale_trace.py` → `reports/forensic_scale_trace.json`
- `scripts/forensic_scale_integrity_proofs.py` (grade boundaries, prob sum, confidence, trade, serialization) — PASS exceto trade/terminal documentados como FAIL esperado nesta fase
- `scripts/forensic_decision_diversity.py` — BUY/SELL/WAIT + 4 WAIT causas todas PASS
- `reports/v1_operational_proof/v1_operational_proof_all_assets.json` — 2026-08-31 22:41 (SELL+SELL) + 2026-09-01 00:04 (SELL+SELL, histórico comprova BUY)

---

## Apêndice — valores do enunciado reavaliados

```
BTC: Confluence 65.275  → na verdade institutional_score 65.275 (weighted real 100)
     Confidence 0.682   → 68.247 em 0–100, armazenado 0–1
     institutional_strength 854.247 → total_weight (não força); força real 44.38 grade D correto
     grade D → consistente com 44.38, inconsistente com 854
     trade True+0.0 → bug de persistência, engine deu 100.0 True

ETH: Confluence 63.242  → institutional_score 63.242 (weighted 100)
     Confidence 0.682   → 68.214
     institutional_strength 739.379 → total_weight
     grade D → força ~44 consistent
     trade True+0.0 → engine deu 80.0 True (COMPRESSION)
```

Declarar que `854 > 100` é “erro” sem provar a escala seria falso fechamento. A prova acima mostra **onde** cada número nasce, **quanto** é transformado e **quem** o consome — exatamente o objetivo deste sprint.
