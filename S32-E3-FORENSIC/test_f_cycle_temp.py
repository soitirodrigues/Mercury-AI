import sys
import json
sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from s32_e3_forensic_execution import LiveEvidenceLogger, run_f_cycle
import os

# Setup
evidence_logger = LiveEvidenceLogger(r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\evidence_live.jsonl')

# Run one F cycle
try:
    result = run_f_cycle(1, evidence_logger, r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\cycle_f_data.json')
    print(f'Result: {result.get("classification", "unknown")}')
    print(f'Target state: {result.get("target_state", "unknown")}')
    print(f'PID match: {result.get("pid_match", False)}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()