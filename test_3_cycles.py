import os, sys, json, multiprocessing, time
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write

TARGET_JSON = r"C:\Projetos\Mercury-AI\test_s32_e3_target.json"
CYCLES = 3

def child_process(pipe_conn, cycle_num, target_path, data):
    pid_child = os.getpid()
    ready_msg = {"type": "READY", "pid": pid_child, "cycle": cycle_num}
    pipe_conn.send(ready_msg)
    go_replace = pipe_conn.recv()
    assert go_replace == "GO_REPLACE"
    pid_replace = os.getpid()
    atomic_json_write(target_path, data, indent=2, handshake_mode=False)
    replace_done_msg = {"type": "REPLACE_DONE", "pid": pid_replace, "cycle": cycle_num}
    pipe_conn.send(replace_done_msg)
    pipe_conn.close()

def parent_process(pipe_cycle_results, cycle_num, target_path, data):
    pid_ready = None
    pid_replace = None
    pid_kill = None
    child_pipe, parent_pipe = multiprocessing.Pipe()
    child = multiprocessing.Process(target=child_process, args=(child_pipe, cycle_num, target_path, data))
    child.start()
    try:
        ready_msg = parent_pipe.recv()
        assert ready_msg["type"] == "READY"
        pid_ready = ready_msg["pid"]
        print("Cycle %d: READY observed, pid=%d" % (cycle_num, pid_ready))
        parent_pipe.send("GO_REPLACE")
        replace_done_msg = parent_pipe.recv()
        assert replace_done_msg["type"] == "REPLACE_DONE"
        pid_replace = replace_done_msg["pid"]
        print("Cycle %d: REPLACE_DONE observed, pid=%d" % (cycle_num, pid_replace))
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
                if target_state == "OLD": target_state = "OLD"
                elif target_state == "NEW": target_state = "NEW"
                else: target_state = "NEW" if parsed else "EMPTY"
            except json.JSONDecodeError:
                target_valid_json = False
                target_state = "INVALID_JSON"
        else:
            target_valid_json = False
            target_state = "MISSING"
        pid_kill = child.pid
        child.terminate()
        try: child.join(timeout=3)
        except: pass
        if child.is_alive(): child.kill(); child.join()
        target_valid_and_new = target_valid_json and target_state == "NEW"
        recovery_state = "NEW" if target_valid_and_new else "FAILED"
        all_pids = pid_ready == pid_replace == pid_kill
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
            "all_pids_equal": all_pids
        }
        pipe_cycle_results.send(results)
        print("Cycle %d RESULT: ALL_PIDS_EQUAL=%s" % (cycle_num, all_pids))
    finally:
        try: parent_pipe.close()
        except: pass
        try:
            if child.is_alive(): child.kill()
            child.join(timeout=2)
        except: pass

all_results = []
for cycle in range(1, CYCLES + 1):
    print("--- Cycle %d ---" % cycle)
    data = {"_state": "NEW", "timestamp": int(time.time()), "cycle": cycle, "test": "test"}
    parent_conn, child_conn = multiprocessing.Pipe()
    parent_process(parent_conn, cycle, TARGET_JSON, data)
    result = parent_conn.recv(timeout=10)
    all_results.append(result)
    time.sleep(0.3)
    print("Cycle %d complete: all_pids_equal=%s" % (cycle, result["all_pids_equal"]))
    print()

print("=== ANALYSIS ===")
pids_equal = all(r["all_pids_equal"] for r in all_results)
target_new = all(r["target_state"] == "NEW" for r in all_results)
json_valid = all(r["json_valid"] for r in all_results)
print("PIDs equal: %s, Target NEW: %s, JSON valid: %s" % (pids_equal, target_new, json_valid))