# DECISION COVERAGE MATRIX

**Generated:** 2026-08-02 20:07:08  
**Symbol:** BTC-USD  
**Total Scenarios:** 500  
**Unique Combinations:** 500  

---

## COVERAGE MATRIX: Decision Type × Grade

| Decision Type | A+ | A | B | C | D | Total |
|---------------|-----|-----|-----|-----|-----|-------|
| BUY | 42 | 42 | 42 | 42 | 21 | 189 |
| SELL | 42 | 42 | 42 | 42 | 21 | 189 |
| WAIT | 0 | 0 | 42 | 42 | 38 | 122 |

## COVERAGE MATRIX: Decision Type × Market Structure

| Decision Type | BOS | CHOCH | FVG | Liquidity | Order Block | Regime | Total |
|---------------|-----|-------|-----|-----------|-------------|--------|-------|
| BUY | 67 | 66 | 82 | 65 | 68 | 54 | 402 |
| SELL | 67 | 66 | 82 | 65 | 68 | 54 | 402 |
| WAIT | 42 | 42 | 51 | 42 | 41 | 32 | 250 |

## COVERAGE MATRIX: Grade × Model C Rule

| Grade | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|-------|--------|--------|--------|--------|--------|--------|--------|-------|
| A+ | 56 | 0 | 28 | 0 | 28 | 28 | 0 | 140 |
| A | 56 | 0 | 28 | 0 | 28 | 28 | 0 | 140 |
| B | 84 | 0 | 42 | 0 | 42 | 42 | 0 | 210 |
| C | 84 | 0 | 42 | 0 | 42 | 42 | 0 | 210 |
| D | 53 | 0 | 26 | 0 | 26 | 27 | 0 | 132 |

## COVERAGE MATRIX: Market Structure × Model C Rule

| Market Structure | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|------------------|--------|--------|--------|--------|--------|--------|--------|-------|
| BOS | 116 | 0 | 58 | 0 | 58 | 60 | 0 | 292 |
| CHOCH | 112 | 0 | 56 | 0 | 56 | 62 | 0 | 286 |
| FVG | 146 | 0 | 73 | 0 | 73 | 69 | 0 | 361 |
| Liquidity | 108 | 0 | 54 | 0 | 54 | 64 | 0 | 280 |
| Order Block | 119 | 0 | 59 | 0 | 59 | 58 | 0 | 295 |
| Regime | 93 | 0 | 46 | 0 | 46 | 47 | 0 | 232 |

## COVERAGE MATRIX: Conflict × Decision Type

| Conflict | BUY | SELL | WAIT | Total |
|----------|-----|------|------|-------|
| False | 168 | 168 | 122 | 458 |
| True | 21 | 21 | 0 | 42 |

## COVERAGE MATRIX: Conflict × Model C Rule

| Conflict | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|----------|--------|--------|--------|--------|--------|--------|--------|-------|
| False | 305 | 0 | 152 | 0 | 152 | 153 | 0 | 762 |
| True | 28 | 0 | 14 | 0 | 14 | 14 | 0 | 70 |


---

## RULE COVERAGE VALIDATION

### Model C Rules Coverage Status

| Rule | Description | Scenarios | Status |
|------|-------------|-----------|--------|
| Rule 1 | Strong Trend + Structure Alignment | 333 | ✅ COVERED |
| Rule 2 | Trend Continuation with Volume Confirmation | 0 | ❌ MISSING |
| Rule 3 | Reversal at Key Level with Confluence | 166 | ✅ COVERED |
| Rule 4 | Breakout with Institutional Volume | 0 | ❌ MISSING |
| Rule 5 | Pullback to Order Block/FVG | 166 | ✅ COVERED |
| Rule 6 | Liquidity Sweep + Reversal | 167 | ✅ COVERED |
| Rule 7 | Regime Change Confirmation | 0 | ❌ MISSING |


### Market Structures Coverage Status

| Structure | Scenarios | Status |
|-----------|-----------|--------|
| BOS | 176 | ✅ COVERED |
| CHOCH | 174 | ✅ COVERED |
| FVG | 215 | ✅ COVERED |
| Liquidity | 172 | ✅ COVERED |
| Order Block | 177 | ✅ COVERED |
| Regime | 140 | ✅ COVERED |


### Grades Coverage Status

| Grade | Scenarios | Status |
|-------|-----------|--------|
| A+ | 84 | ✅ COVERED |
| A | 84 | ✅ COVERED |
| B | 126 | ✅ COVERED |
| C | 126 | ✅ COVERED |
| D | 80 | ✅ COVERED |


### Decision Types Coverage Status

| Decision | Scenarios | Status |
|----------|-----------|--------|
| BUY | 189 | ✅ COVERED |
| SELL | 189 | ✅ COVERED |
| WAIT | 122 | ✅ COVERED |


---

## COMBINATIONAL COVERAGE

**Total Unique Combinations Tested:** 500

### Top 20 Most Tested Combinations

| Combination | Count |
|-------------|-------|
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|BOS|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|Rule 3: Reversal at Key Level with Confluence|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|CHOCH|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|CHOCH|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|CHOCH|Rule 1: Strong Trend + Structure Alignment|Rule 3: Reversal at Key Level with Confluence|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|FVG|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|FVG|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|FVG|Rule 1: Strong Trend + Structure Alignment|Rule 3: Reversal at Key Level with Confluence|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|Liquidity|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|Liquidity|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|Liquidity|Rule 1: Strong Trend + Structure Alignment|Rule 3: Reversal at Key Level with Confluence|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|Order Block|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|Order Block|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|Order Block|Rule 1: Strong Trend + Structure Alignment|Rule 3: Reversal at Key Level with Confluence|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|Regime|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|Regime|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|Regime|Rule 1: Strong Trend + Structure Alignment|Rule 3: Reversal at Key Level with Confluence|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|BOS|FVG|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|BOS|FVG|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |


---

## VALIDATION SUMMARY

- **All 7 Model C Rules Covered:** ❌ NO
- **All 6 Market Structures Covered:** ✅ YES
- **All 5 Grades Covered:** ✅ YES
- **All 3 Decision Types Covered:** ✅ YES
- **Conflict Scenarios Tested:** ✅ YES

**Overall Certification:** ❌ FAILED

---

*Coverage matrix generated by Mercury-AI Sprint 1.9 Bloco 5/10 Decision Scenario Validation*
