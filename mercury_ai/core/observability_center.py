import psutil
import time
from typing import Dict, Any

class ObservabilityCenter:
    """
    Central de observabilidade para métricas de performance do sistema.
    """
    def __init__(self):
        self.metrics = {
            "engine_times": {},
            "provider_latencies": {},
            "asset_times": {},
        }
        
    def record_engine_time(self, engine_name: str, duration: float):
        self.metrics["engine_times"][engine_name] = duration
        
    def record_provider_latency(self, provider_name: str, latency: float):
        self.metrics["provider_latencies"][provider_name] = latency

    def record_asset_time(self, symbol: str, duration: float):
        self.metrics["asset_times"][symbol] = duration

    def get_metrics(self) -> Dict[str, Any]:
        return {
            **self.metrics,
            "cpu_percent": psutil.cpu_percent(),
            "ram_percent": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }
