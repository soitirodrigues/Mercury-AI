def analyze(
        self,
        context: MarketContext,
        evidence_bundle: Any,
        confluence_score: float,
        confidence_score: float,
        dominant_direction: Optional[str] = None,
    ) -> ProbabilityResult:

        # ----------------------------------------------------
        # Descobre direção caso não tenha sido informada
        # ----------------------------------------------------

        if dominant_direction is None:

            bullish = sum(
                1
                for e in evidence_bundle.evidences
                if str(e.direction).upper() == "BULLISH"
            )

            bearish = sum(
                1
                for e in evidence_bundle.evidences
                if str(e.direction).upper() == "BEARISH"
            )

            if bullish > bearish:
                dominant_direction = "BUY"

            elif bearish > bullish:
                dominant_direction = "SELL"

            else:
                dominant_direction = "WAIT"

        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        risk_score = (
            context
            .risk_assessment
            .institutional_risk_score
        )

        risk_factor = max(
            0.0,
            min(
                risk_score / 100.0,
                1.0,
            ),
        )

        # ----------------------------------------------------
        # Quantidade de evidências
        # ----------------------------------------------------

        evidence_bonus = min(
            len(evidence_bundle.evidences) * 4.0,
            20.0,
        )

        # ----------------------------------------------------
        # Score Institucional
        # ----------------------------------------------------

        # Composição canônica:
        # - confluence_score ..... 50%
        # - confidence_score ..... 35%
        # - evidence_bonus ....... 15%

        confluence_coef = 0.50
        confidence_coef = 0.35
        evidence_coef = 0.15

        institutional_strength = (
            confluence_score * confluence_coef
            + confidence_score * confidence_coef
            + evidence_bonus * evidence_coef
        )

        # ----------------------------------------------------
        # Penalidade de risco
        # ----------------------------------------------------

        print("=" * 70)
        print("DEBUG PROBABILITY")
        print("confluence_score:", confluence_score)
        print("confidence_score:", confidence_score)
        print("evidence_bonus:", evidence_bonus)
        print("risk_score:", risk_score)
        print("risk_factor:", risk_factor)
        print(
            "institutional_strength BEFORE RISK:",
            institutional_strength,
        )

        institutional_strength *= (
            1.0 - (risk_factor * 0.50)
        )

        institutional_strength = max(
            0.0,
            min(
                institutional_strength,
                100.0,
            ),
        )

        print(
            "institutional_strength AFTER RISK:",
            institutional_strength,
        )
        print("=" * 70)

        # ----------------------------------------------------
        # WAIT
        # ----------------------------------------------------

        # Quanto menor a força institucional,
        # maior a chance de WAIT.

        wait_probability = max(
            5.0,
            100.0 - institutional_strength,
        )

        wait_probability = min(
            wait_probability,
            60.0,
        )

        remaining = 100.0 - wait_probability

        # ----------------------------------------------------
        # Distribuição das probabilidades
        # ----------------------------------------------------

        directional_probability = remaining

        if dominant_direction in ("BUY", "BULLISH"):

            buy_probability = directional_probability
            sell_probability = 0.0

        elif dominant_direction in ("SELL", "BEARISH"):

            sell_probability = directional_probability
            buy_probability = 0.0

        else:

            # NEUTRAL ou desconhecido.
            buy_probability = directional_probability / 2.0
            sell_probability = directional_probability / 2.0

        # ----------------------------------------------------
        # Opportunity Grade
        # ----------------------------------------------------

        if institutional_strength >= 80:
            grade = "A+"

        elif institutional_strength >= 70:
            grade = "A"

        elif institutional_strength >= 60:
            grade = "B"

        elif institutional_strength >= 50:
            grade = "C"

        else:
            grade = "D"

        # ----------------------------------------------------
        # Resultado
        # ----------------------------------------------------

        return ProbabilityResult(
            buy_probability=round(
                buy_probability,
                2,
            ),
            sell_probability=round(
                sell_probability,
                2,
            ),
            neutral_probability=round(
                wait_probability,
                2,
            ),
            expected_risk=risk_score,
            opportunity_grade=grade,
            institutional_confidence=round(
                confidence_score,
                2,
            ),
        )