from mercury_ai.core.banner import show_banner
from mercury_ai.config import settings
from mercury_ai.providers.provider import MarketProvider

def start():
    banner = show_banner()

    provider = MarketProvider()
    
    # MarketData is a model, typically created by a service. 
    # For startup verification, we can use a dummy or just skip.
    # Removing the direct instantiation of MarketData as it's a frozen dataclass.

    lines = [
        banner,
        "",
        f"Provider: {provider.get_name()}",
        f"Mercado: {provider.get_market_status()}",
        "",
        "Status:",
        "✓ Core iniciado",
        "✓ Configurações carregadas",
        "",
        f"Aplicação: {settings.APP_NAME}",
        f"Versão: {settings.VERSION}",
        "",
        "Mercury AI iniciado com sucesso!",
    ]
    return "\n".join(lines)