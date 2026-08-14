import json, os, tempfile
from mercury_ai.analysis.learning_engine import LearningEngine
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from unittest.mock import MagicMock

tmp = tempfile.mkdtemp()
snap_dir = os.path.join(tmp, 'snapshots')
metrics_dir = os.path.join(tmp, 'metrics')
os.makedirs(snap_dir, exist_ok=True)
os.makedirs(metrics_dir, exist_ok=True)

decision_result = DecisionResult(
    decision='BUY', grade='A', confidence=0.75, clarity=0.9, risk_score=0.1,
    score=1.0, quality=1.0, expected_strength=1.0, buy_probability=0.7,
    sell_probability=0.2, wait_probability=0.1, expected_risk=0.1, expected_reward=0.2,
    expected_drawdown=0.05, audit_id='X', version_metadata=None,
    summary='s', explanation=None, technical_reason='', warnings=(), weaknesses=(), blockers=(),
    institutional_alignment=True, evidence_ranking=None, explainability=None,
)
context = MarketContext(
    market=MagicMock(), trend=(), price_action=MagicMock(), support_resistance=MagicMock(),
    smart_money=MagicMock(), liquidity=MagicMock(), market_state=MagicMock(),
    market_regime=MagicMock(), mtf_consensus=MagicMock(), risk_assessment=MagicMock(),
)
bundle = MarketEvidenceBundle(evidences=(), timestamp='2025-01-01T00:00:00Z', asset='BTC-USD', timeframe='5m')

# Create two snapshots with same audit_id X, different replay_ids via session_id
snapA = DecisionSnapshot(
    timestamp='2025-01-01T00:00:00Z', asset='BTC-USD', timeframe='5m',
    context=context, evidence_bundle=bundle, decision_result=decision_result,
    version_metadata=None, audit_events=(), session_id='SESSION-A', replay_id='',  # will be computed by logger or manually set
)
snapB = DecisionSnapshot(
    timestamp='2025-01-01T01:00:00Z', asset='BTC-USD', timeframe='5m',
    context=context, evidence_bundle=bundle, decision_result=decision_result,
    version_metadata=None, audit_events=(), session_id='SESSION-B', replay_id='',
)

# Use the DecisionSnapshotLogger to compute replay_ids and save
from mercury_ai.database.snapshot_logger import compute_replay_id_from_snapshot, DecisionSnapshotLogger
logger = DecisionSnapshotLogger(base_path=snap_dir)
snapA = logger.save(snapA)
snapB = logger.save(snapB)

print(f'snapA.replay_id = {snapA.replay_id}')
print(f'snapB.replay_id = {snapB.replay_id}')

# Now create metrics files
# Metrics A: with replay_id = snapA.replay_id, pl=10
metrics_A = {
    'audit_id': 'X',
    'replay_id': snapA.replay_id,
    'hit': True,
    'pl': 10.0,
}
with open(os.path.join(metrics_dir, f'{snapA.replay_id}.json'), 'w') as f:
    json.dump(metrics_A, f, indent=4)

# Metrics B: with replay_id = snapB.replay_id, pl=-40
metrics_B = {
    'audit_id': 'X',
    'replay_id': snapB.replay_id,
    'hit': True,
    'pl': -40.0,
}
with open(os.path.join(metrics_dir, f'{snapB.replay_id}.json'), 'w') as f:
    json.dump(metrics_B, f, indent=4)

# Now test LearningEngine
engine = LearningEngine(metrics_dir=metrics_dir, snapshots_dir=snap_dir)
report = engine.run_learning()
print(f'Learning report best_assets: {report.get("best_assets", [])}')
if report.get("best_assets"):
    best = report["best_assets"][0]
    print(f'Best asset: {best["asset"]}, win_rate: {best["win_rate"]}')
    # Check if A->outcome A and B->outcome B (no mixing)
    # Since replay_ids distinct and metrics keyed by replay_id, should be correct
    # But need to verify the legacy ambiguous scenario below

# Now test legacy scenario: metrics WITHOUT replay_id, same audit_id X
# Metrics legacy 1: no replay_id, pl=5
metrics_legacy1 = {
    'audit_id': 'X',
    'hit': True,
    'pl': 5.0,
    'return_pct': 0.005,
}
with open(os.path.join(metrics_dir, 'legacy1.json'), 'w') as f:
    json.dump(metrics_legacy1, f, indent=4)

# Metrics legacy 2: no replay_id, pl=-20, also audit_id X
metrics_legacy2 = {
    'audit_id': 'X',
    'hit': False,
    'pl': -20.0,
    'return_pct': -0.02,
}
with open(os.path.join(metrics_dir, 'legacy2.json'), 'w') as f:
    json.dump(metrics_legacy2, f, indent=4)

# Run learning again with legacy metrics present
report2 = engine.run_learning()
print(f'\nWith legacy metrics: best_assets: {report2.get("best_assets", [])}')
if report2.get("best_assets"):
    best2 = report2["best_assets"][0]
    print(f'Best asset: {best2["asset"]}, win_rate: {best2["win_rate"]}, total: {best2["total"]}')

# Also test with only legacy metrics, no replay-identified snapshots
# Remove the first two metric files temporarily? Actually let's just observe what happens.
# With snapshots A+B present AND legacy1+legacy2 metric files:
# LearningEngine's id_to_context currently last-wins on audit_id X -> arbitrary
# and metrics without replay_id fall back to audit_id -> may pair with whichever snapshot last-wins
print('\n--- Analysis complete ---')