import json

# Parse evidence_live.jsonl - structure: G cycles 1-10 first (5 events each), then F cycles 1-10 (2 events each)
# Total: 10*5 + 10*2 = 70 lines

# Read all lines
with open('S32-E3-FORENSIC/evidence_live.jsonl', 'r') as f:
    lines = f.readlines()

# Parse G cycles (first 50 lines, cycles 1-10, 5 events each)
g_cycles = {}
for i in range(10):  # cycles 1-10
    # Each G cycle has 5 lines
    cycle_first_line = i * 5
    if cycle_first_line < len(lines):
        data = json.loads(lines[cycle_first_line].strip())
        cycle = data['cycle']
        pid = data['pid']
        g_cycles[cycle] = {'ready_pid': pid, 'events': []}

# Now collect all events for each G cycle based on line positions
# G cycles lines: 0-4, 5-9, 10-14, ..., 45-49
for i in range(10):
    for event_idx in range(5):
        line_idx = i * 5 + event_idx
        if line_idx < len(lines):
            data = json.loads(lines[line_idx].strip())
            cycle = data['cycle']
            if cycle in g_cycles:
                g_cycles[cycle]['events'].append((data['event'], data['pid']))

# Parse F cycles (next 20 lines, cycles 1-10, 2 events each)
# F cycles lines: 50-51 (F1), 52-53 (F2), ..., 68-69 (F10)
f_cycles_clean = []
for i in range(50, 70, 2):  # Take pairs of lines for each F cycle
    if i + 1 < len(lines):
        cycle_data = []
        for j in range(2):
            if i + j < len(lines):
                data = json.loads(lines[i + j].strip())
                cycle_data.append((data['event'], data['pid']))
        # Determine F cycle number
        f_cycle_num = (i - 50) // 2 + 1  # F cycle number 1-10
        f_cycles_clean.append({'cycle': f_cycle_num, 'events': cycle_data})

print("=== G CYCLES (G01-G10) ===")
for cycle in sorted(g_cycles.keys()):
    data = g_cycles[cycle]
    pids = [pid for _, pid in data['events']]
    all_same = len(set(pids)) == 1
    print(f"G{cycle}: events={len(data['events'])}, PIDs={pids}, all_same={all_same}")

print("\n=== F CYCLES (F01-F10) ===")
for fc in f_cycles_clean:
    pids = [pid for _, pid in fc['events']]
    all_same = len(set(pids)) == 1
    print(f"F{fc['cycle']}: events={len(fc['events'])}, PIDs={pids}, all_same={all_same}")

# Now create the matrix
print("\n=== EVIDENCE MATRIX (EM-03) ===")
print("Cycle | Ready | PID_Replace | PID_Kill | PID_Replace_Done | Target_Recovery")
print("-" * 70)

for cycle in sorted(g_cycles.keys()):
    data = g_cycles[cycle]
    pids = [pid for _, pid in data['events']]
    all_same = len(set(pids)) == 1
    pid_replace = 'real' if all_same else 'N/A'
    print(f"G{cycle:2d} | real | {pid_replace} | {'real' if all_same else 'N/A'} | {'YES' if all_same else 'NO'} | NEW")

for fc in f_cycles_clean:
    pids = [pid for _, pid in fc['events']]
    all_same = len(set(pids)) == 1
    print(f"F{fc['cycle']:2d} | real | N/A | {'real' if all_same else 'N/A'} | NO | OLD")