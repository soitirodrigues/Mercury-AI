#!/usr/bin/env python
"""Test script for S32-E3 child process communication.

Runs the child script, captures events, and sends commands via stdin.
"""

import sys
import os
import json
import time
import subprocess
import tempfile

sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.utils.atomic_io import (
    atomic_json_write,
)


def main():
    # Create evidence file (fresh)
    evidence_path = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\evidence_live_test.jsonl"
    with open(evidence_path, "w", encoding="utf-8") as f:
        f.write("")
    
    # Create target file
    target_path = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\bridge_target_test.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"initial": "data"}, f, ensure_ascii=False, indent=2)
    
    # Create data file for child
    data_path = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\child_data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump({"cycle": 1, "objective": "test_bridge"}, f, ensure_ascii=False, indent=2)
    
    # Child script path
    child_script = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\child_script.py"
    
    # Run child process
    cmd = [
        sys.executable, child_script,
        "--target", target_path,
        "--data-file", data_path,
        "--cycle", "1",
        "--evidence", evidence_path
    ]
    
    print(f"Starting child process: {cmd}")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Step 1: Read READY event from stdout
    print("\n--- Waiting for READY event ---")
    ready_line = proc.stdout.readline().strip()
    print(f"Got from child: {ready_line}")
    
    if ready_line.startswith("READY:"):
        pid = ready_line.split(":")[1]
        print(f" PID: {pid}")
    else:
        print("ERROR: Did not receive READY event")
        proc.terminate()
        return
    
    # Step 2: Send GO_REPLACE command
    print("\n--- Sending GO_REPLACE ---")
    proc.stdin.write("GO_REPLACE\n")
    proc.stdin.flush()
    print("GO_REPLACE sent")
    
    # Step 3: Read REPLACE_DONE event from stdout
    print("\n--- Waiting for REPLACE_DONE event ---")
    replace_line = proc.stdout.readline().strip()
    print(f"Got from child: {replace_line}")
    
    if replace_line.startswith("REPLACE_DONE:"):
        pid = replace_line.split(":")[1]
        print(f" PID: {pid}")
    else:
        print("ERROR: Did not receive REPLACE_DONE event")
    
    # Step 4: Send KILL command
    print("\n--- Sending KILL ---")
    proc.stdin.write("KILL\n")
    proc.stdin.flush()
    print("KILL sent")
    
    # Step 5: Read KILL_ACK from stdout
    print("\n--- Waiting for KILL_ACK ---")
    ack_line = proc.stdout.readline().strip()
    print(f"Got from child: {ack_line}")
    
    if ack_line == "KILL_ACK":
        print("KILL ACK received successfully")
    else:
        print(f"Expected KILL_ACK, got: {ack_line}")
    
    # Step 6: Wait for process to finish
    print("\n--- Waiting for process to finish ---")
    proc.wait(timeout=5.0)
    print(f"Process exited with code: {proc.returncode}")
    
    # Read evidence file
    print("\n--- Evidence file content ---")
    if os.path.exists(evidence_path):
        with open(evidence_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    else:
        print("Evidence file not found")
    
    # Cleanup
    try:
        proc.stdout.close()
        proc.stdin.close()
    except:
        pass
    
    # Compare with original mercury_ai utils
    print("\n--- Test complete ---")


if __name__ == "__main__":
    main()