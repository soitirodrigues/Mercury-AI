with open('pytest_output.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
    
# Look for the pytest summary at the end
# Print last 30 lines
lines = content.split('\n')
print(f"Total lines: {len(lines)}")
print("Last 30 non-empty lines:")
for line in lines[-30:]:
    if line.strip():
        print(line)