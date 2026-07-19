from typing import List, Tuple
import pandas as pd
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence

class ValidationEngine:
    """
    Camada final de validação institucional.
    """

    def validate_all(self, 
                     context: MarketContext, 
                     evidence_bundle: MarketEvidenceBundle) -> Tuple[bool, List[str]]:
        warnings = []
        
        # 1. Evidence Consistency
        if not self._validate_evidence_consistency(evidence_bundle.evidences):
            warnings.append("Evidence consistency failure")
            
        # 2. Context Consistency
        if not self._validate_context_consistency(context):
            warnings.append("Context consistency failure")
            
        return len(warnings) == 0, warnings

    def _validate_evidence_consistency(self, evidences: tuple[Evidence, ...]) -> bool:
        if not evidences: return True
        # Check for NaN in evidence attributes
        for e in evidences:
            if e.strength < 0 or e.strength > 100 or e.confidence < 0 or e.confidence > 100:
                return False
        return True

    def _validate_context_consistency(self, context: MarketContext) -> bool:
        if not context.market: return False
        return True
