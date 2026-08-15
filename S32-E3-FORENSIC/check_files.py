#!/usr/bin/env python
"""Check the state after forensic execution."""
import json
import os

print("Checking forensic execution state...")
print("=" * 50)

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

# Check target file
print("\nTarget file (bridge_target.json):")
if os.path.exists('bridge_target.json'):
    with open('bridge_target.json', 'r') as f:
        content = f.read()
    print(f"  Exists: YES")
    print(f"  Content: {content[:200] if content else 'EMPTY'}")
else:
    print(f"  Exists: NO")

# Check data files
print("\nData files:")
for f in ['cycle_data.json', 'cycle_f_data.json']:
    if os.path.exists(f):
        with open(f, 'r') as fh:
            content = fh.read()
        print(f"  {f}: {content[:100]}")
    else:
        print(f"  {f}: NOT EXISTS")

print("\n" + "=" * 50)