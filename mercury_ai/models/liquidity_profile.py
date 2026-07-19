from dataclasses import dataclass

@dataclass(frozen=True)
class LiquidityProfile:
    internal_liquidity: float = 0.0
    external_liquidity: float = 0.0
    liquidity_sweep: bool = False
    equal_highs: bool = False
    equal_lows: bool = False
    stop_hunt_probability: float = 0.0
    liquidity_density: float = 0.0
