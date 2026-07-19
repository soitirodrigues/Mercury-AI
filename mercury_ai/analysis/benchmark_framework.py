import time
import tracemalloc
import os
import psutil
from typing import List
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.models.benchmark_report import BenchmarkRunResult, BenchmarkReport
from mercury_ai.analysis.metric_calculator import MetricCalculator
from mercury_ai.utils.deterministic_clock import DeterministicClock

from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

class MercuryBenchmarkFramework:
    def __init__(self):
        provider = YahooFinanceProvider()
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]), 
            providers=[provider]
        )
        tracemalloc.start()


    def run_benchmark(self, symbols: List[str]) -> BenchmarkReport:
        run_results = []
        decisions = []
        outcomes = []
        scores = []

        process = psutil.Process(os.getpid())

        for symbol in symbols:
            tracemalloc.clear_traces()
            start_time = time.perf_counter()

            result = self.pipeline.analyze(symbol)

            end_time = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()

            # Fallback to process RSS if tracemalloc is 0
            memory = float(peak)
            if memory == 0:
                memory = float(process.memory_info().rss)

            run_results.append(BenchmarkRunResult(
                timestamp=DeterministicClock.utcnow().isoformat(),
                symbol=symbol,
                decision_result=result.decision,
                execution_time=end_time - start_time,
                memory_usage=memory
            ))

            # Aggregate for metric calculation (Example: use simulated outcomes for demo)
            decisions.append(result.decision.decision)
            scores.append(result.decision.score)
            outcomes.append(0.01 if result.decision.decision == "BUY" else -0.01) # Dummy outcome

        metrics = MetricCalculator.calculate(decisions, outcomes, scores)

        return BenchmarkReport(
            version="1.0",
            results=tuple(run_results),
            average_execution_time=sum(r.execution_time for r in run_results) / len(run_results),
            performance_metrics=metrics
        )

