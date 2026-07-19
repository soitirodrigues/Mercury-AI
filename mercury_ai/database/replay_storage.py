from dataclasses import dataclass
from typing import Any
import json
import os

@dataclass(frozen=True)
class ReplayMetrics:
    mae: float
    mfe: float
    pl: float
    hit: bool

class ReplayStorage:
    def __init__(self, output_dir: str = "data/replay_results"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, audit_id: str, snapshot: Any, metrics: ReplayMetrics):
        data = {
            "audit_id": audit_id,
            "decision": snapshot.decision_result.decision,
            "confidence": snapshot.decision_result.confidence,
            "mae": metrics.mae,
            "mfe": metrics.mfe,
            "pl": metrics.pl,
            "hit": metrics.hit,
            "timestamp": snapshot.timestamp
        }
        with open(f"{self.output_dir}/{audit_id}.json", 'w') as f:
            json.dump(data, f, indent=4)
