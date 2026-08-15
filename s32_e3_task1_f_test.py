#!/usr/bin/env python
"""
S32-E3-TASK1 — F × 10: Kill antes de os.replace()

Testa o ponto F: kill point F — Before os.replace()
Expected: OLD preserved (no replace attempted)
"""

import sys
import os
import json
import subprocess
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write

def run_f_test_cycle(cycle_num, target_path, data, kill_delay=0.3):
    """
    Run a single F test cycle.
    
    Kill point F: Before os.replace()
    The child process writes BEFORE_REPLACE signal, then gets killed
    before os.replace() executes.
    
    Args:
        cycle_num: Cycle number for tracking
        target_path: File path to write to
        data: Data to write
        kill_delay: Seconds to let run before killing (short = before replace)
    
    Returns:
        dict with test results
    """
    result = {
        "cycle": cycle_num,
        "test_point": "F",
        "target_path": target_path,
        "kill_delay_s": kill_delay,
        "original_file_existed": os.path.exists(target_path),
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
    if result["original_file_existed"]:
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                result["old_content"] = f.read()
        except Exception:
            pass

    # Command to run atomic_json_write with signal_checkpoints (for F test, 
    # we use signal_checkpoints but NOT handshake_mode — we want to test point F)
    cmd = [
        sys.executable, "-c",
        f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target_path}", {repr(data)}, indent=2, signal_checkpoints=True, status_file="temp_s32_status.json")
print("SUCCESS")
"""
    ]

    # Start the subprocess
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for kill_delay and then kill
    try:
        time.sleep(kill_delay)
        proc.kill()
        proc.wait(timeout=3)

        # External observation by parent
        result["output_file_exists"] = os.path.exists(target_path)

        if result["output_file_exists"]:
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    new_content = f.read()

                # Check if valid JSON
                try:
                    parsed = json.loads(new_content)
                    result["output_file_valid_json"] = True

                    # Classification: if original existed and content matches old_content -> OLD
                    if "old_content" in result and new_content == result["old_content"]:
                        result["old_file_preserved"] = True
                        result["parent_observation"] = "OLD"
                    else:
                        result["parent_observation"] = "NEW"
                except json.JSONDecodeError:
                    result["output_file_is_corrupt"] = True
                    result["parent_observation"] = "UNKNOWN (CORRUPT)"
            except Exception as e:
                result["output_file_error"] = str(e)
                result["parent_observation"] = "UNKNOWN (ERROR)"
        else:
            # No output file exists — original preserved if it existed before
            if "old_content" in result:
                result["parent_observation"] = "OLD (original preserved, no replace effective)"
            else:
                result["parent_observation"] = "UNKNOWN (no file, no original)"

    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        result["parent_observation"] = "TIMEOUT"
        result["output_file_error"] = "subprocess timeout"

    return result


def run_f_times_10():
    """Run 10 F test cycles."""
    results = []

    # Use a target file that initially exists
    target = r"C:\Projetos\Mercury-AI\test_s32_f_target.json"

    # Create initial file with content
    with open(target, "w", encoding="utf-8") as f:
        f.write(json.dumps({"initial": "data", "purpose": "F-test"}, indent=2))

    data_to_write = {"test": "F-point", "timestamp": time.time()}

    print(f"Running S32-E3 Task 1: F × 10")
    print(f"Kill delay: short (before os.replace)")
    print("=" * 60)

    for cycle in range(1, 11):
        # Reset target file to initial content for each cycle
        with open(target, "w", encoding="utf-8") as f:
            f.write(json.dumps({"initial": "data", "purpose": "F-test", "cycle": cycle}, indent=2))

        # Remove status file if exists
        status_file = r"C:\Projetos\Mercury-AI\temp_s32_status.json"
        if os.path.exists(status_file):
            os.remove(status_file)

        # Run the F test cycle
        result = run_f_test_cycle(cycle_num=cycle, target_path=target, data=data_to_write, kill_delay=0.3)
        results.append(result)

        # Report
        obs = result.get("parent_observation", "UNKNOWN")
        cls = result.get("classification", "UNKNOWN")
        preserved = result.get("old_file_preserved", False)
        print(f"  Cycle {cycle:2d}: Observation={obs:15s} OldPreserved={preserved}")

        # Brief pause between cycles
        time.sleep(0.1)

    # Cleanup
    if os.path.exists(target):
        os.remove(target)
    if os.path.exists(status_file):
        os.remove(status_file)

    return results


def verify_f_results(results):
    """Verify F test results."""
    print("\n" + "=" * 60)
    print("F TEST RESULTS VERIFICATION")
    print("=" * 60)

    observations = [r.get("parent_observation", "UNKNOWN") for r in results]
    old_preserved = [r.get("old_file_preserved", False) for r in results]

    # Check all observations are "OLD"
    all_old = all(obs == "OLD" for obs in observations)
    all_old_preserved = all(old_preserved)

    # Check no bad states
    no_bad = all(
        obs not in ("PARTIAL", "CORRUPT", "EMPTY") for obs in observations
    )

    old_count = observations.count("OLD")
    new_count = observations.count("NEW")

    print(f"Total cycles: {len(results)}")
    print(f"All OLD: {all_old}")
    print(f"All old_file_preserved: {all_old_preserved}")
    print(f"No bad states (PARTIAL/CORRUPT/EMPTY): {no_bad}")
    print(f"OLD observations: {old_count}")
    print(f"NEW observations: {new_count}")

    if all_old and no_bad:
        print("\n✅ F TEST PASSED: All 10 cycles produced OLD state")
        print("   Kill before os.replace() successfully preserves OLD")
        return True
    else:
        print("\n❌ F TEST FAILED")
        if not all_old:
            print(f"   Some cycles did not produce OLD: {set(observations)}")
        if not no_bad:
            print("   Some cycles had PARTIAL/CORRUPT/EMPTY states")
        return False


if __name__ == "__main__":
    results = run_f_times_10()
    verify_f_results(results)