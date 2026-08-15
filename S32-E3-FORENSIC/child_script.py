#!/usr/bin/env python
"""Child script for S32-E3 forensic execution.

Runs in a subprocess and writes JSONL evidence during execution.
Communicates with parent via stdout (events) and stdin (commands).
Can receive --data as JSON string or --data-file path.

Supports two modes:
- G mode (default): READY->GO_REPLACE->REPLACE_DONE->KILL->NEW
- F mode: READY->KILL->OLD (no REPLACE_EXECUTION)
"""

import sys
import os
import json
import time
import argparse

sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.utils.atomic_io import (
    atomic_json_write,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--data", required=False, default=None)
    parser.add_argument("--data-file", required=False, default=None)
    parser.add_argument("--cycle", required=True, type=int)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--mode", choices=["G", "F"], default="G",
                        help="Execution mode: G (default) or F")
    
    args = parser.parse_args()

    cycle = args.cycle
    target_path = args.target
    evidence_path = args.evidence
    mode = args.mode

    # Load data: prefer --data-file, fall back to --data
    if args.data_file:
        with open(args.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.data:
        data = json.loads(args.data)
    else:
        data = {"cycle": cycle, "objective": "test"}

    child_pid = os.getpid()

    # === Send READY event ===
    with open(evidence_path, "a", encoding="utf-8") as evf:
        evf.write(json.dumps({
            "cycle": cycle,
            "event": "READY",
            "pid": child_pid,
            "source": "child",
            "timestamp": time.monotonic()
        }, ensure_ascii=False) + "\n")
        evf.flush()

    print(f"READY:{child_pid}", flush=True)

    # === Mode F: Exit after READY without GO_REPLACE ===
    if mode == "F":
        # Write evidence and exit immediately (target stays OLD)
        with open(evidence_path, "a", encoding="utf-8") as evf:
            evf.write(json.dumps({
                "cycle": cycle,
                "event": "KILL_COMMAND",
                "pid": child_pid,
                "source": "child",
                "timestamp": time.monotonic()
            }, ensure_ascii=False) + "\n")
            evf.flush()
        print("KILL_ACK", flush=True)
        sys.exit(0)

    # === Mode G: Wait for GO_REPLACE command ===
    try:
        line = input()
        if not line.startswith("GO_REPLACE"):
            # Write RECEIVED event and exit with error
            with open(evidence_path, "a", encoding="utf-8") as evf:
                evf.write(json.dumps({
                    "cycle": cycle,
                    "event": "GO_RECEIVED_ERROR",
                    "pid": child_pid,
                    "source": "child",
                    "timestamp": time.monotonic()
                }, ensure_ascii=False) + "\n")
                evf.flush()
            sys.exit(1)
        
        # Write GO_RECEIVED event
        with open(evidence_path, "a", encoding="utf-8") as evf:
            evf.write(json.dumps({
                "cycle": cycle,
                "event": "GO_RECEIVED",
                "pid": child_pid,
                "source": "child",
                "timestamp": time.monotonic()
            }, ensure_ascii=False) + "\n")
            evf.flush()
        
    except EOFError:
        # Write evidence and exit
        with open(evidence_path, "a", encoding="utf-8") as evf:
            evf.write(json.dumps({
                "cycle": cycle,
                "event": "GO_RECEIVED_EOF",
                "pid": child_pid,
                "source": "child",
                "timestamp": time.monotonic()
            }, ensure_ascii=False) + "\n")
            evf.flush()
        sys.exit(1)

    # === REPLACE execution ===
    pid_replace = os.getpid()

    with open(evidence_path, "a", encoding="utf-8") as evf:
        evf.write(json.dumps({
            "cycle": cycle,
            "event": "BEFORE_REPLACE",
            "pid": pid_replace,
            "source": "child",
            "timestamp": time.monotonic()
        }, ensure_ascii=False) + "\n")
        evf.flush()

    try:
        atomic_json_write(target_path, data, handshake_mode=True)

        with open(evidence_path, "a", encoding="utf-8") as evf:
            evf.write(json.dumps({
                "cycle": cycle,
                "event": "REPLACE_DONE",
                "pid": pid_replace,
                "source": "child",
                "timestamp": time.monotonic()
            }, ensure_ascii=False) + "\n")
            evf.flush()

        print(f"REPLACE_DONE:{pid_replace}", flush=True)
    except Exception as e:
        with open(evidence_path, "a", encoding="utf-8") as evf:
            evf.write(json.dumps({
                "cycle": cycle,
                "event": "REPLACE_ERROR",
                "pid": child_pid,
                "error": str(e),
                "timestamp": time.monotonic()
            }, ensure_ascii=False) + "\n")
            evf.flush()
        print(f"REPLACE_ERROR:{str(e)}", flush=True)
        sys.exit(1)

    # === Wait for KILL or CONTINUE ===
    try:
        line = input()
        if line.startswith("KILL"):
            with open(evidence_path, "a", encoding="utf-8") as evf:
                evf.write(json.dumps({
                    "cycle": cycle,
                    "event": "KILL_COMMAND",
                    "pid": child_pid,
                    "source": "child",
                    "timestamp": time.monotonic()
                }, ensure_ascii=False) + "\n")
                evf.flush()
            print("KILL_ACK", flush=True)
        elif line.startswith("CONTINUE"):
            pass
        else:
            sys.exit(1)
    except EOFError:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()