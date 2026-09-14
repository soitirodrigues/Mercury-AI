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

    # --- Exit plan TP1+BE (propagado do RiskEngine; sem recalculo) ---
    take_profit_1r: float | None = None
    breakeven_trigger: float | None = None
    exit_plan: str = "TP1_50_BE_RUNNER_2R"

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
    # Flags SMC do forward (p/ gates automáticos; sem alterar decisão):
    # displacement=True => trigger N é vela de força (exigido p/ selo A);
    # exhausted=True => pavio oposto dominante/corpo raquítico (corta selo A/B).
    forward_displacement: bool = False
    forward_exhausted: bool = False

    # --- Sessão operacional (propagada de session_analysis; sem recalcular) ---
    # session_thin=True => liquidez<50 (SYDNEY fina): spread/slippage alto
    # na Hezilex — capa selo em C automaticamente (gate F8 automático).
    session: str = "UNKNOWN"
    session_liquidity: float | None = None
    session_thin: bool = False

    # --- Preditor da PRÓXIMA vela (SMC estrutural: topos/fundos; sem alterar decisão) ---
    # direction: BULLISH/BEARISH/NEUTRAL — para onde o preço VAI em N+1.
    # agrees: True concorda c/ decision | False discorda (gate G4) | None NEUTRAL/sem direção.
    next_direction: str = "NEUTRAL"
    next_confidence: float = 0.0
    next_reason: str = ""
    next_structure: str = "RANGE"
    next_key_level: float | None = None
    next_key_kind: str = "NONE"
    next_agrees: bool | None = None

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