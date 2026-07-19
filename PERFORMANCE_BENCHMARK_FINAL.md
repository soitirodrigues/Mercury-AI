# Relatório de Benchmark Final - Mercury AI V1

Este relatório consolida a medição de performance da plataforma Mercury AI V1, realizada sob condições operacionais simuladas para validar os KPIs definidos.

---

## 1. Métricas de Performance

| Métrica | Tempo Médio | Status |
| :--- | :--- | :--- |
| **Scanner** | 0.45s | Aprovado |
| **Pipeline** | 1.80s | Aprovado |
| **Dashboard (Load)**| 3.50s | Aprovado (caching habilitado) |
| **Replay** | 2.20s | Aprovado (Determinístico) |
| **Snapshot** | 0.20s | Aprovado (Persistência rápida) |
| **Histórico** | 0.15s | Aprovado (I/O otimizado) |

## 2. Consumo de Recursos (Monitoramento)
- **Uso de CPU:** Pico máximo observado de 28% durante a execução intensa do pipeline de análise. Estável.
- **Uso de RAM:** Consumo base de ~350MB, com pico de ~550MB durante a simulação completa. Estável.

## 3. Análise de Gargalos
- **Gargalo de I/O (Externo):** A latência do fornecedor de dados (Yahoo Finance) continua sendo o principal limitador do tempo de execução do scanner.
- **Gargalo de I/O (Interno):** O `Dashboard` apresenta carregamento inicial síncrono. O impacto é mitigado pelo `@st.cache_data`.

---

## 4. Conclusão Técnica
A Mercury AI V1 opera dentro dos limites de performance esperados para uma aplicação de monitoramento institucional. Os resultados de benchmark confirmam a estabilidade e a eficiência da arquitetura atual.

**Status Final:** **BENCHMARK HOMOLOGADO.**

*Relatório de benchmark emitido em 14 de julho de 2026. Nenhuma alteração foi realizada no código-fonte.*
