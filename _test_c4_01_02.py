import json, os, tempfile, threading
from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
from mercury_ai.database.snapshot_logger import compute_replay_id_from_snapshot, DecisionSnapshotLogger
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from unittest.mock import MagicMock

tmp = tempfile.mkdtemp()
output_dir = os.path.join(tmp, 'replay_results')
os.makedirs(output_dir, exist_ok=True)

# Create audit_id X
audit_id = "X"

# Create snapshots A and B with same audit_id but different session_ids -> different replay_ids
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

logger = DecisionSnapshotLogger(base_path=os.path.join(tmp, 'snapshots'))
snapA = logger.save(snapA)
snapB = logger.save(snapB)

rA = compute_replay_id_from_snapshot(snapA)
rB = compute_replay_id_from_snapshot(snapB)
print(f'replay_id A = {rA}')
print(f'replay_id B = {rB}')

# Metrics A: confidence=0.61, pl=10
metrics_A = ReplayMetrics(mae=0.0, mfe=0.0, pl=10.0, hit=True)
# Metrics B: confidence=0.93, pl=-40
metrics_B = ReplayMetrics(mae=0.0, mfe=0.0, pl=-40.0, hit=False)

storage = ReplayStorage(output_dir=output_dir)

# Track files created
files_before = set() if not os.path.exists(output_dir) else set(os.listdir(output_dir))
print(f'Files before: {files_before}')

# Concurrent save: save A and B with same audit_id but different run_id A/B
results = {'A': None, 'B': None, 'errors': []}
def save_with_log(tag, snap, metrics, run_id_val):
    try:
        storage.save(audit_id, snap, metrics, run_id=run_id_val)
        results[tag] = 'success'
        # List files after save
        files_after = set(os.listdir(output_dir))
        results[f'{tag}_files'] = files_after - files_before
        files_before.update(results[f'{tag}_files'])
    except Exception as e:
        results[tag] = f'error: {e}'
        results['errors'].append(f'{tag}: {e}')

t1 = threading.Thread(target=save_with_log, args=('A', snapA, metrics_A, 'A'))
t2 = threading.Thread(target=save_with_log, args=('B', snapB, metrics_B, 'B'))
t1.start()
t2.start()
t1.join()
t2.join()

print(f'Results A: {results["A"]}')
print(f'Results B: {results["B"]}')
print(f'Errors: {results["errors"]}')
print(f'Files in output_dir: {sorted(os.listdir(output_dir))}')

# Verify: both files should exist with different run_suffixes
json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
print(f'JSON files created: {json_files}')

# Read and verify file contents
for jf in json_files:
    fpath = os.path.join(output_dir, jf)
    with open(fpath) as f:
        data = json.load(f)
    print(f'File: {jf}, audit_id={data.get("audit_id")}, replay_id={data.get("replay_id")}, run_id={data.get("run_id")}, pl={data.get("pl")}, confidence={data.get("confidence")}')

print("\n--- C4-CLOSURE-01/02 evidence captured ---")