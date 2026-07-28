from typing import List

import pandas as pd
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics

from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.historical_replay_provider import HistoricalReplayProvider

class HistoricalReplayEngine:
    """
    Simula o mercado em tempo real usando dados históricos.
    Previne look-ahead bias através de fatiamento de dados determinístico.
    """

    def run_replay(self, symbol: str, full_df: pd.DataFrame, n_candles: int = 20) -> List[ReplayMetrics]:
        # Mínimo para indicadores (EMA 50)
        start_idx = 60
        
        # Pre-calculate rolling averages
        avg_volume = full_df['volume'].rolling(20).mean()
        avg_body = (full_df['close'] - full_df['open']).abs().rolling(20).mean()
        
        # Inicializa o provedor de dados histórico
        provider = HistoricalReplayProvider() # Will need to adapt this to use provider in loop
        
        # Define o DataFrame completo no provedor
        provider.set_data(full_df)
        
        # Injeta o provedor no pipeline
        pipeline = AnalysisPipeline(market_service=MarketDataService(providers=[provider]), providers=[provider])
        storage = ReplayStorage()
        
        all_metrics: List[ReplayMetrics] = []
        total = len(full_df) - n_candles - start_idx
        last_pct = 0
        
        for i in range(start_idx, len(full_df) - n_candles):
            # Progress logging a cada 5%
            pct = ((i - start_idx) * 100) // total
            if pct >= last_pct + 5:
                last_pct = pct
                print(f"  Progresso: {pct}% ({i-start_idx}/{total} candles)")
            # Update mock time
            current_time = pd.to_datetime(full_df.index[i]).to_pydatetime()
            DeterministicClock.set_time(current_time)

            # Atualiza o provedor com o índice atual
            provider.set_index(i)
            
            # Executa o pipeline de forma determinística
            # A pipeline.analyze() salva o snapshot e o armazena em last_snapshot.
            # Pass pre-calculated metrics for the current slice
            pipeline.analyze(symbol, avg_volume=avg_volume.iloc[:i+1], avg_body=avg_body.iloc[:i+1], silent=True)
            snapshot = pipeline.last_snapshot
            
            # Recalcular métricas
            entry_price = full_df['close'].iloc[i]
            future_prices = full_df['close'].iloc[i+1:i+n_candles+1]
            
            pl = (future_prices.iloc[-1] - entry_price) / entry_price
            mae = (future_prices.min() - entry_price) / entry_price
            mfe = (future_prices.max() - entry_price) / entry_price
            
            decision = snapshot.decision_result.decision
            hit = False
            if decision == "BUY": hit = pl > 0
            elif decision == "SELL": hit = pl < 0
            
            metrics = ReplayMetrics(mae=float(mae), mfe=float(mfe), pl=float(pl), hit=hit)
            storage.save(snapshot.decision_result.audit_id, snapshot, metrics)
            all_metrics.append(metrics)
        
        return all_metrics
