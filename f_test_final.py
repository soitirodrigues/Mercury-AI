import sys, os, json, subprocess, time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from mercury_ai.utils.atomic_io import atomic_json_write

target = r'f_test_final.json'

# Run 10 cycles testing kill before os.replace()
results = []
for i in range(10):
    # Create initial file
    with open(target, 'w') as f:
        f.write(json.dumps({'test': 'old_data', 'cycle': i+1}, indent=2))
    
    # Start subprocess that will kill before os.replace() completes
    cmd_code = f'''import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target}", {{"test": "new_data", "cycle": {i+1}}}, indent=2)
print("SUCCESS")'''
    
    proc = subprocess.Popen(
        [sys.executable, "-c", cmd_code],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    # Simulate kill before os.replace() completes
    time.sleep(0.01)  # Small delay to ensure we're before os.replace
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
print(f'F × 10 Results:')
print(f'  OLD preserved: {old_count}/10')
print(f'  NEW written: {new_count}/10')
print(f'  PARTIAL/CORRUPT: {10 - old_count - new_count}/10')

# Cleanup
os.remove(target)
print('F test complete')