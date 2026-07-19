"""
Módulo de compatibilidade — reexporta MercuryDataProvider do módulo canônico.

ATENÇÃO: Este módulo é mantido apenas para compatibilidade retroativa.
Use ``from mercury_ai.providers.market_provider import MercuryDataProvider``.
"""

from mercury_ai.providers.market_provider import MercuryDataProvider  # noqa: F401

# Alias para compatibilidade com código legado que importa MercuryDataProviderManager
MercuryDataProviderManager = MercuryDataProvider  # noqa: F401