from typing import List
from dataclasses import dataclass
import pandas as pd
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.liquidity_event_enum import LiquidityEventType

@dataclass(frozen=True)
class LiquidityEvent:
    event_type: LiquidityEventType
    price: float
    strength: float
    confidence: float
    explanation: str

class LiquidityEventEngine:
    """
    Motor institucional de detecção de eventos de liquidez.
    """

    def detect(self, df: pd.DataFrame) -> List[LiquidityEvent]:
        events = []
        
        # Exemplo simplificado de detecção
        # 1. Pools/Sweeps (Baseado em preço)
        if df['Low'].iloc[-1] < df['Low'].iloc[-20:-1].min():
            events.append(LiquidityEvent(
                LiquidityEventType.LIQUIDITY_SWEEP, 
                df['Low'].iloc[-1], 85.0, 90.0, "Preço rompeu mínima recente capturando liquidez"
            ))
            
        # 2. Voids
        if df['Open'].iloc[-1] > df['Close'].iloc[-2] + 0.005:
            events.append(LiquidityEvent(
                LiquidityEventType.LIQUIDITY_VOID,
                df['Open'].iloc[-1], 60.0, 70.0, "Gap de liquidez detectado"
            ))
            
        return events

    def to_evidence(self, event: LiquidityEvent) -> Evidence:
        return Evidence(
            engine_name="LiquidityEventEngine",
            evidence_name=event.event_type.value,
            direction="NEUTRAL",
            strength=event.strength,
            confidence=event.confidence,
            description=event.explanation,
            weight=50.0
        )
