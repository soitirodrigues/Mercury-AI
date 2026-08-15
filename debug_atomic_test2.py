import sys
import os
import json
import subprocess
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write

target = r'test_debug_handshake2.json'
status_file = r'test_debug_status2.json'

# Create initial file
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

print(f'Initial file created: {json.dumps({"initial": "data"}, indent=2)}')

# Data to write
write_data = {"test": "new_data", "timestamp": time.time()}

# Run atomic_json_write with handshake_mode in a subprocess with longer wait
cmd_str = (
    f'import sys\n'
    f'sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")\n'
    f'from mercury_ai.utils.atomic_io import atomic_json_write\n'
    f'atomic_json_write(r"{target}", {json.dumps(write_data)}, indent=2, '
    f'signal_checkpoints=True, status_file=r"{status_file}", handshake_mode=True)\n'
    f'print("CHILD DONE")'
)

print(f'Running atomic_json_write with handshake_mode')
proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    stdout, stderr = proc.communicate(timeout=10)
    print(f'Exit code: {proc.returncode}')
    print(f'Stdout: {stdout.decode("latin-1", errors="replace")}')
    print(f'Stderr: {stderr.decode("latin-1", errors="replace")}')
except subprocess.TimeoutExpired:
    proc.kill()
    proc.wait()
    print('Timeout expired - process still running after 10s')

# Check status file
status_exists = os.path.exists(status_file)
print(f'\\nStatus file exists: {status_exists}')

# Check target file
target_exists = os.path.exists(target)
print(f'Target file exists: {target_exists}')

if target_exists:
    with open(target) as f:
        content = f.read()
        print(f'Target file content: {content!r}')
        try:
            parsed = json.loads(content)
            print(f'Parsed JSON: {parsed}')
        except:
            print('Not valid JSON')
else:
    print('Target file does not exist')

# Show what we expect
print(f'\\nExpected target to have: {json.dumps(write_data)} after os.replace()')
print(f'but got: {content!r}')

# Cleanup
os.remove(target)
if status_exists:
    os.remove(status_file)

print('\\nTest complete')