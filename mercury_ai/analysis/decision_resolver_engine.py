from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DecisionResolverResult:
    decision: str
    confidence_override: Optional[float]
    triggered_rule: int


class DecisionResolverEngine:
    """
    Motor institucional de resolução da decisão final.

    Modelo C — Híbrido Institucional:

        Confluence define a direção.
        Probability qualifica com thresholds.
        O Resolver arbitra a decisão final.

    Regras (em ordem de prioridade):

        1. is_valid == False
           → WAIT (confidence_override = 0.0)

        2. dominant_direction == NEUTRAL
           → WAIT

        3. opportunity_grade == "D"
           → WAIT

        4. conflicting_signals == True
           AND opportunity_grade in ("C", "D")
           → WAIT

        5. dominant_direction == BUY
           → BUY

        6. dominant_direction == SELL
           → SELL

        7. Fallback
           → WAIT
    """

    def resolve(
        self,
        dominant_direction: str,
        is_valid: bool,
        opportunity_grade: str = "C",
        conflicting_signals: bool = False,
    ) -> DecisionResolverResult:

        confidence_override: Optional[float] = None

        # Regra 1: Validação
        if not is_valid:
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=0.0,
                triggered_rule=1,
            )

        # Regra 2: Direção neutra
        if dominant_direction == "NEUTRAL":
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=2,
            )

        # Regra 3: Oportunidade muito baixa
        if opportunity_grade == "D":
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=3,
            )

        # Regra 4: Conflito com força insuficiente
        if conflicting_signals and opportunity_grade in ("C", "D"):
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=4,
            )

        # Regra 5: BUY
        if dominant_direction == "BUY":
            return DecisionResolverResult(
                decision="BUY",
                confidence_override=None,
                triggered_rule=5,
            )

        # Regra 6: SELL
        if dominant_direction == "SELL":
            return DecisionResolverResult(
                decision="SELL",
                confidence_override=None,
                triggered_rule=6,
            )

        # Regra 7: Fallback
        return DecisionResolverResult(
            decision="WAIT",
            confidence_override=None,
            triggered_rule=7,
        )