import json, os, tempfile
from mercury_ai.database.replay_storage import ReplayStorage
from mercury_ai.database.snapshot_logger import compute_replay_id_from_snapshot, DecisionSnapshotLogger
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from unittest.mock import MagicMock
from mercury_ai.database.replay_storage import ReplayMetrics

tmp = tempfile.mkdtemp()
output_dir = os.path.join(tmp, 'replay_results')
os.makedirs(output_dir, exist_ok=True)
snap_dir = os.path.join(tmp, 'snapshots')
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
logger.save(snapA)
logger.save(snapB)

storage = ReplayStorage(output_dir=output_dir)

# --- C4-CLOSURE-03: Exact duplicate detection ---
print("=== C4-CLOSURE-03: Exact duplicate detection ===")

# Save A, then save A again with identical content
storage.save(audit_id, snapA, ReplayMetrics(mae=0.0, mfe=0.0, pl=10.0, hit=True))
print(f'After save A (first): files = {sorted(os.listdir(output_dir))}')

# Try saving A again (exact duplicate - same audit_id, same replay_id, same run_id)
try:
    storage.save(audit_id, snapA, ReplayMetrics(mae=0.0, mfe=0.0, pl=10.0, hit=True))
    print('Second save A (identical): NO ERROR - file may have been updated or skipped')
except ValueError as e:
    print(f'Second save A (identical): ValueError raised (as expected) - {e}')

# Save B with different run_id should coexist with A
storage.save(audit_id, snapB, ReplayMetrics(mae=0.0, mfe=0.0, pl=-40.0, hit=False), run_id='B')
print(f'After save B (different run_id): files = {sorted(os.listdir(output_dir))}')

# Verify both files exist
json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
print(f'JSON files: {json_files}')

# Read both files
for jf in json_files:
    fpath = os.path.join(output_dir, jf)
    with open(fpath) as f:
        data = json.load(f)
    print(f'  {jf}: audit_id={data["audit_id"]}, replay_id={data["replay_id"]}, run_id={data.get("run_id", "N/A")}, pl={data["pl"]}')

print("\n--- C4-CLOSURE-03 evidence captured ---")

# --- C4-CLOSURE-04: Snapshot A + Metrics B never paired ---
print("\n=== C4-CLOSURE-04: Snapshot A + Metrics B never paired ===")

# We already have snapA metrics in output_dir from save A above (pl=10)
# Now test: snapshot A (replay_id rA) should pair with its own metrics (pl=10), 
# NOT with metrics B (pl=-40)

# Let's test analytics pairing
from mercury_ai.analysis.institutional_analytics_engine import InstitutionalAnalyticsEngine
replay_dir = output_dir
snapshot_dir = snap_dir

eng = InstitutionalAnalyticsEngine(snapshot_dir=snapshot_dir, replay_dir=replay_dir)
df = eng._load_data()
print(f'DataFrame rows: {len(df)}')
if len(df) > 0:
    for i, row in df.iterrows():
        print(f'  Row {i}: audit_id={row["audit_id"]}, replay_id={row["replay_id"]}, pl={row["pl"]}, hit={row["hit"]}')

# The key test: with only metrics A (pl=10) present, snapshot A should pair, snapshot B should not pair (or be skipped)
# And with both metrics A and B, each should pair correctly via replay_id

print("\n--- C4-CLOSURE-04/03 evidence captured ---")