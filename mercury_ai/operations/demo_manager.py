from typing import List, Dict, Any
import logging
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
from mercury_ai.config.assets import SUPPORTED_ASSETS
from mercury_ai.utils.deterministic_clock import DeterministicClock

class DemoOperationsManager:
    """
    Camada de simulação institucional para execução em conta Demo.
    """
    def __init__(self):
        provider = YahooFinanceProvider()
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]),
            providers=[provider]
        )
        self.demo_log: List[Dict[str, Any]] = []

    def run_simulation(self) -> List[Dict[str, Any]]:
        assets = []
        for asset_list in SUPPORTED_ASSETS.values():
            assets.extend(asset_list)

        for symbol in assets:
            try:
                # Executa a pipeline sem enviar ordens reais
                result = self.pipeline.analyze(symbol)
                
                # Registro dos dados da simulação
                log_entry = {
                    'timestamp': DeterministicClock.utcnow().isoformat(),
                    'asset': symbol,
                    'decision': result.decision.decision,
                    'snapshot': self.pipeline.last_snapshot,
                    'statistics': {
                        'confidence': result.decision.confidence,
                        'risk': result.decision.risk_score
                    }
                }
                self.demo_log.append(log_entry)
<<<<<<< HEAD
            except (RuntimeError, ValueError, TypeError, KeyError, OSError, AttributeError) as e:
                logging.error("Erro na simulação para %s: %s", symbol, e, exc_info=True)
=======
            except Exception as e:
                logging.error(f"Erro na simulação para {symbol}: {e}")
>>>>>>> 67cc5c60936ff914a76d6d94a09c6422d147e02a
        
        return self.demo_log
