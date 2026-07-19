from typing import List, Optional
from dataclasses import replace
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.market_context import MarketContext
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine
from mercury_ai.analysis.conflict_resolution_engine import ConflictResolutionEngine
from mercury_ai.utils.deterministic_clock import DeterministicClock

class EvidenceEngine:
    def __init__(self):
        self.quality_engine = EvidenceQualityEngine()
        self.conflict_resolver = ConflictResolutionEngine()

    def process(self, raw_evidences: List[Evidence], asset: str, timeframe: str, context: Optional[MarketContext] = None) -> MarketEvidenceBundle:
        # 1. Deduplicate
        deduplicated = self._deduplicate(raw_evidences)
        
        # 2. Normalize
        normalized = self._normalize(deduplicated)
        
        # 3. Quality Scored
        quality_scored = self.quality_engine.evaluate(normalized)
        
        # 4. Conflict Resolution
        resolved, conflict_score = self.conflict_resolver.resolve(quality_scored, context)
        
        # 5. Agreement Calculation
        agreement_score = self.calculate_agreement(resolved)
        
        return MarketEvidenceBundle(
            evidences=tuple(resolved),
            timestamp=DeterministicClock.utcnow().isoformat(),
            asset=asset,
            timeframe=timeframe
        )

    def compose(self, asset: str, timeframe: str, context: Optional[MarketContext], **evidence_lists: List[Evidence]) -> MarketEvidenceBundle:
        """
        Agrega evidências de múltiplas fontes e processa o bundle.
        """
        raw = []
        for e_list in evidence_lists.values():
            raw.extend(e_list)
        return self.process(raw, asset, timeframe, context)

    def _deduplicate(self, evidences: List[Evidence]) -> List[Evidence]:
        seen = set()
        deduped = []
        for e in evidences:
            key = (e.engine_name, e.evidence_name)
            if key not in seen:
                seen.add(key)
                deduped.append(e)
        return deduped

    def _normalize(self, evidences: List[Evidence]) -> List[Evidence]:
        normalized = []
        for e in evidences:
            # Ensure 0-100 bounds
            norm_e = replace(e,
                strength=max(0.0, min(100.0, e.strength)),
                confidence=max(0.0, min(100.0, e.confidence))
            )
            normalized.append(norm_e)
        return normalized

    def calculate_agreement(self, evidences: List[Evidence]) -> float:
        if not evidences: return 1.0
        bullish = sum(1 for e in evidences if e.direction == "BULLISH")
        bearish = sum(1 for e in evidences if e.direction == "BEARISH")
        total = len(evidences)
        return max(bullish, bearish) / total
