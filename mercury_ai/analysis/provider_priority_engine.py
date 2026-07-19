import logging
from typing import Optional
from mercury_ai.data.mercury_data_provider import MercuryDataProvider, IMercuryDataProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ProviderPriorityEngine")

class ProviderPriorityEngine:
    def __init__(self, manager: MercuryDataProvider):
        self.manager = manager

    def get_optimal_provider(self, symbol: str) -> Optional[IMercuryDataProvider]:
        provider = self.manager.best_provider(symbol)
        if provider:
            logger.info(f"Optimal provider for {symbol}: {provider.name} (Priority: {provider.priority})")
        else:
            logger.warning(f"No provider found for {symbol}")
        return provider
