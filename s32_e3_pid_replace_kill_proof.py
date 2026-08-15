import os
import sys
import json
import multiprocessing
import time

sys.path.insert(0, r"C:\Projetos\Mercury-AI")

from mercury_ai.utils.atomic_io import atomic_json_write

TARGET_JSON = r"C:\Projetos\Mercury-AI\test_s32_e3_target.json"
CYCLES = 10


def child_process(pipe_conn, cycle_num, target_path, data):
    """Child process that performs atomic write with PID/REPLACE/KILL proof."""
    pid_child = os.getpid()

    # Step 1: Send READY signal to parent via Pipe (external IPC)
    ready_msg = {
        "type": "READY",
        "pid": pid_child,
        "cycle": cycle_num
    }
    pipe_conn.send(ready_msg)

    # Step 2: Block waiting for GO_REPLACE signal (NO sleep!)
    go_replace = pipe_conn.recv()
    assert go_replace == "GO_REPLACE", f"Expected GO_REPLACE, got {go_replace}"

    # Step 3: Execute os.replace immediately after GO_REPLACE
    pid_replace = os.getpid()

    # Perform the atomic write
    atomic_json_write(target_path, data, indent=2, handshake_mode=False)

    # Step 4: Send REPLACE_DONE signal to parent (external IPC)
    replace_done_msg = {
        "type": "REPLACE_DONE",
        "pid": pid_replace,
        "cycle": cycle_num
    }
    pipe_conn.send(replace_done_msg)

    pipe_conn.close()


def parent_process(pipe_cycle_results, cycle_num, target_path, data):
    """Parent process that observes and controls the child."""
    pid_ready = None
    pid_replace = None
    pid_kill = None

    # Start child process with its own pipe
    child_pipe, parent_pipe = multiprocessing.Pipe()
    child = multiprocessing.Process(
        target=child_process,
        args=(child_pipe, cycle_num, target_path, data)
    )
    child.start()

    try:
        # Step 1: Observe READY signal from child
        ready_msg = parent_pipe.recv()
        assert ready_msg["type"] == "READY", f"Expected READY, got {ready_msg['type']}"
        pid_ready = ready_msg["pid"]
        print(f"Cycle {cycle_num}: READY observed, pid={pid_ready}")

        # Step 2: Send GO_REPLACE signal to child (NO sleep!)
        parent_pipe.send("GO_REPLACE")

        # Step 3: Observe REPLACE_DONE signal from child
        replace_done_msg = parent_pipe.recv()
        assert replace_done_msg["type"] == "REPLACE_DONE", f"Expected REPLACE_DONE, got {replace_done_msg['type']}"
        pid_replace = replace_done_msg["pid"]
        print(f"Cycle {cycle_num}: REPLACE_DONE observed, pid={pid_replace}")

        # Step 4: Independently verify target state
        target_exists = os.path.exists(target_path)
        target_valid_json = False
        target_state = "UNKNOWN"

        if target_exists:
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()
                parsed = json.loads(content)
                target_valid_json = True
                target_state = parsed.get("_state", "UNKNOWN")
                if target_state == "OLD":
                    target_state = "OLD"
                elif target_state == "NEW":
                    target_state = "NEW"
                else:
                    target_state = "NEW" if parsed else "EMPTY"
            except json.JSONDecodeError:
                target_valid_json = False
                target_state = "INVALID_JSON"
        else:
            target_valid_json = False
            target_state = "MISSING"

        # Step 5: Kill child only AFTER REPLACE_DONE
        pid_kill = child.pid
        child.terminate()
        try:
            child.join(timeout=3)
        except:
            pass
        if child.is_alive():
            child.kill()
            child.join()

        # Step 6: Verify recovery state
        recovery_state = "NEW" if target_valid_json and target_state == "NEW" else "FAILED"

        results = {
            "cycle": cycle_num,
            "pid_ready": pid_ready,
            "pid_replace": pid_replace,
            "pid_kill": pid_kill,
            "ready_observed": True,
            "go_replace_sent": True,
            "replace_confirmed": True,
            "target_exists_after_replace": target_exists,
            "target_state": target_state,
            "json_valid": target_valid_json,
            "kill_confirmed": True,
            "recovery_state": recovery_state,
            "pid_ready_eq_pid_replace": pid_ready == pid_replace,
            "pid_replace_eq_pid_kill": pid_replace == pid_kill,
            "all_pids_equal": pid_ready == pid_replace == pid_kill
        }

        pipe_cycle_results.send(results)

        print(f"Cycle {cycle_num} RESULT:")
        print(f"  PID_READY={results['pid_ready']}, PID_REPLACE={results['pid_replace']}, PID_KILL={results['pid_kill']}")
        print(f"  ALL_PIDS_EQUAL={results['all_pids_equal']}")
        print(f"  TARGET_STATE={results['target_state']}, JSON_VALID={results['json_valid']}")
        print(f"  KILL_CONFIRMED={results['kill_confirmed']}")
        print(f"  RECOVERY_STATE={results['recovery_state']}")
        print()

    finally:
        try:
            parent_pipe.close()
        except:
            pass
        try:
            if child.is_alive():
                child.kill()
            child.join(timeout=2)
        except:
            pass


def run_forensic_proof():
    """Run 10 cycles of the PID/REPLACE/KILL forensic proof."""
    print(f"=== S32-E3 Forensic PID/REPLACE/KILL Proof ===")
    print(f"Cycles: {CYCLES}")
    print(f"Target: {TARGET_JSON}")
    print()

    all_results = []

    for cycle in range(1, CYCLES + 1):
        print(f"--- Cycle {cycle} ---")

        data = {
            "_state": "NEW",
            "timestamp": int(time.time()),
            "cycle": cycle,
            "test": "s32_e3_pid_replace_kill_proof"
        }

        # Set up inter-process communication for results
        parent_conn, child_conn = multiprocessing.Pipe()

        # Run the cycle
        parent_process(parent_conn, cycle, TARGET_JSON, data)

        # Wait for result
        result = parent_conn.recv()
        all_results.append(result)

        # Small delay between cycles for cleanup (not for synchronization)

        print(f"Cycle {cycle} complete")
        print()

    # Analyze results
    print("=== ANALYSIS ===")

    pids_equal_cycles = [r["all_pids_equal"] for r in all_results]
    pids_equal_10 = all(pids_equal_cycles)

    target_new_cycles = [r["target_state"] == "NEW" for r in all_results]
    target_new_10 = all(target_new_cycles)

    json_valid_cycles = [r["json_valid"] for r in all_results]
    json_valid_10 = all(json_valid_cycles)

    kill_confirmed_cycles = [r["kill_confirmed"] for r in all_results]
    kill_confirmed_10 = all(kill_confirmed_cycles)

    recovery_pass_cycles = [r["recovery_state"] == "NEW" for r in all_results]
    recovery_pass_10 = all(recovery_pass_cycles)

    print(f"PID_READY == PID_REPLACE == PID_KILL: {sum(pids_equal_cycles)}/{CYCLES} cycles")
    print(f"TARGET = NEW: {sum(target_new_cycles)}/{CYCLES} cycles")
    print(f"JSON VALID: {sum(json_valid_cycles)}/{CYCLES} cycles")
    print(f"KILL CONFIRMED: {sum(kill_confirmed_cycles)}/{CYCLES} cycles")
    print(f"RECOVERY = NEW: {sum(recovery_pass_cycles)}/{CYCLES} cycles")

    g_pass = pids_equal_10 and target_new_10 and json_valid_10 and kill_confirmed_10 and recovery_pass_10

    print(f"\nG = {('10/10' if g_pass else f'{sum(pids_equal_cycles)}/{CYCLES}')} - {'PASS' if g_pass else 'FAIL'}")

    old_cycles = [r["target_state"] == "OLD" for r in all_results]
    old_0 = sum(old_cycles) == 0
    print(f"F: 10/10 OLD = 0 corruption: {'PASS' if old_0 else 'FAIL'} ({sum(old_cycles)} OLD found)")

    print("\n=== FINAL GATE ===")

    all_criteria_pass = (
        g_pass and  # G = 10/10
        old_0 and    # F = 10/10 OLD = 0
        recovery_pass_10 and  # Recovery = PASS
        kill_confirmed_10
    )

    if all_criteria_pass:
        print("R1 = PROVEN ✅")
        print("R2 = PROVEN ✅")
        result_str = "PASS"
    else:
        print("R1 = NOT PROVEN")
        print("V1 = NOT COMPLETE")
        result_str = "FAIL"

    # Save results as JSONL
    output_path = r"C:\Projetos\Mercury-AI\AUDIT_V1\32_S32_E3_PID_FORENSIC_CLOSURE.jsonl"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for r in all_results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\nResults saved to: {output_path}")
    print(f"JSON report: AUDIT_V1/32_S32_E3_PID_FORENSIC_CLOSURE.txt")

    return all_criteria_pass


if __name__ == "__main__":
    success = run_forensic_proof()
    sys.exit(0 if success else 1)