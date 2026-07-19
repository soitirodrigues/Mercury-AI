import time
from typing import List
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
from mercury_ai.config.assets import SUPPORTED_ASSETS

class LiveMonitor:
    """
    Camada de monitoramento contínuo da pipeline.
    """
    def __init__(self, interval_seconds: int = 60):
        self.interval = interval_seconds
        self.provider = YahooFinanceProvider()
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[self.provider]),
            providers=[self.provider]
        )
        
    def run_cycle(self):
        """Executa um ciclo completo de análise para todos os ativos."""
        assets = [symbol for asset_list in SUPPORTED_ASSETS.values() for symbol in asset_list]
        for symbol in assets:
            try:
                # Dispara a pipeline já existente
                self.pipeline.analyze(symbol)
            except Exception as e:
                # Log de erro mantido sem alterar a lógica de análise
                print(f"Erro no ciclo de monitoramento para {symbol}: {e}")
