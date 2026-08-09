from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME
from mercury_ai.utils.deterministic_clock import DeterministicClock

@dataclass(frozen=True)
class Evidence:
    engine_name: str
    evidence_name: str
    direction: str  # BULLISH / BEARISH / NEUTRAL
    strength: float # 0-100
    confidence: float # 0-100
    description: str
    weight: float
    contribution_score: float = 0.0
    quality_score: float = 100.0
    context_score: float = 100.0
    timeframe: str = DEFAULT_TIMEFRAME
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        engine_name: str,
        evidence_name: str,
        direction: str,
        strength: float,
        confidence: float,
        description: str,
        weight: float,
        contribution_score: float = 0.0,
        quality_score: float = 100.0,
        context_score: float = 100.0,
        timeframe: str = DEFAULT_TIMEFRAME,
        timestamp: str | None = None,
        metadata: Dict[str, Any] | Mapping[str, Any] | None = None,
    ) -> Evidence:
        """Factory que garante imutabilidade profunda de metadata."""
        ts = timestamp if timestamp is not None else DeterministicClock.utcnow().isoformat()
        meta: Dict[str, Any] = dict(metadata) if metadata is not None else {}
        return cls(
            engine_name=engine_name,
            evidence_name=evidence_name,
            direction=direction,
            strength=float(strength),
            confidence=float(confidence),
            description=description,
            weight=float(weight),
            contribution_score=float(contribution_score),
            quality_score=float(quality_score),
            context_score=float(context_score),
            timeframe=timeframe,
            timestamp=ts,
            metadata=meta,
        )
