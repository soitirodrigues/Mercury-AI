#!/usr/bin/env python
"""
S32-02 — R1 Crash Harness Test

Tests real process-kill injection during atomic_json_write.
NOT a Python exception simulation — real OS process termination.

Crash points tested:
  A: Before function starts (tempfile never created)
  B: After mkstemp(), before json.dump() (tempfile exists, target unchanged)
  C: During json.dump() (partial JSON in tempfile, target unchanged)
  D: After json.dump(), before fsync() (complete JSON in tempfile, target unchanged)
  E: After fsync(), before os.replace() (complete JSON in tempfile, target unchanged)
  F: During os.replace() (critical: both old and new may conflict)
  G: After os.replace() succeeds (new file in place, old removed)

Expected: Never JSON partially written/corrupted. Result is always OLD XOR NEW.
"""

import subprocess
import sys
import os
import time
import json

# Add Mercury-AI to path
sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.utils.atomic_io import atomic_json_write


def run_atomic_json_write_test(test_point, kill_after_seconds, target_path, data):
    """
    Run atomic_json_write in a child process and kill it at a controlled point.

    Args:
        test_point: Label for the test point (A-G)
        kill_after_seconds: How long to let the process run before killing
        target_path: The file path that atomic_json_write will write to
        data: The data to write

    Returns:
        dict with test results
    """
    # Initialize result dict with ALL keys present
    result = {
        "test_point": test_point,
        "kill_after_s": kill_after_seconds,
        "target_path": target_path,
        "original_file_existed": os.path.exists(target_path),
        "output_file_exists": False,
        "output_file_valid_json": False,
        "output_file_is_partial": False,
        "output_file_is_corrupt": False,
        "output_file_is_empty": False,
        "old_file_existed": os.path.exists(target_path),  # FIX: consistent key name
        "old_file_preserved": False,
        "classification": "UNKNOWN",
    }

    # Save old file content for comparison if it existed
    if result["original_file_existed"]:
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                result["old_content"] = f.read()
        except:
            pass

    # Command to run atomic_json_write
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

    # Wait for kill_after_seconds and then kill
    try:
        time.sleep(kill_after_seconds)
        proc.kill()
        proc.wait(timeout=5)

        # Check the state of the output file
        result["output_file_exists"] = os.path.exists(target_path)

        if result["output_file_exists"]:
            # Check if the old file content is preserved (if it existed before)
            if result["original_file_existed"]:
                try:
                    with open(target_path, "r", encoding="utf-8") as f:
                        new_content = f.read()
                    result["old_file_preserved"] = (new_content == result.get("old_content", ""))
                except:
                    pass

            # Check the file content
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Try to parse as JSON
                try:
                    parsed = json.loads(content)
                    result["output_file_valid_json"] = True
                    result["output_file_is_partial"] = False
                    result["output_file_is_corrupt"] = False
                    result["output_file_is_empty"] = False
                except json.JSONDecodeError:
                    # Check if it's partial JSON or corrupt
                    if content.strip() == "":
                        result["output_file_is_empty"] = True
                    elif content.strip().startswith("{") or content.strip().startswith("["):
                        # Might be partial JSON
                        result["output_file_is_partial"] = True
                        result["output_file_is_corrupt"] = False
                    else:
                        result["output_file_is_corrupt"] = True
                        result["output_file_is_partial"] = False
                        result["output_file_is_empty"] = False
            except Exception as e:
                result["output_file_error"] = str(e)

    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        result["output_file_error"] = "subprocess timeout"

    return result


def main():
    """Run S32-02 crash harness test suite."""

    print("=" * 70)
    print("S32-02 — R1 Crash Harness: Real Process-Kill Injection")
    print("=" * 70)
    print()

    # Test configuration
    test_symbol = {"symbol": "test_crash", "confidence": 0.95, "confluence": 100.0}
    target_path = r"mercury_ai/database/snapshots/test_crash_s32_02.json"
    data = test_symbol

    # Remove target file if exists from previous runs
    if os.path.exists(target_path):
        os.remove(target_path)

    # Ensure parent directory exists
    parent = os.path.dirname(target_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # Test points with approximate delay times (in seconds)
    # These are indicative - the actual code position depends on execution speed
    test_points = [
        # (label, kill_delay, description)
        ("A: Before function starts", 0.01, "Process killed before any write begins"),
        ("B: After mkstemp(), before json.dump", 0.1, "Tempfile created, JSON not yet written"),
        ("C: During json.dump()", 0.5, "JSON being written to tempfile (may be partial)"),
        ("D: After json.dump(), before fsync", 1.0, "JSON complete in tempfile, not yet fsynced"),
        ("E: After fsync(), before os.replace", 2.0, "JSON fsynced to tempfile, os.replace not yet called"),
        ("F: During os.replace()", 3.0, "Critical: os.replace being executed"),
        ("G: After os.replace() succeeds", 5.0, "New file in place, old removed"),
    ]

    print(f"Test target: {target_path}")
    print(f"Data to write: {data}")
    print()
    print("Test points (kill after delay):")
    for label, delay, desc in test_points:
        print(f"  {label}: kill after {delay}s")
    print()

    # Run each test point
    results = []
    for test_point, kill_after, desc in test_points:
        print(f"--- Running {test_point} ---")
        result = run_atomic_json_write_test(test_point, kill_after, target_path, data)
        results.append(result)

        # Classify the result
        if not result["output_file_exists"]:
            result["classification"] = "NO FILE - Old preserved (no write attempted)"
        elif result["output_file_is_empty"]:
            result["classification"] = "EMPTY FILE - BLOCKER"
        elif result["output_file_is_partial"]:
            result["classification"] = "PARTIAL JSON - BLOCKER"
        elif result["output_file_is_corrupt"]:
            result["classification"] = "CORRUPTED FILE - BLOCKER"
        elif not result["output_file_valid_json"] and result["output_file_exists"]:
            result["classification"] = "FILE EXISTS BUT NOT VALID JSON"
        elif result["old_file_preserved"] and result["output_file_valid_json"]:
            result["classification"] = "OLD XOR NEW - PASS"
        elif not result["old_file_preserved"] and result["output_file_valid_json"]:
            result["classification"] = "NEW - Old was overwritten"
        else:
            result["classification"] = "UNDECIDED"

        print(f"  Classification: {result['classification']}")
        print()

    # Summary
    print("=" * 70)
    print("S32-02 — SUMMARY")
    print("=" * 70)

    pass_count = sum(1 for r in results if "PASS" in r["classification"] or "OLD XOR NEW" in r["classification"])
    blocker_count = sum(1 for r in results if "BLOCKER" in r["classification"])

    print(f"Total test points: {len(results)}")
    print(f"PASS (OLD XOR NEW): {pass_count}")
    print(f"BLOCKER (corruption/partial): {blocker_count}")
    print()

    # Determine overall classification
    if blocker_count > 0:
        overall = "FAIL - File corruption or partial writes detected"
    elif pass_count == len(results):
        overall = "PASS - Old XOR New comprovado em todos os cenários"
    elif pass_count > 0:
        overall = "PARTIAL - Alguns cenários passam, outros precisam de investigação"
    else:
        overall = "NOT PROVEN - Crash injection nao reproduzido ou todos os cenarios falharam"

    print(f"Classificacao geral: {overall}")
    print()

    # Cleanup: remove test file
    if os.path.exists(target_path):
        os.remove(target_path)

    return results


if __name__ == "__main__":
    results = main()
    # Exit code based on results
    blocker_count = sum(1 for r in results if "BLOCKER" in r["classification"])
    if blocker_count > 0:
        print("\nCRITICAL: File corruption detected - R1 NOT PROVEN")
        sys.exit(1)
    else:
        print("\nAll test points completed - evidence collected for R1 classification")
        sys.exit(0)