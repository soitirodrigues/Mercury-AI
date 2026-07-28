import pandas as pd
import os
from datetime import datetime
from typing import Dict, List

from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.performance_engine import PerformanceEngine
from mercury_ai.database.replay_storage import ReplayMetrics
from mercury_ai.models.equity_metrics import AssetPerformance, UniversePerformance


def load_local_data(asset: str):
    # Try to load data from parquet file
    filepath = f"data/replay/{asset}/data.parquet"
    if not os.path.exists(filepath):
        print(f"Skipping {asset}: data not found at {filepath}")
        return None
    try:
        df = pd.read_parquet(filepath)
        return df
    except Exception as e:
        print(f"Skipping {asset}: Error loading data: {e}")
        return None


def generate_performance_report(
    universe_perf: UniversePerformance,
    output_path: str = "data/replay_results/institutional_report.txt"
):
    """Gera relatório institucional formatado com todas as métricas."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    lines = []
    lines.append("=" * 72)
    lines.append("  MERCURY AI V1 — RELATÓRIO INSTITUCIONAL DE BACKTEST")
    lines.append(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"  Ativos analisados:          {universe_perf.total_assets}")
    lines.append(f"  PnL Global:                 {universe_perf.global_pnl:+.6f}")
    lines.append(f"  Win Rate Global:            {universe_perf.global_win_rate:.2%}")
    lines.append(f"  Profit Factor Global:       {universe_perf.global_profit_factor:.4f}")
    lines.append(f"  Sharpe Ratio Global:        {universe_perf.global_sharpe:.4f}")
    lines.append(f"  Sortino Ratio Global:       {universe_perf.global_sortino:.4f}")
    lines.append(f"  Max Drawdown Global:        {universe_perf.global_max_drawdown:.6f}")
    lines.append("")
    lines.append("-" * 72)
    lines.append("  PERFORMANCE POR ATIVO")
    lines.append("-" * 72)
    lines.append("")
    lines.append(f"  {'Ativo':<12} {'Trades':>6} {'PnL':>12} {'WinRate':>8} {'Sharpe':>8} {'Sortino':>8} {'Drawdown':>10}")
    lines.append(f"  {'-'*12} {'-'*6} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*10}")
    
    for asset_name, stats in sorted(universe_perf.asset_stats.items()):
        lines.append(
            f"  {asset_name:<12} {stats.total_trades:>6} {stats.pnl_accumulated:>+12.6f} "
            f"{stats.win_rate:>7.1%} {stats.sharpe_ratio:>8.4f} "
            f"{stats.sortino_ratio:>8.4f} {stats.max_drawdown:>10.6f}"
        )
    
    lines.append("")
    lines.append("=" * 72)
    lines.append("  FIM DO RELATÓRIO")
    lines.append("=" * 72)
    
    report = "\n".join(lines)
    print(report)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nRelatório salvo em: {output_path}")
    return report


def run_institutional_replay():
    # Dynamically discover assets
    data_dir = "data/replay"
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist.")
        return

    assets = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    if not assets:
        print("Nenhum ativo encontrado para replay.")
        return
    
    print(f"Universo de ativos descobertos: {len(assets)}")
    for a in assets:
        print(f"  - {a}")
    print()
    
    engine = HistoricalReplayEngine()
    perf_engine = PerformanceEngine()
    
    all_results: Dict[str, List[ReplayMetrics]] = {}
    
    for asset in assets:
        print(f"--- Replaying {asset} ---")
        df = load_local_data(asset)
        if df is None:
            continue
        
        # Run replay and collect metrics
        metrics = engine.run_replay(asset, df, n_candles=20)
        all_results[asset] = metrics
        
        # Per-asset summary
        if metrics:
            pnl = sum(m.pl for m in metrics)
            hits = sum(1 for m in metrics if m.hit)
            total = len(metrics)
            print(f"  Trades: {total} | PnL: {pnl:+.6f} | Hits: {hits}/{total} ({hits/total:.1%})")
        else:
            print(f"  Nenhum trade gerado.")
        print(f"  Replay for {asset} complete.")
        print()
    
    if not all_results:
        print("Nenhum resultado de replay para processar.")
        return
    
    # Compute universe performance
    print("=" * 72)
    print("  COMPUTANDO MÉTRICAS DE PERFORMANCE...")
    print("=" * 72)
    print()
    
    universe_perf = perf_engine.calculate_universe_performance(all_results)
    
    # Generate report
    generate_performance_report(universe_perf)


if __name__ == "__main__":
    run_institutional_replay()
