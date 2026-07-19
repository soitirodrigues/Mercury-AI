# Arquitetura - Mercury AI V1

O Mercury AI segue uma arquitetura modular focada em análise institucional.

```mermaid
graph TD
    A[Market Data] --> B[MercuryScanner]
    B --> C[AnalysisPipeline]
    C --> D[AnalysisResult]
    D --> E[Dashboard/Terminal]
```

## Componentes Principais
- **Brain/Scanner:** Motor de decisão principal.
- **AnalysisPipeline:** Processamento de evidências.
- **UI:** Frontend construído com Streamlit.
