from mercury_ai.analysis.benchmark_framework import MercuryBenchmarkFramework

def test_benchmark_framework_execution():
    framework = MercuryBenchmarkFramework()
    symbols = ["GC=F"]
    report = framework.run_benchmark(symbols)
    
    assert len(report.results) == 1
    assert report.average_execution_time > 0
    assert report.results[0].memory_usage > 0
    assert report.performance_metrics.accuracy >= 0
