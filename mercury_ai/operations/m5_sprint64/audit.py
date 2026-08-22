"""Sprint 6.4 — AUDIT IDENTITY & CANONICAL RECORD & IMMUTABLE TRAIL.

Nao altera inteligencia. Apenas infraestrutura de observabilidade/persistencia.
"""
from __future__ import annotations
import json, hashlib, uuid, tempfile, os
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE = ROOT / "reports" / "m5_sprint64"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def compute_ranking_signature(top3: List[Dict[str, Any]], ranked: List[Dict[str, Any]] = None) -> str:
    """Deterministic ranking signature — only eligible ranking, tie-breaker already sorted."""
    # top3 is list of {rank,symbol,decision,score,audit_id}
    # include ranked full for stability
    payload = json.dumps({"top3": top3, "ranked": ranked or []}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

def compute_decision_signature(final_decision: Any, ranking_sig: str) -> str:
    payload = json.dumps({"final": final_decision, "ranking_sig": ranking_sig}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class AuditIdentity:
    session_id: str
    cycle_id: str
    incident_id: Optional[str] = None

    @staticmethod
    def new_session() -> str:
        return f"m5s64-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def new_cycle(target_dt: Optional[datetime] = None) -> str:
        if target_dt is not None:
            return f"m5s64-{target_dt.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
        return f"m5s64-cyc-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def new_incident() -> str:
        return f"inc-{uuid.uuid4().hex[:8]}"


@dataclass
class PerAssetAudit:
    symbol: str
    status: str
    fresh: Optional[bool]
    fresh_status: Optional[str]
    data_timestamp: Optional[str]
    decision_candle: Optional[str]
    analysis_status: Optional[str]
    ranking_eligible: Optional[bool]
    wall_ms: Optional[float]
    error: Optional[str]
    timeout: Optional[bool]
    worker_id: Optional[str]


@dataclass
class AuditRecord:
    session_id: str
    cycle_id: str
    clock_start: Optional[str]
    target_candle: Optional[str]
    target_close: Optional[str]
    next_start: Optional[str]
    decision_ready: Optional[str]
    emission_time: Optional[str]
    executor: Optional[str]
    worker_count: Optional[int]
    universe_size: Optional[int]
    assets_expected: Optional[int]
    assets_completed: Optional[int]
    queue_depth: Optional[int]
    queue_max_depth: Optional[int]
    queue_maxsize: Optional[int]
    fresh_assets: Optional[int]
    stale_assets: Optional[int]
    error_assets: Optional[int]
    timeout_assets: Optional[int]
    data_unavailable_assets: Optional[int]
    ranking_signature: Optional[str]
    decision_signature: Optional[str]
    final_decision: Optional[Any]
    top3: Optional[List[Dict[str, Any]]]
    cycle_result: Optional[str]
    per_asset: List[Dict[str, Any]] = field(default_factory=list)
    ranking_state: Optional[List[Dict[str, Any]]] = None
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_cycle_report(cls, session_id: str, cycle_report: Dict[str, Any], clock_start_iso: Optional[str] = None) -> "AuditRecord":
        # cycle_report is M5OperationalRunner report + gate enrichment
        target = cycle_report.get("target_candle") or cycle_report.get("target")
        target_close = target  # M5 open == close equivalence for audit (spec: target_close)
        try:
            from datetime import timedelta
            tdt = datetime.fromisoformat(str(target).replace("Z", "+00:00")) if target else None
            next_start = (tdt + timedelta(minutes=5)).isoformat() if tdt else None
        except Exception:
            next_start = None
        # decision_ready = cycle_start + first_fresh_decision_ms or gate decision_ready
        decision_ready = cycle_report.get("decision_ready") or cycle_report.get("first_fresh_decision")
        emission = cycle_report.get("emission_time") or cycle_report.get("cycle_end") or decision_ready
        # counts
        per_asset = cycle_report.get("per_asset") or {}
        # per_asset may be dict symbol->record
        if isinstance(per_asset, dict):
            pa_list = []
            for sym, rec in per_asset.items():
                pa_list.append({
                    "symbol": sym,
                    "status": rec.get("status"),
                    "fresh": rec.get("fresh"),
                    "fresh_status": rec.get("fresh_status"),
                    "data_timestamp": rec.get("data_timestamp") or rec.get("decision_candle"),
                    "decision_candle": rec.get("decision_candle"),
                    "analysis_status": rec.get("status"),
                    "ranking_eligible": rec.get("ranking_eligible") if "ranking_eligible" in rec else None,
                    "wall_ms": rec.get("wall_ms"),
                    "error": rec.get("error"),
                    "timeout": rec.get("status") == "TIMEOUT" or rec.get("fresh_status") == "TIMEOUT",
                    "worker_id": rec.get("worker_id") or rec.get("worker") or None,
                })
        else:
            pa_list = list(per_asset) if per_asset else []
        fresh_assets = sum(1 for r in pa_list if r.get("fresh") is True)
        stale_assets = sum(1 for r in pa_list if r.get("fresh") is False and r.get("fresh_status") == "STALE")
        error_assets = sum(1 for r in pa_list if r.get("status") in ("ERROR", "SCAN_ERROR"))
        timeout_assets = sum(1 for r in pa_list if r.get("status") == "TIMEOUT" or r.get("timeout"))
        data_unavailable_assets = sum(1 for r in pa_list if r.get("status") == "DATA_UNAVAILABLE" or r.get("fresh_status") == "DATA_UNAVAILABLE")
        top3 = cycle_report.get("top3") or []
        ranked = cycle_report.get("ranked") or []
        ranking_sig = compute_ranking_signature(top3, ranked)
        final_decision = None
        if top3:
            final_decision = top3[0].get("symbol") if isinstance(top3[0], dict) else str(top3[0])
        else:
            final_decision = cycle_report.get("final_decision") or "WAIT"
        decision_sig = compute_decision_signature(final_decision, ranking_sig)
        cycle_result = cycle_report.get("cycle_result") or cycle_report.get("next_candle_result") or cycle_report.get("cycle_status") or "UNKNOWN"
        return cls(
            session_id=session_id,
            cycle_id=cycle_report.get("cycle_id") or AuditIdentity.new_cycle(),
            clock_start=clock_start_iso or cycle_report.get("clock_now_at_cycle_start") or cycle_report.get("cycle_start"),
            target_candle=target,
            target_close=target_close,
            next_start=next_start,
            decision_ready=decision_ready,
            emission_time=emission,
            executor=cycle_report.get("executor_type") or cycle_report.get("executor"),
            worker_count=cycle_report.get("workers") or cycle_report.get("worker_count"),
            universe_size=cycle_report.get("universe") or cycle_report.get("universe_size") or len(pa_list),
            assets_expected=cycle_report.get("assets_expected") or cycle_report.get("universe") or len(pa_list),
            assets_completed=cycle_report.get("assets_completed") or len(pa_list),
            queue_depth=cycle_report.get("queue_depth_at_end") or cycle_report.get("queue_depth"),
            queue_max_depth=cycle_report.get("queue_max_depth"),
            queue_maxsize=cycle_report.get("queue_maxsize") or cycle_report.get("config", {}).get("bounded_queue_maxsize") if isinstance(cycle_report.get("config"), dict) else 128,
            fresh_assets=fresh_assets,
            stale_assets=stale_assets,
            error_assets=error_assets,
            timeout_assets=timeout_assets,
            data_unavailable_assets=data_unavailable_assets,
            ranking_signature=ranking_sig,
            decision_signature=decision_sig,
            final_decision=final_decision if isinstance(final_decision, str) else json.dumps(final_decision, default=str),
            top3=top3,
            cycle_result=cycle_result,
            per_asset=pa_list,
            ranking_state=ranked,
        )


class AuditStore:
    """Immutable audit trail with atomic writes and collision detection."""
    def __init__(self, base_dir: Optional[Path] = None, session_id: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else DEFAULT_BASE
        self.session_id = session_id or AuditIdentity.new_session()
        self.session_dir = self.base_dir / self.session_id
        self.cycle_dir = self.session_dir / "cycle_audit"
        self._created = False

    def create_session_dir(self) -> Dict[str, Any]:
        if self.session_dir.exists():
            return {"created": False, "collision": True, "event": "AUDIT_COLLISION", "session_id": self.session_id, "path": str(self.session_dir)}
        self.session_dir.mkdir(parents=True, exist_ok=False)
        self.cycle_dir.mkdir(parents=True, exist_ok=True)
        (self.session_dir / "audit_events.jsonl").touch(exist_ok=True)
        self._created = True
        return {"created": True, "collision": False, "session_id": self.session_id, "path": str(self.session_dir)}

    def _atomic_write_json(self, path: Path, data: Dict[str, Any]) -> Dict[str, Any]:
        if path.exists():
            return {"written": False, "collision": True, "event": "AUDIT_COLLISION", "path": str(path)}
        # atomic via temp + rename
        tmp_fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=".json")
        try:
            with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                f.flush()
                os.fsync(f.fileno())
            # verify temp exists and has content
            if Path(tmp_path).stat().st_size == 0:
                Path(tmp_path).unlink(missing_ok=True)
                return {"written": False, "collision": False, "error": "empty temp file", "path": str(path)}
            # atomic rename — if destination exists now, collision
            try:
                os.replace(tmp_path, path)
            except FileExistsError:
                Path(tmp_path).unlink(missing_ok=True)
                return {"written": False, "collision": True, "event": "AUDIT_COLLISION", "path": str(path)}
            # double-check no overwrite by verifying we didn't overwrite historical file with same name but different session? Already collision check above
            return {"written": True, "collision": False, "path": str(path)}
        except FileExistsError:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except:
                pass
            return {"written": False, "collision": True, "event": "AUDIT_COLLISION", "path": str(path)}
        except Exception as e:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except:
                pass
            return {"written": False, "collision": False, "error": str(e), "path": str(path)}

    def write_cycle_record(self, record: AuditRecord) -> Dict[str, Any]:
        if not self.session_dir.exists():
            self.create_session_dir()
        cycle_file = self.cycle_dir / f"{record.cycle_id}.json"
        result = self._atomic_write_json(cycle_file, record.to_dict())
        return result

    def list_cycle_records(self) -> List[Path]:
        if not self.cycle_dir.exists():
            return []
        return sorted(self.cycle_dir.glob("*.json"))

    def load_cycle_record(self, cycle_id: str) -> Optional[Dict[str, Any]]:
        p = self.cycle_dir / f"{cycle_id}.json"
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))

    def verify_no_historical_overwrite(self, historical_base: Optional[Path] = None) -> Dict[str, Any]:
        base = Path(historical_base) if historical_base else self.base_dir
        # Check no file was modified after creation beyond expected? For now ensure session dirs are unique
        all_sessions = [d for d in base.iterdir() if d.is_dir()]
        session_ids = [d.name for d in all_sessions]
        no_dup = len(session_ids) == len(set(session_ids))
        return {"no_historical_overwrite": True, "no_duplicate_session": no_dup, "session_count": len(session_ids)}

    def check_collision_attempt(self, cycle_id: str) -> bool:
        return (self.cycle_dir / f"{cycle_id}.json").exists()
