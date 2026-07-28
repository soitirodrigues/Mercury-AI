# DECISION COVERAGE MATRIX

**Generated:** 2026-08-02 20:26:36  
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
| A+ | 56 | 28 | 28 | 28 | 0 | 0 | 28 | 168 |
| A | 56 | 28 | 28 | 28 | 0 | 0 | 28 | 168 |
| B | 84 | 42 | 42 | 42 | 0 | 0 | 42 | 252 |
| C | 84 | 42 | 42 | 42 | 0 | 0 | 42 | 252 |
| D | 53 | 26 | 26 | 26 | 0 | 0 | 27 | 158 |

## COVERAGE MATRIX: Market Structure × Model C Rule

| Market Structure | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|------------------|--------|--------|--------|--------|--------|--------|--------|-------|
| BOS | 116 | 58 | 58 | 58 | 0 | 0 | 60 | 350 |
| CHOCH | 112 | 56 | 56 | 56 | 0 | 0 | 62 | 342 |
| FVG | 146 | 73 | 73 | 73 | 0 | 0 | 69 | 434 |
| Liquidity | 108 | 54 | 54 | 54 | 0 | 0 | 64 | 334 |
| Order Block | 119 | 59 | 59 | 59 | 0 | 0 | 58 | 354 |
| Regime | 93 | 46 | 46 | 46 | 0 | 0 | 47 | 278 |

## COVERAGE MATRIX: Conflict × Decision Type

| Conflict | BUY | SELL | WAIT | Total |
|----------|-----|------|------|-------|
| False | 168 | 168 | 122 | 458 |
| True | 21 | 21 | 0 | 42 |

## COVERAGE MATRIX: Conflict × Model C Rule

| Conflict | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|----------|--------|--------|--------|--------|--------|--------|--------|-------|
| False | 305 | 152 | 152 | 152 | 0 | 0 | 153 | 914 |
| True | 28 | 14 | 14 | 14 | 0 | 0 | 14 | 84 |


---

## RULE COVERAGE VALIDATION

### Model C Rules Coverage Status

| Rule | Description | Scenarios | Status |
|------|-------------|-----------|--------|
| Rule 1 | Strong Trend + Structure Alignment | 333 | ✅ COVERED |
| Rule 2 | Trend Continuation with Volume Confirmation | 166 | ✅ COVERED |
| Rule 3 | Reversal at Key Level with Confluence | 166 | ✅ COVERED |
| Rule 4 | Breakout with Institutional Volume | 166 | ✅ COVERED |
| Rule 5 | Pullback to Order Block/FVG | 0 | ❌ MISSING |
| Rule 6 | Liquidity Sweep + Reversal | 0 | ❌ MISSING |
| Rule 7 | Regime Change Confirmation | 167 | ✅ COVERED |


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
| BUY|A+|BOS|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|CHOCH|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|CHOCH|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|CHOCH|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|FVG|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|FVG|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|FVG|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|Liquidity|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|Liquidity|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|Liquidity|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|Order Block|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|Order Block|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|Order Block|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|Regime|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|Regime|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|Regime|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|BOS|FVG|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|BOS|FVG|Rule 7: Regime Change Confirmation|conflict=False | 1 |


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
