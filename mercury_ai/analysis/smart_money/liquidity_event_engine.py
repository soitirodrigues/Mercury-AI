from typing import List, Tuple
from dataclasses import dataclass
import pandas as pd
import numpy as np
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
        # Fix: input validation — need at least 20 rows for sweep detection
        if df is None or len(df) < 20:
            return []
        events = []
        
        # Calculate ATR for adaptive thresholds
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df['Close'].shift()).abs()
        low_close = (df['Low'] - df['Close'].shift()).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=14, min_periods=1).mean()
        atr_val = float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else 0.0
        
        # 1. Pools/Sweeps (Baseado em preço)
        recent_low = df['Low'].iloc[-20:-1].min()
        recent_high = df['High'].iloc[-20:-1].max()
        if df['Low'].iloc[-1] < recent_low:
            # Sweep below — bullish reversal context (liquidity grabbed below)
            direction = "BULLISH"
            events.append(LiquidityEvent(
                LiquidityEventType.LIQUIDITY_SWEEP, 
                float(df['Low'].iloc[-1]), 85.0, 90.0, f"Preço rompeu mínima recente ({recent_low:.2f}) capturando liquidez — contexto {direction}"
            ))
        elif df['High'].iloc[-1] > recent_high:
            # Sweep above — bearish reversal context (liquidity grabbed above)
            direction = "BEARISH"
            events.append(LiquidityEvent(
                LiquidityEventType.LIQUIDITY_SWEEP, 
                float(df['High'].iloc[-1]), 85.0, 90.0, f"Preço rompeu máxima recente ({recent_high:.2f}) capturando liquidez — contexto {direction}"
            ))
            
        # 2. Voids — use ATR-based threshold instead of hardcoded 0.005
        gap_threshold = max(atr_val * 0.5, 0.001) if atr_val > 0 else 0.005
        if df['Open'].iloc[-1] > df['Close'].iloc[-2] + gap_threshold:
            events.append(LiquidityEvent(
                LiquidityEventType.LIQUIDITY_VOID,
                float(df['Open'].iloc[-1]), 60.0, 70.0, f"Gap de liquidez detectado (threshold ATR: {gap_threshold:.4f})"
            ))
        elif df['Open'].iloc[-1] < df['Close'].iloc[-2] - gap_threshold:
            events.append(LiquidityEvent(
                LiquidityEventType.LIQUIDITY_VOID,
                float(df['Open'].iloc[-1]), 60.0, 70.0, f"Gap de liquidez (baixa) detectado (threshold ATR: {gap_threshold:.4f})"
            ))
            
        return events

    def detect_with_evidence(self, df: pd.DataFrame) -> Tuple[List[LiquidityEvent], List[Evidence]]:
        """Detect liquidity events and convert them to Evidence objects in one call."""
        events = self.detect(df)
        evidences = [self.to_evidence(e) for e in events]
        return events, evidences

    def to_evidence(self, event: LiquidityEvent) -> Evidence:
        # Fix: directional based on event context instead of always NEUTRAL
        if "BULLISH" in event.explanation:
            direction = "BULLISH"
        elif "BEARISH" in event.explanation:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"
        return Evidence(
            engine_name="LiquidityEventEngine",
            evidence_name=event.event_type.value,
            direction=direction,
            strength=event.strength,
            confidence=event.confidence,
            description=event.explanation,
            weight=50.0
        )
