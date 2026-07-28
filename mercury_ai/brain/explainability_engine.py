from typing import Tuple
from mercury_ai.models.analysis_result import AnalysisResult
from mercury_ai.models.direction import AnalysisDirection
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.probability_result import ProbabilityResult
from mercury_ai.models.trading_explanation import TradingExplanation

class ExplainabilityEngine:
    """
    Motor institucional para geração de explicações de trading determinísticas.
    """

    def analyze(self, prob: ProbabilityResult, conf: ConfluenceResult, analyses: Tuple[AnalysisResult, ...]) -> TradingExplanation:
        
        bullish = []
        bearish = []
        neutral = []
        
        for res in analyses:
            desc = f"{res.engine_name}: {res.direction.value} (Confidence: {res.confidence:.2f})"
            if res.direction == AnalysisDirection.BUY:
                bullish.append(desc)
            elif res.direction == AnalysisDirection.SELL:
                bearish.append(desc)
            else:
                neutral.append(desc)

        conflicts = [f"Signal conflict detected between engines" for _ in range(1) if conf.conflicting_signals]

        # Determine the dominant probability based on the dominant direction
        prob_val = prob.buy_probability if conf.dominant_direction == AnalysisDirection.BUY else \
                   prob.sell_probability if conf.dominant_direction == AnalysisDirection.SELL else \
                   prob.neutral_probability

        summary = f"Trading {conf.dominant_direction.value} with {prob_val:.1f}% probability."
        
        risk = f"Risk factor: {prob.expected_risk:.2f}. Class: {prob.opportunity_grade}."
        
        context = f"Confluence agreement: {conf.agreement_percentage:.1f}% across {conf.independent_confirmations} engines."

        conf_expl = f"Confidence level {prob_val:.1f}% based on confluence of {conf.independent_confirmations} signals."

        return TradingExplanation(
            exec_summary=summary,
            decision_rationale="Explained by ExplainabilityEngine",            market_context="Market context analyzed by pipeline",
            trend_context="Trend context analyzed by pipeline",
            liquidity_context="Liquidity context analyzed by pipeline",
            structure_context="Structure context analyzed by pipeline",
            momentum_context="Momentum analyzed by pipeline",
            volume_context="Volume analyzed by pipeline",
            smart_money_context="SMC analyzed by pipeline",
            confluence_context="Confluence analyzed by pipeline",
            risk_assessment=risk,
            confidence_rationale=conf_expl,            bullish_factors=tuple(bullish),
            bearish_factors=tuple(bearish),
            neutral_factors=tuple(neutral),
            conflicts=tuple(conflicts),
            engine_weights={res.engine_name: res.confidence for res in analyses},
            logical_sequence=("Evidence Analysis", "Confluence Evaluation", "Decision Formulation"),
            risk_analysis=risk,
            institutional_context=context,
            suggested_entry=0.0,
            suggested_stop=0.0,
            suggested_targets=(),
            confidence_explanation=conf_expl,
            machine_readable={},
        )
