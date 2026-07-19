# Mercury AI V1 — Auditoria Completa de Imports

## Escopo
Auditoria estática de imports Python, módulos referenciados e símbolos importados no repositório, sem correções.

## Metodologia
- Varredura de arquivos Python sob o projeto.
- Análise de imports via AST.
- Verificação de módulos internos e símbolos expostos.
- Cross-check com a estrutura real de diretórios e classes.

## Resumo executivo
Foram encontrados problemas concretos de importação e compatibilidade de API em múltiplos pontos do projeto. Os principais itens são:
- imports para módulos que não existem;
- imports de classes/símbolos que não estão mais expostos pelo módulo alvo;
- imports apontando para nomes de classes que mudaram ou foram substituídos;
- dependências de importação bloqueadas por bibliotecas ausentes no ambiente atual;
- arquivos Python que parecem estar órfãos ou sem uso ativo no grafo de imports internos.

---

## 1) Imports inexistentes

### 1.1 Módulo inexistente
- Arquivo: [app/dashboard/observability_panel.py](app/dashboard/observability_panel.py)
- Import: `from mercury_ai.providers.manager import MercuryProviderManager`
- Evidência: não existe o módulo [mercury_ai/providers/manager.py](mercury_ai/providers/manager.py) no repositório.
- Impacto: o import aponta para um módulo que não existe.

---

## 2) Imports antigos / API desatualizada

### 2.1 Classe renomeada ou substituída
- Arquivo: [app/dashboard/dashboard.py](app/dashboard/dashboard.py)
- Import: `from mercury_ai.brain.scanner import Scanner`
- Evidência: o módulo [mercury_ai/brain/scanner.py](mercury_ai/brain/scanner.py) define a classe `MercuryScanner`, não `Scanner`.
- Impacto: o símbolo importado não existe no módulo atual.

### 2.2 Classe renomeada ou substituída
- Arquivo: [app/dashboard/operation_center.py](app/dashboard/operation_center.py)
- Import: `from mercury_ai.brain.scanner import Scanner`
- Evidência: o módulo [mercury_ai/brain/scanner.py](mercury_ai/brain/scanner.py) expõe `MercuryScanner`, não `Scanner`.
- Impacto: o import é incompatível com a API atual.

### 2.3 Classe renomeada ou substituída
- Arquivo: [app/terminal/pages/02_Dashboard.py](app/terminal/pages/02_Dashboard.py)
- Import: `from mercury_ai.brain.scanner import Scanner`
- Evidência: o módulo [mercury_ai/brain/scanner.py](mercury_ai/brain/scanner.py) define `MercuryScanner`.
- Impacto: o nome `Scanner` é antigo ou incompatível com a implementação atual.

### 2.4 Import para nome de classe que não existe no módulo alvo
- Arquivo: [mercury_ai/market/market_engine.py](mercury_ai/market/market_engine.py)
- Import: `from mercury_ai.providers.market_provider import MarketProvider`
- Evidência: o módulo [mercury_ai/providers/market_provider.py](mercury_ai/providers/market_provider.py) define `MercuryDataProvider`, não `MarketProvider`.
- Impacto: o import está desatualizado em relação à classe atual.

### 2.5 Teste apontando para nome antigo
- Arquivo: [mercury_ai/providers/tests/test_market_provider.py](mercury_ai/providers/tests/test_market_provider.py)
- Import: `from mercury_ai.providers.market_provider import MarketProvider`
- Evidência: o módulo alvo não expõe `MarketProvider`.
- Impacto: o teste depende de um nome de API que não está mais presente.

---

## 3) Métodos antigos / compatibilidade de API

### 3.1 Import de símbolo que não existe no módulo alvo
- Arquivo: [app/dashboard/health_center_panel.py](app/dashboard/health_center_panel.py)
- Import: `from mercury_ai.core.health_center import HealthCenter`
- Evidência: o módulo [mercury_ai/core/health_center.py](mercury_ai/core/health_center.py) existe, mas a importação depende de `psutil`, que não está disponível no ambiente atual.
- Impacto: a importação/uso do módulo fica bloqueado por dependência ausente.

### 3.2 Import de símbolo que depende de dependência ausente
- Arquivo: [app/terminal/pages/07_Observabilidade.py](app/terminal/pages/07_Observabilidade.py)
- Import: `from mercury_ai.utils.system_monitor import SystemMonitor`
- Evidência: o módulo [mercury_ai/utils/system_monitor.py](mercury_ai/utils/system_monitor.py) depende de `psutil`, e a dependência não está registrada em [requirements.txt](requirements.txt).
- Impacto: o módulo não pode ser importado corretamente sem o pacote faltante.

### 3.3 Dependência ausente para módulo de saúde
- Arquivo: [mercury_ai/core/auto_health.py](mercury_ai/core/auto_health.py)
- Import: `from mercury_ai.core.health_center import HealthCenter`
- Evidência: o módulo depende de `psutil`, que não está presente no ambiente de execução atual.
- Impacto: o fluxo de saúde fica prejudicado por dependência faltante.

---

## 4) Arquivos mortos ou presumivelmente órfãos

A análise estática de dependência interna apontou 63 módulos Python sob [mercury_ai](mercury_ai) que parecem não ser referenciados pelo grafo de imports interno atual. A lista abaixo é um relatório de suspeitas e não uma afirmação absoluta de que todos estejam sem uso em runtime.

### Arquivos com forte indicativo de desuso/órfãos
- [mercury_ai/ai/llm.py](mercury_ai/ai/llm.py)
- [mercury_ai/analysis/benchmark_framework.py](mercury_ai/analysis/benchmark_framework.py)
- [mercury_ai/analysis/calibration_analyzer.py](mercury_ai/analysis/calibration_analyzer.py)
- [mercury_ai/analysis/data_quality_engine.py](mercury_ai/analysis/data_quality_engine.py)
- [mercury_ai/analysis/health_auditor.py](mercury_ai/analysis/health_auditor.py)
- [mercury_ai/analysis/institutional_analytics_engine.py](mercury_ai/analysis/institutional_analytics_engine.py)
- [mercury_ai/analysis/institutional_context_builder.py](mercury_ai/analysis/institutional_context_builder.py)
- [mercury_ai/analysis/institutional_report.py](mercury_ai/analysis/institutional_report.py)
- [mercury_ai/analysis/learning_engine.py](mercury_ai/analysis/learning_engine.py)
- [mercury_ai/analysis/live_monitor.py](mercury_ai/analysis/live_monitor.py)
- [mercury_ai/analysis/momentum_engine.py](mercury_ai/analysis/momentum_engine.py)
- [mercury_ai/analysis/performance_center.py](mercury_ai/analysis/performance_center.py)
- [mercury_ai/analysis/post_decision_evaluation_engine.py](mercury_ai/analysis/post_decision_evaluation_engine.py)
- [mercury_ai/analysis/price_action_engine.py](mercury_ai/analysis/price_action_engine.py)
- [mercury_ai/analysis/provider_priority_engine.py](mercury_ai/analysis/provider_priority_engine.py)
- [mercury_ai/analysis/smart_money/liquidity_event_engine.py](mercury_ai/analysis/smart_money/liquidity_event_engine.py)
- [mercury_ai/analysis/trade_memory_engine.py](mercury_ai/analysis/trade_memory_engine.py)
- [mercury_ai/analysis/volume_engine.py](mercury_ai/analysis/volume_engine.py)
- [mercury_ai/analysis/vwap_engine.py](mercury_ai/analysis/vwap_engine.py)
- [mercury_ai/analysis/weight_simulator.py](mercury_ai/analysis/weight_simulator.py)
- [mercury_ai/brain/exceptions.py](mercury_ai/brain/exceptions.py)
- [mercury_ai/brain/explainability_engine.py](mercury_ai/brain/explainability_engine.py)
- [mercury_ai/calendar/economic_calendar.py](mercury_ai/calendar/economic_calendar.py)
- [mercury_ai/config/market_regimes.py](mercury_ai/config/market_regimes.py)
- [mercury_ai/config/risk.py](mercury_ai/config/risk.py)
- [mercury_ai/config/sessions.py](mercury_ai/config/sessions.py)
- [mercury_ai/config/strategies.py](mercury_ai/config/strategies.py)
- [mercury_ai/core/auto_health.py](mercury_ai/core/auto_health.py)
- [mercury_ai/core/data_quality_gate.py](mercury_ai/core/data_quality_gate.py)
- [mercury_ai/core/export_center.py](mercury_ai/core/export_center.py)
- [mercury_ai/core/job_manager.py](mercury_ai/core/job_manager.py)
- [mercury_ai/core/observability_center.py](mercury_ai/core/observability_center.py)
- [mercury_ai/core/pipeline_audit_middleware.py](mercury_ai/core/pipeline_audit_middleware.py)
- [mercury_ai/core/project_state.py](mercury_ai/core/project_state.py)
- [mercury_ai/core/read_only.py](mercury_ai/core/read_only.py)
- [mercury_ai/core/security_center.py](mercury_ai/core/security_center.py)
- [mercury_ai/core/session_manager.py](mercury_ai/core/session_manager.py)
- [mercury_ai/core/startup.py](mercury_ai/core/startup.py)
- [mercury_ai/data/market_data_provider.py](mercury_ai/data/market_data_provider.py)
- [mercury_ai/data/providers/historical_data_provider.py](mercury_ai/data/providers/historical_data_provider.py)
- [mercury_ai/data/replay_data_provider.py](mercury_ai/data/replay_data_provider.py)
- [mercury_ai/database/history_logger.py](mercury_ai/database/history_logger.py)
- [mercury_ai/indicators/rsi.py](mercury_ai/indicators/rsi.py)
- [mercury_ai/main.py](mercury_ai/main.py)
- [mercury_ai/market/market_engine.py](mercury_ai/market/market_engine.py)
- [mercury_ai/models/data_quality_result.py](mercury_ai/models/data_quality_result.py)
- [mercury_ai/models/decision_input.py](mercury_ai/models/decision_input.py)
- [mercury_ai/models/decision_outcome.py](mercury_ai/models/decision_outcome.py)
- [mercury_ai/models/professional_thesis.py](mercury_ai/models/professional_thesis.py)
- [mercury_ai/models/signal.py](mercury_ai/models/signal.py)
- [mercury_ai/models/trade_permission.py](mercury_ai/models/trade_permission.py)
- [mercury_ai/models/trend_analysis.py](mercury_ai/models/trend_analysis.py)
- [mercury_ai/news/news_provider.py](mercury_ai/news/news_provider.py)
- [mercury_ai/operations/demo_manager.py](mercury_ai/operations/demo_manager.py)
- [mercury_ai/providers/future_broker_provider.py](mercury_ai/providers/future_broker_provider.py)
- [mercury_ai/providers/future_polygon_provider.py](mercury_ai/providers/future_polygon_provider.py)
- [mercury_ai/providers/future_tradingview_provider.py](mercury_ai/providers/future_tradingview_provider.py)
- [mercury_ai/sessions/market_sessions.py](mercury_ai/sessions/market_sessions.py)
- [mercury_ai/utils/memory_auditor.py](mercury_ai/utils/memory_auditor.py)
- [mercury_ai/utils/performance_collector.py](mercury_ai/utils/performance_collector.py)
- [mercury_ai/utils/regression_detector.py](mercury_ai/utils/regression_detector.py)
- [mercury_ai/utils/report_generator.py](mercury_ai/utils/report_generator.py)
- [mercury_ai/utils/stress_tester.py](mercury_ai/utils/stress_tester.py)

> Observação: esse conjunto deve ser tratado como lista de alvos de revisão, não como prova definitiva de que todos esses módulos estejam mortos em runtime.

---

## 5) Conclusão
Os principais problemas detectados são:
1. imports para módulos que não existem;
2. uso de nomes de classes antigas ou incompatíveis com a implementação atual;
3. dependências ausentes que interrompem a importação de módulos de dashboard/saúde;
4. uma grande massa de módulos que parecem não ser referenciados ativamente pelo fluxo atual.

Nenhuma correção foi aplicada.
