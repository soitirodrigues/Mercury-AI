#!/usr/bin/env python
"""
Debug: Check what atomic_json_write actually does with handshake_mode
"""

import sys
import os
import json
import tempfile
import time

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY, CHECKPOINT_BEFORE_REPLACE, CHECKPOINT_AFTER_REPLACE

# Test 1: Basic atomic_json_write without handshake_mode
print("=" * 60)
print("TEST 1: Basic atomic_json_write (no handshake)")
print("=" * 60)

target = r'test_debug_basic.json'
# Create initial file
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

print(f'Initial: {json.dumps({"initial": "data"}, indent=2)}')

# Run basic atomic_json_write
try:
    atomic_json_write(target, {"test": "new_data"}, indent=2)
    with open(target) as f:
        print(f'After basic write: {f.read()!r}')
except Exception as e:
    print(f'Error: {e}')

os.remove(target)

# Test 2: With handshake_mode but NO signal_checkpoints
print("\n" + "=" * 60)
print("TEST 2: handshake_mode=True, signal_checkpoints=False")
print("=" * 60)

target = r'test_debug_handshake_no_signal.json'
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

try:
    atomic_json_write(target, {"test": "new_data"}, indent=2, handshake_mode=True)
    with open(target) as f:
        content = f.read()
        print(f'After handshake_mode write: {content!r}')
        # Check status file
        status = r'test_debug_status.json'
        if os.path.exists(status):
            with open(status) as f:
                print(f'Status file: {f.read()!r}')
except Exception as e:
    print(f'Error: {e}')

# Cleanup
for f in [target, r'test_debug_status.json']:
    if os.path.exists(f):
        os.remove(f)

# Test 3: With both handshake_mode and signal_checkpoints
print("\n" + "=" * 60)
print("TEST 3: handshake_mode=True, signal_checkpoints=True")
print("=" * 60)

target = r'test_debug_both.json'
with open(target, 'w') as f:
    f.write(json.dumps({'initial': 'data'}, indent=2))

try:
    atomic_json_write(target, {"test": "new_data"}, indent=2, handshake_mode=True, signal_checkpoints=True)
    with open(target) as f:
        content = f.read()
        print(f'After both flags write: {content!r}')
        # Check status file
        status = r'test_debug_status.json'
        if os.path.exists(status):
            with open(status) as f:
                print(f'Status file: {f.read()!r}')
except Exception as e:
    print(f'Error: {e}')

# Cleanup
for f in [target, r'test_debug_status.json']:
    if os.path.exists(f):
        os.remove(f)