from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import pandas as pd

@dataclass(frozen=True)
class AssetPerformance:
    """Estatísticas de performance para um único ativo."""
    asset: str
    total_trades: int
    pnl_accumulated: float
    win_rate: float
    profit_factor: float
    expectancy: float
    avg_win: float
    avg_loss: float
    max_drawdown: float
    recovery_time_candles: int
    sharpe_ratio: float
    sortino_ratio: float
    equity_curve: Tuple[float, ...]

@dataclass(frozen=True)
class UniversePerformance:
    """Estatísticas consolidadas de todo o universo de ativos."""
    total_assets: int
    global_pnl: float
    global_win_rate: float
    global_profit_factor: float
    global_max_drawdown: float
    global_sharpe: float
    global_sortino: float
    asset_stats: Dict[str, AssetPerformance]
    consolidated_equity_curve: Tuple[float, ...]
