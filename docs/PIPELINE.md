# Pipeline de Análise - Mercury AI V1

O `AnalysisPipeline` é o coração do sistema, responsável por orquestrar diversos motores de análise.

- **Orquestração:** `AnalysisPipeline` chama motores em sequência.
- **Motores:** Evidence Engine, Smart Money Engines (BOS, CHOCH, Liquidity), Candlestick Engine, Trend Engine.
- **Consolidação:** Consolida os resultados em um `AnalysisResult`.
