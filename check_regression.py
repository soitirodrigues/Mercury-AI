import argparse
import os
import json
import numpy as np
from glob import glob

class PerformanceRegressionError(Exception):
    """Custom exception for performance regression detection"""
    pass

def get_latest_report(runtime_reports):
    # Sort reports by timestamp in filename
    return sorted(runtime_reports, key=lambda x: int(x.split('_')[-1].split('.')[0]))

def check_regression(current_metrics, historical_averages, threshold=0.1):
    for stage, current_time in current_metrics.items():
        historical_avg = historical_averages.get(stage)
        if historical_avg is None:
            continue
        
        if current_time > historical_avg * (1 + threshold):
            excess = current_time - historical_avg * (1 + threshold)
            raise PerformanceRegressionError(
                f"Regression detected in {stage}: {current_time:.2f}s vs historical avg {historical_avg:.2f}s. "
                f"Threshold exceeded by {excess:.2f}s"
            )

def main():
    parser = argparse.ArgumentParser(description='Performance regression checker')
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='Threshold percentage for regression detection')
    parser.add_argument('--fail-on-threshold', action='store_true',
                        help='Exit with non-zero code on threshold exceedance')
    args = parser.parse_args()

    # Load all runtime reports
    report_files = glob('runtime_reports/*.json')
    if not report_files:
        print('No runtime reports found')
        return 1

    # Get latest report as current metrics
    latest_report = get_latest_report(report_files)[-1]
    with open(latest_report, 'r') as f:
        current_metrics = json.load(f)

    # Calculate historical averages
    historical_metrics = []
    for report in get_latest_report(report_files)[:-1]:  # Exclude current
        with open(report, 'r') as f:
            historical_metrics.append(json.load(f))

    historical_averages = {}
    for stage in current_metrics:
        stages_metrics = [m[stage] for m in historical_metrics if stage in m]
        if stages_metrics:
            historical_averages[stage] = np.mean(stages_metrics)

    # Check regression
    try:
        check_regression(current_metrics, historical_averages, args.threshold)
        print('All performance metrics within acceptable thresholds')
        return 0
    except PerformanceRegressionError as e:
        if args.fail_on_threshold:
            print(str(e))
            return 1
        else:
            print(f'Warning: {e}')
            return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())