from dataclasses import dataclass, field
from typing import Tuple, Optional
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.version_metadata import VersionMetadata
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.config import settings

@dataclass(frozen=True)
class DecisionSnapshot:
    """
    Immutable snapshot for full decision replay.
    """
    timestamp: str
    asset: str
    timeframe: str
    context: MarketContext
    evidence_bundle: MarketEvidenceBundle
    decision_result: DecisionResult
    version_metadata: VersionMetadata
    audit_events: Tuple[str, ...]
    session_id: str
    evidence_ranking: Optional[EvidenceRankingResult] = None
    version: str = field(default_factory=lambda: settings.VERSION)
