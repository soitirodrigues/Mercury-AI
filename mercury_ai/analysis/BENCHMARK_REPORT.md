# BENCHMARK_REPORT.md

## Overview
This report provides performance metrics for the `Mercury-AI` decision pipeline, measured via the `MercuryBenchmarkFramework`.

## Metrics
- **Accuracy**: Based on historical replay classification.
- **Confidence**: Average confidence score of decisions.
- **Execution Time**: Average time per pipeline run.
- **Memory**: Peak memory usage per run.
- **Consistency**: Score representing decision stability across runs.

## Methodology
The benchmark framework replays historical market data through the pipeline, records `DecisionSnapshot` objects, and measures performance across key stages using `PipelineProfiler`.
