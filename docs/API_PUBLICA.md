# API Pública - Mercury AI V1

O Mercury AI expõe internamente os motores de análise.

- **Interface:** `AnalysisPipeline` oferece métodos públicos para análise (`analyze(symbol)`).
- **Dados:** Estruturas de dados baseadas em `dataclasses` para garantir tipagem e integridade.
- **Extensibilidade:** Novos engines devem herdar de `BaseEngine`.
