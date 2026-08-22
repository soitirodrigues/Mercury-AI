"""Sprint 6.4 — DECISION PROVENANCE."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

@dataclass
class DecisionProvenance:
    session_id: str
    cycle_id: str
    target_candle: Optional[str]
    target_close: Optional[str]
    next_start: Optional[str]
    assets_participated: List[str]
    assets_failed: List[str]
    fresh_assets: List[str]
    stale_assets: List[str]
    ranking_signature: Optional[str]
    decision_signature: Optional[str]
    top3: Optional[List[Dict[str, Any]]]
    final_decision: Optional[str]
    audit_record_path: Optional[str]
    manifest_path: Optional[str]
    event_stream_path: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_audit_record(record: Dict[str, Any], manifest_path: Optional[str]=None, event_stream_path: Optional[str]=None) -> "DecisionProvenance":
        per_asset = record.get("per_asset") or []
        participated = [r.get("symbol") for r in per_asset if r.get("symbol")]
        failed = [r.get("symbol") for r in per_asset if r.get("status") in ("ERROR","SCAN_ERROR","TIMEOUT") or r.get("error")]
        fresh = [r.get("symbol") for r in per_asset if r.get("fresh") is True]
        stale = [r.get("symbol") for r in per_asset if r.get("fresh_status")=="STALE"]
        return DecisionProvenance(
            session_id=record.get("session_id"),
            cycle_id=record.get("cycle_id"),
            target_candle=record.get("target_candle"),
            target_close=record.get("target_close"),
            next_start=record.get("next_start"),
            assets_participated=participated,
            assets_failed=failed,
            fresh_assets=fresh,
            stale_assets=stale,
            ranking_signature=record.get("ranking_signature"),
            decision_signature=record.get("decision_signature"),
            top3=record.get("top3"),
            final_decision=str(record.get("final_decision")),
            audit_record_path=None,
            manifest_path=manifest_path,
            event_stream_path=event_stream_path,
        )

    def is_complete(self) -> bool:
        return bool(self.session_id and self.cycle_id and self.target_candle and self.ranking_signature and self.decision_signature)
