#!/usr/bin/env python
"""
Debug: Check what the child process actually does
"""

import sys
import os
import json
import subprocess

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

# Simple test: run atomic_json_write in a subprocess and check result
target = r'test_simple_atomic.json'
status = r'test_simple_status.json'

# Create initial file
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

print(f'Initial file: {json.dumps({"initial": "data"}, indent=2)}')

# Simple command - no handshake, no signal_checkpoints, just basic atomic_json_write
cmd = [
    sys.executable, "-c",
    f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write(r"{target}", {{"new": "data"}}, indent=2)
print("SUCCESS - atomic_json_write completed")
"""
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    stdout, stderr = proc.communicate(timeout=5)
    print(f'Exit code: {proc.returncode}')
    print(f'Stdout: {stdout.decode("latin-1", errors="replace")}')
    print(f'Stderr: {stderr.decode("latin-1", errors="replace")}')
except subprocess.TimeoutExpired:
    proc.kill()
    proc.wait()
    print('Timeout expired')

# Check result
if os.path.exists(target):
    with open(target) as f:
        content = f.read()
        print(f'Target file: {content!r}')
else:
    print('Target file does not exist')

# Check status
if os.path.exists(status):
    with open(status) as f:
        print(f'Status file: {f.read()!r}')

# Cleanup
os.remove(target)
if os.path.exists(status):
    os.remove(status)

print('\\nTest complete')