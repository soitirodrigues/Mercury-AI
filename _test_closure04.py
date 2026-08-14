import json, os, tempfile
from mercury_ai.database.snapshot_logger import compute_replay_id_from_snapshot, DecisionSnapshotLogger
from mercury_ai.analysis.institutional_analytics_engine import InstitutionalAnalyticsEngine
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from unittest.mock import MagicMock

tmp = tempfile.mkdtemp()
snap_dir = os.path.join(tmp, 'snapshots')
replay_dir = os.path.join(tmp, 'replay_results')
os.makedirs(snap_dir, exist_ok=True)
os.makedirs(replay_dir, exist_ok=True)

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

rA = compute_replay_id_from_snapshot(snapA)
rB = compute_replay_id_from_snapshot(snapB)
print(f'replay_id A = {rA}')
print(f'replay_id B = {rB}')

# Write metrics file with replay_id rB and audit_id X (NO rA file)
metrics_B = {
    'audit_id': 'X',
    'replay_id': rB,
    'hit': True,
    'pl': -40.0,
    'return_pct': -0.04,
}
with open(os.path.join(replay_dir, f'{rB}.json'), 'w') as f:
    json.dump(metrics_B, f, indent=4)

# No metrics_A file present

eng = InstitutionalAnalyticsEngine(snapshot_dir=snap_dir, replay_dir=replay_dir)
df = eng._load_data()
print(f'DataFrame rows: {len(df)}')
if len(df) > 0:
    r0_audit = df.loc[0, 'audit_id']
    r0_replay = df.loc[0, 'replay_id']
    r0_pl = df.loc[0, 'pl']
    print(f'Row 0 audit_id: {r0_audit}')
    print(f'Row 0 replay_id: {r0_replay}')
    print(f'Row 0 pl: {r0_pl}')
    if r0_audit == 'X' and r0_replay == rB and r0_pl == -40.0:
        print('RESULT: BUG - snapshot A incorrectly paired with metrics B via audit_id X fallback (forbidden X->B para A)')
    else:
        print(f'RESULT: other outcome audit={r0_audit} replay={r0_replay} pl={r0_pl}')
else:
    print('RESULT: no rows - snapshot A not paired (correct when replay_id rA absent from metrics AND no fallback or fallback skips)')

print("\n--- Analysis complete ---")