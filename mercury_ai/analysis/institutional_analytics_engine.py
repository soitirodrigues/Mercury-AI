import json
import os
from typing import Dict, Any
import pandas as pd

class InstitutionalAnalyticsEngine:
    def __init__(self, snapshot_dir: str = "mercury_ai/database/snapshots", replay_dir: str = "data/replay_results"):
        self.snapshot_dir = snapshot_dir
        self.replay_dir = replay_dir

    def _load_data(self) -> pd.DataFrame:
        data_records = []
        
        # Mapping audit_id to replay metrics
        replay_metrics = {}
        for filename in os.listdir(self.replay_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.replay_dir, filename), 'r') as f:
                    replay_metrics[filename.replace(".json", "")] = json.load(f)
        
        # Load snapshots and join with replay metrics
        for filename in os.listdir(self.snapshot_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.snapshot_dir, filename), 'r') as f:
                    snapshot = json.load(f)
                
                audit_id = snapshot['decision_result']['audit_id']
                if audit_id in replay_metrics:
                    metrics = replay_metrics[audit_id]
                    
                    # Flatten data
                    record = {
                        "audit_id": audit_id,
                        "asset": snapshot['asset'],
                        "timestamp": snapshot['timestamp'],
                        "decision": snapshot['decision_result']['decision'],
                        "score": snapshot['decision_result']['score'],
                        "confidence": snapshot['decision_result']['confidence'],
                        "evidences": [e['evidence_name'] for e in snapshot['evidence_bundle']['evidences']],
                        "engines": list(set([e['engine_name'] for e in snapshot['evidence_bundle']['evidences']])),
                        "hit": metrics['hit'],
                        "pl": metrics['pl']
                    }
                    data_records.append(record)
                    
        return pd.DataFrame(data_records)

    def generate_quality_report(self) -> Dict[str, Any]:
        df = self._load_data()
        if df.empty: return {"error": "No data available"}
        
        # Logic to answer the questions
        report = {
            "win_rate_per_asset": df.groupby('asset')['hit'].mean().to_dict(),
            "avg_score_by_hit": df.groupby('hit')['score'].mean().to_dict(),
            "engine_contribution": self._get_engine_contribution(df),
            "top_patterns": self._get_top_patterns(df)
        }
        return report

    def _get_engine_contribution(self, df: pd.DataFrame) -> Dict[str, float]:
        # Simple contribution: Win rate per engine
        engine_stats = {}
        all_engines = set(e for engines in df['engines'] for e in engines)
        for engine in all_engines:
            mask = df['engines'].apply(lambda x: engine in x)
            engine_stats[engine] = df[mask]['hit'].mean()
        return engine_stats

    def _get_top_patterns(self, df: pd.DataFrame) -> Dict[str, float]:
        # Simple pattern: Win rate per evidence set
        pattern_stats = {}
        # Convert list of evidences to tuple for grouping
        df['pattern'] = df['evidences'].apply(tuple)
        return df.groupby('pattern')['hit'].mean().nlargest(5).to_dict()
