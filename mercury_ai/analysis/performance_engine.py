import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from mercury_ai.models.equity_metrics import AssetPerformance, UniversePerformance
from mercury_ai.analysis.historical_replay_engine import ReplayMetrics

class PerformanceEngine:
    """
    Motor de cálculo de performance e equity para backtests institucionais.
    Implementa métricas financeiras rigorosas sem look-ahead bias.
    """

    def __init__(self, risk_free_rate: float = 0.0):
        self.risk_free_rate = risk_free_rate

    def calculate_asset_performance(self, asset: str, trades: List[ReplayMetrics]) -> AssetPerformance:
        if not trades:
            return self._empty_asset_performance(asset)

        pnls = np.array([t.pl for t in trades])
        
        # PnL Acumulado
        pnl_accumulated = np.sum(pnls)
        
        # Win Rate
        wins = pnls[pnls > 0]
        losses = pnls[pnls <= 0]
        win_rate = len(wins) / len(pnls) if len(pnls) > 0 else 0.0
        
        # Profit Factor
        sum_wins = np.sum(wins)
        sum_losses = abs(np.sum(losses))
        profit_factor = sum_wins / sum_losses if sum_losses > 0 else float('inf')
        
        # Expectancy
        expectancy = np.mean(pnls) if len(pnls) > 0 else 0.0
        
        # Average Win/Loss
        avg_win = np.mean(wins) if len(wins) > 0 else 0.0
        avg_loss = abs(np.mean(losses)) if len(losses) > 0 else 0.0
        
        # Equity Curve & Drawdown
        equity_curve = np.cumsum(pnls)
        max_drawdown, recovery_time = self._calculate_drawdown(equity_curve)
        
        # Sharpe & Sortino
        sharpe = self._calculate_sharpe(pnls)
        sortino = self._calculate_sortino(pnls)
        
        return AssetPerformance(
            asset=asset,
            total_trades=len(trades),
            pnl_accumulated=float(pnl_accumulated),
            win_rate=float(win_rate),
            profit_factor=float(profit_factor),
            expectancy=float(expectancy),
            avg_win=float(avg_win),
            avg_loss=float(avg_loss),
            max_drawdown=float(max_drawdown),
            recovery_time_candles=int(recovery_time),
            sharpe_ratio=float(sharpe),
            sortino_ratio=float(sortino),
            equity_curve=tuple(equity_curve.tolist())
        )

    def calculate_universe_performance(self, all_asset_results: Dict[str, List[ReplayMetrics]]) -> UniversePerformance:
        asset_stats = {}
        all_pnls = []
        
        for asset, trades in all_asset_results.items():
            stats = self.calculate_asset_performance(asset, trades)
            asset_stats[asset] = stats
            all_pnls.extend([t.pl for t in trades])
            
        all_pnls = np.array(all_pnls)
        
        # Global Metrics
        global_pnl = np.sum(all_pnls)
        wins = all_pnls[all_pnls > 0]
        losses = all_pnls[all_pnls <= 0]
        
        global_win_rate = len(wins) / len(all_pnls) if len(all_pnls) > 0 else 0.0
        sum_wins = np.sum(wins)
        sum_losses = abs(np.sum(losses))
        global_profit_factor = sum_wins / sum_losses if sum_losses > 0 else float('inf')
        
        global_equity_curve = np.cumsum(all_pnls)
        global_max_dd, _ = self._calculate_drawdown(global_equity_curve)
        
        return UniversePerformance(
            total_assets=len(all_asset_results),
            global_pnl=float(global_pnl),
            global_win_rate=float(global_win_rate),
            global_profit_factor=float(global_profit_factor),
            global_max_drawdown=float(global_max_dd),
            global_sharpe=float(self._calculate_sharpe(all_pnls)),
            global_sortino=float(self._calculate_sortino(all_pnls)),
            asset_stats=asset_stats,
            consolidated_equity_curve=tuple(global_equity_curve.tolist())
        )

    def _calculate_drawdown(self, equity_curve: np.ndarray) -> Tuple[float, int]:
        if len(equity_curve) == 0:
            return 0.0, 0
            
        peak = equity_curve[0]
        max_dd = 0.0
        recovery_time = 0
        last_peak_idx = 0
        
        for i, val in enumerate(equity_curve):
            if val > peak:
                peak = val
                last_peak_idx = i
            
            dd = peak - val
            if dd > max_dd:
                max_dd = dd
                recovery_time = i - last_peak_idx
                
        return float(max_dd), recovery_time

    def _calculate_sharpe(self, returns: np.ndarray) -> float:
        if len(returns) < 2: return 0.0
        std = np.std(returns)
        if std == 0: return 0.0
        return float((np.mean(returns) - self.risk_free_rate) / std)

    def _calculate_sortino(self, returns: np.ndarray) -> float:
        if len(returns) < 2: return 0.0
        downside_returns = returns[returns < 0]
        if len(downside_returns) == 0: return float('inf')
        downside_std = np.std(downside_returns)
        if downside_std == 0: return 0.0
        return float((np.mean(returns) - self.risk_free_rate) / downside_std)

    def _empty_asset_performance(self, asset: str) -> AssetPerformance:
        return AssetPerformance(
            asset=asset, total_trades=0, pnl_accumulated=0.0, win_rate=0.0,
            profit_factor=0.0, expectancy=0.0, avg_win=0.0, avg_loss=0.0,
            max_drawdown=0.0, recovery_time_candles=0, sharpe_ratio=0.0,
            sortino_ratio=0.0, equity_curve=()
        )
