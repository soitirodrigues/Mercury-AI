# 📐 AUDITORIA DE ARQUITETURA — Mercury-AI

> **Data:** 2025-01-20  
> **Auditor:** GitHub Copilot (glm-5.2)  
> **Escopo:** Análise estrutural, padrões de design, fluxo de execução e modularidade  
> **Código-base:** `mercury_ai/` (Python 3.x)

---

## 1. Visão Geral da Arquitetura

O Mercury-AI é um sistema institucional de análise e decisão de trading construído em Python, com arquitetura orientada a **pipelines determinísticos** e **motores de análise especializados** (engine pattern).

### 1.1 Camadas Principais

| Camada | Diretório | Responsabilidade |
|--------|-----------|------------------|
| **Core** | `mercury_ai/core/` | Infraestrutura: pipeline executor, profiler, auditoria, segurança, sessão, saúde, exportação |
| **Analysis** | `mercury_ai/analysis/` | ~30+ motores de análise técnica (trend, liquidity, smart money, FVG, order blocks, etc.) |
| **Brain** | `mercury_ai/brain/` | Orquestrador de decisão (`MercuryDecisionEngine`) e motor de probabilidade |
| **Providers** | `mercury_ai/providers/` | Fontes de dados de mercado (Yahoo Finance, etc.) |
| **Data** | `mercury_ai/data/` | Serviços de dados, indicadores, qualidade de dados |
| **Models** | `mercury_ai/models/` | Dataclasses imutáveis (frozen) para transferência de dados |
| **Utils** | `mercury_ai/utils/` | Utilitários (DeterministicClock, etc.) |
| **Database** | `mercury_ai/database/` | Persistência de snapshots de decisão |
| **App** | `mercury_ai/app/` | Interface Streamlit (terminal/dashboard) |
| **Tools** | `mercury_ai/tools/` | Ferramentas auxiliares |
| **Config** | `mercury_ai/config/` | Pesos institucionais, timeframes, configurações |

### 1.2 Padrão de Design Central

```
                    ┌─────────────────────┐
                    │   AnalysisPipeline  │  (Orquestrador principal)
                    │   25+ estágios      │
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐ ┌───────────┐ ┌──────────────────┐
     │ 30+ Engines  │ │ Context   │ │ MercuryDecision   │
     │ (BaseEngine) │ │ Engine   │ │ Engine (Brain)    │
     └──────────────┘ └───────────┘ └────────┬─────────┘
                                             │
                                    ┌────────┼────────┐
                                    ▼        ▼        ▼
                              Validation  Quality  Confluence
                              Conflict    Ranking  Probability
                              Confidence  Memory   Narrative
                              Resolver   Score    Builder
```

---

## 2. Pipeline de Análise (25+ Estágios)

O `AnalysisPipeline.analyze()` executa um pipeline sequencial com 25+ estágios:

### 2.1 Fluxo de Execução

1. **Aquisição de Dados** — `MarketDataService` obtém dados via providers
2. **Indicadores** — `IndicatorEngine` calcula indicadores técnicos
3. **Qualidade de Dados** — `DataQualityEngine` avalia integridade
4. **Contexto** — `ContextEngine` constrói `MarketContext`
5. **Motores de Análise** (paralelo conceitual, sequencial na execução):
   - `TrendAnalyzer` — Análise de tendência
   - `MTFEngine` — Multi-timeframe
   - `SupportResistanceAnalyzer` — Suporte/resistência
   - `PriceActionAnalyzer` — Price action
   - `LiquidityEngine` — Liquidez (Smart Money)
   - `SmartMoneyEngine` — Smart money concepts
   - `FairValueGapEngine` — FVG
   - `OrderBlockEngine` — Order blocks
   - `MarketRegimeEngine` — Regime de mercado
   - `SessionEngine` — Sessão de trading
   - `MarketStateEngine` — Estado do mercado
   - `VolumeIntelligenceEngine` — Volume
   - `VolatilityEngine` — Volatilidade
   - `MarketConditionEngine` — Condições de mercado
   - `CandlestickEngine` — Padrões de candle
   - `MarketStructureIntelligenceEngine` — Estrutura
6. **Trade Filter** — `InstitutionalTradeFilterEngine` filtra trades
7. **Decisão** — `MercuryDecisionEngine.analyze()` executa 13 estágios
8. **Snapshot** — `DecisionSnapshotLogger.save()` persiste resultado
9. **Telemetria** — `RuntimeReport` exportado como JSON

### 2.2 Contract Validation

O `PipelineExecutor.execute()` envolve cada chamada com:
- **Profiling** automático via `PipelineProfiler`
- **Validação de tipo** do retorno (contrato)
- `PipelineContractError` em caso de violação de tipo
- Histórico de execuções com status (success/failed)

```python
def execute(self, stage_name, func, expected_type, *args, **kwargs):
    # profiling start
    result = func(*args, **kwargs)
    # profiling end
    if not isinstance(result, expected_type):
        raise PipelineContractError(...)
    return result
```

---

## 3. Motor de Decisão (13 Estágios)

O `MercuryDecisionEngine._analyze_logic()` implementa:

| # | Estágio | Engine | Output |
|---|---------|--------|--------|
| 1 | VALIDATION | `ValidationEngine` | `is_valid`, warnings |
| 2 | QUALITY | `EvidenceQualityEngine` | `quality_score` médio |
| 3 | CONFLICT | `ConflictResolutionEngine` | `resolved_evidences`, `conflict_score` |
| 4 | RANKING | `EvidenceRankingEngine` | Evidências ranqueadas |
| 5 | MEMORY | `InstitutionalMemoryEngine` | `consistency_score` |
| 6 | BUNDLE | `MarketEvidenceBundle` | Bundle reconstruído |
| 7 | CONFIDENCE | `ConfidenceEngine` | `ConfidenceResult` calibrado |
| 8 | CONFLUENCE | `ConfluenceEngine` | Scores BUY/SELL/NEUTRAL |
| 9 | PROBABILITY | `ProbabilityEngine` | Probabilidades normalizadas |
| 10 | RESOLVER | `DecisionResolverEngine` | Decisão final |
| 11 | NARRATIVE | `NarrativeEngine` | Narrativa explicativa |
| 12 | SCORE | `InstitutionalScoreEngine` | Score institucional |
| 13 | BUILDER | `DecisionResultBuilder` | `DecisionResult` |

### 3.1 Injeção de Dependência (DI)

```python
# ConfluenceEngine recebe MarketThesisBuilder via construtor (SRP)
self.confluence = ConfluenceEngine(
    thesis_builder=MarketThesisBuilder(
        risk_engine=RiskEngine(),
        confidence_engine=self.confidence,
        state_engine=MarketStateEngine(),
        score_engine=ConfluenceScoreEngine(),
    ),
)
```

### 3.2 Pesos Institucionais Canônicos

```python
self.probability_engine = ProbabilityEngine(
    weights={
        "trend": INSTITUTIONAL_WEIGHTS_NORMALIZED["trend"],
        "structure": INSTITUTIONAL_WEIGHTS_NORMALIZED["market_structure"],
        "liquidity": INSTITUTIONAL_WEIGHTS_NORMALIZED["liquidity"],
        "volatility": INSTITUTIONAL_WEIGHTS_NORMALIZED["volatility"],
    },
)
```

---

## 4. Padrão Engine (ABC + Frozen Dataclass)

### 4.1 BaseEngine

```python
class BaseEngine(ABC):
    @abstractmethod
    def analyze(self, ...) -> EngineResult:
        ...
```

### 4.2 EngineResult (Frozen Dataclass)

```python
@dataclass(frozen=True)
class EngineResult:
    score: float
    confidence: float
    evidences: tuple
    warnings: tuple
    execution_time: float
```

**Benefícios:**
- Imutabilidade garante integridade dos resultados
- `frozen=True` previne mutação acidental
- `tuple` em vez de `list` para campos mutáveis (compatível com frozen)

---

## 5. Determinismo

### 5.1 DeterministicClock

```python
class DeterministicClock:
    _current_time: Optional[datetime] = None

    @classmethod
    def set_time(cls, time: datetime):
        cls._current_time = time

    @classmethod
    def utcnow(cls) -> datetime:
        return cls._current_time or datetime.utcnow()
```

**Impacto:**
- Todos os timestamps usam `DeterministicClock.utcnow()` em vez de `datetime.now()`
- Permite replay determinístico com timestamps reproduzíveis
- Estado de classe (class-level) — singleton implícito

### 5.2 Two-Pass Context Build

Para resolver dependência circular entre `RiskEngine` e `ContextBuilder`:

1. **Pass 1:** Constrói contexto com risk placeholder
2. **Pass 2:** RiskEngine calcula risk real
3. **Rebuild:** Contexto reconstruído com risk real

---

## 6. Execução em Background

### 6.1 JobManager

```python
class JobManager:
    def __init__(self, interval_seconds=60):
        self.interval_seconds = interval_seconds
        self.running = False
        self.paused = False
        self._thread = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._job_loop, daemon=True)
        self._thread.start()
```

- Loop em thread daemon com intervalo configurável (default: 60s)
- Itera sobre `SUPPORTED_ASSETS` executando `pipeline.analyze(symbol)`
- Suporte a `pause()`, `resume()`, `stop()` com `thread.join()`

### 6.2 AssetRegistry

- Dataclass `Asset` com 16 campos (symbol, category, priority, provider, etc.)
- Persistência em JSON (`data/asset_registry.json`)
- Métodos: `register_asset()`, `set_enabled()`, `set_priority()`, `update_asset_stats()`, `search_assets()`, `filter_assets()`

---

## 7. Auditoria e Observabilidade

### 7.1 Pipeline Audit Middleware

```python
class PipelineAuditMiddleware:
    def __init__(self, profiler, sink):
        self.profiler = profiler  # ⚠️ Recebido mas não utilizado
        self.sink = sink

    def __call__(self, stage_name, func, *args, **kwargs):
        event = AuditEvent(stage_name=stage_name, timestamp=...)
        self.sink.log(event)
        return func(*args, **kwargs)
```

### 7.2 AuditSink (ABC)

```python
class AuditSink(ABC):
    @abstractmethod
    def log(self, event: AuditEvent):
        ...

class MemoryAuditSink(AuditSink):
    def __init__(self):
        self._events = []
```

### 7.3 SecurityCenter

- `AuditEvent` dataclass com user, action, target, severity, timestamp
- `generate_security_report()` retorna SECURE se critical_count == 0, senão WARNING

---

## 8. Avaliação da Arquitetura

### 8.1 Pontos Fortes ✅

| Aspecto | Avaliação |
|---------|-----------|
| **Modularidade** | Excelente — 30+ engines independentes com interface comum |
| **Separation of Concerns** | Excelente — cada engine tem responsabilidade única (SRP) |
| **Determinismo** | Excelente — DeterministicClock garante reprodução |
| **Contract Validation** | Muito bom — PipelineExecutor valida tipos de retorno |
| **Imutabilidade** | Muito bom — frozen dataclasses para resultados |
| **DI** | Bom — ConfluenceEngine recebe MarketThesisBuilder via construtor |
| **Observabilidade** | Muito bom — profiler, telemetry, audit trail, security center |
| **Extensibilidade** | Excelente — novo engine = herdar BaseEngine + implementar analyze() |
| **Background Execution** | Bom — JobManager com thread daemon |

### 8.2 Pontos de Atenção ⚠️

| Aspecto | Observação |
|---------|------------|
| **PipelineAuditMiddleware** | Recebe `profiler` no construtor mas não o utiliza — potencial dead code |
| **DeterministicClock** | Estado de classe (class-level) pode causar problemas em testes paralelos |
| **Two-pass context build** | Padrão necessário mas adiciona complexidade — documentar claramente |
| **JobManager** | Thread daemon — em caso de crash, análises em andamento são perdidas sem recovery |
| **AssetRegistry** | Persistência em JSON simples — sem locking, pode ter race condition em acesso concorrente |

### 8.3 Score Arquitetural

| Critério | Score (0-10) |
|----------|:----------:|
| Modularidade | 9.5 |
| Separation of Concerns | 9.0 |
| Determinismo | 9.5 |
| Contract Validation | 8.5 |
| Imutabilidade | 8.5 |
| Dependency Injection | 8.0 |
| Observabilidade | 8.5 |
| Extensibilidade | 9.5 |
| Concorrência | 7.0 |
| **Score Médio** | **8.7** |

---

## 9. Conclusão

A arquitetura do Mercury-AI é **institucional, modular e determinística**, seguindo padrões de design sólidos (ABC, frozen dataclasses, DI, contract validation). O sistema é altamente extensível e observável. Pontos de atenção são menores e não comprometem a integridade arquitetural.

**Veredito de Arquitetura: ✅ APROVADO (Score: 8.7/10)**

---

*Relatório gerado por GitHub Copilot (glm-5.2) — Auditoria de Arquitetura Mercury-AI*
