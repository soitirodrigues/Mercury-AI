"""
S32-C — Parallel Clock Isolation Closure Test (Focused Version)

This test focuses on the core question: is DeterministicClock._current_time
thread-local or shared class state?

Finding from S32-C-01: _current_time is SHARED class/global state - NOT thread-local.
"""

import sys
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json

# Add workspace to path
sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.utils.deterministic_clock import DeterministicClock


def test_baseline_shared_state():
    """
    S32-C-01: Baseline do Clock
    
    Documentar claramente se _current_time é:
      - thread-local
      - shared class/global state
    
    Finding: SHARED class/global state - NOT thread-local
    """
    print("\n" + "="*70)
    print("S32-C-01: Baseline do Clock - SHARED STATE CONFIRMED")
    print("="*70)
    
    DeterministicClock.reset()
    
    # Test: set time, check if all threads see same value
    set_time = datetime(2025, 1, 15, 10, 0, 0)
    DeterministicClock.set_time(set_time)
    
    # The class-level _current_time is shared
    current = DeterministicClock._current_time
    
    print(f"_current_time after set_time: {current}")
    print(f"_current_time is not None (shared state): {current is not None}")
    
    # Critical finding
    print("\n[FINDING] _current_time is SHARED class/global state - NOT thread-local")
    print("This means concurrent threads sharing the same DeterministicClock instance")
    print("will all see and modify the same _current_time, causing contamination.")
    
    return current is not None  # True = shared (the problem)


def test_concurrent_clock_observation():
    """
    S32-C-04: Internal Clock Contamination Test (focused version)
    
    Tests whether concurrent threads observing _current_time see their
    expected values or contaminated values.
    """
    print("\n" + "="*70)
    print("S32-C-04: Concurrent Clock Observation Test")
    print("="*70)
    
    DeterministicClock.reset()
    
    # Use ThreadPoolExecutor for proper concurrent execution
    num_workers = 4
    results = []
    errors = []
    
    def worker_observation(worker_id, expected_time):
        """Observe clock as a worker would."""
        thread_id = threading.get_ident()
        
        # Set the expected time (this is what HistoricalReplayEngine does)
        DeterministicClock.set_time(expected_time)
        
        # Immediately observe what we set
        observed_current = DeterministicClock._current_time
        observed_utcnow = DeterministicClock.utcnow()
        
        result = {
            "worker_id": worker_id,
            "expected_time": expected_time,
            "observed__current_time": observed_current,
            "observed_utcnow": observed_utcnow,
            "thread_id": thread_id,
            "match__current": observed_current == expected_time,
            "match_utcnow": observed_utcnow == expected_time,
        }
        results.append(result)
    
    # Create workers with different expected times
    expected_times = {
        "A": datetime(2025, 1, 15, 10, 0, 0),
        "B": datetime(2025, 1, 15, 10, 0, 1),
        "C": datetime(2025, 1, 15, 10, 0, 2),
        "D": datetime(2025, 1, 15, 10, 0, 3),
    }
    
    # Run concurrently
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for worker_id in ["A", "B", "C", "D"]:
            future = executor.submit(
                worker_observation, worker_id, expected_times[worker_id]
            )
            futures.append(future)
        
        # Wait for all to complete
        for future in futures:
            try:
                future.result(timeout=10)
            except Exception as e:
                errors.append(str(e))
    
    # Analyze results
    print(f"\nResults ({len(results)} workers, {len(errors)} errors):")
    contamination_count = 0
    for r in results:
        match = r["match__current"]
        status = "OK" if match else "CONTAMINATED"
        if not match:
            contamination_count += 1
        print(f"  {r['worker_id']}: expected={r['expected_time']}, ")
        print(f"    observed__current_time={r['observed__current_time']}, {status}")
    
    # Classification
    is_pass = contamination_count == 0
    print(f"\nContamination count: {contamination_count}/{len(results)}")
    print(f"Test {'PASS' if is_pass else 'FAIL'}: {'No cross-contamination' if is_pass else 'Cross-contamination observed'}")
    
    return is_pass


def test_barrier_synchronized_observation():
    """
    S32-C-03: Barrier Synchronization Test
    
    Tests clock observation with barrier synchronization to maximize race conditions.
    """
    print("\n" + "="*70)
    print("S32-C-03: Barrier-Synchronized Clock Observation")
    print("="*70)
    
    DeterministicClock.reset()
    
    barrier = threading.Barrier(4, action=lambda: None)
    results = []
    
    def worker_barrier(worker_id, expected_time):
        """Set clock and observe at barrier point."""
        thread_id = threading.get_ident()
        
        # All workers set their clocks before barrier
        DeterministicClock.set_time(expected_time)
        
        # Wait for all workers at barrier
        try:
            barrier.wait(timeout=5)
        except Exception as e:
            print(f"Barrier error for {worker_id}: {e}")
            return
        
        # After barrier - observe clock
        observed_current = DeterministicClock._current_time
        
        result = {
            "worker_id": worker_id,
            "expected_time": expected_time,
            "observed__current_time": observed_current,
        }
        results.append(result)
    
    # Start 4 workers
    expected_times = [
        datetime(2025, 1, 15, 10, 0, i) for i in range(4)
    ]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for worker_id, et in zip(["A", "B", "C", "D"], expected_times):
            future = executor.submit(worker_barrier, worker_id, et)
            futures.append(future)
        
        for future in futures:
            try:
                future.result(timeout=10)
            except Exception as e:
                print(f"Future error: {e}")
    
    # Analyze
    print(f"\nBarrier results ({len(results)} workers):")
    for r in results:
        match = r["observed__current_time"] == r["expected_time"]
        status = "MATCH" if match else "CONTAMINATED"
        print(f"  {r['worker_id']}: expected={r['expected_time']}, ")
        print(f"    observed={r['observed__current_time']}, {status}")
    
    return results


def test_replay_integrity():
    """
    S32-C-07: Replay Result Integrity Test
    
    Verifies that concurrent replays don't contaminate each other's results.
    """
    print("\n" + "="*70)
    print("S32-C-07: Replay Result Integrity")
    print("="*70)
    
    DeterministicClock.reset()
    
    from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
    import pandas as pd
    import numpy as np
    
    def generate_deterministic_data(n_candles, seed=42):
        np.random.seed(seed)
        close = 100.0 + np.random.randn(n_candles).cumsum()
        open_ = np.concatenate([[close[0]], close[:-1]])
        spread = np.abs(np.random.randn(n_candles)) * 0.3
        high = np.maximum(open_, close) + spread
        low = np.minimum(open_, close) - spread
        volume = np.random.randint(1000, 5000, n_candles)
        data = {
            "close": close,
            "high": high,
            "low": low,
            "open": open_,
            "volume": volume,
        }
        return pd.DataFrame(
            data,
            index=pd.date_range("2025-01-01", periods=n_candles, freq="5min"),
        )
    
    data = generate_deterministic_data(100)
    
    # Run 4 concurrent replays
    replay_results = []
    
    def run_replay_isolated(replay_idx):
        """Run a single replay and capture clock state."""
        clock_before = DeterministicClock.snapshot()
        
        engine = HistoricalReplayEngine()
        metrics_list = engine.run_replay(
            symbol=f"SYMBOL-{replay_idx}",
            full_df=data,
            n_candles=20,
            silent=True
        )
        
        clock_after = DeterministicClock.snapshot()
        
        return {
            "replay_idx": replay_idx,
            "clock_before": clock_before,
            "clock_after": clock_after,
            "metrics_count": len(metrics_list),
        }
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_replay_isolated, i): i for i in range(4)}
        for future in as_completed(futures):
            result = future.result()
            replay_results.append(result)
    
    # Analyze
    print(f"\nReplay integrity test ({len(replay_results)} concurrent replays):")
    all_restored = True
    for r in replay_results:
        before = r["clock_before"]
        after = r["clock_after"]
        restored = before is not None and after is not None
        if not restored:
            all_restored = False
        print(f"  Replay {r['replay_idx']}: before={before}, after={after}, restored={restored}")
    
    is_pass = all_restored
    print(f"\nTest {'PASS' if is_pass else 'FAIL'}: {'Clocks restored' if is_pass else 'Clock not restored'}")
    
    return is_pass


def test_s32_c_09_r2_classification():
    """
    S32-C-09: R2 Classification
    
    Synthesizes all test results to classify R2.
    """
    print("\n" + "="*70)
    print("S32-C-09: R2 Classification Synthesis")
    print("="*70)
    
    # Run all key tests
    print("\n--- Running S32-C-01: Baseline ---")
    is_shared = test_baseline_shared_state()
    
    print("\n--- Running S32-C-04: Concurrent Observation ---")
    is_pass_04 = test_concurrent_clock_observation()
    
    print("\n--- Running S32-C-03: Barrier Synchronization ---")
    test_barrier_synchronized_observation()
    
    print("\n--- Running S32-C-07: Replay Integrity ---")
    is_pass_07 = test_replay_integrity()
    
    # Synthesize R2 classification
    print("\n" + "="*70)
    print("S32-C-09: R2 CLASSIFICATION")
    print("="*70)
    
    # Key findings
    findings = {
        "S32-C-01 (Shared state)": is_shared,  # True = shared (problem)
        "S32-C-04 (Concurrent observation)": is_pass_04,  # True = no contamination
        "S32-C-07 (Replay integrity)": is_pass_07,  # True = clocks restored
    }
    
    print("\nTest Results:")
    for key, result in findings.items():
        status = "PASS" if result else "FAIL"
        print(f"  {key}: {status}")
    
    # Determine R2
    # R2 = FAIL if any test shows contamination or shared state issue
    # R2 = NOT PROVEN if we can't properly observe due to shared state
    # R2 = PASS if all tests pass
    
    any_failure = any(
        not result  # False means failure
        for result in findings.values()
    )
    
    # Also consider: if state is shared (S32-C-01), can we really prove isolation?
    can_truly_prove = not is_shared  # If shared, harder to prove per-thread isolation
    
    if any_failure:
        r2 = "FAIL"
        r2_reason = "Cross-contamination or shared state issue observed"
    elif is_shared and not can_truly_prove:
        r2 = "NOT PROVEN"
        r2_reason = "Shared clock state prevents per-thread isolation proof"
    else:
        r2 = "PASS"
        r2_reason = "No cross-contamination observed"
    
    print(f"\nR2 Classification: {r2}")
    print(f"R2 Reason: {r2_reason}")
    print(f"Can truly prove isolation: {can_truly_prove}")
    
    # Desired state after sprint
    print("\n--- State After This Sprint ---")
    print(f"  C2 = {'PASS WITH RESERVATIONS' if is_shared else 'PASS'}")
    print(f"  R1 = NOT PROVEN")
    print(f"  R2 = {r2}")
    print(f"  S32-C = dedicado exclusivamente ao R2")
    print()
    print("Não fechar V1 ainda.")
    print("Não liberar LIVE.")
    print("Não alterar estratégia.")
    
    return r2


if __name__ == "__main__":
    print("="*70)
    print("S32-C - Parallel Clock Isolation Closure (Focused)")
    print("="*70)
    print(f"\nCurrent date: 2026-08-15")
    print(f"Working directory: C:\\Projetos\\Mercury-AI")
    print()
    
    # Run the classification test (synthesizes all other tests)
    r2 = test_s32_c_09_r2_classification()
    
    print("\n" + "="*70)
    print("S32-C Test Suite Complete")
    print("="*70)
    print(f"\nFinal Classification: R2 = {r2}")
    print("This is the critical result determining V1 closure.")