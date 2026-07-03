from mercury_ai.models.signal import Signal
from mercury_ai.models.recommendation import Recommendation


class DecisionEngine:
    """
    Responsável por transformar uma Recommendation
    em um Signal operacional.
    """

    def generate(
        self,
        asset: str,
        recommendation: Recommendation,
        current_price: float
    ) -> Signal:

        signal = Signal(
            asset=asset,
            action=recommendation.decision,
            confidence=recommendation.confidence,
            score=recommendation.score,
            entry=current_price,
            strategy=recommendation.strategy,
            evidences=recommendation.evidences,
            explanation=recommendation.explanation
        )

        # Stop e Take provisórios
        if signal.action == "BUY":

            signal.stop_loss = round(current_price * 0.995, 2)
            signal.take_profit = round(current_price * 1.010, 2)

        elif signal.action == "SELL":

            signal.stop_loss = round(current_price * 1.005, 2)
            signal.take_profit = round(current_price * 0.990, 2)

        else:

            signal.stop_loss = None
            signal.take_profit = None

        return signal