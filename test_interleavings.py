"""Test script for DeterministicClock interleavings adversarial patterns."""
import sys
import threading
import time
from datetime import datetime

sys.path.insert(0, r'.')
from mercury_ai.utils.deterministic_clock import DeterministicClock


def test_interleavings():
    """Test different thread interleaving patterns with variable sleeps/barriers."""
    print("=== S32-D-07: Interleavings Adversarial Test ===")
    DeterministicClock.reset()
    
    num_iterations = 20
    total_contamination = 0
    
    for iteration in range(num_iterations):
        DeterministicClock.reset()
        
        # Create 4 threads with different times
        results = {}
        results_lock = threading.Lock()
        
        def worker(worker_id, expected_time, delay_before=0, delay_after=0):
            """Worker with variable delays to increase scheduling space."""
            if delay_before > 0:
                time.sleep(delay_before)
            
            DeterministicClock.set_time(expected_time)
            
            # Read clock immediately after set
            observed = DeterministicClock.utcnow()
            
            if delay_after > 0:
                time.sleep(delay_after)
            
            with results_lock:
                results[worker_id] = {
                    'expected': expected_time,
                    'observed': observed,
                }
        
        # Create threads with varying delays to simulate interleavings
        # Each worker gets (delay_before, delay_after) in seconds
        worker_delays = {
            'A': (0, 0),
            'B': (0, 0),
            'C': (0.01, 0.005),
            'D': (0.005, 0.01),
        }
        
        threads = []
        expected_times = [
            datetime(2025, 1, 15, 10, 0, 0),
            datetime(2025, 1, 15, 10, 0, 1),
            datetime(2025, 1, 15, 10, 0, 2),
            datetime(2025, 1, 15, 10, 0, 3),
        ]
        
        for i, worker_id in enumerate(['A', 'B', 'C', 'D']):
            delay_before, delay_after = worker_delays[worker_id]
            t = threading.Thread(
                target=worker, 
                args=(worker_id, expected_times[i], delay_before, delay_after)
            )
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=10)
        
        # Check for contamination - each worker should see its own expected time
        iteration_contamination = 0
        for worker_id in ['A', 'B', 'C', 'D']:
            if worker_id in results:
                if results[worker_id]['expected'] != results[worker_id]['observed']:
                    iteration_contamination += 1
                    print(f"  Iteration {iteration}: {worker_id} contamination detected")
        
        total_contamination += iteration_contamination
        
        if iteration % 5 == 0:
            print(f"Iteration {iteration}: contamination={iteration_contamination}")
    
    print(f"\nTotal contamination across {num_iterations} iterations: {total_contamination}/{num_iterations * 4} checks")
    print(f"Test {'PASS' if total_contamination == 0 else 'FAIL'}: {'No cross-contamination in any interleaving pattern' if total_contamination == 0 else 'Some contamination observed'}")
    
    assert total_contamination == 0, f"Expected 0 contaminations across {num_iterations} iterations, got {total_contamination}"
    print("PASS: All interleaving patterns maintain clock isolation\n")


if __name__ == "__main__":
    test_interleavings()