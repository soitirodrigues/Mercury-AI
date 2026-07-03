from mercury_ai.providers.market_provider import MarketProvider
from mercury_ai.config.settings import ASSET


class MarketEngine:

    def __init__(self):

        self.provider = MarketProvider()

    def show_market(self):

        data = self.provider.get_price(ASSET)

        if data is None:

            print("Não foi possível obter dados.")

            return

        print("\n========== MERCURY MARKET ==========")

        print(f"Ativo : {data['symbol']}")
        print(f"Abertura : {data['open']:.2f}")
        print(f"Máxima : {data['high']:.2f}")
        print(f"Mínima : {data['low']:.2f}")
        print(f"Fechamento : {data['close']:.2f}")
        print(f"Volume : {data['volume']}")

        print("====================================")