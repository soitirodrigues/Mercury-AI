import sys
import json
import os
sys.path.insert(0, r'C:\Projetos\Mercury-AI')

from s32_e3_forensic_execution import LiveEvidenceLogger, run_f_cycle, TARGET_PATH

# Setup - create evidence logger and clean up
evidence_logger = LiveEvidenceLogger(r'S32-E3-FORENSIC\evidence_direct_test2.jsonl')

# Clean up all relevant files
for f in [r'S32-E3-FORENSIC\evidence_direct_test2.jsonl', TARGET_PATH, r'S32-E3-FORENSIC\cycle_f_data.json']:
    if os.path.exists(f):
        os.remove(f)

# Create initial target file (as main execution does)
os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
with open(TARGET_PATH, 'w', encoding='utf-8') as f:
    json.dump({'initial': 'data', 'purpose': 's32-e3-forensic'}, f, indent=2)

print('=== Initial target file ===')
print(open(TARGET_PATH).read())

# Run one F cycle
result = run_f_cycle(1, evidence_logger, r'S32-E3-FORENSIC\cycle_f_data.json')

print('\n=== F Cycle Result ===')
print('Classification:', result.get('classification'))
print('Target state:', result.get('target_state'))
print('PID match:', result.get('pid_match'))
print('JSON valid:', result.get('json_valid'))
print('Old file preserved:', result.get('old_file_preserved'))
print('PID ready:', result.get('pid_ready'))
print('PID kill:', result.get('pid_kill'))

print('\n=== Target file after F cycle ===')
if os.path.exists(TARGET_PATH):
    print(open(TARGET_PATH).read())
else:
    print('Target file does not exist')