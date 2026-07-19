from mercury_ai.models.analysis_result import AnalysisResult


class InstitutionalBrain:
    """
    Camada de IA explicável.

    Apenas transforma o AnalysisResult em uma
    explicação legível para o operador.
    """

    def explain(
        self,
        result: AnalysisResult
    ) -> str:

        lines = []

        ####################################################
        # DECISÃO
        ####################################################

        lines.append(
            f"Decisão: {result.decision.decision}"
        )

        ####################################################
        # SCORE
        ####################################################

        lines.append(
            f"Score Institucional: {result.decision.score:.2f}"
        )

        ####################################################
        # CONFIANÇA
        ####################################################

        lines.append(
            f"Confiança: {result.decision.confidence*100:.1f}%"
        )

        ####################################################
        # PROBABILIDADES
        ####################################################

        lines.append(
            (
                f"BUY {result.decision.buy_probability:.1f}% | "
                f"SELL {result.decision.sell_probability:.1f}% | "
                f"WAIT {result.decision.wait_probability:.1f}%"
            )
        )

        ####################################################
        # REGIME
        ####################################################

        if result.market_regime:

            lines.append(
                f"Regime: {result.market_regime.regime}"
            )

        ####################################################
        # RESUMO EXECUTIVO
        ####################################################

        if getattr(result, "summary", None):

            lines.append(result.summary)

        ####################################################
        # MOTIVO TÉCNICO
        ####################################################

        if getattr(result, "technical_reason", None):

            lines.append(result.technical_reason)

        ####################################################
        # ALERTAS
        ####################################################

        if getattr(result, "warnings", None):

            if len(result.warnings):

                lines.append(
                    "Alertas: "
                    + ", ".join(result.warnings)
                )

        return "\n".join(lines)