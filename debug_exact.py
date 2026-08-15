#!/usr/bin/env python
"""
Extra debug: Compare exact setup
"""

import sys
import os
import json
import subprocess
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

target = r'test_debug_final.json'

# Create initial file
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data', 'cycle': 1}, indent=2))

print(f'Initial target: {json.dumps({"initial": "data", "cycle": 1}, indent=2)}')

# Command: exactly like s32_e3_task2_g_basic.py
cmd = [
    sys.executable, "-c",
    f'''
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target}", {{"test": "G-basic", "cycle": 1}}, indent=2)
print("SUCCESS")
'''
]

print(f'Running command: {cmd}')
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

# Check target file content
if os.path.exists(target):
    with open(target) as f:
        content = f.read()
    print(f'Target file content: {content!r}')
    
    # Parse and check
    try:
        parsed = json.loads(content)
        print(f'Parsed: {parsed}')
    except:
        print('Not valid JSON')
else:
    print('Target file does not exist')

# Cleanup
os.remove(target)
print('\\nTest complete')