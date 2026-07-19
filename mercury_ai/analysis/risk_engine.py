from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine

class RiskEngine:
    """
    Motor central e único para análise de risco institucional.
    """
    def __init__(self):
        self.quality = EvidenceQualityEngine()

    def assess(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> RiskAssessment:
        # 1. Deterministic Metrics from Evidence/Context
        atr = context.market.atr
        price = context.market.close
        
        # Invalidation (fallback to 1% range if structure data is unavailable)
        invalidation = price * 0.99 if context.smart_money.structure.trend == "BULLISH" else price * 1.01
        
        # Stop/TP/RR
        stop = invalidation
        reward_dist = (price - stop) * 2.0
        tp = price + reward_dist
        rr = reward_dist / abs(price - stop) if abs(price - stop) > 0 else 0.0
        
        # Drawdown/Volatility
        drawdown = next((e.strength for e in evidence_bundle.evidences if e.engine_name == "VolatilityEngine"), 5.0)
        volatility = atr / price * 100 if price > 0 else 0.0
        
        # Quality
        quality_res = self.quality.evaluate(list(evidence_bundle.evidences))
        quality_score = sum(e.quality_score for e in quality_res) / len(quality_res) if quality_res else 50.0
        
        # Institutional Risk Score
        risk_score = 100 - (quality_score * 0.5 + min(rr * 10, 50))
        
        return RiskAssessment(
            suggested_stop=float(stop),
            suggested_take_profit=float(tp),
            risk_reward_ratio=float(rr),
            expected_drawdown=float(drawdown),
            expected_volatility=float(volatility),
            trade_quality=float(quality_score),
            max_exposure=0.02, # 2% default risk
            invalidation_point=float(invalidation),
            institutional_risk_score=float(risk_score)
        )
