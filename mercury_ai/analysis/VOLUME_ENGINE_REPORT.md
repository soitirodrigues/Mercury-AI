# VOLUME_ENGINE_REPORT.md

## Responsibilities
The `VolumeEngine` is responsible for institutional volume analysis (Relative Volume, Spikes, Trends, Absorption, Distribution, Accumulation, Climax).

## Contract
- **Input**: `pd.DataFrame` (OHLCV)
- **Output**: `VolumeAnalysis` (Immutable)

## Validation
- Validates volume signatures, trends, spike status, confidence, and quality metrics via `PipelineExecutor`.

## Integration
- Integrates with `PipelineExecutor` to ensure standardized execution, profiling, and audit trail generation.
