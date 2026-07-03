from mercury_ai.core.banner import show_banner
from mercury_ai.config import settings
from mercury_ai.providers.provider import MarketProvider
from mercury_ai.data.market_data import MarketData
def start():
    show_banner()

    provider = MarketProvider()
    market = MarketData()

    print(f"Ativo: {market.get_symbol()}")
    print(f"Timeframe: {market.get_timeframe()}")

    print()

    print(f"Provider: {provider.get_name()}")
    print(f"Mercado: {provider.get_market_status()}")
    print()

    print("Status:")
    print("✓ Core iniciado")
    print("✓ Configurações carregadas")
    print()

    print(f"Aplicação: {settings.APP_NAME}")
    print(f"Versão: {settings.VERSION}")
    print()

    print("Mercury AI iniciado com sucesso!")