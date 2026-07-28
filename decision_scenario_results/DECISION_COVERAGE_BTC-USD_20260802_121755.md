# DECISION COVERAGE MATRIX

**Generated:** 2026-08-02 12:17:55  
**Symbol:** BTC-USD  
**Total Scenarios:** 500  
**Unique Combinations:** 500  

---

## COVERAGE MATRIX: Decision Type × Grade

| Decision Type | A+ | A | B | C | D | Total |
|---------------|-----|-----|-----|-----|-----|-------|
| BUY | 0 | 0 | 0 | 0 | 0 | 0 |
| SELL | 0 | 0 | 0 | 0 | 0 | 0 |
| WAIT | 0 | 0 | 0 | 0 | 0 | 0 |

## COVERAGE MATRIX: Decision Type × Market Structure

| Decision Type | BOS | CHOCH | FVG | Liquidity | Order Block | Regime | Total |
|---------------|-----|-------|-----|-----------|-------------|--------|-------|
| BUY | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SELL | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| WAIT | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## COVERAGE MATRIX: Grade × Model C Rule

| Grade | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|-------|--------|--------|--------|--------|--------|--------|--------|-------|
| A+ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## COVERAGE MATRIX: Market Structure × Model C Rule

| Market Structure | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|------------------|--------|--------|--------|--------|--------|--------|--------|-------|
| BOS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CHOCH | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FVG | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Liquidity | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Order Block | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Regime | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## COVERAGE MATRIX: Conflict × Decision Type

| Conflict | BUY | SELL | WAIT | Total |
|----------|-----|------|------|-------|
| False | 0 | 0 | 0 | 0 |
| True | 0 | 0 | 0 | 0 |

## COVERAGE MATRIX: Conflict × Model C Rule

| Conflict | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|----------|--------|--------|--------|--------|--------|--------|--------|-------|
| False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| True | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


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
