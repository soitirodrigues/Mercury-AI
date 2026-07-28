"""Teste rápido do replay institucional com dataset reduzido."""
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.performance_engine import PerformanceEngine
from mercury_ai.database.replay_storage import ReplayMetrics

DATA_DIR = "data/replay_test"
ASSET = "EURUSD=X"

def main():
    filepath = os.path.join(DATA_DIR, ASSET, "data.parquet")
    if not os.path.exists(filepath):
        print(f"ERRO: {filepath} não encontrado")
        return

    df = pd.read_parquet(filepath)
    print(f"Carregado: {len(df)} candles de {ASSET}")
    print(f"Range: {df.index[0]} a {df.index[-1]}")
    print()

    engine = HistoricalReplayEngine()
    perf_engine = PerformanceEngine()

    print(f"--- Replaying {ASSET} (test mode) ---")
    metrics = engine.run_replay(ASSET, df, n_candles=20)
    print()

    if metrics:
        pnl = sum(m.pl for m in metrics)
        hits = sum(1 for m in metrics if m.hit)
        total = len(metrics)
        print(f"Resultados do replay:")
        print(f"  Trades: {total}")
        print(f"  PnL: {pnl:+.6f}")
        print(f"  Hits: {hits}/{total} ({hits/total:.1%})")
        print()

        # Calcular performance
        print("=" * 60)
        print("  COMPUTANDO MÉTRICAS DE PERFORMANCE...")
        print("=" * 60)
        print()

        universe_perf = perf_engine.calculate_universe_performance({ASSET: metrics})

        print(f"  Ativos:                 {universe_perf.total_assets}")
        print(f"  PnL Global:             {universe_perf.global_pnl:+.6f}")
        print(f"  Win Rate Global:        {universe_perf.global_win_rate:.2%}")
        print(f"  Profit Factor Global:   {universe_perf.global_profit_factor:.4f}")
        print(f"  Sharpe Ratio Global:    {universe_perf.global_sharpe:.4f}")
        print(f"  Sortino Ratio Global:   {universe_perf.global_sortino:.4f}")
        print(f"  Max Drawdown Global:    {universe_perf.global_max_drawdown:.6f}")
        print()

        # Salvar relatório
        os.makedirs("data/replay_results", exist_ok=True)
        output_path = "data/replay_results/test_report.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"TESTE RÁPIDO - Mercury AI V1\n")
            f.write(f"Ativo: {ASSET}\n")
            f.write(f"Candles: {len(df)}\n")
            f.write(f"Trades: {total}\n")
            f.write(f"PnL: {pnl:+.6f}\n")
            f.write(f"Win Rate: {universe_perf.global_win_rate:.2%}\n")
            f.write(f"Sharpe: {universe_perf.global_sharpe:.4f}\n")
            f.write(f"Sortino: {universe_perf.global_sortino:.4f}\n")
            f.write(f"Max Drawdown: {universe_perf.global_max_drawdown:.6f}\n")
            f.write(f"Profit Factor: {universe_perf.global_profit_factor:.4f}\n")
        print(f"Relatório salvo em: {output_path}")
    else:
        print("Nenhum trade gerado.")

if __name__ == "__main__":
    main()