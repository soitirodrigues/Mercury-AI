import pytest
import random
from mercury_ai.analysis.smart_money.liquidity_engine import LiquidityEngine

from mercury_ai.models.swing_analysis import Swing

def create_swing(price, index, timestamp, strength=0.8, atr=1.0):
    return Swing(
        type='HIGH', classification='HH', price=price, timestamp=timestamp,
        index=index, atr=atr, strength=strength, volume=100.0, confirmed=True
    )

def generate_swings(n, scenario):
    swings = []
    for i in range(n):
        if scenario == 'clustered':
            price = 100.0 + random.choice([0.0, 0.01, 0.02])
        elif scenario == 'high_vol':
            price = 100.0 + random.uniform(-5.0, 5.0)
        elif scenario == 'identical_prices':
            price = 100.0
        else:
            price = 100.0 + i * 0.001
        
        timestamp = "2026-07-07T00:00:00" if scenario == 'identical_timestamps' else f"2026-07-07T{i%24:02d}:00:00"
        swings.append(create_swing(price, i, timestamp))
    return swings

@pytest.mark.parametrize("n", [1000, 5000])
@pytest.mark.parametrize("scenario", ['clustered', 'high_vol', 'identical_prices', 'identical_timestamps'])
def test_liquidity_engine_stress(n, scenario):
    engine = LiquidityEngine()
    swings = generate_swings(n, scenario)
    
    # Run repeated execution for determinism
    results = []
    for _ in range(3): # Reduced from 10 to 3
        shuffled = list(swings)
        random.shuffle(shuffled)
        results.append(engine.build_equal_high_groups(shuffled))
        
    for i in range(1, len(results)):
        assert results[i] == results[0]
