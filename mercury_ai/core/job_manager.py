import time
import threading
from typing import List, Dict, Any, Optional
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
from mercury_ai.config.assets import SUPPORTED_ASSETS
from mercury_ai.analysis.health_checker import HealthChecker
from mercury_ai.analysis.performance_statistics import PerformanceStatistics

class JobManager:
    def __init__(self, interval_seconds: int = 60):
        self.interval = interval_seconds
        self.running = False
        self.paused = False
        self.thread: Optional[threading.Thread] = None
        
        provider = YahooFinanceProvider()
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]),
            providers=[provider]
        )
        self.health = HealthChecker()
        self.stats = PerformanceStatistics()

    def _job_loop(self):
        while self.running:
            if not self.paused:
                self._execute_tasks()
            time.sleep(self.interval)

    def _execute_tasks(self):
        # Scanner + Pipeline Analysis + Snapshot
        assets = [s for sublist in SUPPORTED_ASSETS.values() for s in sublist]
        for symbol in assets:
            self.pipeline.analyze(symbol)
        
        # Health Check & Stats
        self.health.check()
        self.stats.calculate()

    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.thread = threading.Thread(target=self._job_loop, daemon=True)
            self.thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
