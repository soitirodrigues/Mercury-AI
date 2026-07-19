# Mercury AI V1.0 - Documentação Técnica (Release V1)

## 1. Visão Geral
A Mercury AI V1.0 é um sistema de tomada de decisão institucional, focado em explicabilidade, rastreabilidade e determinismo para operações assistidas em conta Demo.

## 2. Arquitetura
O sistema adota uma arquitetura modular baseada em engines de decisão desacopladas. O fluxo de dados é unidirecional, iniciando na ingestão de dados de mercado, passando por engines de análise técnica e fundamentalista, até a persistência institucional.

## 3. Pipeline Institucional
A `AnalysisPipeline` é o orquestrador central. O fluxo é:
1.  **Ingestão:** `MarketDataService` (via Yahoo Finance).
2.  **Qualidade:** `DataQualityEngine` filtra dados inválidos.
3.  **Análise:** Execução paralela de engines (Trend, Smart Money, Liquidity, etc.).
4.  **Confluência:** `ConfluenceEngine` consolida evidências pesadas.
5.  **Decisão:** `MercuryDecisionEngine` gera o veredito final.
6.  **Persistência:** `SnapshotLogger` salva o estado completo para auditoria futura.

## 4. Motores de Análise (Engines)
O sistema conta com 9 engines core validadas:
*   Validation, Quality, Ranking, Conflict, Confidence, Confluence, Memory, Probability, Narrative.

## 5. Explicabilidade (Explainability)
Toda decisão é acompanhada por uma `TradingExplanation`, contendo:
*   Fatores Bullish/Bearish.
*   Conflitos identificados.
*   Sequência lógica da análise.

## 6. Replay e Snapshots
O sistema utiliza `DecisionSnapshot` para garantir que qualquer decisão possa ser reconstruída de forma *bit-identical*. Os snapshots incluem o contexto original, evidências, ranking e resultados.

## 7. Dashboard e Monitoramento
Painel de controle em Streamlit que consome dados processados (`AnalysisResult`) para exibir:
*   Métricas de performance e risco.
*   Histórico e Replay de trades.
*   Estatísticas institucionais.
*   HealthCheck de componentes.

## 8. Estatísticas e Auditoria
Módulos dedicados para análise estatística (*PerformanceAnalytics*, *PerformanceStatistics*, *EnginePerformanceAuditor*) que utilizam dados históricos persistidos para auditar a eficácia de cada engine e a calibração da confiança.

## 9. Modo Demo (Read Only)
O sistema opera em modo de segurança `READ_ONLY`, bloqueando qualquer execução de ordens reais, enquanto permite a execução integral da pipeline para fins de monitoramento e validação.

## 10. Prontidão
O sistema foi certificado técnica e institucionalmente (Testes: 42/42 aprovados), atingindo o status **READY** para operação assistida.
