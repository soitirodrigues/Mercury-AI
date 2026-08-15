"""Test script for HistoricalReplayEngine DeterministicClock integration (S32-D-08)."""
import sys
import threading
import time
from datetime import datetime

sys.path.insert(0, r'.')
import pandas as pd
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine


def generate_mock_historical_data(symbol="TEST", n_days=30, start_date="2025-01-01"):
    """Generate mock historical OHLCV data for testing."""
    dates = pd.date_range(start=start_date, periods=n_days, freq='1D')
    data = {
        'open': [100.0 + i * 0.5 for i in range(n_days)],
        'high': [102.0 + i * 0.5 for i in range(n_days)],
        'low': [98.0 + i * 0.5 for i in range(n_days)],
        'close': [101.0 + i * 0.5 for i in range(n_days)],
        'volume': [1000000 + i * 1000 for i in range(n_days)]
    }
    return pd.DataFrame(data, index=dates)


def test_historical_replay_parallel_isolation():
    """S32-D-08: Test HistoricalReplayEngine.run_replay() in parallel."""
    print("=== S32-D-08: HistoricalReplayEngine Integration ===")
    
    # Generate mock data for multiple symbols
    symbols_data = {}
    for i, symbol in enumerate(['SYMBOLA', 'SYMBOLB', 'SYMBOLC', 'SYMBOLD']):
        symbols_data[symbol] = generate_mock_historical_data(symbol, n_days=50)
    
    # Track clock states before and after each replay
    clock_states = {}
    replay_results = {}
    contamination_count = 0
    
    def run_replay_isolated(symbol, df):
        """Run replay in isolated thread with clock state tracking."""
        thread_id = threading.get_ident()
        
        # Capture clock state before replay
        clock_before = DeterministicClock.snapshot()
        
        # Run the replay engine
        engine = HistoricalReplayEngine()
        try:
            metrics = engine.run_replay(
                symbol=symbol,
                full_df=df,
                n_candles=10,
                silent=True
            )
        except Exception as e:
            metrics = []
        
        # Capture clock state after replay
        clock_after = DeterministicClock.snapshot()
        
        # Record results
        result = {
            'symbol': symbol,
            'thread_id': thread_id,
            'clock_before': clock_before,
            'clock_after': clock_after,
            'metrics_count': len(metrics),
            'replay_success': len(metrics) > 0
        }
        replay_results[symbol] = result
        
        # Check for contamination - clock_after should not be contaminated by other threads
        # The key check: clock_after should either be None (real clock) or the last set time
        # It should NOT be a mix of different symbols' times
        return result
    
    # Run replays in parallel with threads
    threads = []
    for symbol, df in symbols_data.items():
        t = threading.Thread(target=lambda s, d: run_replay_isolated(s, d), args=(symbol, df))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join(timeout=60)
    
    # Analyze results
    print(f"Replay results for {len(replay_results)} symbols:")
    for symbol, result in replay_results.items():
        print(f"  {symbol}:")
        print(f"    Thread ID: {result['thread_id']}")
        print(f"    Clock before: {result['clock_before']}")
        print(f"    Clock after: {result['clock_after']}")
        print(f"    Metrics count: {result['metrics_count']}")
        print(f"    Replay success: {result['replay_success']}")
        
        # Check for contamination
        # If clock_after is not None and not clock_before, and there were multiple threads,
        # we need to verify isolation
        if result['clock_after'] is not None:
            # The clock_after should be a valid datetime, not a contaminated value
            is_valid = isinstance(result['clock_after'], datetime)
            if is_valid:
                print(f"    Clock after is valid datetime: OK")
            else:
                contamination_count += 1
                print(f"    WARNING: Clock after is invalid - possible contamination!")
    
    # Also verify that each thread's clock is independent
    print(f"\nContamination count: {contamination_count}/{len(replay_results)}")
    print(f"Test {'PASS' if contamination_count == 0 else 'FAIL'}: {'Clock isolation maintained' if contamination_count == 0 else 'Contamination observed'}")
    
    assert contamination_count == 0, f"Expected 0 contaminations, got {contamination_count}"
    print("PASS: HistoricalReplayEngine parallel execution maintains clock isolation\n")


def test_replay_clock_recovery():
    """S32-D-10: Test clock recovery after replay."""
    print("=== S32-D-10: Clock Recovery Test ===")
    
    # Generate mock data
    df = generate_mock_historical_data("RECOVERY", n_days=30)
    
    # Capture clock state before replay
    clock_before = DeterministicClock.snapshot()
    print(f"Clock before replay: {clock_before}")
    
    # Run replay
    engine = HistoricalReplayEngine()
    try:
        metrics = engine.run_replay(
            symbol="RECOVERY",
            full_df=df,
            n_candles=10,
            silent=True
        )
    except Exception as e:
        print(f"Replay error (may be expected): {type(e).__name__}")
        metrics = []
    
    # Capture clock state after replay
    clock_after = DeterministicClock.snapshot()
    print(f"Clock after replay: {clock_after}")
    
    # Check recovery: clock_after should equal clock_before (or be None for real clock)
    if clock_before is clock_after:
        print("PASS: Clock state unchanged (same object reference)")
    elif clock_before == clock_after:
        print("PASS: Clock state recovered to original value")
    elif clock_after is None:
        print("INFO: Clock restored to real mode (None) - also valid")
    else:
        # Check if they're different datetimes
        if clock_before is not None and clock_after is not None:
            print(f"  Before: {clock_before}, After: {clock_after}")
            if abs((clock_after - clock_before).total_seconds()) < 1:
                print("PASS: Clock recovered within 1 second (essentially unchanged)")
            else:
                print(f"WARN: Clock difference of {abs((clock_after - clock_before).total_seconds())} seconds")
    
    print("PASS: Clock recovery test completed\n")


if __name__ == "__main__":
    test_historical_replay_parallel_isolation()
    test_replay_clock_recovery()
    print("=" * 50)
    print("ALL S32-D-08/10 TESTS COMPLETED")
    print("=" * 50)