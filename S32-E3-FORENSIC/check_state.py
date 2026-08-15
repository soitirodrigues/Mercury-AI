#!/usr/bin/env python
"""Check the state after forensic execution."""
import json
import os

print("Checking forensic execution state...")
print("=" * 50)

# Check target file
print("\nTarget file (bridge_target.json):")
if os.path.exists('bridge_target.json'):
    with open('bridge_target.json', 'r') as f:
        content = f.read()
    print(f"  Exists: YES")
    print(f"  Content: {content[:200] if content else 'EMPTY'}")
else:
    print(f"  Exists: NO")

# Check evidence file
print("\nEvidence file (evidence_live.jsonl):")
if os.path.exists('evidence_live.jsonl'):
    with open('evidence_live.jsonl', 'r') as f:
        lines = f.readlines()
    print(f"  Exists: YES")
    print(f"  Total lines: {len(lines)}")
    for i, line in enumerate(lines):
        try:
            evt = json.loads(line.strip())
            print(f"  Line {i+1}: cycle={evt.get('cycle')}, event={evt.get('event')}, pid={evt.get('pid')}")
        except:
            print(f"  Line {i+1}: (not valid JSON)")
else:
    print(f"  Exists: NO")

# Check if there are any other relevant files
print("\nOther files in S32-E3-FORENSIC:")
for f in os.listdir('.'):
    if f.endswith('.jsonl') or f.endswith('.json') or f == 's32_e3_forensic_execution.py':
        size = os.path.getsize(f) if os.path.exists(f) else 0
        print(f"  {f}: {size} bytes")