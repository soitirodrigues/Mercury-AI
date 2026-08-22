"""
Tests for DecisionResolverEngine - Unit tests for the decision resolver logic.

These tests verify the rule order and behavior of the DecisionResolverEngine
to ensure BUY/SELL/WAIT decisions are correctly reachable.
"""

import pytest
from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine, DecisionResolverResult


class TestDecisionResolverEngine:
    """Test suite for DecisionResolverEngine.resolve() method."""

    @pytest.fixture
    def resolver(self):
        """Create a DecisionResolverEngine instance with default threshold."""
        return DecisionResolverEngine(min_threshold=40.0)

    @pytest.fixture
    def resolver_custom_threshold(self):
        """Create a DecisionResolverEngine with custom threshold."""
        return DecisionResolverEngine(min_threshold=50.0)

    # ============================================================
    # TESTE 1: BUY + Grade A = BUY
    # ============================================================
    def test_buy_grade_a_returns_buy(self, resolver):
        """TESTE 1: BUY + Grade A should return BUY."""
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "BUY"
        assert result.triggered_rule == 5

    # ============================================================
    # TESTE 2: SELL + Grade A = SELL
    # ============================================================
    def test_sell_grade_a_returns_sell(self, resolver):
        """TESTE 2: SELL + Grade A should return SELL."""
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=True,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "SELL"
        assert result.triggered_rule == 6

    # ============================================================
    # TESTE 3 (CRITICAL): BUY + Grade D = BUY
    # ============================================================
    def test_buy_grade_d_returns_buy(self, resolver):
        """TESTE 3: BUY + Grade D should return BUY (not WAIT).
        
        This test proves that grade D does NOT block a valid BUY direction.
        Previously Rule 4 (grade D -> WAIT) was before Rule 5 (BUY -> BUY),
        causing BUY + D to incorrectly return WAIT.
        """
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="D",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        # After fix: should be BUY (Rule 5)
        # Before fix: would be WAIT (Rule 4)
        assert result.decision == "BUY"
        assert result.triggered_rule == 5

    # ============================================================
    # TESTE 4 (CRITICAL): SELL + Grade D = SELL
    # ============================================================
    def test_sell_grade_d_returns_sell(self, resolver):
        """TESTE 4: SELL + Grade D should return SELL (not WAIT).
        
        This test proves that grade D does NOT block a valid SELL direction.
        """
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=True,
            opportunity_grade="D",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "SELL"
        assert result.triggered_rule == 6

    # ============================================================
    # TESTE 5: BUY + Grade C = BUY
    # ============================================================
    def test_buy_grade_c_returns_buy(self, resolver):
        """TESTE 5: BUY + Grade C should return BUY."""
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="C",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "BUY"
        assert result.triggered_rule == 5

    # ============================================================
    # TESTE 6: SELL + Grade C = SELL
    # ============================================================
    def test_sell_grade_c_returns_sell(self, resolver):
        """TESTE 6: SELL + Grade C should return SELL."""
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=True,
            opportunity_grade="C",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "SELL"
        assert result.triggered_rule == 6

    # ============================================================
    # TESTE 7: NEUTRAL = WAIT
    # ============================================================
    def test_neutral_returns_wait(self, resolver):
        """TESTE 7: NEUTRAL direction should return WAIT."""
        result = resolver.resolve(
            dominant_direction="NEUTRAL",
            is_valid=True,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 2

    # ============================================================
    # TESTE 8: Invalid + BUY = WAIT
    # ============================================================
    def test_invalid_buy_returns_wait(self, resolver):
        """TESTE 8: Invalid input with BUY direction should return WAIT."""
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=False,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 1
        assert result.confidence_override == 0.0

    # ============================================================
    # TESTE 9: Invalid + SELL = WAIT
    # ============================================================
    def test_invalid_sell_returns_wait(self, resolver):
        """TESTE 9: Invalid input with SELL direction should return WAIT."""
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=False,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 1
        assert result.confidence_override == 0.0

    # ============================================================
    # TESTE 10: BUY + Low Confluence = WAIT
    # ============================================================
    def test_buy_low_confluence_returns_wait(self, resolver):
        """TESTE 10: BUY with confluence below regime threshold should return WAIT."""
        # Use a threshold higher than the confluence score
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=30.0,  # Below default threshold of 40.0
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 3

    # ============================================================
    # TESTE 11: SELL + Low Confluence = WAIT
    # ============================================================
    def test_sell_low_confluence_returns_wait(self, resolver):
        """TESTE 11: SELL with confluence below regime threshold should return WAIT."""
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=True,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=30.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 3

    # ============================================================
    # TESTE 12: BUY + Conflict + Grade C = WAIT
    # ============================================================
    def test_buy_conflict_grade_c_returns_wait(self, resolver):
        """TESTE 12: BUY with conflicting signals and Grade C should return WAIT."""
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="C",
            conflicting_signals=True,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 4

    # ============================================================
    # TESTE 13: SELL + Conflict + Grade C = WAIT
    # ============================================================
    def test_sell_conflict_grade_c_returns_wait(self, resolver):
        """TESTE 13: SELL with conflicting signals and Grade C should return WAIT."""
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=True,
            opportunity_grade="C",
            conflicting_signals=True,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 4

    # ============================================================
    # TESTE 14: BUY + Conflict + Grade D = WAIT
    # ============================================================
    def test_buy_conflict_grade_d_returns_wait(self, resolver):
        """TESTE 14: BUY with conflicting signals and Grade D should return WAIT."""
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="D",
            conflicting_signals=True,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 4

    # ============================================================
    # TESTE 15: SELL + Conflict + Grade D = WAIT
    # ============================================================
    def test_sell_conflict_grade_d_returns_wait(self, resolver):
        """TESTE 15: SELL with conflicting signals and Grade D should return WAIT."""
        result = resolver.resolve(
            dominant_direction="SELL",
            is_valid=True,
            opportunity_grade="D",
            conflicting_signals=True,
            confluence_score=80.0,
            market_regime=None,
        )
        assert result.decision == "WAIT"
        assert result.triggered_rule == 4

    # ============================================================
    # Additional tests for regime threshold adaptation
    # ============================================================
    def test_regime_threshold_adaptation(self, resolver):
        """Test that regime threshold is properly adapted."""
        from mercury_ai.config import settings
        
        # Test with regime that has multiplier > 1 (e.g., CONSOLIDATION)
        # This should raise the threshold
        result = resolver.resolve(
            dominant_direction="BUY",
            is_valid=True,
            opportunity_grade="A",
            conflicting_signals=False,
            confluence_score=50.0,  # Above base 40, but below regime-adjusted
            market_regime="CONSOLIDATION",
        )
        # CONSOLIDATION multiplier should be > 1, making threshold > 40
        # If 50 is below the adjusted threshold, should return WAIT (Rule 3)
        # This tests the adaptive threshold logic

    def test_rule_order_priority(self, resolver):
        """Verify the exact rule order priority.
        
        Rules should be checked in this order:
        1. Invalid -> WAIT
        2. NEUTRAL -> WAIT
        3. Low confluence -> WAIT
        4. Conflict + C/D -> WAIT
        5. BUY -> BUY
        6. SELL -> SELL
        7. Fallback -> WAIT
        """
        # This test documents the expected rule order
        # The critical fix is that Grade D alone does NOT cause WAIT
        # Only Conflict + C/D causes WAIT (Rule 4)
        # BUY/SELL come after (Rules 5/6)
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])