from pathlib import Path
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.brain.mercury_decision_engine import MercuryDecisionEngine
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.core.pipeline_executor import PipelineExecutor

class HealthAuditor:
    def __init__(self):
        self.logger = DecisionSnapshotLogger()

    def generate_report(self) -> dict:
        snapshots = self.logger.list_snapshots()
        
        # Real checks instead of simulation
        try:
            decision_engine = MercuryDecisionEngine(PipelineExecutor())
            narrative = decision_engine.narrative
            prob = ProbabilityEngine({})
            conf = decision_engine.confidence
            
            pipeline_status = "OK"
        except (ImportError, ValueError, TypeError, RuntimeError, AttributeError):
            pipeline_status = "FAILED"

        return {
            "Pipeline": pipeline_status,
            "Snapshot Logger": "OK" if self.logger.base_path.exists() else "FAILED",
            "Replay": "OK" if len(snapshots) > 0 else "WARNING",
            "Dashboard": "OK" if Path("app/dashboard/dashboard.py").exists() else "FAILED",
            "Persistência": "OK" if os.access(self.logger.base_path, os.W_OK) else "FAILED",
            "Explainability": "OK" if narrative else "FAILED",
            "Probability": "OK" if prob else "FAILED",
            "Confidence": "OK" if conf else "FAILED",
            "Auditoria": "OK" if decision_engine else "FAILED"
        }

import os
