"""
Módulo de compatibilidade — reexporta o universo operacional oficial.

ATENÇÃO: A fonte única da verdade é mercury_ai.config.universe.
Este módulo é mantido para compatibilidade retroativa.
"""

# Re-exporta tudo do universo oficial
from mercury_ai.config.universe import (  # noqa: F401, E402
    # Dados principais
    OPERATIONAL_UNIVERSE,
    FOREX_UNIVERSE,
    CRYPTO_UNIVERSE,
    STOCK_UNIVERSE,
    COMMODITY_UNIVERSE,
    # Listas derivadas
    FOREX_SYMBOLS,
    CRYPTO_SYMBOLS,
    STOCK_SYMBOLS,
    COMMODITY_SYMBOLS,
    ALL_SYMBOLS,
    # Compatibilidade
    SUPPORTED_ASSETS,
    # Funções
    get_asset,
    get_enabled_symbols,
    get_all_provider_symbols,
    validate_symbol,
    universe_summary,
    # Tipo
    UniverseAsset,
)

# ============================================================
# COMPATIBILIDADE RETROATIVA — listas planas (deprecated)
# ============================================================

FOREX = FOREX_SYMBOLS
CRYPTO = CRYPTO_SYMBOLS
STOCKS = STOCK_SYMBOLS
COMMODITIES = COMMODITY_SYMBOLS
INDICES = SUPPORTED_ASSETS["INDICES"]

# Registry antigo — mantido para compatibilidade com código legado
ASSET_REGISTRY = {
    symbol: {
        "symbol": a.symbol,
        "display_name": a.display_name,
        "market": a.market,
        "enabled": a.enabled,
        "volatility": a.volatility,
        "precision": a.precision,
        "priority": a.priority,
    }
    for symbol, a in FOREX_UNIVERSE.items()
}
ASSET_REGISTRY.update({
    symbol: {
        "symbol": a.symbol,
        "display_name": a.display_name,
        "market": a.market,
        "enabled": a.enabled,
        "volatility": a.volatility,
        "precision": a.precision,
        "priority": a.priority,
    }
    for symbol, a in CRYPTO_UNIVERSE.items()
})
ASSET_REGISTRY.update({
    symbol: {
        "symbol": a.symbol,
        "display_name": a.display_name,
        "market": a.market,
        "enabled": a.enabled,
        "volatility": a.volatility,
        "precision": a.precision,
        "priority": a.priority,
    }
    for symbol, a in STOCK_UNIVERSE.items()
})
ASSET_REGISTRY.update({
    symbol: {
        "symbol": a.symbol,
        "display_name": a.display_name,
        "market": a.market,
        "enabled": a.enabled,
        "volatility": a.volatility,
        "precision": a.precision,
        "priority": a.priority,
    }
    for symbol, a in COMMODITY_UNIVERSE.items()
})

