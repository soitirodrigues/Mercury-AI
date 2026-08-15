import sys
sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from s32_e3_forensic_execution import run_f_cycle, TARGET_PATH, LiveEvidenceLogger
import os

# Clean up
for f in [TARGET_PATH, r'S32-E3-FORENSIC\cycle_f_data.json']:
    if os.path.exists(f):
        os.remove(f)

# Create initial target file
os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
with open(TARGET_PATH, 'w', encoding='utf-8') as f:
    json.dump({'initial': 'data', 'purpose': 's32-e3-forensic'}, f, indent=2)

print('Initial target:', open(TARGET_PATH).read())

# Run F cycle
evidence_logger = LiveEvidenceLogger(r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\evidence_test.jsonl')
result = run_f_cycle(1, evidence_logger, r'C:\Projetos\Mercury-AI\S32-E3-FORENSIC\cycle_f_data.json')

print('Classification:', result.get('classification'))
print('Target state:', result.get('target_state'))
print('JSON valid:', result.get('json_valid'))
print('Old file preserved:', result.get('old_file_preserved'))
print('PID ready:', result.get('pid_ready'))
print('PID kill:', result.get('pid_kill'))