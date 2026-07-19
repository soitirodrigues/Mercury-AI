# Fluxo de Dados - Mercury AI V1

1. **Coleta:** `MarketDataProvider` obtém dados brutos.
2. **Análise:** `AnalysisPipeline` aplica motores de análise (Price Action, Smart Money, etc.).
3. **Decisão:** `MercuryDecisionEngine` gera a tese institucional.
4. **Persistência:** `DecisionSnapshotLogger` registra o resultado.
5. **Visualização:** `Dashboard` consome os resultados para o usuário.
