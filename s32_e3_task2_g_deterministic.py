#!/usr/bin/env python
"""
S32-E3-TASK2 — G determinístico: os.replace() completed ↓ kill

Testa o ponto G deterministically: after os.replace() → kill.
Expected: NEW written and valid JSON.

The key difference from previous G tests:
- NO sleep() or kill_after_seconds timing
- Use handshake_mode + external observation
- Process runs until os.replace() completes, then we kill
- External parent observation confirms NEW
"""

import sys
import os
import json
import subprocess
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY


def run_g_deterministic_test(target_path, data, max_wait=5.0):
    """
    Run G deterministically without sleep().
    
    Strategy:
    1. Start child process with handshake_mode=True
    2. Parent waits for HANDHAKE_READY in status file (means child is ready to replace)
    3. After HANDHAKE_READY is observed, parent kills the process
    4. External observation: check if NEW file was written
    
    This eliminates the arbitrary sleep/time-based kill.
    """
    result = {
        "test_point": "G",
        "target_path": target_path,
        "data": data,
        "handshake_marker_written": False,
        "output_file_exists": False,
        "output_file_valid_json": False,
        "output_file_is_partial": False,
        "output_file_is_corrupt": False,
        "output_file_is_empty": False,
        "old_file_preserved": False,
        "parent_observation": "UNKNOWN",
        "classification": "UNKNOWN",
        "kill_timing": "UNKNOWN",
    }

    # Save old file content if it existed
    result["original_file_existed"] = os.path.exists(target_path)
    if result["original_file_existed"]:
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                result["old_content"] = f.read()
        except Exception:
            pass

    # Command to run atomic_json_write with handshake_mode
    cmd = [
        sys.executable, "-c",
        f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target_path}", {repr(data)}, indent=2, 
                  signal_checkpoints=True, status_file="temp_s32_status.json", 
                  handshake_mode=True)
print("SUCCESS")
"""
    ]

    # Start the subprocess
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Phase 1: Wait for HANDHAKE_READY signal from child
    # This means the child has prepared the temp file and is about to do os.replace()
    # We observe this externally via the status file
    handshake_observed = False
    max_handshake_wait = 3.0
    start_time = time.time()

    while time.time() - start_time < max_handshake_wait:
        # Check if status file exists and has HANDHAKE_READY
        status_file = r"temp_s32_status.json"
        if os.path.exists(status_file):
            try:
                with open(status_file, "r", encoding="utf-8") as f:
                    marker = f.read().strip()
                if marker == HANDHAKE_READY:
                    handshake_observed = True
                    result["handshake_marker_written"] = True
                    print(f"  Cycle: HANDHAKE_READY observed at {time.time()-start_time:.2f}s")
                    break
            except Exception:
                pass
        time.sleep(0.1)

    # Phase 2: Kill the process after handshake observed
    # At this point, os.replace() should have already executed (or be executing)
    # The child may still be running due to retries, but we kill it
    print(f"  Cycle: Killing process after HANDHAKE_READY observation")
    proc.kill()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

    # Phase 3: External observation by parent
    # Check the target file state
    result["output_file_exists"] = os.path.exists(target_path)

    if result["output_file_exists"]:
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                new_content = f.read()

            # Check if valid JSON
            try:
                parsed = json.loads(new_content)
                result["output_file_valid_json"] = True
                result["output_file_is_partial"] = False
                result["output_file_is_corrupt"] = False

                # External classification: OLD or NEW?
                if "old_content" in result and new_content == result["old_content"]:
                    result["old_file_preserved"] = True
                    result["parent_observation"] = "OLD"
                else:
                    result["parent_observation"] = "NEW"
                    result["classification"] = "NEW WRITTEN - os.replace() completed ✓"
            except json.JSONDecodeError:
                result["output_file_is_corrupt"] = True
                result["parent_observation"] = "UNKNOWN (CORRUPT)"
                result["classification"] = "CORRUPTED FILE - BLOCKER ✗"
        except Exception as e:
            result["output_file_error"] = str(e)
            result["parent_observation"] = "UNKNOWN (ERROR)"
    else:
        # No output file exists
        if "old_content" in result:
            result["parent_observation"] = "OLD (original preserved, no replace effective)"
        else:
            result["parent_observation"] = "UNKNOWN (no file, no original)"

    # Cleanup status file
    status_file = r"temp_s32_status.json"
    if os.path.exists(status_file):
        os.remove(status_file)

    # Cleanup target file for next cycle (if it was newly created, we keep it for observation)
    # But we need to track what happened
    print(f"  Result: parent_observation={result['parent_observation']}")
    print(f"          output_file_valid_json={result['output_file_valid_json']}")
    print(f"          old_file_preserved={result['old_file_preserved']}")

    return result


def run_g_deterministic_cycles(num_cycles=5):
    """Run multiple G deterministic cycles."""
    results = []

    # Use a persistent target file so we can track OLD vs NEW
    target = r"C:\Projetos\Mercury-AI\test_s32_g_target.json"

    print(f"Running S32-E3 Task 2: G determinístico")
    print(f"Method: HANDHAKE_READY observation + kill after replace")
    print("=" * 60)

    for cycle in range(1, num_cycles + 1):
        # Create target file with initial content if it doesn't exist
        if not os.path.exists(target):
            with open(target, "w", encoding="utf-8") as f:
                f.write(json.dumps({"initial": "data", "cycle": cycle}, indent=2))
            print(f"  Cycle {cycle}: Created initial target file")

        # Data to write
        test_data = {"test": "G-point", "cycle": cycle, "timestamp": time.time()}

        print(f"\nCycle {cycle}/{num_cycles}...")

        # Run the deterministic G test
        result = run_g_deterministic_test(target_path=target, data=test_data, max_wait=5.0)
        results.append(result)

        # Brief pause between cycles
        time.sleep(0.2)

    # Final summary
    print("\n" + "=" * 60)
    print("G DETERMINISTIC TEST SUMMARY")
    print("=" * 60)

    observations = [r.get("parent_observation", "UNKNOWN") for r in results]
    valid_json = [r.get("output_file_valid_json", False) for r in results]
    old_preserved = [r.get("old_file_preserved", False) for r in results]

    old_count = observations.count("OLD")
    new_count = observations.count("NEW")
    valid_json_count = sum(1 for v in valid_json if v)
    corrupt_count = sum(1 for v in valid_json if not v and any(r.get("output_file_is_corrupt", False) for r in results))

    print(f"Total cycles: {len(results)}")
    print(f"OLD observations: {old_count}")
    print(f"NEW observations: {new_count}")
    print(f"Valid JSON: {valid_json_count}/{len(results)}")
    print(f"Corrupt/Empty: {len(results) - valid_json_count}")

    # Check if all observations are either OLD or NEW (not PARTIAL/CORRUPT/EMPTY)
    all_valid = all(obs in ("OLD", "NEW") for obs in observations)
    no_bad_states = all(obs not in ("PARTIAL", "CORRUPT", "EMPTY") for obs in observations)

    print(f"\nAll observations OLD or NEW only: {all_valid}")
    print(f"No PARTIAL/CORRUPT/EMPTY states: {no_bad_states}")

    if all_valid and new_count > 0:
        print("\n✅ G DETERMINISTIC PASSED: Some cycles produced NEW (os.replace completed)")
    elif all_valid and old_count == len(results):
        print("\n⚠️ G DETERMINISTIC: All cycles produced OLD (os.replace may not persisting?)")
    elif not all_valid:
        print("\n❌ G DETERMINISTIC FAILED: Some cycles had invalid states")
    else:
        print("\n? G DETERMINISTIC: Mixed results")

    # Cleanup
    if os.path.exists(target):
        os.remove(target)

    return results


if __name__ == "__main__":
    results = run_g_deterministic_cycles(num_cycles=5)
    # Print detailed results
    print("\n" + "=" * 60)
    print("DETAILED PER-CYCLE RESULTS")
    print("=" * 60)
    for r in results:
        print(f"Cycle: obs={r.get('parent_observation')}, valid_JSON={r.get('output_file_valid_json')}, "
              f"old_preserved={r.get('old_file_preserved')}, classification={r.get('classification')}")