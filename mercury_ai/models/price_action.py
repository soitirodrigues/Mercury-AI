"""
PriceActionAnalysis — Modelo unificado de análise de Price Action.

Este é o ÚNICO modelo de PriceActionAnalysis no codebase.
Substitui os dois modelos incompatíveis anteriores:
  - models/price_action.py (4 campos, confidence: int)
  - models/price_action_analysis.py (15+ campos, confidence: float)

Unificação:
  - Mantém todos os campos dos dois modelos.
  - confidence é float (0.0–100.0) em toda a codebase.
  - trend_structure e last_event preservados para compatibilidade.
  - explanation é Tuple[str, ...] (imutável).
  - evidences é Tuple[Any, ...] (imutável).
  - metadata é dict (mutável, compatível com asdict/pickle).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Tuple


@dataclass(frozen=True)
class PriceActionAnalysis:
    """
    Modelo imutável de análise de Price Action.

    Campos de estrutura (compatibilidade com MarketContext):
        trend_structure: BULLISH / BEARISH / RANGE / UNKNOWN
        last_event: Último evento detectado
        explanation: Tupla imutável de descrições textuais

    Campos de padrões (compatibilidade com PriceActionEngine):
        is_strong_candle, is_weak_candle, is_engulfing, is_pin_bar,
        is_inside_bar, is_outside_bar, is_false_breakout, is_pullback,
        is_rejection, is_continuation, is_exhaustion

    Campos de qualidade:
        confidence: float (0.0–100.0) — NUNCA int
        quality: float (0.0–100.0)
        engine_name: Nome da engine que produziu a análise
    """

    # Campos de estrutura (compatibilidade com MarketContext/PriceActionAnalyzer)
    trend_structure: str = "UNKNOWN"
    last_event: str = "UNKNOWN"
    explanation: Tuple[str, ...] = field(default_factory=tuple)

    # Campos de padrões (compatibilidade com PriceActionEngine)
    engine_name: str = "PriceActionEngine"
    is_strong_candle: bool = False
    is_weak_candle: bool = False
    is_engulfing: bool = False
    is_pin_bar: bool = False
    is_inside_bar: bool = False
    is_outside_bar: bool = False
    is_false_breakout: bool = False
    is_pullback: bool = False
    is_rejection: bool = False
    is_continuation: bool = False
    is_exhaustion: bool = False

    # Campos de qualidade (float, nunca int)
    confidence: float = 0.0
    quality: float = 0.0

    # Campos imutáveis
    evidences: Tuple[Any, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        trend_structure: str = "UNKNOWN",
        last_event: str = "UNKNOWN",
        explanation: Tuple[str, ...] | list[str] | None = None,
        confidence: float = 0.0,
        quality: float = 0.0,
        engine_name: str = "PriceActionEngine",
        is_strong_candle: bool = False,
        is_weak_candle: bool = False,
        is_engulfing: bool = False,
        is_pin_bar: bool = False,
        is_inside_bar: bool = False,
        is_outside_bar: bool = False,
        is_false_breakout: bool = False,
        is_pullback: bool = False,
        is_rejection: bool = False,
        is_continuation: bool = False,
        is_exhaustion: bool = False,
        evidences: Tuple[Any, ...] | list[Any] | None = None,
        metadata: Dict[str, Any] | Mapping[str, Any] | None = None,
    ) -> PriceActionAnalysis:
        """Factory method que garante imutabilidade profunda."""
        exp_tuple: Tuple[str, ...] = (
            tuple(explanation) if explanation is not None else ()
        )
        ev_tuple: Tuple[Any, ...] = (
            tuple(evidences) if evidences is not None else ()
        )
        meta: Dict[str, Any] = dict(metadata) if metadata is not None else {}
        return cls(
            trend_structure=trend_structure,
            last_event=last_event,
            explanation=exp_tuple,
            confidence=float(confidence),
            quality=float(quality),
            engine_name=engine_name,
            is_strong_candle=is_strong_candle,
            is_weak_candle=is_weak_candle,
            is_engulfing=is_engulfing,
            is_pin_bar=is_pin_bar,
            is_inside_bar=is_inside_bar,
            is_outside_bar=is_outside_bar,
            is_false_breakout=is_false_breakout,
            is_pullback=is_pullback,
            is_rejection=is_rejection,
            is_continuation=is_continuation,
            is_exhaustion=is_exhaustion,
            evidences=ev_tuple,
            metadata=meta,
        )