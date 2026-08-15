import sys
import json
sys.path.insert(0, r'C:\Projetos\Mercury-AI')
from s32_e3_forensic_execution import LiveEvidenceLogger, run_g_cycle, TARGET_PATH
import os

# Setup
evidence_logger = LiveEvidenceLogger(r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\evidence_live.jsonl')
data_path = r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\cycle_data.json'

# Create data file
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump({'cycle': 1, 'objective': 's32-e3-g-bridge'}, f, indent=2)

# Run one G cycle
try:
    result = run_g_cycle(1, evidence_logger, data_path)
    print(f'Result: {result.get("classification", "unknown")}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()