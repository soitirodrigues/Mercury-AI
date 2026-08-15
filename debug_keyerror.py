#!/usr/bin/env python
"""Debug script for S32-E3 KeyError issue"""
import subprocess
import sys
import os
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from mercury_ai.utils.atomic_io import atomic_json_write

target = r'test_s32_e3_target.json'
status_file = r'test_s32_e3_status.json'

# Remove files if exist
if os.path.exists(target): os.remove(target)
if os.path.exists(status_file): os.remove(status_file)

# Simple test - just run atomic_json_write with handshake_mode
cmd = [
    sys.executable, "-c",
    f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target}", {{"test": "data"}}, indent=2, 
                  signal_checkpoints=True, status_file="{status_file}", 
                  handshake_mode=True)
print("SUCCESS")
"""
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(1)
print(f'After 1s, status file exists: {os.path.exists(status_file)}')
if os.path.exists(status_file):
    with open(status_file, 'r') as f:
        content = f.read().strip()
    print(f'Status file content: "{content}"')
    print(f'Content equals READY_TO_REPLACE: {content == "READY_TO_REPLACE"}')
proc.kill()
proc.wait(timeout=5)
print('Done')