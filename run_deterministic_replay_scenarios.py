import pandas as pd
import numpy as np
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine

def generate_deterministic_data(n_candles, seed=42):
    np.random.seed(seed)
    data = {
        'close': np.random.randn(n_candles).cumsum() + 100,
        'high': np.random.randn(n_candles).cumsum() + 101,
        'low': np.random.randn(n_candles).cumsum() + 99,
        'open': np.random.randn(n_candles).cumsum() + 100,
        'volume': np.random.randint(1000, 5000, n_candles)
    }
    return pd.DataFrame(data, index=pd.date_range('2025-01-01', periods=n_candles, freq='5min'))

def run_replay_scenario(asset, months):
    # n_candles estimation: 12 candles/hour * 24 hours * 30 days * months
    n_candles = 12 * 24 * 30 * months
    df = generate_deterministic_data(n_candles)
    
    engine = HistoricalReplayEngine()
    
    # Run deterministic replay
    engine.run_replay(asset, df, n_candles=20)
    print(f"Completed replay for {asset} - {months} months ({n_candles} candles)")

if __name__ == "__main__":
    assets = ["BTCUSD"] # Requirement for this specific prompt
    horizons = [1, 3, 6, 12] # Months
    
    for asset in assets:
        for months in horizons:
            run_replay_scenario(asset, months)
