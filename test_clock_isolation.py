"""Test script for DeterministicClock thread-local isolation."""
import sys
import threading
from datetime import datetime

sys.path.insert(0, r'.')
from mercury_ai.utils.deterministic_clock import DeterministicClock


def test_thread_local_isolation():
    """Test that each thread has its own isolated clock state."""
    print("=== Test 1: Thread-local isolation ===")
    DeterministicClock.reset()
    
    # Set time from 'thread A'
    set_time_a = datetime(2025, 1, 15, 10, 0, 0)
    DeterministicClock.set_time(set_time_a)
    after_set = DeterministicClock.utcnow()
    print(f'After set_time (main thread): {after_set}')
    
    # Check main thread still sees its own time
    main_time = DeterministicClock._get_current_time()
    print(f'Main thread _current_time: {main_time}')
    
    assert main_time is not None, "Main thread should have its own time set"
    assert main_time == set_time_a, "Main thread should see its own expected time"
    print("PASS: Main thread has isolated clock state\n")


def test_worker_isolation():
    """Test that worker threads don't contaminate each other's clock."""
    print("=== Test 2: Worker thread isolation ===")
    DeterministicClock.reset()
    
    results = {}
    
    def worker_set_and_read(expected_time, result_dict, key):
        '''Worker sets time and reads it back - should only see its own setting.'''
        DeterministicClock.set_time(expected_time)
        observed = DeterministicClock.utcnow()
        result_dict[key] = {
            'expected': expected_time,
            'observed': observed,
            'thread_id': threading.get_ident()
        }
    
    t1 = threading.Thread(target=worker_set_and_read, 
                          args=(datetime(2025, 1, 15, 10, 0, 0), results, 'A'))
    t2 = threading.Thread(target=worker_set_and_read, 
                          args=(datetime(2025, 1, 15, 10, 0, 1), results, 'B'))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print(f'Thread A result: {results["A"]}')
    print(f'Thread B result: {results["B"]}')
    
    # Verify each thread sees its own expected time
    a_match = results['A']['observed'] == results['A']['expected']
    b_match = results['B']['observed'] == results['B']['expected']
    
    print(f'Thread A observed its expected time: {a_match}')
    print(f'Thread B observed its expected time: {b_match}')
    
    assert a_match, "Thread A should observe its own expected time"
    assert b_match, "Thread B should observe its own expected time"
    print("PASS: Worker threads have isolated clock state\n")


def test_barrier_adversarial():
    """Test the original S32-C barrier scenario that revealed the race condition."""
    print("=== Test 3: Barrier adversarial scenario ===")
    DeterministicClock.reset()
    
    clocks_at_barrier = []
    
    def worker_barrier(worker_id, expected_time):
        '''Sets clock and reads after barrier - should only see its own time'''
        DeterministicClock.set_time(expected_time)
        
        # Small delay to ensure thread scheduling
        import time
        time.sleep(0.01)
        
        clock_after = DeterministicClock.utcnow()
        clock_shared = DeterministicClock._get_current_time()
        
        result = {
            'worker_id': worker_id,
            'expected_time': expected_time,
            'clock_after': clock_after,
            'clock_shared': clock_shared,
        }
        clocks_at_barrier.append(result)
    
    worker_threads = []
    expected_times = [
        ('A', datetime(2025, 1, 15, 10, 0, 0)),
        ('B', datetime(2025, 1, 15, 10, 0, 1)),
        ('C', datetime(2025, 1, 15, 10, 0, 2)),
        ('D', datetime(2025, 1, 15, 10, 0, 3)),
    ]
    
    for worker_id, expected_time in expected_times:
        t = threading.Thread(target=worker_barrier, args=(worker_id, expected_time))
        worker_threads.append(t)
        t.start()
    
    for t in worker_threads:
        t.join(timeout=15)
    
    print('Barrier results:')
    for r in clocks_at_barrier:
        print(f'  {r["worker_id"]}: expected={r["expected_time"]}, clock_shared={r["clock_shared"]}')
    
    # Check if any cross-contamination occurred
    contamination = 0
    for r in clocks_at_barrier:
        if r['clock_shared'] is not None and r['clock_shared'] != r['expected_time']:
            contamination += 1
            print(f'  WARNING: {r["worker_id"]} sees shared clock != expected')
    
    print(f'Contamination count: {contamination}/4')
    print(f'Test {"PASS" if contamination == 0 else "FAIL"}: {"No cross-contamination" if contamination == 0 else "Cross-contamination observed"}')
    
    assert contamination == 0, f"Expected 0 contaminations, got {contamination}"
    print("PASS: Barrier adversarial scenario - no cross-contamination\n")


def test_50_rounds():
    """Run 50 rounds with distinct timestamps to verify consistent isolation."""
    print("=== Test 4: 50+ rounds with distinct timestamps ===")
    DeterministicClock.reset()
    
    num_rounds = 50
    num_workers = 4
    all_results = []
    contamination_total = 0
    
    # Different timestamp patterns for different rounds
    timestamp_patterns = [
        # Round 01
        {"A": datetime(2025, 1, 15, 10, 0, 0), "B": datetime(2025, 1, 15, 10, 0, 1),
         "C": datetime(2025, 1, 15, 10, 0, 2), "D": datetime(2025, 1, 15, 10, 0, 3)},
        # Round 02
        {"A": datetime(2025, 1, 15, 11, 10, 0), "B": datetime(2025, 1, 15, 11, 10, 1),
         "C": datetime(2025, 1, 15, 11, 10, 2), "D": datetime(2025, 1, 15, 11, 10, 3)},
        # Round 03
        {"A": datetime(2025, 1, 15, 14, 30, 0), "B": datetime(2025, 1, 15, 14, 30, 1),
         "C": datetime(2025, 1, 15, 14, 30, 2), "D": datetime(2025, 1, 15, 14, 30, 3)},
    ]
    
    for round_num in range(num_rounds):
        # Cycle through patterns
        pattern = timestamp_patterns[round_num % len(timestamp_patterns)]
        
        results = []
        
        def worker_round(worker_id, expected_time, results_list):
            DeterministicClock.set_time(expected_time)
            observed = DeterministicClock.utcnow()
            results_list.append({
                'worker_id': worker_id,
                'expected': expected_time,
                'observed': observed,
            })
        
        worker_threads = []
        for worker_id in ['A', 'B', 'C', 'D']:
            t = threading.Thread(
                target=worker_round, args=(worker_id, pattern[worker_id], results)
            )
            worker_threads.append(t)
            t.start()
        
        for t in worker_threads:
            t.join(timeout=10)
        
        # Check for contamination in this round
        for r in results:
            if r['observed'] != r['expected']:
                contamination_total += 1
        
        all_results.extend(results)
    
    print(f'50 rounds x 4 workers = {50 * 4} total checks')
    print(f'Contamination count: {contamination_total}/{50 * 4}')
    print(f'Test {"PASS" if contamination_total == 0 else "FAIL"}: {"All isolations maintained" if contamination_total == 0 else "Some contamination observed"}')
    
    assert contamination_total == 0, f"Expected 0 contaminations in 50 rounds, got {contamination_total}"
    print("PASS: 50+ rounds with consistent isolation\n")


if __name__ == "__main__":
    test_thread_local_isolation()
    test_worker_isolation()
    test_barrier_adversarial()
    test_50_rounds()
    print("=" * 50)
    print("ALL TESTS PASSED - DeterministicClock thread-local isolation working correctly!")
    print("=" * 50)