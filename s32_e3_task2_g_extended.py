#!/usr/bin/env python
"""
S32-E3-TASK2-v2 — G determinístico with extended wait

Testa o ponto G com espera estendida após HANDHAKE_READY 
para permitir que os.replace() retries completem.
"""

import sys
import os
import json
import subprocess
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY


def run_g_deterministic_with_retries(target_path, data, handshake_wait=1.0, post_handshake_wait=3.0):
    """
    Run G with extended post-handshake wait to allow os.replace() retries.
    
    Strategy:
    1. Start child with handshake_mode=True
    2. Wait for HANDHAKE_READY (child signaled ready to replace)
    3. Wait additional post_handshake_wait seconds (allow retries to complete)
    4. Kill the process
    5. External observation
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
    handshake_observed = False
    start_time = time.time()

    while time.time() - start_time < 5.0:  # max 5s to observe handshake
        status_file = r"temp_s32_status.json"
        if os.path.exists(status_file):
            try:
                with open(status_file, "r", encoding="utf-8") as f:
                    marker = f.read().strip()
                if marker == HANDHAKE_READY:
                    handshake_observed = True
                    result["handshake_marker_written"] = True
                    print(f"  HANDHAKE_READY observed at {time.time()-start_time:.2f}s")
                    break
            except Exception:
                pass
        time.sleep(0.2)

    if not handshake_observed:
        print("  WARNING: HANDHAKE_READY not observed within 5s")
        proc.kill()
        proc.wait()
        result["parent_observation"] = "HANDHAKE_TIMEOUT"
        return result

    # Phase 2: Wait post-handshake to allow os.replace() retries to complete
    # The atomic_json_write has max_retries=5 with exponential backoff:
    # 0.05 + 0.1 + 0.2 + 0.4 + 0.8 = ~1.55s total retry time
    print(f"  Waiting {post_handshake_wait}s after HANDHAKE_READY for retries to complete...")
    time.sleep(post_handshake_wait)

    # Phase 3: Kill the process
    print("  Killing process after post-handshake wait")
    proc.kill()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

    # Phase 4: External observation
    result["output_file_exists"] = os.path.exists(target_path)

    if result["output_file_exists"]:
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                new_content = f.read()

            try:
                parsed = json.loads(new_content)
                result["output_file_valid_json"] = True
                result["output_file_is_partial"] = False
                result["output_file_is_corrupt"] = False

                # Classification
                if "old_content" in result and new_content == result["old_content"]:
                    result["old_file_preserved"] = True
                    result["parent_observation"] = "OLD"
                else:
                    result["parent_observation"] = "NEW"
                    result["classification"] = "NEW WRITTEN - os.replace completed ✓"
            except json.JSONDecodeError:
                result["output_file_is_corrupt"] = True
                result["parent_observation"] = "UNKNOWN (CORRUPT)"
                result["classification"] = "CORRUPTED FILE - BLOCKER ✗"
        except Exception as e:
            result["output_file_error"] = str(e)
            result["parent_observation"] = "UNKNOWN (ERROR)"
    else:
        if "old_content" in result:
            result["parent_observation"] = "OLD (original preserved, no replace effective)"
        else:
            result["parent_observation"] = "UNKNOWN (no file, no original)"

    # Cleanup
    status_file = r"temp_s32_status.json"
    if os.path.exists(status_file):
        os.remove(status_file)

    print(f"  Result: parent_observation={result['parent_observation']}")
    return result


def run_g_extended_wait_cycles(num_cycles=5, post_handshake_wait=5.0):
    """Run G cycles with extended post-handshake wait."""
    results = []

    target = r"C:\Projetos\Mercury-AI\test_s32_g_extended.json"

    print(f"Running S32-E3 Task 2 v2: G determinístico com espera estendida")
    print(f"Post-handshake wait: {post_handshake_wait}s (allows ~1.55s of retries)")
    print("=" * 60)

    for cycle in range(1, num_cycles + 1):
        # Create target with initial content
        if not os.path.exists(target):
            with open(target, "w", encoding="utf-8") as f:
                f.write(json.dumps({"initial": "data", "cycle": cycle}, indent=2))

        test_data = {"test": "G-extended", "cycle": cycle}

        print(f"\nCycle {cycle}/{num_cycles}...")

        result = run_g_deterministic_with_retries(
            target_path=target, data=test_data,
            handshake_wait=1.0, post_handshake_wait=post_handshake_wait
        )
        results.append(result)

        obs = result.get("parent_observation", "UNKNOWN")
        print(f"  Observation: {obs}")

        time.sleep(0.3)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    observations = [r.get("parent_observation", "UNKNOWN") for r in results]
    old_count = observations.count("OLD")
    new_count = observations.count("NEW")
    print(f"Total: {len(results)} | OLD: {old_count} | NEW: {new_count}")

    if os.path.exists(target):
        os.remove(target)

    return results


if __name__ == "__main__":
    results = run_g_extended_wait_cycles(num_cycles=5, post_handshake_wait=5.0)
    print("\nDetailed results:")
    for r in results:
        print(f"  obs={r.get('parent_observation')}, valid_JSON={r.get('output_file_valid_json')}, "
              f"old_preserved={r.get('old_file_preserved')}, cls={r.get('classification')}")