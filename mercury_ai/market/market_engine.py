from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.config.settings import ASSET


class MarketEngine:

    def __init__(self):

        self.provider = MercuryDataProvider()

    def show_market(self):

        data = self.provider.get_price(ASSET)

        if data is None:

            return "Não foi possível obter dados."

        lines = [
            "\n========== MERCURY MARKET ==========",
            f"Ativo : {data['symbol']}",
            f"Abertura : {data['open']:.2f}",
            f"Máxima : {data['high']:.2f}",
            f"Mínima : {data['low']:.2f}",
            f"Fechamento : {data['close']:.2f}",
            f"Volume : {data['volume']}",
            "====================================",
        ]
        return "\n".join(lines)