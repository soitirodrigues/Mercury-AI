#!/usr/bin/env python
"""Debug script to check result dictionary keys"""
import subprocess
import sys
import os
import time
import json

sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from mercury_ai.utils.atomic_io import atomic_json_write

# Simulate what the test does
target = r'test_s32_e3_target.json'
status_file = r'test_s32_e3_status.json'

# Remove files if exist
if os.path.exists(target): os.remove(target)
if os.path.exists(status_file): os.remove(status_file)

# Command to run atomic_json_write with handshake_mode
cmd = [
    sys.executable, "-c",
    f'''
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target}", {{{"test": "data"}}}, indent=2, 
                  signal_checkpoints=True, status_file="{status_file}", 
                  handshake_mode=True)
print("SUCCESS")
'''
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait and kill
try:
    time.sleep(1)
    proc.kill()
    proc.wait(timeout=5)
    
    # Now check the result dictionary structure - simulate what the test does
    result = {
        "cycle_id": 1,
        "test_point": "G",
        "kill_after_s": 1,
        "target_path": target,
        "original_file_existed": os.path.exists(target),
        "output_file_exists": False,
        "output_file_valid_json": False,
        "output_file_is_partial": False,
        "output_file_is_corrupt": False,
        "output_file_is_empty": False,
        "old_file_preserved": False,
        "handshake_marker_written": False,
        "replace_confirmed": False,  # G-BRIDGE-03: true REPLACE_CONFIRMED=YES
        "target_is_NEW": False,  # G-BRIDGE-03: target detected as NEW
        "parent_observation": "UNKNOWN",
        "classification": "UNKNOWN",
        "kill_aftermath_state": "UNKNOWN",
    }
    
    # Check handshake marker
    handshake_valid = False
    if os.path.exists(status_file):
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                marker_content = f.read().strip()
            if marker_content == "READY_TO_REPLACE":
                handshake_valid = True
                result["handshake_marker_written"] = True
        except Exception:
            pass
    
    print(f"handshake_valid: {handshake_valid}")
    print(f"result keys: {list(result.keys())}")
    print(f"replace_confirmed in result: {'replace_confirmed' in result}")
    print(f"replace_confirmed value: {result.get('replace_confirmed', 'KEY MISSING')}")
    print(f"target_is_NEW value: {result.get('target_is_NEW', 'KEY MISSING')}")
    print(f"parent_observation value: {result.get('parent_observation', 'KEY MISSING')}")
    
    # Now try the classification code that was failing
    if handshake_valid and result["output_file_valid_json"]:
        classification = (
            f"G-BRIDGE SEQUENCE: READY→REPLACE_CONFIRMED→KILL→NEW "
            f"(handshake_valid={handshake_valid}, "
            f"replace_confirmed={result['replace_confirmed']}, "
            f"target_is_NEW={result['target_is_NEW']}, "
            f"parent_observation={result['parent_observation']})"
        )
        print(f"Classification: {classification}")
    else:
        print("Not in first branch")
        
except subprocess.TimeoutExpired:
    proc.kill()
    proc.wait()
    print("Timeout expired")