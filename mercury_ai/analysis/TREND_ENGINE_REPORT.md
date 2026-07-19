# TREND_ENGINE_REPORT.md

## Responsibilities
The `TrendEngine` is responsible for institutional trend analysis (HH/HL, LH/LL, EMAs, ADX, metrics).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `TrendAnalysis` (Immutable)

## Validation
- Validates structure (HH/HL, LH/LL), moving averages (EMA20, EMA50, EMA200), and trend metrics via `PipelineExecutor`.

## Integration
- Integrates with `PipelineExecutor` to ensure standardized execution, profiling, and audit trail generation.
