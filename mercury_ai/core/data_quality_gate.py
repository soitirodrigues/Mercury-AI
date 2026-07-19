from dataclasses import dataclass


@dataclass
class DataQualityResult:

    score: float
    allowed: bool
    warnings: list



class DataQualityGate:


    MIN_SCORE = 0.50



    def evaluate(self, quality):

        warnings = []


        score = getattr(
            quality,
            "score",
            0
        )


        if score < self.MIN_SCORE:

            warnings.append(
                f"Qualidade de dados baixa: {score:.2f}"
            )


            return DataQualityResult(
                score=score,
                allowed=False,
                warnings=warnings
            )



        return DataQualityResult(
            score=score,
            allowed=True,
            warnings=warnings
        )