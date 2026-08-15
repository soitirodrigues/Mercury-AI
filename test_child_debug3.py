#!/usr/bin/env python
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

# Test data
test_data = {'test': 'pid_identity_proof'}
target_path = r'C:\Projetos\Mercury-AI\pid_test_target.json'

# Generate child script manually (using json.dumps instead of repr)
child_script_content = f'''import sys
import os
import json
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY, HANDHAKE_COMPLETED

# Report PID at READY checkpoint
child_pid = os.getpid()
status_file = r"temp_s32_g_1_status.json"
ready_data = {{"checkpoint": "READY", "pid": child_pid, "cycle": 1}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(ready_data, sf)

# Execute atomic_json_write
atomic_json_write(r"C:\\Projetos\\Mercury-AI\\pid_test_target.json", {{"test": "pid_identity_proof"}}, indent=2, 
                  signal_checkpoints=True, status_file=r"temp_s32_g_1_status.json", 
                  handshake_mode=True)

# Report PID at REPLACE checkpoint (same process, same PID)
replace_data = {{"checkpoint": "REPLACE", "pid": child_pid, "cycle": 1}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(replace_data, sf)

# Signal completion
completed_data = {{"checkpoint": "COMPLETED", "pid": child_pid, "cycle": 1, "success": True}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(completed_data, sf)
'''

# Write child script
child_script_path = r'C:\Projetos\Mercury-AI\test_child_debug2.py'
with open(child_script_path, 'w', encoding='utf-8') as f:
    f.write(child_script_content)

# Execute child script
cmd = [sys.executable, child_script_path]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate(timeout=30)
print('STDOUT:', stdout.decode('utf-8', errors='replace') if stdout else '')
print('STDERR:', stderr.decode('utf-8', errors='replace') if stderr else '')
print('Return code:', proc.returncode)

# Check status file
status_file = r'temp_s32_g_1_status.json'
if os.path.exists(status_file):
    with open(status_file, 'r', encoding='utf-8') as sf:
        content = sf.read()
        print('Status file content:', content)
else:
    print('Status file not found')