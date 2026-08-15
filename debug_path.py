#!/usr/bin/env python
"""Debug script for G cycle file path"""
import sys
sys.path.insert(0, r'C:\Projetos\Mercury-AI')
import os
import json
import subprocess
import time

WORKSPACE = r"C:\Projetos\Mercury-AI"
TARGET_G = os.path.join(WORKSPACE, "test_s32_g_bridge.json")

print(f"WORKSPACE: {WORKSPACE}")
print(f"TARGET_G absolute: {TARGET_G}")
print(f"TARGET_G exists before: {os.path.exists(TARGET_G)}")

# Remove target if exists
if os.path.exists(TARGET_G):
    os.remove(TARGET_G)
    print("Removed target file")

# Now run a simple atomic_json_write test
cmd = [
    sys.executable, "-c",
    f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write('{TARGET_G}', '{{"test": "debug"}}', indent=2, signal_checkpoints=True, status_file="debug_g_status.json")
print("SUCCESS from subprocess")
"""
]

print(f"About to run subprocess with cwd={WORKSPACE}")
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORKSPACE)
stdout, stderr = proc.communicate(timeout=5.0)

print(f"STDOUT: {stdout.decode('utf-8', errors='replace')}")
print(f"STDERR: {stderr.decode('utf-8', errors='replace')}")
print(f"Return code: {proc.returncode}")

print(f"TARGET_G exists after: {os.path.exists(TARGET_G)}")

if os.path.exists(TARGET_G):
    with open(TARGET_G, 'r') as f:
        content = f.read()
    print(f"TARGET_G content: {content}")
else:
    print("TARGET_G does NOT exist after subprocess!")
    
    # Check what files exist in workspace
    print("\nFiles matching *json in workspace:")
    for f in os.listdir(WORKSPACE):
        if f.endswith('.json'):
            full_path = os.path.join(WORKSPACE, f)
            print(f"  {f}: exists={os.path.exists(full_path)}, size={os.path.getsize(full_path) if os.path.exists(full_path) else 0}")

# Cleanup
if os.path.exists(TARGET_G):
    os.remove(TARGET_G)

print("\nDebug complete!")