#!/usr/bin/env python
"""Debug script for atomic_json_write handshake_mode"""
import sys
sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY
import subprocess
import os
import time

# Test 1: Basic atomic_json_write WITHOUT handshake_mode
print("=" * 60)
print("Test 1: Basic atomic_json_write (no handshake_mode)")
print("=" * 60)

target1 = r'test_debug_basic.json'
data1 = {'test': 'basic_debug'}

# Remove target if exists
if os.path.exists(target1):
    os.remove(target1)

# Command without handshake_mode
cmd1 = [
    sys.executable, "-c",
    f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target1}", {repr(data1)}, indent=2, 
                  signal_checkpoints=True, status_file="debug_status_basic.json")
print("SUCCESS")
"""
]

proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout1, stderr1 = proc1.communicate(timeout=5.0)

print('STDOUT:', stdout1.decode())
print('STDERR:', stderr1.decode())
print('Return code:', proc1.returncode)

print('Target exists:', os.path.exists(target1))
if os.path.exists(target1):
    with open(target1, 'r') as f:
        print('Target content:', f.read())

status_file1 = 'debug_status_basic.json'
print('Status exists:', os.path.exists(status_file1))
if os.path.exists(status_file1):
    with open(status_file1, 'r') as f:
        print('Status content:', f.read())

# Cleanup
if os.path.exists(target1):
    os.remove(target1)
if os.path.exists(status_file1):
    os.remove(status_file1)

print()

# Test 2: atomic_json_write WITH handshake_mode
print("=" * 60)
print("Test 2: atomic_json_write WITH handshake_mode")
print("=" * 60)

target2 = r'test_debug_handshake.json'
data2 = {'test': 'handshake_debug'}

# Remove target if exists
if os.path.exists(target2):
    os.remove(target2)

# Command WITH handshake_mode
cmd2 = [
    sys.executable, "-c",
    f"""
import sys
sys.path.insert(0, r"C:\\Projetos\\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write
atomic_json_write("{target2}", {repr(data2)}, indent=2, 
                  signal_checkpoints=True, status_file="debug_status_handshake.json", 
                  handshake_mode=True)
print("SUCCESS")
"""
]

proc2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout2, stderr2 = proc2.communicate(timeout=5.0)

print('STDOUT:', stdout2.decode())
print('STDERR:', stderr2.decode())
print('Return code:', proc2.returncode)

print('Target exists:', os.path.exists(target2))
if os.path.exists(target2):
    with open(target2, 'r') as f:
        print('Target content:', f.read())

status_file2 = 'debug_status_handshake.json'
print('Status exists:', os.path.exists(status_file2))
if os.path.exists(status_file2):
    with open(status_file2, 'r') as f:
        print('Status content:', f.read())

# Cleanup
if os.path.exists(target2):
    os.remove(target2)
if os.path.exists(status_file2):
    os.remove(status_file2)

print()
print("Debug test complete!")