# FVG_ENGINE_REPORT.md

## Responsibilities
The `FairValueGapEngine` is responsible for detecting institutional Fair Value Gaps (Bullish/Bearish, Filled/Open status, Quality).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `FairValueGapAnalysis` (Immutable)

## Validation
- Validates FVG patterns, status, confidence, and quality metrics via `PipelineExecutor`.

## Integration
- Integrates with `PipelineExecutor` to ensure standardized execution, profiling, and audit trail generation.
