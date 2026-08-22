"""Estado incremental por ativo — AssetScanState.

Não duplica DecisionResult. Apenas aponta para o resultado oficial
produzido pelo pipeline e guarda metadados de freshness/rastreabilidade.

Campos obrigatórios conforme spec:
  symbol, last_data_timestamp, last_decision_timestamp,
  last_decision_result (referência), last_audit_id, last_scan_duration,
  status, is_fresh, updated_at

Plus temporais:
  decision_candle_timestamp (open da vela M5 que gerou a decisão)
  data_latest_timestamp    (df.index[-1] real usado)
  decision_age_seconds     (now - decision_timestamp)
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Any, Dict


FRESH_STATES = {"FRESH"}
STALE_STATES = {"STALE", "STALE_CACHED"}
UNAVAILABLE_STATES = {"DATA_UNAVAILABLE", "PIPELINE_ERROR", "INSUFFICIENT_DATA", "MARKET_CLOSED", "SCAN_ERROR", "DATA_QUALITY_FAIL"}
ALL_STATES = FRESH_STATES | STALE_STATES | UNAVAILABLE_STATES | {"UNKNOWN", "PENDING", "PROCESSING"}


@dataclass
class AssetScanState:
    """Estado incremental por ativo (leve, sem duplicar DecisionResult)."""

    symbol: str
    timeframe: str = "M5"

    # Temporais (UTC aware ISO strings para serialização; objetos datetime em memória)
    decision_candle_timestamp: Optional[str] = None  # open da vela M5 que gerou a decisão (ISO UTC)
    data_latest_timestamp: Optional[str] = None      # df.index[-1] real (ISO UTC)
    decision_timestamp: Optional[str] = None         # quando a decisão foi tomada (DecisionSnapshot.timestamp)
    updated_at: Optional[str] = None                 # última atualização deste estado (ISO UTC)

    # Referências ao pipeline oficial (não duplica DecisionResult)
    last_audit_id: Optional[str] = None
    last_decision: Optional[str] = None              # BUY / SELL / WAIT / None
    last_grade: Optional[str] = None
    last_confidence: Optional[float] = None
    last_confluence: Optional[float] = None

    # Métricas operacionais
    last_scan_duration_ms: Optional[float] = None
    scan_count: int = 0
    consecutive_failures: int = 0

    # Status de freshness
    # Valores: FRESH | STALE | DATA_UNAVAILABLE | PIPELINE_ERROR | MARKET_CLOSED | INSUFFICIENT_DATA | SCAN_ERROR | PENDING | PROCESSING
    status: str = "PENDING"
    is_fresh: bool = False

    # Rastreabilidade
    last_error: Optional[str] = None
    decision_age_seconds: Optional[float] = None

    # Cache tracking
    cache_status: Optional[str] = None  # CACHE_HIT / CACHE_MISS / CACHE_STALE / CACHE_REFRESH / None

    # Snapshot file produzido
    snapshot_file: Optional[str] = None

    # Guardar DecisionResult por referência leve (não serializado em JSON por padrão)
    # Preenchido em memória pelo scanner; _result_ref não vai para disco
    _result_ref: Any = field(default=None, repr=False, compare=False)

    def to_dict(self) -> Dict[str, Any]:
        """Serialização para JSON (sem _result_ref)."""
        d = asdict(self)
        d.pop("_result_ref", None)
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AssetScanState":
        d = dict(d)
        d.pop("_result_ref", None)
        # Tolerar campos extras
        allowed = {f.name for f in cls.__dataclass_fields__.values() if f.name != "_result_ref"}
        filtered = {k: v for k, v in d.items() if k in allowed}
        return cls(**filtered)

    def mark_processing(self) -> None:
        self.status = "PROCESSING"
        self.is_fresh = False
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def mark_error(self, audit_id: str, error: Optional[str] = None) -> None:
        self.last_audit_id = audit_id
        self.last_error = error
        self.status = audit_id if audit_id in ALL_STATES else "DATA_UNAVAILABLE"
        if self.status not in ALL_STATES:
            self.status = "DATA_UNAVAILABLE"
        self.is_fresh = False
        self.consecutive_failures += 1
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def is_terminal_unavailable(self) -> bool:
        return self.status in UNAVAILABLE_STATES

    def is_stale(self) -> bool:
        return self.status in STALE_STATES or (not self.is_fresh and self.status == "FRESH")

    def age_seconds(self, now: Optional[datetime] = None) -> Optional[float]:
        if self.decision_timestamp is None:
            return None
        try:
            dt = datetime.fromisoformat(self.decision_timestamp.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if now is None:
                now = datetime.now(timezone.utc)
            if now.tzinfo is None:
                now = now.replace(tzinfo=timezone.utc)
            return (now - dt).total_seconds()
        except Exception:
            return None
