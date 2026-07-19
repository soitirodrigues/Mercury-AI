class SignalFormatter:


    def format(self, result, asset):


        decision = result.decision


        confidence = getattr(
            decision,
            "confidence",
            0
        )


        if confidence <= 1:
            confidence *= 100


        grade = getattr(
            decision,
            "grade",
            "N/A"
        )


        decision_name = getattr(
            decision,
            "decision",
            "UNKNOWN"
        )


        if hasattr(decision_name, "value"):
            decision_name = decision_name.value


        lines = [
            "",
            "=" * 45,
            "        MERCURY AI 🚀🤖",
            "=" * 45,
            f"ATIVO: {asset}",
            f"DECISÃO: {decision_name}",
            f"GRADE: {grade}",
            f"CONFIANÇA: {confidence:.1f}%",
            "-" * 45,
            "CONTEXTO",
        ]


        explanation = getattr(
            decision,
            "explanation",
            None
        )


        if explanation:

            lines.append(explanation.market_context)
            lines.append(explanation.trend_context)
            lines.append(explanation.structure_context)


        lines.append("-" * 45)
        lines.append("ANÁLISE")


        if explanation:

            lines.append("\nFORÇAS:")

            for item in explanation.bullish_factors[:5]:

                lines.append(f"✅ {item}")


            lines.append("\nATENÇÃO:")

            for item in explanation.missing_confirmations:

                lines.append(f"⚠️ {item}")


        lines.append("-" * 45)


        lines.append("AÇÃO MERCURY")


        if decision_name == "WAIT":

            lines.append("⏳ Aguardar confirmação antes da entrada.")


        elif decision_name == "BUY":

            lines.append("🟢 Possível oportunidade de COMPRA.")


        elif decision_name == "SELL":

            lines.append("🔴 Possível oportunidade de VENDA.")


        lines.append("=" * 45)

        return "\n".join(lines)

