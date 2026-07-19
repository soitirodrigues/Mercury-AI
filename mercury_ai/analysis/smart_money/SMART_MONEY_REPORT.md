# SMART_MONEY_REPORT.md

## Responsibilities
The `SmartMoneyEngine` orchestrates institutional analysis by integrating individual V1 engines (Market Structure, Liquidity, FVG, Order Blocks).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `SmartMoneyAnalysis` (Immutable)

## Validation
- Aggregates insights from specialized engines.
- Calculates `institutional_score` based on detected patterns.
- Ensures consistent pipeline execution.

## Integration
- Integrates with `PipelineExecutor` for standardized profiling and audit trails.
- Consumes standardized models from V1 engines.
