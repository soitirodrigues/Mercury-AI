# 🔒 AUDITORIA DE SEGURANÇA — Mercury-AI

> **Data:** 2025-01-20  
> **Auditor:** GitHub Copilot (glm-5.2)  
> **Escopo:** Segurança de dados, validação de entrada, persistência, isolamento, auditoria  
> **Código-base:** `mercury_ai/` (core, brain, providers, data, database, config)

---

## 1. Visão Geral de Segurança

### 1.1 Modelo de Ameaças

O Mercury-AI é um sistema de análise e decisão de trading institucional que:
- Consome dados de mercado de providers externos (Yahoo Finance, etc.)
- Executa pipeline de análise com 25+ estágios
- Produz decisões de trading (direction, confidence, probability)
- Persiste snapshots de decisão em disco
- Expõe interface via Streamlit (app)

### 1.2 Superfície de Ataque

| Vetor | Exposição | Severidade |
|-------|:---------:|:----------:|
| Dados de provider maliciosos | Média | Alta |
| Arquivo JSON corrompido (AssetRegistry) | Média | Média |
| Snapshot de decisão corrompido | Baixa | Baixa |
| Interface Streamlit (XSS, injection) | Baixa | Média |
| Configuração (config.json) | Baixa | Média |
| Persistência de snapshots (race condition) | Baixa | Baixa |

---

## 2. Análise por Categoria

### 2.1 Validação de Entrada

#### 2.1.1 Dados de Provider

```python
# providers/yahoo.py
class YahooProvider:
    def fetch(self, symbol: str, ...) -> pd.DataFrame:
        data = yf.download(symbol, ...)
        return data
```

- ⚠️ **Sem validação de schema** — DataFrame retornado não é validado
- ⚠️ **Sem sanitização de symbol** — Input livre para `yf.download()`
- ⚠️ **Sem limite de tamanho** — DataFrame pode ser arbitrariamente grande
- ❌ **Sem detecção de dados anômalos** — Preços negativos, volumes impossíveis

#### 2.1.2 Configuração (config.json)

```python
# config_ai.py
with open('config.json', 'r') as f:
    config = json.load(f)
```

- ⚠️ **Sem validação de schema** — JSON carregado sem verificar chaves
- ⚠️ **Sem validação de tipos** — Valores não validados
- ⚠️ **Sem valores default** — Falha silenciosa se chave ausente

#### 2.1.3 AssetRegistry (JSON)

```python
# data/asset_registry.py
@dataclass
class Asset:
    symbol: str
    name: str
    # ... 16 fields

class AssetRegistry:
    def load(self) -> None:
        with open(self.path, 'r') as f:
            data = json.load(f)
        self._assets = [Asset(**a) for a in data]
```

- ⚠️ **Sem validação de campos** — `Asset(**a)` pode falhar com chaves extras
- ⚠️ **Sem proteção contra JSON malformado** — `json.load` lança exceção não tratada
- ❌ **Sem locking** — Race condition em acesso concorrente

### 2.2 Persistência e Armazenamento

#### 2.2.1 DecisionSnapshot

```python
# core/snapshot.py
class DecisionSnapshotLogger:
    def save(self, snapshot: DecisionSnapshot) -> Path:
        path = self.output_dir / f"snapshot_{snapshot.symbol}_{timestamp}.json"
        with open(path, 'w') as f:
            json.dump(snapshot.to_dict(), f, indent=2)
        return path
```

- ✅ **Diretório configurável** — `output_dir` parametrizável
- ⚠️ **Sem atomicidade** — Escrita não é atômica (sem temp+rename)
- ⚠️ **Sem verificação de path traversal** — `symbol` no nome do arquivo
- ❌ **Sem locking** — Race condition em save concorrente

#### 2.2.2 Runtime Reports

```python
# runtime_report_ASSET_0_20240103120000.json
```

- ⚠️ **Acumulação sem limpeza** — 24+ arquivos de runtime report no diretório raiz
- ⚠️ **Sem rotação** — Crescimento indefinido
- ⚠️ **Sem compressão** — Arquivos JSON em texto plano

### 2.3 Isolamento e Encapsulamento

#### 2.3.1 Engines

```python
# core/base_engine.py
class BaseEngine(ABC):
    @abstractmethod
    def analyze(self, context: AnalysisContext) -> EngineResult:
        ...
```

- ✅ **Interface abstrata** — Engines não expõem estado interno
- ✅ **EngineResult frozen** — Imutável, não modificável após criação
- ✅ **Evidences como tuple** — Imutável
- ✅ **Warnings como tuple** — Imutável

#### 2.3.2 PipelineExecutor

```python
# core/pipeline_executor.py
class PipelineExecutor:
    def execute(self, stage_name: str, func, *args, **kwargs):
        result = func(*args, **kwargs)
        if not isinstance(result, expected_type):
            raise PipelineContractError(...)
        return result
```

- ✅ **Validação de contrato** — Tipo de retorno verificado
- ✅ **Exceção explícita** — `PipelineContractError` em violação
- ⚠️ **Sem timeout** — Stage pode executar indefinidamente
- ⚠️ **Sem limite de memória** — Stage pode consumir muita memória

### 2.4 Auditoria e Rastreabilidade

#### 2.4.1 PipelineAuditMiddleware

```python
# core/audit.py
class PipelineAuditMiddleware:
    def __call__(self, stage_name: str, func, *args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        event = AuditEvent(
            stage_name=stage_name,
            timestamp=DeterministicClock.utcnow(),
            duration_ms=elapsed * 1000,
            success=True,
        )
        self.sink.log(event)
        return result
```

- ✅ **Rastreabilidade de estágio** — Cada estágio logado
- ✅ **Timestamp determinístico** — Reproducível
- ✅ **Duração medida** — Performance tracking
- ⚠️ **Sem captura de erro** — Exception não logada (apenas success=True)
- ⚠️ **Sem captura de input/output** — Apenas metadados

#### 2.4.2 SecurityCenter

```python
# core/security.py
class SecurityCenter:
    def generate_security_report(self) -> dict:
        ...
```

- ✅ **Geração de relatório** — Consolidado
- ⚠️ **Sem integração com alertas** — Não notifica em caso de anomalia
- ⚠️ **Sem persistência de relatório** — Apenas em memória

### 2.5 Interface de Usuário (Streamlit)

#### 2.5.1 Exposição de Dados

- ⚠️ **Sem autenticação** — Streamlit sem login
- ⚠️ **Sem rate limiting** — Sem limite de requisições
- ⚠️ **Sem CSRF protection** — Formulários sem token
- ⚠️ **Exposição de internals** — Engine results, evidences, warnings exibidos

#### 2.5.2 Input do Usuário

- ⚠️ **Sem sanitização** — Input de symbol não sanitizado
- ⚠️ **Sem validação de range** — Parâmetros sem limites

---

## 3. Matriz de Risco

| Risco | Probabilidade | Impacto | Score | Mitigação |
|-------|:------------:|:-------:|:-----:|:---------:|
| Dados de provider anômalos | Média | Alto | 6 | ❌ Nenhuma |
| JSON corrompido (AssetRegistry) | Baixa | Médio | 3 | ⚠️ Parcial |
| Race condition (snapshot save) | Baixa | Baixo | 2 | ❌ Nenhuma |
| Path traversal (snapshot filename) | Baixa | Médio | 3 | ❌ Nenhuma |
| Crescimento indefinido de logs | Alta | Baixo | 4 | ❌ Nenhuma |
| Exposição via Streamlit | Média | Médio | 4 | ❌ Nenhuma |
| Config inválida | Baixa | Alto | 4 | ⚠️ Parcial |
| Exception não tratada em pipeline | Média | Alto | 6 | ⚠️ Parcial |

---

## 4. Pontos Fortes

1. ✅ **EngineResult frozen** — Imutabilidade garante integridade
2. ✅ **PipelineExecutor com validação de contrato** — Tipos verificados
3. ✅ **PipelineAuditMiddleware** — Rastreabilidade de estágios
4. ✅ **DeterministicClock** — Reproducibilidade sem dependência de tempo real
5. ✅ **Isolamento de engines** — Interface abstrata, sem estado compartilhado
6. ✅ **Evidences/warnings como tuple** — Imutáveis

---

## 5. Pontos Fracos

1. ❌ **Sem validação de schema de entrada** — DataFrames e JSON não validados
2. ❌ **Sem atomicidade na persistência** — Escrita não atômica (sem temp+rename)
3. ❌ **Sem locking** — Race conditions em AssetRegistry e snapshot
4. ❌ **Sem path traversal protection** — Symbol no nome de arquivo
5. ❌ **Sem rotação/limpeza de logs** — Crescimento indefinido
6. ❌ **Sem autenticação na UI** — Streamlit sem login
7. ⚠️ **Sem captura de erro no audit middleware** — Apenas success=True
8. ⚠️ **Sem timeout/limite de memória no pipeline** — Stage pode travar
9. ⚠️ **Sem validação de config** — JSON carregado sem schema

---

## 6. Recomendações

### 6.1 Alta Prioridade

1. **Validar schema de DataFrame de provider** — Usar `pandera` ou validação manual
2. **Sanitizar symbol** — Regex `^[A-Z]{1,10}$` antes de usar em nome de arquivo
3. **Escrita atômica** — Temp file + `os.rename()` para snapshots
4. **Adicionar locking** — `threading.Lock` em AssetRegistry e snapshot save
5. **Capturar erros no audit middleware** — Log de `success=False` com traceback

### 6.2 Média Prioridade

6. **Validar config.json** — Schema com `pydantic` ou `jsonschema`
7. **Adicionar timeout no PipelineExecutor** — `concurrent.futures.TimeoutError`
8. **Rotação de logs** — `logging.handlers.RotatingFileHandler` ou limpeza periódica
9. **Autenticação na UI** — `streamlit-authenticator` ou middleware

### 6.3 Baixa Prioridade

10. **Rate limiting na UI** — Limite de requisições por sessão
11. **Compressão de snapshots** — `gzip` para arquivos antigos
12. **Detecção de anomalias em dados** — Preços negativos, volumes impossíveis

---

## 7. Score de Segurança

| Critério | Score (0-10) |
|----------|:----------:|
| Validação de entrada | 4.0 |
| Persistência segura | 5.0 |
| Isolamento/encapsulamento | 8.0 |
| Auditoria/rastreabilidade | 7.0 |
| Interface de usuário | 3.0 |
| Tratamento de erro | 5.0 |
| Gestão de configuração | 4.0 |
| Proteção de dados | 6.0 |
| **Score Médio** | **5.3** |

---

## 8. Conclusão

O Mercury-AI tem uma **base sólida de isolamento e imutabilidade** (EngineResult frozen, PipelineExecutor com validação de contrato, PipelineAuditMiddleware), mas apresenta **lacunas significativas em validação de entrada, persistência segura e interface de usuário**. A ausência de validação de schema, atomicidade de escrita, locking e autenticação na UI são os pontos mais críticos.

**Veredito de Segurança: ⚠️ APROVADO COM RESSALVAS (Score: 5.3/10)**

> **Ressalvas críticas:**
> 1. Adicionar validação de schema para dados de provider
> 2. Implementar escrita atômica e locking para snapshots
> 3. Sanitizar symbol para prevenir path traversal
> 4. Adicionar autenticação na interface Streamlit
> 5. Capturar erros no PipelineAuditMiddleware

---

*Relatório gerado por GitHub Copilot (glm-5.2) — Auditoria de Segurança Mercury-AI*
