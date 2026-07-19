# Roadmap Técnico - Mercury AI V2

Este documento estabelece a visão arquitetural e o planejamento estratégico para a evolução da plataforma Mercury AI.

---

## 1. Objetivos
- **Escalabilidade:** Migração de processamento síncrono para assíncrono (asyncio).
- **Desacoplamento:** Separação total entre camadas de dados, engines e interface.
- **Performance:** Otimização do pipeline de análise para suportar múltiplos ativos simultâneos.
- **Inteligência:** Implementação de aprendizado de máquina adaptativo para calibração de modelos.

## 2. Arquitetura Proposta
- **Message Bus:** Introdução de um barramento de mensagens (ex: Redis/RabbitMQ) para comunicação entre engines.
- **Service-Oriented:** Engines transformadas em microsserviços independentes.
- **Data Layer:** Migração de armazenamento baseado em arquivos para um banco de dados relacional (TimescaleDB) para séries temporais.

## 3. Prioridades
1. **Infraestrutura Assíncrona:** A base necessária para escalar.
2. **Camada de Dados Institucional:** Migração para banco de dados robusto.
3. **Engines Adaptativas:** Inteligência baseada em feedback de performance.
4. **Dashboard 2.0:** UI/UX focada em alta performance e baixa latência.

## 4. Módulos V2
- `mercury_ai.core.async_engine`: Executor principal assíncrono.
- `mercury_ai.data.store`: Abstração de persistência de dados.
- `mercury_ai.ml.adaptive_tuner`: Módulo de calibração automática de estratégias.
- `mercury_ai.api`: API REST/WebSocket para integrações externas.

## 5. Backlog e Milestones

| Milestone | Descrição | Prioridade |
| :--- | :--- | :--- |
| M1: Foundation | Migração para estrutura async e barramento. | P0 |
| M2: Data Layer | Implementação de banco de dados para séries temporais. | P0 |
| M3: Adaptive Engine | Engines de estratégia aprendendo com o histórico. | P1 |
| M4: API/Integration | Abertura de APIs para consumo externo. | P2 |

## 6. Riscos
- **Complexidade de Migração:** O custo de transição da arquitetura V1 para V2 é alto.
- **Estabilidade:** A introdução de assincronia pode introduzir *race conditions* se não bem projetada.

## 7. Cronograma Proposto
- **Meses 1-2:** Planejamento detalhado e prova de conceito da infraestrutura async.
- **Meses 3-5:** Migração da camada de dados e estruturação dos microsserviços.
- **Meses 6-8:** Implementação das engines adaptativas.
- **Meses 9+:** Testes de carga, stress e lançamento da V2 Beta.

---
*Documento de planejamento emitido. Nenhuma alteração foi realizada na V1.*
