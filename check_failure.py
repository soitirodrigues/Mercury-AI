with open('pytest_output.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find the failed test details
idx = content.find('test_s32_c_01_baseline_clock_ownership')
if idx >= 0:
    section = content[idx:idx+3000]
    failed_idx = section.find('FAILED')
    if failed_idx >= 0:
        print("=== test_s32_c_01_baseline_clock_ownership FAILURE ===")
        print(section[failed_idx:failed_idx+500])