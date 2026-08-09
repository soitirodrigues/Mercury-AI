"""
Replay deterministico DEPOIS da correcao B1 (formula canonica 0.50/0.35/0.15).

Roda HistoricalReplayEngine.run_replay sobre dados deterministicos (seed 42)
e conta as decisoes BUY/SELL/WAIT + distribuicao de grades.

Comparacao com o baseline ANTES (auditoria): 91/91 WAIT, 0 BUY, 0 SELL.

Uso: python probe_b1_replay.py
"""
import numpy as np
import pandas as pd

from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine


def generate_deterministic_data(n_candles, seed=42):
    """Gera OHLCV deterministico e VALIDO (high >= max(open,close),
    low <= min(open,close), timestamps 5min continuos sem gaps)."""
    np.random.seed(seed)
    close = 100.0 + np.random.randn(n_candles).cumsum()
    open_ = np.concatenate([[close[0]], close[:-1]])
    # high >= max(open, close); low <= min(open, close)
    spread = np.abs(np.random.randn(n_candles)) * 0.3
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread
    volume = np.random.randint(1000, 5000, n_candles)
    data = {
        "close": close,
        "high": high,
        "low": low,
        "open": open_,
        "volume": volume,
    }
    return pd.DataFrame(
        data,
        index=pd.date_range("2025-01-01", periods=n_candles, freq="5min"),
    )


def main():
    from collections import Counter
    from mercury_ai.database import replay_storage as rs_mod
    from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine

    # Coleta decisoes em memoria sem depender dos arquivos JSON (que sofrem
    # deduplicacao por audit_id = hash(asset+timeframe+len_evidences)).
    decisions = []
    reasons = []
    grades = []
    original_save = rs_mod.ReplayStorage.save

    def collect_save(self, audit_id, snapshot, metrics):
        dr = snapshot.decision_result
        decisions.append(dr.decision)
        # Extrai apenas a regra disparada (se disponivel)
        rule = "?"
        if dr.explainability is not None:
            rule = dr.explainability.triggered_rule
        reasons.append(rule)
        grades.append(dr.grade if hasattr(dr, "grade") else "?")
        return original_save(self, audit_id, snapshot, metrics)

    rs_mod.ReplayStorage.save = collect_save

    n_candles = 180  # 180 - 60 (start) - 20 (future) = 100 decisoes
    df = generate_deterministic_data(n_candles)

    engine = HistoricalReplayEngine()
    metrics = engine.run_replay("EURUSD=X", df, n_candles=20, silent=True)

    # Restaura o metodo original
    rs_mod.ReplayStorage.save = original_save

    print("=" * 72)
    print("REPLAY DETERMINISTICO DEPOIS DA CORRECAO B1")
    print("=" * 72)
    print(f"Candles de entrada      : {n_candles}")
    print(f"Decisoes geradas        : {len(metrics)}")
    print(f"Replay stats            : {engine.replay_stats}")
    print("-" * 72)

    counter = Counter(decisions)
    print("DISTRIBUICAO DE DECISOES (replay DEPOIS):")
    for k in ("BUY", "SELL", "WAIT"):
        print(f"   {k:5s}: {counter.get(k, 0)}")
    print(f"   TOTAL: {len(decisions)}")

    from collections import Counter as C2
    grade_counter = C2(grades)
    print("-" * 72)
    print("DISTRIBUICAO DE GRADES (replay DEPOIS):")
    for g in ("A+", "A", "B", "C", "D"):
        print(f"   {g:3s}: {grade_counter.get(g, 0)}")

    print("-" * 72)
    print("AMOSTRA DE RAZOES (regras disparadas):")
    for r in reasons[:6]:
        print(f"   {r}")

    print("-" * 72)
    print("BASELINE ANTES (auditoria): 91 WAIT / 0 BUY / 0 SELL")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
