#!/usr/bin/env python
"""Debug script to test single cycle"""
import sys
import os
import json
import subprocess

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import (
    atomic_json_write,
    HANDHAKE_READY,
    HANDHAKE_COMPLETED,
)

print('Imports successful')

# Test a simple cycle
target_path = r'C:\Projetos\Mercury-AI\pid_test_target.json'
test_data = {'test': 'pid_identity_proof'}

status_file = r'temp_s32_g_1_status.json'

# Write the child script to a temp file
child_script = f'''
import sys
import os
import json
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY, HANDHAKE_COMPLETED

child_pid = os.getpid()
status_file = r"{status_file}"
ready_data = {{"checkpoint": "READY", "pid": child_pid, "cycle": 1}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(ready_data, sf)

atomic_json_write(r"{target_path}", {repr(test_data)}, indent=2, 
                  signal_checkpoints=True, status_file=r"{status_file}", 
                  handshake_mode=True)

replace_data = {{"checkpoint": "REPLACE", "pid": child_pid, "cycle": 1}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(replace_data, sf)

completed_data = {{"checkpoint": "COMPLETED", "pid": child_pid, "cycle": 1, "success": True}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(completed_data, sf)
'''

with open(r'C:\Projetos\Mercury-AI\debug_child.py', 'w') as f:
    f.write(child_script)

cmd = [sys.executable, r'C:\Projetos\Mercury-AI\debug_child.py']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate(timeout=30)
print('STDOUT:', stdout.decode('utf-8', errors='replace') if stdout else '')
print('STDERR:', stderr.decode('utf-8', errors='replace') if stderr else '')
print('Return code:', proc.returncode)

if os.path.exists(status_file):
    with open(status_file, 'r', encoding='utf-8') as sf:
        content = sf.read()
        print('Status file content:', content)
else:
    print('Status file not found')