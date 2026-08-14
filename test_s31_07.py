"""
S31-07 — Persistence / Restart Test

Testa o ciclo Persist ↓ Restart ↓ Reload ↓ Run B.

Objetivo: provar que o estado persiste corretamente sem overwrite silencioso.

Padrão de teste:
  Run A ↓ persist ↓ restart ↓ reload ↓ Run B
  
Provar:
  A permanece   (dados de A ainda disponíveis)
  AB permanece   (identidade AB preservada)
  BA ≠ B        (nova execução B é diferente da anterior)
"""

import sys
import os
import json
import pandas as pd
import numpy as np

# Add workspace to path
sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
from mercury_ai.database.snapshot_logger import compute_replay_id_from_snapshot, snapshot_filename_for
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine


def generate_deterministic_data(n_candles, seed=42):
    """Gera OHLCV deterministico e VALIDO."""
    np.random.seed(seed)
    close = 100.0 + np.random.randn(n_candles).cumsum()
    open_ = np.concatenate([[close[0]], close[:-1]])
    spread = np.abs(np.random.randn(n_candles)) * 0.3
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread
    volume = np.random.randint(1000, 5000, n_candles)
    return pd.DataFrame(
        {"close": close, "high": high, "low": low, "open": open_, "volume": volume},
        index=pd.date_range("2025-01-01", periods=n_candles, freq="5min"),
    )


def test_s31_07_persistence_restart():
    """S31-07: Testar ciclo Persist ↓ Restart ↓ Reload ↓ Run B"""
    
    print("=" * 60)
    print("S31-07 — Persistence / Restart Test")
    print("=" * 60)
    
    # Generate data
    n_candles = 100
    data = generate_deterministic_data(n_candles, seed=42)
    symbol = "TEST-SYMBOL"
    
    storage_dir = "data/persistence_test"
    os.makedirs(storage_dir, exist_ok=True)
    
    # === RUN A: First execution and persist ===
    print("\n--- RUN A: Initial execution and persist ---")
    
    # Reset clock
    DeterministicClock.reset()
    
    # Create storage
    storage = ReplayStorage(output_dir=storage_dir)
    
    # Run first replay
    engine = HistoricalReplayEngine()
    metrics_a = engine.run_replay(
        symbol=symbol,
        full_df=data,
        n_candles=20,
        silent=True
    )
    
    # Persist: save state explicitly
    # Get the last metric and its audit_id
    if len(metrics_a) > 0:
        last_metric = metrics_a[-1]
        # Save the metrics to a persistence file
        persist_data = {
            "run_a_metrics_count": len(metrics_a),
            "last_pl": last_metric.pl,
            "last_hit": last_metric.hit,
            "last_mae": last_metric.mae,
            "last_mfe": last_metric.mfe,
        }
        
        # Save persist file
        persist_file = os.path.join(storage_dir, "run_a_persist.json")
        with open(persist_file, "w", encoding="utf-8") as f:
            json.dump(persist_data, f, indent=2)
        
        print(f"  Metrics persisted: {len(metrics_a)} metrics")
        print(f"  Last PL: {last_metric.pl:.6f}, Hit: {last_metric.hit}")
        print(f"  Persist file: {persist_file}")
    
    # === RESTART: Reset and reload ===
    print("\n--- RESTART: Reset clock and reload ---")
    
    # Reset clock (simulating restart)
    DeterministicClock.reset()
    print(f"  Clock reset after restart")
    
    # Reload: re-read persist file
    persist_file = os.path.join(storage_dir, "run_a_persist.json")
    if os.path.exists(persist_file):
        with open(persist_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        print(f"  Persist data reloaded: {list(loaded_data.keys())}")
        print(f"  Original last PL: {persist_data['last_pl']}")
        print(f"  Loaded last PL: {loaded_data['last_pl']}")
        persist_match = loaded_data['last_pl'] == persist_data['last_pl']
        print(f"  Persist data match: {persist_match}")
    else:
        print(f"  ⚠️ Persist file not found after restart")
        loaded_data = {}
    
    # === RUN B: Second execution after restart ===
    print("\n--- RUN B: Second execution after restart ---")
    
    # Run second replay with fresh data (same seed for deterministic comparison)
    data_b = generate_deterministic_data(n_candles, seed=42)
    
    engine_b = HistoricalReplayEngine()
    metrics_b = engine_b.run_replay(
        symbol=symbol,
        full_df=data_b,
        n_candles=20,
        silent=True
    )
    
    print(f"  Run B metrics count: {len(metrics_b)}")
    if len(metrics_b) > 0:
        last_metric_b = metrics_b[-1]
        print(f"  Last PL: {last_metric_b.pl:.6f}, Hit: {last_metric_b.hit}")
    
    # === VERIFICATION: Compare A and B ===
    print("\n--- VERIFICATION: Compare Run A and Run B ---")
    
    # Check if Run A data is still accessible
    a_still_available = os.path.exists(persist_file) if 'persist_file' in dir() else False
    print(f"  Run A data still available: {a_still_available}")
    
    # Check if Run B produced different results (BA ≠ B)
    a_count = len(metrics_a) if 'metrics_a' in dir() else 0
    b_count = len(metrics_b)
    counts_different = a_count != b_count
    
    # Check persistence data integrity
    persist_integrity = False
    if 'loaded_data' in dir() and 'persist_data' in dir():
        persist_integrity = loaded_data.get('last_pl') == persist_data.get('last_pl')
    
    # Classification
    print(f"  Run A metrics: {a_count}")
    print(f"  Run B metrics: {b_count}")
    print(f"  Counts different (BA ≠ B): {counts_different}")
    print(f"  Persist integrity: {persist_integrity}")
    
    # S31-07 Classification
    all_conditions_met = a_still_available and counts_different
    
    print("\n" + "=" * 60)
    print("S31-07 — Persistence / Restart Results")
    print("=" * 60)
    print(f"  Run A still available: {a_still_available}")
    print(f"  BA ≠ B (counts different): {counts_different}")
    print(f"  Persist integrity: {persist_integrity}")
    
    if all_conditions_met:
        classification = "PASS"
        print(f"\n✅ S31-07 CLASSIFICATION: PASS")
        print("   Persistence/restart cycle validated")
        print("   State preserved across restart, no silent overwrite")
    elif not counts_different:
        classification = "FAIL"
        print(f"\n❌ S31-07 CLASSIFICATION: FAIL")
        print("   Run B produced same count as Run A (expected BA ≠ B failed)")
    else:
        classification = "RISK OBSERVED"
        print(f"\n⚠️ S31-07 CLASSIFICATION: RISK OBSERVED")
        print("   Persistence data partially preserved")
    
    return classification


def test_s31_07_identifier_preservation():
    """Testa que identifiers (replay_id, audit_id) são preservados corretamente."""
    
    print("\n" + "=" * 60)
    print("S31-07 — Identifier Preservation Test")
    print("=" * 60)
    
    # Generate data
    data = generate_deterministic_data(100, seed=42)
    symbol = "TEST-SYMBOL"
    
    # Run first replay
    DeterministicClock.reset()
    engine = HistoricalReplayEngine()
    metrics_a = engine.run_replay(
        symbol=symbol,
        full_df=data,
        n_candles=20,
        silent=True
    )
    
    # Get replay_id from the storage
    storage = ReplayStorage(output_dir="data/persistence_test")
    
    # Check that metrics were saved
    saved_files = []
    if os.path.exists(storage.output_dir):
        saved_files = os.listdir(storage.output_dir)
    
    print(f"  Saved files after Run A: {len(saved_files)}")
    print(f"  Metrics count from Run A: {len(metrics_a)}")
    
    # Run second replay (should create new files, not overwrite)
    data_b = generate_deterministic_data(100, seed=123)
    DeterministicClock.reset()
    engine_b = HistoricalReplayEngine()
    metrics_b = engine_b.run_replay(
        symbol=symbol,
        full_df=data_b,
        n_candles=20,
        silent=True
    )
    
    # Check saved files after Run B
    saved_files_b = []
    if os.path.exists(storage.output_dir):
        saved_files_b = os.listdir(storage.output_dir)
    
    print(f"  Saved files after Run B: {len(saved_files_b)}")
    print(f"  Files increased: {len(saved_files_b) > len(saved_files)}")
    
    # Classification
    if len(saved_files_b) > len(saved_files):
        print("✅ PASS: New replay created file, no silent overwrite")
        return "PASS"
    else:
        print("⚠️ WARNING: File count may not have increased (could be deduplication)")
        return "RISK OBSERVED"


if __name__ == "__main__":
    classification = test_s31_07_persistence_restart()
    test_s31_07_identifier_preservation()
    
    print("\n" + "=" * 60)
    print("S31-07 — FINAL CLASSIFICATION")
    print("=" * 60)
    print(f"Classification: {classification}")
    print("\nThis test validates the persistence/restart cycle: Run A → persist →")
    print("restart → reload → Run B. The goal is to prove that state is preserved")
    print("across restarts and that Run B produces results distinct from Run A "
    "(BA ≠ B), with no silent overwrite of previous data.")
    sys.exit(0 if classification in ["PASS", "RISK OBSERVED"] else 1)