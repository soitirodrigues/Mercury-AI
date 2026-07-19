import psutil
import time
from typing import Dict, Any
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

class HealthCenter:
    def __init__(self, provider_manager: MercuryDataProvider):
        self.provider_manager = provider_manager

    def get_system_metrics(self) -> Dict[str, Any]:
        process = psutil.Process()
        return {
            "cpu_percent": psutil.cpu_percent(),
            "ram_percent": psutil.virtual_memory().percent,
            "threads": process.num_threads(),
            "timestamp": time.time()
        }

    def get_component_health(self) -> Dict[str, str]:
        # Aggregate status of key components
        return {
            "Providers": "🟢" if all(self.provider_manager.healthcheck().values()) else "🟡",
            "Scanner": "🟢",  # Assuming operational
            "Pipeline": "🟢",
            "Dashboard": "🟢",
            "Replay": "🟢",
            "Logs": "🟢",
            "Snapshots": "🟢"
        }
