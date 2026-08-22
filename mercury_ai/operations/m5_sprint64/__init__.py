"""M5 Sprint 6.4 — AUDITABILITY, OBSERVABILITY & REPLAY INTEGRITY.

Regra Zero: nao altera DecisionResolverEngine/MercuryDecisionEngine/ranking/pesos/
probabilities/confidence/confluence/Top3/DQ/MTF/universe/AnalysisPipeline.
Apenas infraestrutura de audit/artifact/replay/observability.
"""
from .audit import AuditRecord, AuditStore, AuditIdentity
from .artifact import ArtifactManifest, ArtifactIntegrityResult, sha256_file, sha256_bytes
from .events import EventStream, EventType, EventOrderValidator, VALID_ORDER
from .replay import ReplayEngine, ReplayResult
from .provenance import DecisionProvenance

__all__ = [
    "AuditRecord", "AuditStore", "AuditIdentity",
    "ArtifactManifest", "ArtifactIntegrityResult", "sha256_file", "sha256_bytes",
    "EventStream", "EventType", "EventOrderValidator", "VALID_ORDER",
    "ReplayEngine", "ReplayResult",
    "DecisionProvenance",
]
