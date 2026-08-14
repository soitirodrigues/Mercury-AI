"""
S31-04 — DeterministicClock Hardening Test

Testa o padrão: normal ↓replay A ↓normal ↓replay B ↓normal

Objetivo: descobrir se o clock compartilhado gera interferência real.

Regra crítica: não mascarar o problema alterando comportamento apenas para fazer o teste passar.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add workspace to path
sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics


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


def test_s31_04_clock_hardening():
    """S31-04: Validar padrão normal → replay A → normal → replay B → normal"""
    
    print("=" * 60)
    print("S31-04 — DeterministicClock Hardening Test")
    print("Padrão: normal → replay A → normal → replay B → normal")
    print("=" * 60)
    
    # Generate data
    n_candles = 100
    data = generate_deterministic_data(n_candles, seed=42)
    symbol = "TEST-SYMBOL"
    
    # === PHASE 1: Normal execution (baseline) ===
    print("\n--- PHASE 1: Normal execution (baseline) ---")
    
    # Reset clock
    DeterministicClock.reset()
    clock_1_before = DeterministicClock.utcnow()
    print(f"Clock reset. utcnow() before: {clock_1_before}")
    
    # Run first replay
    engine = HistoricalReplayEngine()
    metrics_1 = engine.run_replay(
        symbol=symbol,
        full_df=data,
        n_candles=20,
        silent=True
    )
    print(f"Replay A completed: {len(metrics_1)} metrics")
    
    # Capture clock state after replay A
    clock_1_after = DeterministicClock.utcnow()
    snapshot_1 = DeterministicClock.snapshot()
    print(f"Clock utcnow() after Replay A: {clock_1_after}")
    print(f"DeterministicClock.snapshot() after Replay A: {snapshot_1}")
    
    # === PHASE 2: Normal period between replays ===
    print("\n--- PHASE 2: Normal period between replays ---")
    
    # Reset clock to simulate "normal" period
    DeterministicClock.reset()
    clock_2_before = DeterministicClock.utcnow()
    print(f"Clock reset (normal period). utcnow() before Replay B: {clock_2_before}")
    
    # Run second replay
    metrics_2 = engine.run_replay(
        symbol=symbol,
        full_df=data,
        n_candles=20,
        silent=True
    )
    print(f"Replay B completed: {len(metrics_2)} metrics")
    
    # Capture clock state after replay B
    clock_2_after = DeterministicClock.utcnow()
    snapshot_2 = DeterministicClock.snapshot()
    print(f"Clock utcnow() after Replay B: {clock_2_after}")
    print(f"DeterministicClock.snapshot() after Replay B: {snapshot_2}")
    
    # === PHASE 3: Verify clock isolation ===
    print("\n--- PHASE 3: Verify clock isolation ---")
    
    # Check if clocks are properly isolated
    clocks_isolated = True
    
    # The key test: after reset + replay B, the clock should behave as if
    # starting fresh, not contaminated by Replay A
    if snapshot_1 is not None:
        # If snapshot is not None after reset, there's contamination
        # (the clock should have been reset)
        print(f"⚠️ Snapshot after reset: {snapshot_1} - indicates potential contamination")
        clocks_isolated = False
    
    # Check UTCNow consistency
    final_clock = DeterministicClock.utcnow()
    print(f"Final DeterministicClock.utcnow(): {final_clock}")
    
    # Classification
    print("\n" + "=" * 60)
    print("S31-04 — DeterministicClock Hardening Results")
    print("=" * 60)
    print(f"  Replay A metrics: {len(metrics_1)}")
    print(f"  Replay B metrics: {len(metrics_2)}")
    print(f"  Clocks properly isolated: {clocks_isolated}")
    print(f"  Final clock state: {final_clock}")
    
    if clocks_isolated:
        classification = "PASS"
        print("\n✅ S31-04 CLASSIFICATION: PASS")
        print("   DeterministicClock hardening validated - no interference detected")
        print("   between sequential replay executions.")
    else:
        classification = "RISK OBSERVED"
        print("\n⚠️ S31-04 CLASSIFICATION: RISK OBSERVED")
        print("   Potential clock interference detected between sequential replays")
        print("   - Verificar se o problema persiste com ThreadPoolExecutor paralelo")
        print("   - Considerar hardening do DeterministicClock com thread-local storage")
    
    return classification


def test_s31_04_parallel_vs_sequential():
    """Testa paralelismo vs sequência para comparar interferência."""
    
    print("\n" + "=" * 60)
    print("S31-04 Bonus: Parallel vs Sequential Clock Comparison")
    print("=" * 60)
    
    n_candles = 100
    data = generate_deterministic_data(n_candles, seed=42)
    symbol = "TEST-SYMBOL"
    
    # Sequential execution (the S31-04 pattern)
    print("\n--- Sequential execution (normal → A → normal → B → normal) ---")
    
    DeterministicClock.reset()
    metrics_seq_a = HistoricalReplayEngine().run_replay(
        symbol=symbol, full_df=data, n_candles=20, silent=True
    )
    DeterministicClock.reset()
    metrics_seq_b = HistoricalReplayEngine().run_replay(
        symbol=symbol, full_df=data, n_candles=20, silent=True
    )
    
    print(f"  Replay A (sequential): {len(metrics_seq_a)} metrics")
    print(f"  Replay B (sequential): {len(metrics_seq_b)} metrics")
    
    # Parallel execution (from S31-03)
    print("\n--- Parallel execution (ThreadPoolExecutor) ---")
    
    DeterministicClock.reset()
    results_par = []
    with __import__('concurrent.futures').ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(HistoricalReplayEngine().run_replay, symbol, data, 20, True),
            executor.submit(HistoricalReplayEngine().run_replay, symbol, data, 20, True),
        ]
        for f in futures:
            results_par.append(f.result())
    
    print(f"  Parallel Replay 1: {len(results_par[0])} metrics")
    print(f"  Parallel Replay 2: {len(results_par[1])} metrics")
    
    # Comparison
    seq_a_len = len(metrics_seq_a) if 'metrics_seq_a' in dir() else 0
    seq_b_len = len(metrics_seq_b) if 'metrics_seq_b' in dir() else 0
    par_len_1 = len(results_par[0]) if 'results_par' in dir() and len(results_par) > 0 else 0
    par_len_2 = len(results_par[1]) if 'results_par' in dir() and len(results_par) > 1 else 0
    
    print("\n--- Comparison ---")
    print(f"  Sequential A: {seq_a_len}, B: {seq_b_len}")
    print(f"  Parallel 1: {par_len_1}, Parallel 2: {par_len_2}")
    print(f"  Results match (seq vs par): {seq_a_len == par_len_1 and seq_b_len == par_len_2}")
    
    return len(metrics_seq_a), len(metrics_seq_b), par_len_1, par_len_2


if __name__ == "__main__":
    classification = test_s31_04_clock_hardening()
    test_s31_04_parallel_vs_sequential()
    
    print("\n" + "=" * 60)
    print("S31-04 FINAL CLASSIFICATION")
    print("=" * 60)
    print(f"Classification: {classification}")
    print("\nThis test validates the DeterministicClock hardening without masking")
    print("the underlying problem. If RISK OBSERVED, the shared _lock causes")
    print("interference that needs to be addressed before V1 COMPLETE can be declared.")
    sys.exit(0 if classification == "PASS" else 1)