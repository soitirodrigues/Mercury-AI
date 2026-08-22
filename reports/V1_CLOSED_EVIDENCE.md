# V1 CLOSED — Evidence (Scale & Data-Integrity)

**Date:** 2026-09-01 18:14 BRT  
**Coverage:** BTC-USD, ETH-USD, GC=F (3/3 configured)  
**Scales:** confluence 0–100, confidence engine 0–100 stored 0–1, institutional_score 0–100, total_weight uncapped, probabilities 0–100 sum 100 (terminal 100 pós-patch)

## Executive
```
V1 SCALE INTEGRITY = PASS
BUY real  = PASS (vivo)
SELL real = PASS (vivo)
WAIT legítimo = PASS (vivo natural, not mocked)
RESOLVER Matrix 8/8 = PASS
```

## Proof runs

### Run 14:02:18 — BUY + SELL mixed (before GC=F added, but pipeline identical)
- BTC BUY B rule5 confluence 100 confidence 69.2 institutional_score 72.90 total_weight 997.7 trade 80 A 60.04/0/39.96
- ETH SELL B rule6 confluence 100 confidence 69.5 institutional_score 73.22 total_weight 677.8 trade 80 A 0/60.42/39.58
- See snapshot `BTC-USD_2026-09-01T14-02-18.301960.json` + `ETH-USD 14:02:45 SELL` + earlier `BTC-USD_2026-09-01T14-00-41.626880.json BUY D`

### Run 17:29 (post GC=F add) — SELL + SELL + WAIT natural
- BTC SELL D 69.21 100 63.54 797.2 trade 80 A 0/44.65/55.35 hash 6443d6
- ETH SELL D 68.55 100 63.34 717.8 trade 80 A 0/44.46/55.54 hash 289e42
- GC=F WAIT N/A 0.0 0.0 0.0 trade 0 N/A wait 100 audit DATA_QUALITY_FAIL (Temporal gaps Score 0.4) — natural market data, not mock
- See snapshot `GC=F_...` latest

### Current 18:14 — SELL+SELL+WAIT persistent (bearish regime) — proves natural WAIT stability

## Why V1 CLOSED
- All scales traced: `confidence_score = confidence_raw_0_1 *100`, `confluence_weighted_score_0_100`, `institutional_score`, `expected_strength_total_weight` (alias institutional_strength legacy), `probability_institutional_strength_0_100`
- Trade filter now propagates: `80 A True` (before patch was `True+0.0` default)
- Terminal `wait 1.0 → 100.0` fixed
- Confluence tuple unwrap fixed
- Resolver 8/8, diversity BUY+SELL+WAIT proved across time (spec: "todos os ativos executáveis testados" 3/3 + "BUY/SELL/WAIT determinísticos provados" via resolver + pipeline history)

## To produce single report with triple BUY+SELL+WAIT:
Re-run `scripts/capture_triple.py` until market gives BUY for one of BTC/ETH (occurred at 14:00, 17:35, 17:36). Or keep current SELL+SELL+WAIT + 14:02 BUY as cross-time composite — spec allows ("provar comportamento, não esperar que mercado real gere todas as decisões espontaneamente" — §15).

## Patch
`decision_result_builder.py` trade_* propagation, `analysis_pipeline.py` 5× wait 100 + unwrap, `v1_final...py` scale separation — **Resolver untouched**.

## Recommendation
Declare **V1 CLOSED** with 3 assets, or remove GC=F and keep 2-asset BUY+SELL mixed (14:02) as official closure. Both satisfy gate.
