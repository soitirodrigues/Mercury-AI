
import sys
import os
import json
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
from mercury_ai.utils.atomic_io import atomic_json_write, HANDHAKE_READY, HANDHAKE_COMPLETED

child_pid = os.getpid()
status_file = r"temp_s32_g_1_status.json"
ready_data = {"checkpoint": "READY", "pid": child_pid, "cycle": 1}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(ready_data, sf)

atomic_json_write(r"C:\Projetos\Mercury-AI\pid_test_target.json", {'test': 'pid_identity_proof'}, indent=2, 
                  signal_checkpoints=True, status_file=r"temp_s32_g_1_status.json", 
                  handshake_mode=True)

replace_data = {"checkpoint": "REPLACE", "pid": child_pid, "cycle": 1}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(replace_data, sf)

completed_data = {"checkpoint": "COMPLETED", "pid": child_pid, "cycle": 1, "success": True}
with open(status_file, "w", encoding="utf-8") as sf:
    json.dump(completed_data, sf)
