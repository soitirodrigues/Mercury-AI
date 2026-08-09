"""
Probe B1 — Executa o pipeline REAL (AnalysisPipeline) com dados deterministicos
(seed 42, 1200 candles 5min continuos, mesmo do criterio C8 da auditoria).
Captura a cadeia completa de decisao para provar que a formula canonica
desbloqueia grade != D e permite BUY/SELL.

Uso: python probe_b1_pipeline.py
"""
import numpy as np
import pandas as pd

from mercury_ai.core.analysis_pipeline import AnalysisPipeline


def generate_continuous_data(n_candles: int = 1200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    # Caminhada aleatoria com tendencia suave para criar sinal direcional real
    drift = np.linspace(0.0, 0.5, n_candles)
    close = 100.0 + np.cumsum(np.random.randn(n_candles) * 0.3 + drift * 0.05)
    open_ = np.concatenate([[close[0]], close[:-1]])
    high = np.maximum(open_, close) + np.abs(np.random.randn(n_candles) * 0.2)
    low = np.minimum(open_, close) - np.abs(np.random.randn(n_candles) * 0.2)
    volume = np.random.randint(1000, 5000, n_candles)
    idx = pd.date_range("2024-01-01", periods=n_candles, freq="5min")
    return pd.DataFrame(
        {"close": close, "high": high, "low": low, "open": open_, "volume": volume},
        index=idx,
    )


def main():
    print("=" * 78)
    print("PROBE B1 — PIPELINE REAL (AnalysisPipeline) com formula canonica")
    print("=" * 78)

    df = generate_continuous_data()

    # Injeta o dataframe direto no pipeline via provider historico
    from mercury_ai.providers.historical_replay_provider import HistoricalReplayProvider
    from mercury_ai.data.market_data import MarketDataService
    provider = HistoricalReplayProvider()
    provider.set_data(df)
    provider.set_index(len(df) - 1)

    pipeline = AnalysisPipeline(
        market_service=MarketDataService(providers=[provider]),
        providers=[provider],
    )
    result = pipeline.analyze("EURUSD=X", silent=False)

    print("-" * 78)
    print("RESULTADO DO PIPELINE REAL")
    print("-" * 78)
    d = result.decision
    print(f"decision          : {d.decision}")
    print(f"score             : {d.score:.4f}")
    print(f"confidence        : {d.confidence:.4f}")
    print(f"buy_probability   : {d.buy_probability:.2f}")
    print(f"sell_probability  : {d.sell_probability:.2f}")
    print(f"wait_probability  : {d.wait_probability:.2f}")
    if d.explainability:
        e = d.explainability
        print(f"grade             : {e.opportunity_grade}")
        print(f"dominant_direction: {e.dominant_direction}")
        print(f"triggered_rule    : {e.triggered_rule}")
        print(f"institutional_score: {e.institutional_score:.4f}")
        print(f"conflicting       : {e.conflicting_signals}")
        print("decision_chain:")
        for step in e.decision_chain:
            print(f"   {step}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
