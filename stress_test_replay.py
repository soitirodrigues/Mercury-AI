import pandas as pd
import numpy as np
import time
import tracemalloc
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
import shutil
import os

def generate_mock_data(n_candles):
    data = {
        'Close': np.random.randn(n_candles).cumsum() + 100,
        'High': np.random.randn(n_candles).cumsum() + 101,
        'Low': np.random.randn(n_candles).cumsum() + 99,
        'Open': np.random.randn(n_candles).cumsum() + 100,
        'Volume': np.random.randint(1000, 5000, n_candles)
    }
    return pd.DataFrame(data, index=pd.date_range('2020-01-01', periods=n_candles, freq='5min'))

def run_stress_test(n_candles):
    print(f"\n--- Running Stress Test: {n_candles} candles ---")
    df = generate_mock_data(n_candles)
    engine = HistoricalReplayEngine()
    
    # Cleanup previous runs
    if os.path.exists("data/replay_results"): shutil.rmtree("data/replay_results")
    if os.path.exists("mercury_ai/database/snapshots"): shutil.rmtree("mercury_ai/database/snapshots")
    os.makedirs("data/replay_results", exist_ok=True)
    
    tracemalloc.start()
    start_time = time.perf_counter()
    
    engine.run_replay("GC=F", df, n_candles=20)
    
    end_time = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Time: {end_time - start_time:.2f}s")
    print(f"Peak Memory: {peak / 10**6:.2f} MB")

if __name__ == "__main__":
    for n in [10000, 50000, 100000, 500000, 1000000]:
        run_stress_test(n)
