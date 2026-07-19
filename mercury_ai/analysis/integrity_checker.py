from typing import List, Dict, Any
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
import re

class IntegrityChecker:
    """
    Camada de verificação de integridade institucional.
    """
    def __init__(self):
        self.logger = DecisionSnapshotLogger()
    
    def check_all(self) -> List[str]:
        issues = []
        for path in self.logger.list_snapshots():
            try:
                data = self.logger.load_snapshot(path)
                issues.extend(self._check_snapshot(data, path.name))
            except Exception as e:
                issues.append(f"File {path.name} corrupted: {e}")
        return issues

    def _check_snapshot(self, data: Dict[str, Any], filename: str) -> List[str]:
        errors = []
        # Mandatory fields
        mandatory = ['timestamp', 'asset', 'decision_result', 'session_id']
        for field in mandatory:
            if field not in data:
                errors.append(f"{filename}: Missing mandatory field {field}")
        
        if 'decision_result' in data:
            dr = data['decision_result']
            # Probability consistency
            buy = dr.get('buy_probability', 0)
            sell = dr.get('sell_probability', 0)
            wait = dr.get('wait_probability', 0)
            if not (99.0 <= (buy + sell + wait) <= 101.0):
                errors.append(f"{filename}: Inconsistent probability sum ({buy+sell+wait})")
            
            # Confidence validity
            conf = dr.get('confidence', -1)
            if not (0.0 <= conf <= 1.0):
                errors.append(f"{filename}: Invalid confidence range ({conf})")
                
            # Audit ID integrity
            audit_id = dr.get('audit_id', '')
            if audit_id != 'MARKET_CLOSED' and not re.match(r'^[a-f0-9]{64}$', str(audit_id)):
                errors.append(f"{filename}: Invalid audit_id format")
                
        return errors
