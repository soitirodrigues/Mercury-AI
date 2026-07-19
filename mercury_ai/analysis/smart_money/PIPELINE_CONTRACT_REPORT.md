# Pipeline Contract Report

## Overview
This report documents the implementation of contract-based validation for the Liquidity Engine pipeline stages. Each stage now includes pre- and post-condition checks to ensure data integrity and fail-fast behavior.

## Implementation Detail
- Each stage (`build`, `validate`, `metrics`, `scores`, `selector`, `populate`, `evidence`) now includes explicit type-checking, field validation, and contract enforcement using custom validation logic.
- Immutability is ensured by operating on data passed through the pipeline and not modifying input objects directly.
- Fail-fast exceptions (TypeError, ValueError) are raised immediately upon detection of a contract violation.

## Pipeline Stages Validated
1.  **Build Groups:** Input List[Swing] -> Output List[EqualHighGroup]
2.  **Validation:** Input List[EqualHighGroup] -> Output List[EqualHighGroup]
3.  **Metrics:** Input List[EqualHighGroup] -> Output List[EqualHighMetrics]
4.  **Scores:** Input List[EqualHighMetrics] -> Output List[EqualHighScore]
5.  **Selector:** Input List[EqualHighScore] -> Output Optional[EqualHighScore]
6.  **Profile:** Input MarketStructureProfile, SelectedScore -> Output MarketStructureProfile
7.  **Evidence:** Input SelectedScore -> Output List[Evidence]
8.  **Analysis:** Aggregates stage outputs -> LiquidityAnalysis
