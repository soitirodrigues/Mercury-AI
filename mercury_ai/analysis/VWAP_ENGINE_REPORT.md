# VWAP_ENGINE_REPORT.md

## Responsibilities
The `VWAPEngine` is responsible for institutional VWAP analysis (VWAP calculation, Distance to VWAP, Acceptance, Rejection, Mean Reversion, Institutional Bias).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `VWAPAnalysis` (Immutable)

## Validation
- Validates VWAP calculation, price-VWAP interaction, institutional bias, confidence, and quality metrics via `PipelineExecutor`.

## Integration
- Integrates with `PipelineExecutor` to ensure standardized execution, profiling, and audit trail generation.
