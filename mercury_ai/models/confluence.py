from dataclasses import dataclass

from mercury_ai.models.recommendation import Recommendation


@dataclass
class ConfluenceResult:

    score: int
    confidence: int
    decision: str
    evidences: list

    def to_recommendation(self):

        return Recommendation(

            decision=self.decision,

            confidence=self.confidence,

            score=abs(self.score),

            strategy="Mercury AI",

            evidences=self.evidences,

            explanation="Decisão baseada na confluência dos analisadores."

        )