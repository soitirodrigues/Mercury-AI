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



        print("\n")
        print("=" * 45)
        print("        MERCURY AI 🚀🤖")
        print("=" * 45)


        print(f"ATIVO: {asset}")
        print(f"DECISÃO: {decision_name}")
        print(f"GRADE: {grade}")
        print(f"CONFIANÇA: {confidence:.1f}%")



        print("-" * 45)

        print("CONTEXTO")


        explanation = getattr(
            decision,
            "explanation",
            None
        )


        if explanation:

            print(
                explanation.market_context
            )

            print(
                explanation.trend_context
            )

            print(
                explanation.structure_context
            )



        print("-" * 45)

        print("ANÁLISE")


        if explanation:

            print("\nFORÇAS:")

            for item in explanation.bullish_factors[:5]:

                print(
                    f"✅ {item}"
                )



            print("\nATENÇÃO:")

            for item in explanation.missing_confirmations:

                print(
                    f"⚠️ {item}"
                )



        print("-" * 45)


        print("AÇÃO MERCURY")


        if decision_name == "WAIT":

            print(
                "⏳ Aguardar confirmação antes da entrada."
            )


        elif decision_name == "BUY":

            print(
                "🟢 Possível oportunidade de COMPRA."
            )


        elif decision_name == "SELL":

            print(
                "🔴 Possível oportunidade de VENDA."
            )



        print("=" * 45)

