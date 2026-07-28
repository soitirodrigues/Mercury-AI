import unittest
import numpy as np
from mercury_ai.analysis.performance_engine import PerformanceEngine
from mercury_ai.analysis.historical_replay_engine import ReplayMetrics

class TestPerformanceEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PerformanceEngine(risk_free_rate=0.0)

    def test_calculate_drawdown(self):
        # Equity curve with a clear peak and drawdown
        # Peak at 10, drops to 4 (DD=6), recovers to 12
        equity = np.array([0, 5, 10, 8, 4, 6, 12])
        max_dd, recovery_time = self.engine._calculate_drawdown(equity)
        
        self.assertEqual(max_dd, 6.0)
        # Recovery time is from peak (idx 2) to the point of max DD (idx 4)
        # In the current implementation, recovery_time is the distance from last peak to the max DD point
        self.assertEqual(recovery_time, 2)

    def test_calculate_sharpe(self):
        # Constant positive returns
        returns = np.array([1.0, 1.0, 1.0, 1.0])
        # std is 0, should return 0.0 as per implementation to avoid div by zero
        self.assertEqual(self.engine._calculate_sharpe(returns), 0.0)
        
        # Variable returns
        returns = np.array([1.0, -1.0, 1.0, -1.0])
        # mean=0, std=1.0 -> sharpe=0
        self.assertEqual(self.engine._calculate_sharpe(returns), 0.0)

    def test_calculate_sortino(self):
        # Only positive returns
        returns = np.array([1.0, 2.0, 1.0])
        # downside_returns is empty, should return inf
        self.assertEqual(self.engine._calculate_sortino(returns), float('inf'))
        
        # Mixed returns
        returns = np.array([1.0, -1.0, 1.0, -1.0])
        # mean=0, downside_returns=[-1, -1], downside_std=0 -> returns 0.0
        self.assertEqual(self.engine._calculate_sortino(returns), 0.0)

    def test_asset_performance_basic(self):
        # Mock trades: 2 wins, 1 loss
        trades = [
            ReplayMetrics(pl=100.0, mae=10.0, mfe=110.0, hit=1),
            ReplayMetrics(pl=50.0, mae=5.0, mfe=60.0, hit=1),
            ReplayMetrics(pl=-30.0, mae=40.0, mfe=10.0, hit=0),
        ]
        
        perf = self.engine.calculate_asset_performance("BTC-USD", trades)
        
        self.assertEqual(perf.total_trades, 3)
        self.assertEqual(perf.pnl_accumulated, 120.0)
        self.assertAlmostEqual(perf.win_rate, 2/3)
        self.assertEqual(perf.profit_factor, 150.0 / 30.0)
        self.assertEqual(perf.expectancy, 120.0 / 3)

    def test_universe_performance(self):
        # Asset A: 1 win
        # Asset B: 1 loss
        all_results = {
            "AssetA": [ReplayMetrics(pl=100.0, mae=0, mfe=100, hit=1)],
            "AssetB": [ReplayMetrics(pl=-50.0, mae=50, mfe=0, hit=0)]
        }
        
        univ = self.engine.calculate_universe_performance(all_results)
        
        self.assertEqual(univ.total_assets, 2)
        self.assertEqual(univ.global_pnl, 50.0)
        self.assertEqual(univ.global_win_rate, 0.5)
        self.assertEqual(univ.global_profit_factor, 100.0 / 50.0)

if __name__ == "__main__":
    unittest.main()
