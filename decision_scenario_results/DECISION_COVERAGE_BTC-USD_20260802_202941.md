# DECISION COVERAGE MATRIX

**Generated:** 2026-08-02 20:29:41  
**Symbol:** BTC-USD  
**Total Scenarios:** 5000  
**Unique Combinations:** 5000  

---

## COVERAGE MATRIX: Decision Type × Grade

| Decision Type | A+ | A | B | C | D | Total |
|---------------|-----|-----|-----|-----|-----|-------|
| BUY | 504 | 504 | 504 | 504 | 252 | 2268 |
| SELL | 504 | 504 | 504 | 504 | 252 | 2268 |
| WAIT | 0 | 0 | 464 | 0 | 0 | 464 |

## COVERAGE MATRIX: Decision Type × Market Structure

| Decision Type | BOS | CHOCH | FVG | Liquidity | Order Block | Regime | Total |
|---------------|-----|-------|-----|-----------|-------------|--------|-------|
| BUY | 810 | 810 | 972 | 810 | 810 | 648 | 4860 |
| SELL | 810 | 810 | 972 | 810 | 810 | 648 | 4860 |
| WAIT | 144 | 144 | 180 | 144 | 140 | 104 | 856 |

## COVERAGE MATRIX: Grade × Model C Rule

| Grade | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|-------|--------|--------|--------|--------|--------|--------|--------|-------|
| A+ | 280 | 392 | 280 | 392 | 336 | 280 | 280 | 2240 |
| A | 280 | 392 | 280 | 392 | 336 | 280 | 280 | 2240 |
| B | 410 | 572 | 410 | 570 | 492 | 410 | 406 | 3270 |
| C | 280 | 392 | 280 | 392 | 336 | 280 | 280 | 2240 |
| D | 140 | 196 | 140 | 196 | 168 | 140 | 140 | 1120 |

## COVERAGE MATRIX: Market Structure × Model C Rule

| Market Structure | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|------------------|--------|--------|--------|--------|--------|--------|--------|-------|
| BOS | 490 | 686 | 490 | 686 | 588 | 490 | 490 | 3920 |
| CHOCH | 490 | 686 | 490 | 686 | 588 | 490 | 490 | 3920 |
| FVG | 590 | 826 | 590 | 826 | 708 | 590 | 590 | 4720 |
| Liquidity | 490 | 686 | 490 | 686 | 588 | 490 | 490 | 3920 |
| Order Block | 490 | 684 | 490 | 682 | 588 | 490 | 486 | 3910 |
| Regime | 390 | 544 | 390 | 542 | 468 | 390 | 386 | 3110 |

## COVERAGE MATRIX: Conflict × Decision Type

| Conflict | BUY | SELL | WAIT | Total |
|----------|-----|------|------|-------|
| False | 1008 | 1008 | 232 | 2248 |
| True | 1260 | 1260 | 232 | 2752 |

## COVERAGE MATRIX: Conflict × Model C Rule

| Conflict | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Total |
|----------|--------|--------|--------|--------|--------|--------|--------|-------|
| False | 625 | 874 | 625 | 873 | 750 | 625 | 623 | 4995 |
| True | 765 | 1070 | 765 | 1069 | 918 | 765 | 763 | 6115 |


---

## RULE COVERAGE VALIDATION

### Model C Rules Coverage Status

| Rule | Description | Scenarios | Status |
|------|-------------|-----------|--------|
| Rule 1 | Strong Trend + Structure Alignment | 1390 | ✅ COVERED |
| Rule 2 | Trend Continuation with Volume Confirmation | 1944 | ✅ COVERED |
| Rule 3 | Reversal at Key Level with Confluence | 1390 | ✅ COVERED |
| Rule 4 | Breakout with Institutional Volume | 1942 | ✅ COVERED |
| Rule 5 | Pullback to Order Block/FVG | 1668 | ✅ COVERED |
| Rule 6 | Liquidity Sweep + Reversal | 1390 | ✅ COVERED |
| Rule 7 | Regime Change Confirmation | 1386 | ✅ COVERED |


### Market Structures Coverage Status

| Structure | Scenarios | Status |
|-----------|-----------|--------|
| BOS | 1764 | ✅ COVERED |
| CHOCH | 1764 | ✅ COVERED |
| FVG | 2124 | ✅ COVERED |
| Liquidity | 1764 | ✅ COVERED |
| Order Block | 1760 | ✅ COVERED |
| Regime | 1400 | ✅ COVERED |


### Grades Coverage Status

| Grade | Scenarios | Status |
|-------|-----------|--------|
| A+ | 1008 | ✅ COVERED |
| A | 1008 | ✅ COVERED |
| B | 1472 | ✅ COVERED |
| C | 1008 | ✅ COVERED |
| D | 504 | ✅ COVERED |


### Decision Types Coverage Status

| Decision | Scenarios | Status |
|----------|-----------|--------|
| BUY | 2268 | ✅ COVERED |
| SELL | 2268 | ✅ COVERED |
| WAIT | 464 | ✅ COVERED |


---

## COMBINATIONAL COVERAGE

**Total Unique Combinations Tested:** 5000

### Top 20 Most Tested Combinations

| Combination | Count |
|-------------|-------|
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|conflict=False | 1 |
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|conflict=True | 1 |
| BUY|A+|BOS|Rule 2: Trend Continuation with Volume Confirmation|conflict=False | 1 |
| BUY|A+|BOS|Rule 2: Trend Continuation with Volume Confirmation|conflict=True | 1 |
| BUY|A+|BOS|Rule 3: Reversal at Key Level with Confluence|conflict=False | 1 |
| BUY|A+|BOS|Rule 3: Reversal at Key Level with Confluence|conflict=True | 1 |
| BUY|A+|BOS|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|BOS|Rule 4: Breakout with Institutional Volume|conflict=True | 1 |
| BUY|A+|BOS|Rule 5: Pullback to Order Block/FVG|conflict=False | 1 |
| BUY|A+|BOS|Rule 5: Pullback to Order Block/FVG|conflict=True | 1 |
| BUY|A+|BOS|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|BOS|Rule 6: Liquidity Sweep + Reversal|conflict=True | 1 |
| BUY|A+|BOS|Rule 7: Regime Change Confirmation|conflict=False | 1 |
| BUY|A+|BOS|Rule 7: Regime Change Confirmation|conflict=True | 1 |
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|conflict=False | 1 |
| BUY|A+|BOS|Rule 1: Strong Trend + Structure Alignment|Rule 2: Trend Continuation with Volume Confirmation|conflict=True | 1 |
| BUY|A+|BOS|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=False | 1 |
| BUY|A+|BOS|Rule 3: Reversal at Key Level with Confluence|Rule 4: Breakout with Institutional Volume|conflict=True | 1 |
| BUY|A+|BOS|Rule 5: Pullback to Order Block/FVG|Rule 6: Liquidity Sweep + Reversal|conflict=False | 1 |
| BUY|A+|BOS|Rule 5: Pullback to Order Block/FVG|Rule 6: Liquidity Sweep + Reversal|conflict=True | 1 |


---

## VALIDATION SUMMARY

- **All 7 Model C Rules Covered:** ✅ YES
- **All 6 Market Structures Covered:** ✅ YES
- **All 5 Grades Covered:** ✅ YES
- **All 3 Decision Types Covered:** ✅ YES
- **Conflict Scenarios Tested:** ✅ YES

**Overall Certification:** ✅ PASSED

---

*Coverage matrix generated by Mercury-AI Sprint 1.9 Bloco 5/10 Decision Scenario Validation*
