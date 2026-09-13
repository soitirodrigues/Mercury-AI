from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME


@dataclass(frozen=True)
class Signal:
    """
    SIGNAL operacional formal (S33-E.6).

    Completa o contrato existente em vez de criar um segundo modelo.
    PROPAGACAO pura: nenhum campo aqui altera thresholds/pesos/engines.
    Campos legados (asset/action/entry/explanation) preservados para
    compatibilidade; symbol/decision/entry_price sao aliases operacionais.

    ENTRY WINDOW RULE (derivada de signal_ts/last_m5_ts/next_m5_ts):
    next_m5_ts = strict ceil M5 apos last_m5_ts; VALID sse
    signal_ts < next_m5_ts (janela [signal_ts, next_m5_ts), seconds > 0),
    EXPIRED caso contrario (protecao contra falso timing).
    """

    asset: str

    action: str

    confidence: float

    score: float

    entry: float | None = None

    stop_loss: float | None = None

    take_profit: float | None = None

    timeframe: str = DEFAULT_TIMEFRAME

    strategy: str = ""

    evidences: Tuple[str, ...] = field(default_factory=tuple)

    explanation: str = ""

    # --- S33-E.6: identidade/temporal (operacional) ---
    signal_id: str = ""
    signal_ts: Optional[str] = None
    last_m5_ts: Optional[str] = None
    next_m5_ts: Optional[str] = None
    entry_price: float | None = None
    entry_window_start: Optional[str] = None
    entry_window_end: Optional[str] = None
    entry_window_seconds: float = 0.0
    seconds_to_next_m5: Optional[float] = None
    entry_valid_for_next_m5: bool = False
    entry_timing_state: str = "EXPIRED"

    # --- S33-E.6: risco (propagado do RiskEngine, sem recalculo) ---
    invalidation: float | None = None
    risk_reward: float = 0.0

    # --- S33-E.6: decisao (propagada, sem alterar regras) ---
    probability_buy: float = 0.0
    probability_sell: float = 0.0
    probability_wait: float = 0.0
    confluence: float = 0.0
    quality: float = 0.0
    institutional_score: float = 0.0
    grade: str = "N/A"
    mtf_summary: Dict[str, Any] = field(default_factory=dict)
    market_regime: str = "UNKNOWN"
    reason: str = ""
    audit_id: str = ""

    # --- Forward-bias M5 (classificação p/ PRÓXIMA vela; sem alterar decisão) ---
    forward_state: str = "EXPIRED"
    forward_reason: str = ""
    forward_direction: str = "NONE"

    @property
    def symbol(self) -> str:
        """Alias operacional: symbol == asset (contrato S33-E.6)."""
        return self.asset

    @property
    def decision(self) -> str:
        """Alias operacional: decision == action (contrato S33-E.6)."""
        return self.action

    @property
    def valid_for_next_m5(self) -> bool:
        """Alias legivel da validade temporal."""
        return self.entry_valid_for_next_m5

    def to_dict(self) -> Dict[str, Any]:
        """Serializa TODOS os campos (nenhum campo critico some)."""
        data = asdict(self)
        # aliases operacionais exigidos pelo contrato (transportaveis)
        data["symbol"] = self.asset
        data["decision"] = self.action
        return data