"""F2 — Session Eligibility Contract (Forex weekend closed, Crypto 24/7).

Covers Fase 10 cases 1-6. Deterministic via explicit UTC datetimes,
not wall-clock-dependent. MarketSessions is the single decision point.
"""
from datetime import datetime, timezone
import pytest
from mercury_ai.sessions.market_sessions import MarketSessions
from mercury_ai.utils.deterministic_clock import DeterministicClock


@pytest.fixture
def ms():
    return MarketSessions()


# 2026-09-04 Fri, 2026-09-05 Sat, 2026-09-06 Sun, 2026-09-07 Mon (ISO)
FRI = datetime(2026, 9, 4, 12, 0, tzinfo=timezone.utc)
SAT = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)
SUN = datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc)
MON_0005 = datetime(2026, 9, 7, 0, 5, tzinfo=timezone.utc)
MON_NOON = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)


def test_case1_forex_saturday_closed(ms):
    assert ms.is_market_eligible("FOREX", SAT) is False
    assert ms.is_symbol_eligible("EURUSD=X", SAT) is False
    assert ms.is_symbol_eligible("USDAUD=X", SAT) is False
    assert ms.is_symbol_eligible("EURNZD=X", SAT) is False


def test_case2_forex_sunday_closed(ms):
    assert ms.is_market_eligible("FOREX", SUN) is False
    assert ms.is_symbol_eligible("GBPUSD=X", SUN) is False


def test_case3_crypto_saturday_open(ms):
    assert ms.is_market_eligible("CRYPTO", SAT) is True
    assert ms.is_symbol_eligible("BTC-USD", SAT) is True
    assert ms.is_symbol_eligible("LTC-USD", SAT) is True
    assert ms.is_symbol_eligible("LINK-USD", SAT) is True
    assert ms.is_symbol_eligible("XPL-USD", SAT) is True


def test_case4_crypto_sunday_open(ms):
    assert ms.is_market_eligible("CRYPTO", SUN) is True
    assert ms.is_symbol_eligible("ETH-USD", SUN) is True
    assert ms.is_symbol_eligible("SOL-USD", SUN) is True


def test_case5_sunday_to_monday_forex_reopens(ms):
    # Sunday late -> Monday early UTC weekday transition
    assert ms.is_market_eligible("FOREX", SUN) is False
    assert ms.is_market_eligible("FOREX", MON_0005) is True
    assert ms.is_market_eligible("FOREX", MON_NOON) is True
    assert ms.is_symbol_eligible("EURUSD=X", MON_0005) is True


def test_case6_crypto_sunday_to_monday_stays_open(ms):
    assert ms.is_market_eligible("CRYPTO", SUN) is True
    assert ms.is_market_eligible("CRYPTO", MON_0005) is True
    assert ms.is_market_eligible("CRYPTO", MON_NOON) is True


def test_weekday_forex_open(ms):
    assert ms.is_market_eligible("FOREX", FRI) is True
    assert ms.is_market_eligible("FOREX", MON_NOON) is True


def test_deterministic_clock_path(ms):
    """DeterministicClock frozen path mirrors explicit now."""
    DeterministicClock.set_time(SAT.replace(tzinfo=None))
    try:
        assert ms.is_market_eligible("FOREX") is False
        assert ms.is_market_eligible("CRYPTO") is True
    finally:
        DeterministicClock.reset()


def test_scanner_weekend_filters_forex_only(ms):
    """Scanner gate keeps 12 Crypto on weekend, 39 on weekday."""
    from mercury_ai.brain.scanner import MercuryScanner
    from mercury_ai.config.universe import get_asset

    scanner = MercuryScanner()
    auth = scanner.asset_registry.get_assets_for_broker("XP")
    enabled = [a for a in scanner.asset_registry.assets.values() if a.enabled and a.profile == "Demo" and a.symbol in auth]
    assert len(enabled) == 39

    kept_sat = [a for a in enabled if ms.is_symbol_eligible(a.symbol, SAT)]
    skipped_sat = [a for a in enabled if not ms.is_symbol_eligible(a.symbol, SAT)]
    assert len(kept_sat) == 12
    assert len(skipped_sat) == 27
    assert all(get_asset(a.symbol).market == "CRYPTO" for a in kept_sat)

    kept_mon = [a for a in enabled if ms.is_symbol_eligible(a.symbol, MON_NOON)]
    assert len(kept_mon) == 39


def test_runner_weekend_filters_forex_only(ms):
    from mercury_ai.operations.m5_operational.runner import M5OperationalRunner

    r = M5OperationalRunner(universe=None)
    kept = [s for s in r.universe if ms.is_symbol_eligible(s, SAT)]
    assert len(kept) == 12
    kept_mon = [s for s in r.universe if ms.is_symbol_eligible(s, MON_NOON)]
    assert len(kept_mon) == 39
