import sys, os, json, subprocess

sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from mercury_ai.utils.atomic_io import atomic_json_write

target = r'test_direct.json'

# Exact setup from s32_e3_task2_g_basic.py
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data', 'cycle': 1}, indent=2))

print('Initial:', json.dumps({'initial': 'data', 'cycle': 1}, indent=2))

cmd = [
    sys.executable, '-c',
    f'''import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target}", {"test": "G-basic", "cycle": 1}, indent=2)
print("SUCCESS")'''
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate(timeout=5)

print(f'Exit code: {proc.returncode}')
print(f'Stdout: {stdout.decode("latin-1", errors="replace")}')
print(f'Stderr: {stderr.decode("latin-1", errors="replace")}')

# Check target file
if os.path.exists(target):
    with open(target) as f:
        content = f.read()
    print(f'Target file content: {content!r}')
    try:
        parsed = json.loads(content)
        print(f'Parsed: {parsed}')
        # Compare with old
        old = json.dumps({'initial': 'data', 'cycle': 1}, indent=2)
        print(f'Old content: {old!r}')
        print(f'Content matches old: {content == old}')
    except:
        print('Not valid JSON')
else:
    print('Target file does not exist')

# Cleanup
os.remove(target)
print('Test complete')