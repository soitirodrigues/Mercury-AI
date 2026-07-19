from dataclasses import dataclass

@dataclass(frozen=True)
class RiskAssessment:
    suggested_stop: float
    suggested_take_profit: float
    risk_reward_ratio: float
    expected_drawdown: float
    expected_volatility: float
    trade_quality: float
    max_exposure: float
    invalidation_point: float
    institutional_risk_score: float
