import json
import os
import hashlib
from mercury_ai.models.decision_snapshot import DecisionSnapshot

class InstitutionalMemoryEngine:
    def __init__(self, memory_path: str = "data/institutional_memory.json"):
        self.memory_path = memory_path
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, 'w') as f:
                json.dump([], f)

    def _get_setup_key(self, asset: str, evidences: tuple) -> str:
        # Deterministic hash of setup
        setup = sorted([f"{e.engine_name}_{e.evidence_name}_{e.direction}" for e in evidences])
        return hashlib.sha256(f"{asset}_{'_'.join(setup)}".encode()).hexdigest()

    def get_consistency_score(self, asset: str, evidences: tuple) -> float:
        """
        Analisa o histórico e retorna um fator de reforço (-1.0 a 1.0).
        """
        setup_key = self._get_setup_key(asset, evidences)
        
        with open(self.memory_path, 'r') as f:
            memory = json.load(f)
            
        history = [m for m in memory if m['setup_key'] == setup_key]
        if not history:
            return 0.0
            
        outcomes = [m['outcome'] for m in history if 'outcome' in m]
        if not outcomes:
            return 0.0
            
        # Reforça sucesso, penaliza falha
        avg_outcome = sum(outcomes) / len(outcomes)
        
        # Penality for high variance (instability)
        variance = sum((o - avg_outcome)**2 for o in outcomes) / len(outcomes)
        
        return avg_outcome - (variance * 0.5)

    def record_decision(self, snapshot: DecisionSnapshot):
        setup_key = self._get_setup_key(snapshot.asset, snapshot.evidence_bundle.evidences)
        
        entry = {
            'setup_key': setup_key,
            'audit_id': snapshot.decision_result.audit_id,
            'asset': snapshot.asset,
            'decision': snapshot.decision_result.decision,
            'confidence': snapshot.decision_result.confidence,
            'timestamp': snapshot.timestamp
        }
        
        with open(self.memory_path, 'r+') as f:
            memory = json.load(f)
            memory.append(entry)
            f.seek(0)
            json.dump(memory, f, indent=4)

    def record_outcome(self, audit_id: str, outcome: float):
        with open(self.memory_path, 'r+') as f:
            memory = json.load(f)
            for entry in memory:
                if entry['audit_id'] == audit_id:
                    entry['outcome'] = outcome
            f.seek(0)
            json.dump(memory, f, indent=4)
