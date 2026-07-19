import json
import os
from typing import Dict, Any
from collections import defaultdict

class LearningEngine:
    """
    Motor de aprendizado institucional estatístico.
    Analisa snapshots e resultados para identificar padrões de performance.
    """
    def __init__(self, metrics_dir: str = "data/replay_results", snapshots_dir: str = "mercury_ai/database/snapshots"):
        self.metrics_dir = metrics_dir
        self.snapshots_dir = snapshots_dir

    def run_learning(self) -> Dict[str, Any]:
        # 1. Load context
        audit_to_context = {}
        for filename in os.listdir(self.snapshots_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.snapshots_dir, filename), 'r') as f:
                    snap = json.load(f)
                    audit_id = snap["decision_result"]["audit_id"]
                    audit_to_context[audit_id] = snap
                    
        # 2. Analyze
        stats = {
            "assets": defaultdict(lambda: {"wins": 0, "total": 0, "pl": 0.0}),
            "evidences": defaultdict(lambda: {"wins": 0, "total": 0, "pl": 0.0}),
        }
        
        for filename in os.listdir(self.metrics_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.metrics_dir, filename), 'r') as f:
                    m = json.load(f)
                
                ctx = audit_to_context.get(m["audit_id"])
                if ctx:
                    self._accumulate(stats, m, ctx)
        
        return self._finalize_stats(stats)

    def _accumulate(self, stats: Dict, m: Dict, ctx: Dict):
        # Asset Stats
        asset = ctx["asset"]
        s = stats["assets"][asset]
        s["total"] += 1
        s["pl"] += m["pl"]
        if m["hit"]: s["wins"] += 1
            
        # Evidence Stats
        for ev in ctx["evidence_bundle"]["evidences"]:
            e_key = f"{ev['engine_name']}:{ev['evidence_name']}"
            e = stats["evidences"][e_key]
            e["total"] += 1
            e["pl"] += m["pl"]
            if m["hit"]: e["wins"] += 1

    def _finalize_stats(self, stats: Dict) -> Dict[str, Any]:
        report = {}
        
        # Best/Worst Assets
        asset_perf = []
        for asset, data in stats["assets"].items():
            asset_perf.append({
                "asset": asset,
                "win_rate": data["wins"] / data["total"] if data["total"] > 0 else 0,
                "avg_pl": data["pl"] / data["total"]
            })
        report["best_assets"] = sorted(asset_perf, key=lambda x: x["win_rate"], reverse=True)[:5]
        
        # Best Evidences
        ev_perf = []
        for e_key, data in stats["evidences"].items():
            ev_perf.append({
                "evidence": e_key,
                "win_rate": data["wins"] / data["total"] if data["total"] > 0 else 0
            })
        report["most_accurate_evidences"] = sorted(ev_perf, key=lambda x: x["win_rate"], reverse=True)[:5]
        
        return report
