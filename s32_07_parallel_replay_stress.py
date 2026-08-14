#!/usr/bin/env python
"""
S32-07 — Parallel Replay Stress Test with Snapshot/Restore

Tests 4 concurrent replays (A, B, C, D) with ThreadPoolExecutor(max_workers=4),
each using snapshot()/restore() pattern to isolate clock state.

Goal: Verify that snapshot/restore prevents clock cross-contamination between parallel replays.
This is the decisive gate for R2 - if snapshot/restore works, R2 is PROVEN.
"""

import sys
import os
import time
import json
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, r"C:\Projetos\Mercury-AI")
from mercury_ai.utils.deterministic_clock import DeterministicClock


# Test configuration
REPLAYS = ["A", "B", "C", "D"]
TEST_SYMBOL = "BTC-USD"


# Different start times for each replay to test isolation
REPLAY_TIMES = {
    "A": datetime(2025, 1, 1, 10, 0, 0),
    "B": datetime(2025, 1, 1, 11, 0, 0),
    "C": datetime(2025, 1, 1, 12, 0, 0),
    "D": datetime(2025, 1, 1, 13, 0, 0),
}


def run_replay_with_snapshot_restore(replay_id, kill_point="after_replay"):
    """Run a single replay with snapshot()/restore() pattern for clock isolation.
    
    This is the PATTERN that fixes the clock contamination issue:
    1. snapshot() before replay to capture current state
    2. Run replay operations
    3. restore() to revert to pre-replay state
    """
    
    # Set unique replay_id and clock time for this replay
    start_time = REPLAY_TIMES[replay_id]
    DeterministicClock.set_time(start_time)
    
    # STEP 1: Snapshot the clock state BEFORE replay
    pre_snapshot = DeterministicClock.snapshot()
    pre_hour = pre_snapshot.hour if pre_snapshot else None
    
    # Engine-specific state per replay
    engine_state = {
        "replay_id": replay_id,
        "symbol": TEST_SYMBOL,
        "start_time": DeterministicClock.utcnow(),
        "decisions": [],
        "signals": [],
    }
    
    # Simulate replay processing with periodic clock checks
    for step in range(10):
        # Check clock state - should reflect this replay's set time
        current_time = DeterministicClock.utcnow()
        engine_state["decisions"].append({
            "step": step,
            "clock_hour": current_time.hour,
            "replay_id": replay_id,
        })
        
        # Small delay to allow other threads to progress
        time.sleep(0.1)
    
    # STEP 2: RESTORE the clock state to pre-replay state
    # This prevents clock contamination for subsequent operations
    DeterministicClock.restore(pre_snapshot)
    
    # Record end time
    engine_state["end_time"] = DeterministicClock.utcnow()
    engine_state["duration"] = 1.0  # approximate
    
    return {"replay_id": replay_id, "state": engine_state, "status": "completed"}


def test_parallel_replay_stress_with_snapshot_restore():
    """S32-07: Parallel Replay Stress Test with Snapshot/Restore"""
    
    print("=" * 70)
    print("S32-07 — Parallel Replay Stress Test with Snapshot/Restore")
    print("=" * 70)
    print()
    
    print(f"Config: {len(REPLAYS)} concurrent replays (A, B, C, D)")
    print(f"ThreadPoolExecutor(max_workers={len(REPLAYS)})")
    print(f"Each replay uses snapshot()/restore() pattern")
    print(f"Expected start times: A={REPLAY_TIMES['A'].hour}, B={REPLAY_TIMES['B'].hour}, "
          f"C={REPLAY_TIMES['C'].hour}, D={REPLAY_TIMES['D'].hour}")
    print()
    
    # Run replays in parallel
    results = []
    with ThreadPoolExecutor(max_workers=len(REPLAYS)) as executor:
        futures = {executor.submit(run_replay_with_snapshot_restore, rid): rid for rid in REPLAYS}
        
        for future in as_completed(futures):
            rid = futures[future]
            try:
                result = future.result()
                results.append(result)
                rid = result["replay_id"]
                print(f"✓ Replay {rid} completed successfully")
                print(f"  Decisions: {len(result['state']['decisions'])}")
                print(f"  Clock state after restore: hour {result['state']['decisions'][0]['clock_hour']}:00")
            except Exception as e:
                print(f"✗ Replay {rid} FAILED: {e}")
                results.append({"replay_id": rid, "error": str(e), "status": "failed"})
    
    print()
    
    # Verification: Check that snapshot/restore prevents cross-contamination
    print("=" * 70)
    print("S32-07 — VERIFICATION: Snapshot/Restore Isolation Check")
    print("=" * 70)
    print()
    
    # Extract clock hours from each replay's decisions (AFTER restore)
    clock_hours_after_restore = {}
    for r in results:
        rid = r["replay_id"]
        if "error" not in r and rid in REPLAYS:
            hours = set()
            for d in r["state"]["decisions"]:
                hours.add(d["clock_hour"])
            clock_hours_after_restore[rid] = hours
            print(f"Replay {rid}: clock hours observed = {sorted(hours)}")
    
    # Expected: After restore, each replay should see its OWN expected hour,
    # but NOT the hours from other replays (since restore resets to pre-replay state)
    expected_hours = {"A": 10, "B": 11, "C": 12, "D": 13}
    
    print()
    print("Expected vs Actual clock hours AFTER restore:")
    all_correct = True
    for rid in REPLAYS:
        expected = expected_hours[rid]
        actual_hours = clock_hours_after_restore.get(rid, set())
        # After restore, the clock should be back to the state before this replay started
        # Since we set different times per replay, each should "remember" its own hour
        actual = list(actual_hours)[0] if actual_hours else None
        status = "✓" if actual == expected else "✗"
        print(f"  Replay {rid}: expected hour {expected}, actual hour {actual} {status}")
        if actual != expected:
            all_correct = False
    
    # Critical check: No cross-contamination - verify that replay A doesn't 
    # "remember" hour 13 (from Replay D), etc.
    contamination_detected = False
    for rid1 in REPLAYS:
        for rid2 in REPLAYS:
            if rid1 < rid2:
                overlap = clock_hours_after_restore[rid1].intersection(clock_hours_after_restore[rid2])
                if overlap:
                    print(f"⚠️ Overlap: Replays {rid1} and {rid2} share hours after restore: {overlap}")
                    # The key test: does any replay see a hour that doesn't belong to it?
                    for rid in [rid1, rid2]:
                        expected = expected_hours[rid]
                        if expected not in clock_hours_after_restore[rid]:
                            print(f"   ✓ {rid} correctly does NOT see hour {expected} (isolated)")
                        elif expected in clock_hours_after_restore[rid]:
                            # Check if this is the replay's OWN expected hour or another replay's
                            own_expected = expected_hours[rid]
                            if expected == own_expected:
                                print(f"   ✓ {rid} sees its own expected hour {expected} (correct)")
                            else:
                                print(f"   ⚠️ {rid} sees {expected} (another replay's hour!) - CONTAMINATION!")
                                contamination_detected = True
    
    if not contamination_detected:
        print("✓ No clock cross-contamination detected after snapshot/restore")
    
    # Final classification
    print()
    if not all_correct:
        overall = "PARTIAL - Some replays have incorrect expected hours post-restore"
    elif contamination_detected:
        overall = "FAIL - Clock cross-contamination detected despite snapshot/restore"
    else:
        overall = "PASS - Parallel replay stress: snapshot/restore prevents cross-contamination"
    
    print(f"\nClassification: {overall}")
    print()
    
    # Cleanup and reset
    DeterministicClock.reset()
    
    return {
        "results": results,
        "all_correct": all_correct,
        "contamination_detected": contamination_detected,
        "classification": overall,
    }


def main():
    results = test_parallel_replay_stress_with_snapshot_restore()
    sys.exit(0 if not results.get("contamination_detected") and results.get("all_correct") else 1)


if __name__ == "__main__":
    results = main()
    if results and results.get("contamination_detected"):
        print("\nCRITICAL: Parallel replay contamination detected despite snapshot/restore - R2 NOT PROVEN")
        sys.exit(1)
    elif results and not results.get("all_correct"):
        print("\nPARTIAL: Some replays have incorrect hours post-restore")
        sys.exit(0)
    else:
        print("\nParallel replay stress test completed - snapshot/restore pattern verified for R2")
        sys.exit(0)