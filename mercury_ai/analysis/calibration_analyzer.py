import json
import os
from typing import Dict

class CalibrationAnalyzer:
    def __init__(self, replay_dir: str = "data/replay_results"):
        self.replay_dir = replay_dir

    def analyze_calibration(self, num_bins: int = 10) -> Dict[str, Dict[str, float]]:
        bins = {f"bin_{i}": {"hits": 0, "total": 0, "avg_confidence": 0.0} for i in range(num_bins)}
        
        # Load all replay results
        for filename in os.listdir(self.replay_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.replay_dir, filename), 'r') as f:
                    data = json.load(f)
                
                confidence = data.get("confidence", 0.5) 
                
                bin_idx = int(confidence * num_bins)
                if bin_idx == num_bins: bin_idx = num_bins - 1
                
                b = bins[f"bin_{bin_idx}"]
                b["total"] += 1
                if data["hit"]:
                    b["hits"] += 1
                b["avg_confidence"] += confidence

        # Calculate final metrics
        results = {}
        for b_name, b_data in bins.items():
            if b_data["total"] > 0:
                results[b_name] = {
                    "win_rate": b_data["hits"] / b_data["total"],
                    "avg_confidence": b_data["avg_confidence"] / b_data["total"],
                    "sample_size": b_data["total"]
                }
        return results
