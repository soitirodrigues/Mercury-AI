# LIQUIDITY_ENGINE_REPORT.md

## Responsibilities
The `LiquidityEngine` is responsible for detecting institutional liquidity patterns (Equal Highs/Lows, Sweeps, Voids, Premium/Discount zones).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `LiquidityAnalysis` (Immutable)

## Validation
- Validates liquidity signatures, confidence, and quality metrics via `PipelineExecutor`.

## Integration
- Integrates with `PipelineExecutor` to ensure standardized execution, profiling, and audit trail generation.
