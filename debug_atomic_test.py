import sys
import os
import json
import subprocess

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write

target = r'test_debug_handshake.json'
status_file = r'test_debug_status.json'

# Create initial file
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

print('Initial file created')

# Data to write
write_data = {"test": "new_data"}

# Run atomic_json_write with handshake_mode in a subprocess
cmd_str = (
    f'import sys\n'
    f'sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")\n'
    f'from mercury_ai.utils.atomic_io import atomic_json_write\n'
    f'atomic_json_write(r"{target}", {json.dumps(write_data)}, indent=2, '
    f'signal_checkpoints=True, status_file=r"{status_file}", handshake_mode=True)\n'
    f'print("CHILD DONE")'
)

print(f'Running command')
proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)

try:
    stdout = proc.stdout.read()
    print(f'Stdout bytes: {stdout}')
    try:
        print(f'Stdout decoded: {stdout.decode("latin-1")}')
    except:
        print('Could not decode stdout')
except Exception as e:
    print(f'Error reading stdout: {e}')
    
proc.wait()

# Check status file
status_exists = os.path.exists(status_file)
print(f'Status file exists: {status_exists}')

# Check target file
target_exists = os.path.exists(target)
print(f'Target file exists: {target_exists}')

if target_exists:
    with open(target) as f:
        content = f.read()
        print(f'Target file content: {content!r}')
else:
    print('Target file does not exist')

# Show what we expect
print(f'Expected target to have: {json.dumps(write_data)} after os.replace()')

# Cleanup
os.remove(target)
if status_exists:
    os.remove(status_file)

print('\nTest complete')