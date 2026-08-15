import sys
import os
sys.path.insert(0, r'C:\Projetos\Mercury-AI')

# Import the module fresh
import importlib
if 's32_e3_forensic_execution' in sys.modules:
    del sys.modules['s32_e3_forensic_execution']

from s32_e3_forensic_execution import run_f_cycle, LiveEvidenceLogger, TARGET_PATH

# Setup
evidence_logger = LiveEvidenceLogger(r'S32-E3-FORENSIC\evidence_debug_test2.jsonl')

# Clean up
for f in [r'S32-E3-FORENSIC\evidence_debug_test2.jsonl', TARGET_PATH, r'S32-E3-FORENSIC\cycle_f_data.json']:
    if os.path.exists(f):
        os.remove(f)

# Create initial target file
os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
with open(TARGET_PATH, 'w', encoding='utf-8') as f:
    json.dump({'initial': 'data', 'purpose': 's32-e3-forensic'}, f, indent=2)

print('=== Running F cycle with debug output ===')
print('Target file before:', open(TARGET_PATH).read() if os.path.exists(TARGET_PATH) else 'N/A')

# Run one F cycle
try:
    result = run_f_cycle(1, evidence_logger, r'S32-E3-FORENSIC\cycle_f_data.json')
    
    print('\n=== F Cycle Result ===')
    for key in sorted(result.keys()):
        print(f'  {key}: {result[key]}')
except Exception as e:
    print(f'\nException: {e}')
    import traceback
    traceback.print_exc()