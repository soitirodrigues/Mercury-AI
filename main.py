from mercury_ai.analysis.confluence_engine import ConfluenceEngine
from mercury_ai.analysis.market_context_builder import MarketContextBuilder
from mercury_ai.data.indicator_engine import IndicatorEngine
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.models.market_data import MarketData


def main():

    print("=" * 60)
    print("MERCURY AI")
    print("=" * 60)

    service = MarketDataService()
    indicator = IndicatorEngine()

    print("\nBaixando dados do mercado...")

    df = service.get_data("GC=F")

    print("Calculando indicadores...")

    dados = indicator.calculate(df)

    market = MarketData(
        symbol="OURO",
        timeframe="M5",
        **dados
    )

    builder = MarketContextBuilder()

    context = builder.build(df, market)

    engine = ConfluenceEngine()

    result = engine.analyze(context)

    print("\n" + "=" * 60)
    print("RELATÓRIO MERCURY")
    print("=" * 60)

    print(f"\nAtivo............. {market.symbol}")
    print(f"Timeframe......... {market.timeframe}")

    print("\nTENDÊNCIA")
    print("----------------------------")
    print(context.trend.trend)
    print(context.trend.explanation)

    print("\nPRICE ACTION")
    print("----------------------------")
    print(context.price_action.trend_structure)

    print("\nSUPORTE")
    print("----------------------------")
    print(context.support_resistance.support)

    print("\nRESISTÊNCIA")
    print("----------------------------")
    print(context.support_resistance.resistance)

    print("\nDECISÃO")
    print("----------------------------")
    print(result.decision)

    print(f"Score............. {result.score}")
    print(f"Confiança......... {result.confidence}%")

    print("\nEVIDÊNCIAS")

    for evidence in result.evidences:
        print(f"✓ {evidence}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()