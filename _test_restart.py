import json, os, tempfile
from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from unittest.mock import MagicMock

tmp = tempfile.mkdtemp()
output_dir = os.path.join(tmp, 'replay_results')
snap_dir = os.path.join(tmp, 'snapshots')
os.makedirs(output_dir, exist_ok=True)
os.makedirs(snap_dir, exist_ok=True)

audit_id = "X"

decision_result = DecisionResult(
    decision='BUY', grade='A', confidence=0.75, clarity=0.9, risk_score=0.1,
    score=1.0, quality=1.0, expected_strength=1.0, buy_probability=0.7,
    sell_probability=0.2, wait_probability=0.1, expected_risk=0.1, expected_reward=0.2,
    expected_drawdown=0.05, audit_id=audit_id, version_metadata=None,
    summary='s', explanation=None, technical_reason='', warnings=(), weaknesses=(), blockers=(),
    institutional_alignment=True, evidence_ranking=None, explainability=None,
)
context = MarketContext(
    market=MagicMock(), trend=(), price_action=MagicMock(), support_resistance=MagicMock(),
    smart_money=MagicMock(), liquidity=MagicMock(), market_state=MagicMock(),
    market_regime=MagicMock(), mtf_consensus=MagicMock(), risk_assessment=MagicMock(),
)
bundle = MarketEvidenceBundle(evidences=(), timestamp='2025-01-01T00:00:00Z', asset='BTC-USD', timeframe='5m')

snapA = DecisionSnapshot(
    timestamp='2025-01-01T00:00:00Z', asset='BTC-USD', timeframe='5m',
    context=context, evidence_bundle=bundle, decision_result=decision_result,
    version_metadata=None, audit_events=(), session_id='SESSION-A', replay_id='',
)
snapB = DecisionSnapshot(
    timestamp='2025-01-01T01:00:00Z', asset='BTC-USD', timeframe='5m',
    context=context, evidence_bundle=bundle, decision_result=decision_result,
    version_metadata=None, audit_events=(), session_id='SESSION-B', replay_id='',
)

logger = DecisionSnapshotLogger(base_path=snap_dir)
snapA = logger.save(snapA)
snapB = logger.save(snapB)

storage = ReplayStorage(output_dir=output_dir)

print("=== Restart/reload test ===")

# Save A and B
storage.save(audit_id, snapA, ReplayMetrics(mae=0.0, mfe=0.0, pl=10.0, hit=True), run_id='A')
storage.save(audit_id, snapB, ReplayMetrics(mae=0.0, mfe=0.0, pl=-40.0, hit=False), run_id='B')

print(f'Files after saves: {sorted(os.listdir(output_dir))}')

# Simulate reload: read the files and verify content
json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
print(f'Files: {json_files}')

# Read and verify each file
for jf in json_files:
    fpath = os.path.join(output_dir, jf)
    with open(fpath) as f:
        data = json.load(f)
    print(f'  {jf}:')
    print(f'    audit_id: {data.get("audit_id")}')
    print(f'    replay_id: {data.get("replay_id")}')
    print(f'    run_id: {data.get("run_id")}')
    print(f'    pl: {data.get("pl")}')
    print(f'    hit: {data.get("hit")}')

# Simulate restart: delete and re-save, or just verify files persist
print(f'\n--- Restart simulation ---')
print('Files persist after "restart":', len(os.listdir(output_dir)) == 2)

# Now save C to verify A and B are still there
storage.save(audit_id, snapA, ReplayMetrics(mae=0.0, mfe=0.0, pl=5.0, hit=True), run_id='C')
print(f'After save C: {sorted(os.listdir(output_dir))}')

# Verify A and B are still present and correct
json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
pl_values = []
for jf in json_files:
    fpath = os.path.join(output_dir, jf)
    with open(fpath) as f:
        data = json.load(f)
    pl_values.append(data.get('pl'))
    print(f'  {jf}: pl={data.get("pl")}, run_id={data.get("run_id")}')

print(f'\npl values: {pl_values}')
print(f'A and B preserved: {10.0 in pl_values and -40.0 in pl_values}')
print(f'C is new: {5.0 in pl_values}')

print('\n=== Restart/reload test complete ===')