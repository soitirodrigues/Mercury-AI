# 🔍 Mercury AI V1 — Relatório de Auditoria de Integridade Forense

**Data:** 2026-08-01T15:23:49.800976
**Projeto:** Mercury AI V1
**Veredito do Release Gate:** **NO_GO**

> 2 falha(s) crítica(s) encontrada(s). Correção obrigatória antes do release.

---

## 📊 Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Achados | 112 |
| ✅ PASS | 62 |
| ❌ FAIL | 2 |
| ⚠️ WARNING | 31 |
| 🔴 CRÍTICOS | 2 |

---

## 1. Static Audit (AST)

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| STATIC-001 | LOW | ℹ️ INFO | Total de arquivos Python analisados: 261 |
| STATIC-002 | LOW | ✅ PASS | Nenhum erro de sintaxe encontrado |
| STATIC-003 | MEDIUM | ⚠️ WARNING | 19 função(ões) stub (não implementadas) |
| STATIC-004 | LOW | ✅ PASS | Nenhum bare except encontrado |
| STATIC-005 | MEDIUM | ⚠️ WARNING | 7 função(ões) muito longas (>200 linhas) |

#### STATIC-003: 19 função(ões) stub (não implementadas)

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** Vários

**Descrição:** Funções que levantam NotImplementedError ou têm corpo vazio:
  mercury_ai\data\market_data_provider.py:5 -> get_data()
  mercury_ai\data\mercury_data_provider.py:48 -> connect()
  mercury_ai\data\mercury_data_provider.py:49 -> health()
  mercury_ai\data\mercury_data_provider.py:50 -> get_history()
  mercury_ai\data\mercury_data_provider.py:51 -> get_last_price()
  mercury_ai\data\mercury_data_provider.py:52 -> get_candles()
  mercury_ai\data\mercury_data_provider.py:53 -> market_status()
  mercury_ai\providers\base_provider.py:5 -> get_data()
  mercury_ai\providers\base_provider.py:8 -> is_available()
  mercury_ai\providers\base_provider.py:11 -> supports_symbol()
  mercury_ai\providers\base_provider.py:14 -> supports_market()
  mercury_ai\providers\base_provider.py:17 -> supports_timeframe()
  mercury_ai\providers\base_provider.py:20 -> max_history()
  mercury_ai\providers\base_provider.py:23 -> source_name()
  mercury_ai\providers\data_interfaces.py:12 -> get_data()
  mercury_ai\providers\data_interfaces.py:14 -> check_health()
  mercury_ai\providers\future_broker_provider.py:2 -> get_data()
  mercury_ai\providers\future_polygon_provider.py:2 -> get_data()
  mercury_ai\providers\future_tradingview_provider.py:2 -> get_data()

**Recomendação:** Implementar ou remover funções stub antes do release.

#### STATIC-005: 7 função(ões) muito longas (>200 linhas)

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** 

**Descrição:** Funções com mais de 200 linhas:
  mercury_ai\analysis\market_structure_intelligence_engine.py:17 evaluate() — 204 linhas
  mercury_ai\analysis\swing_engine.py:65 detect_swings() — 215 linhas
  mercury_ai\analysis\volatility_engine.py:20 analyze() — 222 linhas
  mercury_ai\analysis\volume_intelligence_engine.py:15 evaluate() — 218 linhas
  mercury_ai\brain\mercury_decision_engine.py:113 _analyze_logic() — 287 linhas
  mercury_ai\brain\probability_engine.py:34 analyze() — 212 linhas
  mercury_ai\core\analysis_pipeline.py:159 analyze() — 267 linhas

**Recomendação:** Refatorar funções longas em unidades menores.

---

## 2. Contract Audit

**Status da Seção:** PASS

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| CONTRACT-RiskAssessment-001 | LOW | ✅ PASS | RiskAssessment está corretamente frozen=True |
| CONTRACT-RiskAssessment-002 | LOW | ✅ PASS | RiskAssessment: todos os campos obrigatórios presentes |
| CONTRACT-MarketData-001 | LOW | ✅ PASS | MarketData está corretamente frozen=True |
| CONTRACT-MarketData-002 | LOW | ✅ PASS | MarketData: todos os campos obrigatórios presentes |
| CONTRACT-MarketContext-001 | LOW | ✅ PASS | MarketContext está corretamente frozen=True |
| CONTRACT-MarketContext-002 | LOW | ✅ PASS | MarketContext: todos os campos obrigatórios presentes |
| CONTRACT-MarketEvidenceBundle-001 | LOW | ✅ PASS | MarketEvidenceBundle está corretamente frozen=True |
| CONTRACT-MarketEvidenceBundle-002 | LOW | ✅ PASS | MarketEvidenceBundle: todos os campos obrigatórios presentes |
| CONTRACT-SUMMARY | LOW | ℹ️ INFO | Total de dataclasses encontrados: 65 |

---

## 3. Dependency Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| DEP-001 | LOW | ✅ PASS | requirements.txt com 12 dependências declaradas |
| DEP-002 | LOW | ✅ PASS | Todas as dependências declaradas estão instaladas |
| DEP-003 | MEDIUM | ⚠️ WARNING | 3 import(s) de terceiros não declarados em requirements.txt |
| DEP-004 | LOW | ✅ PASS | Nenhuma dependência circular detectada |

#### DEP-003: 3 import(s) de terceiros não declarados em requirements.txt

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** 

**Descrição:** Pacotes importados mas não listados: __future__, gc, tracemalloc

**Recomendação:** Adicionar pacotes ao requirements.txt ou verificar se são necessários.

---

## 4. Masking Audit

**Status da Seção:** PASS

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| MASK-001 | LOW | ✅ PASS | Nenhum Mock/MagicMock em código de produção |
| MASK-002 | LOW | ✅ PASS | Nenhum bare except em produção |

---

## 5. Runtime Audit

**Status da Seção:** PASS

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| RUNTIME-001 | LOW | ℹ️ INFO | main.py executado 3 vezes |
| RUNTIME-002 | LOW | ✅ PASS | Nenhum crash detectado |
| RUNTIME-003 | LOW | ℹ️ INFO | Tempo médio de execução: 2.93s (max: 5.46s) |
| RUNTIME-004 | LOW | ✅ PASS | Saída consistente entre execuções |

---

## 6. Flow & Pipeline Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| FLOW-AnalysisPipeline-METHODS | HIGH | ⚠️ WARNING | AnalysisPipeline: métodos esperados ausentes |
| FLOW-HistoricalReplayEngine-METHODS | HIGH | ⚠️ WARNING | HistoricalReplayEngine: métodos esperados ausentes |
| FLOW-RiskEngine | LOW | ✅ PASS | RiskEngine encontrado com todos os métodos |
| FLOW-InstitutionalMemoryEngine | LOW | ✅ PASS | InstitutionalMemoryEngine encontrado com todos os métodos |
| FLOW-MercuryDecisionEngine-METHODS | HIGH | ⚠️ WARNING | MercuryDecisionEngine: métodos esperados ausentes |
| FLOW-PerformanceEngine-METHODS | HIGH | ⚠️ WARNING | PerformanceEngine: métodos esperados ausentes |
| FLOW-PipelineExecutor-METHODS | HIGH | ⚠️ WARNING | PipelineExecutor: métodos esperados ausentes |
| FLOW-ReplayBatchProcessor-METHODS | HIGH | ⚠️ WARNING | ReplayBatchProcessor: métodos esperados ausentes |
| FLOW-SUMMARY | LOW | ℹ️ INFO | Componentes: 8/8 encontrados, 0 ausentes, 6 com métodos faltando |

#### FLOW-AnalysisPipeline-METHODS: AnalysisPipeline: métodos esperados ausentes

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** mercury_ai\core\analysis_pipeline.py:57

**Descrição:** Encontrados: [], Ausentes: ['run', 'execute', 'process']

**Recomendação:** Implementar métodos: run, execute, process

#### FLOW-HistoricalReplayEngine-METHODS: HistoricalReplayEngine: métodos esperados ausentes

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** mercury_ai\analysis\historical_replay_engine.py:27

**Descrição:** Encontrados: ['run_replay'], Ausentes: ['replay', 'process']

**Recomendação:** Implementar métodos: replay, process

#### FLOW-MercuryDecisionEngine-METHODS: MercuryDecisionEngine: métodos esperados ausentes

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** mercury_ai\brain\mercury_decision_engine.py:38

**Descrição:** Encontrados: [], Ausentes: ['decide', 'evaluate']

**Recomendação:** Implementar métodos: decide, evaluate

#### FLOW-PerformanceEngine-METHODS: PerformanceEngine: métodos esperados ausentes

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** mercury_ai\analysis\performance_engine.py:7

**Descrição:** Encontrados: [], Ausentes: ['calculate', 'evaluate']

**Recomendação:** Implementar métodos: calculate, evaluate

#### FLOW-PipelineExecutor-METHODS: PipelineExecutor: métodos esperados ausentes

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** mercury_ai\core\pipeline_executor.py:7

**Descrição:** Encontrados: ['execute'], Ausentes: ['run']

**Recomendação:** Implementar métodos: run

#### FLOW-ReplayBatchProcessor-METHODS: ReplayBatchProcessor: métodos esperados ausentes

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** mercury_ai\analysis\replay_batch_processor.py:58

**Descrição:** Encontrados: [], Ausentes: ['process_batch', 'run']

**Recomendação:** Implementar métodos: process_batch, run

---

## 7. Test Audit

**Status da Seção:** PASS

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| TEST-001 | LOW | ✅ PASS | Todos os 100 testes passaram! |
| TEST-003 | LOW | ℹ️ INFO | Tempo total de execução: 1884.3s |
| TEST-004 | LOW | ℹ️ INFO | Cobertura de código não disponível |

---

## 8. Decision Integrity Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| DEC-001 | LOW | ℹ️ INFO | Total de pontos de decisão: 8 |
| DEC-002 | LOW | ✅ PASS | Nenhuma chamada a random() detectada |
| DEC-003 | MEDIUM | ⚠️ WARNING | Nenhum guard contra NaN/Inf detectado |
| DEC-004 | LOW | ✅ PASS | Validação de decisão detectada |

#### DEC-003: Nenhum guard contra NaN/Inf detectado

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** 

**Descrição:** Decisões podem produzir valores inválidos sem detecção.

**Recomendação:** Adicionar verificações math.isfinite() em cálculos críticos.

---

## 9. Coverage Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| COV-001 | HIGH | ⚠️ WARNING | Falha ao obter dados de cobertura |
| COV-004 | LOW | ✅ PASS | Todos os módulos têm testes associados |

#### COV-001: Falha ao obter dados de cobertura

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** 

**Descrição:** Erro: timeout. Cobertura não pôde ser medida.

**Recomendação:** Verificar se pytest-cov está instalado e configurado.

---

## 10. Integrity Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| INT-CFG-CONFIG.JSON | LOW | ✅ PASS | Configuração válida: config.json |
| INT-CFG-MODELS.JSON | LOW | ✅ PASS | Configuração válida: models.json |
| INT-RUNTIME-002 | LOW | ✅ PASS | Todos os relatórios de runtime têm JSON válido |
| INT-RUNTIME-004 | MEDIUM | ⚠️ WARNING | 100 relatórios com schema incompleto |
| INT-DOTMERCURY-001 | LOW | ✅ PASS | Todos os artefatos do Project Mapper presentes |
| INT-DOTMERCURY-DEPENDENCY_GRAPH.JSON | LOW | ✅ PASS | Artefato válido: dependency_graph.json |
| INT-DOTMERCURY-CALL_GRAPH.JSON | LOW | ✅ PASS | Artefato válido: call_graph.json |
| INT-DOTMERCURY-MERCURY_SNAPSHOT.JSON | LOW | ✅ PASS | Artefato válido: mercury_snapshot.json |
| INT-MODELS-001 | LOW | ✅ PASS | models.json válido com 3 modelos |
| INT-MODELS-003 | MEDIUM | ⚠️ WARNING | 3 modelos com campos incompletos |
| INT-CHECKSUM-CONFIG.JSON | LOW | ℹ️ INFO | Checksum config.json: 01d7bf5715e0aea3 |
| INT-CHECKSUM-MAIN.PY | LOW | ℹ️ INFO | Checksum main.py: 05da59aa6901eb26 |
| INT-CHECKSUM-REQUIREMENTS.TXT | LOW | ℹ️ INFO | Checksum requirements.txt: 847cd75afa2c1743 |

#### INT-RUNTIME-004: 100 relatórios com schema incompleto

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** 

**Descrição:** Chaves esperadas: {'timestamp', 'indicators', 'metadata', 'price', 'symbol', 'decision'}. Alguns relatórios faltam campos obrigatórios.

#### INT-MODELS-003: 3 modelos com campos incompletos

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** 

**Descrição:** Campos esperados: {'type', 'version', 'params'}

---

## 11. Explainability Audit

**Status da Seção:** PASS

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| EXP-001 | LOW | ✅ PASS | Feature Importance / SHAP Implementation Found |
| EXP-002 | LOW | ✅ PASS | Decision Logging with Explanations Found |
| EXP-003 | LOW | ✅ PASS | Model Documentation Found |
| EXP-004 | LOW | ℹ️ INFO | Counterfactual Explanations Not Implemented |

---

## 12. Data Audit

**Status da Seção:** FAIL

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| DATA-001 | LOW | ✅ PASS | Data Schema Validation Found |
| DATA-002 | MEDIUM | ⚠️ WARNING | Data Lineage / Versioning Missing |
| DATA-003 | LOW | ✅ PASS | Missing Data Handling Found |
| DATA-004 | LOW | ✅ PASS | Data Drift Detection Found |
| DATA-005 | LOW | ✅ PASS | Train/Test Leakage Prevention Found |
| DATA-006 | CRITICAL | ❌ FAIL | Potential Secrets in Code/Config |

#### DATA-002: Data Lineage / Versioning Missing

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI

**Descrição:** Não há rastreabilidade de lineage dos dados (origem, transformações, versionamento).

**Recomendação:** Implementar data lineage tracking e considerar DVC para versionamento de datasets.

#### DATA-006: Potential Secrets in Code/Config

- **Severidade:** CRITICAL
- **Status:** FAIL
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Possíveis secrets (password, api_key, token) encontrados em arquivos de config/log.

**Recomendação:** Mover secrets para variáveis de ambiente ou vault. Nunca commitar secrets.

---

## 13. Universe Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| UNIV-001 | LOW | ✅ PASS | Universe Definition Found |
| UNIV-002 | LOW | ✅ PASS | Data Coverage Check Found |
| UNIV-003 | LOW | ✅ PASS | Liquidity/Volume Filters Found |
| UNIV-004 | MEDIUM | ⚠️ WARNING | Sector Diversification Not Enforced |
| UNIV-005 | LOW | ✅ PASS | Corporate Actions Handling Found |
| UNIV-006 | MEDIUM | ⚠️ WARNING | Universe Rebalancing Not Defined |

#### UNIV-004: Sector Diversification Not Enforced

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Não há controle de concentração setorial/industrial no universo ou portfolio.

**Recomendação:** Implementar limites de concentração setorial (ex: max 20% por setor, max 10% por indústria).

#### UNIV-006: Universe Rebalancing Not Defined

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Não há processo definido de rebalanceamento/atualização periódica do universo (frequência, critérios, automação).

**Recomendação:** Definir política de rebalanceamento: frequência (mensal/trimestral), critérios de entrada/saída, automação.

---

## 14. Global State Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| GST-001 | MEDIUM | ⚠️ WARNING | Potential Mutable Global Variables: 4593 |
| GST-002 | MEDIUM | ⚠️ WARNING | Singleton Patterns Found: 1 |
| GST-003 | LOW | ✅ PASS | Global Configuration Found |
| GST-003b | LOW | ✅ PASS | config.json Valid JSON |
| GST-004 | LOW | ✅ PASS | Runtime State Management Found |
| GST-005 | LOW | ✅ PASS | Thread Safety Mechanisms Found |
| GST-006 | LOW | ✅ PASS | State Persistence/Recovery Found |

#### GST-001: Potential Mutable Global Variables: 4593

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Variáveis globais potencialmente mutáveis encontradas: [('mercury_ai\\main.py', 6, 'scanner'), ('mercury_ai\\main.py', 11, 'if __name__'), ('mercury_ai\\ai\\llm.py', 8, 'self.client'), ('mercury_ai\\ai\\llm.py', 9, 'api_key'), ('mercury_ai\\ai\\llm.py', 10, 'base_url')]

**Recomendação:** Evitar variáveis globais mutáveis. Usar dependency injection, context managers, ou classes de estado.

#### GST-002: Singleton Patterns Found: 1

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Padrões Singleton detectados em: mercury_ai\analysis\institutional_memory_engine.py

**Recomendação:** Avaliar se singletons são necessários. Preferir dependency injection para testabilidade.

---

## 15. Determinism Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| DET-001 | LOW | ✅ PASS | Fixed Seeds Found: 2 |
| DET-003 | HIGH | ⚠️ WARNING | Time-Based Operations: 26 |
| DET-004 | MEDIUM | ⚠️ WARNING | UUID Generation: 2 |
| DET-005 | HIGH | ⚠️ WARNING | Concurrency Operations: 8 |
| DET-006 | LOW | ℹ️ INFO | Dict Iteration Order: 2 |
| DET-007 | MEDIUM | ⚠️ WARNING | Floating Point Comparisons: 14 |
| DET-008 | MEDIUM | ⚠️ WARNING | External Dependencies: 23 files |
| DET-009 | LOW | ✅ PASS | Deterministic Replay Capability Found |
| DET-010 | MEDIUM | ⚠️ WARNING | Dependencies Not Fully Pinned |
| DET-011 | LOW | ℹ️ INFO | No Containerization |

#### DET-003: Time-Based Operations: 26

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Operações baseadas em tempo (não-determinísticas): [('mercury_ai\\analysis\\benchmark_framework.py', 139, 'start_time = time.perf_counter()'), ('mercury_ai\\analysis\\benchmark_framework.py', 143, 'end_time = time.perf_counter()'), ('mercury_ai\\analysis\\benchmark_framework.py', 347, 'wall_start = time.perf_counter()')]

**Recomendação:** Injetar tempo como dependência (time_provider) para testes determinísticos. Usar freezegun em testes.

#### DET-004: UUID Generation: 2

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Geração de UUID aleatórios: [('mercury_ai\\core\\analysis_pipeline.py', 75, 'self.session_id = str(uuid.uuid4())'), ('mercury_ai\\core\\session_manager.py', 10, 'self.session_id = str(uuid.uuid4())')]

**Recomendação:** Para testes: usar uuid determinístico (uuid5 com namespace fixo) ou mock.

#### DET-005: Concurrency Operations: 8

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Operações de concorrência (ordem não-determinística): [('mercury_ai\\analysis\\institutional_memory_engine.py', 12, '_lock = threading.Lock()'), ('mercury_ai\\analysis\\replay_cache.py', 32, 'self._lock = threading.Lock()'), ('mercury_ai\\analysis\\tests\\test_replay_cache.py', 203, 'threading.Thread(target=reader),')]

**Recomendação:** Evitar concorrência em lógica crítica. Se necessário, usar locks determinísticos ou single-threaded para replay.

#### DET-007: Floating Point Comparisons: 14

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Possíveis comparações de ponto flutuante: [('mercury_ai\\analysis\\performance_engine.py', 132, "if len(downside_returns) == 0: return float('inf')"), ('mercury_ai\\analysis\\smart_money\\tests\\test_liquidity_engine.py', 44, 'assert groups[0].prices == [100.0, 100.2]'), ('mercury_ai\\analysis\\smart_money\\tests\\test_liquidity_engine.py', 55, 'assert groups[0].prices == [100.0, 100.1]')]

**Recomendação:** Usar math.isclose() ou decimal.Decimal para comparações financeiras. Evitar == com floats.

#### DET-008: External Dependencies: 23 files

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Dependências externas (API, DB, FS, network) em: mercury_ai\analysis\health_auditor.py, mercury_ai\analysis\data_exporter.py, mercury_ai\analysis\health_checker.py, mercury_ai\analysis\calibration_analyzer.py, mercury_ai\analysis\institutional_analytics_engine.py

**Recomendação:** Isolar dependências externas atrás de interfaces. Usar mocks/fakes para testes determinísticos. Implementar replay de dados externos.

#### DET-010: Dependencies Not Fully Pinned

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\requirements.txt

**Descrição:** requirements.txt não tem versões pinadas consistentemente. Risco de drift de dependências.

**Recomendação:** Pin todas as dependências com == em requirements.txt ou usar pip-tools/poetry lockfile.

---

## 16. Performance Audit

**Status da Seção:** WARNING

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| PERF-001 | MEDIUM | ⚠️ WARNING | Nested Loops Detected: 157 |
| PERF-002 | LOW | ℹ️ INFO | Nested List Comprehensions: 3 |
| PERF-003 | MEDIUM | ⚠️ WARNING | Recursive Functions: 49 |
| PERF-004 | LOW | ℹ️ INFO | Large Object Creation: 33 |
| PERF-005 | MEDIUM | ⚠️ WARNING | Potential Global Accumulators: 887 |
| PERF-006 | HIGH | ⚠️ WARNING | Potentially Unclosed Resources: 9 |
| PERF-007 | MEDIUM | ⚠️ WARNING | Sync I/O Without Async Alternative: 22 files |
| PERF-008 | LOW | ✅ PASS | Batching/Streaming Patterns Found |
| PERF-011 | LOW | ✅ PASS | Caching Strategy Found |
| PERF-012 | LOW | ✅ PASS | Profiling/Benchmarking Found |
| PERF-013 | LOW | ℹ️ INFO | Critical Latency Paths Identified: 4 |
| PERF-014 | LOW | ✅ PASS | Resource Monitoring Found |

#### PERF-001: Nested Loops Detected: 157

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Loops aninhados (potencial O(n²+)): [('mercury_ai\\analysis\\benchmark_framework.py', 312, 'for _ in range(min(self.bootstrap_samples, 10000)):', 2), ('mercury_ai\\analysis\\benchmark_framework.py', 358, 'for future in as_completed(futures):', 3), ('mercury_ai\\analysis\\benchmark_framework.py', 384, 'for outcome in filtered_outcomes:', 2)]

**Recomendação:** Revisar complexidade. Considerar: vectorização (numpy/pandas), sets/dicts para lookup O(1), algoritmos mais eficientes.

#### PERF-003: Recursive Functions: 49

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Funções recursivas detectadas: [('mercury_ai\\main.py', 4, 'main'), ('mercury_ai\\analysis\\benchmark_framework.py', 302, 'norm_sf'), ('mercury_ai\\analysis\\data_exporter.py', 20, '_export_to_formats')]. Risco de stack overflow e overhead.

**Recomendação:** Converter para iterativo se possível. Usar @lru_cache para memoização se recursão necessária.

#### PERF-005: Potential Global Accumulators: 887

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Possíveis acumuladores globais (memory leak risk): [('mercury_ai\\ai\\llm.py', 19, 'messages=['), ('mercury_ai\\analysis\\adaptive_weight_engine.py', 33, 'weights["Trend"] = min(weights["Trend"] * 1.5, 2.0)'), ('mercury_ai\\analysis\\adaptive_weight_engine.py', 34, 'weights["Structure"] = min(weights["Structure"] * 1.2, 1.8)')]

**Recomendação:** Evitar listas/dicts globais que crescem indefinidamente. Usar bounded collections, rotating buffers, ou persistência periódica.

#### PERF-006: Potentially Unclosed Resources: 9

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Recursos que podem não ser fechados (file handles, DB connections): [('mercury_ai\\analysis\\session_engine.py', 15, 'session = self._detect_session(hour, evidences)'), ('mercury_ai\\analysis\\session_engine.py', 29, 'def _detect_session(self, hour: int, evidences: List[str]) -> str:'), ('mercury_ai\\data\\mercury_data_provider.py', 48, 'def connect(self) -> bool: ...')]

**Recomendação:** Usar context managers (with statement) para files, connections, sessions. Implementar __enter__/__exit__ ou usar try/finally.

#### PERF-007: Sync I/O Without Async Alternative: 22 files

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** I/O síncrono detectado sem uso de async: mercury_ai\analysis\data_exporter.py, mercury_ai\database\replay_storage.py, mercury_ai\analysis\tests\test_replay_cache.py, mercury_ai\data\replay_data_provider.py, mercury_ai\core\export_center.py

**Recomendação:** Considerar async/await para I/O bound operations (HTTP, DB, FS). Usar aiohttp, asyncpg, aiofiles. Batching para reduzir round-trips.

---

## 17. Backtest Audit

**Status da Seção:** FAIL

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| BACK-001 | CRITICAL | ❌ FAIL | Potential Look-Ahead Bias: 14 |
| BACK-002 | MEDIUM | ⚠️ WARNING | Shift Usage in Features: 5 |
| BACK-003 | HIGH | ⚠️ WARNING | Suspicious Leakage Patterns: 26 |
| BACK-004 | LOW | ✅ PASS | Delisted Handling Found |
| BACK-006 | LOW | ✅ PASS | Comprehensive Transaction Costs: 3/4 components |
| BACK-009 | LOW | ✅ PASS | Out-of-Sample Validation Found |
| BACK-010 | LOW | ✅ PASS | Walk-Forward Analysis Found |
| BACK-011 | LOW | ✅ PASS | Monte Carlo / Bootstrap Validation Found |
| BACK-012 | LOW | ✅ PASS | Realistic Execution Simulation: 4/5 |
| BACK-013 | LOW | ✅ PASS | Comprehensive Risk Management: 4/5 |
| BACK-014 | LOW | ✅ PASS | Robust Performance Metrics: 6/6 + Statistical Significance |

#### BACK-001: Potential Look-Ahead Bias: 14

- **Severidade:** CRITICAL
- **Status:** FAIL
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Acesso a dados futuros detectado: [('mercury_ai\\analysis\\benchmark_framework.py', 185, 'close_next = float(df.iloc[-1]["Close"])'), ('mercury_ai\\analysis\\historical_replay_engine.py', 143, 'avg_volume=avg_volume.iloc[:i+1],'), ('mercury_ai\\analysis\\historical_replay_engine.py', 144, 'avg_body=avg_body.iloc[:i+1],')]

**Recomendação:** CRÍTICO: Verificar se features usam apenas dados disponíveis no momento da decisão. Usar shift(1+) para features lagged. Nunca usar shift(-n) ou iloc futuro em features de entrada.

#### BACK-002: Shift Usage in Features: 5

- **Severidade:** MEDIUM
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Uso de shift() em features: [('mercury_ai\\analysis\\support_resistance_analyzer.py', 61, "highs = df[(df['High'] > df['High'].shift(SWING_WINDOW)) & (df['High'] > df['Hig"), ('mercury_ai\\analysis\\support_resistance_analyzer.py', 62, "lows = df[(df['Low'] < df['Low'].shift(SWING_WINDOW)) & (df['Low'] < df['Low'].s"), ('mercury_ai\\analysis\\swing_engine.py', 41, 'prev_close = close.shift(1)')]. Verificar se shift > 0 (lag) e não shift < 0 (lead).

**Recomendação:** Auditar cada uso de shift(). Features devem usar shift(1+) apenas. Target/label pode usar shift(-1) mas NUNCA features de entrada.

#### BACK-003: Suspicious Leakage Patterns: 26

- **Severidade:** HIGH
- **Status:** WARNING
- **Localização:** C:\Projetos\Mercury-AI\mercury_ai

**Descrição:** Patterns suspeitos: [('mercury_ai\\analysis\\benchmark_framework.py', 22, 'from concurrent.futures import ThreadPoolExecutor, as_completed'), ('mercury_ai\\analysis\\benchmark_framework.py', 357, 'futures = {executor.submit(self._run_single_symbol, sym): sym for sym in symbols'), ('mercury_ai\\analysis\\benchmark_framework.py', 358, 'for future in as_completed(futures):')]

**Recomendação:** Revisar cada ocorrência. ffill/bfill pode causar leakage se aplicado antes de split train/test. Forward fill apenas em dados históricos já conhecidos.

---

## 18. Final Report Generation

**Status da Seção:** PASS

| ID | Severidade | Status | Título |
|----|-----------|--------|--------|
| RPT-001 | INFO | ✅ PASS | Report Generation Complete |

---

## 🏁 Veredito Final: NO_GO

2 falha(s) crítica(s) encontrada(s). Correção obrigatória antes do release.
