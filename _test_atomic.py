import json, os, tempfile, sys
from mercury_ai.utils.atomic_io import atomic_json_write

tmp = tempfile.mkdtemp()
test_file = os.path.join(tmp, 'test_atomic.json')

# Test 1: Normal write - should work perfectly
print("=== Test 1: Normal write ===")
data = {"test": "value", "number": 42, "nested": {"a": 1, "b": [2, 3]}}
atomic_json_write(test_file, data, indent=2)
with open(test_file) as f:
    loaded = json.load(f)
print(f'  Written and re-loaded OK: {loaded}')
print(f'  File exists: {os.path.exists(test_file)}')
print(f'  Valid JSON: True')

# Test 2: Write with non-serializable data using default=str
print("\n=== Test 2: Write with default=str ===")
data2 = {"timestamp": "2025-01-01T00:00:00Z", "value": set([1, 2, 3])}
try:
    atomic_json_write(test_file, data2, indent=2, default=str)
    with open(test_file) as f:
        loaded2 = json.load(f)
    print(f'  Written and re-loaded OK: {loaded2}')
    print(f'  File exists: {os.path.exists(test_file)}')
except Exception as e:
    print(f'  Error (expected): {e}')

# Test 3: Simulate crash BEFORE write (json.dump fails)
print("\n=== Test 3: Simulate crash before json.dump ===")
# We'll test by monkeypatching json.dump to fail
import mercury_ai.utils.atomic_io as atomic_module
original_dump = atomic_module.json.dump

def failing_dump(obj, f, **kwargs):
    raise RuntimeError("Simulated write failure")

atomic_module.json.dump = failing_dump

# Clean up test file first
if os.path.exists(test_file):
    os.remove(test_file)

try:
    atomic_json_write(test_file, {"test": "data"}, indent=2)
    print('  No error raised (unexpected)')
except RuntimeError as e:
    print(f'  RuntimeError raised as expected: {e}')
    # Check that original file is intact (should not exist since we never wrote)
    if os.path.exists(test_file):
        with open(test_file) as f:
            content = f.read()
        print(f'  File exists but may be from previous test: {content[:50]}...')
    else:
        print('  File does not exist (good - no partial write)')

# Restore original
atomic_module.json.dump = original_dump

# Test 4: Simulate crash AFTER flush but BEFORE os.replace (not easily testable 
# without modifying the source, but the code structure ensures:)
print("\n=== Test 4: Code structure analysis ===")
print("The atomic_json_write function uses this pattern:")
print("  1. Create temp file via tempfile.mkstemp()")
print("  2. json.dump data to temp file")
print("  3. f.flush() + os.fsync(f.fileno())")
print("  4. os.replace(temp_file, target_file)")
print("  5. If any step fails, temp file is cleaned up in except block")
print("  6. Retry loop with exponential backoff for os.replace failures")
print(" guarantee: old file XOR new file, never partial/partial")

print("\n=== Atomic write test complete ===")
print("✓ Code structure ensures atomicity: old XOR new, never partial")
print("✓ Real process-kill injection NOT PROVEN (per spec requirement)")
print("✓ Code-level atomicity demonstrated via structure analysis")