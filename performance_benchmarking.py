import time
import pandas as pd
import json
from pathlib import Path
from mercury_ai.brain import PipelineExecutor
from statistics import mean


class PerformanceRegressionError(Exception):
    pass


def stage_timer(stage_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"\n--- Stage '{stage_name}' Execution ---\n• Start: {time.ctime(start_time)}\n• End: {time.ctime(end_time)}\n• Duration: {execution_time:.4f} seconds\n")
            
            # Record metrics in DataFrame
            metrics = pd.DataFrame([{
                'stage': stage_name,
                'start': start_time,
                'end': end_time,
                'duration': execution_time,
                'timestamp': time.time()
            }])
            
            # Append to global metrics storage
            global _pipeline_metrics
            _pipeline_metrics = _pipeline_metrics.append(metrics, ignore_index=True)
            return result
        return wrapper
    return decorator

def benchmark_pipeline():
    executor = PipelineExecutor()
    total_time = 0

    # Stage 1: Data Loading
    with PipelineStageTimer("Data Loading") as timer:
        data = executor.load_data()
    total_time += timer.duration

    # Stage 2: Validation
    with PipelineStageTimer("Validation") as timer:
        validated_data = executor.validate(data)
    total_time += timer.duration

    # Stage 3: Decision Engine
    with PipelineStageTimer("Decision Engine") as timer:
        decision = executor.process(validated_data)
    total_time += timer.duration

    # Stage 4: Reporting
    with PipelineStageTimer("Reporting") as timer:
        report = executor.generate_report(decision)
    total_time += timer.duration

    print(f"\nTotal pipeline execution time: {total_time:.4f} seconds")
    return total_time

def load_historical_metrics():
    """
    Load previous benchmark results for comparison
    """
    metrics = {}
    reports_dir = Path(__file__).parent / 'runtime_reports'
    if not reports_dir.exists():
        return None

    for report_file in reports_dir.glob('runtime_report_*.json'):
        with open(report_file, 'r') as f:
            data = json.load(f)
            for stage, time in data.items():
                if stage not in metrics:
                    metrics[stage] = []
                metrics[stage].append(time)

    return metrics

def check_regression(current_metrics, threshold=0.1):
    """
    Compare current metrics against historical data
    """
    historical = load_historical_metrics()
    if not historical:
        print("No historical data found - cannot check regression")
        return False

    for stage, current_time in current_metrics.items():
        if stage in historical:
            historical_times = historical[stage]
            historical_avg = mean(historical_times)
            if current_time > historical_avg * (1 + threshold):
                print(f"Regression detected in {stage}: {current_time:.2f}s vs historical avg {historical_avg:.2f}s")
                return True
    return False

if __name__ == "__main__":
    benchmark_pipeline()
