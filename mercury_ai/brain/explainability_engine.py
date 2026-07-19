from typing import Tuple
from mercury_ai.models.analysis_result import AnalysisResult, AnalysisDirection
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

        summary = f"Trading {conf.dominant_direction.value} with {prob.probability:.1f}% probability."
        
        risk = f"Risk factor: {prob.risk_factor:.2f}. Class: {prob.probability_class}."
        
        context = f"Confluence agreement: {conf.agreement_percentage:.1f}% across {conf.independent_confirmations} engines."

        conf_expl = f"Confidence level {prob.probability:.1f}% based on confluence of {conf.independent_confirmations} signals."

        return TradingExplanation(
            exec_summary=summary,
            decision_rationale="Explained by ExplainabilityEngine",
            bullish_factors=tuple(bullish),
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
