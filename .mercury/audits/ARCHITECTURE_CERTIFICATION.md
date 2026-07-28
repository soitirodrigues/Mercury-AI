# ARCHITECTURE CERTIFICATION REPORT

**Project:** Mercury AI V1
**Audit:** SPRINT 1.9 BLOCO 1/10 - Architecture Certification
**Verdict:** FAIL
**Total Findings:** 1980
**FAIL:** 847
**WARNING:** 1046
**INFO:** 87

## Summary by Category

| Category | Count | Severity |
|----------|-------|----------|
| BROKEN_IMPORT | 847 | FAIL |
| DEAD_CODE_MODULE | 88 | WARNING |
| DIP_VIOLATION | 7 | WARNING |
| DUPLICATE_CLASS | 12 | WARNING |
| DUPLICATE_FUNCTION | 61 | WARNING |
| EXCESSIVE_COUPLING_FANIN | 7 | WARNING |
| EXCESSIVE_COUPLING_FANOUT | 4 | WARNING |
| HIDDEN_DEPENDENCY | 60 | WARNING |
| LSP_CONCERN | 15 | INFO |
| OCP_VIOLATION | 72 | INFO |
| ORPHAN_MODULE | 241 | WARNING |
| UNUSED_CLASS | 75 | WARNING |
| UNUSED_FUNCTION | 491 | WARNING |

## Detailed Findings

### BROKEN_IMPORT (847 findings)

#### FAIL: main

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'main' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: run_deterministic_replay_scenarios

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'run_deterministic_replay_scenarios' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: run_institutional_replay

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'run_institutional_replay' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: run_institutional_replay

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'run_institutional_replay' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: run_institutional_replay

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'run_institutional_replay' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: run_institutional_replay

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'run_institutional_replay' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: run_institutional_replay

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'run_institutional_replay' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: run_instrumented

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'run_instrumented' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: run_instrumented

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'run_instrumented' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: stress_test_replay

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'stress_test_replay' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: test_bloco7_scenarios

**Message:** Broken import: 'mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine' not found in codebase

**Evidence:** Module 'test_bloco7_scenarios' imports 'mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine' which does not exist

**import:** mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine

#### FAIL: test_bloco7_scenarios

**Message:** Broken import: 'mercury_ai.analysis.decision_resolver_engine.DecisionResolverResult' not found in codebase

**Evidence:** Module 'test_bloco7_scenarios' imports 'mercury_ai.analysis.decision_resolver_engine.DecisionResolverResult' which does not exist

**import:** mercury_ai.analysis.decision_resolver_engine.DecisionResolverResult

#### FAIL: test_mercury_signal

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'test_mercury_signal' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: test_mercury_signal

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'test_mercury_signal' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: test_mercury_signal

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'test_mercury_signal' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: test_mercury_signal

**Message:** Broken import: 'mercury_ai.presentation.signal_formatter.SignalFormatter' not found in codebase

**Evidence:** Module 'test_mercury_signal' imports 'mercury_ai.presentation.signal_formatter.SignalFormatter' which does not exist

**import:** mercury_ai.presentation.signal_formatter.SignalFormatter

#### FAIL: test_replay_quick

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'test_replay_quick' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: test_replay_quick

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'test_replay_quick' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: test_replay_quick

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'test_replay_quick' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: validate_universe_parity

**Message:** Broken import: 'mercury_ai.config.universe.ALL_SYMBOLS' not found in codebase

**Evidence:** Module 'validate_universe_parity' imports 'mercury_ai.config.universe.ALL_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### FAIL: verify_assets

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'verify_assets' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: verify_assets

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'verify_assets' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: verify_assets

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'verify_assets' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: app.launcher

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'app.launcher' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: app.dashboard.asset_registry_panel

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'app.dashboard.asset_registry_panel' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: app.dashboard.asset_registry_panel

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'app.dashboard.asset_registry_panel' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' which does not exist

**import:** mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator' which does not exist

**import:** mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.notification_center.NotificationCenter' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.notification_center.NotificationCenter' which does not exist

**import:** mercury_ai.analysis.notification_center.NotificationCenter

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'app.ui_utils.apply_design_system' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'app.ui_utils.apply_design_system' which does not exist

**import:** app.ui_utils.apply_design_system

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'app.ui_utils.display_metric' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'app.ui_utils.display_metric' which does not exist

**import:** app.ui_utils.display_metric

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.analysis.data_exporter.DataExporter' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.analysis.data_exporter.DataExporter' which does not exist

**import:** mercury_ai.analysis.data_exporter.DataExporter

#### FAIL: app.dashboard.dashboard

**Message:** Broken import: 'mercury_ai.config.configuration_center.MercuryConfigCenter' not found in codebase

**Evidence:** Module 'app.dashboard.dashboard' imports 'mercury_ai.config.configuration_center.MercuryConfigCenter' which does not exist

**import:** mercury_ai.config.configuration_center.MercuryConfigCenter

#### FAIL: app.dashboard.health_center_panel

**Message:** Broken import: 'mercury_ai.core.health_center.HealthCenter' not found in codebase

**Evidence:** Module 'app.dashboard.health_center_panel' imports 'mercury_ai.core.health_center.HealthCenter' which does not exist

**import:** mercury_ai.core.health_center.HealthCenter

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'mercury_ai.core.health_center.HealthCenter' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'mercury_ai.core.health_center.HealthCenter' which does not exist

**import:** mercury_ai.core.health_center.HealthCenter

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'app.dashboard.asset_registry_panel.render_asset_registry_dashboard' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'app.dashboard.asset_registry_panel.render_asset_registry_dashboard' which does not exist

**import:** app.dashboard.asset_registry_panel.render_asset_registry_dashboard

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'app.dashboard.provider_health_panel.render_provider_health_dashboard' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'app.dashboard.provider_health_panel.render_provider_health_dashboard' which does not exist

**import:** app.dashboard.provider_health_panel.render_provider_health_dashboard

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'app.dashboard.observability_panel.render_observability_dashboard' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'app.dashboard.observability_panel.render_observability_dashboard' which does not exist

**import:** app.dashboard.observability_panel.render_observability_dashboard

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'app.dashboard.health_center_panel.render_health_center_panel' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'app.dashboard.health_center_panel.render_health_center_panel' which does not exist

**import:** app.dashboard.health_center_panel.render_health_center_panel

#### FAIL: app.dashboard.main_dashboard

**Message:** Broken import: 'app.dashboard.market_map_panel.render_market_map_panel' not found in codebase

**Evidence:** Module 'app.dashboard.main_dashboard' imports 'app.dashboard.market_map_panel.render_market_map_panel' which does not exist

**import:** app.dashboard.market_map_panel.render_market_map_panel

#### FAIL: app.dashboard.market_map_panel

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'app.dashboard.market_map_panel' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: app.dashboard.observability_panel

**Message:** Broken import: 'mercury_ai.providers.market_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'app.dashboard.observability_panel' imports 'mercury_ai.providers.market_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.market_provider.MercuryDataProvider

#### FAIL: app.dashboard.operation_center

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'app.dashboard.operation_center' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: app.dashboard.operation_center

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'app.dashboard.operation_center' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: app.dashboard.operation_center

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'app.dashboard.operation_center' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: app.dashboard.operation_center

**Message:** Broken import: 'mercury_ai.analysis.integrity_checker.IntegrityChecker' not found in codebase

**Evidence:** Module 'app.dashboard.operation_center' imports 'mercury_ai.analysis.integrity_checker.IntegrityChecker' which does not exist

**import:** mercury_ai.analysis.integrity_checker.IntegrityChecker

#### FAIL: app.dashboard.operation_center

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'app.dashboard.operation_center' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: app.dashboard.operation_center

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'app.dashboard.operation_center' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: app.dashboard.provider_health_panel

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'app.dashboard.provider_health_panel' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: app.dashboard.provider_health_panel

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.ProviderStatus' not found in codebase

**Evidence:** Module 'app.dashboard.provider_health_panel' imports 'mercury_ai.data.mercury_data_provider.ProviderStatus' which does not exist

**import:** mercury_ai.data.mercury_data_provider.ProviderStatus

#### FAIL: app.terminal.terminal

**Message:** Broken import: 'app.ui_utils.apply_design_system' not found in codebase

**Evidence:** Module 'app.terminal.terminal' imports 'app.ui_utils.apply_design_system' which does not exist

**import:** app.ui_utils.apply_design_system

#### FAIL: app.terminal.terminal

**Message:** Broken import: 'app.ui_utils.display_status' not found in codebase

**Evidence:** Module 'app.terminal.terminal' imports 'app.ui_utils.display_status' which does not exist

**import:** app.ui_utils.display_status

#### FAIL: app.terminal.terminal

**Message:** Broken import: 'app.ui_utils.display_card' not found in codebase

**Evidence:** Module 'app.terminal.terminal' imports 'app.ui_utils.display_card' which does not exist

**import:** app.ui_utils.display_card

#### FAIL: app.terminal.terminal

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'app.terminal.terminal' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: app.terminal.terminal

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'app.terminal.terminal' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: app.terminal.pages.01_Scanner

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'app.terminal.pages.01_Scanner' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: app.terminal.pages.01_Scanner

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'app.terminal.pages.01_Scanner' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: app.terminal.pages.02_Dashboard

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'app.terminal.pages.02_Dashboard' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: app.terminal.pages.03_Historico_Estatisticas

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'app.terminal.pages.03_Historico_Estatisticas' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: app.terminal.pages.03_Historico_Estatisticas

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'app.terminal.pages.03_Historico_Estatisticas' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: app.terminal.pages.04_Auditoria_Configuracoes

**Message:** Broken import: 'mercury_ai.analysis.integrity_checker.IntegrityChecker' not found in codebase

**Evidence:** Module 'app.terminal.pages.04_Auditoria_Configuracoes' imports 'mercury_ai.analysis.integrity_checker.IntegrityChecker' which does not exist

**import:** mercury_ai.analysis.integrity_checker.IntegrityChecker

#### FAIL: app.terminal.pages.04_Auditoria_Configuracoes

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'app.terminal.pages.04_Auditoria_Configuracoes' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: app.terminal.pages.04_Auditoria_Configuracoes

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'app.terminal.pages.04_Auditoria_Configuracoes' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: app.terminal.pages.05_Replay

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'app.terminal.pages.05_Replay' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: app.terminal.pages.06_Demo

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'app.terminal.pages.06_Demo' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: app.terminal.pages.06_Demo

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'app.terminal.pages.06_Demo' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: app.terminal.pages.06_Demo

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'app.terminal.pages.06_Demo' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: app.terminal.pages.06_Demo

**Message:** Broken import: 'mercury_ai.config.assets.SUPPORTED_ASSETS' not found in codebase

**Evidence:** Module 'app.terminal.pages.06_Demo' imports 'mercury_ai.config.assets.SUPPORTED_ASSETS' which does not exist

**import:** mercury_ai.config.assets.SUPPORTED_ASSETS

#### FAIL: app.terminal.pages.06_Demo

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'app.terminal.pages.06_Demo' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: app.terminal.pages.06_Demo

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'app.terminal.pages.06_Demo' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: app.terminal.pages.07_Observabilidade

**Message:** Broken import: 'mercury_ai.utils.system_monitor.SystemMonitor' not found in codebase

**Evidence:** Module 'app.terminal.pages.07_Observabilidade' imports 'mercury_ai.utils.system_monitor.SystemMonitor' which does not exist

**import:** mercury_ai.utils.system_monitor.SystemMonitor

#### FAIL: app.terminal.pages.07_Observabilidade

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'app.terminal.pages.07_Observabilidade' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: app.terminal.pages.07_Observabilidade

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'app.terminal.pages.07_Observabilidade' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: app.terminal.pages.07_Observabilidade

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'app.terminal.pages.07_Observabilidade' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.main

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'mercury_ai.main' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: mercury_ai.analysis.adaptive_weight_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.adaptive_weight_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.adaptive_weight_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.adaptive_weight_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.models.benchmark_report.BenchmarkRunResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.models.benchmark_report.BenchmarkRunResult' which does not exist

**import:** mercury_ai.models.benchmark_report.BenchmarkRunResult

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.models.benchmark_report.BenchmarkReport' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.models.benchmark_report.BenchmarkReport' which does not exist

**import:** mercury_ai.models.benchmark_report.BenchmarkReport

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.metric_calculator.MetricCalculator' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.analysis.metric_calculator.MetricCalculator' which does not exist

**import:** mercury_ai.analysis.metric_calculator.MetricCalculator

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.metric_calculator.PerformanceMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.analysis.metric_calculator.PerformanceMetrics' which does not exist

**import:** mercury_ai.analysis.metric_calculator.PerformanceMetrics

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: mercury_ai.analysis.benchmark_framework

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.core.base_engine.BaseEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.core.base_engine.BaseEngine' which does not exist

**import:** mercury_ai.core.base_engine.BaseEngine

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.core.base_engine.EngineResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.core.base_engine.EngineResult' which does not exist

**import:** mercury_ai.core.base_engine.EngineResult

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.models.candlestick_analysis.CandlestickAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.models.candlestick_analysis.CandlestickAnalysis' which does not exist

**import:** mercury_ai.models.candlestick_analysis.CandlestickAnalysis

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.models.market_condition.MarketCondition' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.models.market_condition.MarketCondition' which does not exist

**import:** mercury_ai.models.market_condition.MarketCondition

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.candlestick_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_query.EvidenceQuery' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' imports 'mercury_ai.analysis.evidence_query.EvidenceQuery' which does not exist

**import:** mercury_ai.analysis.evidence_query.EvidenceQuery

#### FAIL: mercury_ai.analysis.confidence_calibration_auditor

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_calibration_auditor' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.confidence_calibration_auditor

**Message:** Broken import: 'mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_calibration_auditor' imports 'mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine' which does not exist

**import:** mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine

#### FAIL: mercury_ai.analysis.confidence_calibration_auditor

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_calibration_auditor' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.analysis.confidence_calibration_auditor

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_calibration_auditor' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: mercury_ai.analysis.confidence_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.confidence_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.confidence_engine

**Message:** Broken import: 'mercury_ai.models.confidence_result.ConfidenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' imports 'mercury_ai.models.confidence_result.ConfidenceResult' which does not exist

**import:** mercury_ai.models.confidence_result.ConfidenceResult

#### FAIL: mercury_ai.analysis.confidence_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_query.EvidenceQuery' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' imports 'mercury_ai.analysis.evidence_query.EvidenceQuery' which does not exist

**import:** mercury_ai.analysis.evidence_query.EvidenceQuery

#### FAIL: mercury_ai.analysis.confidence_engine

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.analysis.confidence_engine

**Message:** Broken import: 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' imports 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' which does not exist

**import:** mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine

#### FAIL: mercury_ai.analysis.conflict_resolution_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.conflict_resolution_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.conflict_resolution_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.conflict_resolution_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.conflict_resolution_engine

**Message:** Broken import: 'mercury_ai.analysis.adaptive_weight_engine.AdaptiveWeightEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.conflict_resolution_engine' imports 'mercury_ai.analysis.adaptive_weight_engine.AdaptiveWeightEngine' which does not exist

**import:** mercury_ai.analysis.adaptive_weight_engine.AdaptiveWeightEngine

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.models.confluence_result.ConfluenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.models.confluence_result.ConfluenceResult' which does not exist

**import:** mercury_ai.models.confluence_result.ConfluenceResult

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder' which does not exist

**import:** mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.analysis.decision_trace_engine.DecisionTraceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.analysis.decision_trace_engine.DecisionTraceEngine' which does not exist

**import:** mercury_ai.analysis.decision_trace_engine.DecisionTraceEngine

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.analysis.institutional_contribution.InstitutionalContribution' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.analysis.institutional_contribution.InstitutionalContribution' which does not exist

**import:** mercury_ai.analysis.institutional_contribution.InstitutionalContribution

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_helpers.has_conflict' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.analysis.confluence_helpers.has_conflict' which does not exist

**import:** mercury_ai.analysis.confluence_helpers.has_conflict

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_helpers.clamp_score' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.analysis.confluence_helpers.clamp_score' which does not exist

**import:** mercury_ai.analysis.confluence_helpers.clamp_score

#### FAIL: mercury_ai.analysis.confluence_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_helpers.dominant_direction' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' imports 'mercury_ai.analysis.confluence_helpers.dominant_direction' which does not exist

**import:** mercury_ai.analysis.confluence_helpers.dominant_direction

#### FAIL: mercury_ai.analysis.confluence_helpers

**Message:** Broken import: 'mercury_ai.models.direction.AnalysisDirection' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_helpers' imports 'mercury_ai.models.direction.AnalysisDirection' which does not exist

**import:** mercury_ai.models.direction.AnalysisDirection

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.models.confluence_score.ConfluenceScore' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.models.confluence_score.ConfluenceScore' which does not exist

**import:** mercury_ai.models.confluence_score.ConfluenceScore

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_query.EvidenceQuery' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.analysis.evidence_query.EvidenceQuery' which does not exist

**import:** mercury_ai.analysis.evidence_query.EvidenceQuery

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_helpers.has_conflict' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.analysis.confluence_helpers.has_conflict' which does not exist

**import:** mercury_ai.analysis.confluence_helpers.has_conflict

#### FAIL: mercury_ai.analysis.confluence_score_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_helpers.clamp_score' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' imports 'mercury_ai.analysis.confluence_helpers.clamp_score' which does not exist

**import:** mercury_ai.analysis.confluence_helpers.clamp_score

#### FAIL: mercury_ai.analysis.context_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.context_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.context_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.context_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.context_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.context_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.context_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.context_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.context_intelligence_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.context_intelligence_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.context_intelligence_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.context_intelligence_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.data_exporter

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.data_exporter' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: mercury_ai.analysis.data_exporter

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.data_exporter' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.decision_explainability

**Message:** Broken import: 'mercury_ai.analysis.institutional_contribution.InstitutionalContribution' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_explainability' imports 'mercury_ai.analysis.institutional_contribution.InstitutionalContribution' which does not exist

**import:** mercury_ai.analysis.institutional_contribution.InstitutionalContribution

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.version_metadata.VersionMetadata' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.version_metadata.VersionMetadata' which does not exist

**import:** mercury_ai.models.version_metadata.VersionMetadata

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.confidence_result.ConfidenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.confidence_result.ConfidenceResult' which does not exist

**import:** mercury_ai.models.confidence_result.ConfidenceResult

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.confluence_result.ConfluenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.confluence_result.ConfluenceResult' which does not exist

**import:** mercury_ai.models.confluence_result.ConfluenceResult

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.probability_result.ProbabilityResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.probability_result.ProbabilityResult' which does not exist

**import:** mercury_ai.models.probability_result.ProbabilityResult

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.models.trading_explanation.TradingExplanation' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.models.trading_explanation.TradingExplanation' which does not exist

**import:** mercury_ai.models.trading_explanation.TradingExplanation

#### FAIL: mercury_ai.analysis.decision_result_builder

**Message:** Broken import: 'mercury_ai.analysis.decision_explainability.DecisionExplainability' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' imports 'mercury_ai.analysis.decision_explainability.DecisionExplainability' which does not exist

**import:** mercury_ai.analysis.decision_explainability.DecisionExplainability

#### FAIL: mercury_ai.analysis.decision_trace_engine

**Message:** Broken import: 'mercury_ai.models.decision_trace.DecisionTrace' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_trace_engine' imports 'mercury_ai.models.decision_trace.DecisionTrace' which does not exist

**import:** mercury_ai.models.decision_trace.DecisionTrace

#### FAIL: mercury_ai.analysis.decision_trace_engine

**Message:** Broken import: 'mercury_ai.models.decision_trace.DecisionNode' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.decision_trace_engine' imports 'mercury_ai.models.decision_trace.DecisionNode' which does not exist

**import:** mercury_ai.models.decision_trace.DecisionNode

#### FAIL: mercury_ai.analysis.engine_performance_auditor

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.engine_performance_auditor' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.engine_performance_auditor

**Message:** Broken import: 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.engine_performance_auditor' imports 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' which does not exist

**import:** mercury_ai.analysis.performance_analytics.PerformanceAnalytics

#### FAIL: mercury_ai.analysis.engine_performance_auditor

**Message:** Broken import: 'mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.engine_performance_auditor' imports 'mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine' which does not exist

**import:** mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine

#### FAIL: mercury_ai.analysis.evidence_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.evidence_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.evidence_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.evidence_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' imports 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' which does not exist

**import:** mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine

#### FAIL: mercury_ai.analysis.evidence_engine

**Message:** Broken import: 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' imports 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' which does not exist

**import:** mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine

#### FAIL: mercury_ai.analysis.evidence_engine

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.analysis.evidence_quality_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_quality_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.evidence_query

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_query' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.evidence_ranking_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_ranking_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.evidence_ranking_engine

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.evidence_ranking_engine' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.analysis.fair_value_gap_engine

**Message:** Broken import: 'mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.fair_value_gap_engine' imports 'mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis' which does not exist

**import:** mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis

#### FAIL: mercury_ai.analysis.fair_value_gap_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.fair_value_gap_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.fair_value_gap_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.fair_value_gap_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.fair_value_gap_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.fair_value_gap_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.health_auditor

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_auditor' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.health_auditor

**Message:** Broken import: 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_auditor' imports 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' which does not exist

**import:** mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine

#### FAIL: mercury_ai.analysis.health_auditor

**Message:** Broken import: 'mercury_ai.brain.probability_engine.ProbabilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_auditor' imports 'mercury_ai.brain.probability_engine.ProbabilityEngine' which does not exist

**import:** mercury_ai.brain.probability_engine.ProbabilityEngine

#### FAIL: mercury_ai.analysis.health_auditor

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_auditor' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.health_checker

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_checker' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.health_checker

**Message:** Broken import: 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_checker' imports 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' which does not exist

**import:** mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine

#### FAIL: mercury_ai.analysis.health_checker

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_checker' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.health_checker

**Message:** Broken import: 'mercury_ai.brain.probability_engine.ProbabilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_checker' imports 'mercury_ai.brain.probability_engine.ProbabilityEngine' which does not exist

**import:** mercury_ai.brain.probability_engine.ProbabilityEngine

#### FAIL: mercury_ai.analysis.health_checker

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_checker' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.analysis.health_checker

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.health_checker' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayStorage' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.database.replay_storage.ReplayStorage' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayStorage

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider' which does not exist

**import:** mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider

#### FAIL: mercury_ai.analysis.historical_replay_engine

**Message:** Broken import: 'mercury_ai.analysis.replay_cache.ReplayCache' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' imports 'mercury_ai.analysis.replay_cache.ReplayCache' which does not exist

**import:** mercury_ai.analysis.replay_cache.ReplayCache

#### FAIL: mercury_ai.analysis.institutional_memory_engine

**Message:** Broken import: 'mercury_ai.models.decision_snapshot.DecisionSnapshot' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_memory_engine' imports 'mercury_ai.models.decision_snapshot.DecisionSnapshot' which does not exist

**import:** mercury_ai.models.decision_snapshot.DecisionSnapshot

#### FAIL: mercury_ai.analysis.institutional_report

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_report' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.institutional_report_generator

**Message:** Broken import: 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_report_generator' imports 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' which does not exist

**import:** mercury_ai.analysis.performance_analytics.PerformanceAnalytics

#### FAIL: mercury_ai.analysis.institutional_report_generator

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_report_generator' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: mercury_ai.analysis.institutional_report_generator

**Message:** Broken import: 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_report_generator' imports 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' which does not exist

**import:** mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor

#### FAIL: mercury_ai.analysis.institutional_report_generator

**Message:** Broken import: 'mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_report_generator' imports 'mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor' which does not exist

**import:** mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor

#### FAIL: mercury_ai.analysis.institutional_trade_filter_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_trade_filter_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.institutional_trade_filter_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_trade_filter_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.institutional_trade_filter_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_trade_filter_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.analysis.institutional_trade_filter_engine

**Message:** Broken import: 'mercury_ai.models.trade_filter_result.TradeFilterResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.institutional_trade_filter_engine' imports 'mercury_ai.models.trade_filter_result.TradeFilterResult' which does not exist

**import:** mercury_ai.models.trade_filter_result.TradeFilterResult

#### FAIL: mercury_ai.analysis.integrity_checker

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.integrity_checker' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.market_condition_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_condition_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.market_condition_engine

**Message:** Broken import: 'mercury_ai.models.market_condition.MarketCondition' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_condition_engine' imports 'mercury_ai.models.market_condition.MarketCondition' which does not exist

**import:** mercury_ai.models.market_condition.MarketCondition

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.market_state.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.market_state.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state.MarketStateEnum

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.liquidity_profile.LiquidityProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.liquidity_profile.LiquidityProfile' which does not exist

**import:** mercury_ai.models.liquidity_profile.LiquidityProfile

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.price_action.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.price_action.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action.PriceActionAnalysis

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.analysis.market_context_builder

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.analysis.market_regime_engine

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_regime_engine' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.analysis.market_regime_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_regime_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.analysis.market_state_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_state_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.market_state_engine

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_state_engine' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.analysis.market_state_engine

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_state_engine' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.analysis.market_state_engine

**Message:** Broken import: 'mercury_ai.models.session_analysis.SessionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_state_engine' imports 'mercury_ai.models.session_analysis.SessionAnalysis' which does not exist

**import:** mercury_ai.models.session_analysis.SessionAnalysis

#### FAIL: mercury_ai.analysis.market_structure_intelligence_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_structure_intelligence_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.market_structure_intelligence_engine

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_structure_intelligence_engine' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: mercury_ai.analysis.market_structure_intelligence_engine

**Message:** Broken import: 'mercury_ai.analysis.swing_engine.SwingEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_structure_intelligence_engine' imports 'mercury_ai.analysis.swing_engine.SwingEngine' which does not exist

**import:** mercury_ai.analysis.swing_engine.SwingEngine

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.models.market_thesis.MarketThesis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.models.market_thesis.MarketThesis' which does not exist

**import:** mercury_ai.models.market_thesis.MarketThesis

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.analysis.risk_engine.RiskEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.analysis.risk_engine.RiskEngine' which does not exist

**import:** mercury_ai.analysis.risk_engine.RiskEngine

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' which does not exist

**import:** mercury_ai.analysis.confidence_engine.ConfidenceEngine

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.analysis.market_state_engine.MarketStateEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.analysis.market_state_engine.MarketStateEngine' which does not exist

**import:** mercury_ai.analysis.market_state_engine.MarketStateEngine

#### FAIL: mercury_ai.analysis.market_thesis_builder

**Message:** Broken import: 'mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' imports 'mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine' which does not exist

**import:** mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine

#### FAIL: mercury_ai.analysis.momentum_engine

**Message:** Broken import: 'mercury_ai.models.momentum_analysis.MomentumAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.momentum_engine' imports 'mercury_ai.models.momentum_analysis.MomentumAnalysis' which does not exist

**import:** mercury_ai.models.momentum_analysis.MomentumAnalysis

#### FAIL: mercury_ai.analysis.momentum_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.momentum_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.momentum_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.momentum_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.momentum_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.momentum_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.providers.base_provider.MarketDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.providers.base_provider.MarketDataProvider' which does not exist

**import:** mercury_ai.providers.base_provider.MarketDataProvider

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.data.indicator_engine.IndicatorEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.data.indicator_engine.IndicatorEngine' which does not exist

**import:** mercury_ai.data.indicator_engine.IndicatorEngine

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.analysis.trend_analyzer.TrendAnalyzer' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.analysis.trend_analyzer.TrendAnalyzer' which does not exist

**import:** mercury_ai.analysis.trend_analyzer.TrendAnalyzer

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.analysis.volatility_engine.VolatilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.analysis.volatility_engine.VolatilityEngine' which does not exist

**import:** mercury_ai.analysis.volatility_engine.VolatilityEngine

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine' which does not exist

**import:** mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.analysis.mtf_engine

**Message:** Broken import: 'mercury_ai.config.timeframes.YFINANCE_INTERVALS' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' imports 'mercury_ai.config.timeframes.YFINANCE_INTERVALS' which does not exist

**import:** mercury_ai.config.timeframes.YFINANCE_INTERVALS

#### FAIL: mercury_ai.analysis.narrative_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.narrative_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.narrative_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.narrative_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.narrative_engine

**Message:** Broken import: 'mercury_ai.models.trading_explanation.TradingExplanation' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.narrative_engine' imports 'mercury_ai.models.trading_explanation.TradingExplanation' which does not exist

**import:** mercury_ai.models.trading_explanation.TradingExplanation

#### FAIL: mercury_ai.analysis.notification_center

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.notification_center' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.analysis.operational_history

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.operational_history' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.operational_history

**Message:** Broken import: 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.operational_history' imports 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' which does not exist

**import:** mercury_ai.analysis.performance_analytics.PerformanceAnalytics

#### FAIL: mercury_ai.analysis.performance_analytics

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_analytics' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.performance_analytics

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_analytics' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.analysis.performance_analytics

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_analytics' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: mercury_ai.analysis.performance_analytics

**Message:** Broken import: 'mercury_ai.core.exceptions.MarketClosedException' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_analytics' imports 'mercury_ai.core.exceptions.MarketClosedException' which does not exist

**import:** mercury_ai.core.exceptions.MarketClosedException

#### FAIL: mercury_ai.analysis.performance_center

**Message:** Broken import: 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_center' imports 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' which does not exist

**import:** mercury_ai.analysis.performance_analytics.PerformanceAnalytics

#### FAIL: mercury_ai.analysis.performance_center

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_center' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: mercury_ai.analysis.performance_center

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_center' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.performance_engine

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_engine' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: mercury_ai.analysis.performance_engine

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_engine' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: mercury_ai.analysis.performance_engine

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.ReplayMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_engine' imports 'mercury_ai.analysis.historical_replay_engine.ReplayMetrics' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.ReplayMetrics

#### FAIL: mercury_ai.analysis.performance_statistics

**Message:** Broken import: 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.performance_statistics' imports 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' which does not exist

**import:** mercury_ai.analysis.performance_analytics.PerformanceAnalytics

#### FAIL: mercury_ai.analysis.post_decision_evaluation_engine

**Message:** Broken import: 'mercury_ai.models.decision_snapshot.DecisionSnapshot' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.post_decision_evaluation_engine' imports 'mercury_ai.models.decision_snapshot.DecisionSnapshot' which does not exist

**import:** mercury_ai.models.decision_snapshot.DecisionSnapshot

#### FAIL: mercury_ai.analysis.post_decision_evaluation_engine

**Message:** Broken import: 'mercury_ai.models.performance_metrics.PerformanceMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.post_decision_evaluation_engine' imports 'mercury_ai.models.performance_metrics.PerformanceMetrics' which does not exist

**import:** mercury_ai.models.performance_metrics.PerformanceMetrics

#### FAIL: mercury_ai.analysis.price_action_analyzer

**Message:** Broken import: 'mercury_ai.models.price_action.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.price_action_analyzer' imports 'mercury_ai.models.price_action.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action.PriceActionAnalysis

#### FAIL: mercury_ai.analysis.price_action_engine

**Message:** Broken import: 'mercury_ai.models.price_action_analysis.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.price_action_engine' imports 'mercury_ai.models.price_action_analysis.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action_analysis.PriceActionAnalysis

#### FAIL: mercury_ai.analysis.price_action_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.price_action_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.price_action_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.price_action_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.MercuryDataProvider

#### FAIL: mercury_ai.analysis.provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.IMercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.IMercuryDataProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.IMercuryDataProvider

#### FAIL: mercury_ai.analysis.ranking_engine

**Message:** Broken import: 'mercury_ai.models.analysis_result.AnalysisResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.ranking_engine' imports 'mercury_ai.models.analysis_result.AnalysisResult' which does not exist

**import:** mercury_ai.models.analysis_result.AnalysisResult

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.replay_cache.ReplayCache' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.analysis.replay_cache.ReplayCache' which does not exist

**import:** mercury_ai.analysis.replay_cache.ReplayCache

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine' which does not exist

**import:** mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: mercury_ai.analysis.replay_batch_processor

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' which does not exist

**import:** mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.config.risk.VAR_CONFIDENCE_95' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.config.risk.VAR_CONFIDENCE_95' which does not exist

**import:** mercury_ai.config.risk.VAR_CONFIDENCE_95

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.config.risk.VAR_CONFIDENCE_99' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.config.risk.VAR_CONFIDENCE_99' which does not exist

**import:** mercury_ai.config.risk.VAR_CONFIDENCE_99

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE' which does not exist

**import:** mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF' which does not exist

**import:** mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.config.risk.KELLY_MAX_FRACTION' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.config.risk.KELLY_MAX_FRACTION' which does not exist

**import:** mercury_ai.config.risk.KELLY_MAX_FRACTION

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.config.risk.STRESS_SCENARIOS' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.config.risk.STRESS_SCENARIOS' which does not exist

**import:** mercury_ai.config.risk.STRESS_SCENARIOS

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.price_action.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.price_action.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action.PriceActionAnalysis

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_profile.LiquidityProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.liquidity_profile.LiquidityProfile' which does not exist

**import:** mercury_ai.models.liquidity_profile.LiquidityProfile

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.analysis.risk_engine

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.risk_engine' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.analysis.session_engine

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.session_engine' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.analysis.session_engine

**Message:** Broken import: 'mercury_ai.models.session_analysis.SessionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.session_engine' imports 'mercury_ai.models.session_analysis.SessionAnalysis' which does not exist

**import:** mercury_ai.models.session_analysis.SessionAnalysis

#### FAIL: mercury_ai.analysis.session_engine

**Message:** Broken import: 'mercury_ai.config.sessions' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.session_engine' imports 'mercury_ai.config.sessions' which does not exist

**import:** mercury_ai.config.sessions

#### FAIL: mercury_ai.analysis.statistical_auditor

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.statistical_auditor' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.analysis.support_resistance_analyzer

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.support_resistance_analyzer' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.analysis.swing_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.swing_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.swing_engine

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.swing_engine' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: mercury_ai.analysis.swing_engine

**Message:** Broken import: 'mercury_ai.models.swing_analysis.SwingSequenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.swing_engine' imports 'mercury_ai.models.swing_analysis.SwingSequenceResult' which does not exist

**import:** mercury_ai.models.swing_analysis.SwingSequenceResult

#### FAIL: mercury_ai.analysis.trade_memory_engine

**Message:** Broken import: 'mercury_ai.models.trade_memory.TradeMemory' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.trade_memory_engine' imports 'mercury_ai.models.trade_memory.TradeMemory' which does not exist

**import:** mercury_ai.models.trade_memory.TradeMemory

#### FAIL: mercury_ai.analysis.trend_analyzer

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.trend_analyzer' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.trend_analyzer

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.trend_analyzer' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.validation_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.validation_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.validation_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.validation_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.validation_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.validation_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.volatility_engine

**Message:** Broken import: 'mercury_ai.models.volatility_analysis.VolatilityAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volatility_engine' imports 'mercury_ai.models.volatility_analysis.VolatilityAnalysis' which does not exist

**import:** mercury_ai.models.volatility_analysis.VolatilityAnalysis

#### FAIL: mercury_ai.analysis.volatility_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volatility_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.volatility_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volatility_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.volume_engine

**Message:** Broken import: 'mercury_ai.models.volume_analysis.VolumeAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volume_engine' imports 'mercury_ai.models.volume_analysis.VolumeAnalysis' which does not exist

**import:** mercury_ai.models.volume_analysis.VolumeAnalysis

#### FAIL: mercury_ai.analysis.volume_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volume_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.volume_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volume_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.volume_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volume_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.volume_intelligence_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volume_intelligence_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.volume_intelligence_engine

**Message:** Broken import: 'mercury_ai.models.volume_profile.VolumeProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.volume_intelligence_engine' imports 'mercury_ai.models.volume_profile.VolumeProfile' which does not exist

**import:** mercury_ai.models.volume_profile.VolumeProfile

#### FAIL: mercury_ai.analysis.vwap_engine

**Message:** Broken import: 'mercury_ai.models.vwap_analysis.VWAPAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.vwap_engine' imports 'mercury_ai.models.vwap_analysis.VWAPAnalysis' which does not exist

**import:** mercury_ai.models.vwap_analysis.VWAPAnalysis

#### FAIL: mercury_ai.analysis.vwap_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.vwap_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.vwap_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.vwap_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.vwap_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.vwap_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.weight_simulator

**Message:** Broken import: 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.weight_simulator' imports 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' which does not exist

**import:** mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor

#### FAIL: mercury_ai.analysis.smart_money.bos_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.bos_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.analysis.smart_money.choch_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.choch_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_analysis.LiquidityAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.models.liquidity_analysis.LiquidityAnalysis' which does not exist

**import:** mercury_ai.models.liquidity_analysis.LiquidityAnalysis

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_result.LiquidityResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.models.liquidity_result.LiquidityResult' which does not exist

**import:** mercury_ai.models.liquidity_result.LiquidityResult

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_analysis.LiquidityAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' imports 'mercury_ai.models.liquidity_analysis.LiquidityAnalysis' which does not exist

**import:** mercury_ai.models.liquidity_analysis.LiquidityAnalysis

#### FAIL: mercury_ai.analysis.smart_money.liquidity_event_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_event_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.smart_money.liquidity_event_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_event_enum.LiquidityEventType' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_event_engine' imports 'mercury_ai.models.liquidity_event_enum.LiquidityEventType' which does not exist

**import:** mercury_ai.models.liquidity_event_enum.LiquidityEventType

#### FAIL: mercury_ai.analysis.smart_money.market_structure_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.market_structure_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.market_structure_engine.MarketStructureEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.analysis.smart_money.market_structure_engine.MarketStructureEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.market_structure_engine.MarketStructureEngine

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.bos_engine.BOSEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.analysis.smart_money.bos_engine.BOSEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.bos_engine.BOSEngine

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.choch_engine.CHOCHEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.analysis.smart_money.choch_engine.CHOCHEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.choch_engine.CHOCHEngine

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine' which does not exist

**import:** mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighMetrics' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.EqualHighMetrics

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighScore' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighScore' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.EqualHighScore

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_stress

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_stress' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: mercury_ai.analysis.smart_money.tests.test_liquidity_stress

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_stress' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.benchmark_framework.MercuryBenchmarkFramework' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_benchmark_framework' imports 'mercury_ai.analysis.benchmark_framework.MercuryBenchmarkFramework' which does not exist

**import:** mercury_ai.analysis.benchmark_framework.MercuryBenchmarkFramework

#### FAIL: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.benchmark_framework.EnhancedBenchmarkReport' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_benchmark_framework' imports 'mercury_ai.analysis.benchmark_framework.EnhancedBenchmarkReport' which does not exist

**import:** mercury_ai.analysis.benchmark_framework.EnhancedBenchmarkReport

#### FAIL: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.benchmark_framework.StatisticalTestResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_benchmark_framework' imports 'mercury_ai.analysis.benchmark_framework.StatisticalTestResult' which does not exist

**import:** mercury_ai.analysis.benchmark_framework.StatisticalTestResult

#### FAIL: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** Broken import: 'mercury_ai.analysis.benchmark_framework.BuyAndHoldBaseline' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_benchmark_framework' imports 'mercury_ai.analysis.benchmark_framework.BuyAndHoldBaseline' which does not exist

**import:** mercury_ai.analysis.benchmark_framework.BuyAndHoldBaseline

#### FAIL: mercury_ai.analysis.tests.test_candlestick_engine

**Message:** Broken import: 'mercury_ai.analysis.candlestick_engine.CandlestickEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_candlestick_engine' imports 'mercury_ai.analysis.candlestick_engine.CandlestickEngine' which does not exist

**import:** mercury_ai.analysis.candlestick_engine.CandlestickEngine

#### FAIL: mercury_ai.analysis.tests.test_candlestick_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_candlestick_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.tests.test_candlestick_engine

**Message:** Broken import: 'mercury_ai.models.market_condition.MarketCondition' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_candlestick_engine' imports 'mercury_ai.models.market_condition.MarketCondition' which does not exist

**import:** mercury_ai.models.market_condition.MarketCondition

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.analysis.context_engine.ContextEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.analysis.context_engine.ContextEngine' which does not exist

**import:** mercury_ai.analysis.context_engine.ContextEngine

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.price_action.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.price_action.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action.PriceActionAnalysis

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_profile.LiquidityProfile' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.liquidity_profile.LiquidityProfile' which does not exist

**import:** mercury_ai.models.liquidity_profile.LiquidityProfile

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.analysis.tests.test_context_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_context_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.analysis.tests.test_fvg_engine

**Message:** Broken import: 'mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_fvg_engine' imports 'mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine' which does not exist

**import:** mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine

#### FAIL: mercury_ai.analysis.tests.test_fvg_engine

**Message:** Broken import: 'mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_fvg_engine' imports 'mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis' which does not exist

**import:** mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis

#### FAIL: mercury_ai.analysis.tests.test_fvg_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_fvg_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_historical_replay_engine' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Broken import: 'mercury_ai.analysis.replay_cache.ReplayCache' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_historical_replay_engine' imports 'mercury_ai.analysis.replay_cache.ReplayCache' which does not exist

**import:** mercury_ai.analysis.replay_cache.ReplayCache

#### FAIL: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_historical_replay_engine' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: mercury_ai.analysis.tests.test_market_regime_engine

**Message:** Broken import: 'mercury_ai.analysis.market_regime_engine.MarketRegimeEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_market_regime_engine' imports 'mercury_ai.analysis.market_regime_engine.MarketRegimeEngine' which does not exist

**import:** mercury_ai.analysis.market_regime_engine.MarketRegimeEngine

#### FAIL: mercury_ai.analysis.tests.test_market_regime_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_market_regime_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.analysis.tests.test_market_structure_engine

**Message:** Broken import: 'mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_market_structure_engine' imports 'mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine' which does not exist

**import:** mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine

#### FAIL: mercury_ai.analysis.tests.test_market_structure_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_market_structure_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.tests.test_momentum_engine

**Message:** Broken import: 'mercury_ai.analysis.momentum_engine.MomentumEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_momentum_engine' imports 'mercury_ai.analysis.momentum_engine.MomentumEngine' which does not exist

**import:** mercury_ai.analysis.momentum_engine.MomentumEngine

#### FAIL: mercury_ai.analysis.tests.test_momentum_engine

**Message:** Broken import: 'mercury_ai.models.momentum_analysis.MomentumAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_momentum_engine' imports 'mercury_ai.models.momentum_analysis.MomentumAnalysis' which does not exist

**import:** mercury_ai.models.momentum_analysis.MomentumAnalysis

#### FAIL: mercury_ai.analysis.tests.test_momentum_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_momentum_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.tests.test_price_action_engine

**Message:** Broken import: 'mercury_ai.analysis.price_action_engine.PriceActionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_price_action_engine' imports 'mercury_ai.analysis.price_action_engine.PriceActionEngine' which does not exist

**import:** mercury_ai.analysis.price_action_engine.PriceActionEngine

#### FAIL: mercury_ai.analysis.tests.test_price_action_engine

**Message:** Broken import: 'mercury_ai.models.price_action_analysis.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_price_action_engine' imports 'mercury_ai.models.price_action_analysis.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action_analysis.PriceActionAnalysis

#### FAIL: mercury_ai.analysis.tests.test_price_action_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_price_action_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' imports 'mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor' which does not exist

**import:** mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor

#### FAIL: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.replay_batch_processor.BatchReplayResult' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' imports 'mercury_ai.analysis.replay_batch_processor.BatchReplayResult' which does not exist

**import:** mercury_ai.analysis.replay_batch_processor.BatchReplayResult

#### FAIL: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Broken import: 'mercury_ai.analysis.replay_batch_processor.BatchReplayReport' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' imports 'mercury_ai.analysis.replay_batch_processor.BatchReplayReport' which does not exist

**import:** mercury_ai.analysis.replay_batch_processor.BatchReplayReport

#### FAIL: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: mercury_ai.analysis.tests.test_replay_cache

**Message:** Broken import: 'mercury_ai.analysis.replay_cache.ReplayCache' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_cache' imports 'mercury_ai.analysis.replay_cache.ReplayCache' which does not exist

**import:** mercury_ai.analysis.replay_cache.ReplayCache

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.analysis.risk_engine.RiskEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.analysis.risk_engine.RiskEngine' which does not exist

**import:** mercury_ai.analysis.risk_engine.RiskEngine

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.tests.test_risk_engine

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.analysis.tests.test_trend_engine

**Message:** Broken import: 'mercury_ai.analysis.trend_analyzer.TrendAnalyzer' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_trend_engine' imports 'mercury_ai.analysis.trend_analyzer.TrendAnalyzer' which does not exist

**import:** mercury_ai.analysis.trend_analyzer.TrendAnalyzer

#### FAIL: mercury_ai.analysis.tests.test_trend_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_trend_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.analysis.tests.test_trend_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_trend_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.analysis.tests.test_volume_engine

**Message:** Broken import: 'mercury_ai.analysis.volume_engine.VolumeEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_volume_engine' imports 'mercury_ai.analysis.volume_engine.VolumeEngine' which does not exist

**import:** mercury_ai.analysis.volume_engine.VolumeEngine

#### FAIL: mercury_ai.analysis.tests.test_volume_engine

**Message:** Broken import: 'mercury_ai.models.volume_analysis.VolumeAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_volume_engine' imports 'mercury_ai.models.volume_analysis.VolumeAnalysis' which does not exist

**import:** mercury_ai.models.volume_analysis.VolumeAnalysis

#### FAIL: mercury_ai.analysis.tests.test_volume_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_volume_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.analysis.tests.test_vwap_engine

**Message:** Broken import: 'mercury_ai.analysis.vwap_engine.VWAPEngine' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_vwap_engine' imports 'mercury_ai.analysis.vwap_engine.VWAPEngine' which does not exist

**import:** mercury_ai.analysis.vwap_engine.VWAPEngine

#### FAIL: mercury_ai.analysis.tests.test_vwap_engine

**Message:** Broken import: 'mercury_ai.models.vwap_analysis.VWAPAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_vwap_engine' imports 'mercury_ai.models.vwap_analysis.VWAPAnalysis' which does not exist

**import:** mercury_ai.models.vwap_analysis.VWAPAnalysis

#### FAIL: mercury_ai.analysis.tests.test_vwap_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.analysis.tests.test_vwap_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.brain.explainability_engine

**Message:** Broken import: 'mercury_ai.models.analysis_result.AnalysisResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.explainability_engine' imports 'mercury_ai.models.analysis_result.AnalysisResult' which does not exist

**import:** mercury_ai.models.analysis_result.AnalysisResult

#### FAIL: mercury_ai.brain.explainability_engine

**Message:** Broken import: 'mercury_ai.models.direction.AnalysisDirection' not found in codebase

**Evidence:** Module 'mercury_ai.brain.explainability_engine' imports 'mercury_ai.models.direction.AnalysisDirection' which does not exist

**import:** mercury_ai.models.direction.AnalysisDirection

#### FAIL: mercury_ai.brain.explainability_engine

**Message:** Broken import: 'mercury_ai.models.confluence_result.ConfluenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.explainability_engine' imports 'mercury_ai.models.confluence_result.ConfluenceResult' which does not exist

**import:** mercury_ai.models.confluence_result.ConfluenceResult

#### FAIL: mercury_ai.brain.explainability_engine

**Message:** Broken import: 'mercury_ai.models.probability_result.ProbabilityResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.explainability_engine' imports 'mercury_ai.models.probability_result.ProbabilityResult' which does not exist

**import:** mercury_ai.models.probability_result.ProbabilityResult

#### FAIL: mercury_ai.brain.explainability_engine

**Message:** Broken import: 'mercury_ai.models.trading_explanation.TradingExplanation' not found in codebase

**Evidence:** Module 'mercury_ai.brain.explainability_engine' imports 'mercury_ai.models.trading_explanation.TradingExplanation' which does not exist

**import:** mercury_ai.models.trading_explanation.TradingExplanation

#### FAIL: mercury_ai.brain.institutional_brain

**Message:** Broken import: 'mercury_ai.models.analysis_result.AnalysisResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.institutional_brain' imports 'mercury_ai.models.analysis_result.AnalysisResult' which does not exist

**import:** mercury_ai.models.analysis_result.AnalysisResult

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.confidence_result.ConfidenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.models.confidence_result.ConfidenceResult' which does not exist

**import:** mercury_ai.models.confidence_result.ConfidenceResult

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.trade_filter_result.TradeFilterResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.models.trade_filter_result.TradeFilterResult' which does not exist

**import:** mercury_ai.models.trade_filter_result.TradeFilterResult

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.validation_engine.ValidationEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.validation_engine.ValidationEngine' which does not exist

**import:** mercury_ai.analysis.validation_engine.ValidationEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' which does not exist

**import:** mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine' which does not exist

**import:** mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' which does not exist

**import:** mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' which does not exist

**import:** mercury_ai.analysis.confidence_engine.ConfidenceEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_engine.ConfluenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.confluence_engine.ConfluenceEngine' which does not exist

**import:** mercury_ai.analysis.confluence_engine.ConfluenceEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine' which does not exist

**import:** mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.narrative_engine.NarrativeEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.narrative_engine.NarrativeEngine' which does not exist

**import:** mercury_ai.analysis.narrative_engine.NarrativeEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.institutional_score_engine.InstitutionalScoreEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.institutional_score_engine.InstitutionalScoreEngine' which does not exist

**import:** mercury_ai.analysis.institutional_score_engine.InstitutionalScoreEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine' which does not exist

**import:** mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.decision_result_builder.DecisionResultBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.decision_result_builder.DecisionResultBuilder' which does not exist

**import:** mercury_ai.analysis.decision_result_builder.DecisionResultBuilder

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder' which does not exist

**import:** mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.risk_engine.RiskEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.risk_engine.RiskEngine' which does not exist

**import:** mercury_ai.analysis.risk_engine.RiskEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.market_state_engine.MarketStateEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.market_state_engine.MarketStateEngine' which does not exist

**import:** mercury_ai.analysis.market_state_engine.MarketStateEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine' which does not exist

**import:** mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.analysis.decision_explainability.DecisionExplainability' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.analysis.decision_explainability.DecisionExplainability' which does not exist

**import:** mercury_ai.analysis.decision_explainability.DecisionExplainability

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.brain.probability_engine.ProbabilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.brain.probability_engine.ProbabilityEngine' which does not exist

**import:** mercury_ai.brain.probability_engine.ProbabilityEngine

#### FAIL: mercury_ai.brain.mercury_decision_engine

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' not found in codebase

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED

#### FAIL: mercury_ai.brain.probability_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.brain.probability_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.brain.probability_engine

**Message:** Broken import: 'mercury_ai.models.probability_result.ProbabilityResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.probability_engine' imports 'mercury_ai.models.probability_result.ProbabilityResult' which does not exist

**import:** mercury_ai.models.probability_result.ProbabilityResult

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.config.configuration_center.MercuryConfigCenter' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.config.configuration_center.MercuryConfigCenter' which does not exist

**import:** mercury_ai.config.configuration_center.MercuryConfigCenter

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.analysis.ranking_engine.RankingEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.analysis.ranking_engine.RankingEngine' which does not exist

**import:** mercury_ai.analysis.ranking_engine.RankingEngine

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.brain.institutional_brain.InstitutionalBrain' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.brain.institutional_brain.InstitutionalBrain' which does not exist

**import:** mercury_ai.brain.institutional_brain.InstitutionalBrain

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.brain.scanner

**Message:** Broken import: 'mercury_ai.analysis.notification_center.NotificationCenter' not found in codebase

**Evidence:** Module 'mercury_ai.brain.scanner' imports 'mercury_ai.analysis.notification_center.NotificationCenter' which does not exist

**import:** mercury_ai.analysis.notification_center.NotificationCenter

#### FAIL: mercury_ai.brain.tests.test_explainability_engine

**Message:** Broken import: 'mercury_ai.brain.explainability_engine.ExplainabilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_explainability_engine' imports 'mercury_ai.brain.explainability_engine.ExplainabilityEngine' which does not exist

**import:** mercury_ai.brain.explainability_engine.ExplainabilityEngine

#### FAIL: mercury_ai.brain.tests.test_explainability_engine

**Message:** Broken import: 'mercury_ai.models.direction.AnalysisDirection' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_explainability_engine' imports 'mercury_ai.models.direction.AnalysisDirection' which does not exist

**import:** mercury_ai.models.direction.AnalysisDirection

#### FAIL: mercury_ai.brain.tests.test_explainability_engine

**Message:** Broken import: 'mercury_ai.models.confluence_result.ConfluenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_explainability_engine' imports 'mercury_ai.models.confluence_result.ConfluenceResult' which does not exist

**import:** mercury_ai.models.confluence_result.ConfluenceResult

#### FAIL: mercury_ai.brain.tests.test_explainability_engine

**Message:** Broken import: 'mercury_ai.models.probability_result.ProbabilityResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_explainability_engine' imports 'mercury_ai.models.probability_result.ProbabilityResult' which does not exist

**import:** mercury_ai.models.probability_result.ProbabilityResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' which does not exist

**import:** mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.confidence_result.ConfidenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.confidence_result.ConfidenceResult' which does not exist

**import:** mercury_ai.models.confidence_result.ConfidenceResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.data_quality_result.DataQualityResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.data_quality_result.DataQualityResult' which does not exist

**import:** mercury_ai.models.data_quality_result.DataQualityResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.models.trade_filter_result.TradeFilterResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.models.trade_filter_result.TradeFilterResult' which does not exist

**import:** mercury_ai.models.trade_filter_result.TradeFilterResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' which does not exist

**import:** mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.confidence_result.ConfidenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.confidence_result.ConfidenceResult' which does not exist

**import:** mercury_ai.models.confidence_result.ConfidenceResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.probability_result.ProbabilityResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.probability_result.ProbabilityResult' which does not exist

**import:** mercury_ai.models.probability_result.ProbabilityResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.trading_explanation.TradingExplanation' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.trading_explanation.TradingExplanation' which does not exist

**import:** mercury_ai.models.trading_explanation.TradingExplanation

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.trade_filter_result.TradeFilterResult' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.trade_filter_result.TradeFilterResult' which does not exist

**import:** mercury_ai.models.trade_filter_result.TradeFilterResult

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.price_action.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.price_action.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action.PriceActionAnalysis

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.liquidity_profile.LiquidityProfile' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.liquidity_profile.LiquidityProfile' which does not exist

**import:** mercury_ai.models.liquidity_profile.LiquidityProfile

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.brain.tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.brain.probability_engine.ProbabilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_probability_engine' imports 'mercury_ai.brain.probability_engine.ProbabilityEngine' which does not exist

**import:** mercury_ai.brain.probability_engine.ProbabilityEngine

#### FAIL: mercury_ai.brain.tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_probability_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.brain.tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_probability_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.brain.tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.brain.tests.test_probability_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.calendar.tests.test_economic_calendar

**Message:** Broken import: 'mercury_ai.calendar.economic_calendar.EconomicCalendar' not found in codebase

**Evidence:** Module 'mercury_ai.calendar.tests.test_economic_calendar' imports 'mercury_ai.calendar.economic_calendar.EconomicCalendar' which does not exist

**import:** mercury_ai.calendar.economic_calendar.EconomicCalendar

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.OPERATIONAL_UNIVERSE' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.OPERATIONAL_UNIVERSE' which does not exist

**import:** mercury_ai.config.universe.OPERATIONAL_UNIVERSE

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.FOREX_UNIVERSE' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.FOREX_UNIVERSE' which does not exist

**import:** mercury_ai.config.universe.FOREX_UNIVERSE

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.CRYPTO_UNIVERSE' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.CRYPTO_UNIVERSE' which does not exist

**import:** mercury_ai.config.universe.CRYPTO_UNIVERSE

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.STOCK_UNIVERSE' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.STOCK_UNIVERSE' which does not exist

**import:** mercury_ai.config.universe.STOCK_UNIVERSE

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.COMMODITY_UNIVERSE' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.COMMODITY_UNIVERSE' which does not exist

**import:** mercury_ai.config.universe.COMMODITY_UNIVERSE

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.FOREX_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.FOREX_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.FOREX_SYMBOLS

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.CRYPTO_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.CRYPTO_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.CRYPTO_SYMBOLS

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.STOCK_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.STOCK_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.STOCK_SYMBOLS

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.COMMODITY_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.COMMODITY_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.COMMODITY_SYMBOLS

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.ALL_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.ALL_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.SUPPORTED_ASSETS' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.SUPPORTED_ASSETS' which does not exist

**import:** mercury_ai.config.universe.SUPPORTED_ASSETS

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.get_asset' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.get_asset' which does not exist

**import:** mercury_ai.config.universe.get_asset

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.get_enabled_symbols' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.get_enabled_symbols' which does not exist

**import:** mercury_ai.config.universe.get_enabled_symbols

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.get_all_provider_symbols' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.get_all_provider_symbols' which does not exist

**import:** mercury_ai.config.universe.get_all_provider_symbols

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.validate_symbol' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.validate_symbol' which does not exist

**import:** mercury_ai.config.universe.validate_symbol

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.universe_summary' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.universe_summary' which does not exist

**import:** mercury_ai.config.universe.universe_summary

#### FAIL: mercury_ai.config.assets

**Message:** Broken import: 'mercury_ai.config.universe.UniverseAsset' not found in codebase

**Evidence:** Module 'mercury_ai.config.assets' imports 'mercury_ai.config.universe.UniverseAsset' which does not exist

**import:** mercury_ai.config.universe.UniverseAsset

#### FAIL: mercury_ai.config.configuration_center

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'mercury_ai.config.configuration_center' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: mercury_ai.config.__init__

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' not found in codebase

**Evidence:** Module 'mercury_ai.config.__init__' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS

#### FAIL: mercury_ai.config.__init__

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' not found in codebase

**Evidence:** Module 'mercury_ai.config.__init__' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED

#### FAIL: mercury_ai.config.__init__

**Message:** Broken import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' not found in codebase

**Evidence:** Module 'mercury_ai.config.__init__' imports 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' which does not exist

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.data.data_quality_engine.DataQualityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.data.data_quality_engine.DataQualityEngine' which does not exist

**import:** mercury_ai.data.data_quality_engine.DataQualityEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.providers.base_provider.MarketDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.providers.base_provider.MarketDataProvider' which does not exist

**import:** mercury_ai.providers.base_provider.MarketDataProvider

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.data.indicator_engine.IndicatorEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.data.indicator_engine.IndicatorEngine' which does not exist

**import:** mercury_ai.data.indicator_engine.IndicatorEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.core.exceptions.MarketClosedException' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.core.exceptions.MarketClosedException' which does not exist

**import:** mercury_ai.core.exceptions.MarketClosedException

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.models.analysis_result.AnalysisResult' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.models.analysis_result.AnalysisResult' which does not exist

**import:** mercury_ai.models.analysis_result.AnalysisResult

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.models.decision_snapshot.DecisionSnapshot' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.models.decision_snapshot.DecisionSnapshot' which does not exist

**import:** mercury_ai.models.decision_snapshot.DecisionSnapshot

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.models.version_metadata.VersionMetadata' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.models.version_metadata.VersionMetadata' which does not exist

**import:** mercury_ai.models.version_metadata.VersionMetadata

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.context_engine.ContextEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.context_engine.ContextEngine' which does not exist

**import:** mercury_ai.analysis.context_engine.ContextEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine' which does not exist

**import:** mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine' which does not exist

**import:** mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger' which does not exist

**import:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.core.pipeline_executor.PipelineExecutor' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.core.pipeline_executor.PipelineExecutor' which does not exist

**import:** mercury_ai.core.pipeline_executor.PipelineExecutor

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.market_context_builder.MarketContextBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.market_context_builder.MarketContextBuilder' which does not exist

**import:** mercury_ai.analysis.market_context_builder.MarketContextBuilder

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.smart_money.smart_money_engine.SmartMoneyEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.smart_money.smart_money_engine.SmartMoneyEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.smart_money_engine.SmartMoneyEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.trend_analyzer.TrendAnalyzer' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.trend_analyzer.TrendAnalyzer' which does not exist

**import:** mercury_ai.analysis.trend_analyzer.TrendAnalyzer

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.market_condition_engine.MarketConditionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.market_condition_engine.MarketConditionEngine' which does not exist

**import:** mercury_ai.analysis.market_condition_engine.MarketConditionEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.market_regime_engine.MarketRegimeEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.market_regime_engine.MarketRegimeEngine' which does not exist

**import:** mercury_ai.analysis.market_regime_engine.MarketRegimeEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.mtf_engine.MTFEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.mtf_engine.MTFEngine' which does not exist

**import:** mercury_ai.analysis.mtf_engine.MTFEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.candlestick_engine.CandlestickEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.candlestick_engine.CandlestickEngine' which does not exist

**import:** mercury_ai.analysis.candlestick_engine.CandlestickEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.volatility_engine.VolatilityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.volatility_engine.VolatilityEngine' which does not exist

**import:** mercury_ai.analysis.volatility_engine.VolatilityEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.session_engine.SessionEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.session_engine.SessionEngine' which does not exist

**import:** mercury_ai.analysis.session_engine.SessionEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.support_resistance_analyzer.SupportResistanceAnalyzer' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.support_resistance_analyzer.SupportResistanceAnalyzer' which does not exist

**import:** mercury_ai.analysis.support_resistance_analyzer.SupportResistanceAnalyzer

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.risk_engine.RiskEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.risk_engine.RiskEngine' which does not exist

**import:** mercury_ai.analysis.risk_engine.RiskEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.market_state_engine.MarketStateEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.market_state_engine.MarketStateEngine' which does not exist

**import:** mercury_ai.analysis.market_state_engine.MarketStateEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine' which does not exist

**import:** mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' which does not exist

**import:** mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.evidence_engine.EvidenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.evidence_engine.EvidenceEngine' which does not exist

**import:** mercury_ai.analysis.evidence_engine.EvidenceEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.context_intelligence_engine.ContextIntelligenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.context_intelligence_engine.ContextIntelligenceEngine' which does not exist

**import:** mercury_ai.analysis.context_intelligence_engine.ContextIntelligenceEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.volume_intelligence_engine.VolumeIntelligenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.volume_intelligence_engine.VolumeIntelligenceEngine' which does not exist

**import:** mercury_ai.analysis.volume_intelligence_engine.VolumeIntelligenceEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine' which does not exist

**import:** mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' which does not exist

**import:** mercury_ai.config.timeframes.DEFAULT_TIMEFRAME

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.institutional_trade_filter_engine.InstitutionalTradeFilterEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.institutional_trade_filter_engine.InstitutionalTradeFilterEngine' which does not exist

**import:** mercury_ai.analysis.institutional_trade_filter_engine.InstitutionalTradeFilterEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.confluence_engine.ConfluenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.confluence_engine.ConfluenceEngine' which does not exist

**import:** mercury_ai.analysis.confluence_engine.ConfluenceEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' which does not exist

**import:** mercury_ai.analysis.confidence_engine.ConfidenceEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine' which does not exist

**import:** mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder' which does not exist

**import:** mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.price_action_analyzer.PriceActionAnalyzer' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.price_action_analyzer.PriceActionAnalyzer' which does not exist

**import:** mercury_ai.analysis.price_action_analyzer.PriceActionAnalyzer

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine' which does not exist

**import:** mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.core.runtime_report.RuntimeReport' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.core.runtime_report.RuntimeReport' which does not exist

**import:** mercury_ai.core.runtime_report.RuntimeReport

#### FAIL: mercury_ai.core.analysis_pipeline

**Message:** Broken import: 'mercury_ai.core.runtime_report.TelemetryData' not found in codebase

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' imports 'mercury_ai.core.runtime_report.TelemetryData' which does not exist

**import:** mercury_ai.core.runtime_report.TelemetryData

#### FAIL: mercury_ai.core.auto_health

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.core.auto_health' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: mercury_ai.core.auto_health

**Message:** Broken import: 'mercury_ai.core.health_center.HealthCenter' not found in codebase

**Evidence:** Module 'mercury_ai.core.auto_health' imports 'mercury_ai.core.health_center.HealthCenter' which does not exist

**import:** mercury_ai.core.health_center.HealthCenter

#### FAIL: mercury_ai.core.auto_health

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'mercury_ai.core.auto_health' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: mercury_ai.core.export_center

**Message:** Broken import: 'mercury_ai.analysis.data_exporter.DataExporter' not found in codebase

**Evidence:** Module 'mercury_ai.core.export_center' imports 'mercury_ai.analysis.data_exporter.DataExporter' which does not exist

**import:** mercury_ai.analysis.data_exporter.DataExporter

#### FAIL: mercury_ai.core.health_center

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.core.health_center' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: mercury_ai.core.job_manager

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'mercury_ai.core.job_manager' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: mercury_ai.core.job_manager

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.core.job_manager' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.core.job_manager

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'mercury_ai.core.job_manager' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: mercury_ai.core.job_manager

**Message:** Broken import: 'mercury_ai.config.assets.SUPPORTED_ASSETS' not found in codebase

**Evidence:** Module 'mercury_ai.core.job_manager' imports 'mercury_ai.config.assets.SUPPORTED_ASSETS' which does not exist

**import:** mercury_ai.config.assets.SUPPORTED_ASSETS

#### FAIL: mercury_ai.core.job_manager

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'mercury_ai.core.job_manager' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: mercury_ai.core.job_manager

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'mercury_ai.core.job_manager' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: mercury_ai.core.pipeline_audit_middleware

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_audit_middleware' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.core.pipeline_audit_middleware

**Message:** Broken import: 'mercury_ai.core.audit_sink.AuditSink' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_audit_middleware' imports 'mercury_ai.core.audit_sink.AuditSink' which does not exist

**import:** mercury_ai.core.audit_sink.AuditSink

#### FAIL: mercury_ai.core.pipeline_audit_middleware

**Message:** Broken import: 'mercury_ai.core.audit_sink.AuditEvent' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_audit_middleware' imports 'mercury_ai.core.audit_sink.AuditEvent' which does not exist

**import:** mercury_ai.core.audit_sink.AuditEvent

#### FAIL: mercury_ai.core.pipeline_executor

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_executor' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: mercury_ai.core.pipeline_profiler

**Message:** Broken import: 'mercury_ai.models.profiler_models.StageProfile' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_profiler' imports 'mercury_ai.models.profiler_models.StageProfile' which does not exist

**import:** mercury_ai.models.profiler_models.StageProfile

#### FAIL: mercury_ai.core.pipeline_profiler

**Message:** Broken import: 'mercury_ai.models.profiler_models.PipelineProfile' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_profiler' imports 'mercury_ai.models.profiler_models.PipelineProfile' which does not exist

**import:** mercury_ai.models.profiler_models.PipelineProfile

#### FAIL: mercury_ai.core.pipeline_profiler

**Message:** Broken import: 'mercury_ai.core._stage_builder._StageBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.core.pipeline_profiler' imports 'mercury_ai.core._stage_builder._StageBuilder' which does not exist

**import:** mercury_ai.core._stage_builder._StageBuilder

#### FAIL: mercury_ai.core.security_center

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.core.security_center' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.core.session_manager

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'mercury_ai.core.session_manager' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: mercury_ai.core.session_manager

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.core.session_manager' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.core.startup

**Message:** Broken import: 'mercury_ai.core.banner.show_banner' not found in codebase

**Evidence:** Module 'mercury_ai.core.startup' imports 'mercury_ai.core.banner.show_banner' which does not exist

**import:** mercury_ai.core.banner.show_banner

#### FAIL: mercury_ai.core.startup

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'mercury_ai.core.startup' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: mercury_ai.core.startup

**Message:** Broken import: 'mercury_ai.providers.provider.MarketProvider' not found in codebase

**Evidence:** Module 'mercury_ai.core.startup' imports 'mercury_ai.providers.provider.MarketProvider' which does not exist

**import:** mercury_ai.providers.provider.MarketProvider

#### FAIL: mercury_ai.data.market_data

**Message:** Broken import: 'mercury_ai.core.exceptions.MarketClosedException' not found in codebase

**Evidence:** Module 'mercury_ai.data.market_data' imports 'mercury_ai.core.exceptions.MarketClosedException' which does not exist

**import:** mercury_ai.core.exceptions.MarketClosedException

#### FAIL: mercury_ai.data.market_data

**Message:** Broken import: 'mercury_ai.data.data_normalizer.DataNormalizer' not found in codebase

**Evidence:** Module 'mercury_ai.data.market_data' imports 'mercury_ai.data.data_normalizer.DataNormalizer' which does not exist

**import:** mercury_ai.data.data_normalizer.DataNormalizer

#### FAIL: mercury_ai.database.snapshot_logger

**Message:** Broken import: 'mercury_ai.models.decision_snapshot.DecisionSnapshot' not found in codebase

**Evidence:** Module 'mercury_ai.database.snapshot_logger' imports 'mercury_ai.models.decision_snapshot.DecisionSnapshot' which does not exist

**import:** mercury_ai.models.decision_snapshot.DecisionSnapshot

#### FAIL: mercury_ai.market.market_engine

**Message:** Broken import: 'mercury_ai.providers.market_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.market.market_engine' imports 'mercury_ai.providers.market_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.market_provider.MercuryDataProvider

#### FAIL: mercury_ai.market.market_engine

**Message:** Broken import: 'mercury_ai.config.settings.ASSET' not found in codebase

**Evidence:** Module 'mercury_ai.market.market_engine' imports 'mercury_ai.config.settings.ASSET' which does not exist

**import:** mercury_ai.config.settings.ASSET

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.confluence_result.ConfluenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.confluence_result.ConfluenceResult' which does not exist

**import:** mercury_ai.models.confluence_result.ConfluenceResult

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.market_condition.MarketCondition' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.market_condition.MarketCondition' which does not exist

**import:** mercury_ai.models.market_condition.MarketCondition

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.candlestick_analysis.CandlestickAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.candlestick_analysis.CandlestickAnalysis' which does not exist

**import:** mercury_ai.models.candlestick_analysis.CandlestickAnalysis

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.volatility_analysis.VolatilityAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.volatility_analysis.VolatilityAnalysis' which does not exist

**import:** mercury_ai.models.volatility_analysis.VolatilityAnalysis

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.session_analysis.SessionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.session_analysis.SessionAnalysis' which does not exist

**import:** mercury_ai.models.session_analysis.SessionAnalysis

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.liquidity_result.LiquidityResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.liquidity_result.LiquidityResult' which does not exist

**import:** mercury_ai.models.liquidity_result.LiquidityResult

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.volume_analysis.VolumeAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.volume_analysis.VolumeAnalysis' which does not exist

**import:** mercury_ai.models.volume_analysis.VolumeAnalysis

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: mercury_ai.models.analysis_result

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.analysis_result' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.models.benchmark_report

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.benchmark_report' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.models.benchmark_report

**Message:** Broken import: 'mercury_ai.analysis.metric_calculator.PerformanceMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.models.benchmark_report' imports 'mercury_ai.analysis.metric_calculator.PerformanceMetrics' which does not exist

**import:** mercury_ai.analysis.metric_calculator.PerformanceMetrics

#### FAIL: mercury_ai.models.confluence_result

**Message:** Broken import: 'mercury_ai.models.direction.AnalysisDirection' not found in codebase

**Evidence:** Module 'mercury_ai.models.confluence_result' imports 'mercury_ai.models.direction.AnalysisDirection' which does not exist

**import:** mercury_ai.models.direction.AnalysisDirection

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.models.decision_trace.DecisionTrace' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.models.decision_trace.DecisionTrace' which does not exist

**import:** mercury_ai.models.decision_trace.DecisionTrace

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.models.version_metadata.VersionMetadata' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.models.version_metadata.VersionMetadata' which does not exist

**import:** mercury_ai.models.version_metadata.VersionMetadata

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.models.trading_explanation.TradingExplanation' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.models.trading_explanation.TradingExplanation' which does not exist

**import:** mercury_ai.models.trading_explanation.TradingExplanation

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.models.decision_result

**Message:** Broken import: 'mercury_ai.analysis.decision_explainability.DecisionExplainability' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_result' imports 'mercury_ai.analysis.decision_explainability.DecisionExplainability' which does not exist

**import:** mercury_ai.analysis.decision_explainability.DecisionExplainability

#### FAIL: mercury_ai.models.decision_snapshot

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_snapshot' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: mercury_ai.models.decision_snapshot

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_snapshot' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: mercury_ai.models.decision_snapshot

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_snapshot' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.models.decision_snapshot

**Message:** Broken import: 'mercury_ai.models.version_metadata.VersionMetadata' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_snapshot' imports 'mercury_ai.models.version_metadata.VersionMetadata' which does not exist

**import:** mercury_ai.models.version_metadata.VersionMetadata

#### FAIL: mercury_ai.models.decision_snapshot

**Message:** Broken import: 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_snapshot' imports 'mercury_ai.models.evidence_ranking.EvidenceRankingResult' which does not exist

**import:** mercury_ai.models.evidence_ranking.EvidenceRankingResult

#### FAIL: mercury_ai.models.decision_snapshot

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_snapshot' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: mercury_ai.models.decision_trace

**Message:** Broken import: 'mercury_ai.models.decision_node.DecisionNode' not found in codebase

**Evidence:** Module 'mercury_ai.models.decision_trace' imports 'mercury_ai.models.decision_node.DecisionNode' which does not exist

**import:** mercury_ai.models.decision_node.DecisionNode

#### FAIL: mercury_ai.models.evidence

**Message:** Broken import: 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' not found in codebase

**Evidence:** Module 'mercury_ai.models.evidence' imports 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' which does not exist

**import:** mercury_ai.config.timeframes.DEFAULT_TIMEFRAME

#### FAIL: mercury_ai.models.evidence

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.models.evidence' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.models.evidence_ranking

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.evidence_ranking' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.fair_value_gap_analysis

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.fair_value_gap_analysis' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.liquidity_analysis

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.liquidity_analysis' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.price_action.PriceActionAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.price_action.PriceActionAnalysis' which does not exist

**import:** mercury_ai.models.price_action.PriceActionAnalysis

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.support_resistance.SupportResistanceAnalysis' which does not exist

**import:** mercury_ai.models.support_resistance.SupportResistanceAnalysis

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.smart_money.SmartMoneyAnalysis' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.smart_money.SmartMoneyAnalysis' which does not exist

**import:** mercury_ai.models.smart_money.SmartMoneyAnalysis

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.liquidity_profile.LiquidityProfile' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.liquidity_profile.LiquidityProfile' which does not exist

**import:** mercury_ai.models.liquidity_profile.LiquidityProfile

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: mercury_ai.models.market_context

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_context' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.models.market_evidence_bundle

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_evidence_bundle' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.market_regime

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_regime' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.market_regime

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_regime' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: mercury_ai.models.market_state

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_state' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: mercury_ai.models.market_structure_profile

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_structure_profile' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: mercury_ai.models.market_thesis

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_thesis' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: mercury_ai.models.market_thesis

**Message:** Broken import: 'mercury_ai.models.confidence_result.ConfidenceResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_thesis' imports 'mercury_ai.models.confidence_result.ConfidenceResult' which does not exist

**import:** mercury_ai.models.confidence_result.ConfidenceResult

#### FAIL: mercury_ai.models.market_thesis

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'mercury_ai.models.market_thesis' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: mercury_ai.models.momentum_analysis

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.momentum_analysis' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.signal

**Message:** Broken import: 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' not found in codebase

**Evidence:** Module 'mercury_ai.models.signal' imports 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' which does not exist

**import:** mercury_ai.config.timeframes.DEFAULT_TIMEFRAME

#### FAIL: mercury_ai.models.smart_money

**Message:** Broken import: 'mercury_ai.models.market_structure.MarketStructure' not found in codebase

**Evidence:** Module 'mercury_ai.models.smart_money' imports 'mercury_ai.models.market_structure.MarketStructure' which does not exist

**import:** mercury_ai.models.market_structure.MarketStructure

#### FAIL: mercury_ai.models.stress_test

**Message:** Broken import: 'mercury_ai.models.market_data.MarketData' not found in codebase

**Evidence:** Module 'mercury_ai.models.stress_test' imports 'mercury_ai.models.market_data.MarketData' which does not exist

**import:** mercury_ai.models.market_data.MarketData

#### FAIL: mercury_ai.models.trade_memory

**Message:** Broken import: 'mercury_ai.models.decision_snapshot.DecisionSnapshot' not found in codebase

**Evidence:** Module 'mercury_ai.models.trade_memory' imports 'mercury_ai.models.decision_snapshot.DecisionSnapshot' which does not exist

**import:** mercury_ai.models.decision_snapshot.DecisionSnapshot

#### FAIL: mercury_ai.models.trading_explanation

**Message:** Broken import: 'mercury_ai.models.decision_result.DecisionResult' not found in codebase

**Evidence:** Module 'mercury_ai.models.trading_explanation' imports 'mercury_ai.models.decision_result.DecisionResult' which does not exist

**import:** mercury_ai.models.decision_result.DecisionResult

#### FAIL: mercury_ai.models.volatility_analysis

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.volatility_analysis' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.volume_analysis

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.volume_analysis' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.models.vwap_analysis

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'mercury_ai.models.vwap_analysis' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: mercury_ai.news.tests.test_news_provider

**Message:** Broken import: 'mercury_ai.news.news_provider.NewsProvider' not found in codebase

**Evidence:** Module 'mercury_ai.news.tests.test_news_provider' imports 'mercury_ai.news.news_provider.NewsProvider' which does not exist

**import:** mercury_ai.news.news_provider.NewsProvider

#### FAIL: mercury_ai.operations.demo_manager

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'mercury_ai.operations.demo_manager' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: mercury_ai.operations.demo_manager

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'mercury_ai.operations.demo_manager' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: mercury_ai.operations.demo_manager

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'mercury_ai.operations.demo_manager' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: mercury_ai.operations.demo_manager

**Message:** Broken import: 'mercury_ai.config.assets.SUPPORTED_ASSETS' not found in codebase

**Evidence:** Module 'mercury_ai.operations.demo_manager' imports 'mercury_ai.config.assets.SUPPORTED_ASSETS' which does not exist

**import:** mercury_ai.config.assets.SUPPORTED_ASSETS

#### FAIL: mercury_ai.operations.demo_manager

**Message:** Broken import: 'mercury_ai.utils.deterministic_clock.DeterministicClock' not found in codebase

**Evidence:** Module 'mercury_ai.operations.demo_manager' imports 'mercury_ai.utils.deterministic_clock.DeterministicClock' which does not exist

**import:** mercury_ai.utils.deterministic_clock.DeterministicClock

#### FAIL: mercury_ai.providers.data_adapters

**Message:** Broken import: 'mercury_ai.providers.data_interfaces.IDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.providers.data_adapters' imports 'mercury_ai.providers.data_interfaces.IDataProvider' which does not exist

**import:** mercury_ai.providers.data_interfaces.IDataProvider

#### FAIL: mercury_ai.providers.data_adapters

**Message:** Broken import: 'mercury_ai.config.universe.ALL_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.providers.data_adapters' imports 'mercury_ai.config.universe.ALL_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### FAIL: mercury_ai.providers.data_adapters

**Message:** Broken import: 'mercury_ai.config.universe.FOREX_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.providers.data_adapters' imports 'mercury_ai.config.universe.FOREX_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.FOREX_SYMBOLS

#### FAIL: mercury_ai.providers.data_adapters

**Message:** Broken import: 'mercury_ai.config.universe.CRYPTO_SYMBOLS' not found in codebase

**Evidence:** Module 'mercury_ai.providers.data_adapters' imports 'mercury_ai.config.universe.CRYPTO_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.CRYPTO_SYMBOLS

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_interfaces.IDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_interfaces.IDataProvider' which does not exist

**import:** mercury_ai.providers.data_interfaces.IDataProvider

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_adapters.YahooAdapter' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_adapters.YahooAdapter' which does not exist

**import:** mercury_ai.providers.data_adapters.YahooAdapter

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_adapters.PolygonAdapter' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_adapters.PolygonAdapter' which does not exist

**import:** mercury_ai.providers.data_adapters.PolygonAdapter

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_adapters.TwelveDataAdapter' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_adapters.TwelveDataAdapter' which does not exist

**import:** mercury_ai.providers.data_adapters.TwelveDataAdapter

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_adapters.AlphaVantageAdapter' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_adapters.AlphaVantageAdapter' which does not exist

**import:** mercury_ai.providers.data_adapters.AlphaVantageAdapter

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_adapters.BinanceAdapter' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_adapters.BinanceAdapter' which does not exist

**import:** mercury_ai.providers.data_adapters.BinanceAdapter

#### FAIL: mercury_ai.providers.market_provider

**Message:** Broken import: 'mercury_ai.providers.data_adapters.MetaTrader5Adapter' not found in codebase

**Evidence:** Module 'mercury_ai.providers.market_provider' imports 'mercury_ai.providers.data_adapters.MetaTrader5Adapter' which does not exist

**import:** mercury_ai.providers.data_adapters.MetaTrader5Adapter

#### FAIL: mercury_ai.providers.mercury_data_provider

**Message:** Broken import: 'mercury_ai.providers.market_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.providers.mercury_data_provider' imports 'mercury_ai.providers.market_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.market_provider.MercuryDataProvider

#### FAIL: mercury_ai.providers.yahoo_finance_provider

**Message:** Broken import: 'mercury_ai.core.exceptions.MarketClosedException' not found in codebase

**Evidence:** Module 'mercury_ai.providers.yahoo_finance_provider' imports 'mercury_ai.core.exceptions.MarketClosedException' which does not exist

**import:** mercury_ai.core.exceptions.MarketClosedException

#### FAIL: mercury_ai.providers.tests.test_market_provider

**Message:** Broken import: 'mercury_ai.providers.market_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'mercury_ai.providers.tests.test_market_provider' imports 'mercury_ai.providers.market_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.market_provider.MercuryDataProvider

#### FAIL: mercury_ai.sessions.market_sessions

**Message:** Broken import: 'mercury_ai.config.sessions' not found in codebase

**Evidence:** Module 'mercury_ai.sessions.market_sessions' imports 'mercury_ai.config.sessions' which does not exist

**import:** mercury_ai.config.sessions

#### FAIL: mercury_ai.sessions.tests.test_market_sessions

**Message:** Broken import: 'mercury_ai.sessions.market_sessions.MarketSessions' not found in codebase

**Evidence:** Module 'mercury_ai.sessions.tests.test_market_sessions' imports 'mercury_ai.sessions.market_sessions.MarketSessions' which does not exist

**import:** mercury_ai.sessions.market_sessions.MarketSessions

#### FAIL: mercury_ai.utils.memory_auditor

**Message:** Broken import: 'mercury_ai.models.memory_audit.MemorySnapshot' not found in codebase

**Evidence:** Module 'mercury_ai.utils.memory_auditor' imports 'mercury_ai.models.memory_audit.MemorySnapshot' which does not exist

**import:** mercury_ai.models.memory_audit.MemorySnapshot

#### FAIL: mercury_ai.utils.memory_auditor

**Message:** Broken import: 'mercury_ai.models.memory_audit.MemoryAuditResult' not found in codebase

**Evidence:** Module 'mercury_ai.utils.memory_auditor' imports 'mercury_ai.models.memory_audit.MemoryAuditResult' which does not exist

**import:** mercury_ai.models.memory_audit.MemoryAuditResult

#### FAIL: mercury_ai.utils.performance_collector

**Message:** Broken import: 'mercury_ai.models.performance.StageMetric' not found in codebase

**Evidence:** Module 'mercury_ai.utils.performance_collector' imports 'mercury_ai.models.performance.StageMetric' which does not exist

**import:** mercury_ai.models.performance.StageMetric

#### FAIL: mercury_ai.utils.performance_collector

**Message:** Broken import: 'mercury_ai.models.performance.PipelineMetric' not found in codebase

**Evidence:** Module 'mercury_ai.utils.performance_collector' imports 'mercury_ai.models.performance.PipelineMetric' which does not exist

**import:** mercury_ai.models.performance.PipelineMetric

#### FAIL: mercury_ai.utils.performance_collector

**Message:** Broken import: 'mercury_ai.models.performance.HotspotReport' not found in codebase

**Evidence:** Module 'mercury_ai.utils.performance_collector' imports 'mercury_ai.models.performance.HotspotReport' which does not exist

**import:** mercury_ai.models.performance.HotspotReport

#### FAIL: mercury_ai.utils.performance_collector

**Message:** Broken import: 'mercury_ai.core._stage_builder._StageBuilder' not found in codebase

**Evidence:** Module 'mercury_ai.utils.performance_collector' imports 'mercury_ai.core._stage_builder._StageBuilder' which does not exist

**import:** mercury_ai.core._stage_builder._StageBuilder

#### FAIL: mercury_ai.utils.regression_detector

**Message:** Broken import: 'mercury_ai.models.regression.BenchmarkMetrics' not found in codebase

**Evidence:** Module 'mercury_ai.utils.regression_detector' imports 'mercury_ai.models.regression.BenchmarkMetrics' which does not exist

**import:** mercury_ai.models.regression.BenchmarkMetrics

#### FAIL: mercury_ai.utils.regression_detector

**Message:** Broken import: 'mercury_ai.models.regression.RegressionResult' not found in codebase

**Evidence:** Module 'mercury_ai.utils.regression_detector' imports 'mercury_ai.models.regression.RegressionResult' which does not exist

**import:** mercury_ai.models.regression.RegressionResult

#### FAIL: mercury_ai.utils.stress_tester

**Message:** Broken import: 'mercury_ai.models.stress_test.StressTestResult' not found in codebase

**Evidence:** Module 'mercury_ai.utils.stress_tester' imports 'mercury_ai.models.stress_test.StressTestResult' which does not exist

**import:** mercury_ai.models.stress_test.StressTestResult

#### FAIL: scripts.prepare_replay_data

**Message:** Broken import: 'mercury_ai.config.universe.ALL_SYMBOLS' not found in codebase

**Evidence:** Module 'scripts.prepare_replay_data' imports 'mercury_ai.config.universe.ALL_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### FAIL: scripts.prepare_replay_data

**Message:** Broken import: 'mercury_ai.config.universe.FOREX_SYMBOLS' not found in codebase

**Evidence:** Module 'scripts.prepare_replay_data' imports 'mercury_ai.config.universe.FOREX_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.FOREX_SYMBOLS

#### FAIL: scripts.prepare_replay_data

**Message:** Broken import: 'mercury_ai.config.universe.CRYPTO_SYMBOLS' not found in codebase

**Evidence:** Module 'scripts.prepare_replay_data' imports 'mercury_ai.config.universe.CRYPTO_SYMBOLS' which does not exist

**import:** mercury_ai.config.universe.CRYPTO_SYMBOLS

#### FAIL: scripts.run_replay_3500

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'scripts.run_replay_3500' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: scripts.run_replay_3500

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'scripts.run_replay_3500' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: scripts.run_replay_3500

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'scripts.run_replay_3500' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: scripts.run_replay_3500

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'scripts.run_replay_3500' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: scripts.run_replay_3500

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'scripts.run_replay_3500' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: tests.test_adaptive_weighting

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_adaptive_weighting' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_adaptive_weighting

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'tests.test_adaptive_weighting' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: tests.test_adaptive_weighting

**Message:** Broken import: 'mercury_ai.models.market_regime.MarketRegime' not found in codebase

**Evidence:** Module 'tests.test_adaptive_weighting' imports 'mercury_ai.models.market_regime.MarketRegime' which does not exist

**import:** mercury_ai.models.market_regime.MarketRegime

#### FAIL: tests.test_adaptive_weighting

**Message:** Broken import: 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' not found in codebase

**Evidence:** Module 'tests.test_adaptive_weighting' imports 'mercury_ai.models.market_regime_enum.MarketRegimeEnum' which does not exist

**import:** mercury_ai.models.market_regime_enum.MarketRegimeEnum

#### FAIL: tests.test_adaptive_weighting

**Message:** Broken import: 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' not found in codebase

**Evidence:** Module 'tests.test_adaptive_weighting' imports 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' which does not exist

**import:** mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine

#### FAIL: tests.test_asset_registry

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'tests.test_asset_registry' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: tests.test_asset_registry

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'tests.test_asset_registry' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: tests.test_auto_health

**Message:** Broken import: 'mercury_ai.core.auto_health.MercuryAutoHealth' not found in codebase

**Evidence:** Module 'tests.test_auto_health' imports 'mercury_ai.core.auto_health.MercuryAutoHealth' which does not exist

**import:** mercury_ai.core.auto_health.MercuryAutoHealth

#### FAIL: tests.test_auto_health

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'tests.test_auto_health' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### FAIL: tests.test_auto_health

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'tests.test_auto_health' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: tests.test_benchmark_integration

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' not found in codebase

**Evidence:** Module 'tests.test_benchmark_integration' imports 'mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine

#### FAIL: tests.test_benchmark_integration

**Message:** Broken import: 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup' not found in codebase

**Evidence:** Module 'tests.test_benchmark_integration' imports 'mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup' which does not exist

**import:** mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup

#### FAIL: tests.test_benchmark_integration

**Message:** Broken import: 'mercury_ai.models.swing_analysis.Swing' not found in codebase

**Evidence:** Module 'tests.test_benchmark_integration' imports 'mercury_ai.models.swing_analysis.Swing' which does not exist

**import:** mercury_ai.models.swing_analysis.Swing

#### FAIL: tests.test_benchmark_integration

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'tests.test_benchmark_integration' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: tests.test_benchmark_integration

**Message:** Broken import: 'mercury_ai.core.pipeline_profiler.PipelineProfiler' not found in codebase

**Evidence:** Module 'tests.test_benchmark_integration' imports 'mercury_ai.core.pipeline_profiler.PipelineProfiler' which does not exist

**import:** mercury_ai.core.pipeline_profiler.PipelineProfiler

#### FAIL: tests.test_broker_filtering

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'tests.test_broker_filtering' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: tests.test_broker_filtering

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'tests.test_broker_filtering' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.models.market_state.MarketState' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.models.market_state.MarketState' which does not exist

**import:** mercury_ai.models.market_state.MarketState

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.models.market_state_enum.MarketStateEnum' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.models.market_state_enum.MarketStateEnum' which does not exist

**import:** mercury_ai.models.market_state_enum.MarketStateEnum

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.models.mtf_consensus.MTFConsensus' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.models.mtf_consensus.MTFConsensus' which does not exist

**import:** mercury_ai.models.mtf_consensus.MTFConsensus

#### FAIL: tests.test_confidence_calibration

**Message:** Broken import: 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration' imports 'mercury_ai.analysis.confidence_engine.ConfidenceEngine' which does not exist

**import:** mercury_ai.analysis.confidence_engine.ConfidenceEngine

#### FAIL: tests.test_confidence_calibration_auditor

**Message:** Broken import: 'mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor' not found in codebase

**Evidence:** Module 'tests.test_confidence_calibration_auditor' imports 'mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor' which does not exist

**import:** mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor

#### FAIL: tests.test_configuration_center

**Message:** Broken import: 'mercury_ai.config.configuration_center.MercuryConfigCenter' not found in codebase

**Evidence:** Module 'tests.test_configuration_center' imports 'mercury_ai.config.configuration_center.MercuryConfigCenter' which does not exist

**import:** mercury_ai.config.configuration_center.MercuryConfigCenter

#### FAIL: tests.test_conflict_resolution

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_conflict_resolution' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_conflict_resolution

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'tests.test_conflict_resolution' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: tests.test_conflict_resolution

**Message:** Broken import: 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' not found in codebase

**Evidence:** Module 'tests.test_conflict_resolution' imports 'mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine' which does not exist

**import:** mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine

#### FAIL: tests.test_data_exporter

**Message:** Broken import: 'mercury_ai.analysis.data_exporter.DataExporter' not found in codebase

**Evidence:** Module 'tests.test_data_exporter' imports 'mercury_ai.analysis.data_exporter.DataExporter' which does not exist

**import:** mercury_ai.analysis.data_exporter.DataExporter

#### FAIL: tests.test_data_provider_manager

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'tests.test_data_provider_manager' imports 'mercury_ai.data.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.MercuryDataProvider

#### FAIL: tests.test_data_provider_manager

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.YahooProvider' not found in codebase

**Evidence:** Module 'tests.test_data_provider_manager' imports 'mercury_ai.data.mercury_data_provider.YahooProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.YahooProvider

#### FAIL: tests.test_data_provider_manager

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.BinanceProvider' not found in codebase

**Evidence:** Module 'tests.test_data_provider_manager' imports 'mercury_ai.data.mercury_data_provider.BinanceProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.BinanceProvider

#### FAIL: tests.test_data_quality_engine

**Message:** Broken import: 'mercury_ai.analysis.data_quality_engine.DataQualityEngine' not found in codebase

**Evidence:** Module 'tests.test_data_quality_engine' imports 'mercury_ai.analysis.data_quality_engine.DataQualityEngine' which does not exist

**import:** mercury_ai.analysis.data_quality_engine.DataQualityEngine

#### FAIL: tests.test_demo_operations

**Message:** Broken import: 'mercury_ai.operations.demo_manager.DemoOperationsManager' not found in codebase

**Evidence:** Module 'tests.test_demo_operations' imports 'mercury_ai.operations.demo_manager.DemoOperationsManager' which does not exist

**import:** mercury_ai.operations.demo_manager.DemoOperationsManager

#### FAIL: tests.test_demo_page

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_demo_page' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_demo_page

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_demo_page' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_demo_page

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'tests.test_demo_page' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: tests.test_determinism

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_determinism' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_determinism

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_determinism' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_determinism

**Message:** Broken import: 'mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider' not found in codebase

**Evidence:** Module 'tests.test_determinism' imports 'mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider' which does not exist

**import:** mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider

#### FAIL: tests.test_engine_performance_auditor

**Message:** Broken import: 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' not found in codebase

**Evidence:** Module 'tests.test_engine_performance_auditor' imports 'mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor' which does not exist

**import:** mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor

#### FAIL: tests.test_evidence_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_evidence_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_evidence_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_engine.EvidenceEngine' not found in codebase

**Evidence:** Module 'tests.test_evidence_engine' imports 'mercury_ai.analysis.evidence_engine.EvidenceEngine' which does not exist

**import:** mercury_ai.analysis.evidence_engine.EvidenceEngine

#### FAIL: tests.test_evidence_quality_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_evidence_quality_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_evidence_quality_engine

**Message:** Broken import: 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' not found in codebase

**Evidence:** Module 'tests.test_evidence_quality_engine' imports 'mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine' which does not exist

**import:** mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine

#### FAIL: tests.test_export_center

**Message:** Broken import: 'mercury_ai.core.export_center.ExportCenter' not found in codebase

**Evidence:** Module 'tests.test_export_center' imports 'mercury_ai.core.export_center.ExportCenter' which does not exist

**import:** mercury_ai.core.export_center.ExportCenter

#### FAIL: tests.test_health_auditor

**Message:** Broken import: 'mercury_ai.analysis.health_auditor.HealthAuditor' not found in codebase

**Evidence:** Module 'tests.test_health_auditor' imports 'mercury_ai.analysis.health_auditor.HealthAuditor' which does not exist

**import:** mercury_ai.analysis.health_auditor.HealthAuditor

#### FAIL: tests.test_health_center

**Message:** Broken import: 'mercury_ai.core.health_center.HealthCenter' not found in codebase

**Evidence:** Module 'tests.test_health_center' imports 'mercury_ai.core.health_center.HealthCenter' which does not exist

**import:** mercury_ai.core.health_center.HealthCenter

#### FAIL: tests.test_health_center

**Message:** Broken import: 'mercury_ai.providers.mercury_data_provider.MercuryDataProviderManager' not found in codebase

**Evidence:** Module 'tests.test_health_center' imports 'mercury_ai.providers.mercury_data_provider.MercuryDataProviderManager' which does not exist

**import:** mercury_ai.providers.mercury_data_provider.MercuryDataProviderManager

#### FAIL: tests.test_health_center

**Message:** Broken import: 'app.dashboard.health_center_panel.render_health_center_panel' not found in codebase

**Evidence:** Module 'tests.test_health_center' imports 'app.dashboard.health_center_panel.render_health_center_panel' which does not exist

**import:** app.dashboard.health_center_panel.render_health_center_panel

#### FAIL: tests.test_health_checker

**Message:** Broken import: 'mercury_ai.analysis.health_checker.HealthChecker' not found in codebase

**Evidence:** Module 'tests.test_health_checker' imports 'mercury_ai.analysis.health_checker.HealthChecker' which does not exist

**import:** mercury_ai.analysis.health_checker.HealthChecker

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.replay_cache.ReplayCache' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.replay_cache.ReplayCache' which does not exist

**import:** mercury_ai.analysis.replay_cache.ReplayCache

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor' which does not exist

**import:** mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.replay_batch_processor.BatchReplayResult' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.replay_batch_processor.BatchReplayResult' which does not exist

**import:** mercury_ai.analysis.replay_batch_processor.BatchReplayResult

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.replay_batch_processor.BatchReplayReport' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.replay_batch_processor.BatchReplayReport' which does not exist

**import:** mercury_ai.analysis.replay_batch_processor.BatchReplayReport

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.risk_engine.RiskEngine' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.risk_engine.RiskEngine' which does not exist

**import:** mercury_ai.analysis.risk_engine.RiskEngine

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.models.equity_metrics.AssetPerformance' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.models.equity_metrics.AssetPerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.AssetPerformance

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.models.equity_metrics.UniversePerformance' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.models.equity_metrics.UniversePerformance' which does not exist

**import:** mercury_ai.models.equity_metrics.UniversePerformance

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.models.risk_assessment.RiskAssessment' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.models.risk_assessment.RiskAssessment' which does not exist

**import:** mercury_ai.models.risk_assessment.RiskAssessment

#### FAIL: tests.test_institutional_backtest

**Message:** Broken import: 'mercury_ai.database.replay_storage.ReplayMetrics' not found in codebase

**Evidence:** Module 'tests.test_institutional_backtest' imports 'mercury_ai.database.replay_storage.ReplayMetrics' which does not exist

**import:** mercury_ai.database.replay_storage.ReplayMetrics

#### FAIL: tests.test_institutional_report_generator

**Message:** Broken import: 'mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator' not found in codebase

**Evidence:** Module 'tests.test_institutional_report_generator' imports 'mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator' which does not exist

**import:** mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator

#### FAIL: tests.test_integrity_checker

**Message:** Broken import: 'mercury_ai.analysis.integrity_checker.IntegrityChecker' not found in codebase

**Evidence:** Module 'tests.test_integrity_checker' imports 'mercury_ai.analysis.integrity_checker.IntegrityChecker' which does not exist

**import:** mercury_ai.analysis.integrity_checker.IntegrityChecker

#### FAIL: tests.test_job_manager

**Message:** Broken import: 'mercury_ai.core.job_manager.JobManager' not found in codebase

**Evidence:** Module 'tests.test_job_manager' imports 'mercury_ai.core.job_manager.JobManager' which does not exist

**import:** mercury_ai.core.job_manager.JobManager

#### FAIL: tests.test_live_monitor

**Message:** Broken import: 'mercury_ai.analysis.live_monitor.LiveMonitor' not found in codebase

**Evidence:** Module 'tests.test_live_monitor' imports 'mercury_ai.analysis.live_monitor.LiveMonitor' which does not exist

**import:** mercury_ai.analysis.live_monitor.LiveMonitor

#### FAIL: tests.test_live_monitor

**Message:** Broken import: 'mercury_ai.analysis.live_monitor.LiveMonitor' not found in codebase

**Evidence:** Module 'tests.test_live_monitor' imports 'mercury_ai.analysis.live_monitor.LiveMonitor' which does not exist

**import:** mercury_ai.analysis.live_monitor.LiveMonitor

#### FAIL: tests.test_main_dashboard

**Message:** Broken import: 'app.dashboard.main_dashboard.main' not found in codebase

**Evidence:** Module 'tests.test_main_dashboard' imports 'app.dashboard.main_dashboard.main' which does not exist

**import:** app.dashboard.main_dashboard.main

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.core.exceptions.MarketClosedException' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.core.exceptions.MarketClosedException' which does not exist

**import:** mercury_ai.core.exceptions.MarketClosedException

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_market_resilience

**Message:** Broken import: 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' not found in codebase

**Evidence:** Module 'tests.test_market_resilience' imports 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider' which does not exist

**import:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### FAIL: tests.test_notification_center

**Message:** Broken import: 'mercury_ai.analysis.notification_center.NotificationCenter' not found in codebase

**Evidence:** Module 'tests.test_notification_center' imports 'mercury_ai.analysis.notification_center.NotificationCenter' which does not exist

**import:** mercury_ai.analysis.notification_center.NotificationCenter

#### FAIL: tests.test_observability_center

**Message:** Broken import: 'mercury_ai.core.observability_center.ObservabilityCenter' not found in codebase

**Evidence:** Module 'tests.test_observability_center' imports 'mercury_ai.core.observability_center.ObservabilityCenter' which does not exist

**import:** mercury_ai.core.observability_center.ObservabilityCenter

#### FAIL: tests.test_observability_panel

**Message:** Broken import: 'app.dashboard.observability_panel.render_observability_dashboard' not found in codebase

**Evidence:** Module 'tests.test_observability_panel' imports 'app.dashboard.observability_panel.render_observability_dashboard' which does not exist

**import:** app.dashboard.observability_panel.render_observability_dashboard

#### FAIL: tests.test_operational_history

**Message:** Broken import: 'mercury_ai.analysis.operational_history.OperationalHistory' not found in codebase

**Evidence:** Module 'tests.test_operational_history' imports 'mercury_ai.analysis.operational_history.OperationalHistory' which does not exist

**import:** mercury_ai.analysis.operational_history.OperationalHistory

#### FAIL: tests.test_performance_analytics

**Message:** Broken import: 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' not found in codebase

**Evidence:** Module 'tests.test_performance_analytics' imports 'mercury_ai.analysis.performance_analytics.PerformanceAnalytics' which does not exist

**import:** mercury_ai.analysis.performance_analytics.PerformanceAnalytics

#### FAIL: tests.test_performance_center

**Message:** Broken import: 'mercury_ai.analysis.performance_center.PerformanceCenter' not found in codebase

**Evidence:** Module 'tests.test_performance_center' imports 'mercury_ai.analysis.performance_center.PerformanceCenter' which does not exist

**import:** mercury_ai.analysis.performance_center.PerformanceCenter

#### FAIL: tests.test_performance_collector

**Message:** Broken import: 'mercury_ai.utils.performance_collector.PerformanceCollector' not found in codebase

**Evidence:** Module 'tests.test_performance_collector' imports 'mercury_ai.utils.performance_collector.PerformanceCollector' which does not exist

**import:** mercury_ai.utils.performance_collector.PerformanceCollector

#### FAIL: tests.test_performance_engine

**Message:** Broken import: 'mercury_ai.analysis.performance_engine.PerformanceEngine' not found in codebase

**Evidence:** Module 'tests.test_performance_engine' imports 'mercury_ai.analysis.performance_engine.PerformanceEngine' which does not exist

**import:** mercury_ai.analysis.performance_engine.PerformanceEngine

#### FAIL: tests.test_performance_engine

**Message:** Broken import: 'mercury_ai.analysis.historical_replay_engine.ReplayMetrics' not found in codebase

**Evidence:** Module 'tests.test_performance_engine' imports 'mercury_ai.analysis.historical_replay_engine.ReplayMetrics' which does not exist

**import:** mercury_ai.analysis.historical_replay_engine.ReplayMetrics

#### FAIL: tests.test_performance_statistics

**Message:** Broken import: 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' not found in codebase

**Evidence:** Module 'tests.test_performance_statistics' imports 'mercury_ai.analysis.performance_statistics.PerformanceStatistics' which does not exist

**import:** mercury_ai.analysis.performance_statistics.PerformanceStatistics

#### FAIL: tests.test_pipeline_persistence

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_pipeline_persistence' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_pipeline_persistence

**Message:** Broken import: 'mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider' not found in codebase

**Evidence:** Module 'tests.test_pipeline_persistence' imports 'mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider' which does not exist

**import:** mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider

#### FAIL: tests.test_pipeline_persistence

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_pipeline_persistence' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.brain.probability_engine.ProbabilityEngine' not found in codebase

**Evidence:** Module 'tests.test_probability_engine' imports 'mercury_ai.brain.probability_engine.ProbabilityEngine' which does not exist

**import:** mercury_ai.brain.probability_engine.ProbabilityEngine

#### FAIL: tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'tests.test_probability_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'tests.test_probability_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: tests.test_probability_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_probability_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.MercuryDataProvider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.MercuryDataProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.MercuryDataProvider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.YahooProvider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.YahooProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.YahooProvider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.PolygonProvider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.PolygonProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.PolygonProvider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.TwelveDataProvider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.TwelveDataProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.TwelveDataProvider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.AlphaVantageProvider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.AlphaVantageProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.AlphaVantageProvider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.BinanceProvider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.BinanceProvider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.BinanceProvider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.data.mercury_data_provider.MetaTrader5Provider' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.data.mercury_data_provider.MetaTrader5Provider' which does not exist

**import:** mercury_ai.data.mercury_data_provider.MetaTrader5Provider

#### FAIL: tests.test_provider_priority_engine

**Message:** Broken import: 'mercury_ai.analysis.provider_priority_engine.ProviderPriorityEngine' not found in codebase

**Evidence:** Module 'tests.test_provider_priority_engine' imports 'mercury_ai.analysis.provider_priority_engine.ProviderPriorityEngine' which does not exist

**import:** mercury_ai.analysis.provider_priority_engine.ProviderPriorityEngine

#### FAIL: tests.test_read_only

**Message:** Broken import: 'mercury_ai.core.read_only.check_read_only' not found in codebase

**Evidence:** Module 'tests.test_read_only' imports 'mercury_ai.core.read_only.check_read_only' which does not exist

**import:** mercury_ai.core.read_only.check_read_only

#### FAIL: tests.test_read_only

**Message:** Broken import: 'mercury_ai.core.read_only.ReadOnlyViolation' not found in codebase

**Evidence:** Module 'tests.test_read_only' imports 'mercury_ai.core.read_only.ReadOnlyViolation' which does not exist

**import:** mercury_ai.core.read_only.ReadOnlyViolation

#### FAIL: tests.test_regression_sprint18

**Message:** Broken import: 'mercury_ai.models.market_structure_profile.MarketStructureProfile' not found in codebase

**Evidence:** Module 'tests.test_regression_sprint18' imports 'mercury_ai.models.market_structure_profile.MarketStructureProfile' which does not exist

**import:** mercury_ai.models.market_structure_profile.MarketStructureProfile

#### FAIL: tests.test_regression_sprint18

**Message:** Broken import: 'mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider' not found in codebase

**Evidence:** Module 'tests.test_regression_sprint18' imports 'mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider' which does not exist

**import:** mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider

#### FAIL: tests.test_regression_sprint18

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_regression_sprint18' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_regression_sprint18

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_regression_sprint18' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_robustness

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_robustness' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_robustness

**Message:** Broken import: 'mercury_ai.data.market_data_provider.MarketDataProvider' not found in codebase

**Evidence:** Module 'tests.test_robustness' imports 'mercury_ai.data.market_data_provider.MarketDataProvider' which does not exist

**import:** mercury_ai.data.market_data_provider.MarketDataProvider

#### FAIL: tests.test_robustness

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_robustness' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_scanner_priority

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'tests.test_scanner_priority' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: tests.test_scanner_priority

**Message:** Broken import: 'mercury_ai.core.asset_registry.AssetRegistry' not found in codebase

**Evidence:** Module 'tests.test_scanner_priority' imports 'mercury_ai.core.asset_registry.AssetRegistry' which does not exist

**import:** mercury_ai.core.asset_registry.AssetRegistry

#### FAIL: tests.test_scanner_recovery

**Message:** Broken import: 'mercury_ai.brain.scanner.MercuryScanner' not found in codebase

**Evidence:** Module 'tests.test_scanner_recovery' imports 'mercury_ai.brain.scanner.MercuryScanner' which does not exist

**import:** mercury_ai.brain.scanner.MercuryScanner

#### FAIL: tests.test_security_center

**Message:** Broken import: 'mercury_ai.core.security_center.SecurityCenter' not found in codebase

**Evidence:** Module 'tests.test_security_center' imports 'mercury_ai.core.security_center.SecurityCenter' which does not exist

**import:** mercury_ai.core.security_center.SecurityCenter

#### FAIL: tests.test_session_id

**Message:** Broken import: 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' not found in codebase

**Evidence:** Module 'tests.test_session_id' imports 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' which does not exist

**import:** mercury_ai.core.analysis_pipeline.AnalysisPipeline

#### FAIL: tests.test_session_id

**Message:** Broken import: 'mercury_ai.data.market_data.MarketDataService' not found in codebase

**Evidence:** Module 'tests.test_session_id' imports 'mercury_ai.data.market_data.MarketDataService' which does not exist

**import:** mercury_ai.data.market_data.MarketDataService

#### FAIL: tests.test_session_id

**Message:** Broken import: 'mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider' not found in codebase

**Evidence:** Module 'tests.test_session_id' imports 'mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider' which does not exist

**import:** mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider

#### FAIL: tests.test_session_manager

**Message:** Broken import: 'mercury_ai.core.session_manager.SessionManager' not found in codebase

**Evidence:** Module 'tests.test_session_manager' imports 'mercury_ai.core.session_manager.SessionManager' which does not exist

**import:** mercury_ai.core.session_manager.SessionManager

#### FAIL: tests.test_statistical_auditor

**Message:** Broken import: 'mercury_ai.analysis.statistical_auditor.StatisticalAuditor' not found in codebase

**Evidence:** Module 'tests.test_statistical_auditor' imports 'mercury_ai.analysis.statistical_auditor.StatisticalAuditor' which does not exist

**import:** mercury_ai.analysis.statistical_auditor.StatisticalAuditor

#### FAIL: tests.test_trade_outcome_engine

**Message:** Broken import: 'mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine' not found in codebase

**Evidence:** Module 'tests.test_trade_outcome_engine' imports 'mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine' which does not exist

**import:** mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine

#### FAIL: tests.test_validation_engine

**Message:** Broken import: 'mercury_ai.analysis.validation_engine.ValidationEngine' not found in codebase

**Evidence:** Module 'tests.test_validation_engine' imports 'mercury_ai.analysis.validation_engine.ValidationEngine' which does not exist

**import:** mercury_ai.analysis.validation_engine.ValidationEngine

#### FAIL: tests.test_validation_engine

**Message:** Broken import: 'mercury_ai.models.market_context.MarketContext' not found in codebase

**Evidence:** Module 'tests.test_validation_engine' imports 'mercury_ai.models.market_context.MarketContext' which does not exist

**import:** mercury_ai.models.market_context.MarketContext

#### FAIL: tests.test_validation_engine

**Message:** Broken import: 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' not found in codebase

**Evidence:** Module 'tests.test_validation_engine' imports 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' which does not exist

**import:** mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

#### FAIL: tests.test_validation_engine

**Message:** Broken import: 'mercury_ai.models.evidence.Evidence' not found in codebase

**Evidence:** Module 'tests.test_validation_engine' imports 'mercury_ai.models.evidence.Evidence' which does not exist

**import:** mercury_ai.models.evidence.Evidence

#### FAIL: tests.test_versioning

**Message:** Broken import: 'mercury_ai.models.analysis_result.AnalysisResult' not found in codebase

**Evidence:** Module 'tests.test_versioning' imports 'mercury_ai.models.analysis_result.AnalysisResult' which does not exist

**import:** mercury_ai.models.analysis_result.AnalysisResult

#### FAIL: tests.test_versioning

**Message:** Broken import: 'mercury_ai.models.decision_snapshot.DecisionSnapshot' not found in codebase

**Evidence:** Module 'tests.test_versioning' imports 'mercury_ai.models.decision_snapshot.DecisionSnapshot' which does not exist

**import:** mercury_ai.models.decision_snapshot.DecisionSnapshot

#### FAIL: tests.test_versioning

**Message:** Broken import: 'mercury_ai.config.settings' not found in codebase

**Evidence:** Module 'tests.test_versioning' imports 'mercury_ai.config.settings' which does not exist

**import:** mercury_ai.config.settings

#### FAIL: tests.test_weight_simulator

**Message:** Broken import: 'mercury_ai.analysis.weight_simulator.WeightSimulator' not found in codebase

**Evidence:** Module 'tests.test_weight_simulator' imports 'mercury_ai.analysis.weight_simulator.WeightSimulator' which does not exist

**import:** mercury_ai.analysis.weight_simulator.WeightSimulator

### DEAD_CODE_MODULE (88 findings)

#### WARNING: mercury_ai.models.market_structure

**Message:** Dead code: Module 'mercury_ai.models.market_structure' is unreachable

**Evidence:** Module 'mercury_ai.models.market_structure' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.provider

**Message:** Dead code: Module 'mercury_ai.providers.provider' is unreachable

**Evidence:** Module 'mercury_ai.providers.provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.data_quality_result

**Message:** Dead code: Module 'mercury_ai.models.data_quality_result' is unreachable

**Evidence:** Module 'mercury_ai.models.data_quality_result' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.ai.llm

**Message:** Dead code: Module 'mercury_ai.ai.llm' is unreachable

**Evidence:** Module 'mercury_ai.ai.llm' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.base_provider

**Message:** Dead code: Module 'mercury_ai.providers.base_provider' is unreachable

**Evidence:** Module 'mercury_ai.providers.base_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Dead code: Module 'mercury_ai.analysis.institutional_context_builder' is unreachable

**Evidence:** Module 'mercury_ai.analysis.institutional_context_builder' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.decision_resolver_engine

**Message:** Dead code: Module 'mercury_ai.analysis.decision_resolver_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.decision_resolver_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.support_resistance

**Message:** Dead code: Module 'mercury_ai.models.support_resistance' is unreachable

**Evidence:** Module 'mercury_ai.models.support_resistance' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.liquidity_result

**Message:** Dead code: Module 'mercury_ai.models.liquidity_result' is unreachable

**Evidence:** Module 'mercury_ai.models.liquidity_result' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.indicators.rsi

**Message:** Dead code: Module 'mercury_ai.indicators.rsi' is unreachable

**Evidence:** Module 'mercury_ai.indicators.rsi' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.data_quality_engine

**Message:** Dead code: Module 'mercury_ai.data.data_quality_engine' is unreachable

**Evidence:** Module 'mercury_ai.data.data_quality_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.config.universe

**Message:** Dead code: Module 'mercury_ai.config.universe' is unreachable

**Evidence:** Module 'mercury_ai.config.universe' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.equity_metrics

**Message:** Dead code: Module 'mercury_ai.models.equity_metrics' is unreachable

**Evidence:** Module 'mercury_ai.models.equity_metrics' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.utils.deterministic_clock

**Message:** Dead code: Module 'mercury_ai.utils.deterministic_clock' is unreachable

**Evidence:** Module 'mercury_ai.utils.deterministic_clock' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.audit_sink

**Message:** Dead code: Module 'mercury_ai.core.audit_sink' is unreachable

**Evidence:** Module 'mercury_ai.core.audit_sink' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Dead code: Module 'mercury_ai.data.mercury_data_provider' is unreachable

**Evidence:** Module 'mercury_ai.data.mercury_data_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.database.replay_storage

**Message:** Dead code: Module 'mercury_ai.database.replay_storage' is unreachable

**Evidence:** Module 'mercury_ai.database.replay_storage' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.version_metadata

**Message:** Dead code: Module 'mercury_ai.models.version_metadata' is unreachable

**Evidence:** Module 'mercury_ai.models.version_metadata' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.decision_input

**Message:** Dead code: Module 'mercury_ai.models.decision_input' is unreachable

**Evidence:** Module 'mercury_ai.models.decision_input' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.read_only

**Message:** Dead code: Module 'mercury_ai.core.read_only' is unreachable

**Evidence:** Module 'mercury_ai.core.read_only' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Dead code: Module 'mercury_ai.providers.historical_replay_provider' is unreachable

**Evidence:** Module 'mercury_ai.providers.historical_replay_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.swing_analysis

**Message:** Dead code: Module 'mercury_ai.models.swing_analysis' is unreachable

**Evidence:** Module 'mercury_ai.models.swing_analysis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.profiler_models

**Message:** Dead code: Module 'mercury_ai.models.profiler_models' is unreachable

**Evidence:** Module 'mercury_ai.models.profiler_models' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.learning_engine

**Message:** Dead code: Module 'mercury_ai.analysis.learning_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.learning_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.confluence_score

**Message:** Dead code: Module 'mercury_ai.models.confluence_score' is unreachable

**Evidence:** Module 'mercury_ai.models.confluence_score' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.market_data_provider

**Message:** Dead code: Module 'mercury_ai.data.market_data_provider' is unreachable

**Evidence:** Module 'mercury_ai.data.market_data_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Dead code: Module 'mercury_ai.providers.future_tradingview_provider' is unreachable

**Evidence:** Module 'mercury_ai.providers.future_tradingview_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core._stage_builder

**Message:** Dead code: Module 'mercury_ai.core._stage_builder' is unreachable

**Evidence:** Module 'mercury_ai.core._stage_builder' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.market_data

**Message:** Dead code: Module 'mercury_ai.models.market_data' is unreachable

**Evidence:** Module 'mercury_ai.models.market_data' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.mtf_consensus

**Message:** Dead code: Module 'mercury_ai.models.mtf_consensus' is unreachable

**Evidence:** Module 'mercury_ai.models.mtf_consensus' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.decision_node

**Message:** Dead code: Module 'mercury_ai.models.decision_node' is unreachable

**Evidence:** Module 'mercury_ai.models.decision_node' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.data_quality_engine

**Message:** Dead code: Module 'mercury_ai.analysis.data_quality_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.data_quality_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.market_regime_enum

**Message:** Dead code: Module 'mercury_ai.models.market_regime_enum' is unreachable

**Evidence:** Module 'mercury_ai.models.market_regime_enum' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.direction

**Message:** Dead code: Module 'mercury_ai.models.direction' is unreachable

**Evidence:** Module 'mercury_ai.models.direction' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Dead code: Module 'mercury_ai.analysis.replay_cache' is unreachable

**Evidence:** Module 'mercury_ai.analysis.replay_cache' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.volume_profile

**Message:** Dead code: Module 'mercury_ai.models.volume_profile' is unreachable

**Evidence:** Module 'mercury_ai.models.volume_profile' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.runtime_report

**Message:** Dead code: Module 'mercury_ai.core.runtime_report' is unreachable

**Evidence:** Module 'mercury_ai.core.runtime_report' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.utils.report_generator

**Message:** Dead code: Module 'mercury_ai.utils.report_generator' is unreachable

**Evidence:** Module 'mercury_ai.utils.report_generator' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.risk_assessment

**Message:** Dead code: Module 'mercury_ai.models.risk_assessment' is unreachable

**Evidence:** Module 'mercury_ai.models.risk_assessment' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.session_analysis

**Message:** Dead code: Module 'mercury_ai.models.session_analysis' is unreachable

**Evidence:** Module 'mercury_ai.models.session_analysis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.liquidity_event_enum

**Message:** Dead code: Module 'mercury_ai.models.liquidity_event_enum' is unreachable

**Evidence:** Module 'mercury_ai.models.liquidity_event_enum' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Dead code: Module 'mercury_ai.providers.future_polygon_provider' is unreachable

**Evidence:** Module 'mercury_ai.providers.future_polygon_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Dead code: Module 'mercury_ai.analysis.institutional_analytics_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.institutional_analytics_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.news.news_provider

**Message:** Dead code: Module 'mercury_ai.news.news_provider' is unreachable

**Evidence:** Module 'mercury_ai.news.news_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.data_quality_gate

**Message:** Dead code: Module 'mercury_ai.core.data_quality_gate' is unreachable

**Evidence:** Module 'mercury_ai.core.data_quality_gate' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.brain.exceptions

**Message:** Dead code: Module 'mercury_ai.brain.exceptions' is unreachable

**Evidence:** Module 'mercury_ai.brain.exceptions' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.confidence_result

**Message:** Dead code: Module 'mercury_ai.models.confidence_result' is unreachable

**Evidence:** Module 'mercury_ai.models.confidence_result' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.data_interfaces

**Message:** Dead code: Module 'mercury_ai.providers.data_interfaces' is unreachable

**Evidence:** Module 'mercury_ai.providers.data_interfaces' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.banner

**Message:** Dead code: Module 'mercury_ai.core.banner' is unreachable

**Evidence:** Module 'mercury_ai.core.banner' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.probability_result

**Message:** Dead code: Module 'mercury_ai.models.probability_result' is unreachable

**Evidence:** Module 'mercury_ai.models.probability_result' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.indicator_engine

**Message:** Dead code: Module 'mercury_ai.data.indicator_engine' is unreachable

**Evidence:** Module 'mercury_ai.data.indicator_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.market_condition

**Message:** Dead code: Module 'mercury_ai.models.market_condition' is unreachable

**Evidence:** Module 'mercury_ai.models.market_condition' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.support_resistance_analysis

**Message:** Dead code: Module 'mercury_ai.models.support_resistance_analysis' is unreachable

**Evidence:** Module 'mercury_ai.models.support_resistance_analysis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.market_state_enum

**Message:** Dead code: Module 'mercury_ai.models.market_state_enum' is unreachable

**Evidence:** Module 'mercury_ai.models.market_state_enum' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.project_state

**Message:** Dead code: Module 'mercury_ai.core.project_state' is unreachable

**Evidence:** Module 'mercury_ai.core.project_state' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.data_normalizer

**Message:** Dead code: Module 'mercury_ai.data.data_normalizer' is unreachable

**Evidence:** Module 'mercury_ai.data.data_normalizer' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.trade_filter_result

**Message:** Dead code: Module 'mercury_ai.models.trade_filter_result' is unreachable

**Evidence:** Module 'mercury_ai.models.trade_filter_result' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Dead code: Module 'mercury_ai.providers.future_broker_provider' is unreachable

**Evidence:** Module 'mercury_ai.providers.future_broker_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.exceptions

**Message:** Dead code: Module 'mercury_ai.core.exceptions' is unreachable

**Evidence:** Module 'mercury_ai.core.exceptions' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.metric_calculator

**Message:** Dead code: Module 'mercury_ai.analysis.metric_calculator' is unreachable

**Evidence:** Module 'mercury_ai.analysis.metric_calculator' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.base_engine

**Message:** Dead code: Module 'mercury_ai.core.base_engine' is unreachable

**Evidence:** Module 'mercury_ai.core.base_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.price_action

**Message:** Dead code: Module 'mercury_ai.models.price_action' is unreachable

**Evidence:** Module 'mercury_ai.models.price_action' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.institutional_contribution

**Message:** Dead code: Module 'mercury_ai.analysis.institutional_contribution' is unreachable

**Evidence:** Module 'mercury_ai.analysis.institutional_contribution' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.observability_center

**Message:** Dead code: Module 'mercury_ai.core.observability_center' is unreachable

**Evidence:** Module 'mercury_ai.core.observability_center' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.performance_metrics

**Message:** Dead code: Module 'mercury_ai.models.performance_metrics' is unreachable

**Evidence:** Module 'mercury_ai.models.performance_metrics' has content but is not an entry point and not imported by any module


#### WARNING: app.ui_utils

**Message:** Dead code: Module 'app.ui_utils' is unreachable

**Evidence:** Module 'app.ui_utils' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.core.asset_registry

**Message:** Dead code: Module 'mercury_ai.core.asset_registry' is unreachable

**Evidence:** Module 'mercury_ai.core.asset_registry' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.utils.system_monitor

**Message:** Dead code: Module 'mercury_ai.utils.system_monitor' is unreachable

**Evidence:** Module 'mercury_ai.utils.system_monitor' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.professional_thesis

**Message:** Dead code: Module 'mercury_ai.models.professional_thesis' is unreachable

**Evidence:** Module 'mercury_ai.models.professional_thesis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.presentation.signal_formatter

**Message:** Dead code: Module 'mercury_ai.presentation.signal_formatter' is unreachable

**Evidence:** Module 'mercury_ai.presentation.signal_formatter' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.live_monitor

**Message:** Dead code: Module 'mercury_ai.analysis.live_monitor' is unreachable

**Evidence:** Module 'mercury_ai.analysis.live_monitor' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.regression

**Message:** Dead code: Module 'mercury_ai.models.regression' is unreachable

**Evidence:** Module 'mercury_ai.models.regression' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.trade_permission

**Message:** Dead code: Module 'mercury_ai.models.trade_permission' is unreachable

**Evidence:** Module 'mercury_ai.models.trade_permission' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.calibration_analyzer

**Message:** Dead code: Module 'mercury_ai.analysis.calibration_analyzer' is unreachable

**Evidence:** Module 'mercury_ai.analysis.calibration_analyzer' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.database.history_logger

**Message:** Dead code: Module 'mercury_ai.database.history_logger' is unreachable

**Evidence:** Module 'mercury_ai.database.history_logger' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.candlestick_analysis

**Message:** Dead code: Module 'mercury_ai.models.candlestick_analysis' is unreachable

**Evidence:** Module 'mercury_ai.models.candlestick_analysis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.price_action_analysis

**Message:** Dead code: Module 'mercury_ai.models.price_action_analysis' is unreachable

**Evidence:** Module 'mercury_ai.models.price_action_analysis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.decision_outcome

**Message:** Dead code: Module 'mercury_ai.models.decision_outcome' is unreachable

**Evidence:** Module 'mercury_ai.models.decision_outcome' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.replay_data_provider

**Message:** Dead code: Module 'mercury_ai.data.replay_data_provider' is unreachable

**Evidence:** Module 'mercury_ai.data.replay_data_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.trade_outcome_engine

**Message:** Dead code: Module 'mercury_ai.analysis.trade_outcome_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.trade_outcome_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.performance

**Message:** Dead code: Module 'mercury_ai.models.performance' is unreachable

**Evidence:** Module 'mercury_ai.models.performance' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Dead code: Module 'mercury_ai.data.providers.historical_data_provider' is unreachable

**Evidence:** Module 'mercury_ai.data.providers.historical_data_provider' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.institutional_score_engine

**Message:** Dead code: Module 'mercury_ai.analysis.institutional_score_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.institutional_score_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.liquidity_profile

**Message:** Dead code: Module 'mercury_ai.models.liquidity_profile' is unreachable

**Evidence:** Module 'mercury_ai.models.liquidity_profile' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.trend_analysis

**Message:** Dead code: Module 'mercury_ai.models.trend_analysis' is unreachable

**Evidence:** Module 'mercury_ai.models.trend_analysis' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.calendar.economic_calendar

**Message:** Dead code: Module 'mercury_ai.calendar.economic_calendar' is unreachable

**Evidence:** Module 'mercury_ai.calendar.economic_calendar' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.analysis.smart_money.order_block_engine

**Message:** Dead code: Module 'mercury_ai.analysis.smart_money.order_block_engine' is unreachable

**Evidence:** Module 'mercury_ai.analysis.smart_money.order_block_engine' has content but is not an entry point and not imported by any module


#### WARNING: mercury_ai.models.memory_audit

**Message:** Dead code: Module 'mercury_ai.models.memory_audit' is unreachable

**Evidence:** Module 'mercury_ai.models.memory_audit' has content but is not an entry point and not imported by any module


### DIP_VIOLATION (7 findings)

#### WARNING: mercury_ai.brain.scanner

**Message:** DIP violation: High-level module 'mercury_ai.brain.scanner' depends on low-level 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider'

**Evidence:** Core/brain module 'mercury_ai.brain.scanner' directly depends on provider/database/market implementation 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider'

**depends_on:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** DIP violation: High-level module 'mercury_ai.core.analysis_pipeline' depends on low-level 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger'

**Evidence:** Core/brain module 'mercury_ai.core.analysis_pipeline' directly depends on provider/database/market implementation 'mercury_ai.database.snapshot_logger.DecisionSnapshotLogger'

**depends_on:** mercury_ai.database.snapshot_logger.DecisionSnapshotLogger

#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** DIP violation: High-level module 'mercury_ai.core.analysis_pipeline' depends on low-level 'mercury_ai.providers.base_provider.MarketDataProvider'

**Evidence:** Core/brain module 'mercury_ai.core.analysis_pipeline' directly depends on provider/database/market implementation 'mercury_ai.providers.base_provider.MarketDataProvider'

**depends_on:** mercury_ai.providers.base_provider.MarketDataProvider

#### WARNING: mercury_ai.core.auto_health

**Message:** DIP violation: High-level module 'mercury_ai.core.auto_health' depends on low-level 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider'

**Evidence:** Core/brain module 'mercury_ai.core.auto_health' directly depends on provider/database/market implementation 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider'

**depends_on:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### WARNING: mercury_ai.core.health_center

**Message:** DIP violation: High-level module 'mercury_ai.core.health_center' depends on low-level 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider'

**Evidence:** Core/brain module 'mercury_ai.core.health_center' directly depends on provider/database/market implementation 'mercury_ai.providers.mercury_data_provider.MercuryDataProvider'

**depends_on:** mercury_ai.providers.mercury_data_provider.MercuryDataProvider

#### WARNING: mercury_ai.core.job_manager

**Message:** DIP violation: High-level module 'mercury_ai.core.job_manager' depends on low-level 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider'

**Evidence:** Core/brain module 'mercury_ai.core.job_manager' directly depends on provider/database/market implementation 'mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider'

**depends_on:** mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

#### WARNING: mercury_ai.core.startup

**Message:** DIP violation: High-level module 'mercury_ai.core.startup' depends on low-level 'mercury_ai.providers.provider.MarketProvider'

**Evidence:** Core/brain module 'mercury_ai.core.startup' directly depends on provider/database/market implementation 'mercury_ai.providers.provider.MarketProvider'

**depends_on:** mercury_ai.providers.provider.MarketProvider

### DUPLICATE_CLASS (12 findings)

#### WARNING: DataQualityEngine

**Message:** Duplicate class name 'DataQualityEngine' found in 2 modules

**Evidence:** Class 'DataQualityEngine' defined in: mercury_ai.analysis.data_quality_engine, mercury_ai.data.data_quality_engine

**modules:** ['mercury_ai.analysis.data_quality_engine', 'mercury_ai.data.data_quality_engine']

#### WARNING: PerformanceMetrics

**Message:** Duplicate class name 'PerformanceMetrics' found in 2 modules

**Evidence:** Class 'PerformanceMetrics' defined in: mercury_ai.analysis.metric_calculator, mercury_ai.models.performance_metrics

**modules:** ['mercury_ai.analysis.metric_calculator', 'mercury_ai.models.performance_metrics']

#### WARNING: AuditEvent

**Message:** Duplicate class name 'AuditEvent' found in 2 modules

**Evidence:** Class 'AuditEvent' defined in: mercury_ai.core.audit_sink, mercury_ai.core.security_center

**modules:** ['mercury_ai.core.audit_sink', 'mercury_ai.core.security_center']

#### WARNING: DataQualityResult

**Message:** Duplicate class name 'DataQualityResult' found in 2 modules

**Evidence:** Class 'DataQualityResult' defined in: mercury_ai.core.data_quality_gate, mercury_ai.models.data_quality_result

**modules:** ['mercury_ai.core.data_quality_gate', 'mercury_ai.models.data_quality_result']

#### WARNING: MarketDataProvider

**Message:** Duplicate class name 'MarketDataProvider' found in 2 modules

**Evidence:** Class 'MarketDataProvider' defined in: mercury_ai.data.market_data_provider, mercury_ai.providers.base_provider

**modules:** ['mercury_ai.data.market_data_provider', 'mercury_ai.providers.base_provider']

#### WARNING: MercuryDataProvider

**Message:** Duplicate class name 'MercuryDataProvider' found in 2 modules

**Evidence:** Class 'MercuryDataProvider' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: PriceActionAnalysis

**Message:** Duplicate class name 'PriceActionAnalysis' found in 2 modules

**Evidence:** Class 'PriceActionAnalysis' defined in: mercury_ai.models.price_action, mercury_ai.models.price_action_analysis

**modules:** ['mercury_ai.models.price_action', 'mercury_ai.models.price_action_analysis']

#### WARNING: SupportResistanceAnalysis

**Message:** Duplicate class name 'SupportResistanceAnalysis' found in 2 modules

**Evidence:** Class 'SupportResistanceAnalysis' defined in: mercury_ai.models.support_resistance, mercury_ai.models.support_resistance_analysis

**modules:** ['mercury_ai.models.support_resistance', 'mercury_ai.models.support_resistance_analysis']

#### WARNING: FileInfo

**Message:** Duplicate class name 'FileInfo' found in 2 modules

**Evidence:** Class 'FileInfo' defined in: tools.models, tools.project_mapper.models

**modules:** ['tools.models', 'tools.project_mapper.models']

#### WARNING: Inventory

**Message:** Duplicate class name 'Inventory' found in 2 modules

**Evidence:** Class 'Inventory' defined in: tools.models, tools.project_mapper.models

**modules:** ['tools.models', 'tools.project_mapper.models']

#### WARNING: ProjectScanner

**Message:** Duplicate class name 'ProjectScanner' found in 2 modules

**Evidence:** Class 'ProjectScanner' defined in: tools.scanner, tools.project_mapper.scanner

**modules:** ['tools.scanner', 'tools.project_mapper.scanner']

#### WARNING: InventoryWriter

**Message:** Duplicate class name 'InventoryWriter' found in 2 modules

**Evidence:** Class 'InventoryWriter' defined in: tools.writer, tools.project_mapper.writer

**modules:** ['tools.writer', 'tools.project_mapper.writer']

### DUPLICATE_FUNCTION (61 findings)

#### WARNING: main

**Message:** Duplicate function name 'main' found in 10 modules

**Evidence:** Function 'main' defined in: main, resolve_merge_conflicts, test_bloco7_scenarios, test_replay_quick, app.dashboard.main_dashboard, mercury_ai.main, scripts.run_replay_3500, tools.main, tools.mercury_integrity_auditor.main, tools.project_mapper.main

**modules:** ['main', 'resolve_merge_conflicts', 'test_bloco7_scenarios', 'test_replay_quick', 'app.dashboard.main_dashboard', 'mercury_ai.main', 'scripts.run_replay_3500', 'tools.main', 'tools.mercury_integrity_auditor.main', 'tools.project_mapper.main']

#### WARNING: get_data

**Message:** Duplicate function name 'get_data' found in 16 modules

**Evidence:** Function 'get_data' defined in: run_instrumented, mercury_ai.data.market_data, mercury_ai.data.market_data_provider, mercury_ai.data.replay_data_provider, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.data_interfaces, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.market_provider, mercury_ai.providers.yahoo_finance_provider, tests.test_robustness

**modules:** ['run_instrumented', 'mercury_ai.data.market_data', 'mercury_ai.data.market_data_provider', 'mercury_ai.data.replay_data_provider', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_interfaces', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.market_provider', 'mercury_ai.providers.yahoo_finance_provider', 'tests.test_robustness']

#### WARNING: is_available

**Message:** Duplicate function name 'is_available' found in 10 modules

**Evidence:** Function 'is_available' defined in: run_instrumented, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.market_provider, mercury_ai.providers.yahoo_finance_provider, tests.test_robustness

**modules:** ['run_instrumented', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.market_provider', 'mercury_ai.providers.yahoo_finance_provider', 'tests.test_robustness']

#### WARNING: supports_symbol

**Message:** Duplicate function name 'supports_symbol' found in 9 modules

**Evidence:** Function 'supports_symbol' defined in: run_instrumented, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.yahoo_finance_provider, tests.test_robustness

**modules:** ['run_instrumented', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.yahoo_finance_provider', 'tests.test_robustness']

#### WARNING: supports_market

**Message:** Duplicate function name 'supports_market' found in 8 modules

**Evidence:** Function 'supports_market' defined in: run_instrumented, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.yahoo_finance_provider

**modules:** ['run_instrumented', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.yahoo_finance_provider']

#### WARNING: supports_timeframe

**Message:** Duplicate function name 'supports_timeframe' found in 8 modules

**Evidence:** Function 'supports_timeframe' defined in: run_instrumented, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.yahoo_finance_provider

**modules:** ['run_instrumented', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.yahoo_finance_provider']

#### WARNING: max_history

**Message:** Duplicate function name 'max_history' found in 8 modules

**Evidence:** Function 'max_history' defined in: run_instrumented, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.yahoo_finance_provider

**modules:** ['run_instrumented', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.yahoo_finance_provider']

#### WARNING: source_name

**Message:** Duplicate function name 'source_name' found in 9 modules

**Evidence:** Function 'source_name' defined in: run_instrumented, mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.base_provider, mercury_ai.providers.future_broker_provider, mercury_ai.providers.future_polygon_provider, mercury_ai.providers.future_tradingview_provider, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.yahoo_finance_provider, tests.test_robustness

**modules:** ['run_instrumented', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.base_provider', 'mercury_ai.providers.future_broker_provider', 'mercury_ai.providers.future_polygon_provider', 'mercury_ai.providers.future_tradingview_provider', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.yahoo_finance_provider', 'tests.test_robustness']

#### WARNING: load_data

**Message:** Duplicate function name 'load_data' found in 2 modules

**Evidence:** Function 'load_data' defined in: app.dashboard.dashboard, app.terminal.pages.01_Scanner

**modules:** ['app.dashboard.dashboard', 'app.terminal.pages.01_Scanner']

#### WARNING: __init__

**Message:** Duplicate function name '__init__' found in 100 modules

**Evidence:** Function '__init__' defined in: mercury_ai.ai.llm, mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.calibration_analyzer, mercury_ai.analysis.confidence_calibration_auditor, mercury_ai.analysis.conflict_resolution_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.data_exporter, mercury_ai.analysis.decision_trace_engine, mercury_ai.analysis.engine_performance_auditor, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.health_auditor, mercury_ai.analysis.health_checker, mercury_ai.analysis.historical_replay_engine, mercury_ai.analysis.institutional_analytics_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.institutional_report, mercury_ai.analysis.institutional_report_generator, mercury_ai.analysis.integrity_checker, mercury_ai.analysis.learning_engine, mercury_ai.analysis.live_monitor, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.market_thesis_builder, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.notification_center, mercury_ai.analysis.operational_history, mercury_ai.analysis.performance_analytics, mercury_ai.analysis.performance_center, mercury_ai.analysis.performance_engine, mercury_ai.analysis.performance_statistics, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.provider_priority_engine, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.replay_cache, mercury_ai.analysis.risk_engine, mercury_ai.analysis.statistical_auditor, mercury_ai.analysis.swing_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.vwap_engine, mercury_ai.analysis.weight_simulator, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.scanner, mercury_ai.config.configuration_center, mercury_ai.core.analysis_pipeline, mercury_ai.core.asset_registry, mercury_ai.core.audit_sink, mercury_ai.core.auto_health, mercury_ai.core.export_center, mercury_ai.core.health_center, mercury_ai.core.job_manager, mercury_ai.core.observability_center, mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.pipeline_executor, mercury_ai.core.pipeline_profiler, mercury_ai.core.project_state, mercury_ai.core.security_center, mercury_ai.core.session_manager, mercury_ai.core._stage_builder, mercury_ai.data.market_data, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.replay_data_provider, mercury_ai.data.providers.historical_data_provider, mercury_ai.database.history_logger, mercury_ai.database.replay_storage, mercury_ai.database.snapshot_logger, mercury_ai.market.market_engine, mercury_ai.operations.demo_manager, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.data_adapters, mercury_ai.providers.historical_replay_provider, mercury_ai.providers.market_provider, mercury_ai.utils.memory_auditor, mercury_ai.utils.performance_collector, mercury_ai.utils.regression_detector, mercury_ai.utils.report_generator, mercury_ai.utils.stress_tester, tests.test_robustness, tools.mercury_integrity_auditor.auditors.contract_auditor, tools.mercury_integrity_auditor.auditors.decision_auditor, tools.mercury_integrity_auditor.auditors.flow_auditor, tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.static_auditor, tools.project_mapper.snapshot_builder

**modules:** ['mercury_ai.ai.llm', 'mercury_ai.analysis.benchmark_framework', 'mercury_ai.analysis.calibration_analyzer', 'mercury_ai.analysis.confidence_calibration_auditor', 'mercury_ai.analysis.conflict_resolution_engine', 'mercury_ai.analysis.confluence_engine', 'mercury_ai.analysis.context_engine', 'mercury_ai.analysis.data_exporter', 'mercury_ai.analysis.decision_trace_engine', 'mercury_ai.analysis.engine_performance_auditor', 'mercury_ai.analysis.evidence_engine', 'mercury_ai.analysis.fair_value_gap_engine', 'mercury_ai.analysis.health_auditor', 'mercury_ai.analysis.health_checker', 'mercury_ai.analysis.historical_replay_engine', 'mercury_ai.analysis.institutional_analytics_engine', 'mercury_ai.analysis.institutional_memory_engine', 'mercury_ai.analysis.institutional_report', 'mercury_ai.analysis.institutional_report_generator', 'mercury_ai.analysis.integrity_checker', 'mercury_ai.analysis.learning_engine', 'mercury_ai.analysis.live_monitor', 'mercury_ai.analysis.market_structure_intelligence_engine', 'mercury_ai.analysis.market_thesis_builder', 'mercury_ai.analysis.momentum_engine', 'mercury_ai.analysis.mtf_engine', 'mercury_ai.analysis.notification_center', 'mercury_ai.analysis.operational_history', 'mercury_ai.analysis.performance_analytics', 'mercury_ai.analysis.performance_center', 'mercury_ai.analysis.performance_engine', 'mercury_ai.analysis.performance_statistics', 'mercury_ai.analysis.price_action_engine', 'mercury_ai.analysis.provider_priority_engine', 'mercury_ai.analysis.replay_batch_processor', 'mercury_ai.analysis.replay_cache', 'mercury_ai.analysis.risk_engine', 'mercury_ai.analysis.statistical_auditor', 'mercury_ai.analysis.swing_engine', 'mercury_ai.analysis.volume_engine', 'mercury_ai.analysis.vwap_engine', 'mercury_ai.analysis.weight_simulator', 'mercury_ai.analysis.smart_money.liquidity_engine', 'mercury_ai.analysis.smart_money.smart_money_engine', 'mercury_ai.brain.mercury_decision_engine', 'mercury_ai.brain.probability_engine', 'mercury_ai.brain.scanner', 'mercury_ai.config.configuration_center', 'mercury_ai.core.analysis_pipeline', 'mercury_ai.core.asset_registry', 'mercury_ai.core.audit_sink', 'mercury_ai.core.auto_health', 'mercury_ai.core.export_center', 'mercury_ai.core.health_center', 'mercury_ai.core.job_manager', 'mercury_ai.core.observability_center', 'mercury_ai.core.pipeline_audit_middleware', 'mercury_ai.core.pipeline_executor', 'mercury_ai.core.pipeline_profiler', 'mercury_ai.core.project_state', 'mercury_ai.core.security_center', 'mercury_ai.core.session_manager', 'mercury_ai.core._stage_builder', 'mercury_ai.data.market_data', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.replay_data_provider', 'mercury_ai.data.providers.historical_data_provider', 'mercury_ai.database.history_logger', 'mercury_ai.database.replay_storage', 'mercury_ai.database.snapshot_logger', 'mercury_ai.market.market_engine', 'mercury_ai.operations.demo_manager', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_adapters', 'mercury_ai.providers.historical_replay_provider', 'mercury_ai.providers.market_provider', 'mercury_ai.utils.memory_auditor', 'mercury_ai.utils.performance_collector', 'mercury_ai.utils.regression_detector', 'mercury_ai.utils.report_generator', 'mercury_ai.utils.stress_tester', 'tests.test_robustness', 'tools.mercury_integrity_auditor.auditors.contract_auditor', 'tools.mercury_integrity_auditor.auditors.decision_auditor', 'tools.mercury_integrity_auditor.auditors.flow_auditor', 'tools.mercury_integrity_auditor.auditors.masking_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor', 'tools.project_mapper.snapshot_builder']

#### WARNING: _run_single_symbol

**Message:** Duplicate function name '_run_single_symbol' found in 2 modules

**Evidence:** Function '_run_single_symbol' defined in: mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.replay_batch_processor

**modules:** ['mercury_ai.analysis.benchmark_framework', 'mercury_ai.analysis.replay_batch_processor']

#### WARNING: analyze

**Message:** Duplicate function name 'analyze' found in 28 modules

**Evidence:** Function 'analyze' defined in: mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.session_engine, mercury_ai.analysis.support_resistance_analyzer, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.vwap_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.smart_money.order_block_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.core.analysis_pipeline, mercury_ai.core.base_engine

**modules:** ['mercury_ai.analysis.candlestick_engine', 'mercury_ai.analysis.confluence_engine', 'mercury_ai.analysis.context_engine', 'mercury_ai.analysis.fair_value_gap_engine', 'mercury_ai.analysis.market_condition_engine', 'mercury_ai.analysis.market_regime_engine', 'mercury_ai.analysis.market_state_engine', 'mercury_ai.analysis.momentum_engine', 'mercury_ai.analysis.mtf_engine', 'mercury_ai.analysis.price_action_analyzer', 'mercury_ai.analysis.price_action_engine', 'mercury_ai.analysis.session_engine', 'mercury_ai.analysis.support_resistance_analyzer', 'mercury_ai.analysis.trend_analyzer', 'mercury_ai.analysis.volatility_engine', 'mercury_ai.analysis.volume_engine', 'mercury_ai.analysis.vwap_engine', 'mercury_ai.analysis.smart_money.bos_engine', 'mercury_ai.analysis.smart_money.choch_engine', 'mercury_ai.analysis.smart_money.liquidity_engine', 'mercury_ai.analysis.smart_money.market_structure_engine', 'mercury_ai.analysis.smart_money.order_block_engine', 'mercury_ai.analysis.smart_money.smart_money_engine', 'mercury_ai.brain.explainability_engine', 'mercury_ai.brain.mercury_decision_engine', 'mercury_ai.brain.probability_engine', 'mercury_ai.core.analysis_pipeline', 'mercury_ai.core.base_engine']

#### WARNING: audit

**Message:** Duplicate function name 'audit' found in 2 modules

**Evidence:** Function 'audit' defined in: mercury_ai.analysis.confidence_calibration_auditor, mercury_ai.analysis.statistical_auditor

**modules:** ['mercury_ai.analysis.confidence_calibration_auditor', 'mercury_ai.analysis.statistical_auditor']

#### WARNING: calculate

**Message:** Duplicate function name 'calculate' found in 7 modules

**Evidence:** Function 'calculate' defined in: mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.institutional_score_engine, mercury_ai.analysis.metric_calculator, mercury_ai.analysis.performance_statistics, mercury_ai.data.indicator_engine, mercury_ai.indicators.rsi

**modules:** ['mercury_ai.analysis.confidence_engine', 'mercury_ai.analysis.confluence_score_engine', 'mercury_ai.analysis.institutional_score_engine', 'mercury_ai.analysis.metric_calculator', 'mercury_ai.analysis.performance_statistics', 'mercury_ai.data.indicator_engine', 'mercury_ai.indicators.rsi']

#### WARNING: resolve

**Message:** Duplicate function name 'resolve' found in 2 modules

**Evidence:** Function 'resolve' defined in: mercury_ai.analysis.conflict_resolution_engine, mercury_ai.analysis.decision_resolver_engine

**modules:** ['mercury_ai.analysis.conflict_resolution_engine', 'mercury_ai.analysis.decision_resolver_engine']

#### WARNING: _calculate_quality

**Message:** Duplicate function name '_calculate_quality' found in 2 modules

**Evidence:** Function '_calculate_quality' defined in: mercury_ai.analysis.context_engine, mercury_ai.analysis.session_engine

**modules:** ['mercury_ai.analysis.context_engine', 'mercury_ai.analysis.session_engine']

#### WARNING: evaluate

**Message:** Duplicate function name 'evaluate' found in 7 modules

**Evidence:** Function 'evaluate' defined in: mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.evidence_quality_engine, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.core.data_quality_gate

**modules:** ['mercury_ai.analysis.context_intelligence_engine', 'mercury_ai.analysis.evidence_quality_engine', 'mercury_ai.analysis.institutional_trade_filter_engine', 'mercury_ai.analysis.market_structure_intelligence_engine', 'mercury_ai.analysis.post_decision_evaluation_engine', 'mercury_ai.analysis.volume_intelligence_engine', 'mercury_ai.core.data_quality_gate']

#### WARNING: export_history

**Message:** Duplicate function name 'export_history' found in 2 modules

**Evidence:** Function 'export_history' defined in: mercury_ai.analysis.data_exporter, mercury_ai.core.export_center

**modules:** ['mercury_ai.analysis.data_exporter', 'mercury_ai.core.export_center']

#### WARNING: export_snapshots

**Message:** Duplicate function name 'export_snapshots' found in 2 modules

**Evidence:** Function 'export_snapshots' defined in: mercury_ai.analysis.data_exporter, mercury_ai.core.export_center

**modules:** ['mercury_ai.analysis.data_exporter', 'mercury_ai.core.export_center']

#### WARNING: generate_report

**Message:** Duplicate function name 'generate_report' found in 2 modules

**Evidence:** Function 'generate_report' defined in: mercury_ai.analysis.data_quality_engine, mercury_ai.analysis.health_auditor

**modules:** ['mercury_ai.analysis.data_quality_engine', 'mercury_ai.analysis.health_auditor']

#### WARNING: build

**Message:** Duplicate function name 'build' found in 5 modules

**Evidence:** Function 'build' defined in: mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_thesis_builder, tools.project_mapper.snapshot_builder

**modules:** ['mercury_ai.analysis.decision_result_builder', 'mercury_ai.analysis.institutional_context_builder', 'mercury_ai.analysis.market_context_builder', 'mercury_ai.analysis.market_thesis_builder', 'tools.project_mapper.snapshot_builder']

#### WARNING: rank

**Message:** Duplicate function name 'rank' found in 2 modules

**Evidence:** Function 'rank' defined in: mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.ranking_engine

**modules:** ['mercury_ai.analysis.evidence_ranking_engine', 'mercury_ai.analysis.ranking_engine']

#### WARNING: _analyze_logic

**Message:** Duplicate function name '_analyze_logic' found in 6 modules

**Evidence:** Function '_analyze_logic' defined in: mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.mercury_decision_engine

**modules:** ['mercury_ai.analysis.fair_value_gap_engine', 'mercury_ai.analysis.momentum_engine', 'mercury_ai.analysis.price_action_engine', 'mercury_ai.analysis.volume_engine', 'mercury_ai.analysis.vwap_engine', 'mercury_ai.brain.mercury_decision_engine']

#### WARNING: generate

**Message:** Duplicate function name 'generate' found in 3 modules

**Evidence:** Function 'generate' defined in: mercury_ai.analysis.institutional_report, mercury_ai.analysis.institutional_report_generator, mercury_ai.analysis.narrative_engine

**modules:** ['mercury_ai.analysis.institutional_report', 'mercury_ai.analysis.institutional_report_generator', 'mercury_ai.analysis.narrative_engine']

#### WARNING: start

**Message:** Duplicate function name 'start' found in 3 modules

**Evidence:** Function 'start' defined in: mercury_ai.analysis.live_monitor, mercury_ai.core.job_manager, mercury_ai.core.startup

**modules:** ['mercury_ai.analysis.live_monitor', 'mercury_ai.core.job_manager', 'mercury_ai.core.startup']

#### WARNING: stop

**Message:** Duplicate function name 'stop' found in 2 modules

**Evidence:** Function 'stop' defined in: mercury_ai.analysis.live_monitor, mercury_ai.core.job_manager

**modules:** ['mercury_ai.analysis.live_monitor', 'mercury_ai.core.job_manager']

#### WARNING: _build_explanation

**Message:** Duplicate function name '_build_explanation' found in 3 modules

**Evidence:** Function '_build_explanation' defined in: mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.session_engine, mercury_ai.analysis.support_resistance_analyzer

**modules:** ['mercury_ai.analysis.market_condition_engine', 'mercury_ai.analysis.session_engine', 'mercury_ai.analysis.support_resistance_analyzer']

#### WARNING: get_history

**Message:** Duplicate function name 'get_history' found in 5 modules

**Evidence:** Function 'get_history' defined in: mercury_ai.analysis.notification_center, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.analysis.notification_center', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: get

**Message:** Duplicate function name 'get' found in 3 modules

**Evidence:** Function 'get' defined in: mercury_ai.analysis.replay_cache, mercury_ai.config.configuration_center, mercury_ai.core.project_state

**modules:** ['mercury_ai.analysis.replay_cache', 'mercury_ai.config.configuration_center', 'mercury_ai.core.project_state']

#### WARNING: detect

**Message:** Duplicate function name 'detect' found in 2 modules

**Evidence:** Function 'detect' defined in: mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.utils.regression_detector

**modules:** ['mercury_ai.analysis.smart_money.liquidity_event_engine', 'mercury_ai.utils.regression_detector']

#### WARNING: create_mock_swing

**Message:** Duplicate function name 'create_mock_swing' found in 3 modules

**Evidence:** Function 'create_mock_swing' defined in: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration

**modules:** ['mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases', 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine', 'tests.test_benchmark_integration']

#### WARNING: engine

**Message:** Duplicate function name 'engine' found in 2 modules

**Evidence:** Function 'engine' defined in: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.tests.test_risk_engine

**modules:** ['mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases', 'mercury_ai.analysis.tests.test_risk_engine']

#### WARNING: test_determinism

**Message:** Duplicate function name 'test_determinism' found in 2 modules

**Evidence:** Function 'test_determinism' defined in: mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_determinism

**modules:** ['mercury_ai.analysis.smart_money.tests.test_liquidity_engine', 'tests.test_determinism']

#### WARNING: scan

**Message:** Duplicate function name 'scan' found in 3 modules

**Evidence:** Function 'scan' defined in: mercury_ai.brain.scanner, tools.scanner, tools.project_mapper.scanner

**modules:** ['mercury_ai.brain.scanner', 'tools.scanner', 'tools.project_mapper.scanner']

#### WARNING: get_events

**Message:** Duplicate function name 'get_events' found in 2 modules

**Evidence:** Function 'get_events' defined in: mercury_ai.calendar.economic_calendar, mercury_ai.core.audit_sink

**modules:** ['mercury_ai.calendar.economic_calendar', 'mercury_ai.core.audit_sink']

#### WARNING: _load_from_file

**Message:** Duplicate function name '_load_from_file' found in 2 modules

**Evidence:** Function '_load_from_file' defined in: mercury_ai.config.configuration_center, mercury_ai.core.asset_registry

**modules:** ['mercury_ai.config.configuration_center', 'mercury_ai.core.asset_registry']

#### WARNING: save

**Message:** Duplicate function name 'save' found in 7 modules

**Evidence:** Function 'save' defined in: mercury_ai.config.configuration_center, mercury_ai.core.asset_registry, mercury_ai.database.history_logger, mercury_ai.database.replay_storage, mercury_ai.database.snapshot_logger, tools.writer, tools.project_mapper.writer

**modules:** ['mercury_ai.config.configuration_center', 'mercury_ai.core.asset_registry', 'mercury_ai.database.history_logger', 'mercury_ai.database.replay_storage', 'mercury_ai.database.snapshot_logger', 'tools.writer', 'tools.project_mapper.writer']

#### WARNING: get_metrics

**Message:** Duplicate function name 'get_metrics' found in 2 modules

**Evidence:** Function 'get_metrics' defined in: mercury_ai.core.observability_center, mercury_ai.utils.system_monitor

**modules:** ['mercury_ai.core.observability_center', 'mercury_ai.utils.system_monitor']

#### WARNING: stage

**Message:** Duplicate function name 'stage' found in 3 modules

**Evidence:** Function 'stage' defined in: mercury_ai.core.pipeline_executor, mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector

**modules:** ['mercury_ai.core.pipeline_executor', 'mercury_ai.core.pipeline_profiler', 'mercury_ai.utils.performance_collector']

#### WARNING: summary

**Message:** Duplicate function name 'summary' found in 2 modules

**Evidence:** Function 'summary' defined in: mercury_ai.core.pipeline_profiler, mercury_ai.core.project_state

**modules:** ['mercury_ai.core.pipeline_profiler', 'mercury_ai.core.project_state']

#### WARNING: json

**Message:** Duplicate function name 'json' found in 2 modules

**Evidence:** Function 'json' defined in: mercury_ai.core.pipeline_profiler, mercury_ai.core.project_state

**modules:** ['mercury_ai.core.pipeline_profiler', 'mercury_ai.core.project_state']

#### WARNING: connect

**Message:** Duplicate function name 'connect' found in 4 modules

**Evidence:** Function 'connect' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: health

**Message:** Duplicate function name 'health' found in 4 modules

**Evidence:** Function 'health' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: get_last_price

**Message:** Duplicate function name 'get_last_price' found in 4 modules

**Evidence:** Function 'get_last_price' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: get_candles

**Message:** Duplicate function name 'get_candles' found in 4 modules

**Evidence:** Function 'get_candles' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: market_status

**Message:** Duplicate function name 'market_status' found in 4 modules

**Evidence:** Function 'market_status' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: register_provider

**Message:** Duplicate function name 'register_provider' found in 2 modules

**Evidence:** Function 'register_provider' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: _get_best_provider

**Message:** Duplicate function name '_get_best_provider' found in 2 modules

**Evidence:** Function '_get_best_provider' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: list_providers

**Message:** Duplicate function name 'list_providers' found in 2 modules

**Evidence:** Function 'list_providers' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: best_provider

**Message:** Duplicate function name 'best_provider' found in 2 modules

**Evidence:** Function 'best_provider' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: healthcheck

**Message:** Duplicate function name 'healthcheck' found in 3 modules

**Evidence:** Function 'healthcheck' defined in: mercury_ai.data.mercury_data_provider, mercury_ai.data.mercury_data_provider, mercury_ai.providers.market_provider

**modules:** ['mercury_ai.data.mercury_data_provider', 'mercury_ai.data.mercury_data_provider', 'mercury_ai.providers.market_provider']

#### WARNING: set_index

**Message:** Duplicate function name 'set_index' found in 2 modules

**Evidence:** Function 'set_index' defined in: mercury_ai.data.providers.historical_data_provider, mercury_ai.providers.historical_replay_provider

**modules:** ['mercury_ai.data.providers.historical_data_provider', 'mercury_ai.providers.historical_replay_provider']

#### WARNING: check_health

**Message:** Duplicate function name 'check_health' found in 2 modules

**Evidence:** Function 'check_health' defined in: mercury_ai.providers.data_adapters, mercury_ai.providers.data_interfaces

**modules:** ['mercury_ai.providers.data_adapters', 'mercury_ai.providers.data_interfaces']

#### WARNING: run

**Message:** Duplicate function name 'run' found in 24 modules

**Evidence:** Function 'run' defined in: mercury_ai.utils.stress_tester, tools.mercury_integrity_auditor.auditors.backtest_auditor, tools.mercury_integrity_auditor.auditors.contract_auditor, tools.mercury_integrity_auditor.auditors.coverage_auditor, tools.mercury_integrity_auditor.auditors.data_auditor, tools.mercury_integrity_auditor.auditors.decision_auditor, tools.mercury_integrity_auditor.auditors.dependency_auditor, tools.mercury_integrity_auditor.auditors.determinism_auditor, tools.mercury_integrity_auditor.auditors.explainability_auditor, tools.mercury_integrity_auditor.auditors.flow_auditor, tools.mercury_integrity_auditor.auditors.global_state_auditor, tools.mercury_integrity_auditor.auditors.integrity_auditor, tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.performance_auditor, tools.mercury_integrity_auditor.auditors.report, tools.mercury_integrity_auditor.auditors.runtime_auditor, tools.mercury_integrity_auditor.auditors.static_auditor, tools.mercury_integrity_auditor.auditors.test_auditor, tools.mercury_integrity_auditor.auditors.universe_auditor, tools.project_mapper.architecture_audit, tools.project_mapper.call_graph_builder, tools.project_mapper.dependency_builder, tools.project_mapper.module_index, tools.project_mapper.python_indexer

**modules:** ['mercury_ai.utils.stress_tester', 'tools.mercury_integrity_auditor.auditors.backtest_auditor', 'tools.mercury_integrity_auditor.auditors.contract_auditor', 'tools.mercury_integrity_auditor.auditors.coverage_auditor', 'tools.mercury_integrity_auditor.auditors.data_auditor', 'tools.mercury_integrity_auditor.auditors.decision_auditor', 'tools.mercury_integrity_auditor.auditors.dependency_auditor', 'tools.mercury_integrity_auditor.auditors.determinism_auditor', 'tools.mercury_integrity_auditor.auditors.explainability_auditor', 'tools.mercury_integrity_auditor.auditors.flow_auditor', 'tools.mercury_integrity_auditor.auditors.global_state_auditor', 'tools.mercury_integrity_auditor.auditors.integrity_auditor', 'tools.mercury_integrity_auditor.auditors.masking_auditor', 'tools.mercury_integrity_auditor.auditors.performance_auditor', 'tools.mercury_integrity_auditor.auditors.report', 'tools.mercury_integrity_auditor.auditors.runtime_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor', 'tools.mercury_integrity_auditor.auditors.test_auditor', 'tools.mercury_integrity_auditor.auditors.universe_auditor', 'tools.project_mapper.architecture_audit', 'tools.project_mapper.call_graph_builder', 'tools.project_mapper.dependency_builder', 'tools.project_mapper.module_index', 'tools.project_mapper.python_indexer']

#### WARNING: base_context

**Message:** Duplicate function name 'base_context' found in 2 modules

**Evidence:** Function 'base_context' defined in: tests.test_adaptive_weighting, tests.test_confidence_calibration

**modules:** ['tests.test_adaptive_weighting', 'tests.test_confidence_calibration']

#### WARNING: visit_ClassDef

**Message:** Duplicate function name 'visit_ClassDef' found in 3 modules

**Evidence:** Function 'visit_ClassDef' defined in: tools.mercury_integrity_auditor.auditors.contract_auditor, tools.mercury_integrity_auditor.auditors.flow_auditor, tools.mercury_integrity_auditor.auditors.static_auditor

**modules:** ['tools.mercury_integrity_auditor.auditors.contract_auditor', 'tools.mercury_integrity_auditor.auditors.flow_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor']

#### WARNING: visit_Call

**Message:** Duplicate function name 'visit_Call' found in 2 modules

**Evidence:** Function 'visit_Call' defined in: tools.mercury_integrity_auditor.auditors.decision_auditor, tools.mercury_integrity_auditor.auditors.masking_auditor

**modules:** ['tools.mercury_integrity_auditor.auditors.decision_auditor', 'tools.mercury_integrity_auditor.auditors.masking_auditor']

#### WARNING: visit_FunctionDef

**Message:** Duplicate function name 'visit_FunctionDef' found in 2 modules

**Evidence:** Function 'visit_FunctionDef' defined in: tools.mercury_integrity_auditor.auditors.flow_auditor, tools.mercury_integrity_auditor.auditors.static_auditor

**modules:** ['tools.mercury_integrity_auditor.auditors.flow_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor']

#### WARNING: visit_Import

**Message:** Duplicate function name 'visit_Import' found in 2 modules

**Evidence:** Function 'visit_Import' defined in: tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.static_auditor

**modules:** ['tools.mercury_integrity_auditor.auditors.masking_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor']

#### WARNING: visit_ImportFrom

**Message:** Duplicate function name 'visit_ImportFrom' found in 2 modules

**Evidence:** Function 'visit_ImportFrom' defined in: tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.static_auditor

**modules:** ['tools.mercury_integrity_auditor.auditors.masking_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor']

#### WARNING: visit_ExceptHandler

**Message:** Duplicate function name 'visit_ExceptHandler' found in 2 modules

**Evidence:** Function 'visit_ExceptHandler' defined in: tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.static_auditor

**modules:** ['tools.mercury_integrity_auditor.auditors.masking_auditor', 'tools.mercury_integrity_auditor.auditors.static_auditor']

### EXCESSIVE_COUPLING_FANIN (7 findings)

#### WARNING: mercury_ai.core.analysis_pipeline.AnalysisPipeline

**Message:** God module: Module 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' has fan-in of 16 (exceeds 15)

**Evidence:** Module 'mercury_ai.core.analysis_pipeline.AnalysisPipeline' is depended upon by 16 other modules

**fan_in:** 16

#### WARNING: mercury_ai.data.market_data.MarketDataService

**Message:** God module: Module 'mercury_ai.data.market_data.MarketDataService' has fan-in of 20 (exceeds 15)

**Evidence:** Module 'mercury_ai.data.market_data.MarketDataService' is depended upon by 20 other modules

**fan_in:** 20

#### WARNING: mercury_ai.models.market_context.MarketContext

**Message:** God module: Module 'mercury_ai.models.market_context.MarketContext' has fan-in of 29 (exceeds 15)

**Evidence:** Module 'mercury_ai.models.market_context.MarketContext' is depended upon by 29 other modules

**fan_in:** 29

#### WARNING: mercury_ai.models.evidence.Evidence

**Message:** God module: Module 'mercury_ai.models.evidence.Evidence' has fan-in of 50 (exceeds 15)

**Evidence:** Module 'mercury_ai.models.evidence.Evidence' is depended upon by 50 other modules

**fan_in:** 50

#### WARNING: mercury_ai.models.market_data.MarketData

**Message:** God module: Module 'mercury_ai.models.market_data.MarketData' has fan-in of 16 (exceeds 15)

**Evidence:** Module 'mercury_ai.models.market_data.MarketData' is depended upon by 16 other modules

**fan_in:** 16

#### WARNING: mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

**Message:** God module: Module 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' has fan-in of 17 (exceeds 15)

**Evidence:** Module 'mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle' is depended upon by 17 other modules

**fan_in:** 17

#### WARNING: mercury_ai.core.pipeline_executor.PipelineExecutor

**Message:** God module: Module 'mercury_ai.core.pipeline_executor.PipelineExecutor' has fan-in of 21 (exceeds 15)

**Evidence:** Module 'mercury_ai.core.pipeline_executor.PipelineExecutor' is depended upon by 21 other modules

**fan_in:** 21

### EXCESSIVE_COUPLING_FANOUT (4 findings)

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Excessive coupling: Module 'mercury_ai.analysis.risk_engine' has fan-out of 22 (exceeds 20)

**Evidence:** Module 'mercury_ai.analysis.risk_engine' depends on 22 internal modules

**fan_out:** 22

#### WARNING: mercury_ai.brain.mercury_decision_engine

**Message:** Excessive coupling: Module 'mercury_ai.brain.mercury_decision_engine' has fan-out of 25 (exceeds 20)

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' depends on 25 internal modules

**fan_out:** 25

#### WARNING: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Excessive coupling: Module 'mercury_ai.brain.tests.test_mercury_decision_engine' has fan-out of 22 (exceeds 20)

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' depends on 22 internal modules

**fan_out:** 22

#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** Excessive coupling: Module 'mercury_ai.core.analysis_pipeline' has fan-out of 48 (exceeds 20)

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' depends on 48 internal modules

**fan_out:** 48

### HIDDEN_DEPENDENCY (60 findings)

#### WARNING: validate_universe_parity

**Message:** Potentially unused import: 'mercury_ai.config.universe.ALL_SYMBOLS' in 'validate_universe_parity'

**Evidence:** Import 'mercury_ai.config.universe.ALL_SYMBOLS' in module 'validate_universe_parity' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### WARNING: app.dashboard.dashboard

**Message:** Potentially unused import: 'app.ui_utils.display_metric' in 'app.dashboard.dashboard'

**Evidence:** Import 'app.ui_utils.display_metric' in module 'app.dashboard.dashboard' does not appear to be used in call graph or class hierarchy

**import:** app.ui_utils.display_metric

#### WARNING: app.dashboard.dashboard

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'app.dashboard.dashboard'

**Evidence:** Import 'mercury_ai.config.settings' in module 'app.dashboard.dashboard' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: app.dashboard.operation_center

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'app.dashboard.operation_center'

**Evidence:** Import 'mercury_ai.config.settings' in module 'app.dashboard.operation_center' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: app.terminal.terminal

**Message:** Potentially unused import: 'app.ui_utils.display_status' in 'app.terminal.terminal'

**Evidence:** Import 'app.ui_utils.display_status' in module 'app.terminal.terminal' does not appear to be used in call graph or class hierarchy

**import:** app.ui_utils.display_status

#### WARNING: app.terminal.terminal

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'app.terminal.terminal'

**Evidence:** Import 'mercury_ai.config.settings' in module 'app.terminal.terminal' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: app.terminal.pages.01_Scanner

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'app.terminal.pages.01_Scanner'

**Evidence:** Import 'mercury_ai.config.settings' in module 'app.terminal.pages.01_Scanner' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: app.terminal.pages.04_Auditoria_Configuracoes

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'app.terminal.pages.04_Auditoria_Configuracoes'

**Evidence:** Import 'mercury_ai.config.settings' in module 'app.terminal.pages.04_Auditoria_Configuracoes' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: app.terminal.pages.06_Demo

**Message:** Potentially unused import: 'mercury_ai.config.assets.SUPPORTED_ASSETS' in 'app.terminal.pages.06_Demo'

**Evidence:** Import 'mercury_ai.config.assets.SUPPORTED_ASSETS' in module 'app.terminal.pages.06_Demo' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.assets.SUPPORTED_ASSETS

#### WARNING: mercury_ai.analysis.confluence_engine

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' in 'mercury_ai.analysis.confluence_engine'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' in module 'mercury_ai.analysis.confluence_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS

#### WARNING: mercury_ai.analysis.confluence_engine

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' in 'mercury_ai.analysis.confluence_engine'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' in module 'mercury_ai.analysis.confluence_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM

#### WARNING: mercury_ai.analysis.confluence_score_engine

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' in 'mercury_ai.analysis.confluence_score_engine'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' in module 'mercury_ai.analysis.confluence_score_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS

#### WARNING: mercury_ai.analysis.health_checker

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'mercury_ai.analysis.health_checker'

**Evidence:** Import 'mercury_ai.config.settings' in module 'mercury_ai.analysis.health_checker' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: mercury_ai.analysis.mtf_engine

**Message:** Potentially unused import: 'mercury_ai.config.timeframes.YFINANCE_INTERVALS' in 'mercury_ai.analysis.mtf_engine'

**Evidence:** Import 'mercury_ai.config.timeframes.YFINANCE_INTERVALS' in module 'mercury_ai.analysis.mtf_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.timeframes.YFINANCE_INTERVALS

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Potentially unused import: 'mercury_ai.config.risk.VAR_CONFIDENCE_95' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Import 'mercury_ai.config.risk.VAR_CONFIDENCE_95' in module 'mercury_ai.analysis.risk_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.risk.VAR_CONFIDENCE_95

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Potentially unused import: 'mercury_ai.config.risk.VAR_CONFIDENCE_99' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Import 'mercury_ai.config.risk.VAR_CONFIDENCE_99' in module 'mercury_ai.analysis.risk_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.risk.VAR_CONFIDENCE_99

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Potentially unused import: 'mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Import 'mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE' in module 'mercury_ai.analysis.risk_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Potentially unused import: 'mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Import 'mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF' in module 'mercury_ai.analysis.risk_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Potentially unused import: 'mercury_ai.config.risk.KELLY_MAX_FRACTION' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Import 'mercury_ai.config.risk.KELLY_MAX_FRACTION' in module 'mercury_ai.analysis.risk_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.risk.KELLY_MAX_FRACTION

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Potentially unused import: 'mercury_ai.config.risk.STRESS_SCENARIOS' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Import 'mercury_ai.config.risk.STRESS_SCENARIOS' in module 'mercury_ai.analysis.risk_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.risk.STRESS_SCENARIOS

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Potentially unused import: 'mercury_ai.config.sessions' in 'mercury_ai.analysis.session_engine'

**Evidence:** Import 'mercury_ai.config.sessions' in module 'mercury_ai.analysis.session_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.sessions

#### WARNING: mercury_ai.brain.mercury_decision_engine

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' in 'mercury_ai.brain.mercury_decision_engine'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' in module 'mercury_ai.brain.mercury_decision_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.OPERATIONAL_UNIVERSE' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.OPERATIONAL_UNIVERSE' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.OPERATIONAL_UNIVERSE

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.FOREX_UNIVERSE' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.FOREX_UNIVERSE' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.FOREX_UNIVERSE

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.CRYPTO_UNIVERSE' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.CRYPTO_UNIVERSE' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.CRYPTO_UNIVERSE

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.STOCK_UNIVERSE' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.STOCK_UNIVERSE' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.STOCK_UNIVERSE

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.COMMODITY_UNIVERSE' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.COMMODITY_UNIVERSE' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.COMMODITY_UNIVERSE

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.FOREX_SYMBOLS' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.FOREX_SYMBOLS' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.FOREX_SYMBOLS

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.CRYPTO_SYMBOLS' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.CRYPTO_SYMBOLS' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.CRYPTO_SYMBOLS

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.STOCK_SYMBOLS' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.STOCK_SYMBOLS' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.STOCK_SYMBOLS

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.COMMODITY_SYMBOLS' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.COMMODITY_SYMBOLS' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.COMMODITY_SYMBOLS

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.ALL_SYMBOLS' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.ALL_SYMBOLS' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.SUPPORTED_ASSETS' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.SUPPORTED_ASSETS' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.SUPPORTED_ASSETS

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.get_asset' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.get_asset' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.get_asset

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.get_enabled_symbols' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.get_enabled_symbols' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.get_enabled_symbols

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.get_all_provider_symbols' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.get_all_provider_symbols' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.get_all_provider_symbols

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.validate_symbol' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.validate_symbol' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.validate_symbol

#### WARNING: mercury_ai.config.assets

**Message:** Potentially unused import: 'mercury_ai.config.universe.universe_summary' in 'mercury_ai.config.assets'

**Evidence:** Import 'mercury_ai.config.universe.universe_summary' in module 'mercury_ai.config.assets' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.universe_summary

#### WARNING: mercury_ai.config.configuration_center

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'mercury_ai.config.configuration_center'

**Evidence:** Import 'mercury_ai.config.settings' in module 'mercury_ai.config.configuration_center' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: mercury_ai.config.__init__

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' in 'mercury_ai.config.__init__'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS' in module 'mercury_ai.config.__init__' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS

#### WARNING: mercury_ai.config.__init__

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' in 'mercury_ai.config.__init__'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED' in module 'mercury_ai.config.__init__' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED

#### WARNING: mercury_ai.config.__init__

**Message:** Potentially unused import: 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' in 'mercury_ai.config.__init__'

**Evidence:** Import 'mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM' in module 'mercury_ai.config.__init__' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM

#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** Potentially unused import: 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' in 'mercury_ai.core.analysis_pipeline'

**Evidence:** Import 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' in module 'mercury_ai.core.analysis_pipeline' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.timeframes.DEFAULT_TIMEFRAME

#### WARNING: mercury_ai.core.job_manager

**Message:** Potentially unused import: 'mercury_ai.config.assets.SUPPORTED_ASSETS' in 'mercury_ai.core.job_manager'

**Evidence:** Import 'mercury_ai.config.assets.SUPPORTED_ASSETS' in module 'mercury_ai.core.job_manager' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.assets.SUPPORTED_ASSETS

#### WARNING: mercury_ai.core.session_manager

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'mercury_ai.core.session_manager'

**Evidence:** Import 'mercury_ai.config.settings' in module 'mercury_ai.core.session_manager' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: mercury_ai.core.startup

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'mercury_ai.core.startup'

**Evidence:** Import 'mercury_ai.config.settings' in module 'mercury_ai.core.startup' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: mercury_ai.market.market_engine

**Message:** Potentially unused import: 'mercury_ai.config.settings.ASSET' in 'mercury_ai.market.market_engine'

**Evidence:** Import 'mercury_ai.config.settings.ASSET' in module 'mercury_ai.market.market_engine' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings.ASSET

#### WARNING: mercury_ai.models.analysis_result

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'mercury_ai.models.analysis_result'

**Evidence:** Import 'mercury_ai.config.settings' in module 'mercury_ai.models.analysis_result' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: mercury_ai.models.decision_snapshot

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'mercury_ai.models.decision_snapshot'

**Evidence:** Import 'mercury_ai.config.settings' in module 'mercury_ai.models.decision_snapshot' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

#### WARNING: mercury_ai.models.evidence

**Message:** Potentially unused import: 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' in 'mercury_ai.models.evidence'

**Evidence:** Import 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' in module 'mercury_ai.models.evidence' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.timeframes.DEFAULT_TIMEFRAME

#### WARNING: mercury_ai.models.signal

**Message:** Potentially unused import: 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' in 'mercury_ai.models.signal'

**Evidence:** Import 'mercury_ai.config.timeframes.DEFAULT_TIMEFRAME' in module 'mercury_ai.models.signal' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.timeframes.DEFAULT_TIMEFRAME

#### WARNING: mercury_ai.operations.demo_manager

**Message:** Potentially unused import: 'mercury_ai.config.assets.SUPPORTED_ASSETS' in 'mercury_ai.operations.demo_manager'

**Evidence:** Import 'mercury_ai.config.assets.SUPPORTED_ASSETS' in module 'mercury_ai.operations.demo_manager' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.assets.SUPPORTED_ASSETS

#### WARNING: mercury_ai.providers.data_adapters

**Message:** Potentially unused import: 'mercury_ai.config.universe.ALL_SYMBOLS' in 'mercury_ai.providers.data_adapters'

**Evidence:** Import 'mercury_ai.config.universe.ALL_SYMBOLS' in module 'mercury_ai.providers.data_adapters' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### WARNING: mercury_ai.providers.data_adapters

**Message:** Potentially unused import: 'mercury_ai.config.universe.FOREX_SYMBOLS' in 'mercury_ai.providers.data_adapters'

**Evidence:** Import 'mercury_ai.config.universe.FOREX_SYMBOLS' in module 'mercury_ai.providers.data_adapters' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.FOREX_SYMBOLS

#### WARNING: mercury_ai.providers.data_adapters

**Message:** Potentially unused import: 'mercury_ai.config.universe.CRYPTO_SYMBOLS' in 'mercury_ai.providers.data_adapters'

**Evidence:** Import 'mercury_ai.config.universe.CRYPTO_SYMBOLS' in module 'mercury_ai.providers.data_adapters' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.CRYPTO_SYMBOLS

#### WARNING: mercury_ai.sessions.market_sessions

**Message:** Potentially unused import: 'mercury_ai.config.sessions' in 'mercury_ai.sessions.market_sessions'

**Evidence:** Import 'mercury_ai.config.sessions' in module 'mercury_ai.sessions.market_sessions' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.sessions

#### WARNING: scripts.prepare_replay_data

**Message:** Potentially unused import: 'mercury_ai.config.universe.ALL_SYMBOLS' in 'scripts.prepare_replay_data'

**Evidence:** Import 'mercury_ai.config.universe.ALL_SYMBOLS' in module 'scripts.prepare_replay_data' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.ALL_SYMBOLS

#### WARNING: scripts.prepare_replay_data

**Message:** Potentially unused import: 'mercury_ai.config.universe.FOREX_SYMBOLS' in 'scripts.prepare_replay_data'

**Evidence:** Import 'mercury_ai.config.universe.FOREX_SYMBOLS' in module 'scripts.prepare_replay_data' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.FOREX_SYMBOLS

#### WARNING: scripts.prepare_replay_data

**Message:** Potentially unused import: 'mercury_ai.config.universe.CRYPTO_SYMBOLS' in 'scripts.prepare_replay_data'

**Evidence:** Import 'mercury_ai.config.universe.CRYPTO_SYMBOLS' in module 'scripts.prepare_replay_data' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.universe.CRYPTO_SYMBOLS

#### WARNING: tests.test_versioning

**Message:** Potentially unused import: 'mercury_ai.config.settings' in 'tests.test_versioning'

**Evidence:** Import 'mercury_ai.config.settings' in module 'tests.test_versioning' does not appear to be used in call graph or class hierarchy

**import:** mercury_ai.config.settings

### LSP_CONCERN (15 findings)

#### INFO: mercury_ai.analysis.candlestick_engine

**Message:** LSP concern: Class 'CandlestickEngine' overrides 1 methods from 'BaseEngine'

**Evidence:** Class 'CandlestickEngine' in 'mercury_ai.analysis.candlestick_engine' overrides methods: analyze

**class:** CandlestickEngine
**base_class:** BaseEngine
**overlapping_methods:** ['analyze']

#### INFO: mercury_ai.core.audit_sink

**Message:** LSP concern: Class 'MemoryAuditSink' overrides 3 methods from 'AuditSink'

**Evidence:** Class 'MemoryAuditSink' in 'mercury_ai.core.audit_sink' overrides methods: log, __init__, get_events

**class:** MemoryAuditSink
**base_class:** AuditSink
**overlapping_methods:** ['log', '__init__', 'get_events']

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** LSP concern: Class 'YahooProvider' overrides 15 methods from 'BaseProvider'

**Evidence:** Class 'YahooProvider' in 'mercury_ai.data.mercury_data_provider' overrides methods: health, get_history, best_provider, trigger_failover, get_candles

**class:** YahooProvider
**base_class:** BaseProvider
**overlapping_methods:** ['health', 'get_history', 'best_provider', 'trigger_failover', 'get_candles']

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** LSP concern: Class 'PolygonProvider' overrides 15 methods from 'BaseProvider'

**Evidence:** Class 'PolygonProvider' in 'mercury_ai.data.mercury_data_provider' overrides methods: health, get_history, best_provider, trigger_failover, get_candles

**class:** PolygonProvider
**base_class:** BaseProvider
**overlapping_methods:** ['health', 'get_history', 'best_provider', 'trigger_failover', 'get_candles']

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** LSP concern: Class 'TwelveDataProvider' overrides 15 methods from 'BaseProvider'

**Evidence:** Class 'TwelveDataProvider' in 'mercury_ai.data.mercury_data_provider' overrides methods: health, get_history, best_provider, trigger_failover, get_candles

**class:** TwelveDataProvider
**base_class:** BaseProvider
**overlapping_methods:** ['health', 'get_history', 'best_provider', 'trigger_failover', 'get_candles']

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** LSP concern: Class 'AlphaVantageProvider' overrides 15 methods from 'BaseProvider'

**Evidence:** Class 'AlphaVantageProvider' in 'mercury_ai.data.mercury_data_provider' overrides methods: health, get_history, best_provider, trigger_failover, get_candles

**class:** AlphaVantageProvider
**base_class:** BaseProvider
**overlapping_methods:** ['health', 'get_history', 'best_provider', 'trigger_failover', 'get_candles']

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** LSP concern: Class 'BinanceProvider' overrides 15 methods from 'BaseProvider'

**Evidence:** Class 'BinanceProvider' in 'mercury_ai.data.mercury_data_provider' overrides methods: health, get_history, best_provider, trigger_failover, get_candles

**class:** BinanceProvider
**base_class:** BaseProvider
**overlapping_methods:** ['health', 'get_history', 'best_provider', 'trigger_failover', 'get_candles']

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** LSP concern: Class 'MetaTrader5Provider' overrides 15 methods from 'BaseProvider'

**Evidence:** Class 'MetaTrader5Provider' in 'mercury_ai.data.mercury_data_provider' overrides methods: health, get_history, best_provider, trigger_failover, get_candles

**class:** MetaTrader5Provider
**base_class:** BaseProvider
**overlapping_methods:** ['health', 'get_history', 'best_provider', 'trigger_failover', 'get_candles']

#### INFO: mercury_ai.providers.data_adapters

**Message:** LSP concern: Class 'YahooAdapter' overrides 3 methods from 'BaseAdapter'

**Evidence:** Class 'YahooAdapter' in 'mercury_ai.providers.data_adapters' overrides methods: get_data, __init__, check_health

**class:** YahooAdapter
**base_class:** BaseAdapter
**overlapping_methods:** ['get_data', '__init__', 'check_health']

#### INFO: mercury_ai.providers.data_adapters

**Message:** LSP concern: Class 'PolygonAdapter' overrides 3 methods from 'BaseAdapter'

**Evidence:** Class 'PolygonAdapter' in 'mercury_ai.providers.data_adapters' overrides methods: get_data, __init__, check_health

**class:** PolygonAdapter
**base_class:** BaseAdapter
**overlapping_methods:** ['get_data', '__init__', 'check_health']

#### INFO: mercury_ai.providers.data_adapters

**Message:** LSP concern: Class 'TwelveDataAdapter' overrides 3 methods from 'BaseAdapter'

**Evidence:** Class 'TwelveDataAdapter' in 'mercury_ai.providers.data_adapters' overrides methods: get_data, __init__, check_health

**class:** TwelveDataAdapter
**base_class:** BaseAdapter
**overlapping_methods:** ['get_data', '__init__', 'check_health']

#### INFO: mercury_ai.providers.data_adapters

**Message:** LSP concern: Class 'AlphaVantageAdapter' overrides 3 methods from 'BaseAdapter'

**Evidence:** Class 'AlphaVantageAdapter' in 'mercury_ai.providers.data_adapters' overrides methods: get_data, __init__, check_health

**class:** AlphaVantageAdapter
**base_class:** BaseAdapter
**overlapping_methods:** ['get_data', '__init__', 'check_health']

#### INFO: mercury_ai.providers.data_adapters

**Message:** LSP concern: Class 'BinanceAdapter' overrides 3 methods from 'BaseAdapter'

**Evidence:** Class 'BinanceAdapter' in 'mercury_ai.providers.data_adapters' overrides methods: get_data, __init__, check_health

**class:** BinanceAdapter
**base_class:** BaseAdapter
**overlapping_methods:** ['get_data', '__init__', 'check_health']

#### INFO: mercury_ai.providers.data_adapters

**Message:** LSP concern: Class 'MetaTrader5Adapter' overrides 3 methods from 'BaseAdapter'

**Evidence:** Class 'MetaTrader5Adapter' in 'mercury_ai.providers.data_adapters' overrides methods: get_data, __init__, check_health

**class:** MetaTrader5Adapter
**base_class:** BaseAdapter
**overlapping_methods:** ['get_data', '__init__', 'check_health']

#### INFO: tests.test_robustness

**Message:** LSP concern: Class 'RobustnessMarketDataProvider' overrides 1 methods from 'MarketDataProvider'

**Evidence:** Class 'RobustnessMarketDataProvider' in 'tests.test_robustness' overrides methods: get_data

**class:** RobustnessMarketDataProvider
**base_class:** MarketDataProvider
**overlapping_methods:** ['get_data']

### OCP_VIOLATION (72 findings)

#### INFO: run_instrumented

**Message:** OCP concern: Class 'MockProvider' has no inheritance hierarchy

**Evidence:** Class 'MockProvider' in 'run_instrumented' has no subclasses and no base classes, limiting extensibility

**class:** MockProvider

#### INFO: mercury_ai.analysis.benchmark_framework

**Message:** OCP concern: Class 'StatisticalTestResult' has no inheritance hierarchy

**Evidence:** Class 'StatisticalTestResult' in 'mercury_ai.analysis.benchmark_framework' has no subclasses and no base classes, limiting extensibility

**class:** StatisticalTestResult

#### INFO: mercury_ai.analysis.benchmark_framework

**Message:** OCP concern: Class 'BuyAndHoldBaseline' has no inheritance hierarchy

**Evidence:** Class 'BuyAndHoldBaseline' in 'mercury_ai.analysis.benchmark_framework' has no subclasses and no base classes, limiting extensibility

**class:** BuyAndHoldBaseline

#### INFO: mercury_ai.analysis.benchmark_framework

**Message:** OCP concern: Class 'EnhancedBenchmarkReport' has no inheritance hierarchy

**Evidence:** Class 'EnhancedBenchmarkReport' in 'mercury_ai.analysis.benchmark_framework' has no subclasses and no base classes, limiting extensibility

**class:** EnhancedBenchmarkReport

#### INFO: mercury_ai.analysis.benchmark_framework

**Message:** OCP concern: Class 'MercuryBenchmarkFramework' has no inheritance hierarchy

**Evidence:** Class 'MercuryBenchmarkFramework' in 'mercury_ai.analysis.benchmark_framework' has no subclasses and no base classes, limiting extensibility

**class:** MercuryBenchmarkFramework

#### INFO: mercury_ai.analysis.context_engine

**Message:** OCP concern: Class 'ContextEngine' has no inheritance hierarchy

**Evidence:** Class 'ContextEngine' in 'mercury_ai.analysis.context_engine' has no subclasses and no base classes, limiting extensibility

**class:** ContextEngine

#### INFO: mercury_ai.analysis.evidence_engine

**Message:** OCP concern: Class 'EvidenceEngine' has no inheritance hierarchy

**Evidence:** Class 'EvidenceEngine' in 'mercury_ai.analysis.evidence_engine' has no subclasses and no base classes, limiting extensibility

**class:** EvidenceEngine

#### INFO: mercury_ai.analysis.institutional_analytics_engine

**Message:** OCP concern: Class 'InstitutionalAnalyticsEngine' has no inheritance hierarchy

**Evidence:** Class 'InstitutionalAnalyticsEngine' in 'mercury_ai.analysis.institutional_analytics_engine' has no subclasses and no base classes, limiting extensibility

**class:** InstitutionalAnalyticsEngine

#### INFO: mercury_ai.analysis.institutional_memory_engine

**Message:** OCP concern: Class 'InstitutionalMemoryEngine' has no inheritance hierarchy

**Evidence:** Class 'InstitutionalMemoryEngine' in 'mercury_ai.analysis.institutional_memory_engine' has no subclasses and no base classes, limiting extensibility

**class:** InstitutionalMemoryEngine

#### INFO: mercury_ai.analysis.market_condition_engine

**Message:** OCP concern: Class 'MarketConditionEngine' has no inheritance hierarchy

**Evidence:** Class 'MarketConditionEngine' in 'mercury_ai.analysis.market_condition_engine' has no subclasses and no base classes, limiting extensibility

**class:** MarketConditionEngine

#### INFO: mercury_ai.analysis.performance_engine

**Message:** OCP concern: Class 'PerformanceEngine' has no inheritance hierarchy

**Evidence:** Class 'PerformanceEngine' in 'mercury_ai.analysis.performance_engine' has no subclasses and no base classes, limiting extensibility

**class:** PerformanceEngine

#### INFO: mercury_ai.analysis.replay_cache

**Message:** OCP concern: Class 'ReplayCache' has no inheritance hierarchy

**Evidence:** Class 'ReplayCache' in 'mercury_ai.analysis.replay_cache' has no subclasses and no base classes, limiting extensibility

**class:** ReplayCache

#### INFO: mercury_ai.analysis.risk_engine

**Message:** OCP concern: Class 'RiskEngine' has no inheritance hierarchy

**Evidence:** Class 'RiskEngine' in 'mercury_ai.analysis.risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** RiskEngine

#### INFO: mercury_ai.analysis.session_engine

**Message:** OCP concern: Class 'SessionEngine' has no inheritance hierarchy

**Evidence:** Class 'SessionEngine' in 'mercury_ai.analysis.session_engine' has no subclasses and no base classes, limiting extensibility

**class:** SessionEngine

#### INFO: mercury_ai.analysis.support_resistance_analyzer

**Message:** OCP concern: Class 'SupportResistanceAnalyzer' has no inheritance hierarchy

**Evidence:** Class 'SupportResistanceAnalyzer' in 'mercury_ai.analysis.support_resistance_analyzer' has no subclasses and no base classes, limiting extensibility

**class:** SupportResistanceAnalyzer

#### INFO: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** OCP concern: Class 'EqualHighGroup' has no inheritance hierarchy

**Evidence:** Class 'EqualHighGroup' in 'mercury_ai.analysis.smart_money.liquidity_engine' has no subclasses and no base classes, limiting extensibility

**class:** EqualHighGroup

#### INFO: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** OCP concern: Class 'EqualHighMetrics' has no inheritance hierarchy

**Evidence:** Class 'EqualHighMetrics' in 'mercury_ai.analysis.smart_money.liquidity_engine' has no subclasses and no base classes, limiting extensibility

**class:** EqualHighMetrics

#### INFO: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** OCP concern: Class 'EqualHighScore' has no inheritance hierarchy

**Evidence:** Class 'EqualHighScore' in 'mercury_ai.analysis.smart_money.liquidity_engine' has no subclasses and no base classes, limiting extensibility

**class:** EqualHighScore

#### INFO: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** OCP concern: Class 'LiquidityEngine' has no inheritance hierarchy

**Evidence:** Class 'LiquidityEngine' in 'mercury_ai.analysis.smart_money.liquidity_engine' has no subclasses and no base classes, limiting extensibility

**class:** LiquidityEngine

#### INFO: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** OCP concern: Class 'TestMercuryBenchmarkFramework' has no inheritance hierarchy

**Evidence:** Class 'TestMercuryBenchmarkFramework' in 'mercury_ai.analysis.tests.test_benchmark_framework' has no subclasses and no base classes, limiting extensibility

**class:** TestMercuryBenchmarkFramework

#### INFO: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** OCP concern: Class 'TestHistoricalReplayEngineConstructor' has no inheritance hierarchy

**Evidence:** Class 'TestHistoricalReplayEngineConstructor' in 'mercury_ai.analysis.tests.test_historical_replay_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestHistoricalReplayEngineConstructor

#### INFO: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** OCP concern: Class 'TestHistoricalReplayEngineBasic' has no inheritance hierarchy

**Evidence:** Class 'TestHistoricalReplayEngineBasic' in 'mercury_ai.analysis.tests.test_historical_replay_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestHistoricalReplayEngineBasic

#### INFO: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** OCP concern: Class 'TestReplayCacheIntegration' has no inheritance hierarchy

**Evidence:** Class 'TestReplayCacheIntegration' in 'mercury_ai.analysis.tests.test_historical_replay_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayCacheIntegration

#### INFO: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** OCP concern: Class 'TestSilentMode' has no inheritance hierarchy

**Evidence:** Class 'TestSilentMode' in 'mercury_ai.analysis.tests.test_historical_replay_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestSilentMode

#### INFO: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** OCP concern: Class 'TestReplayEdgeCases' has no inheritance hierarchy

**Evidence:** Class 'TestReplayEdgeCases' in 'mercury_ai.analysis.tests.test_historical_replay_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayEdgeCases

#### INFO: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** OCP concern: Class 'TestBatchReplayResult' has no inheritance hierarchy

**Evidence:** Class 'TestBatchReplayResult' in 'mercury_ai.analysis.tests.test_replay_batch_processor' has no subclasses and no base classes, limiting extensibility

**class:** TestBatchReplayResult

#### INFO: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** OCP concern: Class 'TestBatchReplayReport' has no inheritance hierarchy

**Evidence:** Class 'TestBatchReplayReport' in 'mercury_ai.analysis.tests.test_replay_batch_processor' has no subclasses and no base classes, limiting extensibility

**class:** TestBatchReplayReport

#### INFO: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** OCP concern: Class 'TestReplayBatchProcessorBasic' has no inheritance hierarchy

**Evidence:** Class 'TestReplayBatchProcessorBasic' in 'mercury_ai.analysis.tests.test_replay_batch_processor' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayBatchProcessorBasic

#### INFO: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** OCP concern: Class 'TestBatchProcessorErrorHandling' has no inheritance hierarchy

**Evidence:** Class 'TestBatchProcessorErrorHandling' in 'mercury_ai.analysis.tests.test_replay_batch_processor' has no subclasses and no base classes, limiting extensibility

**class:** TestBatchProcessorErrorHandling

#### INFO: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** OCP concern: Class 'TestCacheAggregation' has no inheritance hierarchy

**Evidence:** Class 'TestCacheAggregation' in 'mercury_ai.analysis.tests.test_replay_batch_processor' has no subclasses and no base classes, limiting extensibility

**class:** TestCacheAggregation

#### INFO: mercury_ai.analysis.tests.test_replay_cache

**Message:** OCP concern: Class 'TestReplayCacheBasic' has no inheritance hierarchy

**Evidence:** Class 'TestReplayCacheBasic' in 'mercury_ai.analysis.tests.test_replay_cache' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayCacheBasic

#### INFO: mercury_ai.analysis.tests.test_replay_cache

**Message:** OCP concern: Class 'TestReplayCacheLRU' has no inheritance hierarchy

**Evidence:** Class 'TestReplayCacheLRU' in 'mercury_ai.analysis.tests.test_replay_cache' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayCacheLRU

#### INFO: mercury_ai.analysis.tests.test_replay_cache

**Message:** OCP concern: Class 'TestCacheStats' has no inheritance hierarchy

**Evidence:** Class 'TestCacheStats' in 'mercury_ai.analysis.tests.test_replay_cache' has no subclasses and no base classes, limiting extensibility

**class:** TestCacheStats

#### INFO: mercury_ai.analysis.tests.test_replay_cache

**Message:** OCP concern: Class 'TestReplayCacheThreadSafety' has no inheritance hierarchy

**Evidence:** Class 'TestReplayCacheThreadSafety' in 'mercury_ai.analysis.tests.test_replay_cache' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayCacheThreadSafety

#### INFO: mercury_ai.analysis.tests.test_replay_cache

**Message:** OCP concern: Class 'TestReplayCacheEdgeCases' has no inheritance hierarchy

**Evidence:** Class 'TestReplayCacheEdgeCases' in 'mercury_ai.analysis.tests.test_replay_cache' has no subclasses and no base classes, limiting extensibility

**class:** TestReplayCacheEdgeCases

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestVaRCVaR' has no inheritance hierarchy

**Evidence:** Class 'TestVaRCVaR' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestVaRCVaR

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestKellyCriterion' has no inheritance hierarchy

**Evidence:** Class 'TestKellyCriterion' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestKellyCriterion

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestCorrelationMatrix' has no inheritance hierarchy

**Evidence:** Class 'TestCorrelationMatrix' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestCorrelationMatrix

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestPearsonCorrelation' has no inheritance hierarchy

**Evidence:** Class 'TestPearsonCorrelation' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestPearsonCorrelation

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestStressTesting' has no inheritance hierarchy

**Evidence:** Class 'TestStressTesting' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestStressTesting

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestAssessIntegration' has no inheritance hierarchy

**Evidence:** Class 'TestAssessIntegration' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestAssessIntegration

#### INFO: mercury_ai.analysis.tests.test_risk_engine

**Message:** OCP concern: Class 'TestEdgeCases' has no inheritance hierarchy

**Evidence:** Class 'TestEdgeCases' in 'mercury_ai.analysis.tests.test_risk_engine' has no subclasses and no base classes, limiting extensibility

**class:** TestEdgeCases

#### INFO: mercury_ai.brain.scanner

**Message:** OCP concern: Class 'MercuryScanner' has no inheritance hierarchy

**Evidence:** Class 'MercuryScanner' in 'mercury_ai.brain.scanner' has no subclasses and no base classes, limiting extensibility

**class:** MercuryScanner

#### INFO: mercury_ai.core.asset_registry

**Message:** OCP concern: Class 'Asset' has no inheritance hierarchy

**Evidence:** Class 'Asset' in 'mercury_ai.core.asset_registry' has no subclasses and no base classes, limiting extensibility

**class:** Asset

#### INFO: mercury_ai.core.asset_registry

**Message:** OCP concern: Class 'AssetRegistry' has no inheritance hierarchy

**Evidence:** Class 'AssetRegistry' in 'mercury_ai.core.asset_registry' has no subclasses and no base classes, limiting extensibility

**class:** AssetRegistry

#### INFO: mercury_ai.core.job_manager

**Message:** OCP concern: Class 'JobManager' has no inheritance hierarchy

**Evidence:** Class 'JobManager' in 'mercury_ai.core.job_manager' has no subclasses and no base classes, limiting extensibility

**class:** JobManager

#### INFO: mercury_ai.core.pipeline_profiler

**Message:** OCP concern: Class 'PipelineProfiler' has no inheritance hierarchy

**Evidence:** Class 'PipelineProfiler' in 'mercury_ai.core.pipeline_profiler' has no subclasses and no base classes, limiting extensibility

**class:** PipelineProfiler

#### INFO: mercury_ai.core.project_state

**Message:** OCP concern: Class 'ProjectState' has no inheritance hierarchy

**Evidence:** Class 'ProjectState' in 'mercury_ai.core.project_state' has no subclasses and no base classes, limiting extensibility

**class:** ProjectState

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** OCP concern: Class 'ProviderMetrics' has no inheritance hierarchy

**Evidence:** Class 'ProviderMetrics' in 'mercury_ai.data.mercury_data_provider' has no subclasses and no base classes, limiting extensibility

**class:** ProviderMetrics

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** OCP concern: Class 'ProviderHealth' has no inheritance hierarchy

**Evidence:** Class 'ProviderHealth' in 'mercury_ai.data.mercury_data_provider' has no subclasses and no base classes, limiting extensibility

**class:** ProviderHealth

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** OCP concern: Class 'ProviderRegistry' has no inheritance hierarchy

**Evidence:** Class 'ProviderRegistry' in 'mercury_ai.data.mercury_data_provider' has no subclasses and no base classes, limiting extensibility

**class:** ProviderRegistry

#### INFO: mercury_ai.data.mercury_data_provider

**Message:** OCP concern: Class 'MercuryDataProvider' has no inheritance hierarchy

**Evidence:** Class 'MercuryDataProvider' in 'mercury_ai.data.mercury_data_provider' has no subclasses and no base classes, limiting extensibility

**class:** MercuryDataProvider

#### INFO: mercury_ai.data.providers.historical_data_provider

**Message:** OCP concern: Class 'HistoricalDataProvider' has no inheritance hierarchy

**Evidence:** Class 'HistoricalDataProvider' in 'mercury_ai.data.providers.historical_data_provider' has no subclasses and no base classes, limiting extensibility

**class:** HistoricalDataProvider

#### INFO: mercury_ai.providers.future_broker_provider

**Message:** OCP concern: Class 'FutureBrokerProvider' has no inheritance hierarchy

**Evidence:** Class 'FutureBrokerProvider' in 'mercury_ai.providers.future_broker_provider' has no subclasses and no base classes, limiting extensibility

**class:** FutureBrokerProvider

#### INFO: mercury_ai.providers.future_polygon_provider

**Message:** OCP concern: Class 'FuturePolygonProvider' has no inheritance hierarchy

**Evidence:** Class 'FuturePolygonProvider' in 'mercury_ai.providers.future_polygon_provider' has no subclasses and no base classes, limiting extensibility

**class:** FuturePolygonProvider

#### INFO: mercury_ai.providers.future_tradingview_provider

**Message:** OCP concern: Class 'FutureTradingViewProvider' has no inheritance hierarchy

**Evidence:** Class 'FutureTradingViewProvider' in 'mercury_ai.providers.future_tradingview_provider' has no subclasses and no base classes, limiting extensibility

**class:** FutureTradingViewProvider

#### INFO: mercury_ai.providers.historical_replay_provider

**Message:** OCP concern: Class 'HistoricalReplayProvider' has no inheritance hierarchy

**Evidence:** Class 'HistoricalReplayProvider' in 'mercury_ai.providers.historical_replay_provider' has no subclasses and no base classes, limiting extensibility

**class:** HistoricalReplayProvider

#### INFO: mercury_ai.providers.market_provider

**Message:** OCP concern: Class 'MercuryDataProvider' has no inheritance hierarchy

**Evidence:** Class 'MercuryDataProvider' in 'mercury_ai.providers.market_provider' has no subclasses and no base classes, limiting extensibility

**class:** MercuryDataProvider

#### INFO: mercury_ai.providers.yahoo_finance_provider

**Message:** OCP concern: Class 'YahooFinanceProvider' has no inheritance hierarchy

**Evidence:** Class 'YahooFinanceProvider' in 'mercury_ai.providers.yahoo_finance_provider' has no subclasses and no base classes, limiting extensibility

**class:** YahooFinanceProvider

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationReplayToMetrics' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationReplayToMetrics' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationReplayToMetrics

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationReplayToCache' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationReplayToCache' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationReplayToCache

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationReplayToPerformance' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationReplayToPerformance' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationReplayToPerformance

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationBatchToUniverse' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationBatchToUniverse' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationBatchToUniverse

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationRiskAndReplay' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationRiskAndReplay' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationRiskAndReplay

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationExtremeScenarios' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationExtremeScenarios' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationExtremeScenarios

#### INFO: tests.test_institutional_backtest

**Message:** OCP concern: Class 'TestIntegrationEndToEnd' has no inheritance hierarchy

**Evidence:** Class 'TestIntegrationEndToEnd' in 'tests.test_institutional_backtest' has no subclasses and no base classes, limiting extensibility

**class:** TestIntegrationEndToEnd

#### INFO: tests.test_regression_sprint18

**Message:** OCP concern: Class 'TestRegressionBug1MarketStructureProfileTrend' has no inheritance hierarchy

**Evidence:** Class 'TestRegressionBug1MarketStructureProfileTrend' in 'tests.test_regression_sprint18' has no subclasses and no base classes, limiting extensibility

**class:** TestRegressionBug1MarketStructureProfileTrend

#### INFO: tests.test_regression_sprint18

**Message:** OCP concern: Class 'TestRegressionBug2AnalysisPipelineInit' has no inheritance hierarchy

**Evidence:** Class 'TestRegressionBug2AnalysisPipelineInit' in 'tests.test_regression_sprint18' has no subclasses and no base classes, limiting extensibility

**class:** TestRegressionBug2AnalysisPipelineInit

#### INFO: tests.test_regression_sprint18

**Message:** OCP concern: Class 'TestRegressionBug3HistoricalReplayProvider' has no inheritance hierarchy

**Evidence:** Class 'TestRegressionBug3HistoricalReplayProvider' in 'tests.test_regression_sprint18' has no subclasses and no base classes, limiting extensibility

**class:** TestRegressionBug3HistoricalReplayProvider

#### INFO: tools.mercury_integrity_auditor.models

**Message:** OCP concern: Class 'AuditFinding' has no inheritance hierarchy

**Evidence:** Class 'AuditFinding' in 'tools.mercury_integrity_auditor.models' has no subclasses and no base classes, limiting extensibility

**class:** AuditFinding

#### INFO: tools.mercury_integrity_auditor.models

**Message:** OCP concern: Class 'AuditSection' has no inheritance hierarchy

**Evidence:** Class 'AuditSection' in 'tools.mercury_integrity_auditor.models' has no subclasses and no base classes, limiting extensibility

**class:** AuditSection

#### INFO: tools.mercury_integrity_auditor.models

**Message:** OCP concern: Class 'AuditReport' has no inheritance hierarchy

**Evidence:** Class 'AuditReport' in 'tools.mercury_integrity_auditor.models' has no subclasses and no base classes, limiting extensibility

**class:** AuditReport

### ORPHAN_MODULE (241 findings)

#### WARNING: app.dashboard.asset_registry_panel

**Message:** Orphan module: 'app.dashboard.asset_registry_panel' is not imported by any other module

**Evidence:** Module 'app.dashboard.asset_registry_panel' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.dashboard.dashboard

**Message:** Orphan module: 'app.dashboard.dashboard' is not imported by any other module

**Evidence:** Module 'app.dashboard.dashboard' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.dashboard.health_center_panel

**Message:** Orphan module: 'app.dashboard.health_center_panel' is not imported by any other module

**Evidence:** Module 'app.dashboard.health_center_panel' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.dashboard.main_dashboard

**Message:** Orphan module: 'app.dashboard.main_dashboard' is not imported by any other module

**Evidence:** Module 'app.dashboard.main_dashboard' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.dashboard.market_map_panel

**Message:** Orphan module: 'app.dashboard.market_map_panel' is not imported by any other module

**Evidence:** Module 'app.dashboard.market_map_panel' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.dashboard.observability_panel

**Message:** Orphan module: 'app.dashboard.observability_panel' is not imported by any other module

**Evidence:** Module 'app.dashboard.observability_panel' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.dashboard.provider_health_panel

**Message:** Orphan module: 'app.dashboard.provider_health_panel' is not imported by any other module

**Evidence:** Module 'app.dashboard.provider_health_panel' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.terminal.pages.01_Scanner

**Message:** Orphan module: 'app.terminal.pages.01_Scanner' is not imported by any other module

**Evidence:** Module 'app.terminal.pages.01_Scanner' has 0 classes and 1 functions but zero inbound imports


#### WARNING: app.ui_utils

**Message:** Orphan module: 'app.ui_utils' is not imported by any other module

**Evidence:** Module 'app.ui_utils' has 0 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.ai.llm

**Message:** Orphan module: 'mercury_ai.ai.llm' is not imported by any other module

**Evidence:** Module 'mercury_ai.ai.llm' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.adaptive_weight_engine

**Message:** Orphan module: 'mercury_ai.analysis.adaptive_weight_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.adaptive_weight_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Orphan module: 'mercury_ai.analysis.benchmark_framework' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.benchmark_framework' has 4 classes and 9 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.calibration_analyzer

**Message:** Orphan module: 'mercury_ai.analysis.calibration_analyzer' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.calibration_analyzer' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Orphan module: 'mercury_ai.analysis.candlestick_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.candlestick_engine' has 1 classes and 6 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.confidence_calibration_auditor

**Message:** Orphan module: 'mercury_ai.analysis.confidence_calibration_auditor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.confidence_calibration_auditor' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.confidence_engine

**Message:** Orphan module: 'mercury_ai.analysis.confidence_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.confidence_engine' has 2 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.conflict_resolution_engine

**Message:** Orphan module: 'mercury_ai.analysis.conflict_resolution_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.conflict_resolution_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.confluence_engine

**Message:** Orphan module: 'mercury_ai.analysis.confluence_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.confluence_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.confluence_helpers

**Message:** Orphan module: 'mercury_ai.analysis.confluence_helpers' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.confluence_helpers' has 0 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.confluence_score_engine

**Message:** Orphan module: 'mercury_ai.analysis.confluence_score_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.confluence_score_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.context_engine

**Message:** Orphan module: 'mercury_ai.analysis.context_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.context_engine' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.context_intelligence_engine

**Message:** Orphan module: 'mercury_ai.analysis.context_intelligence_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.context_intelligence_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.data_exporter

**Message:** Orphan module: 'mercury_ai.analysis.data_exporter' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.data_exporter' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.data_quality_engine

**Message:** Orphan module: 'mercury_ai.analysis.data_quality_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.data_quality_engine' has 2 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.decision_explainability

**Message:** Orphan module: 'mercury_ai.analysis.decision_explainability' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.decision_explainability' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.decision_resolver_engine

**Message:** Orphan module: 'mercury_ai.analysis.decision_resolver_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.decision_resolver_engine' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.decision_result_builder

**Message:** Orphan module: 'mercury_ai.analysis.decision_result_builder' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.decision_result_builder' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.decision_trace_engine

**Message:** Orphan module: 'mercury_ai.analysis.decision_trace_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.decision_trace_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.engine_performance_auditor

**Message:** Orphan module: 'mercury_ai.analysis.engine_performance_auditor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.engine_performance_auditor' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.evidence_engine

**Message:** Orphan module: 'mercury_ai.analysis.evidence_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.evidence_engine' has 1 classes and 6 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.evidence_quality_engine

**Message:** Orphan module: 'mercury_ai.analysis.evidence_quality_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.evidence_quality_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.evidence_query

**Message:** Orphan module: 'mercury_ai.analysis.evidence_query' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.evidence_query' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.evidence_ranking_engine

**Message:** Orphan module: 'mercury_ai.analysis.evidence_ranking_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.evidence_ranking_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.fair_value_gap_engine

**Message:** Orphan module: 'mercury_ai.analysis.fair_value_gap_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.fair_value_gap_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.health_auditor

**Message:** Orphan module: 'mercury_ai.analysis.health_auditor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.health_auditor' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.health_checker

**Message:** Orphan module: 'mercury_ai.analysis.health_checker' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.health_checker' has 2 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.historical_replay_engine

**Message:** Orphan module: 'mercury_ai.analysis.historical_replay_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.historical_replay_engine' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Orphan module: 'mercury_ai.analysis.institutional_analytics_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_analytics_engine' has 1 classes and 16 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Orphan module: 'mercury_ai.analysis.institutional_context_builder' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_context_builder' has 2 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_contribution

**Message:** Orphan module: 'mercury_ai.analysis.institutional_contribution' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_contribution' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Orphan module: 'mercury_ai.analysis.institutional_memory_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_memory_engine' has 1 classes and 11 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_report

**Message:** Orphan module: 'mercury_ai.analysis.institutional_report' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_report' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_report_generator

**Message:** Orphan module: 'mercury_ai.analysis.institutional_report_generator' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_report_generator' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_score_engine

**Message:** Orphan module: 'mercury_ai.analysis.institutional_score_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_score_engine' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.institutional_trade_filter_engine

**Message:** Orphan module: 'mercury_ai.analysis.institutional_trade_filter_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.institutional_trade_filter_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.integrity_checker

**Message:** Orphan module: 'mercury_ai.analysis.integrity_checker' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.integrity_checker' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.learning_engine

**Message:** Orphan module: 'mercury_ai.analysis.learning_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.learning_engine' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.live_monitor

**Message:** Orphan module: 'mercury_ai.analysis.live_monitor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.live_monitor' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Orphan module: 'mercury_ai.analysis.market_condition_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.market_condition_engine' has 1 classes and 11 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.market_context_builder

**Message:** Orphan module: 'mercury_ai.analysis.market_context_builder' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.market_context_builder' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.market_regime_engine

**Message:** Orphan module: 'mercury_ai.analysis.market_regime_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.market_regime_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.market_state_engine

**Message:** Orphan module: 'mercury_ai.analysis.market_state_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.market_state_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.market_structure_intelligence_engine

**Message:** Orphan module: 'mercury_ai.analysis.market_structure_intelligence_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.market_structure_intelligence_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.market_thesis_builder

**Message:** Orphan module: 'mercury_ai.analysis.market_thesis_builder' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.market_thesis_builder' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.metric_calculator

**Message:** Orphan module: 'mercury_ai.analysis.metric_calculator' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.metric_calculator' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.momentum_engine

**Message:** Orphan module: 'mercury_ai.analysis.momentum_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.momentum_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.mtf_engine

**Message:** Orphan module: 'mercury_ai.analysis.mtf_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.mtf_engine' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.narrative_engine

**Message:** Orphan module: 'mercury_ai.analysis.narrative_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.narrative_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.notification_center

**Message:** Orphan module: 'mercury_ai.analysis.notification_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.notification_center' has 2 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.operational_history

**Message:** Orphan module: 'mercury_ai.analysis.operational_history' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.operational_history' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.performance_analytics

**Message:** Orphan module: 'mercury_ai.analysis.performance_analytics' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.performance_analytics' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.performance_center

**Message:** Orphan module: 'mercury_ai.analysis.performance_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.performance_center' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Orphan module: 'mercury_ai.analysis.performance_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.performance_engine' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.performance_statistics

**Message:** Orphan module: 'mercury_ai.analysis.performance_statistics' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.performance_statistics' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.post_decision_evaluation_engine

**Message:** Orphan module: 'mercury_ai.analysis.post_decision_evaluation_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.post_decision_evaluation_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.price_action_analyzer

**Message:** Orphan module: 'mercury_ai.analysis.price_action_analyzer' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.price_action_analyzer' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.price_action_engine

**Message:** Orphan module: 'mercury_ai.analysis.price_action_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.price_action_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.provider_priority_engine

**Message:** Orphan module: 'mercury_ai.analysis.provider_priority_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.provider_priority_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.ranking_engine

**Message:** Orphan module: 'mercury_ai.analysis.ranking_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.ranking_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.replay_batch_processor

**Message:** Orphan module: 'mercury_ai.analysis.replay_batch_processor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.replay_batch_processor' has 3 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Orphan module: 'mercury_ai.analysis.replay_cache' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.replay_cache' has 1 classes and 9 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Orphan module: 'mercury_ai.analysis.risk_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.risk_engine' has 1 classes and 8 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.session_engine

**Message:** Orphan module: 'mercury_ai.analysis.session_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.session_engine' has 1 classes and 6 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.bos_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.bos_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.bos_engine' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.choch_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.choch_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.choch_engine' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.liquidity_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_engine' has 4 classes and 10 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.liquidity_event_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.liquidity_event_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.liquidity_event_engine' has 2 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.market_structure_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.market_structure_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.market_structure_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.order_block_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.order_block_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.order_block_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.smart_money_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.smart_money_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases' has 0 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' has 0 classes and 19 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.smart_money.tests.test_liquidity_stress

**Message:** Orphan module: 'mercury_ai.analysis.smart_money.tests.test_liquidity_stress' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.smart_money.tests.test_liquidity_stress' has 0 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.statistical_auditor

**Message:** Orphan module: 'mercury_ai.analysis.statistical_auditor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.statistical_auditor' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Orphan module: 'mercury_ai.analysis.support_resistance_analyzer' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.support_resistance_analyzer' has 1 classes and 8 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.swing_engine

**Message:** Orphan module: 'mercury_ai.analysis.swing_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.swing_engine' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_benchmark_framework' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_benchmark_framework' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_candlestick_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_candlestick_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_candlestick_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_fvg_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_fvg_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_fvg_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_historical_replay_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_historical_replay_engine' has 5 classes and 17 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_market_regime_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_market_regime_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_market_regime_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_market_structure_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_market_structure_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_market_structure_engine' has 0 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_momentum_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_momentum_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_momentum_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_price_action_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_price_action_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_price_action_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_replay_batch_processor' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_batch_processor' has 5 classes and 17 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_replay_cache' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_replay_cache' has 5 classes and 25 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_risk_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_risk_engine' has 7 classes and 52 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_trend_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_trend_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_trend_engine' has 0 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_volume_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_volume_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_volume_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.tests.test_vwap_engine

**Message:** Orphan module: 'mercury_ai.analysis.tests.test_vwap_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.tests.test_vwap_engine' has 0 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.trade_memory_engine

**Message:** Orphan module: 'mercury_ai.analysis.trade_memory_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.trade_memory_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.trade_outcome_engine

**Message:** Orphan module: 'mercury_ai.analysis.trade_outcome_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.trade_outcome_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.trend_analyzer

**Message:** Orphan module: 'mercury_ai.analysis.trend_analyzer' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.trend_analyzer' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.validation_engine

**Message:** Orphan module: 'mercury_ai.analysis.validation_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.validation_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.volatility_engine

**Message:** Orphan module: 'mercury_ai.analysis.volatility_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.volatility_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.volume_engine

**Message:** Orphan module: 'mercury_ai.analysis.volume_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.volume_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.volume_intelligence_engine

**Message:** Orphan module: 'mercury_ai.analysis.volume_intelligence_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.volume_intelligence_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.vwap_engine

**Message:** Orphan module: 'mercury_ai.analysis.vwap_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.vwap_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.analysis.weight_simulator

**Message:** Orphan module: 'mercury_ai.analysis.weight_simulator' is not imported by any other module

**Evidence:** Module 'mercury_ai.analysis.weight_simulator' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.brain.exceptions

**Message:** Orphan module: 'mercury_ai.brain.exceptions' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.exceptions' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.brain.explainability_engine

**Message:** Orphan module: 'mercury_ai.brain.explainability_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.explainability_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.brain.institutional_brain

**Message:** Orphan module: 'mercury_ai.brain.institutional_brain' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.institutional_brain' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.brain.mercury_decision_engine

**Message:** Orphan module: 'mercury_ai.brain.mercury_decision_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.mercury_decision_engine' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.brain.probability_engine

**Message:** Orphan module: 'mercury_ai.brain.probability_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.probability_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.brain.scanner

**Message:** Orphan module: 'mercury_ai.brain.scanner' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.scanner' has 1 classes and 6 functions but zero inbound imports


#### WARNING: mercury_ai.brain.tests.test_explainability_engine

**Message:** Orphan module: 'mercury_ai.brain.tests.test_explainability_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.tests.test_explainability_engine' has 0 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Message:** Orphan module: 'mercury_ai.brain.tests.test_mercury_decision_benchmark' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_benchmark' has 0 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Orphan module: 'mercury_ai.brain.tests.test_mercury_decision_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.tests.test_mercury_decision_engine' has 0 classes and 6 functions but zero inbound imports


#### WARNING: mercury_ai.brain.tests.test_probability_engine

**Message:** Orphan module: 'mercury_ai.brain.tests.test_probability_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.brain.tests.test_probability_engine' has 0 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.calendar.economic_calendar

**Message:** Orphan module: 'mercury_ai.calendar.economic_calendar' is not imported by any other module

**Evidence:** Module 'mercury_ai.calendar.economic_calendar' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.config.configuration_center

**Message:** Orphan module: 'mercury_ai.config.configuration_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.config.configuration_center' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.config.universe

**Message:** Orphan module: 'mercury_ai.config.universe' is not imported by any other module

**Evidence:** Module 'mercury_ai.config.universe' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.core._stage_builder

**Message:** Orphan module: 'mercury_ai.core._stage_builder' is not imported by any other module

**Evidence:** Module 'mercury_ai.core._stage_builder' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** Orphan module: 'mercury_ai.core.analysis_pipeline' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.analysis_pipeline' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.core.asset_registry

**Message:** Orphan module: 'mercury_ai.core.asset_registry' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.asset_registry' has 2 classes and 11 functions but zero inbound imports


#### WARNING: mercury_ai.core.audit_sink

**Message:** Orphan module: 'mercury_ai.core.audit_sink' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.audit_sink' has 3 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.core.auto_health

**Message:** Orphan module: 'mercury_ai.core.auto_health' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.auto_health' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.core.banner

**Message:** Orphan module: 'mercury_ai.core.banner' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.banner' has 0 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.core.base_engine

**Message:** Orphan module: 'mercury_ai.core.base_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.base_engine' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.core.data_quality_gate

**Message:** Orphan module: 'mercury_ai.core.data_quality_gate' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.data_quality_gate' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.core.exceptions

**Message:** Orphan module: 'mercury_ai.core.exceptions' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.exceptions' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.core.export_center

**Message:** Orphan module: 'mercury_ai.core.export_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.export_center' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.core.health_center

**Message:** Orphan module: 'mercury_ai.core.health_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.health_center' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.core.job_manager

**Message:** Orphan module: 'mercury_ai.core.job_manager' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.job_manager' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.core.observability_center

**Message:** Orphan module: 'mercury_ai.core.observability_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.observability_center' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.core.pipeline_audit_middleware

**Message:** Orphan module: 'mercury_ai.core.pipeline_audit_middleware' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.pipeline_audit_middleware' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.core.pipeline_executor

**Message:** Orphan module: 'mercury_ai.core.pipeline_executor' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.pipeline_executor' has 2 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Orphan module: 'mercury_ai.core.pipeline_profiler' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.pipeline_profiler' has 1 classes and 10 functions but zero inbound imports


#### WARNING: mercury_ai.core.project_state

**Message:** Orphan module: 'mercury_ai.core.project_state' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.project_state' has 1 classes and 8 functions but zero inbound imports


#### WARNING: mercury_ai.core.read_only

**Message:** Orphan module: 'mercury_ai.core.read_only' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.read_only' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.core.runtime_report

**Message:** Orphan module: 'mercury_ai.core.runtime_report' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.runtime_report' has 2 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.core.security_center

**Message:** Orphan module: 'mercury_ai.core.security_center' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.security_center' has 2 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.core.session_manager

**Message:** Orphan module: 'mercury_ai.core.session_manager' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.session_manager' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.core.startup

**Message:** Orphan module: 'mercury_ai.core.startup' is not imported by any other module

**Evidence:** Module 'mercury_ai.core.startup' has 0 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.data.data_normalizer

**Message:** Orphan module: 'mercury_ai.data.data_normalizer' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.data_normalizer' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.data.data_quality_engine

**Message:** Orphan module: 'mercury_ai.data.data_quality_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.data_quality_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.data.indicator_engine

**Message:** Orphan module: 'mercury_ai.data.indicator_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.indicator_engine' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.data.market_data

**Message:** Orphan module: 'mercury_ai.data.market_data' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.market_data' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.data.market_data_provider

**Message:** Orphan module: 'mercury_ai.data.market_data_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.market_data_provider' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Orphan module: 'mercury_ai.data.mercury_data_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.mercury_data_provider' has 14 classes and 35 functions but zero inbound imports


#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Orphan module: 'mercury_ai.data.providers.historical_data_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.providers.historical_data_provider' has 1 classes and 9 functions but zero inbound imports


#### WARNING: mercury_ai.data.replay_data_provider

**Message:** Orphan module: 'mercury_ai.data.replay_data_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.data.replay_data_provider' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.database.history_logger

**Message:** Orphan module: 'mercury_ai.database.history_logger' is not imported by any other module

**Evidence:** Module 'mercury_ai.database.history_logger' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.database.replay_storage

**Message:** Orphan module: 'mercury_ai.database.replay_storage' is not imported by any other module

**Evidence:** Module 'mercury_ai.database.replay_storage' has 2 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.database.snapshot_logger

**Message:** Orphan module: 'mercury_ai.database.snapshot_logger' is not imported by any other module

**Evidence:** Module 'mercury_ai.database.snapshot_logger' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.indicators.rsi

**Message:** Orphan module: 'mercury_ai.indicators.rsi' is not imported by any other module

**Evidence:** Module 'mercury_ai.indicators.rsi' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.main

**Message:** Orphan module: 'mercury_ai.main' is not imported by any other module

**Evidence:** Module 'mercury_ai.main' has 0 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.market.market_engine

**Message:** Orphan module: 'mercury_ai.market.market_engine' is not imported by any other module

**Evidence:** Module 'mercury_ai.market.market_engine' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.models.analysis_result

**Message:** Orphan module: 'mercury_ai.models.analysis_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.analysis_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.benchmark_report

**Message:** Orphan module: 'mercury_ai.models.benchmark_report' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.benchmark_report' has 2 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.candlestick_analysis

**Message:** Orphan module: 'mercury_ai.models.candlestick_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.candlestick_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.confidence_result

**Message:** Orphan module: 'mercury_ai.models.confidence_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.confidence_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.confluence_result

**Message:** Orphan module: 'mercury_ai.models.confluence_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.confluence_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.confluence_score

**Message:** Orphan module: 'mercury_ai.models.confluence_score' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.confluence_score' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.data_quality_result

**Message:** Orphan module: 'mercury_ai.models.data_quality_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.data_quality_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.decision_input

**Message:** Orphan module: 'mercury_ai.models.decision_input' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.decision_input' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.decision_node

**Message:** Orphan module: 'mercury_ai.models.decision_node' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.decision_node' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.decision_outcome

**Message:** Orphan module: 'mercury_ai.models.decision_outcome' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.decision_outcome' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.decision_result

**Message:** Orphan module: 'mercury_ai.models.decision_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.decision_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.decision_snapshot

**Message:** Orphan module: 'mercury_ai.models.decision_snapshot' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.decision_snapshot' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.decision_trace

**Message:** Orphan module: 'mercury_ai.models.decision_trace' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.decision_trace' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.direction

**Message:** Orphan module: 'mercury_ai.models.direction' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.direction' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.equity_metrics

**Message:** Orphan module: 'mercury_ai.models.equity_metrics' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.equity_metrics' has 2 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.evidence

**Message:** Orphan module: 'mercury_ai.models.evidence' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.evidence' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.evidence_ranking

**Message:** Orphan module: 'mercury_ai.models.evidence_ranking' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.evidence_ranking' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.fair_value_gap_analysis

**Message:** Orphan module: 'mercury_ai.models.fair_value_gap_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.fair_value_gap_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.liquidity_analysis

**Message:** Orphan module: 'mercury_ai.models.liquidity_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.liquidity_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.liquidity_event_enum

**Message:** Orphan module: 'mercury_ai.models.liquidity_event_enum' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.liquidity_event_enum' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.liquidity_profile

**Message:** Orphan module: 'mercury_ai.models.liquidity_profile' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.liquidity_profile' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.liquidity_result

**Message:** Orphan module: 'mercury_ai.models.liquidity_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.liquidity_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_condition

**Message:** Orphan module: 'mercury_ai.models.market_condition' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_condition' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_context

**Message:** Orphan module: 'mercury_ai.models.market_context' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_context' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_data

**Message:** Orphan module: 'mercury_ai.models.market_data' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_data' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_evidence_bundle

**Message:** Orphan module: 'mercury_ai.models.market_evidence_bundle' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_evidence_bundle' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_regime

**Message:** Orphan module: 'mercury_ai.models.market_regime' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_regime' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_regime_enum

**Message:** Orphan module: 'mercury_ai.models.market_regime_enum' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_regime_enum' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_state

**Message:** Orphan module: 'mercury_ai.models.market_state' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_state' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_state_enum

**Message:** Orphan module: 'mercury_ai.models.market_state_enum' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_state_enum' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_structure

**Message:** Orphan module: 'mercury_ai.models.market_structure' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_structure' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_structure_profile

**Message:** Orphan module: 'mercury_ai.models.market_structure_profile' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_structure_profile' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.market_thesis

**Message:** Orphan module: 'mercury_ai.models.market_thesis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.market_thesis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.memory_audit

**Message:** Orphan module: 'mercury_ai.models.memory_audit' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.memory_audit' has 2 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.momentum_analysis

**Message:** Orphan module: 'mercury_ai.models.momentum_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.momentum_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.mtf_consensus

**Message:** Orphan module: 'mercury_ai.models.mtf_consensus' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.mtf_consensus' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.performance

**Message:** Orphan module: 'mercury_ai.models.performance' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.performance' has 3 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.performance_metrics

**Message:** Orphan module: 'mercury_ai.models.performance_metrics' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.performance_metrics' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.price_action

**Message:** Orphan module: 'mercury_ai.models.price_action' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.price_action' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.price_action_analysis

**Message:** Orphan module: 'mercury_ai.models.price_action_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.price_action_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.probability_result

**Message:** Orphan module: 'mercury_ai.models.probability_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.probability_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.professional_thesis

**Message:** Orphan module: 'mercury_ai.models.professional_thesis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.professional_thesis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.profiler_models

**Message:** Orphan module: 'mercury_ai.models.profiler_models' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.profiler_models' has 3 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.regression

**Message:** Orphan module: 'mercury_ai.models.regression' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.regression' has 2 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.risk_assessment

**Message:** Orphan module: 'mercury_ai.models.risk_assessment' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.risk_assessment' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.session_analysis

**Message:** Orphan module: 'mercury_ai.models.session_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.session_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.signal

**Message:** Orphan module: 'mercury_ai.models.signal' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.signal' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.smart_money

**Message:** Orphan module: 'mercury_ai.models.smart_money' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.smart_money' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.stress_test

**Message:** Orphan module: 'mercury_ai.models.stress_test' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.stress_test' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.support_resistance

**Message:** Orphan module: 'mercury_ai.models.support_resistance' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.support_resistance' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.support_resistance_analysis

**Message:** Orphan module: 'mercury_ai.models.support_resistance_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.support_resistance_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.swing_analysis

**Message:** Orphan module: 'mercury_ai.models.swing_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.swing_analysis' has 2 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.trade_filter_result

**Message:** Orphan module: 'mercury_ai.models.trade_filter_result' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.trade_filter_result' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.trade_memory

**Message:** Orphan module: 'mercury_ai.models.trade_memory' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.trade_memory' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.trade_permission

**Message:** Orphan module: 'mercury_ai.models.trade_permission' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.trade_permission' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.trading_explanation

**Message:** Orphan module: 'mercury_ai.models.trading_explanation' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.trading_explanation' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.trend_analysis

**Message:** Orphan module: 'mercury_ai.models.trend_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.trend_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.version_metadata

**Message:** Orphan module: 'mercury_ai.models.version_metadata' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.version_metadata' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.volatility_analysis

**Message:** Orphan module: 'mercury_ai.models.volatility_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.volatility_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.volume_analysis

**Message:** Orphan module: 'mercury_ai.models.volume_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.volume_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.volume_profile

**Message:** Orphan module: 'mercury_ai.models.volume_profile' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.volume_profile' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.models.vwap_analysis

**Message:** Orphan module: 'mercury_ai.models.vwap_analysis' is not imported by any other module

**Evidence:** Module 'mercury_ai.models.vwap_analysis' has 1 classes and 0 functions but zero inbound imports


#### WARNING: mercury_ai.news.news_provider

**Message:** Orphan module: 'mercury_ai.news.news_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.news.news_provider' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.operations.demo_manager

**Message:** Orphan module: 'mercury_ai.operations.demo_manager' is not imported by any other module

**Evidence:** Module 'mercury_ai.operations.demo_manager' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.presentation.signal_formatter

**Message:** Orphan module: 'mercury_ai.presentation.signal_formatter' is not imported by any other module

**Evidence:** Module 'mercury_ai.presentation.signal_formatter' has 1 classes and 1 functions but zero inbound imports


#### WARNING: mercury_ai.providers.base_provider

**Message:** Orphan module: 'mercury_ai.providers.base_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.base_provider' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.providers.data_adapters

**Message:** Orphan module: 'mercury_ai.providers.data_adapters' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.data_adapters' has 7 classes and 10 functions but zero inbound imports


#### WARNING: mercury_ai.providers.data_interfaces

**Message:** Orphan module: 'mercury_ai.providers.data_interfaces' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.data_interfaces' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Orphan module: 'mercury_ai.providers.future_broker_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.future_broker_provider' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Orphan module: 'mercury_ai.providers.future_polygon_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.future_polygon_provider' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Orphan module: 'mercury_ai.providers.future_tradingview_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.future_tradingview_provider' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Orphan module: 'mercury_ai.providers.historical_replay_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.historical_replay_provider' has 1 classes and 10 functions but zero inbound imports


#### WARNING: mercury_ai.providers.market_provider

**Message:** Orphan module: 'mercury_ai.providers.market_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.market_provider' has 1 classes and 15 functions but zero inbound imports


#### WARNING: mercury_ai.providers.provider

**Message:** Orphan module: 'mercury_ai.providers.provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.provider' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Orphan module: 'mercury_ai.providers.yahoo_finance_provider' is not imported by any other module

**Evidence:** Module 'mercury_ai.providers.yahoo_finance_provider' has 1 classes and 7 functions but zero inbound imports


#### WARNING: mercury_ai.sessions.market_sessions

**Message:** Orphan module: 'mercury_ai.sessions.market_sessions' is not imported by any other module

**Evidence:** Module 'mercury_ai.sessions.market_sessions' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.utils.deterministic_clock

**Message:** Orphan module: 'mercury_ai.utils.deterministic_clock' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.deterministic_clock' has 1 classes and 2 functions but zero inbound imports


#### WARNING: mercury_ai.utils.memory_auditor

**Message:** Orphan module: 'mercury_ai.utils.memory_auditor' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.memory_auditor' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.utils.performance_collector

**Message:** Orphan module: 'mercury_ai.utils.performance_collector' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.performance_collector' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.utils.regression_detector

**Message:** Orphan module: 'mercury_ai.utils.regression_detector' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.regression_detector' has 1 classes and 4 functions but zero inbound imports


#### WARNING: mercury_ai.utils.report_generator

**Message:** Orphan module: 'mercury_ai.utils.report_generator' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.report_generator' has 1 classes and 5 functions but zero inbound imports


#### WARNING: mercury_ai.utils.stress_tester

**Message:** Orphan module: 'mercury_ai.utils.stress_tester' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.stress_tester' has 1 classes and 3 functions but zero inbound imports


#### WARNING: mercury_ai.utils.system_monitor

**Message:** Orphan module: 'mercury_ai.utils.system_monitor' is not imported by any other module

**Evidence:** Module 'mercury_ai.utils.system_monitor' has 1 classes and 1 functions but zero inbound imports


### UNUSED_CLASS (75 findings)

#### WARNING: mercury_ai.ai.llm

**Message:** Unused class: 'MercuryLLM' in 'mercury_ai.ai.llm'

**Evidence:** Class 'MercuryLLM' at line 5 in 'mercury_ai.ai.llm' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.analysis.calibration_analyzer

**Message:** Unused class: 'CalibrationAnalyzer' in 'mercury_ai.analysis.calibration_analyzer'

**Evidence:** Class 'CalibrationAnalyzer' at line 5 in 'mercury_ai.analysis.calibration_analyzer' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused class: 'InstitutionalAnalyticsEngine' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Class 'InstitutionalAnalyticsEngine' at line 10 in 'mercury_ai.analysis.institutional_analytics_engine' is never instantiated or inherited

**line:** 10

#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Unused class: 'InstitutionalContextBuilder' in 'mercury_ai.analysis.institutional_context_builder'

**Evidence:** Class 'InstitutionalContextBuilder' at line 21 in 'mercury_ai.analysis.institutional_context_builder' is never instantiated or inherited

**line:** 21

#### WARNING: mercury_ai.analysis.learning_engine

**Message:** Unused class: 'LearningEngine' in 'mercury_ai.analysis.learning_engine'

**Evidence:** Class 'LearningEngine' at line 6 in 'mercury_ai.analysis.learning_engine' is never instantiated or inherited

**line:** 6

#### WARNING: mercury_ai.analysis.post_decision_evaluation_engine

**Message:** Unused class: 'PostDecisionEvaluationEngine' in 'mercury_ai.analysis.post_decision_evaluation_engine'

**Evidence:** Class 'PostDecisionEvaluationEngine' at line 5 in 'mercury_ai.analysis.post_decision_evaluation_engine' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.analysis.trade_memory_engine

**Message:** Unused class: 'TradeMemoryEngine' in 'mercury_ai.analysis.trade_memory_engine'

**Evidence:** Class 'TradeMemoryEngine' at line 6 in 'mercury_ai.analysis.trade_memory_engine' is never instantiated or inherited

**line:** 6

#### WARNING: mercury_ai.analysis.smart_money.liquidity_event_engine

**Message:** Unused class: 'LiquidityEventEngine' in 'mercury_ai.analysis.smart_money.liquidity_event_engine'

**Evidence:** Class 'LiquidityEventEngine' at line 15 in 'mercury_ai.analysis.smart_money.liquidity_event_engine' is never instantiated or inherited

**line:** 15

#### WARNING: mercury_ai.analysis.tests.test_benchmark_framework

**Message:** Unused class: 'TestMercuryBenchmarkFramework' in 'mercury_ai.analysis.tests.test_benchmark_framework'

**Evidence:** Class 'TestMercuryBenchmarkFramework' at line 11 in 'mercury_ai.analysis.tests.test_benchmark_framework' is never instantiated or inherited

**line:** 11

#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Unused class: 'TestHistoricalReplayEngineConstructor' in 'mercury_ai.analysis.tests.test_historical_replay_engine'

**Evidence:** Class 'TestHistoricalReplayEngineConstructor' at line 29 in 'mercury_ai.analysis.tests.test_historical_replay_engine' is never instantiated or inherited

**line:** 29

#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Unused class: 'TestHistoricalReplayEngineBasic' in 'mercury_ai.analysis.tests.test_historical_replay_engine'

**Evidence:** Class 'TestHistoricalReplayEngineBasic' at line 48 in 'mercury_ai.analysis.tests.test_historical_replay_engine' is never instantiated or inherited

**line:** 48

#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Unused class: 'TestReplayCacheIntegration' in 'mercury_ai.analysis.tests.test_historical_replay_engine'

**Evidence:** Class 'TestReplayCacheIntegration' at line 90 in 'mercury_ai.analysis.tests.test_historical_replay_engine' is never instantiated or inherited

**line:** 90

#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Unused class: 'TestSilentMode' in 'mercury_ai.analysis.tests.test_historical_replay_engine'

**Evidence:** Class 'TestSilentMode' at line 130 in 'mercury_ai.analysis.tests.test_historical_replay_engine' is never instantiated or inherited

**line:** 130

#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Unused class: 'TestReplayEdgeCases' in 'mercury_ai.analysis.tests.test_historical_replay_engine'

**Evidence:** Class 'TestReplayEdgeCases' at line 147 in 'mercury_ai.analysis.tests.test_historical_replay_engine' is never instantiated or inherited

**line:** 147

#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Unused class: 'TestBatchReplayResult' in 'mercury_ai.analysis.tests.test_replay_batch_processor'

**Evidence:** Class 'TestBatchReplayResult' at line 36 in 'mercury_ai.analysis.tests.test_replay_batch_processor' is never instantiated or inherited

**line:** 36

#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Unused class: 'TestBatchReplayReport' in 'mercury_ai.analysis.tests.test_replay_batch_processor'

**Evidence:** Class 'TestBatchReplayReport' at line 77 in 'mercury_ai.analysis.tests.test_replay_batch_processor' is never instantiated or inherited

**line:** 77

#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Unused class: 'TestReplayBatchProcessorBasic' in 'mercury_ai.analysis.tests.test_replay_batch_processor'

**Evidence:** Class 'TestReplayBatchProcessorBasic' at line 112 in 'mercury_ai.analysis.tests.test_replay_batch_processor' is never instantiated or inherited

**line:** 112

#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Unused class: 'TestBatchProcessorErrorHandling' in 'mercury_ai.analysis.tests.test_replay_batch_processor'

**Evidence:** Class 'TestBatchProcessorErrorHandling' at line 190 in 'mercury_ai.analysis.tests.test_replay_batch_processor' is never instantiated or inherited

**line:** 190

#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Unused class: 'TestCacheAggregation' in 'mercury_ai.analysis.tests.test_replay_batch_processor'

**Evidence:** Class 'TestCacheAggregation' at line 235 in 'mercury_ai.analysis.tests.test_replay_batch_processor' is never instantiated or inherited

**line:** 235

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused class: 'TestReplayCacheBasic' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Class 'TestReplayCacheBasic' at line 10 in 'mercury_ai.analysis.tests.test_replay_cache' is never instantiated or inherited

**line:** 10

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused class: 'TestReplayCacheLRU' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Class 'TestReplayCacheLRU' at line 51 in 'mercury_ai.analysis.tests.test_replay_cache' is never instantiated or inherited

**line:** 51

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused class: 'TestCacheStats' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Class 'TestCacheStats' at line 96 in 'mercury_ai.analysis.tests.test_replay_cache' is never instantiated or inherited

**line:** 96

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused class: 'TestReplayCacheThreadSafety' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Class 'TestReplayCacheThreadSafety' at line 146 in 'mercury_ai.analysis.tests.test_replay_cache' is never instantiated or inherited

**line:** 146

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused class: 'TestReplayCacheEdgeCases' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Class 'TestReplayCacheEdgeCases' at line 215 in 'mercury_ai.analysis.tests.test_replay_cache' is never instantiated or inherited

**line:** 215

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestVaRCVaR' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestVaRCVaR' at line 136 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 136

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestKellyCriterion' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestKellyCriterion' at line 198 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 198

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestCorrelationMatrix' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestCorrelationMatrix' at line 260 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 260

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestPearsonCorrelation' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestPearsonCorrelation' at line 341 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 341

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestStressTesting' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestStressTesting' at line 380 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 380

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestAssessIntegration' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestAssessIntegration' at line 424 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 424

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused class: 'TestEdgeCases' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Class 'TestEdgeCases' at line 534 in 'mercury_ai.analysis.tests.test_risk_engine' is never instantiated or inherited

**line:** 534

#### WARNING: mercury_ai.brain.exceptions

**Message:** Unused class: 'InvalidWeightConfiguration' in 'mercury_ai.brain.exceptions'

**Evidence:** Class 'InvalidWeightConfiguration' at line 1 in 'mercury_ai.brain.exceptions' is never instantiated or inherited

**line:** 1

#### WARNING: mercury_ai.core.audit_sink

**Message:** Unused class: 'MemoryAuditSink' in 'mercury_ai.core.audit_sink'

**Evidence:** Class 'MemoryAuditSink' at line 15 in 'mercury_ai.core.audit_sink' is never instantiated or inherited

**line:** 15

#### WARNING: mercury_ai.core.data_quality_gate

**Message:** Unused class: 'DataQualityGate' in 'mercury_ai.core.data_quality_gate'

**Evidence:** Class 'DataQualityGate' at line 13 in 'mercury_ai.core.data_quality_gate' is never instantiated or inherited

**line:** 13

#### WARNING: mercury_ai.core.pipeline_audit_middleware

**Message:** Unused class: 'PipelineAuditMiddleware' in 'mercury_ai.core.pipeline_audit_middleware'

**Evidence:** Class 'PipelineAuditMiddleware' at line 6 in 'mercury_ai.core.pipeline_audit_middleware' is never instantiated or inherited

**line:** 6

#### WARNING: mercury_ai.core.project_state

**Message:** Unused class: 'ProjectState' in 'mercury_ai.core.project_state'

**Evidence:** Class 'ProjectState' at line 8 in 'mercury_ai.core.project_state' is never instantiated or inherited

**line:** 8

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused class: 'ProviderStatus' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Class 'ProviderStatus' at line 13 in 'mercury_ai.data.mercury_data_provider' is never instantiated or inherited

**line:** 13

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused class: 'ProviderMetrics' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Class 'ProviderMetrics' at line 19 in 'mercury_ai.data.mercury_data_provider' is never instantiated or inherited

**line:** 19

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused class: 'ProviderHealth' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Class 'ProviderHealth' at line 25 in 'mercury_ai.data.mercury_data_provider' is never instantiated or inherited

**line:** 25

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused class: 'ProviderRegistry' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Class 'ProviderRegistry' at line 37 in 'mercury_ai.data.mercury_data_provider' is never instantiated or inherited

**line:** 37

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused class: 'IMercuryDataProvider' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Class 'IMercuryDataProvider' at line 44 in 'mercury_ai.data.mercury_data_provider' is never instantiated or inherited

**line:** 44

#### WARNING: mercury_ai.data.replay_data_provider

**Message:** Unused class: 'ReplayDataProvider' in 'mercury_ai.data.replay_data_provider'

**Evidence:** Class 'ReplayDataProvider' at line 4 in 'mercury_ai.data.replay_data_provider' is never instantiated or inherited

**line:** 4

#### WARNING: mercury_ai.database.history_logger

**Message:** Unused class: 'HistoryLogger' in 'mercury_ai.database.history_logger'

**Evidence:** Class 'HistoryLogger' at line 6 in 'mercury_ai.database.history_logger' is never instantiated or inherited

**line:** 6

#### WARNING: mercury_ai.indicators.rsi

**Message:** Unused class: 'RSIIndicator' in 'mercury_ai.indicators.rsi'

**Evidence:** Class 'RSIIndicator' at line 3 in 'mercury_ai.indicators.rsi' is never instantiated or inherited

**line:** 3

#### WARNING: mercury_ai.market.market_engine

**Message:** Unused class: 'MarketEngine' in 'mercury_ai.market.market_engine'

**Evidence:** Class 'MarketEngine' at line 5 in 'mercury_ai.market.market_engine' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.models.decision_input

**Message:** Unused class: 'DecisionInput' in 'mercury_ai.models.decision_input'

**Evidence:** Class 'DecisionInput' at line 5 in 'mercury_ai.models.decision_input' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.models.decision_outcome

**Message:** Unused class: 'DecisionOutcome' in 'mercury_ai.models.decision_outcome'

**Evidence:** Class 'DecisionOutcome' at line 5 in 'mercury_ai.models.decision_outcome' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.models.direction

**Message:** Unused class: 'AnalysisDirection' in 'mercury_ai.models.direction'

**Evidence:** Class 'AnalysisDirection' at line 4 in 'mercury_ai.models.direction' is never instantiated or inherited

**line:** 4

#### WARNING: mercury_ai.models.liquidity_event_enum

**Message:** Unused class: 'LiquidityEventType' in 'mercury_ai.models.liquidity_event_enum'

**Evidence:** Class 'LiquidityEventType' at line 3 in 'mercury_ai.models.liquidity_event_enum' is never instantiated or inherited

**line:** 3

#### WARNING: mercury_ai.models.market_regime_enum

**Message:** Unused class: 'MarketRegimeEnum' in 'mercury_ai.models.market_regime_enum'

**Evidence:** Class 'MarketRegimeEnum' at line 3 in 'mercury_ai.models.market_regime_enum' is never instantiated or inherited

**line:** 3

#### WARNING: mercury_ai.models.market_state_enum

**Message:** Unused class: 'MarketStateEnum' in 'mercury_ai.models.market_state_enum'

**Evidence:** Class 'MarketStateEnum' at line 3 in 'mercury_ai.models.market_state_enum' is never instantiated or inherited

**line:** 3

#### WARNING: mercury_ai.models.professional_thesis

**Message:** Unused class: 'ProfessionalThesis' in 'mercury_ai.models.professional_thesis'

**Evidence:** Class 'ProfessionalThesis' at line 5 in 'mercury_ai.models.professional_thesis' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.models.profiler_models

**Message:** Unused class: 'HotspotSummary' in 'mercury_ai.models.profiler_models'

**Evidence:** Class 'HotspotSummary' at line 20 in 'mercury_ai.models.profiler_models' is never instantiated or inherited

**line:** 20

#### WARNING: mercury_ai.models.trade_memory

**Message:** Unused class: 'TradeMemory' in 'mercury_ai.models.trade_memory'

**Evidence:** Class 'TradeMemory' at line 6 in 'mercury_ai.models.trade_memory' is never instantiated or inherited

**line:** 6

#### WARNING: mercury_ai.models.trade_permission

**Message:** Unused class: 'TradePermission' in 'mercury_ai.models.trade_permission'

**Evidence:** Class 'TradePermission' at line 5 in 'mercury_ai.models.trade_permission' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.models.trend_analysis

**Message:** Unused class: 'TrendAnalysis' in 'mercury_ai.models.trend_analysis'

**Evidence:** Class 'TrendAnalysis' at line 5 in 'mercury_ai.models.trend_analysis' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.providers.data_interfaces

**Message:** Unused class: 'IDataProvider' in 'mercury_ai.providers.data_interfaces'

**Evidence:** Class 'IDataProvider' at line 4 in 'mercury_ai.providers.data_interfaces' is never instantiated or inherited

**line:** 4

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused class: 'FutureBrokerProvider' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Class 'FutureBrokerProvider' at line 1 in 'mercury_ai.providers.future_broker_provider' is never instantiated or inherited

**line:** 1

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused class: 'FuturePolygonProvider' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Class 'FuturePolygonProvider' at line 1 in 'mercury_ai.providers.future_polygon_provider' is never instantiated or inherited

**line:** 1

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused class: 'FutureTradingViewProvider' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Class 'FutureTradingViewProvider' at line 1 in 'mercury_ai.providers.future_tradingview_provider' is never instantiated or inherited

**line:** 1

#### WARNING: mercury_ai.utils.memory_auditor

**Message:** Unused class: 'MemoryAuditor' in 'mercury_ai.utils.memory_auditor'

**Evidence:** Class 'MemoryAuditor' at line 6 in 'mercury_ai.utils.memory_auditor' is never instantiated or inherited

**line:** 6

#### WARNING: mercury_ai.utils.regression_detector

**Message:** Unused class: 'RegressionDetector' in 'mercury_ai.utils.regression_detector'

**Evidence:** Class 'RegressionDetector' at line 5 in 'mercury_ai.utils.regression_detector' is never instantiated or inherited

**line:** 5

#### WARNING: mercury_ai.utils.report_generator

**Message:** Unused class: 'BenchmarkReportGenerator' in 'mercury_ai.utils.report_generator'

**Evidence:** Class 'BenchmarkReportGenerator' at line 8 in 'mercury_ai.utils.report_generator' is never instantiated or inherited

**line:** 8

#### WARNING: mercury_ai.utils.stress_tester

**Message:** Unused class: 'StressTester' in 'mercury_ai.utils.stress_tester'

**Evidence:** Class 'StressTester' at line 6 in 'mercury_ai.utils.stress_tester' is never instantiated or inherited

**line:** 6

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationReplayToMetrics' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationReplayToMetrics' at line 75 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 75

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationReplayToCache' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationReplayToCache' at line 118 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 118

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationReplayToPerformance' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationReplayToPerformance' at line 150 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 150

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationBatchToUniverse' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationBatchToUniverse' at line 191 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 191

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationRiskAndReplay' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationRiskAndReplay' at line 229 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 229

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationExtremeScenarios' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationExtremeScenarios' at line 285 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 285

#### WARNING: tests.test_institutional_backtest

**Message:** Unused class: 'TestIntegrationEndToEnd' in 'tests.test_institutional_backtest'

**Evidence:** Class 'TestIntegrationEndToEnd' at line 366 in 'tests.test_institutional_backtest' is never instantiated or inherited

**line:** 366

#### WARNING: tests.test_performance_engine

**Message:** Unused class: 'TestPerformanceEngine' in 'tests.test_performance_engine'

**Evidence:** Class 'TestPerformanceEngine' at line 6 in 'tests.test_performance_engine' is never instantiated or inherited

**line:** 6

#### WARNING: tests.test_regression_sprint18

**Message:** Unused class: 'TestRegressionBug1MarketStructureProfileTrend' in 'tests.test_regression_sprint18'

**Evidence:** Class 'TestRegressionBug1MarketStructureProfileTrend' at line 24 in 'tests.test_regression_sprint18' is never instantiated or inherited

**line:** 24

#### WARNING: tests.test_regression_sprint18

**Message:** Unused class: 'TestRegressionBug2AnalysisPipelineInit' in 'tests.test_regression_sprint18'

**Evidence:** Class 'TestRegressionBug2AnalysisPipelineInit' at line 54 in 'tests.test_regression_sprint18' is never instantiated or inherited

**line:** 54

#### WARNING: tests.test_regression_sprint18

**Message:** Unused class: 'TestRegressionBug3HistoricalReplayProvider' in 'tests.test_regression_sprint18'

**Evidence:** Class 'TestRegressionBug3HistoricalReplayProvider' at line 79 in 'tests.test_regression_sprint18' is never instantiated or inherited

**line:** 79

### UNUSED_FUNCTION (491 findings)

#### WARNING: main

**Message:** Unused function: '_run_scan' in 'main'

**Evidence:** Function '_run_scan' at line 17 in 'main' is never called

**line:** 17

#### WARNING: run_instrumented

**Message:** Unused function: 'get_data' in 'run_instrumented'

**Evidence:** Function 'get_data' at line 6 in 'run_instrumented' is never called

**line:** 6

#### WARNING: run_instrumented

**Message:** Unused function: 'is_available' in 'run_instrumented'

**Evidence:** Function 'is_available' at line 8 in 'run_instrumented' is never called

**line:** 8

#### WARNING: run_instrumented

**Message:** Unused function: 'supports_symbol' in 'run_instrumented'

**Evidence:** Function 'supports_symbol' at line 9 in 'run_instrumented' is never called

**line:** 9

#### WARNING: run_instrumented

**Message:** Unused function: 'supports_market' in 'run_instrumented'

**Evidence:** Function 'supports_market' at line 10 in 'run_instrumented' is never called

**line:** 10

#### WARNING: run_instrumented

**Message:** Unused function: 'supports_timeframe' in 'run_instrumented'

**Evidence:** Function 'supports_timeframe' at line 11 in 'run_instrumented' is never called

**line:** 11

#### WARNING: run_instrumented

**Message:** Unused function: 'max_history' in 'run_instrumented'

**Evidence:** Function 'max_history' at line 12 in 'run_instrumented' is never called

**line:** 12

#### WARNING: run_instrumented

**Message:** Unused function: 'source_name' in 'run_instrumented'

**Evidence:** Function 'source_name' at line 13 in 'run_instrumented' is never called

**line:** 13

#### WARNING: app.ui_utils

**Message:** Unused function: 'display_metric' in 'app.ui_utils'

**Evidence:** Function 'display_metric' at line 27 in 'app.ui_utils' is never called

**line:** 27

#### WARNING: app.ui_utils

**Message:** Unused function: 'display_status' in 'app.ui_utils'

**Evidence:** Function 'display_status' at line 31 in 'app.ui_utils' is never called

**line:** 31

#### WARNING: mercury_ai.ai.llm

**Message:** Unused function: 'ask' in 'mercury_ai.ai.llm'

**Evidence:** Function 'ask' at line 13 in 'mercury_ai.ai.llm' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.adaptive_weight_engine

**Message:** Unused function: 'calculate_weights' in 'mercury_ai.analysis.adaptive_weight_engine'

**Evidence:** Function 'calculate_weights' at line 10 in 'mercury_ai.analysis.adaptive_weight_engine' is never called

**line:** 10

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: '_run_single_symbol' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function '_run_single_symbol' at line 132 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 132

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: '_get_real_outcome' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function '_get_real_outcome' at line 174 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 174

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: '_apply_warm_cool_filter' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function '_apply_warm_cool_filter' at line 198 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 198

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: '_compute_buy_and_hold' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function '_compute_buy_and_hold' at line 226 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 226

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: '_run_statistical_tests' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function '_run_statistical_tests' at line 273 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 273

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: 'run_benchmark' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function 'run_benchmark' at line 333 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 333

#### WARNING: mercury_ai.analysis.benchmark_framework

**Message:** Unused function: 'run_quick_benchmark' in 'mercury_ai.analysis.benchmark_framework'

**Evidence:** Function 'run_quick_benchmark' at line 442 in 'mercury_ai.analysis.benchmark_framework' is never called

**line:** 442

#### WARNING: mercury_ai.analysis.calibration_analyzer

**Message:** Unused function: 'analyze_calibration' in 'mercury_ai.analysis.calibration_analyzer'

**Evidence:** Function 'analyze_calibration' at line 9 in 'mercury_ai.analysis.calibration_analyzer' is never called

**line:** 9

#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.candlestick_engine'

**Evidence:** Function 'analyze' at line 21 in 'mercury_ai.analysis.candlestick_engine' is never called

**line:** 21

#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Unused function: '_detect_context' in 'mercury_ai.analysis.candlestick_engine'

**Evidence:** Function '_detect_context' at line 84 in 'mercury_ai.analysis.candlestick_engine' is never called

**line:** 84

#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Unused function: '_detect_pattern' in 'mercury_ai.analysis.candlestick_engine'

**Evidence:** Function '_detect_pattern' at line 98 in 'mercury_ai.analysis.candlestick_engine' is never called

**line:** 98

#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Unused function: '_detect_engulfing' in 'mercury_ai.analysis.candlestick_engine'

**Evidence:** Function '_detect_engulfing' at line 117 in 'mercury_ai.analysis.candlestick_engine' is never called

**line:** 117

#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Unused function: '_detect_rejection' in 'mercury_ai.analysis.candlestick_engine'

**Evidence:** Function '_detect_rejection' at line 124 in 'mercury_ai.analysis.candlestick_engine' is never called

**line:** 124

#### WARNING: mercury_ai.analysis.candlestick_engine

**Message:** Unused function: '_detect_continuation' in 'mercury_ai.analysis.candlestick_engine'

**Evidence:** Function '_detect_continuation' at line 130 in 'mercury_ai.analysis.candlestick_engine' is never called

**line:** 130

#### WARNING: mercury_ai.analysis.confidence_calibration_auditor

**Message:** Unused function: 'audit' in 'mercury_ai.analysis.confidence_calibration_auditor'

**Evidence:** Function 'audit' at line 14 in 'mercury_ai.analysis.confidence_calibration_auditor' is never called

**line:** 14

#### WARNING: mercury_ai.analysis.confidence_engine

**Message:** Unused function: 'calculate' in 'mercury_ai.analysis.confidence_engine'

**Evidence:** Function 'calculate' at line 22 in 'mercury_ai.analysis.confidence_engine' is never called

**line:** 22

#### WARNING: mercury_ai.analysis.confidence_engine

**Message:** Unused function: 'calibrate' in 'mercury_ai.analysis.confidence_engine'

**Evidence:** Function 'calibrate' at line 107 in 'mercury_ai.analysis.confidence_engine' is never called

**line:** 107

#### WARNING: mercury_ai.analysis.confidence_engine

**Message:** Unused function: '_get_grade' in 'mercury_ai.analysis.confidence_engine'

**Evidence:** Function '_get_grade' at line 136 in 'mercury_ai.analysis.confidence_engine' is never called

**line:** 136

#### WARNING: mercury_ai.analysis.conflict_resolution_engine

**Message:** Unused function: 'resolve' in 'mercury_ai.analysis.conflict_resolution_engine'

**Evidence:** Function 'resolve' at line 14 in 'mercury_ai.analysis.conflict_resolution_engine' is never called

**line:** 14

#### WARNING: mercury_ai.analysis.confluence_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.confluence_engine'

**Evidence:** Function 'analyze' at line 50 in 'mercury_ai.analysis.confluence_engine' is never called

**line:** 50

#### WARNING: mercury_ai.analysis.confluence_score_engine

**Message:** Unused function: 'calculate' in 'mercury_ai.analysis.confluence_score_engine'

**Evidence:** Function 'calculate' at line 17 in 'mercury_ai.analysis.confluence_score_engine' is never called

**line:** 17

#### WARNING: mercury_ai.analysis.context_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.context_engine'

**Evidence:** Function 'analyze' at line 27 in 'mercury_ai.analysis.context_engine' is never called

**line:** 27

#### WARNING: mercury_ai.analysis.context_engine

**Message:** Unused function: '_merge_evidences' in 'mercury_ai.analysis.context_engine'

**Evidence:** Function '_merge_evidences' at line 72 in 'mercury_ai.analysis.context_engine' is never called

**line:** 72

#### WARNING: mercury_ai.analysis.context_engine

**Message:** Unused function: '_deduplicate_evidences' in 'mercury_ai.analysis.context_engine'

**Evidence:** Function '_deduplicate_evidences' at line 79 in 'mercury_ai.analysis.context_engine' is never called

**line:** 79

#### WARNING: mercury_ai.analysis.context_engine

**Message:** Unused function: '_detect_conflicts' in 'mercury_ai.analysis.context_engine'

**Evidence:** Function '_detect_conflicts' at line 101 in 'mercury_ai.analysis.context_engine' is never called

**line:** 101

#### WARNING: mercury_ai.analysis.context_engine

**Message:** Unused function: '_calculate_quality' in 'mercury_ai.analysis.context_engine'

**Evidence:** Function '_calculate_quality' at line 149 in 'mercury_ai.analysis.context_engine' is never called

**line:** 149

#### WARNING: mercury_ai.analysis.context_engine

**Message:** Unused function: '_refine_context' in 'mercury_ai.analysis.context_engine'

**Evidence:** Function '_refine_context' at line 172 in 'mercury_ai.analysis.context_engine' is never called

**line:** 172

#### WARNING: mercury_ai.analysis.context_intelligence_engine

**Message:** Unused function: 'evaluate' in 'mercury_ai.analysis.context_intelligence_engine'

**Evidence:** Function 'evaluate' at line 10 in 'mercury_ai.analysis.context_intelligence_engine' is never called

**line:** 10

#### WARNING: mercury_ai.analysis.data_exporter

**Message:** Unused function: '_export_to_formats' in 'mercury_ai.analysis.data_exporter'

**Evidence:** Function '_export_to_formats' at line 20 in 'mercury_ai.analysis.data_exporter' is never called

**line:** 20

#### WARNING: mercury_ai.analysis.data_exporter

**Message:** Unused function: 'export_history' in 'mercury_ai.analysis.data_exporter'

**Evidence:** Function 'export_history' at line 43 in 'mercury_ai.analysis.data_exporter' is never called

**line:** 43

#### WARNING: mercury_ai.analysis.data_exporter

**Message:** Unused function: 'export_snapshots' in 'mercury_ai.analysis.data_exporter'

**Evidence:** Function 'export_snapshots' at line 47 in 'mercury_ai.analysis.data_exporter' is never called

**line:** 47

#### WARNING: mercury_ai.analysis.data_exporter

**Message:** Unused function: 'export_all' in 'mercury_ai.analysis.data_exporter'

**Evidence:** Function 'export_all' at line 52 in 'mercury_ai.analysis.data_exporter' is never called

**line:** 52

#### WARNING: mercury_ai.analysis.data_quality_engine

**Message:** Unused function: 'calculate_score' in 'mercury_ai.analysis.data_quality_engine'

**Evidence:** Function 'calculate_score' at line 19 in 'mercury_ai.analysis.data_quality_engine' is never called

**line:** 19

#### WARNING: mercury_ai.analysis.data_quality_engine

**Message:** Unused function: 'generate_report' in 'mercury_ai.analysis.data_quality_engine'

**Evidence:** Function 'generate_report' at line 23 in 'mercury_ai.analysis.data_quality_engine' is never called

**line:** 23

#### WARNING: mercury_ai.analysis.decision_resolver_engine

**Message:** Unused function: 'resolve' in 'mercury_ai.analysis.decision_resolver_engine'

**Evidence:** Function 'resolve' at line 47 in 'mercury_ai.analysis.decision_resolver_engine' is never called

**line:** 47

#### WARNING: mercury_ai.analysis.decision_result_builder

**Message:** Unused function: 'build' in 'mercury_ai.analysis.decision_result_builder'

**Evidence:** Function 'build' at line 28 in 'mercury_ai.analysis.decision_result_builder' is never called

**line:** 28

#### WARNING: mercury_ai.analysis.decision_trace_engine

**Message:** Unused function: 'log_step' in 'mercury_ai.analysis.decision_trace_engine'

**Evidence:** Function 'log_step' at line 12 in 'mercury_ai.analysis.decision_trace_engine' is never called

**line:** 12

#### WARNING: mercury_ai.analysis.decision_trace_engine

**Message:** Unused function: 'finalize' in 'mercury_ai.analysis.decision_trace_engine'

**Evidence:** Function 'finalize' at line 18 in 'mercury_ai.analysis.decision_trace_engine' is never called

**line:** 18

#### WARNING: mercury_ai.analysis.engine_performance_auditor

**Message:** Unused function: 'audit_engines' in 'mercury_ai.analysis.engine_performance_auditor'

**Evidence:** Function 'audit_engines' at line 12 in 'mercury_ai.analysis.engine_performance_auditor' is never called

**line:** 12

#### WARNING: mercury_ai.analysis.evidence_engine

**Message:** Unused function: 'process' in 'mercury_ai.analysis.evidence_engine'

**Evidence:** Function 'process' at line 15 in 'mercury_ai.analysis.evidence_engine' is never called

**line:** 15

#### WARNING: mercury_ai.analysis.evidence_engine

**Message:** Unused function: 'compose' in 'mercury_ai.analysis.evidence_engine'

**Evidence:** Function 'compose' at line 38 in 'mercury_ai.analysis.evidence_engine' is never called

**line:** 38

#### WARNING: mercury_ai.analysis.evidence_engine

**Message:** Unused function: '_deduplicate' in 'mercury_ai.analysis.evidence_engine'

**Evidence:** Function '_deduplicate' at line 47 in 'mercury_ai.analysis.evidence_engine' is never called

**line:** 47

#### WARNING: mercury_ai.analysis.evidence_engine

**Message:** Unused function: '_normalize' in 'mercury_ai.analysis.evidence_engine'

**Evidence:** Function '_normalize' at line 57 in 'mercury_ai.analysis.evidence_engine' is never called

**line:** 57

#### WARNING: mercury_ai.analysis.evidence_engine

**Message:** Unused function: 'calculate_agreement' in 'mercury_ai.analysis.evidence_engine'

**Evidence:** Function 'calculate_agreement' at line 68 in 'mercury_ai.analysis.evidence_engine' is never called

**line:** 68

#### WARNING: mercury_ai.analysis.evidence_quality_engine

**Message:** Unused function: 'evaluate' in 'mercury_ai.analysis.evidence_quality_engine'

**Evidence:** Function 'evaluate' at line 10 in 'mercury_ai.analysis.evidence_quality_engine' is never called

**line:** 10

#### WARNING: mercury_ai.analysis.evidence_query

**Message:** Unused function: 'get_trend_direction' in 'mercury_ai.analysis.evidence_query'

**Evidence:** Function 'get_trend_direction' at line 11 in 'mercury_ai.analysis.evidence_query' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.evidence_query

**Message:** Unused function: 'is_uptrend' in 'mercury_ai.analysis.evidence_query'

**Evidence:** Function 'is_uptrend' at line 23 in 'mercury_ai.analysis.evidence_query' is never called

**line:** 23

#### WARNING: mercury_ai.analysis.evidence_query

**Message:** Unused function: 'is_downtrend' in 'mercury_ai.analysis.evidence_query'

**Evidence:** Function 'is_downtrend' at line 27 in 'mercury_ai.analysis.evidence_query' is never called

**line:** 27

#### WARNING: mercury_ai.analysis.evidence_query

**Message:** Unused function: 'has_strong_trend' in 'mercury_ai.analysis.evidence_query'

**Evidence:** Function 'has_strong_trend' at line 31 in 'mercury_ai.analysis.evidence_query' is never called

**line:** 31

#### WARNING: mercury_ai.analysis.evidence_ranking_engine

**Message:** Unused function: 'calculate_contribution_score' in 'mercury_ai.analysis.evidence_ranking_engine'

**Evidence:** Function 'calculate_contribution_score' at line 11 in 'mercury_ai.analysis.evidence_ranking_engine' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.evidence_ranking_engine

**Message:** Unused function: 'rank' in 'mercury_ai.analysis.evidence_ranking_engine'

**Evidence:** Function 'rank' at line 16 in 'mercury_ai.analysis.evidence_ranking_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.fair_value_gap_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.fair_value_gap_engine'

**Evidence:** Function 'analyze' at line 21 in 'mercury_ai.analysis.fair_value_gap_engine' is never called

**line:** 21

#### WARNING: mercury_ai.analysis.fair_value_gap_engine

**Message:** Unused function: '_analyze_logic' in 'mercury_ai.analysis.fair_value_gap_engine'

**Evidence:** Function '_analyze_logic' at line 34 in 'mercury_ai.analysis.fair_value_gap_engine' is never called

**line:** 34

#### WARNING: mercury_ai.analysis.health_auditor

**Message:** Unused function: 'generate_report' in 'mercury_ai.analysis.health_auditor'

**Evidence:** Function 'generate_report' at line 11 in 'mercury_ai.analysis.health_auditor' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.health_checker

**Message:** Unused function: 'check' in 'mercury_ai.analysis.health_checker'

**Evidence:** Function 'check' at line 21 in 'mercury_ai.analysis.health_checker' is never called

**line:** 21

#### WARNING: mercury_ai.analysis.historical_replay_engine

**Message:** Unused function: 'cache' in 'mercury_ai.analysis.historical_replay_engine'

**Evidence:** Function 'cache' at line 48 in 'mercury_ai.analysis.historical_replay_engine' is never called

**line:** 48

#### WARNING: mercury_ai.analysis.historical_replay_engine

**Message:** Unused function: 'replay_stats' in 'mercury_ai.analysis.historical_replay_engine'

**Evidence:** Function 'replay_stats' at line 52 in 'mercury_ai.analysis.historical_replay_engine' is never called

**line:** 52

#### WARNING: mercury_ai.analysis.historical_replay_engine

**Message:** Unused function: 'run_replay' in 'mercury_ai.analysis.historical_replay_engine'

**Evidence:** Function 'run_replay' at line 56 in 'mercury_ai.analysis.historical_replay_engine' is never called

**line:** 56

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_load_data' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_load_data' at line 35 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 35

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_load_replay_metrics' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_load_replay_metrics' at line 80 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 80

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: 'generate_quality_report' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function 'generate_quality_report' at line 100 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 100

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_overview_stats' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_overview_stats' at line 123 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 123

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_win_rate_analysis' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_win_rate_analysis' at line 146 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 146

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_risk_metrics' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_risk_metrics' at line 177 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 177

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_max_consecutive' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_max_consecutive' at line 244 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 244

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_engine_contribution' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_engine_contribution' at line 260 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 260

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_pattern_analysis' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_pattern_analysis' at line 285 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 285

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_temporal_analysis' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_temporal_analysis' at line 305 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 305

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_recent_trend' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_recent_trend' at line 329 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 329

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_confidence_analysis' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_confidence_analysis' at line 351 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 351

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: '_attribution_analysis' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function '_attribution_analysis' at line 373 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 373

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: 'export_report_json' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function 'export_report_json' at line 418 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 418

#### WARNING: mercury_ai.analysis.institutional_analytics_engine

**Message:** Unused function: 'export_report_summary' in 'mercury_ai.analysis.institutional_analytics_engine'

**Evidence:** Function 'export_report_summary' at line 426 in 'mercury_ai.analysis.institutional_analytics_engine' is never called

**line:** 426

#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Unused function: 'build' in 'mercury_ai.analysis.institutional_context_builder'

**Evidence:** Function 'build' at line 27 in 'mercury_ai.analysis.institutional_context_builder' is never called

**line:** 27

#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Unused function: '_calculate_bias' in 'mercury_ai.analysis.institutional_context_builder'

**Evidence:** Function '_calculate_bias' at line 72 in 'mercury_ai.analysis.institutional_context_builder' is never called

**line:** 72

#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Unused function: '_calculate_confidence' in 'mercury_ai.analysis.institutional_context_builder'

**Evidence:** Function '_calculate_confidence' at line 102 in 'mercury_ai.analysis.institutional_context_builder' is never called

**line:** 102

#### WARNING: mercury_ai.analysis.institutional_context_builder

**Message:** Unused function: '_build_text' in 'mercury_ai.analysis.institutional_context_builder'

**Evidence:** Function '_build_text' at line 119 in 'mercury_ai.analysis.institutional_context_builder' is never called

**line:** 119

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: '_load_into_cache' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function '_load_into_cache' at line 33 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 33

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: '_initialize_memory' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function '_initialize_memory' at line 43 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 43

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: 'flush' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function 'flush' at line 49 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 49

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: '_load_memory' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function '_load_memory' at line 75 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 75

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: '_save_memory' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function '_save_memory' at line 79 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 79

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: '_get_setup_key' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function '_get_setup_key' at line 86 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 86

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: 'get_consistency_score' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function 'get_consistency_score' at line 91 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 91

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: 'record_decision' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function 'record_decision' at line 116 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 116

#### WARNING: mercury_ai.analysis.institutional_memory_engine

**Message:** Unused function: 'record_outcome' in 'mercury_ai.analysis.institutional_memory_engine'

**Evidence:** Function 'record_outcome' at line 133 in 'mercury_ai.analysis.institutional_memory_engine' is never called

**line:** 133

#### WARNING: mercury_ai.analysis.institutional_report

**Message:** Unused function: 'generate' in 'mercury_ai.analysis.institutional_report'

**Evidence:** Function 'generate' at line 8 in 'mercury_ai.analysis.institutional_report' is never called

**line:** 8

#### WARNING: mercury_ai.analysis.institutional_report_generator

**Message:** Unused function: 'generate' in 'mercury_ai.analysis.institutional_report_generator'

**Evidence:** Function 'generate' at line 14 in 'mercury_ai.analysis.institutional_report_generator' is never called

**line:** 14

#### WARNING: mercury_ai.analysis.institutional_score_engine

**Message:** Unused function: 'calculate' in 'mercury_ai.analysis.institutional_score_engine'

**Evidence:** Function 'calculate' at line 25 in 'mercury_ai.analysis.institutional_score_engine' is never called

**line:** 25

#### WARNING: mercury_ai.analysis.institutional_trade_filter_engine

**Message:** Unused function: 'evaluate' in 'mercury_ai.analysis.institutional_trade_filter_engine'

**Evidence:** Function 'evaluate' at line 20 in 'mercury_ai.analysis.institutional_trade_filter_engine' is never called

**line:** 20

#### WARNING: mercury_ai.analysis.integrity_checker

**Message:** Unused function: 'check_all' in 'mercury_ai.analysis.integrity_checker'

**Evidence:** Function 'check_all' at line 12 in 'mercury_ai.analysis.integrity_checker' is never called

**line:** 12

#### WARNING: mercury_ai.analysis.integrity_checker

**Message:** Unused function: '_check_snapshot' in 'mercury_ai.analysis.integrity_checker'

**Evidence:** Function '_check_snapshot' at line 22 in 'mercury_ai.analysis.integrity_checker' is never called

**line:** 22

#### WARNING: mercury_ai.analysis.learning_engine

**Message:** Unused function: 'run_learning' in 'mercury_ai.analysis.learning_engine'

**Evidence:** Function 'run_learning' at line 15 in 'mercury_ai.analysis.learning_engine' is never called

**line:** 15

#### WARNING: mercury_ai.analysis.learning_engine

**Message:** Unused function: '_accumulate' in 'mercury_ai.analysis.learning_engine'

**Evidence:** Function '_accumulate' at line 42 in 'mercury_ai.analysis.learning_engine' is never called

**line:** 42

#### WARNING: mercury_ai.analysis.learning_engine

**Message:** Unused function: '_finalize_stats' in 'mercury_ai.analysis.learning_engine'

**Evidence:** Function '_finalize_stats' at line 58 in 'mercury_ai.analysis.learning_engine' is never called

**line:** 58

#### WARNING: mercury_ai.analysis.live_monitor

**Message:** Unused function: 'start' in 'mercury_ai.analysis.live_monitor'

**Evidence:** Function 'start' at line 11 in 'mercury_ai.analysis.live_monitor' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.live_monitor

**Message:** Unused function: 'stop' in 'mercury_ai.analysis.live_monitor'

**Evidence:** Function 'stop' at line 14 in 'mercury_ai.analysis.live_monitor' is never called

**line:** 14

#### WARNING: mercury_ai.analysis.live_monitor

**Message:** Unused function: 'is_running' in 'mercury_ai.analysis.live_monitor'

**Evidence:** Function 'is_running' at line 18 in 'mercury_ai.analysis.live_monitor' is never called

**line:** 18

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function 'analyze' at line 18 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 18

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_detect_trend' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_detect_trend' at line 44 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 44

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_measure_ema_alignment' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_measure_ema_alignment' at line 52 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 52

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_measure_ema_distance' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_measure_ema_distance' at line 58 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 58

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_measure_ema_slope' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_measure_ema_slope' at line 75 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 75

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_analyze_price_position' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_analyze_price_position' at line 82 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 82

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_analyze_adx' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_analyze_adx' at line 96 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 96

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_analyze_rsi' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_analyze_rsi' at line 108 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 108

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_calculate_trend_strength' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_calculate_trend_strength' at line 119 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 119

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_detect_market_state' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_detect_market_state' at line 122 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 122

#### WARNING: mercury_ai.analysis.market_condition_engine

**Message:** Unused function: '_build_explanation' in 'mercury_ai.analysis.market_condition_engine'

**Evidence:** Function '_build_explanation' at line 129 in 'mercury_ai.analysis.market_condition_engine' is never called

**line:** 129

#### WARNING: mercury_ai.analysis.market_context_builder

**Message:** Unused function: 'build' in 'mercury_ai.analysis.market_context_builder'

**Evidence:** Function 'build' at line 34 in 'mercury_ai.analysis.market_context_builder' is never called

**line:** 34

#### WARNING: mercury_ai.analysis.market_regime_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.market_regime_engine'

**Evidence:** Function 'analyze' at line 16 in 'mercury_ai.analysis.market_regime_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.market_state_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.market_state_engine'

**Evidence:** Function 'analyze' at line 13 in 'mercury_ai.analysis.market_state_engine' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.market_structure_intelligence_engine

**Message:** Unused function: 'evaluate' in 'mercury_ai.analysis.market_structure_intelligence_engine'

**Evidence:** Function 'evaluate' at line 17 in 'mercury_ai.analysis.market_structure_intelligence_engine' is never called

**line:** 17

#### WARNING: mercury_ai.analysis.market_thesis_builder

**Message:** Unused function: 'build' in 'mercury_ai.analysis.market_thesis_builder'

**Evidence:** Function 'build' at line 29 in 'mercury_ai.analysis.market_thesis_builder' is never called

**line:** 29

#### WARNING: mercury_ai.analysis.metric_calculator

**Message:** Unused function: 'calculate' in 'mercury_ai.analysis.metric_calculator'

**Evidence:** Function 'calculate' at line 25 in 'mercury_ai.analysis.metric_calculator' is never called

**line:** 25

#### WARNING: mercury_ai.analysis.momentum_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.momentum_engine'

**Evidence:** Function 'analyze' at line 13 in 'mercury_ai.analysis.momentum_engine' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.momentum_engine

**Message:** Unused function: '_analyze_logic' in 'mercury_ai.analysis.momentum_engine'

**Evidence:** Function '_analyze_logic' at line 16 in 'mercury_ai.analysis.momentum_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.mtf_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.mtf_engine'

**Evidence:** Function 'analyze' at line 27 in 'mercury_ai.analysis.mtf_engine' is never called

**line:** 27

#### WARNING: mercury_ai.analysis.mtf_engine

**Message:** Unused function: '_determine_trend' in 'mercury_ai.analysis.mtf_engine'

**Evidence:** Function '_determine_trend' at line 74 in 'mercury_ai.analysis.mtf_engine' is never called

**line:** 74

#### WARNING: mercury_ai.analysis.mtf_engine

**Message:** Unused function: '_build_consensus' in 'mercury_ai.analysis.mtf_engine'

**Evidence:** Function '_build_consensus' at line 84 in 'mercury_ai.analysis.mtf_engine' is never called

**line:** 84

#### WARNING: mercury_ai.analysis.narrative_engine

**Message:** Unused function: 'generate' in 'mercury_ai.analysis.narrative_engine'

**Evidence:** Function 'generate' at line 11 in 'mercury_ai.analysis.narrative_engine' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.notification_center

**Message:** Unused function: 'send' in 'mercury_ai.analysis.notification_center'

**Evidence:** Function 'send' at line 22 in 'mercury_ai.analysis.notification_center' is never called

**line:** 22

#### WARNING: mercury_ai.analysis.notification_center

**Message:** Unused function: 'get_history' in 'mercury_ai.analysis.notification_center'

**Evidence:** Function 'get_history' at line 25 in 'mercury_ai.analysis.notification_center' is never called

**line:** 25

#### WARNING: mercury_ai.analysis.notification_center

**Message:** Unused function: 'export_to_json' in 'mercury_ai.analysis.notification_center'

**Evidence:** Function 'export_to_json' at line 33 in 'mercury_ai.analysis.notification_center' is never called

**line:** 33

#### WARNING: mercury_ai.analysis.notification_center

**Message:** Unused function: 'export_to_csv' in 'mercury_ai.analysis.notification_center'

**Evidence:** Function 'export_to_csv' at line 37 in 'mercury_ai.analysis.notification_center' is never called

**line:** 37

#### WARNING: mercury_ai.analysis.operational_history

**Message:** Unused function: 'query' in 'mercury_ai.analysis.operational_history'

**Evidence:** Function 'query' at line 13 in 'mercury_ai.analysis.operational_history' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.performance_analytics

**Message:** Unused function: 'analyze_performance' in 'mercury_ai.analysis.performance_analytics'

**Evidence:** Function 'analyze_performance' at line 13 in 'mercury_ai.analysis.performance_analytics' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.performance_center

**Message:** Unused function: 'get_report' in 'mercury_ai.analysis.performance_center'

**Evidence:** Function 'get_report' at line 18 in 'mercury_ai.analysis.performance_center' is never called

**line:** 18

#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Unused function: 'calculate_asset_performance' in 'mercury_ai.analysis.performance_engine'

**Evidence:** Function 'calculate_asset_performance' at line 16 in 'mercury_ai.analysis.performance_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Unused function: 'calculate_universe_performance' in 'mercury_ai.analysis.performance_engine'

**Evidence:** Function 'calculate_universe_performance' at line 66 in 'mercury_ai.analysis.performance_engine' is never called

**line:** 66

#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Unused function: '_calculate_drawdown' in 'mercury_ai.analysis.performance_engine'

**Evidence:** Function '_calculate_drawdown' at line 102 in 'mercury_ai.analysis.performance_engine' is never called

**line:** 102

#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Unused function: '_calculate_sharpe' in 'mercury_ai.analysis.performance_engine'

**Evidence:** Function '_calculate_sharpe' at line 123 in 'mercury_ai.analysis.performance_engine' is never called

**line:** 123

#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Unused function: '_calculate_sortino' in 'mercury_ai.analysis.performance_engine'

**Evidence:** Function '_calculate_sortino' at line 129 in 'mercury_ai.analysis.performance_engine' is never called

**line:** 129

#### WARNING: mercury_ai.analysis.performance_engine

**Message:** Unused function: '_empty_asset_performance' in 'mercury_ai.analysis.performance_engine'

**Evidence:** Function '_empty_asset_performance' at line 137 in 'mercury_ai.analysis.performance_engine' is never called

**line:** 137

#### WARNING: mercury_ai.analysis.performance_statistics

**Message:** Unused function: 'calculate' in 'mercury_ai.analysis.performance_statistics'

**Evidence:** Function 'calculate' at line 8 in 'mercury_ai.analysis.performance_statistics' is never called

**line:** 8

#### WARNING: mercury_ai.analysis.post_decision_evaluation_engine

**Message:** Unused function: 'evaluate' in 'mercury_ai.analysis.post_decision_evaluation_engine'

**Evidence:** Function 'evaluate' at line 10 in 'mercury_ai.analysis.post_decision_evaluation_engine' is never called

**line:** 10

#### WARNING: mercury_ai.analysis.price_action_analyzer

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.price_action_analyzer'

**Evidence:** Function 'analyze' at line 6 in 'mercury_ai.analysis.price_action_analyzer' is never called

**line:** 6

#### WARNING: mercury_ai.analysis.price_action_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.price_action_engine'

**Evidence:** Function 'analyze' at line 12 in 'mercury_ai.analysis.price_action_engine' is never called

**line:** 12

#### WARNING: mercury_ai.analysis.price_action_engine

**Message:** Unused function: '_analyze_logic' in 'mercury_ai.analysis.price_action_engine'

**Evidence:** Function '_analyze_logic' at line 18 in 'mercury_ai.analysis.price_action_engine' is never called

**line:** 18

#### WARNING: mercury_ai.analysis.provider_priority_engine

**Message:** Unused function: 'get_optimal_provider' in 'mercury_ai.analysis.provider_priority_engine'

**Evidence:** Function 'get_optimal_provider' at line 12 in 'mercury_ai.analysis.provider_priority_engine' is never called

**line:** 12

#### WARNING: mercury_ai.analysis.ranking_engine

**Message:** Unused function: 'rank' in 'mercury_ai.analysis.ranking_engine'

**Evidence:** Function 'rank' at line 14 in 'mercury_ai.analysis.ranking_engine' is never called

**line:** 14

#### WARNING: mercury_ai.analysis.replay_batch_processor

**Message:** Unused function: 'run_batch' in 'mercury_ai.analysis.replay_batch_processor'

**Evidence:** Function 'run_batch' at line 87 in 'mercury_ai.analysis.replay_batch_processor' is never called

**line:** 87

#### WARNING: mercury_ai.analysis.replay_batch_processor

**Message:** Unused function: '_run_single_symbol' in 'mercury_ai.analysis.replay_batch_processor'

**Evidence:** Function '_run_single_symbol' at line 162 in 'mercury_ai.analysis.replay_batch_processor' is never called

**line:** 162

#### WARNING: mercury_ai.analysis.replay_batch_processor

**Message:** Unused function: '_aggregate_cache_stats' in 'mercury_ai.analysis.replay_batch_processor'

**Evidence:** Function '_aggregate_cache_stats' at line 209 in 'mercury_ai.analysis.replay_batch_processor' is never called

**line:** 209

#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Unused function: 'get' in 'mercury_ai.analysis.replay_cache'

**Evidence:** Function 'get' at line 36 in 'mercury_ai.analysis.replay_cache' is never called

**line:** 36

#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Unused function: 'put' in 'mercury_ai.analysis.replay_cache'

**Evidence:** Function 'put' at line 47 in 'mercury_ai.analysis.replay_cache' is never called

**line:** 47

#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Unused function: 'clear' in 'mercury_ai.analysis.replay_cache'

**Evidence:** Function 'clear' at line 58 in 'mercury_ai.analysis.replay_cache' is never called

**line:** 58

#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Unused function: 'hit_rate' in 'mercury_ai.analysis.replay_cache'

**Evidence:** Function 'hit_rate' at line 66 in 'mercury_ai.analysis.replay_cache' is never called

**line:** 66

#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Unused function: 'size' in 'mercury_ai.analysis.replay_cache'

**Evidence:** Function 'size' at line 74 in 'mercury_ai.analysis.replay_cache' is never called

**line:** 74

#### WARNING: mercury_ai.analysis.replay_cache

**Message:** Unused function: 'stats' in 'mercury_ai.analysis.replay_cache'

**Evidence:** Function 'stats' at line 80 in 'mercury_ai.analysis.replay_cache' is never called

**line:** 80

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: 'assess' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function 'assess' at line 42 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 42

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: 'assess_simple' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function 'assess_simple' at line 134 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 134

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: '_compute_var_cvar' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function '_compute_var_cvar' at line 263 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 263

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: '_compute_kelly' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function '_compute_kelly' at line 304 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 304

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: '_compute_correlation_matrix' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function '_compute_correlation_matrix' at line 347 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 347

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: '_pearson_correlation' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function '_pearson_correlation' at line 383 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 383

#### WARNING: mercury_ai.analysis.risk_engine

**Message:** Unused function: '_compute_stress_test' in 'mercury_ai.analysis.risk_engine'

**Evidence:** Function '_compute_stress_test' at line 404 in 'mercury_ai.analysis.risk_engine' is never called

**line:** 404

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.session_engine'

**Evidence:** Function 'analyze' at line 11 in 'mercury_ai.analysis.session_engine' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Unused function: '_detect_session' in 'mercury_ai.analysis.session_engine'

**Evidence:** Function '_detect_session' at line 29 in 'mercury_ai.analysis.session_engine' is never called

**line:** 29

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Unused function: '_detect_overlap' in 'mercury_ai.analysis.session_engine'

**Evidence:** Function '_detect_overlap' at line 47 in 'mercury_ai.analysis.session_engine' is never called

**line:** 47

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Unused function: '_calculate_quality' in 'mercury_ai.analysis.session_engine'

**Evidence:** Function '_calculate_quality' at line 57 in 'mercury_ai.analysis.session_engine' is never called

**line:** 57

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Unused function: '_calculate_liquidity' in 'mercury_ai.analysis.session_engine'

**Evidence:** Function '_calculate_liquidity' at line 66 in 'mercury_ai.analysis.session_engine' is never called

**line:** 66

#### WARNING: mercury_ai.analysis.session_engine

**Message:** Unused function: '_build_explanation' in 'mercury_ai.analysis.session_engine'

**Evidence:** Function '_build_explanation' at line 75 in 'mercury_ai.analysis.session_engine' is never called

**line:** 75

#### WARNING: mercury_ai.analysis.statistical_auditor

**Message:** Unused function: 'audit' in 'mercury_ai.analysis.statistical_auditor'

**Evidence:** Function 'audit' at line 9 in 'mercury_ai.analysis.statistical_auditor' is never called

**line:** 9

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function 'analyze' at line 16 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_detect_swings' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_detect_swings' at line 60 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 60

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_cluster_zones' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_cluster_zones' at line 70 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 70

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_finalize_zone' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_finalize_zone' at line 85 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 85

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_score_zones' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_score_zones' at line 97 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 97

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_find_nearest_zones' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_find_nearest_zones' at line 101 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 101

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_detect_price_location' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_detect_price_location' at line 109 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 109

#### WARNING: mercury_ai.analysis.support_resistance_analyzer

**Message:** Unused function: '_build_explanation' in 'mercury_ai.analysis.support_resistance_analyzer'

**Evidence:** Function '_build_explanation' at line 114 in 'mercury_ai.analysis.support_resistance_analyzer' is never called

**line:** 114

#### WARNING: mercury_ai.analysis.swing_engine

**Message:** Unused function: 'calculate_atr' in 'mercury_ai.analysis.swing_engine'

**Evidence:** Function 'calculate_atr' at line 28 in 'mercury_ai.analysis.swing_engine' is never called

**line:** 28

#### WARNING: mercury_ai.analysis.swing_engine

**Message:** Unused function: 'detect_swings' in 'mercury_ai.analysis.swing_engine'

**Evidence:** Function 'detect_swings' at line 65 in 'mercury_ai.analysis.swing_engine' is never called

**line:** 65

#### WARNING: mercury_ai.analysis.swing_engine

**Message:** Unused function: 'analyze_sequence' in 'mercury_ai.analysis.swing_engine'

**Evidence:** Function 'analyze_sequence' at line 283 in 'mercury_ai.analysis.swing_engine' is never called

**line:** 283

#### WARNING: mercury_ai.analysis.trade_memory_engine

**Message:** Unused function: 'save_trade' in 'mercury_ai.analysis.trade_memory_engine'

**Evidence:** Function 'save_trade' at line 13 in 'mercury_ai.analysis.trade_memory_engine' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.trade_memory_engine

**Message:** Unused function: 'find_similar_trades' in 'mercury_ai.analysis.trade_memory_engine'

**Evidence:** Function 'find_similar_trades' at line 19 in 'mercury_ai.analysis.trade_memory_engine' is never called

**line:** 19

#### WARNING: mercury_ai.analysis.trade_outcome_engine

**Message:** Unused function: 'determine_outcome' in 'mercury_ai.analysis.trade_outcome_engine'

**Evidence:** Function 'determine_outcome' at line 9 in 'mercury_ai.analysis.trade_outcome_engine' is never called

**line:** 9

#### WARNING: mercury_ai.analysis.trend_analyzer

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.trend_analyzer'

**Evidence:** Function 'analyze' at line 10 in 'mercury_ai.analysis.trend_analyzer' is never called

**line:** 10

#### WARNING: mercury_ai.analysis.validation_engine

**Message:** Unused function: 'validate_all' in 'mercury_ai.analysis.validation_engine'

**Evidence:** Function 'validate_all' at line 11 in 'mercury_ai.analysis.validation_engine' is never called

**line:** 11

#### WARNING: mercury_ai.analysis.validation_engine

**Message:** Unused function: '_validate_evidence_consistency' in 'mercury_ai.analysis.validation_engine'

**Evidence:** Function '_validate_evidence_consistency' at line 26 in 'mercury_ai.analysis.validation_engine' is never called

**line:** 26

#### WARNING: mercury_ai.analysis.validation_engine

**Message:** Unused function: '_validate_context_consistency' in 'mercury_ai.analysis.validation_engine'

**Evidence:** Function '_validate_context_consistency' at line 34 in 'mercury_ai.analysis.validation_engine' is never called

**line:** 34

#### WARNING: mercury_ai.analysis.volatility_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.volatility_engine'

**Evidence:** Function 'analyze' at line 20 in 'mercury_ai.analysis.volatility_engine' is never called

**line:** 20

#### WARNING: mercury_ai.analysis.volume_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.volume_engine'

**Evidence:** Function 'analyze' at line 13 in 'mercury_ai.analysis.volume_engine' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.volume_engine

**Message:** Unused function: '_analyze_logic' in 'mercury_ai.analysis.volume_engine'

**Evidence:** Function '_analyze_logic' at line 16 in 'mercury_ai.analysis.volume_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.volume_intelligence_engine

**Message:** Unused function: 'evaluate' in 'mercury_ai.analysis.volume_intelligence_engine'

**Evidence:** Function 'evaluate' at line 15 in 'mercury_ai.analysis.volume_intelligence_engine' is never called

**line:** 15

#### WARNING: mercury_ai.analysis.vwap_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.vwap_engine'

**Evidence:** Function 'analyze' at line 13 in 'mercury_ai.analysis.vwap_engine' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.vwap_engine

**Message:** Unused function: '_analyze_logic' in 'mercury_ai.analysis.vwap_engine'

**Evidence:** Function '_analyze_logic' at line 16 in 'mercury_ai.analysis.vwap_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.weight_simulator

**Message:** Unused function: 'simulate' in 'mercury_ai.analysis.weight_simulator'

**Evidence:** Function 'simulate' at line 15 in 'mercury_ai.analysis.weight_simulator' is never called

**line:** 15

#### WARNING: mercury_ai.analysis.smart_money.bos_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.smart_money.bos_engine'

**Evidence:** Function 'analyze' at line 16 in 'mercury_ai.analysis.smart_money.bos_engine' is never called

**line:** 16

#### WARNING: mercury_ai.analysis.smart_money.choch_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.smart_money.choch_engine'

**Evidence:** Function 'analyze' at line 17 in 'mercury_ai.analysis.smart_money.choch_engine' is never called

**line:** 17

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'build_equal_high_groups' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'build_equal_high_groups' at line 96 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 96

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'validate_equal_high_groups' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'validate_equal_high_groups' at line 154 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 154

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'calculate_metrics' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'calculate_metrics' at line 190 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 190

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'calculate_scores' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'calculate_scores' at line 199 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 199

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'select_best_equal_high' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'select_best_equal_high' at line 218 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 218

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'populate_profile' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'populate_profile' at line 222 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 222

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'generate_equal_high_evidence' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'generate_equal_high_evidence' at line 225 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 225

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'analyze' at line 245 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 245

#### WARNING: mercury_ai.analysis.smart_money.liquidity_engine

**Message:** Unused function: 'analyze_tuple' in 'mercury_ai.analysis.smart_money.liquidity_engine'

**Evidence:** Function 'analyze_tuple' at line 290 in 'mercury_ai.analysis.smart_money.liquidity_engine' is never called

**line:** 290

#### WARNING: mercury_ai.analysis.smart_money.liquidity_event_engine

**Message:** Unused function: 'detect' in 'mercury_ai.analysis.smart_money.liquidity_event_engine'

**Evidence:** Function 'detect' at line 20 in 'mercury_ai.analysis.smart_money.liquidity_event_engine' is never called

**line:** 20

#### WARNING: mercury_ai.analysis.smart_money.liquidity_event_engine

**Message:** Unused function: 'to_evidence' in 'mercury_ai.analysis.smart_money.liquidity_event_engine'

**Evidence:** Function 'to_evidence' at line 40 in 'mercury_ai.analysis.smart_money.liquidity_event_engine' is never called

**line:** 40

#### WARNING: mercury_ai.analysis.smart_money.market_structure_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.smart_money.market_structure_engine'

**Evidence:** Function 'analyze' at line 8 in 'mercury_ai.analysis.smart_money.market_structure_engine' is never called

**line:** 8

#### WARNING: mercury_ai.analysis.smart_money.order_block_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.smart_money.order_block_engine'

**Evidence:** Function 'analyze' at line 10 in 'mercury_ai.analysis.smart_money.order_block_engine' is never called

**line:** 10

#### WARNING: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.analysis.smart_money.smart_money_engine'

**Evidence:** Function 'analyze' at line 26 in 'mercury_ai.analysis.smart_money.smart_money_engine' is never called

**line:** 26

#### WARNING: mercury_ai.analysis.smart_money.smart_money_engine

**Message:** Unused function: 'get_evidences' in 'mercury_ai.analysis.smart_money.smart_money_engine'

**Evidence:** Function 'get_evidences' at line 70 in 'mercury_ai.analysis.smart_money.smart_money_engine' is never called

**line:** 70

#### WARNING: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases

**Message:** Unused function: 'engine' in 'mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases'

**Evidence:** Function 'engine' at line 13 in 'mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases' is never called

**line:** 13

#### WARNING: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Message:** Unused function: 'default_engine' in 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine'

**Evidence:** Function 'default_engine' at line 23 in 'mercury_ai.analysis.smart_money.tests.test_liquidity_engine' is never called

**line:** 23

#### WARNING: mercury_ai.analysis.tests.test_fvg_engine

**Message:** Unused function: 'fvg_engine' in 'mercury_ai.analysis.tests.test_fvg_engine'

**Evidence:** Function 'fvg_engine' at line 8 in 'mercury_ai.analysis.tests.test_fvg_engine' is never called

**line:** 8

#### WARNING: mercury_ai.analysis.tests.test_historical_replay_engine

**Message:** Unused function: 'sample_df' in 'mercury_ai.analysis.tests.test_historical_replay_engine'

**Evidence:** Function 'sample_df' at line 15 in 'mercury_ai.analysis.tests.test_historical_replay_engine' is never called

**line:** 15

#### WARNING: mercury_ai.analysis.tests.test_market_structure_engine

**Message:** Unused function: 'ms_engine' in 'mercury_ai.analysis.tests.test_market_structure_engine'

**Evidence:** Function 'ms_engine' at line 7 in 'mercury_ai.analysis.tests.test_market_structure_engine' is never called

**line:** 7

#### WARNING: mercury_ai.analysis.tests.test_momentum_engine

**Message:** Unused function: 'momentum_engine' in 'mercury_ai.analysis.tests.test_momentum_engine'

**Evidence:** Function 'momentum_engine' at line 9 in 'mercury_ai.analysis.tests.test_momentum_engine' is never called

**line:** 9

#### WARNING: mercury_ai.analysis.tests.test_price_action_engine

**Message:** Unused function: 'price_action_engine' in 'mercury_ai.analysis.tests.test_price_action_engine'

**Evidence:** Function 'price_action_engine' at line 8 in 'mercury_ai.analysis.tests.test_price_action_engine' is never called

**line:** 8

#### WARNING: mercury_ai.analysis.tests.test_replay_batch_processor

**Message:** Unused function: 'sample_data_map' in 'mercury_ai.analysis.tests.test_replay_batch_processor'

**Evidence:** Function 'sample_data_map' at line 19 in 'mercury_ai.analysis.tests.test_replay_batch_processor' is never called

**line:** 19

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused function: 'put_entries' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Function 'put_entries' at line 153 in 'mercury_ai.analysis.tests.test_replay_cache' is never called

**line:** 153

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused function: 'reader' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Function 'reader' at line 187 in 'mercury_ai.analysis.tests.test_replay_cache' is never called

**line:** 187

#### WARNING: mercury_ai.analysis.tests.test_replay_cache

**Message:** Unused function: 'writer' in 'mercury_ai.analysis.tests.test_replay_cache'

**Evidence:** Function 'writer' at line 195 in 'mercury_ai.analysis.tests.test_replay_cache' is never called

**line:** 195

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused function: 'engine' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Function 'engine' at line 32 in 'mercury_ai.analysis.tests.test_risk_engine' is never called

**line:** 32

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused function: 'mock_context' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Function 'mock_context' at line 38 in 'mercury_ai.analysis.tests.test_risk_engine' is never called

**line:** 38

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused function: 'mock_evidence_bundle' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Function 'mock_evidence_bundle' at line 66 in 'mercury_ai.analysis.tests.test_risk_engine' is never called

**line:** 66

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused function: 'sample_returns_normal' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Function 'sample_returns_normal' at line 104 in 'mercury_ai.analysis.tests.test_risk_engine' is never called

**line:** 104

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused function: 'sample_returns_positive' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Function 'sample_returns_positive' at line 117 in 'mercury_ai.analysis.tests.test_risk_engine' is never called

**line:** 117

#### WARNING: mercury_ai.analysis.tests.test_risk_engine

**Message:** Unused function: 'sample_returns_negative' in 'mercury_ai.analysis.tests.test_risk_engine'

**Evidence:** Function 'sample_returns_negative' at line 125 in 'mercury_ai.analysis.tests.test_risk_engine' is never called

**line:** 125

#### WARNING: mercury_ai.analysis.tests.test_trend_engine

**Message:** Unused function: 'trend_engine' in 'mercury_ai.analysis.tests.test_trend_engine'

**Evidence:** Function 'trend_engine' at line 7 in 'mercury_ai.analysis.tests.test_trend_engine' is never called

**line:** 7

#### WARNING: mercury_ai.analysis.tests.test_volume_engine

**Message:** Unused function: 'volume_engine' in 'mercury_ai.analysis.tests.test_volume_engine'

**Evidence:** Function 'volume_engine' at line 8 in 'mercury_ai.analysis.tests.test_volume_engine' is never called

**line:** 8

#### WARNING: mercury_ai.analysis.tests.test_vwap_engine

**Message:** Unused function: 'vwap_engine' in 'mercury_ai.analysis.tests.test_vwap_engine'

**Evidence:** Function 'vwap_engine' at line 8 in 'mercury_ai.analysis.tests.test_vwap_engine' is never called

**line:** 8

#### WARNING: mercury_ai.brain.explainability_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.brain.explainability_engine'

**Evidence:** Function 'analyze' at line 13 in 'mercury_ai.brain.explainability_engine' is never called

**line:** 13

#### WARNING: mercury_ai.brain.institutional_brain

**Message:** Unused function: 'explain' in 'mercury_ai.brain.institutional_brain'

**Evidence:** Function 'explain' at line 12 in 'mercury_ai.brain.institutional_brain' is never called

**line:** 12

#### WARNING: mercury_ai.brain.mercury_decision_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.brain.mercury_decision_engine'

**Evidence:** Function 'analyze' at line 94 in 'mercury_ai.brain.mercury_decision_engine' is never called

**line:** 94

#### WARNING: mercury_ai.brain.mercury_decision_engine

**Message:** Unused function: '_analyze_logic' in 'mercury_ai.brain.mercury_decision_engine'

**Evidence:** Function '_analyze_logic' at line 113 in 'mercury_ai.brain.mercury_decision_engine' is never called

**line:** 113

#### WARNING: mercury_ai.brain.probability_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.brain.probability_engine'

**Evidence:** Function 'analyze' at line 34 in 'mercury_ai.brain.probability_engine' is never called

**line:** 34

#### WARNING: mercury_ai.brain.scanner

**Message:** Unused function: 'scan' in 'mercury_ai.brain.scanner'

**Evidence:** Function 'scan' at line 47 in 'mercury_ai.brain.scanner' is never called

**line:** 47

#### WARNING: mercury_ai.brain.scanner

**Message:** Unused function: '_print_ranking' in 'mercury_ai.brain.scanner'

**Evidence:** Function '_print_ranking' at line 180 in 'mercury_ai.brain.scanner' is never called

**line:** 180

#### WARNING: mercury_ai.brain.scanner

**Message:** Unused function: '_print_report' in 'mercury_ai.brain.scanner'

**Evidence:** Function '_print_report' at line 207 in 'mercury_ai.brain.scanner' is never called

**line:** 207

#### WARNING: mercury_ai.brain.scanner

**Message:** Unused function: '_print_line' in 'mercury_ai.brain.scanner'

**Evidence:** Function '_print_line' at line 283 in 'mercury_ai.brain.scanner' is never called

**line:** 283

#### WARNING: mercury_ai.brain.scanner

**Message:** Unused function: '_value' in 'mercury_ai.brain.scanner'

**Evidence:** Function '_value' at line 287 in 'mercury_ai.brain.scanner' is never called

**line:** 287

#### WARNING: mercury_ai.brain.tests.test_mercury_decision_engine

**Message:** Unused function: 'decision_engine' in 'mercury_ai.brain.tests.test_mercury_decision_engine'

**Evidence:** Function 'decision_engine' at line 15 in 'mercury_ai.brain.tests.test_mercury_decision_engine' is never called

**line:** 15

#### WARNING: mercury_ai.calendar.economic_calendar

**Message:** Unused function: 'get_events' in 'mercury_ai.calendar.economic_calendar'

**Evidence:** Function 'get_events' at line 6 in 'mercury_ai.calendar.economic_calendar' is never called

**line:** 6

#### WARNING: mercury_ai.config.configuration_center

**Message:** Unused function: '_load_from_file' in 'mercury_ai.config.configuration_center'

**Evidence:** Function '_load_from_file' at line 26 in 'mercury_ai.config.configuration_center' is never called

**line:** 26

#### WARNING: mercury_ai.config.configuration_center

**Message:** Unused function: 'save' in 'mercury_ai.config.configuration_center'

**Evidence:** Function 'save' at line 39 in 'mercury_ai.config.configuration_center' is never called

**line:** 39

#### WARNING: mercury_ai.config.configuration_center

**Message:** Unused function: 'get' in 'mercury_ai.config.configuration_center'

**Evidence:** Function 'get' at line 47 in 'mercury_ai.config.configuration_center' is never called

**line:** 47

#### WARNING: mercury_ai.config.universe

**Message:** Unused function: 'get_asset' in 'mercury_ai.config.universe'

**Evidence:** Function 'get_asset' at line 432 in 'mercury_ai.config.universe' is never called

**line:** 432

#### WARNING: mercury_ai.config.universe

**Message:** Unused function: 'get_enabled_symbols' in 'mercury_ai.config.universe'

**Evidence:** Function 'get_enabled_symbols' at line 437 in 'mercury_ai.config.universe' is never called

**line:** 437

#### WARNING: mercury_ai.config.universe

**Message:** Unused function: 'get_all_provider_symbols' in 'mercury_ai.config.universe'

**Evidence:** Function 'get_all_provider_symbols' at line 452 in 'mercury_ai.config.universe' is never called

**line:** 452

#### WARNING: mercury_ai.config.universe

**Message:** Unused function: 'validate_symbol' in 'mercury_ai.config.universe'

**Evidence:** Function 'validate_symbol' at line 457 in 'mercury_ai.config.universe' is never called

**line:** 457

#### WARNING: mercury_ai.config.universe

**Message:** Unused function: 'universe_summary' in 'mercury_ai.config.universe'

**Evidence:** Function 'universe_summary' at line 462 in 'mercury_ai.config.universe' is never called

**line:** 462

#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** Unused function: '_record_telemetry' in 'mercury_ai.core.analysis_pipeline'

**Evidence:** Function '_record_telemetry' at line 113 in 'mercury_ai.core.analysis_pipeline' is never called

**line:** 113

#### WARNING: mercury_ai.core.analysis_pipeline

**Message:** Unused function: 'analyze' in 'mercury_ai.core.analysis_pipeline'

**Evidence:** Function 'analyze' at line 159 in 'mercury_ai.core.analysis_pipeline' is never called

**line:** 159

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: '_load_from_file' in 'mercury_ai.core.asset_registry'

**Evidence:** Function '_load_from_file' at line 33 in 'mercury_ai.core.asset_registry' is never called

**line:** 33

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'save' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'save' at line 43 in 'mercury_ai.core.asset_registry' is never called

**line:** 43

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'register_asset' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'register_asset' at line 48 in 'mercury_ai.core.asset_registry' is never called

**line:** 48

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'set_enabled' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'set_enabled' at line 58 in 'mercury_ai.core.asset_registry' is never called

**line:** 58

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'set_priority' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'set_priority' at line 63 in 'mercury_ai.core.asset_registry' is never called

**line:** 63

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'update_asset_stats' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'update_asset_stats' at line 68 in 'mercury_ai.core.asset_registry' is never called

**line:** 68

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'get_enabled_assets' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'get_enabled_assets' at line 74 in 'mercury_ai.core.asset_registry' is never called

**line:** 74

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'get_assets_for_broker' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'get_assets_for_broker' at line 77 in 'mercury_ai.core.asset_registry' is never called

**line:** 77

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'search_assets' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'search_assets' at line 87 in 'mercury_ai.core.asset_registry' is never called

**line:** 87

#### WARNING: mercury_ai.core.asset_registry

**Message:** Unused function: 'filter_assets' in 'mercury_ai.core.asset_registry'

**Evidence:** Function 'filter_assets' at line 91 in 'mercury_ai.core.asset_registry' is never called

**line:** 91

#### WARNING: mercury_ai.core.audit_sink

**Message:** Unused function: 'log' in 'mercury_ai.core.audit_sink'

**Evidence:** Function 'log' at line 12 in 'mercury_ai.core.audit_sink' is never called

**line:** 12

#### WARNING: mercury_ai.core.audit_sink

**Message:** Unused function: 'log' in 'mercury_ai.core.audit_sink'

**Evidence:** Function 'log' at line 19 in 'mercury_ai.core.audit_sink' is never called

**line:** 19

#### WARNING: mercury_ai.core.audit_sink

**Message:** Unused function: 'get_events' in 'mercury_ai.core.audit_sink'

**Evidence:** Function 'get_events' at line 22 in 'mercury_ai.core.audit_sink' is never called

**line:** 22

#### WARNING: mercury_ai.core.auto_health

**Message:** Unused function: 'run_all_checks' in 'mercury_ai.core.auto_health'

**Evidence:** Function 'run_all_checks' at line 14 in 'mercury_ai.core.auto_health' is never called

**line:** 14

#### WARNING: mercury_ai.core.base_engine

**Message:** Unused function: 'analyze' in 'mercury_ai.core.base_engine'

**Evidence:** Function 'analyze' at line 15 in 'mercury_ai.core.base_engine' is never called

**line:** 15

#### WARNING: mercury_ai.core.data_quality_gate

**Message:** Unused function: 'evaluate' in 'mercury_ai.core.data_quality_gate'

**Evidence:** Function 'evaluate' at line 20 in 'mercury_ai.core.data_quality_gate' is never called

**line:** 20

#### WARNING: mercury_ai.core.export_center

**Message:** Unused function: 'export_data' in 'mercury_ai.core.export_center'

**Evidence:** Function 'export_data' at line 17 in 'mercury_ai.core.export_center' is never called

**line:** 17

#### WARNING: mercury_ai.core.export_center

**Message:** Unused function: 'export_history' in 'mercury_ai.core.export_center'

**Evidence:** Function 'export_history' at line 54 in 'mercury_ai.core.export_center' is never called

**line:** 54

#### WARNING: mercury_ai.core.export_center

**Message:** Unused function: 'export_snapshots' in 'mercury_ai.core.export_center'

**Evidence:** Function 'export_snapshots' at line 58 in 'mercury_ai.core.export_center' is never called

**line:** 58

#### WARNING: mercury_ai.core.health_center

**Message:** Unused function: 'get_system_metrics' in 'mercury_ai.core.health_center'

**Evidence:** Function 'get_system_metrics' at line 10 in 'mercury_ai.core.health_center' is never called

**line:** 10

#### WARNING: mercury_ai.core.health_center

**Message:** Unused function: 'get_component_health' in 'mercury_ai.core.health_center'

**Evidence:** Function 'get_component_health' at line 19 in 'mercury_ai.core.health_center' is never called

**line:** 19

#### WARNING: mercury_ai.core.job_manager

**Message:** Unused function: '_job_loop' in 'mercury_ai.core.job_manager'

**Evidence:** Function '_job_loop' at line 26 in 'mercury_ai.core.job_manager' is never called

**line:** 26

#### WARNING: mercury_ai.core.job_manager

**Message:** Unused function: '_execute_tasks' in 'mercury_ai.core.job_manager'

**Evidence:** Function '_execute_tasks' at line 32 in 'mercury_ai.core.job_manager' is never called

**line:** 32

#### WARNING: mercury_ai.core.job_manager

**Message:** Unused function: 'start' in 'mercury_ai.core.job_manager'

**Evidence:** Function 'start' at line 42 in 'mercury_ai.core.job_manager' is never called

**line:** 42

#### WARNING: mercury_ai.core.job_manager

**Message:** Unused function: 'pause' in 'mercury_ai.core.job_manager'

**Evidence:** Function 'pause' at line 49 in 'mercury_ai.core.job_manager' is never called

**line:** 49

#### WARNING: mercury_ai.core.job_manager

**Message:** Unused function: 'resume' in 'mercury_ai.core.job_manager'

**Evidence:** Function 'resume' at line 52 in 'mercury_ai.core.job_manager' is never called

**line:** 52

#### WARNING: mercury_ai.core.job_manager

**Message:** Unused function: 'stop' in 'mercury_ai.core.job_manager'

**Evidence:** Function 'stop' at line 55 in 'mercury_ai.core.job_manager' is never called

**line:** 55

#### WARNING: mercury_ai.core.observability_center

**Message:** Unused function: 'record_engine_time' in 'mercury_ai.core.observability_center'

**Evidence:** Function 'record_engine_time' at line 16 in 'mercury_ai.core.observability_center' is never called

**line:** 16

#### WARNING: mercury_ai.core.observability_center

**Message:** Unused function: 'record_provider_latency' in 'mercury_ai.core.observability_center'

**Evidence:** Function 'record_provider_latency' at line 19 in 'mercury_ai.core.observability_center' is never called

**line:** 19

#### WARNING: mercury_ai.core.observability_center

**Message:** Unused function: 'record_asset_time' in 'mercury_ai.core.observability_center'

**Evidence:** Function 'record_asset_time' at line 22 in 'mercury_ai.core.observability_center' is never called

**line:** 22

#### WARNING: mercury_ai.core.observability_center

**Message:** Unused function: 'get_metrics' in 'mercury_ai.core.observability_center'

**Evidence:** Function 'get_metrics' at line 25 in 'mercury_ai.core.observability_center' is never called

**line:** 25

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'start_pipeline' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'start_pipeline' at line 29 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 29

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'end_pipeline' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'end_pipeline' at line 36 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 36

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'start_stage' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'start_stage' at line 40 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 40

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'end_stage' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'end_stage' at line 51 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 51

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'summary' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'summary' at line 66 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 66

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'json' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'json' at line 74 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 74

#### WARNING: mercury_ai.core.pipeline_profiler

**Message:** Unused function: 'pretty_print' in 'mercury_ai.core.pipeline_profiler'

**Evidence:** Function 'pretty_print' at line 79 in 'mercury_ai.core.pipeline_profiler' is never called

**line:** 79

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'metadata' in 'mercury_ai.core.project_state'

**Evidence:** Function 'metadata' at line 29 in 'mercury_ai.core.project_state' is never called

**line:** 29

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'json' in 'mercury_ai.core.project_state'

**Evidence:** Function 'json' at line 33 in 'mercury_ai.core.project_state' is never called

**line:** 33

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'documents' in 'mercury_ai.core.project_state'

**Evidence:** Function 'documents' at line 37 in 'mercury_ai.core.project_state' is never called

**line:** 37

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'statistics' in 'mercury_ai.core.project_state'

**Evidence:** Function 'statistics' at line 41 in 'mercury_ai.core.project_state' is never called

**line:** 41

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'get' in 'mercury_ai.core.project_state'

**Evidence:** Function 'get' at line 44 in 'mercury_ai.core.project_state' is never called

**line:** 44

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'has' in 'mercury_ai.core.project_state'

**Evidence:** Function 'has' at line 47 in 'mercury_ai.core.project_state' is never called

**line:** 47

#### WARNING: mercury_ai.core.project_state

**Message:** Unused function: 'summary' in 'mercury_ai.core.project_state'

**Evidence:** Function 'summary' at line 50 in 'mercury_ai.core.project_state' is never called

**line:** 50

#### WARNING: mercury_ai.core.runtime_report

**Message:** Unused function: 'to_dict' in 'mercury_ai.core.runtime_report'

**Evidence:** Function 'to_dict' at line 28 in 'mercury_ai.core.runtime_report' is never called

**line:** 28

#### WARNING: mercury_ai.core.security_center

**Message:** Unused function: 'log_event' in 'mercury_ai.core.security_center'

**Evidence:** Function 'log_event' at line 20 in 'mercury_ai.core.security_center' is never called

**line:** 20

#### WARNING: mercury_ai.core.security_center

**Message:** Unused function: 'generate_audit_trail' in 'mercury_ai.core.security_center'

**Evidence:** Function 'generate_audit_trail' at line 24 in 'mercury_ai.core.security_center' is never called

**line:** 24

#### WARNING: mercury_ai.core.security_center

**Message:** Unused function: 'generate_security_report' in 'mercury_ai.core.security_center'

**Evidence:** Function 'generate_security_report' at line 27 in 'mercury_ai.core.security_center' is never called

**line:** 27

#### WARNING: mercury_ai.core.session_manager

**Message:** Unused function: 'get_info' in 'mercury_ai.core.session_manager'

**Evidence:** Function 'get_info' at line 16 in 'mercury_ai.core.session_manager' is never called

**line:** 16

#### WARNING: mercury_ai.core.startup

**Message:** Unused function: 'start' in 'mercury_ai.core.startup'

**Evidence:** Function 'start' at line 5 in 'mercury_ai.core.startup' is never called

**line:** 5

#### WARNING: mercury_ai.core._stage_builder

**Message:** Unused function: 'duration' in 'mercury_ai.core._stage_builder'

**Evidence:** Function 'duration' at line 27 in 'mercury_ai.core._stage_builder' is never called

**line:** 27

#### WARNING: mercury_ai.core._stage_builder

**Message:** Unused function: 'memory_delta' in 'mercury_ai.core._stage_builder'

**Evidence:** Function 'memory_delta' at line 32 in 'mercury_ai.core._stage_builder' is never called

**line:** 32

#### WARNING: mercury_ai.core._stage_builder

**Message:** Unused function: 'percentage_of' in 'mercury_ai.core._stage_builder'

**Evidence:** Function 'percentage_of' at line 36 in 'mercury_ai.core._stage_builder' is never called

**line:** 36

#### WARNING: mercury_ai.data.data_normalizer

**Message:** Unused function: 'normalize' in 'mercury_ai.data.data_normalizer'

**Evidence:** Function 'normalize' at line 12 in 'mercury_ai.data.data_normalizer' is never called

**line:** 12

#### WARNING: mercury_ai.data.data_quality_engine

**Message:** Unused function: 'validate' in 'mercury_ai.data.data_quality_engine'

**Evidence:** Function 'validate' at line 10 in 'mercury_ai.data.data_quality_engine' is never called

**line:** 10

#### WARNING: mercury_ai.data.indicator_engine

**Message:** Unused function: 'calculate' in 'mercury_ai.data.indicator_engine'

**Evidence:** Function 'calculate' at line 13 in 'mercury_ai.data.indicator_engine' is never called

**line:** 13

#### WARNING: mercury_ai.data.market_data

**Message:** Unused function: '_normalize_dataframe' in 'mercury_ai.data.market_data'

**Evidence:** Function '_normalize_dataframe' at line 33 in 'mercury_ai.data.market_data' is never called

**line:** 33

#### WARNING: mercury_ai.data.market_data

**Message:** Unused function: 'get_data' in 'mercury_ai.data.market_data'

**Evidence:** Function 'get_data' at line 111 in 'mercury_ai.data.market_data' is never called

**line:** 111

#### WARNING: mercury_ai.data.market_data_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.data.market_data_provider'

**Evidence:** Function 'get_data' at line 5 in 'mercury_ai.data.market_data_provider' is never called

**line:** 5

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'connect' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'connect' at line 48 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 48

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'health' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'health' at line 49 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 49

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_history' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_history' at line 50 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 50

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_last_price' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_last_price' at line 51 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 51

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_candles' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_candles' at line 52 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 52

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'market_status' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'market_status' at line 53 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 53

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'connect' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'connect' at line 60 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 60

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'health' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'health' at line 61 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 61

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_history' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_history' at line 62 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 62

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_last_price' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_last_price' at line 63 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 63

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_candles' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_candles' at line 64 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 64

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'market_status' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'market_status' at line 65 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 65

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'register_provider' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'register_provider' at line 85 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 85

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: '_get_best_provider' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function '_get_best_provider' at line 88 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 88

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'connect' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'connect' at line 94 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 94

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'health' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'health' at line 97 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 97

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_candles' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_candles' at line 101 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 101

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'trigger_failover' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'trigger_failover' at line 116 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 116

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_history' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_history' at line 120 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 120

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'list_providers' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'list_providers' at line 126 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 126

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'provider_status' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'provider_status' at line 129 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 129

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'best_provider' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'best_provider' at line 133 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 133

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'healthcheck' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'healthcheck' at line 150 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 150

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_last_price' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_last_price' at line 152 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 152

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'get_symbols' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'get_symbols' at line 153 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 153

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'market_status' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'market_status' at line 158 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 158

#### WARNING: mercury_ai.data.mercury_data_provider

**Message:** Unused function: 'healthcheck' in 'mercury_ai.data.mercury_data_provider'

**Evidence:** Function 'healthcheck' at line 159 in 'mercury_ai.data.mercury_data_provider' is never called

**line:** 159

#### WARNING: mercury_ai.data.replay_data_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.data.replay_data_provider'

**Evidence:** Function 'get_data' at line 8 in 'mercury_ai.data.replay_data_provider' is never called

**line:** 8

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'set_index' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'set_index' at line 12 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 12

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'get_data' at line 15 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 15

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'is_available' at line 19 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 19

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'supports_symbol' at line 22 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 22

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'supports_market' at line 25 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 25

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'supports_timeframe' at line 28 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 28

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'max_history' at line 31 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 31

#### WARNING: mercury_ai.data.providers.historical_data_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.data.providers.historical_data_provider'

**Evidence:** Function 'source_name' at line 34 in 'mercury_ai.data.providers.historical_data_provider' is never called

**line:** 34

#### WARNING: mercury_ai.database.history_logger

**Message:** Unused function: 'save' in 'mercury_ai.database.history_logger'

**Evidence:** Function 'save' at line 29 in 'mercury_ai.database.history_logger' is never called

**line:** 29

#### WARNING: mercury_ai.database.replay_storage

**Message:** Unused function: 'save' in 'mercury_ai.database.replay_storage'

**Evidence:** Function 'save' at line 18 in 'mercury_ai.database.replay_storage' is never called

**line:** 18

#### WARNING: mercury_ai.database.snapshot_logger

**Message:** Unused function: 'save' in 'mercury_ai.database.snapshot_logger'

**Evidence:** Function 'save' at line 13 in 'mercury_ai.database.snapshot_logger' is never called

**line:** 13

#### WARNING: mercury_ai.database.snapshot_logger

**Message:** Unused function: 'list_snapshots' in 'mercury_ai.database.snapshot_logger'

**Evidence:** Function 'list_snapshots' at line 21 in 'mercury_ai.database.snapshot_logger' is never called

**line:** 21

#### WARNING: mercury_ai.database.snapshot_logger

**Message:** Unused function: 'load_snapshot' in 'mercury_ai.database.snapshot_logger'

**Evidence:** Function 'load_snapshot' at line 25 in 'mercury_ai.database.snapshot_logger' is never called

**line:** 25

#### WARNING: mercury_ai.indicators.rsi

**Message:** Unused function: 'calculate' in 'mercury_ai.indicators.rsi'

**Evidence:** Function 'calculate' at line 6 in 'mercury_ai.indicators.rsi' is never called

**line:** 6

#### WARNING: mercury_ai.market.market_engine

**Message:** Unused function: 'show_market' in 'mercury_ai.market.market_engine'

**Evidence:** Function 'show_market' at line 11 in 'mercury_ai.market.market_engine' is never called

**line:** 11

#### WARNING: mercury_ai.news.news_provider

**Message:** Unused function: 'get_news' in 'mercury_ai.news.news_provider'

**Evidence:** Function 'get_news' at line 6 in 'mercury_ai.news.news_provider' is never called

**line:** 6

#### WARNING: mercury_ai.operations.demo_manager

**Message:** Unused function: 'run_simulation' in 'mercury_ai.operations.demo_manager'

**Evidence:** Function 'run_simulation' at line 21 in 'mercury_ai.operations.demo_manager' is never called

**line:** 21

#### WARNING: mercury_ai.presentation.signal_formatter

**Message:** Unused function: 'format' in 'mercury_ai.presentation.signal_formatter'

**Evidence:** Function 'format' at line 4 in 'mercury_ai.presentation.signal_formatter' is never called

**line:** 4

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'get_data' at line 5 in 'mercury_ai.providers.base_provider' is never called

**line:** 5

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'is_available' at line 8 in 'mercury_ai.providers.base_provider' is never called

**line:** 8

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'supports_symbol' at line 11 in 'mercury_ai.providers.base_provider' is never called

**line:** 11

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'supports_market' at line 14 in 'mercury_ai.providers.base_provider' is never called

**line:** 14

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'supports_timeframe' at line 17 in 'mercury_ai.providers.base_provider' is never called

**line:** 17

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'max_history' at line 20 in 'mercury_ai.providers.base_provider' is never called

**line:** 20

#### WARNING: mercury_ai.providers.base_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.providers.base_provider'

**Evidence:** Function 'source_name' at line 23 in 'mercury_ai.providers.base_provider' is never called

**line:** 23

#### WARNING: mercury_ai.providers.data_adapters

**Message:** Unused function: 'check_health' in 'mercury_ai.providers.data_adapters'

**Evidence:** Function 'check_health' at line 29 in 'mercury_ai.providers.data_adapters' is never called

**line:** 29

#### WARNING: mercury_ai.providers.data_adapters

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.data_adapters'

**Evidence:** Function 'get_data' at line 35 in 'mercury_ai.providers.data_adapters' is never called

**line:** 35

#### WARNING: mercury_ai.providers.data_adapters

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.data_adapters'

**Evidence:** Function 'get_data' at line 69 in 'mercury_ai.providers.data_adapters' is never called

**line:** 69

#### WARNING: mercury_ai.providers.data_interfaces

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.data_interfaces'

**Evidence:** Function 'get_data' at line 12 in 'mercury_ai.providers.data_interfaces' is never called

**line:** 12

#### WARNING: mercury_ai.providers.data_interfaces

**Message:** Unused function: 'check_health' in 'mercury_ai.providers.data_interfaces'

**Evidence:** Function 'check_health' at line 14 in 'mercury_ai.providers.data_interfaces' is never called

**line:** 14

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'get_data' at line 2 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 2

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'is_available' at line 5 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 5

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'supports_symbol' at line 8 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 8

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'supports_market' at line 11 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 11

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'supports_timeframe' at line 14 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 14

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'max_history' at line 17 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 17

#### WARNING: mercury_ai.providers.future_broker_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.providers.future_broker_provider'

**Evidence:** Function 'source_name' at line 20 in 'mercury_ai.providers.future_broker_provider' is never called

**line:** 20

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'get_data' at line 2 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 2

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'is_available' at line 5 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 5

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'supports_symbol' at line 8 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 8

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'supports_market' at line 11 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 11

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'supports_timeframe' at line 14 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 14

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'max_history' at line 17 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 17

#### WARNING: mercury_ai.providers.future_polygon_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.providers.future_polygon_provider'

**Evidence:** Function 'source_name' at line 20 in 'mercury_ai.providers.future_polygon_provider' is never called

**line:** 20

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'get_data' at line 2 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 2

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'is_available' at line 5 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 5

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'supports_symbol' at line 8 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 8

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'supports_market' at line 11 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 11

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'supports_timeframe' at line 14 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 14

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'max_history' at line 17 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 17

#### WARNING: mercury_ai.providers.future_tradingview_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.providers.future_tradingview_provider'

**Evidence:** Function 'source_name' at line 20 in 'mercury_ai.providers.future_tradingview_provider' is never called

**line:** 20

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'set_data' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'set_data' at line 11 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 11

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'set_index' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'set_index' at line 15 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 15

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'get_data' at line 19 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 19

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'is_available' at line 33 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 33

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'supports_symbol' at line 36 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 36

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'supports_market' at line 39 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 39

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'supports_timeframe' at line 42 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 42

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'max_history' at line 45 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 45

#### WARNING: mercury_ai.providers.historical_replay_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.providers.historical_replay_provider'

**Evidence:** Function 'source_name' at line 48 in 'mercury_ai.providers.historical_replay_provider' is never called

**line:** 48

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'register_provider' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'register_provider' at line 36 in 'mercury_ai.providers.market_provider' is never called

**line:** 36

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: '_healthy_providers' in 'mercury_ai.providers.market_provider'

**Evidence:** Function '_healthy_providers' at line 42 in 'mercury_ai.providers.market_provider' is never called

**line:** 42

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: '_get_best_provider' in 'mercury_ai.providers.market_provider'

**Evidence:** Function '_get_best_provider' at line 52 in 'mercury_ai.providers.market_provider' is never called

**line:** 52

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'healthcheck' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'healthcheck' at line 80 in 'mercury_ai.providers.market_provider' is never called

**line:** 80

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'list_providers' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'list_providers' at line 87 in 'mercury_ai.providers.market_provider' is never called

**line:** 87

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'best_provider' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'best_provider' at line 93 in 'mercury_ai.providers.market_provider' is never called

**line:** 93

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'is_available' at line 98 in 'mercury_ai.providers.market_provider' is never called

**line:** 98

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'get_data' at line 110 in 'mercury_ai.providers.market_provider' is never called

**line:** 110

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'connect' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'connect' at line 138 in 'mercury_ai.providers.market_provider' is never called

**line:** 138

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'health' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'health' at line 144 in 'mercury_ai.providers.market_provider' is never called

**line:** 144

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'get_candles' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'get_candles' at line 158 in 'mercury_ai.providers.market_provider' is never called

**line:** 158

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'get_history' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'get_history' at line 214 in 'mercury_ai.providers.market_provider' is never called

**line:** 214

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'get_last_price' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'get_last_price' at line 228 in 'mercury_ai.providers.market_provider' is never called

**line:** 228

#### WARNING: mercury_ai.providers.market_provider

**Message:** Unused function: 'market_status' in 'mercury_ai.providers.market_provider'

**Evidence:** Function 'market_status' at line 244 in 'mercury_ai.providers.market_provider' is never called

**line:** 244

#### WARNING: mercury_ai.providers.provider

**Message:** Unused function: 'get_market_status' in 'mercury_ai.providers.provider'

**Evidence:** Function 'get_market_status' at line 3 in 'mercury_ai.providers.provider' is never called

**line:** 3

#### WARNING: mercury_ai.providers.provider

**Message:** Unused function: 'get_name' in 'mercury_ai.providers.provider'

**Evidence:** Function 'get_name' at line 6 in 'mercury_ai.providers.provider' is never called

**line:** 6

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'get_data' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'get_data' at line 6 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 6

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'is_available' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'is_available' at line 19 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 19

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'supports_symbol' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'supports_symbol' at line 22 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 22

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'supports_market' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'supports_market' at line 25 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 25

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'supports_timeframe' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'supports_timeframe' at line 28 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 28

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'max_history' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'max_history' at line 31 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 31

#### WARNING: mercury_ai.providers.yahoo_finance_provider

**Message:** Unused function: 'source_name' in 'mercury_ai.providers.yahoo_finance_provider'

**Evidence:** Function 'source_name' at line 34 in 'mercury_ai.providers.yahoo_finance_provider' is never called

**line:** 34

#### WARNING: mercury_ai.sessions.market_sessions

**Message:** Unused function: 'get_current_session' in 'mercury_ai.sessions.market_sessions'

**Evidence:** Function 'get_current_session' at line 7 in 'mercury_ai.sessions.market_sessions' is never called

**line:** 7

#### WARNING: mercury_ai.sessions.market_sessions

**Message:** Unused function: 'is_high_liquidity' in 'mercury_ai.sessions.market_sessions'

**Evidence:** Function 'is_high_liquidity' at line 25 in 'mercury_ai.sessions.market_sessions' is never called

**line:** 25

#### WARNING: mercury_ai.utils.deterministic_clock

**Message:** Unused function: 'set_time' in 'mercury_ai.utils.deterministic_clock'

**Evidence:** Function 'set_time' at line 7 in 'mercury_ai.utils.deterministic_clock' is never called

**line:** 7

#### WARNING: mercury_ai.utils.deterministic_clock

**Message:** Unused function: 'utcnow' in 'mercury_ai.utils.deterministic_clock'

**Evidence:** Function 'utcnow' at line 11 in 'mercury_ai.utils.deterministic_clock' is never called

**line:** 11

#### WARNING: mercury_ai.utils.memory_auditor

**Message:** Unused function: '_take_snapshot' in 'mercury_ai.utils.memory_auditor'

**Evidence:** Function '_take_snapshot' at line 12 in 'mercury_ai.utils.memory_auditor' is never called

**line:** 12

#### WARNING: mercury_ai.utils.memory_auditor

**Message:** Unused function: '_compare' in 'mercury_ai.utils.memory_auditor'

**Evidence:** Function '_compare' at line 28 in 'mercury_ai.utils.memory_auditor' is never called

**line:** 28

#### WARNING: mercury_ai.utils.performance_collector

**Message:** Unused function: 'collect' in 'mercury_ai.utils.performance_collector'

**Evidence:** Function 'collect' at line 46 in 'mercury_ai.utils.performance_collector' is never called

**line:** 46

#### WARNING: mercury_ai.utils.performance_collector

**Message:** Unused function: '_flatten_stages' in 'mercury_ai.utils.performance_collector'

**Evidence:** Function '_flatten_stages' at line 61 in 'mercury_ai.utils.performance_collector' is never called

**line:** 61

#### WARNING: mercury_ai.utils.regression_detector

**Message:** Unused function: '_load_history' in 'mercury_ai.utils.regression_detector'

**Evidence:** Function '_load_history' at line 11 in 'mercury_ai.utils.regression_detector' is never called

**line:** 11

#### WARNING: mercury_ai.utils.regression_detector

**Message:** Unused function: 'save_history' in 'mercury_ai.utils.regression_detector'

**Evidence:** Function 'save_history' at line 19 in 'mercury_ai.utils.regression_detector' is never called

**line:** 19

#### WARNING: mercury_ai.utils.regression_detector

**Message:** Unused function: 'detect' in 'mercury_ai.utils.regression_detector'

**Evidence:** Function 'detect' at line 23 in 'mercury_ai.utils.regression_detector' is never called

**line:** 23

#### WARNING: mercury_ai.utils.report_generator

**Message:** Unused function: 'generate_json' in 'mercury_ai.utils.report_generator'

**Evidence:** Function 'generate_json' at line 19 in 'mercury_ai.utils.report_generator' is never called

**line:** 19

#### WARNING: mercury_ai.utils.report_generator

**Message:** Unused function: 'generate_csv' in 'mercury_ai.utils.report_generator'

**Evidence:** Function 'generate_csv' at line 23 in 'mercury_ai.utils.report_generator' is never called

**line:** 23

#### WARNING: mercury_ai.utils.report_generator

**Message:** Unused function: 'generate_markdown' in 'mercury_ai.utils.report_generator'

**Evidence:** Function 'generate_markdown' at line 29 in 'mercury_ai.utils.report_generator' is never called

**line:** 29

#### WARNING: mercury_ai.utils.report_generator

**Message:** Unused function: 'generate_html' in 'mercury_ai.utils.report_generator'

**Evidence:** Function 'generate_html' at line 41 in 'mercury_ai.utils.report_generator' is never called

**line:** 41

#### WARNING: mercury_ai.utils.stress_tester

**Message:** Unused function: 'register_generator' in 'mercury_ai.utils.stress_tester'

**Evidence:** Function 'register_generator' at line 11 in 'mercury_ai.utils.stress_tester' is never called

**line:** 11

#### WARNING: mercury_ai.utils.system_monitor

**Message:** Unused function: 'get_metrics' in 'mercury_ai.utils.system_monitor'

**Evidence:** Function 'get_metrics' at line 5 in 'mercury_ai.utils.system_monitor' is never called

**line:** 5

#### WARNING: tests.test_adaptive_weighting

**Message:** Unused function: 'base_context' in 'tests.test_adaptive_weighting'

**Evidence:** Function 'base_context' at line 10 in 'tests.test_adaptive_weighting' is never called

**line:** 10

#### WARNING: tests.test_confidence_calibration

**Message:** Unused function: 'base_context' in 'tests.test_confidence_calibration'

**Evidence:** Function 'base_context' at line 12 in 'tests.test_confidence_calibration' is never called

**line:** 12

#### WARNING: tests.test_institutional_backtest

**Message:** Unused function: 'build_data_symbol_data' in 'tests.test_institutional_backtest'

**Evidence:** Function 'build_data_symbol_data' at line 462 in 'tests.test_institutional_backtest' is never called

**line:** 462

#### WARNING: tests.test_performance_engine

**Message:** Unused function: 'setUp' in 'tests.test_performance_engine'

**Evidence:** Function 'setUp' at line 7 in 'tests.test_performance_engine' is never called

**line:** 7

#### WARNING: tests.test_robustness

**Message:** Unused function: 'get_data' in 'tests.test_robustness'

**Evidence:** Function 'get_data' at line 13 in 'tests.test_robustness' is never called

**line:** 13

#### WARNING: tests.test_robustness

**Message:** Unused function: 'is_available' in 'tests.test_robustness'

**Evidence:** Function 'is_available' at line 16 in 'tests.test_robustness' is never called

**line:** 16

#### WARNING: tests.test_robustness

**Message:** Unused function: 'supports_symbol' in 'tests.test_robustness'

**Evidence:** Function 'supports_symbol' at line 19 in 'tests.test_robustness' is never called

**line:** 19

#### WARNING: tests.test_robustness

**Message:** Unused function: 'source_name' in 'tests.test_robustness'

**Evidence:** Function 'source_name' at line 22 in 'tests.test_robustness' is never called

**line:** 22

#### WARNING: tests.test_validation_engine

**Message:** Unused function: 'validation_engine' in 'tests.test_validation_engine'

**Evidence:** Function 'validation_engine' at line 9 in 'tests.test_validation_engine' is never called

**line:** 9

#### WARNING: tools.scanner

**Message:** Unused function: 'scan' in 'tools.scanner'

**Evidence:** Function 'scan' at line 18 in 'tools.scanner' is never called

**line:** 18

#### WARNING: tools.writer

**Message:** Unused function: 'save' in 'tools.writer'

**Evidence:** Function 'save' at line 13 in 'tools.writer' is never called

**line:** 13

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'pass_count' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'pass_count' at line 34 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 34

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'fail_count' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'fail_count' at line 38 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 38

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'warning_count' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'warning_count' at line 42 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 42

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'info_count' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'info_count' at line 46 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 46

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'inconclusive_count' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'inconclusive_count' at line 50 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 50

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'total_findings' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'total_findings' at line 64 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 64

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'total_pass' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'total_pass' at line 68 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 68

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'total_fail' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'total_fail' at line 72 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 72

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'total_warning' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'total_warning' at line 76 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 76

#### WARNING: tools.mercury_integrity_auditor.models

**Message:** Unused function: 'total_critical' in 'tools.mercury_integrity_auditor.models'

**Evidence:** Function 'total_critical' at line 80 in 'tools.mercury_integrity_auditor.models' is never called

**line:** 80

#### WARNING: tools.mercury_integrity_auditor.auditors.contract_auditor

**Message:** Unused function: 'visit_ClassDef' in 'tools.mercury_integrity_auditor.auditors.contract_auditor'

**Evidence:** Function 'visit_ClassDef' at line 80 in 'tools.mercury_integrity_auditor.auditors.contract_auditor' is never called

**line:** 80

#### WARNING: tools.mercury_integrity_auditor.auditors.decision_auditor

**Message:** Unused function: 'visit_If' in 'tools.mercury_integrity_auditor.auditors.decision_auditor'

**Evidence:** Function 'visit_If' at line 40 in 'tools.mercury_integrity_auditor.auditors.decision_auditor' is never called

**line:** 40

#### WARNING: tools.mercury_integrity_auditor.auditors.decision_auditor

**Message:** Unused function: 'visit_Call' in 'tools.mercury_integrity_auditor.auditors.decision_auditor'

**Evidence:** Function 'visit_Call' at line 47 in 'tools.mercury_integrity_auditor.auditors.decision_auditor' is never called

**line:** 47

#### WARNING: tools.mercury_integrity_auditor.auditors.flow_auditor

**Message:** Unused function: 'visit_ClassDef' in 'tools.mercury_integrity_auditor.auditors.flow_auditor'

**Evidence:** Function 'visit_ClassDef' at line 91 in 'tools.mercury_integrity_auditor.auditors.flow_auditor' is never called

**line:** 91

#### WARNING: tools.mercury_integrity_auditor.auditors.flow_auditor

**Message:** Unused function: 'visit_FunctionDef' in 'tools.mercury_integrity_auditor.auditors.flow_auditor'

**Evidence:** Function 'visit_FunctionDef' at line 102 in 'tools.mercury_integrity_auditor.auditors.flow_auditor' is never called

**line:** 102

#### WARNING: tools.mercury_integrity_auditor.auditors.masking_auditor

**Message:** Unused function: 'visit_Import' in 'tools.mercury_integrity_auditor.auditors.masking_auditor'

**Evidence:** Function 'visit_Import' at line 48 in 'tools.mercury_integrity_auditor.auditors.masking_auditor' is never called

**line:** 48

#### WARNING: tools.mercury_integrity_auditor.auditors.masking_auditor

**Message:** Unused function: 'visit_ImportFrom' in 'tools.mercury_integrity_auditor.auditors.masking_auditor'

**Evidence:** Function 'visit_ImportFrom' at line 54 in 'tools.mercury_integrity_auditor.auditors.masking_auditor' is never called

**line:** 54

#### WARNING: tools.mercury_integrity_auditor.auditors.masking_auditor

**Message:** Unused function: 'visit_Call' in 'tools.mercury_integrity_auditor.auditors.masking_auditor'

**Evidence:** Function 'visit_Call' at line 60 in 'tools.mercury_integrity_auditor.auditors.masking_auditor' is never called

**line:** 60

#### WARNING: tools.mercury_integrity_auditor.auditors.masking_auditor

**Message:** Unused function: 'visit_ExceptHandler' in 'tools.mercury_integrity_auditor.auditors.masking_auditor'

**Evidence:** Function 'visit_ExceptHandler' at line 65 in 'tools.mercury_integrity_auditor.auditors.masking_auditor' is never called

**line:** 65

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: 'visit_ClassDef' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function 'visit_ClassDef' at line 72 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 72

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: 'visit_FunctionDef' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function 'visit_FunctionDef' at line 79 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 79

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: 'visit_AsyncFunctionDef' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function 'visit_AsyncFunctionDef' at line 90 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 90

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: 'visit_ExceptHandler' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function 'visit_ExceptHandler' at line 99 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 99

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: 'visit_Import' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function 'visit_Import' at line 104 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 104

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: 'visit_ImportFrom' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function 'visit_ImportFrom' at line 109 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 109

#### WARNING: tools.mercury_integrity_auditor.auditors.static_auditor

**Message:** Unused function: '_is_stub' in 'tools.mercury_integrity_auditor.auditors.static_auditor'

**Evidence:** Function '_is_stub' at line 114 in 'tools.mercury_integrity_auditor.auditors.static_auditor' is never called

**line:** 114

#### WARNING: tools.project_mapper.ast_parser

**Message:** Unused function: 'parse' in 'tools.project_mapper.ast_parser'

**Evidence:** Function 'parse' at line 7 in 'tools.project_mapper.ast_parser' is never called

**line:** 7

#### WARNING: tools.project_mapper.scanner

**Message:** Unused function: 'scan' in 'tools.project_mapper.scanner'

**Evidence:** Function 'scan' at line 20 in 'tools.project_mapper.scanner' is never called

**line:** 20

#### WARNING: tools.project_mapper.snapshot_builder

**Message:** Unused function: '_load_json' in 'tools.project_mapper.snapshot_builder'

**Evidence:** Function '_load_json' at line 21 in 'tools.project_mapper.snapshot_builder' is never called

**line:** 21

#### WARNING: tools.project_mapper.snapshot_builder

**Message:** Unused function: '_load_text' in 'tools.project_mapper.snapshot_builder'

**Evidence:** Function '_load_text' at line 30 in 'tools.project_mapper.snapshot_builder' is never called

**line:** 30

#### WARNING: tools.project_mapper.snapshot_builder

**Message:** Unused function: 'build' in 'tools.project_mapper.snapshot_builder'

**Evidence:** Function 'build' at line 38 in 'tools.project_mapper.snapshot_builder' is never called

**line:** 38

#### WARNING: tools.project_mapper.writer

**Message:** Unused function: 'save' in 'tools.project_mapper.writer'

**Evidence:** Function 'save' at line 13 in 'tools.project_mapper.writer' is never called

**line:** 13
