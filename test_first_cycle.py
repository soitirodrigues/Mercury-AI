#!/usr/bin/env python
"""Test just the first cycle with error handling"""
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

print('Starting first cycle test...')

# Target path and data
target_path = r'C:\Projetos\Mercury-AI\pid_test_target.json'
test_data = {
    "test": "pid_identity_proof",
    "timestamp": "2026-08-16 10:00:00",
    "cycle_data": []
}

cycle_num = 1
status_file = r'temp_s32_g_1_status.json'

try:
    # Generate the data representation
    data_json = json.dumps(test_data)

    # Write the child script to a temp file
    use_handshake = True
    use_handshake_lower = str(use_handshake)  # Use str() not .lower()
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

    child_script_path = rf"temp_s32_child_{cycle_num}.py"
    with open(child_script_path, "w", encoding="utf-8") as f:
        f.write(child_script)

    # Launch child process
    cmd = [sys.executable, child_script_path]
    print(f'Running command: {cmd}')
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the process to complete
    try:
        stdout, stderr = proc.communicate(timeout=30)
        print('STDOUT:', stdout.decode('utf-8', errors='replace') if stdout else '')
        print('STDERR:', stderr.decode('utf-8', errors='replace') if stderr else '')
        print('Return code:', proc.returncode)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        print('Timeout expired')
    
    # Read the status file written by the child process
    if os.path.exists(status_file):
        try:
            with open(status_file, "r", encoding="utf-8") as sf:
                status_content = sf.read()
                status_data = json.loads(status_content) if status_content else None
                
            print('Status file content:', status_content if status_content else '(empty)')
            if status_data:
                print('Parsed status data:', status_data)
                print('Checkpoint:', status_data.get('checkpoint'))
                print('PID:', status_data.get('pid'))
                print('Success:', status_data.get('success'))
        except Exception as e:
            print('Error reading status file:', e)
    else:
        print('Status file not found')
    
    # Clean up
    if os.path.exists(child_script_path):
        os.remove(child_script_path)
    
    print('First cycle test completed successfully!')
    
except Exception as e:
    print(f'ERROR: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()