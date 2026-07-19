import logging
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider
from mercury_ai.core.health_center import HealthCenter
from mercury_ai.core.asset_registry import AssetRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MercuryAutoHealth")

class MercuryAutoHealth:
    def __init__(self, provider_manager: MercuryDataProvider, asset_registry: AssetRegistry):
        self.health_center = HealthCenter(provider_manager)
        self.asset_registry = asset_registry

    def run_all_checks(self) -> dict:
        results = {}
        
        # Providers
        results["Providers"] = all(self.health_center.provider_manager.healthcheck().values())
        
        # Scanner, Dashboard, Replay, Pipeline (from HealthCenter)
        component_health = self.health_center.get_component_health()
        results.update({k: (v == "🟢") for k, v in component_health.items()})
        
        # Database/Registry
        results["AssetRegistry"] = len(self.asset_registry.assets) > 0
        
        # Logs (simulated check)
        import os
        results["Logs"] = os.path.exists("logs")
        
        logger.info(f"Auto Health Report: {results}")
        return results
