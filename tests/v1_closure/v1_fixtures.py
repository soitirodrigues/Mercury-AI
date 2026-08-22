"""
MERCURY-AI V1 — CLOSURE FIXTURES

Este arquivo NÃO altera produção.

Ele deve reutilizar os factories/fixtures existentes no projeto.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.market_regime import MarketRegime, MarketRegimeEnum
from mercury_ai.models.market_state import MarketState, MarketStateEnum
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.models.liquidity_profile import LiquidityProfile
from mercury_ai.models.evidence import Evidence


def _make_evidence(engine_name: str, evidence_name: str, direction: str, strength: float, confidence: float = 0.9, description: str = "", weight: float = 1.0) -> Evidence:
    """Cria uma Evidence com os parâmetros corretos."""
    return Evidence(engine_name, evidence_name, direction, strength, confidence, description, weight)


def build_buy_case():
    """
    Retornar o fixture/contexto que o próprio projeto já usa
    para produzir BUY.

    PRIORIDADE:
        1. fixture existente
        2. factory existente
        3. builder existente

    NÃO criar MarketContext artificial aqui se o projeto já possui
    um fixture operacional.
    """
    from mercury_ai.analysis.market_context_builder import MarketContextBuilder

    builder = MarketContextBuilder()

    # Cria evidências simples que indicam BUY
    evidence1 = _make_evidence('trend', 'trend_evidence', 'BUY', 0.85)
    evidence2 = _make_evidence('structure', 'structure_evidence', 'BUY', 0.75)

    # Cria MarketContext com direcionalidade BUY
    market_context = builder.build(
        market=MagicMock(),
        trend=[evidence1, evidence2],
        price_action=MagicMock(),
        support_resistance=MagicMock(),
        smart_money=MagicMock(),
        market_state=MagicMock(),
        regime=MagicMock(),
        risk_assessment=MagicMock(),
        mtf_consensus=MagicMock(),
        structure=MagicMock(),
    )

    # Retorna o contexto e também dados adicionais esperados pelo pipeline
    return {
        "context": market_context,
        "expected_direction": "BUY",
        "confluence_score": 85.0,
        "is_valid": True,
        "opportunity_grade": "A",
    }


def build_sell_case():
    """
    Retornar o fixture/contexto que produz SELL.
    """

    from mercury_ai.analysis.market_context_builder import MarketContextBuilder

    builder = MarketContextBuilder()

    # Cria evidências simples que indicam SELL
    evidence1 = _make_evidence('trend', 'trend_evidence', 'SELL', 0.85)
    evidence2 = _make_evidence('structure', 'structure_evidence', 'SELL', 0.75)

    # Cria MarketContext com direcionalidade SELL
    market_context = builder.build(
        market=MagicMock(),
        trend=[evidence1, evidence2],
        price_action=MagicMock(),
        support_resistance=MagicMock(),
        smart_money=MagicMock(),
        market_state=MagicMock(),
        regime=MagicMock(),
        risk_assessment=MagicMock(),
        mtf_consensus=MagicMock(),
        structure=MagicMock(),
    )

    # Retorna o contexto e também dados adicionais esperados pelo pipeline
    return {
        "context": market_context,
        "expected_direction": "SELL",
        "confluence_score": 85.0,  # Lower confluence for SELL in this test
        "is_valid": True,
        "opportunity_grade": "A",
    }


def build_wait_case():
    """
    Retornar o fixture/contexto que produz WAIT legítimo.
    """

    from mercury_ai.analysis.market_context_builder import MarketContextBuilder

    builder = MarketContextBuilder()

    # Cria evidências que resultam em WAIT (conflito, baixa confluência, etc.)
    evidence1 = _make_evidence('trend', 'trend_evidence', 'BUY', 0.55)  # Moderate strength
    evidence2 = _make_evidence('structure', 'structure_evidence', 'SELL', 0.50)  # Moderate strength

    # Cria MarketContext com direcionalidade mista (resultará em WAIT)
    market_context = builder.build(
        market=MagicMock(),
        trend=[evidence1, evidence2],
        price_action=MagicMock(),
        support_resistance=MagicMock(),
        smart_money=MagicMock(),
        market_state=MagicMock(),
        regime=MagicMock(),
        risk_assessment=MagicMock(),
        mtf_consensus=MagicMock(),
        structure=MagicMock(),
    )

    # Retorna o contexto e também dados adicionais esperados pelo pipeline
    return {
        "context": market_context,
        "expected_direction": "WAIT",
        "confluence_score": 30.0,  # Low confluence → WAIT
        "is_valid": True,
        "opportunity_grade": "D",  # Grade D → WAIT per resolver rules
    }