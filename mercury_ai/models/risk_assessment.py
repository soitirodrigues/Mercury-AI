from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

@dataclass(frozen=True)
class RiskAssessment:
    """Avaliação completa de risco institucional (Bloco 4 Enhanced)."""
    # --- Campos originais (Bloco 1-3) ---
    suggested_stop: float
    suggested_take_profit: float
    risk_reward_ratio: float
    expected_drawdown: float
    expected_volatility: float
    trade_quality: float
    max_exposure: float
    invalidation_point: float
    institutional_risk_score: float

    # --- Bloco 4: Value at Risk ---
    var_95: float = 0.0           # Value at Risk paramétrico (95% confiança)
    var_99: float = 0.0           # Value at Risk paramétrico (99% confiança)
    cvar_95: float = 0.0          # Conditional VaR / Expected Shortfall (95%)

    # --- Bloco 4: Kelly Criterion ---
    kelly_fraction: float = 0.0   # Fração ótima de Kelly (full)
    kelly_half: float = 0.0       # Half-Kelly (mais conservador)
    kelly_quarter: float = 0.0    # Quarter-Kelly (ultra conservador)

    # --- Bloco 4: Correlation & Stress ---
    correlation_matrix: Optional[Tuple[Tuple[float, ...], ...]] = None  # Matriz de correlação entre ativos
    stress_test_loss: float = 0.0  # Perda estimada no pior cenário de stress
