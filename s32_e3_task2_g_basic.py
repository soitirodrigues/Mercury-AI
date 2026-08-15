#!/usr/bin/env python
"""
S32-E3-TASK2-v4 — G básico: atomic_json_write normal (sem handshake_mode)

Testa o ponto G com atomic_json_write normal (sem handshake_mode).
Este teste prova que o mecanismo funciona quando permitido completar.
"""

import sys
import os
import json
import subprocess
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')


def run_g_basic_test(target_path, data, max_wait=5.0):
    """
    Run G: atomic_json_write normal, process runs to completion.
    
    No handshake_mode, no crash kill - just run the function and wait for completion.
    """
    result = {
        "test_point": "G_basic",
        "target_path": target_path,
        "data": data,
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

    # Command: basic atomic_json_write (no handshake_mode)
    cmd = [
        sys.executable, "-c",
        f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target_path}", {repr(data)}, indent=2)
print("SUCCESS")
"""
    ]

    # Start the subprocess
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for process to complete
    try:
        stdout, stderr = proc.communicate(timeout=max_wait)
        result["process_terminated_normally"] = (proc.returncode == 0)
        result["stderr"] = stderr.decode("latin-1", errors="replace") if stderr else ""
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        result["process_terminated_normally"] = False
        result["stderr"] = "TIMEOUT".latin-1 if hasattr(str, 'latin-1') else "TIMEOUT"
        result["timeout"] = max_wait

    # External observation
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
                    result["classification"] = "NEW WRITTEN - atomic_json_write completed ✓"
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

    return result


def run_g_basic_cycles(num_cycles=3):
    """Run G basic cycles."""
    results = []

    target = r"C:\Projetos\Mercury-AI\test_s32_g_basic.json"

    print(f"Running S32-E3 Task 2 v4: G - atomic_json_write normal")
    print("=" * 60)

    for cycle in range(1, num_cycles + 1):
        # Create target with initial content
        if not os.path.exists(target):
            with open(target, "w", encoding="utf-8") as f:
                f.write(json.dumps({"initial": "data", "cycle": cycle}, indent=2))

        test_data = {"test": "G-basic", "cycle": cycle}

        print(f"\nCycle {cycle}/{num_cycles}...")

        result = run_g_basic_test(target_path=target, data=test_data, max_wait=5.0)
        results.append(result)

        obs = result.get("parent_observation", "UNKNOWN")
        print(f"  Observation: {obs}")

        time.sleep(0.3)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY - G BASIC (no handshake)")
    print("=" * 60)
    observations = [r.get("parent_observation", "UNKNOWN") for r in results]
    old_count = observations.count("OLD")
    new_count = observations.count("NEW")
    print(f"Total: {len(results)} | OLD: {old_count} | NEW: {new_count}")

    if os.path.exists(target):
        os.remove(target)

    return results


if __name__ == "__main__":
    results = run_g_basic_cycles(num_cycles=3)
    print("\nDetailed results:")
    for r in results:
        print(f"  obs={r.get('parent_observation')}, valid_JSON={r.get('output_file_valid_json')}, "
              f"old_preserved={r.get('old_file_preserved')}, cls={r.get('classification')}, "
              f"proc_norm={r.get('process_terminated_normally')}")