#!/usr/bin/env python
"""Debug forensic execution - test single G cycle with error handling."""
import subprocess
import sys
import json
import os

def test_single_g_cycle(cycle):
    """Test a single G cycle with detailed error handling."""
    evidence_path = f'evidence_cycle_{cycle}.jsonl'
    target_path = f'target_cycle_{cycle}.json'
    data_path = r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\cycle_data.json'
    
    # Create data file
    cycle_data = {"cycle": cycle, "objective": "s32-e3-g-bridge"}
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(cycle_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== Testing G Cycle {cycle} ===")
    
    try:
        # Run Child Process using --data-file
        proc = subprocess.Popen(
            [sys.executable, "child_script.py",
             "--target", target_path,
             "--data-file", data_path,
             "--cycle", str(cycle),
             "--evidence", evidence_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # === Observe READY ===
        ready_line = proc.stdout.readline().strip()
        print(f"  READY: {ready_line}")
        
        if not ready_line.startswith("READY:"):
            proc.wait()
            return False, "No READY event"
        
        pid_ready = int(ready_line.split(":")[1])
        
        # === Send GO_REPLACE ===
        proc.stdin.write("GO_REPLACE\n")
        proc.stdin.flush()
        print(f"  Sent GO_REPLACE")
        
        # === Observe REPLACE_DONE ===
        replace_line = proc.stdout.readline().strip()
        print(f"  REPLACE_DONE: {replace_line}")
        
        if not replace_line.startswith("REPLACE_DONE:"):
            proc.stdout.close()
            proc.wait()
            return False, "No REPLACE_DONE event"
        
        pid_replace = int(replace_line.split(":")[1])
        
        # Check target file
        if os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"  Target file content: {content[:100]}")
        else:
            print(f"  Target file does not exist")
        
        # Send KILL
        proc.stdin.write("KILL\n")
        proc.stdin.flush()
        
        # Read ACK
        try:
            ack = proc.stdout.readline().strip()
            print(f"  ACK: {ack}")
        except:
            print(f"  No ACK received")
        
        proc.wait()
        proc.stdout.close()
        proc.stdin.close()
        
        print(f"  G Cycle {cycle}: SUCCESS")
        return True, "Success"
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)

# Test cycle 1
success, msg = test_single_g_cycle(1)
print(f"\nCycle 1 result: success={success}, msg={msg}")