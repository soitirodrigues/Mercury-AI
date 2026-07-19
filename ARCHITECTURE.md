# Mercury AI V1.0 - Arquitetura de Sistema

## 1. Visão Geral
A Mercury AI V1.0 é um sistema de tomada de decisão institucional baseado em evidências, projetado para alta explicabilidade, rastreabilidade e determinismo. A arquitetura segue um fluxo rígido de processamento de dados (Pipeline Institucional), garantindo que cada decisão seja fundamentada, auditable e reprodutível.

## 2. Fluxo Arquitetural (Pipeline de Dados)

### Market Data
*   **Componentes:** `MarketDataService`, `YahooFinanceProvider`.
*   **Responsabilidade:** Coleta bruta de dados, normalização e validação inicial (`DataQualityEngine`).

### Analysis Engines
*   **Componentes:** Diversas engines técnicas (`TrendAnalyzer`, `SmartMoneyEngine`, `LiquidityEngine`, etc.).
*   **Responsabilidade:** Geração de `Evidence` (vetores de opinião técnica) baseados em indicadores e análise estrutural.

### Conflict Resolution
*   **Componentes:** `ConflictResolutionEngine`.
*   **Responsabilidade:** Filtragem e ponderação de evidências conflitantes (bullish vs bearish) para resolver o suporte real de mercado.

### Confluence
*   **Componentes:** `ConfluenceEngine`.
*   **Responsabilidade:** Cálculo da confluência de sinais ponderada, determinando o `score` e a direção dominante do mercado.

### Decision
*   **Componentes:** `MercuryDecisionEngine`.
*   **Responsabilidade:** Consolidação do suporte, risco e confluência para gerar o `DecisionResult` (BUY, SELL, WAIT).

### Probability
*   **Componentes:** `ProbabilityEngine`.
*   **Responsabilidade:** Calibração probabilística da execução, ajustada pelo regime de mercado e risco institucional.

### Narrative
*   **Componentes:** `NarrativeEngine`.
*   **Responsabilidade:** Geração da `TradingExplanation` (racional, fatores de suporte/conflito, sequência lógica).

### Snapshot
*   **Componentes:** `DecisionSnapshotLogger`.
*   **Responsabilidade:** Persistência do estado completo da decisão (`DecisionSnapshot`) para auditoria de longo prazo.

### Replay
*   **Componentes:** `SnapshotLogger` + `AnalysisPipeline`.
*   **Responsabilidade:** Capacidade de reconstrução *bit-identical* de decisões passadas a partir de dados persistidos.

### Statistics
*   **Componentes:** `PerformanceAnalytics`, `PerformanceStatistics`, `EnginePerformanceAuditor`.
*   **Responsabilidade:** Cálculo determinístico de métricas institucionais (Win Rate, Expectancy, Engine Performance) sobre dados históricos.

### Dashboard
*   **Componentes:** Streamlit (`app/dashboard/`).
*   **Responsabilidade:** Exposição institucional de dados processados, histórico, estatísticas e replay, com monitoramento em tempo real.
