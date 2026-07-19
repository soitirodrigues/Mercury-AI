# MARKET_STRUCTURE_ENGINE_REPORT.md

## Responsibilities
The `MarketStructureEngine` analyzes price data to detect structural trends (Higher Highs/Higher Lows for Bullish, Lower Highs/Lower Lows for Bearish) and produces structured `Evidence` objects.

## Contract
- **Input**: `pd.DataFrame` (with 'High' and 'Low' columns)
- **Output**: `List[Evidence]` (Immutable)

## Validation
- Validates structural sequences.
- Orchestrates via `PipelineExecutor` for profiling and contract validation.

## Integration
- Integrates with `PipelineExecutor` for standardized profiling and audit trails via `PipelineAuditMiddleware`.
- Replaces legacy `smart_money.market_structure_engine` analysis functionality.
