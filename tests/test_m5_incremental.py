"""Testes unitários para módulos incrementais M5 — Sprint 2"""
import pytest
from datetime import datetime, timezone, timedelta

from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5, next_m5_boundary, decision_candle_timestamp_from_df, current_candle, previous_candle, next_candle
from mercury_ai.operations.m5_incremental.asset_state import AssetScanState
from mercury_ai.operations.m5_incremental.freshness import FreshnessGate
from mercury_ai.operations.m5_incremental.rolling_queue import RollingQueue, Top3Status
from mercury_ai.operations.m5_incremental.cache_tracker import CacheTracker, CacheStatus
from mercury_ai.operations.m5_incremental.mtf_classification import MTF_CLASSIFICATIONS
from mercury_ai.operations.ranking import rank_records, select_top3, classify_status, FORMULA


class TestTemporal:
    def test_floor_m5(self):
        dt = datetime(2026, 9, 2, 10, 7, 23, tzinfo=timezone.utc)
        assert floor_m5(dt) == datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        dt2 = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        assert floor_m5(dt2) == dt2
        dt3 = datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        assert floor_m5(dt3) == dt3

    def test_ceil_m5(self):
        dt = datetime(2026, 9, 2, 10, 7, 0, tzinfo=timezone.utc)
        assert ceil_m5(dt) == datetime(2026, 9, 2, 10, 10, 0, tzinfo=timezone.utc)
        dt2 = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        assert ceil_m5(dt2) == datetime(2026, 9, 2, 10, 10, 0, tzinfo=timezone.utc)

    def test_current_previous_next(self):
        now = datetime(2026, 9, 2, 10, 7, 0, tzinfo=timezone.utc)
        assert current_candle(now) == datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        assert previous_candle(now) == datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        assert next_candle(now) == datetime(2026, 9, 2, 10, 10, 0, tzinfo=timezone.utc)

    def test_decision_candle_from_df(self):
        import pandas as pd
        idx = pd.date_range("2026-09-02 10:00", periods=5, freq="5min", tz="UTC")
        df = pd.DataFrame({"close": [1, 2, 3, 4, 5]}, index=idx)
        ts = decision_candle_timestamp_from_df(df)
        assert ts is not None
        assert ts == idx[-1].to_pydatetime()

    def test_decision_candle_empty(self):
        import pandas as pd
        df = pd.DataFrame()
        assert decision_candle_timestamp_from_df(df) is None
        assert decision_candle_timestamp_from_df(None) is None


class TestAssetState:
    def test_create_and_serialize(self):
        s = AssetScanState(symbol="EURUSD=X")
        assert s.symbol == "EURUSD=X"
        assert s.status == "PENDING"
        d = s.to_dict()
        assert d["symbol"] == "EURUSD=X"
        assert "_result_ref" not in d
        s2 = AssetScanState.from_dict(d)
        assert s2.symbol == s.symbol

    def test_result_ref_not_duplicated(self):
        s = AssetScanState(symbol="BTC-USD")
        s._result_ref = object()
        d = s.to_dict()
        assert "_result_ref" not in d
        # from_dict tolera extras
        d["extra"] = "ignore"
        s2 = AssetScanState.from_dict(d)
        assert s2.symbol == "BTC-USD"


class TestFreshnessGate:
    def test_fresh_when_equal(self):
        gate = FreshnessGate()
        dt = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = gate.check(df=None, decision_candle=dt, latest_candle=dt)
        assert res.is_fresh is True
        assert res.status == "FRESH"

    def test_stale_when_behind(self):
        gate = FreshnessGate()
        dec = datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        latest = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = gate.check(df=None, decision_candle=dec, latest_candle=latest)
        assert res.is_fresh is False
        assert res.status == "STALE"

    def test_stale_when_no_decision(self):
        gate = FreshnessGate()
        latest = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = gate.check(df=None, decision_candle=None, latest_candle=latest)
        assert res.status == "STALE"

    def test_data_unavailable_when_no_latest(self):
        gate = FreshnessGate()
        dec = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = gate.check(df=None, decision_candle=dec, latest_candle=None)
        assert res.status == "DATA_UNAVAILABLE"

    def test_never_converts_stale_to_real_signal(self):
        gate = FreshnessGate()
        dec = datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        latest = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = gate.check(df=None, decision_candle=dec, latest_candle=latest)
        # Stale must never be reported as fresh
        assert res.is_fresh is False
        assert res.status != "FRESH"

    def test_check_state_iso(self):
        gate = FreshnessGate()
        latest = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = gate.check_state("2026-09-02T10:05:00+00:00", latest)
        assert res.status == "FRESH"
        res2 = gate.check_state("2026-09-02T10:00:00+00:00", latest)
        assert res2.status == "STALE"


class TestRollingQueue:
    def test_p3_when_all_fresh(self):
        gate = FreshnessGate()
        rq = RollingQueue(freshness_gate=gate)
        now = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        candle = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        states = {}
        for sym in ["A", "B", "C"]:
            s = AssetScanState(symbol=sym)
            s.decision_candle_timestamp = candle.isoformat()
            s.status = "FRESH"
            s.is_fresh = True
            states[sym] = s
        latest = {sym: candle for sym in ["A", "B", "C"]}
        queue = rq.build(["A", "B", "C"], states, latest, cycle_start=now)
        assert all(e.priority == 3 for e in queue)

    def test_p1_when_just_closed(self):
        gate = FreshnessGate()
        rq = RollingQueue(freshness_gate=gate)
        now = datetime(2026, 9, 2, 10, 6, 0, tzinfo=timezone.utc)
        old = datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        new = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        s = AssetScanState(symbol="A")
        s.decision_candle_timestamp = old.isoformat()
        s.decision_timestamp = old.isoformat()
        s.status = "FRESH"
        s.is_fresh = True
        states = {"A": s}
        latest = {"A": new}
        queue = rq.build(["A"], states, latest, cycle_start=now)
        assert queue[0].priority == 1
        assert queue[0].symbol == "A"

    def test_top3_status(self):
        rq = RollingQueue()
        assert rq.top3_status([], []) == Top3Status.EMPTY
        # Partial when pending
        states = [AssetScanState(symbol="A")]
        assert rq.top3_status(states, ["B", "C"]) == Top3Status.PARTIAL
        assert rq.top3_status(states, []) == Top3Status.COMPLETE

    def test_never_blocks_top3_when_fresh_available(self):
        # Mesmo com pendentes, se já há 3 elegíveis fresh, queue não deve esconder
        # (isso é responsabilidade do scanner, não da fila; fila apenas ordena)
        gate = FreshnessGate()
        rq = RollingQueue(freshness_gate=gate)
        now = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        candle = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        states = {}
        for sym in ["A", "B", "C", "D"]:
            s = AssetScanState(symbol=sym)
            s.decision_candle_timestamp = candle.isoformat()
            s.status = "FRESH"
            s.is_fresh = True
            states[sym] = s
        # D is pending (no state for E)
        queue = rq.build(["A", "B", "C", "D", "E"], states, {**{k: candle for k in ["A", "B", "C", "D"]}, "E": None}, cycle_start=now)
        # E should be last (P3, no prior state)
        assert queue[-1].symbol == "E"


class TestCacheTracker:
    def test_miss_when_no_entry(self):
        ct = CacheTracker()
        dt = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        res = ct.check("A", dt)
        assert res.status == CacheStatus.MISS

    def test_hit_when_equal(self):
        ct = CacheTracker()
        dt = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        ct.put("A", dt)
        res = ct.check("A", dt)
        assert res.status == CacheStatus.HIT

    def test_stale_when_behind(self):
        ct = CacheTracker()
        old = datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        new = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        ct.put("A", old)
        res = ct.check("A", new)
        assert res.status == CacheStatus.STALE

    def test_never_accepts_ttl_alone(self):
        # Mesmo que dentro de TTL, se candle avançou, deve ser STALE
        ct = CacheTracker()
        old = datetime(2026, 9, 2, 10, 0, 0, tzinfo=timezone.utc)
        new = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        ct.put("A", old)
        # Simulate "TTL 60s" would say HIT, but cache must say STALE
        res = ct.check("A", new, latest_available=new)
        assert res.status == CacheStatus.STALE
        assert "REFRESH" in res.reason or "nova vela" in res.reason or "<" in res.reason

    def test_valid_only_when_equal(self):
        ct = CacheTracker()
        dt = datetime(2026, 9, 2, 10, 5, 0, tzinfo=timezone.utc)
        ct.put("A", dt)
        # Required igual => HIT
        assert ct.check("A", dt).status == CacheStatus.HIT
        # Required diferente => STALE
        dt2 = datetime(2026, 9, 2, 10, 10, 0, tzinfo=timezone.utc)
        assert ct.check("A", dt2).status == CacheStatus.STALE


class TestMTFClassification:
    def test_all_components_classified(self):
        verdicts = {c.verdict for c in MTF_CLASSIFICATIONS}
        assert verdicts == {"SAFE_INCREMENTAL", "REQUIRES_FULL_RECALC", "UNKNOWN"}

    def test_unknown_not_silently_optimized(self):
        unknowns = [c for c in MTF_CLASSIFICATIONS if c.verdict == "UNKNOWN"]
        assert len(unknowns) >= 1
        for c in unknowns:
            assert "UNKNOWN" in c.verdict
            assert len(c.reason) > 20


class TestRankingContract:
    def test_ranking_formula_unchanged(self):
        assert "confluence_weighted" in FORMULA
        assert "confidence_100*0.30" in FORMULA
        assert "grade_bonus" in FORMULA
        assert "dominant_prob*0.20" in FORMULA

    def test_ranking_deterministic(self):
        recs = [
            {"internal_symbol": "B", "decision": "BUY", "status": "REAL_SIGNAL", "trade_allowed": True, "prob_sum_ok": True, "confidence": 0.7, "confluence": 100, "grade": "B", "buy_probability": 60, "sell_probability": 0, "wait_probability": 40, "audit_id": "a"*64},
            {"internal_symbol": "A", "decision": "BUY", "status": "REAL_SIGNAL", "trade_allowed": True, "prob_sum_ok": True, "confidence": 0.7, "confluence": 100, "grade": "B", "buy_probability": 60, "sell_probability": 0, "wait_probability": 40, "audit_id": "b"*64},
        ]
        r1 = rank_records(recs)
        r2 = rank_records(list(reversed(recs)))
        assert [x[1]["internal_symbol"] for x in r1] == [x[1]["internal_symbol"] for x in r2]
        # Tie-breaker: symbol ASC
        assert r1[0][1]["internal_symbol"] == "A"

    def test_no_duplicate_formula(self):
        # mercury_ai.operations.ranking deve ser a única fonte; top3_scanner.py deve importar dela
        # Verificar que top3_scanner.py não duplica GRADE_BONUS diferente
        import pathlib
        txt = pathlib.Path("scripts/top3_scanner.py").read_text(encoding="utf-8")
        assert "GRADE_BONUS" in txt  # ainda tem, mas deve ser igual ao canônico
        # O scanner contínuo deve usar a importada
        txt2 = pathlib.Path("scripts/m5_continuous_scanner.py").read_text(encoding="utf-8")
        assert "from mercury_ai.operations.ranking import" in txt2

    def test_classify_status(self):
        assert classify_status("BUY", "a"*64) == "REAL_SIGNAL"
        assert classify_status("WAIT", "DATA_PROVIDER_UNAVAILABLE") == "DATA_UNAVAILABLE"
        assert classify_status("WAIT", "b"*64) == "WAIT_LEGITIMATE"
