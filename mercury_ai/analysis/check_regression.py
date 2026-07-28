import os
import json
from dataclasses import asdict
from typing import List, Dict, Any

class RegressionThresholdExceededError(Exception):
    pass

def check_regression(
    baseline_file: str,
    current_data: Dict[str, Any],
    thresholds: Dict[str, float]
) -> None:
    """
    Compares current execution metrics against baseline values,
    raising RegressionThresholdExceededError if any threshold is exceeded.

    Args:
        baseline_file: Path to baseline data JSON file
        current_data: Dictionary of current metrics
        thresholds: Dictionary of {metric_name: max_allowed_deviation}
    """
    try:
        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Baseline file not found: {baseline_file}")

    for metric, max_deviation in thresholds.items():
        current_value = current_data.get(metric)
        baseline_value = baseline_data.get(metric)

        if current_value is None or baseline_value is None:
            continue  # Skip metrics not present in both

        if isinstance(current_value, (int, float)) and isinstance(baseline_value, (int, float)):
            relative_diff = (current_value - baseline_value) / baseline_value if baseline_value != 0 else (current_value - baseline_value)
            if abs(relative_diff) > max_deviation:
                raise RegressionThresholdExceededError(
                    f"{metric} exceeded threshold:"
                    f"  Current: {current_value}"
                    f"  Baseline: {baseline_value}"
                    f"  Allowed deviation: {max_deviation * 100:.2f}%"
                )
    print(f"Regression check passed for {len(thresholds)} metrics")