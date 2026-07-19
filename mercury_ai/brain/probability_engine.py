from typing import Dict, Any, Optional
from mercury_ai.models.probability_result import ProbabilityResult


class ProbabilityEngine:

    """
    Motor institucional de probabilidade Mercury AI.
    Converte confluência + contexto em decisão operacional.
    """

    def __init__(self, weights: Dict[str, float]):
        self.weights = weights


    def analyze(
        self,
        context: Any,
        evidence_bundle: Any,
        confluence_score: float,
        confidence_score: float,
        dominant_direction: Optional[str] = None
    ) -> ProbabilityResult:


        if not dominant_direction:

            bullish = sum(
                1 for e in evidence_bundle.evidences
                if e.direction == "BULLISH"
            )

            bearish = sum(
                1 for e in evidence_bundle.evidences
                if e.direction == "BEARISH"
            )


            if bullish > bearish:
                dominant_direction = "BUY"

            elif bearish > bullish:
                dominant_direction = "SELL"

            else:
                dominant_direction = "NEUTRAL"



        risk_score = (
            context
            .risk_assessment
            .institutional_risk_score
        )


        risk_factor = risk_score / 100



        evidence_bonus = min(
            len(evidence_bundle.evidences) * 5,
            25
        )


        probability = (
            confluence_score
            +
            evidence_bonus
            +
            (confidence_score * 0.2)
        )


        probability *= (
            1 - risk_factor
        )


        probability = max(
            0,
            min(
                probability,
                95
            )
        )



        if probability >= 75:

            grade = "A"
            action = "EXECUTE"

        elif probability >= 55:

            grade = "B"
            action = "MONITOR"

        else:

            grade = "C"
            action = "WAIT"



        if dominant_direction == "BUY":

            return ProbabilityResult(

                buy_probability=probability,

                sell_probability=max(
                    5,
                    100 - probability
                ),

                neutral_probability=10,

                expected_risk=risk_score,

                opportunity_grade=grade,

                institutional_confidence=confidence_score
            )


        elif dominant_direction == "SELL":

            return ProbabilityResult(

                buy_probability=max(
                    5,
                    100 - probability
                ),

                sell_probability=probability,

                neutral_probability=10,

                expected_risk=risk_score,

                opportunity_grade=grade,

                institutional_confidence=confidence_score
            )



        return ProbabilityResult(

            buy_probability=20,

            sell_probability=20,

            neutral_probability=60,

            expected_risk=risk_score,

            opportunity_grade="C",

            institutional_confidence=confidence_score
        )