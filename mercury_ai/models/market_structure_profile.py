from dataclasses import dataclass, field
from typing import Tuple, Optional
from mercury_ai.models.swing_analysis import Swing

@dataclass(frozen=True)
class MarketStructureProfile:
    classification: str = "UNKNOWN"
    trend: str = "NEUTRAL"  # BULLISH, BEARISH, NEUTRAL
    trend_strength: float = 0.0
    bos_detected: bool = False
    choch_detected: bool = False
    hh_count: int = 0
    hl_count: int = 0
    lh_count: int = 0
    ll_count: int = 0
    expansion: bool = False
    compression: bool = False
    confidence_score: float = 0.0
    trap_detected: bool = False
    liquidity_sweep: bool = False
    breakout: bool = False
    false_breakout: bool = False
    market_shift: bool = False
    pullback: bool = False
    retracement_quality: float = 0.0
    impulse_strength: float = 0.0
    equal_highs: bool = False
    equal_lows: bool = False
    internal_bos: bool = False
    external_bos: bool = False
    last_confirmed_high: float = 0.0
    last_confirmed_low: float = 0.0
    current_sequence: Tuple[str, ...] = field(default_factory=tuple)
    # Estrutural
    bos: bool = False
    choch: bool = False
    mss: bool = False
    break_strength: float = 0.0
    break_price: float = 0.0
    break_timestamp: str = ""
    current_swing: Optional[Swing] = None
    previous_swing: Optional[Swing] = None

    # Liquidez
    stop_hunt: bool = False
    false_break: bool = False
    reclaim: bool = False
    buy_side_liquidity: float = 0.0
    sell_side_liquidity: float = 0.0
    internal_liquidity: float = 0.0
    external_liquidity: float = 0.0
    liquidity_cluster: float = 0.0
    
    # Ordem Flow
    correction_strength: float = 0.0
    expansion_ratio: float = 0.0
    compression_ratio: float = 0.0
    momentum_state: str = "NEUTRAL"
    
    # Displacement
    displacement: bool = False
    displacement_strength: float = 0.0
    displacement_direction: str = "NEUTRAL"

    # Premium/Discount
    premium_zone: float = 0.0
    discount_zone: float = 0.0
    equilibrium: float = 0.0
    ote: float = 0.0
