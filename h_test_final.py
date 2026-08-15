import sys, os, json, subprocess, time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from mercury_ai.utils.atomic_io import atomic_json_write

target = r'h_test_final.json'

# Run 5 cycles testing handshake_mode with kill
results = []
for i in range(5):
    # Create initial file
    with open(target, 'w') as f:
        f.write(json.dumps({'test': 'old_data', 'cycle': i+1}, indent=2))
    
    # Start subprocess
    cmd_code = f'''import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target}", {{"test": "new_data", "cycle": {i+1}}}, handshake_mode=True, indent=2)
print("SUCCESS")'''
    
    proc = subprocess.Popen(
        [sys.executable, "-c", cmd_code],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    # Wait a moment then kill
    time.sleep(0.005)
    proc.kill()
    proc.wait()
    
    # Check target file
    if os.path.exists(target):
        with open(target) as f:
            content = f.read()
        results.append(content)
    else:
        results.append('FILE_NOT_FOUND')

# Analyze results
old_count = sum(1 for r in results if json.loads(r).get('test') == 'old_data')
new_count = sum(1 for r in results if json.loads(r).get('test') == 'new_data')
print(f'Handshake Mode × 5 Results:')
print(f'  OLD preserved: {old_count}/5')
print(f'  NEW written: {new_count}/5')
print(f'  PARTIAL/CORRUPT: {(5 - old_count - new_count)}/5')

# Cleanup
os.remove(target)
print('Handshake test complete')