# PRICE_ACTION_REPORT.md

## Responsibilities
The `PriceActionEngine` is responsible for institutional price action analysis (patterns like Engulfing, Pin Bars, etc.).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `PriceActionAnalysis` (Immutable)

## Validation
- Validates price action patterns, confidence, and quality metrics via `PipelineExecutor`.

## Integration
- Integrates with `PipelineExecutor` to ensure standardized execution, profiling, and audit trail generation.
