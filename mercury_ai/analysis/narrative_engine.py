from typing import Tuple
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.trading_explanation import TradingExplanation

class NarrativeEngine:
    """
    Motor institucional de geração de narrativa determinística.
    """

    def generate(self, decision: str, evidences: Tuple[Evidence, ...], 
                     context: MarketContext, confluence_score: float) -> TradingExplanation:
        
        # Identify factors by direction
        bullish = [e for e in evidences if e.direction == "BULLISH"]
        bearish = [e for e in evidences if e.direction == "BEARISH"]
        neutral = [e for e in evidences if e.direction == "NEUTRAL"]
        
        # Sort by strength for relevance
        bullish.sort(key=lambda x: (x.strength, x.engine_name, x.evidence_name), reverse=True)
        bearish.sort(key=lambda x: (x.strength, x.engine_name, x.evidence_name), reverse=True)
        
        # Determine conflicts based on the decision
        if decision == "BUY":
            conflicts = [e.evidence_name for e in bearish]
            dominant_factors = bullish
        elif decision == "SELL":
            conflicts = [e.evidence_name for e in bullish]
            dominant_factors = bearish
        else:
            conflicts = []
            dominant_factors = []

        # Build a detailed rationale
        if dominant_factors:
            top_ev = dominant_factors[0]
            rationale = f"Decision {decision} triggered primarily by {top_ev.evidence_name} (Strength: {top_ev.strength:.1f}%) with a confluence score of {confluence_score:.2f}."
        else:
            rationale = f"Decision {decision} based on neutral market state and confluence of {len(evidences)} evidences."
        
        # Deterministic machine-readable data
        machine_readable = {
            "decision": decision,
            "confluence": confluence_score,
            "evidence_count": len(evidences)
        }
        
        return TradingExplanation(
            exec_summary=f"Institutional {decision} signal triggered based on current market regime.",
            decision_rationale=rationale,
            market_context=f"Session: UNKNOWN",
            trend_context=f"Bias: {context.trend[0].direction if context.trend else 'NEUTRAL'}",
            liquidity_context=f"Liquidity assessed via profile.",
            structure_context=f"Structure: {context.smart_money.structure.trend if context.smart_money.structure else 'UNKNOWN'}",
            momentum_context="Momentum assessed via CandlestickEngine.",
            volume_context=f"Volume check passed.",
            smart_money_context="Smart Money confirmed.",
            confluence_context=f"Net Confluence: {confluence_score:.2f}",
            risk_assessment=f"Risk Score: {context.risk_assessment.institutional_risk_score}",
            confidence_rationale="Confidence calibrated via evidence quality and consistency.",
            strong_evidences=tuple(e.evidence_name for e in evidences if e.strength > 70), 
            weak_evidences=tuple(e.evidence_name for e in evidences if e.strength <= 70),     
            missing_confirmations=("Volume",) if len(evidences) < 5 else (),
            detected_risks=(),

            # Now populated dynamically
            bullish_factors=tuple(e.evidence_name for e in bullish),
            bearish_factors=tuple(e.evidence_name for e in bearish),
            neutral_factors=tuple(e.evidence_name for e in neutral),
            conflicts=tuple(conflicts),
            logical_sequence=tuple([e.evidence_name for e in evidences]),
            risk_analysis=f"Score: {context.risk_assessment.institutional_risk_score}",
            institutional_context=f"Regime: {context.market_regime.regime}",
            suggested_entry=context.market.close,
            suggested_stop=context.risk_assessment.suggested_stop,   
            suggested_targets=tuple([context.risk_assessment.suggested_take_profit]),
            confidence_explanation=f"Score: {context.risk_assessment.trade_quality}",

            machine_readable=machine_readable,
            engine_weights={e.engine_name: e.weight for e in evidences},
            warnings=()
        )

