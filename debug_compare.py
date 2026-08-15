#!/usr/bin/env python
"""
Compare: debug script vs test script setup
"""

import sys
import os
import json
import subprocess

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

# ===== SETUP 1: debug_process_insight.py style =====
print("=" * 60)
print("SETUP 1: debug_process_insight.py style")
print("=" * 60)

target1 = r'test_compare1.json'
with open(target1, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

cmd1 = [
    sys.executable, "-c",
    f'''
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write(r"{target1}", {{"new": "data"}}, indent=2)
print("SUCCESS")
'''
]

proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout1, stderr1 = proc1.communicate(timeout=5)

result1_content = None
if os.path.exists(target1):
    with open(target1) as f:
        result1_content = f.read()
    print(f'Target after: {result1_content!r}')

# Cleanup
os.remove(target1)

# ===== SETUP 2: s32_e3_task2_g_basic.py style =====
print("\n" + "=" * 60)
print("SETUP 2: s32_e3_task2_g_basic.py style")
print("=" * 60)

target2 = r'test_compare2.json'
with open(target2, 'w') as f:
    f.write(json.dumps({'initial': 'data', 'cycle': 1}, indent=2))

cmd2 = [
    sys.executable, "-c",
    f'''
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target2}", {{"test": "G-basic", "cycle": 1}}, indent=2)
print("SUCCESS")
'''
]

proc2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout2, stderr2 = proc2.communicate(timeout=5)

result2_content = None
if os.path.exists(target2):
    with open(target2) as f:
        result2_content = f.read()
    print(f'Target after: {result2_content!r}')

# Cleanup
os.remove(target2)

# Compare
print("\n" + "=" * 60)
print("COMPARISON")
print("=" * 60)
print(f'Setup 1 - Exit code: ? (communicated successfully)')
print(f'Setup 1 - Target content: {result1_content!r}')
print(f'Setup 2 - Exit code: ? (communicated successfully)')
print(f'Setup 2 - Target content: {result2_content!r}')

if result1_content and result2_content:
    if result1_content != result2_content:
        print(f'\nDIFFERENCE: Setup 1 has {result1_content!r} but Setup 2 has {result2_content!r}')