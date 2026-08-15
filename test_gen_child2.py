#!/usr/bin/env python
import sys
import os
import json
import subprocess

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

target_path = r'C:\Projetos\Mercury-AI\pid_test_target.json'
test_data = {'test': 'pid_identity_proof'}

cycle_num = 1
status_file = r'temp_s32_g_1_status.json'

# Generate the data representation
data_json = json.dumps(test_data)

# Generate child script - use str(use_handshake) not .lower()
use_handshake = True
child_script = f'''
import sys
import os
import json
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY, HANDHAKE_COMPLETED

# Report PID at READY checkpoint
child_pid = os.getpid()
status_file = r"{status_file}"
ready_data = {{"checkpoint": "READY", "pid": child_pid, "cycle": {cycle_num}}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(ready_data, sf)

# Execute atomic_json_write
atomic_json_write(r"{target_path}", {data_json}, indent=2, 
                  signal_checkpoints=True, status_file=r"{status_file}", 
                  handshake_mode={str(use_handshake)})

# Report PID at REPLACE checkpoint (same process, same PID)
replace_data = {{"checkpoint": "REPLACE", "pid": child_pid, "cycle": {cycle_num}}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(replace_data, sf)

# Signal completion
completed_data = {{"checkpoint": "COMPLETED", "pid": child_pid, "cycle": {cycle_num}, "success": True}}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(completed_data, sf)
'''

print('Generated child script (first 300 chars):')
print(child_script[:300])
print('...')
print()

# Write and execute
child_script_path = r'temp_test_child2.py'
with open(child_script_path, 'w', encoding='utf-8') as f:
    f.write(child_script)

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