import psutil
import time

class SystemMonitor:
    @staticmethod
    def get_metrics():
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }
