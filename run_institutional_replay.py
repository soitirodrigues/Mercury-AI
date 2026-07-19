import pandas as pd
import os
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine

def load_local_data(asset: str):
    # Try to load data from parquet file
    filepath = f"data/replay/{asset}/data.parquet"
    if not os.path.exists(filepath):
        print(f"Skipping {asset}: data not found at {filepath}")
        return None
    try:
        df = pd.read_parquet(filepath)
        return df
    except Exception as e:
        print(f"Skipping {asset}: Error loading data: {e}")
        return None

def run_institutional_replay():
    # Dynamically discover assets
    data_dir = "data/replay"
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist.")
        return

    assets = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    for asset in assets:
        print(f"--- Replaying {asset} ---")
        df = load_local_data(asset)
        if df is None:
            continue
            
        engine = HistoricalReplayEngine()
        
        # Run replay
        engine.run_replay(asset, df, n_candles=20)
        print(f"Replay for {asset} complete.")

if __name__ == "__main__":
    run_institutional_replay()
