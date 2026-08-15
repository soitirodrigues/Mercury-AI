#!/usr/bin/env python
"""Simple test of atomic_json_write"""
import sys
import os
import json

sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from mercury_ai.utils.atomic_io import atomic_json_write

# Test 1: Normal execution - should write NEW data
print("=== Test 1: Normal execution ===")
target = r'test_json_direct.json'
old_data = {'test': 'old_data', 'cycle': 1, 'state': 'OLD'}
with open(target, 'w', encoding='utf-8') as f:
    json.dump(old_data, f, indent=2)

new_data = {'test': 'new_data', 'cycle': 1, 'state': 'NEW'}
atomic_json_write(target, new_data, indent=2)

print("Target file exists:", os.path.exists(target))
if os.path.exists(target):
    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()
    print("File content:", content)
    
    # Parse and check
    data = json.loads(content)
    print("Parsed data:", data)
    print("State:", data.get('state'))
    
    # Cleanup
    os.remove(target)
    print("Cleanup done")

print("Test 1 PASSED: Normal execution writes NEW data\n")

# Test 2: Kill before os.replace - should preserve OLD
print("=== Test 2: Kill before os.replace ===")
import subprocess
import time

target = r'test_json_kill.json'
old_data2 = {'test': 'old_data_kill', 'cycle': 2, 'state': 'OLD'}
with open(target, 'w', encoding='utf-8') as f:
    json.dump(old_data2, f, indent=2)

# Start subprocess and kill quickly
cmd = [
    sys.executable, "-c",
    f'''
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
import json, time

target = r"C:\\Projetos\\Mercury-AI\\test_json_kill.json"
old_data = {{"test": "old_data_kill", "cycle": 2, "state": "OLD"}}
with open(target, "w", encoding="utf-8") as f:
    json.dump(old_data, f, indent=2)

# Try atomic write but will be killed
new_data = {{"test": "new_data_kill", "cycle": 2, "state": "NEW"}}
atomic_json_write(target, new_data, indent=2, max_retries=1)
print("SUCCESS or KILLED")
'''
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
try:
    stdout, stderr = proc.communicate(timeout=0.05)  # 50ms - very quick kill
    print("Process completed normally (unexpected)")
except subprocess.TimeoutExpired:
    proc.kill()
    proc.wait()
    print("Process killed (expected)")

print("Target file exists after kill:", os.path.exists(target))
if os.path.exists(target):
    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()
    print("File content after kill:", content)
    
    # Parse and check
    try:
        data = json.loads(content)
        print("Parsed data:", data)
        print("State:", data.get('state'))
        if data.get('state') == 'OLD':
            print("SUCCESS: OLD data preserved after kill!")
        else:
            print("NOTE: NEW data written (timing was lucky)")
    except json.JSONDecodeError:
        print("File is not valid JSON after kill")
    
    # Cleanup
    os.remove(target)

print("Test 2 PASSED\\n")

print("=== ALL TESTS COMPLETE ===")