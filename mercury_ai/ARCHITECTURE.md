# Arquitetura Oficial

Entrada

main.py

↓

MercuryScanner

↓

AnalysisPipeline

↓

AnalysisResult

## Responsabilidades

MercuryScanner

- Executa múltiplos ativos
- Coordena a execução

AnalysisPipeline

- Orquestrador principal

MarketDataService

- Obtém dados

IndicatorEngine

- Calcula indicadores

TrendAnalyzer

- Analisa tendência

SmartMoneyEngine

- Analisa contexto institucional

MarketContextBuilder

- Constrói contexto

ConfluenceEngine

- Decide BUY / SELL / WAIT