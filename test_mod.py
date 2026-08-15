import importlib.util
spec = importlib.util.spec_from_file_location('s32_e3_forensic', r'S32-E3-FORENSIC\s32_e3_forensic_execution.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Get the source code of run_f_cycle
import inspect
source = inspect.getsource(mod.run_f_cycle)
# Check for key phrases from our modification
checks = [
    'ready_observed',
    'kill_confirmed',
    'replace_done',
    'target_state',
    'json_valid_check',
    'recovery_state',
    'pid_ready_check',
    'pid_kill_check',
    'classification_conditions',
    'PASS_OLD',
    'FAIL:',
    'Instrument classification'
]
print('Checking modified run_f_cycle:')
for check in checks:
    found = check in source
    print(f'  {check}: {"FOUND" if found else "NOT FOUND"}')