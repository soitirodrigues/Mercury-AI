from mercury_ai.core.banner import show_banner
from mercury_ai.config import settings
from mercury_ai.providers.provider import MarketProvider

def start():
    show_banner()

    provider = MarketProvider()
    
    # MarketData is a model, typically created by a service. 
    # For startup verification, we can use a dummy or just skip.
    # Removing the direct instantiation of MarketData as it's a frozen dataclass.

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