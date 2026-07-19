import json
from pathlib import Path
from dataclasses import asdict
from typing import List, Dict, Any
from functools import lru_cache
from mercury_ai.models.decision_snapshot import DecisionSnapshot

class DecisionSnapshotLogger:
    def __init__(self, base_path: str = "mercury_ai/database/snapshots"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, snapshot: DecisionSnapshot) -> DecisionSnapshot:
        filename = f"{snapshot.asset}_{snapshot.timestamp.replace(':', '-')}.json"
        filepath = self.base_path / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(asdict(snapshot), f, indent=4, default=str)
        return snapshot

    def list_snapshots(self) -> List[Path]:
        return sorted(list(self.base_path.glob("*.json")), reverse=True)

    @lru_cache(maxsize=128)
    def load_snapshot(self, snapshot_path: Path) -> Dict[str, Any]:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            return json.load(f)
