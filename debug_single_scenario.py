"""Quick debug script to find the .lower() error source."""
import sys
import traceback

sys.path.insert(0, '.')

from run_decision_scenarios import DecisionScenarioTester

tester = DecisionScenarioTester('BTC-USD', target_scenarios=1)
configs = tester._generate_scenario_configs()
print(f'Generated {len(configs)} configs')

for i, cfg in enumerate(configs[:1]):
    sid = cfg["scenario_id"]
    print(f'Running scenario {sid}...')
    try:
        result = tester._run_scenario(cfg)
        print(f'Success: {result.success}')
        if not result.success:
            print(f'Error: {result.error}')
    except Exception as e:
        print(f'FULL TRACEBACK:')
        traceback.print_exc()