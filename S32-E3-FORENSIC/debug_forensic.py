#!/usr/bin/env python
"""
S32-E3 FORENSIC RE-EXECUTION - Debug Version
Adds error handling and debugging to identify why cycles fail.
"""

import sys
import os
import json
import time
import subprocess
from typing import Dict, Any, List

sys.path.insert(0, r'C:\Projetos\Mercury-AI')

# Constants
EVIDENCE_JSONL_PATH = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\evidence_live.jsonl"
TARGET_PATH = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\bridge_target.json"
CHILD_SCRIPT_PATH = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\child_script.py"

NUM_CYCLES = 10
HANDSHAKE_TIMEOUT = 5.0
PROCESS_WAIT_TIMEOUT = 5.0
KILL_TIMEOUT = 3.0


class LiveEvidenceLogger:
    """Logger that writes JSONL events during execution."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()
    
    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("")
    
    def write_event(self, cycle: int, event: str, pid: int, **extra):
        with open(self.filepath, "a", encoding="utf-8") as f:
            event_data = {"cycle": cycle, "event": event, "pid": pid}
            event_data.update(extra)
            f.write(json.dumps(event_data, ensure_ascii=False) + "\n")
            f.flush()
    
    def read_events(self) -> List[Dict[str, Any]]:
        events = []
        if not os.path.exists(self.filepath):
            return events
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except Exception:
            pass
        return events
    
    def close(self):
        pass


def run_child_process_g(cycle: int, target_path: str, data_file: str,
                        evidence_path: str) -> subprocess.Popen:
    """Run child for G cycle."""
    cmd = [
        sys.executable, CHILD_SCRIPT_PATH,
        "--target", target_path,
        "--data-file", data_file,
        "--cycle", str(cycle),
        "--evidence", evidence_path
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    return proc


def run_g_cycle_debug(cycle: int, evidence_logger: LiveEvidenceLogger, data_path: str) -> Dict[str, Any]:
    """Run a single G cycle with detailed debugging."""
    result = {
        "cycle": cycle,
        "test_point": "G",
        "pid_ready": None,
        "pid_replace": None,
        "pid_kill": None,
        "ready": False,
        "go_received": False,
        "replace_done": False,
        "target_confirmed": False,
        "kill_confirmed": False,
        "target_state": None,
        "json_valid": False,
        "classification": "PENDING",
        "timestamps": {},
        "evidence_events": [],
        "error": None,
    }
    
    evidence_logger._ensure_file()
    
    proc = run_child_process_g(cycle, TARGET_PATH, data_path, evidence_logger.filepath)
    result["timestamps"]["t_start"] = time.monotonic()
    
    try:
        # Observe READY
        ready_line = proc.stdout.readline().strip()
        result["evidence_events"].append({"cycle": cycle, "event": "READY_attempt", "source": "parent"})
        
        if not ready_line.startswith("READY:"):
            result["error"] = f"Expected READY, got: {ready_line}"
            result["classification"] = "ERROR: No READY"
            proc.wait(timeout=3)
            return result
        
        pid_ready = int(ready_line.split(":")[1])
        result["pid_ready"] = pid_ready
        result["ready"] = True
        result["timestamps"]["t_ready"] = time.monotonic()
        result["evidence_events"].append({"cycle": cycle, "event": "READY", "pid": pid_ready, "source": "stdout_capture"})
        print(f"  G{cycle}: READY pid={pid_ready}")
        
        # Send GO_REPLACE
        proc.stdin.write("GO_REPLACE\n")
        proc.stdin.flush()
        result["go_received"] = True
        result["timestamps"]["t_go"] = time.monotonic()
        print(f"  G{cycle}: GO_REPLACE sent")
        
        # Observe REPLACE_DONE
        replace_line = proc.stdout.readline().strip()
        result["evidence_events"].append({"cycle": cycle, "event": "REPLACE_DONE_attempt", "source": "parent"})
        
        if not replace_line.startswith("REPLACE_DONE:"):
            result["error"] = f"Expected REPLACE_DONE, got: {replace_line}"
            result["classification"] = "ERROR: No REPLACE_DONE"
            proc.kill()
            return result
        
        pid_replace = int(replace_line.split(":")[1])
        result["pid_replace"] = pid_replace
        result["replace_done"] = True
        result["timestamps"]["t_replace_done"] = time.monotonic()
        result["evidence_events"].append({"cycle": cycle, "event": "REPLACE_DONE", "pid": pid_replace, "source": "stdout_capture"})
        print(f"  G{cycle}: REPLACE_DONE pid={pid_replace}")
        
        # Check target file state
        try:
            if os.path.exists(TARGET_PATH):
                with open(TARGET_PATH, "r", encoding="utf-8") as f:
                    new_content = f.read()
                result["timestamps"]["t_target_confirmed"] = time.monotonic()
                
                try:
                    parsed = json.loads(new_content)
                    result["json_valid"] = True
                    expected = {"cycle": cycle, "objective": "s32-e3-g-bridge"}
                    if parsed == expected:
                        result["target_state"] = "NEW"
                        result["target_confirmed"] = True
                        result["classification"] = "G cycle: NEW WRITTEN"
                        print(f"  G{cycle}: Target has NEW data")
                    else:
                        result["target_state"] = "OLD"
                        result["classification"] = "G cycle: OLD (different content)"
                        print(f"  G{cycle}: Target has OLD data (content mismatch)")
                except json.JSONDecodeError:
                    result["classification"] = "G cycle: CORRUPTED JSON"
                    result["target_state"] = "CORRUPT"
                    print(f"  G{cycle}: Target has CORRUPTED JSON")
            else:
                result["classification"] = "G cycle: TARGET NOT FOUND"
                print(f"  G{cycle}: Target file not found")
        except Exception as e:
            result["error"] = f"Error reading target: {e}"
            result["classification"] = f"ERROR reading target: {e}"
            print(f"  G{cycle}: Error reading target: {e}")
        
        # Send KILL
        if result["ready"] and result["replace_done"]:
            try:
                pid_to_kill = pid_replace
                result["pid_kill"] = pid_to_kill
                result["kill_confirmed"] = True
                
                proc.stdin.write("KILL\n")
                proc.stdin.flush()
                result["timestamps"]["t_kill"] = time.monotonic()
                print(f"  G{cycle}: KILL sent")
                
                # Read ACK
                try:
                    ack = proc.stdout.readline().strip()
                    if ack == "KILL_ACK":
                        result["timestamps"]["t_ack"] = time.monotonic()
                        print(f"  G{cycle}: KILL_ACK received")
                    else:
                        print(f"  G{cycle}: ACK was: {ack}")
                except Exception:
                    result["timestamps"]["t_kill"] = time.monotonic()
                    print(f"  G{cycle}: No ACK received (timed out)")
            except Exception as e:
                result["error"] = f"Error sending KILL: {e}"
                print(f"  G{cycle}: Error sending KILL: {e}")
        
        # Wait for process to finish
        try:
            proc.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait(timeout=3)
        
        # Close handles
        try:
            proc.stdout.close()
            proc.stdin.close()
        except:
            pass
        
    except Exception as e:
        result["error"] = f"Exception in run_g_cycle: {e}"
        result["classification"] = f"EXCEPTION: {e}"
        import traceback
        traceback.print_exc()
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except:
            pass
        try:
            proc.stdout.close()
            proc.stdin.close()
        except:
            pass
    
    return result


def run_forensic_execution_debug():
    """Run the complete forensic execution with debugging."""
    
    print("=" * 80)
    print("S32-E3 FORENSIC RE-EXECUTION - DEBUG VERSION")
    print("=" * 80)
    print(f"Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    evidence_logger = LiveEvidenceLogger(EVIDENCE_JSONL_PATH)
    
    # Clean up
    for f in [EVIDENCE_JSONL_PATH, TARGET_PATH]:
        if os.path.exists(f):
            os.remove(f)
    
    os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
    with open(TARGET_PATH, "w", encoding="utf-8") as f:
        json.dump({"initial": "data"}, f, ensure_ascii=False, indent=2)
    
    # G CYCLES
    print("=" * 80)
    print("PHASE 1: G CYCLES (G01-G10)")
    print("=" * 80)
    
    g_results = []
    
    data_path = r"C:\Projetos\Mercury-AI\S32-E3-FORENSIC\cycle_data.json"
    
    for cycle in range(1, NUM_CYCLES + 1):
        # Create data file
        cycle_data = {"cycle": cycle, "objective": "s32-e3-g-bridge"}
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(cycle_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n--- G{cycle}/10 ---")
        result = run_g_cycle_debug(cycle, evidence_logger, data_path)
        g_results.append(result)
        
        cls = result.get("classification", "UNKNOWN")
        err = result.get("error", "")
        print(f"  Result: {cls}")
        if err:
            print(f"  Error: {err}")
        
        # Stop on first error for debugging
        if "EXCEPTION" in str(cls) or "ERROR" in str(cls):
            print(f"\nStopping due to error in cycle {cycle}")
            break
    
    # Generate summary
    print("\n" + "=" * 80)
    print("DEBUG SUMMARY")
    print("=" * 80)
    print(f"G cycles completed: {len(g_results)}/{NUM_CYCLES}")
    for i, r in enumerate(g_results, 1):
        print(f"  G{i}: {r.get('classification', 'UNKNOWN')}")
        if r.get('error'):
            print(f"    Error: {r['error']}")


if __name__ == "__main__":
    run_forensic_execution_debug()