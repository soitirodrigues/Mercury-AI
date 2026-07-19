================================================================================
app.dashboard.asset_registry_panel
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- render_asset_registry_dashboard

Imports
-------
- mercury_ai.core.asset_registry.AssetRegistry
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- pandas
- streamlit


================================================================================
app.dashboard.dashboard
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- load_data

Imports
-------
- app.ui_utils.apply_design_system
- app.ui_utils.display_metric
- mercury_ai.analysis.data_exporter.DataExporter
- mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor
- mercury_ai.analysis.health_checker.HealthChecker
- mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator
- mercury_ai.analysis.notification_center.NotificationCenter
- mercury_ai.analysis.operational_history.OperationalHistory
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- mercury_ai.brain.scanner.Scanner
- mercury_ai.config.configuration_center.MercuryConfigCenter
- mercury_ai.config.settings
- pandas
- pathlib.Path
- streamlit
- sys
- time


================================================================================
app.dashboard.health_center_panel
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- render_health_center_panel

Imports
-------
- mercury_ai.core.health_center.HealthCenter
- streamlit


================================================================================
app.dashboard.main_dashboard
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- app.dashboard.asset_registry_panel.render_asset_registry_dashboard
- app.dashboard.health_center_panel.render_health_center_panel
- app.dashboard.market_map_panel.render_market_map_panel
- app.dashboard.observability_panel.render_observability_dashboard
- app.dashboard.provider_health_panel.render_provider_health_dashboard
- mercury_ai.core.asset_registry.AssetRegistry
- mercury_ai.core.health_center.HealthCenter
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- streamlit


================================================================================
app.dashboard.market_map_panel
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- render_market_map_panel

Imports
-------
- mercury_ai.core.asset_registry.AssetRegistry
- pandas
- plotly.express
- streamlit


================================================================================
app.dashboard.observability_panel
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- render_observability_dashboard

Imports
-------
- mercury_ai.providers.manager.MercuryProviderManager
- psutil
- streamlit
- time


================================================================================
app.dashboard.operation_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.analysis.health_checker.HealthChecker
- mercury_ai.analysis.integrity_checker.IntegrityChecker
- mercury_ai.analysis.operational_history.OperationalHistory
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- mercury_ai.brain.scanner.Scanner
- mercury_ai.config.settings
- pandas
- pathlib.Path
- streamlit
- sys


================================================================================
app.dashboard.provider_health_panel
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- render_provider_health_dashboard

Imports
-------
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- streamlit


================================================================================
app.launcher
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.analysis.health_checker.HealthChecker
- os
- streamlit
- sys


================================================================================
app.terminal.pages.01_Scanner
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- load_data

Imports
-------
- mercury_ai.brain.scanner.MercuryScanner
- mercury_ai.config.settings
- pandas
- pathlib.Path
- streamlit
- sys
- time


================================================================================
app.terminal.pages.02_Dashboard
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.brain.scanner.Scanner
- pandas
- pathlib.Path
- streamlit
- sys


================================================================================
app.terminal.pages.03_Historico_Estatisticas
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.analysis.operational_history.OperationalHistory
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- pandas
- pathlib.Path
- streamlit
- sys


================================================================================
app.terminal.pages.04_Auditoria_Configuracoes
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.analysis.health_checker.HealthChecker
- mercury_ai.analysis.integrity_checker.IntegrityChecker
- mercury_ai.config.settings
- pathlib.Path
- streamlit
- sys


================================================================================
app.terminal.pages.05_Replay
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- pandas
- pathlib.Path
- streamlit
- sys


================================================================================
app.terminal.pages.06_Demo
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.analysis.operational_history.OperationalHistory
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- mercury_ai.config.assets.SUPPORTED_ASSETS
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- pandas
- pathlib.Path
- streamlit
- sys


================================================================================
app.terminal.pages.07_Observabilidade
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.analysis.health_checker.HealthChecker
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- mercury_ai.utils.system_monitor.SystemMonitor
- pandas
- streamlit
- time


================================================================================
app.terminal.terminal
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- app.ui_utils.apply_design_system
- app.ui_utils.display_card
- app.ui_utils.display_status
- mercury_ai.analysis.health_checker.HealthChecker
- mercury_ai.config.settings
- streamlit


================================================================================
app.ui_utils
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- apply_design_system
- display_card
- display_metric
- display_status

Imports
-------
- streamlit


================================================================================
calculate_institutional_stats
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- calculate_statistics

Imports
-------
- json
- os
- pandas


================================================================================
main
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- mercury_ai.brain.scanner.MercuryScanner


================================================================================
mercury_ai.ai.llm
================================================================================

Classes
--------
- MercuryLLM

Funções
--------
- __init__
- ask

Imports
-------
- openai.OpenAI
- os


================================================================================
mercury_ai.analysis.adaptive_weight_engine
================================================================================

Classes
--------
- AdaptiveWeightEngine

Funções
--------
- calculate_weights

Imports
-------
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- typing.Dict


================================================================================
mercury_ai.analysis.benchmark_framework
================================================================================

Classes
--------
- MercuryBenchmarkFramework

Funções
--------
- __init__
- run_benchmark

Imports
-------
- mercury_ai.analysis.metric_calculator.MetricCalculator
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.models.benchmark_report.BenchmarkReport
- mercury_ai.models.benchmark_report.BenchmarkRunResult
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- mercury_ai.utils.deterministic_clock.DeterministicClock
- os
- psutil
- time
- tracemalloc
- typing.List


================================================================================
mercury_ai.analysis.calibration_analyzer
================================================================================

Classes
--------
- CalibrationAnalyzer

Funções
--------
- __init__
- analyze_calibration

Imports
-------
- json
- os
- typing.Dict


================================================================================
mercury_ai.analysis.candlestick_engine
================================================================================

Classes
--------
- CandlestickEngine

Funções
--------
- _detect_context
- _detect_continuation
- _detect_engulfing
- _detect_pattern
- _detect_rejection
- analyze

Imports
-------
- mercury_ai.analysis.evidence_query.EvidenceQuery
- mercury_ai.core.base_engine.BaseEngine
- mercury_ai.core.base_engine.EngineResult
- mercury_ai.models.candlestick_analysis.CandlestickAnalysis
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_condition.MarketCondition
- mercury_ai.models.market_data.MarketData
- pandas
- time
- typing.List
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.analysis.confidence_calibration_auditor
================================================================================

Classes
--------
- ConfidenceCalibrationAuditor

Funções
--------
- __init__
- audit

Imports
-------
- mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- numpy
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.confidence_engine
================================================================================

Classes
--------
- ConfidenceEngine

Funções
--------
- _get_grade
- calculate

Imports
-------
- mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
- mercury_ai.analysis.evidence_query.EvidenceQuery
- mercury_ai.models.confidence_result.ConfidenceResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_state_enum.MarketStateEnum


================================================================================
mercury_ai.analysis.conflict_resolution_engine
================================================================================

Classes
--------
- ConflictResolutionEngine

Funções
--------
- __init__
- resolve

Imports
-------
- dataclasses.replace
- mercury_ai.analysis.adaptive_weight_engine.AdaptiveWeightEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.confluence_engine
================================================================================

Classes
--------
- ConfluenceEngine

Funções
--------
- __init__
- analyze

Imports
-------
- mercury_ai.analysis.decision_trace_engine.DecisionTraceEngine
- mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder
- mercury_ai.models.analysis_result.AnalysisDirection
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle


================================================================================
mercury_ai.analysis.confluence_score_engine
================================================================================

Classes
--------
- ConfluenceScoreEngine

Funções
--------
- calculate

Imports
-------
- mercury_ai.analysis.evidence_query.EvidenceQuery
- mercury_ai.models.confluence_score.ConfluenceScore
- mercury_ai.models.market_context.MarketContext


================================================================================
mercury_ai.analysis.context_engine
================================================================================

Classes
--------
- ContextEngine

Funções
--------
- __init__
- _calculate_quality
- _deduplicate_evidences
- _detect_conflicts
- _merge_evidences
- _refine_context
- analyze

Imports
-------
- dataclasses.replace
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- typing.List


================================================================================
mercury_ai.analysis.context_intelligence_engine
================================================================================

Classes
--------
- ContextIntelligenceEngine

Funções
--------
- evaluate

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- typing.List


================================================================================
mercury_ai.analysis.data_exporter
================================================================================

Classes
--------
- DataExporter

Funções
--------
- __init__
- _export_to_formats
- export_all
- export_history
- export_snapshots

Imports
-------
- json
- mercury_ai.analysis.operational_history.OperationalHistory
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- pandas
- pathlib.Path
- typing.Any
- typing.Dict
- typing.List
- zipfile


================================================================================
mercury_ai.analysis.data_quality_engine
================================================================================

Classes
--------
- DataQualityEngine
- QualityReport

Funções
--------
- calculate_score
- generate_report

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- datetime.datetime
- numpy
- pandas
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.decision_trace_engine
================================================================================

Classes
--------
- DecisionTraceEngine

Funções
--------
- __init__
- finalize
- log_step

Imports
-------
- dataclasses.replace
- mercury_ai.models.decision_trace.DecisionNode
- mercury_ai.models.decision_trace.DecisionTrace


================================================================================
mercury_ai.analysis.engine_performance_auditor
================================================================================

Classes
--------
- EnginePerformanceAuditor

Funções
--------
- __init__
- audit_engines

Imports
-------
- collections.defaultdict
- mercury_ai.analysis.performance_analytics.PerformanceAnalytics
- mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.evidence_engine
================================================================================

Classes
--------
- EvidenceEngine

Funções
--------
- __init__
- _deduplicate
- _normalize
- calculate_agreement
- compose
- process

Imports
-------
- dataclasses.replace
- mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.List
- typing.Optional


================================================================================
mercury_ai.analysis.evidence_quality_engine
================================================================================

Classes
--------
- EvidenceQualityEngine

Funções
--------
- evaluate

Imports
-------
- dataclasses.replace
- mercury_ai.models.evidence.Evidence
- typing.List


================================================================================
mercury_ai.analysis.evidence_query
================================================================================

Classes
--------
- EvidenceQuery

Funções
--------
- get_trend_direction
- has_strong_trend
- is_downtrend
- is_uptrend

Imports
-------
- mercury_ai.models.evidence.Evidence
- typing.List


================================================================================
mercury_ai.analysis.evidence_ranking_engine
================================================================================

Classes
--------
- EvidenceRankingEngine

Funções
--------
- calculate_contribution_score
- rank

Imports
-------
- dataclasses.replace
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- typing.List


================================================================================
mercury_ai.analysis.fair_value_gap_engine
================================================================================

Classes
--------
- FairValueGapEngine

Funções
--------
- __init__
- _analyze_logic
- analyze

Imports
-------
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis
- pandas
- typing.Optional


================================================================================
mercury_ai.analysis.health_auditor
================================================================================

Classes
--------
- HealthAuditor

Funções
--------
- __init__
- generate_report

Imports
-------
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.analysis.narrative_engine.NarrativeEngine
- mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
- mercury_ai.brain.probability_engine.ProbabilityEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- os
- pathlib.Path


================================================================================
mercury_ai.analysis.health_checker
================================================================================

Classes
--------
- HealthChecker
- HealthStatus

Funções
--------
- __init__
- check

Imports
-------
- dataclasses.asdict
- dataclasses.dataclass
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.analysis.narrative_engine.NarrativeEngine
- mercury_ai.analysis.operational_history.OperationalHistory
- mercury_ai.analysis.statistical_auditor.StatisticalAuditor
- mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
- mercury_ai.brain.probability_engine.ProbabilityEngine
- mercury_ai.config.settings
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- mercury_ai.utils.deterministic_clock.DeterministicClock
- pathlib.Path
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.historical_replay_engine
================================================================================

Classes
--------
- HistoricalReplayEngine

Funções
--------
- run_replay

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.database.replay_storage.ReplayStorage
- mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider
- mercury_ai.utils.deterministic_clock.DeterministicClock
- pandas


================================================================================
mercury_ai.analysis.institutional_analytics_engine
================================================================================

Classes
--------
- InstitutionalAnalyticsEngine

Funções
--------
- __init__
- _get_engine_contribution
- _get_top_patterns
- _load_data
- generate_quality_report

Imports
-------
- json
- os
- pandas
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.institutional_context_builder
================================================================================

Classes
--------
- InstitutionalContext
- InstitutionalContextBuilder

Funções
--------
- _build_text
- _calculate_bias
- _calculate_confidence
- build

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.analysis.institutional_memory_engine
================================================================================

Classes
--------
- InstitutionalMemoryEngine

Funções
--------
- __init__
- _get_setup_key
- get_consistency_score
- record_decision
- record_outcome

Imports
-------
- hashlib
- json
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- os


================================================================================
mercury_ai.analysis.institutional_report
================================================================================

Classes
--------
- InstitutionalReport

Funções
--------
- __init__
- generate

Imports
-------
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- pytest
- subprocess


================================================================================
mercury_ai.analysis.institutional_report_generator
================================================================================

Classes
--------
- InstitutionalReportGenerator

Funções
--------
- __init__
- generate

Imports
-------
- mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor
- mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor
- mercury_ai.analysis.performance_analytics.PerformanceAnalytics
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.institutional_trade_filter_engine
================================================================================

Classes
--------
- InstitutionalTradeFilterEngine

Funções
--------
- evaluate

Imports
-------
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.integrity_checker
================================================================================

Classes
--------
- IntegrityChecker

Funções
--------
- __init__
- _check_snapshot
- check_all

Imports
-------
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- re
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.learning_engine
================================================================================

Classes
--------
- LearningEngine

Funções
--------
- __init__
- _accumulate
- _finalize_stats
- run_learning

Imports
-------
- collections.defaultdict
- json
- os
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.live_monitor
================================================================================

Classes
--------
- LiveMonitor

Funções
--------
- __init__
- run_cycle

Imports
-------
- mercury_ai.config.assets.SUPPORTED_ASSETS
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- time
- typing.List


================================================================================
mercury_ai.analysis.market_condition_engine
================================================================================

Classes
--------
- MarketConditionEngine

Funções
--------
- _analyze_adx
- _analyze_price_position
- _analyze_rsi
- _build_explanation
- _calculate_trend_strength
- _detect_market_state
- _detect_trend
- _measure_ema_alignment
- _measure_ema_distance
- _measure_ema_slope
- analyze

Imports
-------
- mercury_ai.models.market_condition.MarketCondition
- mercury_ai.models.market_data.MarketData
- typing.List


================================================================================
mercury_ai.analysis.market_context_builder
================================================================================

Classes
--------
- MarketContextBuilder

Funções
--------
- __init__
- build

Imports
-------
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state.MarketStateEnum
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.risk_assessment.RiskAssessment


================================================================================
mercury_ai.analysis.market_regime_engine
================================================================================

Classes
--------
- MarketRegimeEngine

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.market_regime_enum.MarketRegimeEnum


================================================================================
mercury_ai.analysis.market_state_engine
================================================================================

Classes
--------
- MarketStateEngine

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state_enum.MarketStateEnum
- mercury_ai.models.session_analysis.SessionAnalysis
- typing.Optional


================================================================================
mercury_ai.analysis.market_structure_intelligence_engine
================================================================================

Classes
--------
- MarketStructureIntelligenceEngine

Funções
--------
- __init__
- evaluate

Imports
-------
- mercury_ai.analysis.swing_engine.SwingEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- pandas
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.market_thesis_builder
================================================================================

Classes
--------
- MarketThesisBuilder

Funções
--------
- __init__
- build

Imports
-------
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine
- mercury_ai.analysis.market_state_engine.MarketStateEngine
- mercury_ai.analysis.risk_engine.RiskEngine
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_thesis.MarketThesis


================================================================================
mercury_ai.analysis.metric_calculator
================================================================================

Classes
--------
- MetricCalculator
- PerformanceMetrics

Funções
--------
- calculate

Imports
-------
- dataclasses.dataclass
- numpy
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.momentum_engine
================================================================================

Classes
--------
- MomentumEngine

Funções
--------
- __init__
- _analyze_logic
- analyze

Imports
-------
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.momentum_analysis.MomentumAnalysis
- pandas
- typing.Optional


================================================================================
mercury_ai.analysis.mtf_engine
================================================================================

Classes
--------
- MTFEngine

Funções
--------
- __init__
- _build_consensus
- analyze
- calculate_factor_alignment

Imports
-------
- mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.analysis.trend_analyzer.TrendAnalyzer
- mercury_ai.analysis.volatility_engine.VolatilityEngine
- mercury_ai.config.timeframes.YFINANCE_INTERVALS
- mercury_ai.data.indicator_engine.IndicatorEngine
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.providers.base_provider.MarketDataProvider
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.narrative_engine
================================================================================

Classes
--------
- NarrativeEngine

Funções
--------
- generate

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.trading_explanation.TradingExplanation
- typing.List


================================================================================
mercury_ai.analysis.notification_center
================================================================================

Classes
--------
- Notification
- NotificationCenter

Funções
--------
- __init__
- export_to_csv
- export_to_json
- get_history
- send

Imports
-------
- csv
- dataclasses.dataclass
- dataclasses.field
- json
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.List
- typing.Optional


================================================================================
mercury_ai.analysis.operational_history
================================================================================

Classes
--------
- OperationalHistory

Funções
--------
- __init__
- query

Imports
-------
- mercury_ai.analysis.performance_analytics.PerformanceAnalytics
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.performance_analytics
================================================================================

Classes
--------
- PerformanceAnalytics

Funções
--------
- __init__
- analyze_performance

Imports
-------
- datetime.datetime
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- pathlib.Path
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.performance_center
================================================================================

Classes
--------
- PerformanceCenter

Funções
--------
- __init__
- get_report

Imports
-------
- collections.Counter
- mercury_ai.analysis.performance_analytics.PerformanceAnalytics
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- pandas
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.performance_statistics
================================================================================

Classes
--------
- PerformanceStatistics

Funções
--------
- __init__
- calculate

Imports
-------
- mercury_ai.analysis.performance_analytics.PerformanceAnalytics
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.post_decision_evaluation_engine
================================================================================

Classes
--------
- PostDecisionEvaluationEngine

Funções
--------
- evaluate

Imports
-------
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- mercury_ai.models.performance_metrics.PerformanceMetrics
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.price_action_analyzer
================================================================================

Classes
--------
- PriceActionAnalyzer

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.price_action.PriceActionAnalysis


================================================================================
mercury_ai.analysis.price_action_engine
================================================================================

Classes
--------
- PriceActionEngine

Funções
--------
- __init__
- _analyze_logic
- analyze

Imports
-------
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.price_action_analysis.PriceActionAnalysis
- pandas
- typing.Optional


================================================================================
mercury_ai.analysis.provider_priority_engine
================================================================================

Classes
--------
- ProviderPriorityEngine

Funções
--------
- __init__
- get_optimal_provider

Imports
-------
- logging
- mercury_ai.data.mercury_data_provider.IMercuryDataProvider
- mercury_ai.data.mercury_data_provider.MercuryDataProvider
- typing.Optional


================================================================================
mercury_ai.analysis.ranking_engine
================================================================================

Classes
--------
- RankingEngine

Funções
--------
- calculate_rank_score
- rank

Imports
-------
- mercury_ai.models.analysis_result.AnalysisResult
- typing.List


================================================================================
mercury_ai.analysis.risk_engine
================================================================================

Classes
--------
- RiskEngine

Funções
--------
- __init__
- assess

Imports
-------
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.risk_assessment.RiskAssessment


================================================================================
mercury_ai.analysis.session_engine
================================================================================

Classes
--------
- SessionEngine

Funções
--------
- _build_explanation
- _calculate_liquidity
- _calculate_quality
- _detect_overlap
- _detect_session
- analyze

Imports
-------
- mercury_ai.config.sessions
- mercury_ai.models.session_analysis.SessionAnalysis
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.List


================================================================================
mercury_ai.analysis.smart_money.bos_engine
================================================================================

Classes
--------
- BOSEngine
- BOSResult

Funções
--------
- analyze

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.market_structure.MarketStructure


================================================================================
mercury_ai.analysis.smart_money.choch_engine
================================================================================

Classes
--------
- CHOCHEngine
- CHOCHResult

Funções
--------
- analyze

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.market_structure.MarketStructure


================================================================================
mercury_ai.analysis.smart_money.liquidity_engine
================================================================================

Classes
--------
- EqualHighGroup
- EqualHighMetrics
- EqualHighScore
- LiquidityEngine

Funções
--------
- __init__
- analyze
- analyze_tuple
- build_equal_high_groups
- calculate_metrics
- calculate_scores
- generate_equal_high_evidence
- populate_profile
- select_best_equal_high
- validate_equal_high_groups

Imports
-------
- dataclasses.dataclass
- dataclasses.replace
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.liquidity_analysis.LiquidityAnalysis
- mercury_ai.models.liquidity_result.LiquidityResult
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- mercury_ai.models.swing_analysis.Swing
- numpy
- pandas
- typing.List
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.analysis.smart_money.liquidity_event_engine
================================================================================

Classes
--------
- LiquidityEvent
- LiquidityEventEngine

Funções
--------
- detect
- to_evidence

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.liquidity_event_enum.LiquidityEventType
- pandas
- typing.List


================================================================================
mercury_ai.analysis.smart_money.market_structure_engine
================================================================================

Classes
--------
- MarketStructureEngine

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.market_structure.MarketStructure
- pandas


================================================================================
mercury_ai.analysis.smart_money.order_block_engine
================================================================================

Classes
--------
- OrderBlockEngine

Funções
--------
- analyze

Imports
-------
- pandas
- typing.Dict
- typing.Optional


================================================================================
mercury_ai.analysis.smart_money.smart_money_engine
================================================================================

Classes
--------
- SmartMoneyEngine

Funções
--------
- __init__
- analyze
- get_evidences

Imports
-------
- mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine
- mercury_ai.analysis.smart_money.bos_engine.BOSEngine
- mercury_ai.analysis.smart_money.choch_engine.CHOCHEngine
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.analysis.smart_money.market_structure_engine.MarketStructureEngine
- mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- typing.List
- typing.Optional


================================================================================
mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- create_mock_swing
- engine
- test_duplicate_timestamps_and_prices
- test_extreme_atr_values
- test_floating_point_precision
- test_large_candidate_set
- test_ordering_determinism

Imports
-------
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.models.swing_analysis.Swing
- numpy
- pytest


================================================================================
mercury_ai.analysis.smart_money.tests.test_liquidity_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- create_mock_swing
- default_engine
- test_analyze_orchestrator_full
- test_determinism
- test_evidence_builder_generation
- test_group_builder_atr_tolerance
- test_group_builder_distance_filter
- test_group_builder_duplicate_swings
- test_group_builder_empty
- test_group_builder_maximum_touches
- test_group_builder_minimum_touches
- test_group_builder_multiple_groups
- test_group_builder_single_group
- test_group_builder_strength_filter
- test_metrics_builder_single_group
- test_profile_builder_population
- test_score_builder_logic
- test_selector_empty_input
- test_selector_ordering_and_tie_breakers

Imports
-------
- mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup
- mercury_ai.analysis.smart_money.liquidity_engine.EqualHighMetrics
- mercury_ai.analysis.smart_money.liquidity_engine.EqualHighScore
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- mercury_ai.models.swing_analysis.Swing
- pandas
- pytest
- random
- typing.List


================================================================================
mercury_ai.analysis.smart_money.tests.test_liquidity_stress
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- create_swing
- generate_swings
- test_liquidity_engine_stress

Imports
-------
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.models.swing_analysis.Swing
- pytest
- random


================================================================================
mercury_ai.analysis.statistical_auditor
================================================================================

Classes
--------
- StatisticalAuditor

Funções
--------
- __init__
- audit

Imports
-------
- collections.Counter
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.analysis.support_resistance_analyzer
================================================================================

Classes
--------
- SupportResistanceAnalyzer

Funções
--------
- _build_explanation
- _cluster_zones
- _detect_price_location
- _detect_swings
- _finalize_zone
- _find_nearest_zones
- _score_zones
- analyze

Imports
-------
- mercury_ai.models.support_resistance_analysis.SupportResistanceAnalysis
- numpy
- pandas
- ta.volatility.AverageTrueRange
- typing.List
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.analysis.swing_engine
================================================================================

Classes
--------
- SwingEngine

Funções
--------
- __init__
- analyze_sequence
- calculate_atr
- detect_swings

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.swing_analysis.Swing
- mercury_ai.models.swing_analysis.SwingSequenceResult
- pandas
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.tests.test_benchmark_framework
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_benchmark_framework_execution

Imports
-------
- mercury_ai.analysis.benchmark_framework.MercuryBenchmarkFramework


================================================================================
mercury_ai.analysis.tests.test_candlestick_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_candlestick_engine_doji
- test_candlestick_engine_insufficient_data

Imports
-------
- mercury_ai.analysis.candlestick_engine.CandlestickEngine
- mercury_ai.models.market_condition.MarketCondition
- mercury_ai.models.market_data.MarketData
- pandas
- pytest


================================================================================
mercury_ai.analysis.tests.test_context_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_context_engine_aggregation

Imports
-------
- mercury_ai.analysis.context_engine.ContextEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_data.MarketData
- unittest.mock.Mock


================================================================================
mercury_ai.analysis.tests.test_fvg_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- fvg_engine
- test_fvg_engine_bullish

Imports
-------
- mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis
- pandas
- pytest


================================================================================
mercury_ai.analysis.tests.test_market_regime_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_market_regime_compression
- test_market_regime_strong_uptrend

Imports
-------
- mercury_ai.analysis.market_regime_engine.MarketRegimeEngine
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- unittest.mock.MagicMock


================================================================================
mercury_ai.analysis.tests.test_market_structure_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- ms_engine
- test_ms_engine_bearish
- test_ms_engine_bullish

Imports
-------
- mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- pandas
- pytest


================================================================================
mercury_ai.analysis.tests.test_momentum_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- momentum_engine
- test_momentum_engine_rsi_oversold

Imports
-------
- mercury_ai.analysis.momentum_engine.MomentumEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.momentum_analysis.MomentumAnalysis
- numpy
- pandas
- pytest


================================================================================
mercury_ai.analysis.tests.test_price_action_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- price_action_engine
- test_price_action_engine_engulfing

Imports
-------
- mercury_ai.analysis.price_action_engine.PriceActionEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.price_action_analysis.PriceActionAnalysis
- pandas
- pytest


================================================================================
mercury_ai.analysis.tests.test_trend_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_trend_engine_bearish_structure
- test_trend_engine_bullish_structure
- trend_engine

Imports
-------
- mercury_ai.analysis.trend_analyzer.TrendAnalyzer
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_data.MarketData
- pytest


================================================================================
mercury_ai.analysis.tests.test_volume_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_volume_engine_spike
- volume_engine

Imports
-------
- mercury_ai.analysis.volume_engine.VolumeEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.volume_analysis.VolumeAnalysis
- pandas
- pytest


================================================================================
mercury_ai.analysis.tests.test_vwap_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_vwap_engine_calculation
- vwap_engine

Imports
-------
- mercury_ai.analysis.vwap_engine.VWAPEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.vwap_analysis.VWAPAnalysis
- pandas
- pytest


================================================================================
mercury_ai.analysis.trade_memory_engine
================================================================================

Classes
--------
- TradeMemoryEngine

Funções
--------
- find_similar_trades
- save_trade

Imports
-------
- mercury_ai.models.trade_memory.TradeMemory
- os
- pandas
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.trade_outcome_engine
================================================================================

Classes
--------
- TradeOutcomeEngine

Funções
--------
- determine_outcome

Imports
-------
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- typing.Any
- typing.Dict


================================================================================
mercury_ai.analysis.trend_analyzer
================================================================================

Classes
--------
- TrendAnalyzer

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_data.MarketData
- typing.List


================================================================================
mercury_ai.analysis.validation_engine
================================================================================

Classes
--------
- ValidationEngine

Funções
--------
- _validate_context_consistency
- _validate_evidence_consistency
- validate_all

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- pandas
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.volatility_engine
================================================================================

Classes
--------
- VolatilityEngine

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.volatility_analysis.VolatilityAnalysis
- pandas
- ta.volatility.AverageTrueRange
- typing.List


================================================================================
mercury_ai.analysis.volume_engine
================================================================================

Classes
--------
- VolumeEngine

Funções
--------
- __init__
- _analyze_logic
- analyze

Imports
-------
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.volume_analysis.VolumeAnalysis
- pandas
- typing.Optional


================================================================================
mercury_ai.analysis.volume_intelligence_engine
================================================================================

Classes
--------
- VolumeIntelligenceEngine

Funções
--------
- evaluate

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.volume_profile.VolumeProfile
- pandas
- typing.List
- typing.Tuple


================================================================================
mercury_ai.analysis.vwap_engine
================================================================================

Classes
--------
- VWAPEngine

Funções
--------
- __init__
- _analyze_logic
- analyze

Imports
-------
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.vwap_analysis.VWAPAnalysis
- pandas
- typing.Optional


================================================================================
mercury_ai.analysis.weight_simulator
================================================================================

Classes
--------
- WeightSimulator

Funções
--------
- __init__
- simulate

Imports
-------
- mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor
- typing.Any
- typing.Dict


================================================================================
mercury_ai.brain.exceptions
================================================================================

Classes
--------
- InvalidWeightConfiguration

Funções
--------
(nenhuma)

Imports
-------
(nenhum)


================================================================================
mercury_ai.brain.explainability_engine
================================================================================

Classes
--------
- ExplainabilityEngine

Funções
--------
- analyze

Imports
-------
- mercury_ai.models.analysis_result.AnalysisDirection
- mercury_ai.models.analysis_result.AnalysisResult
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.probability_result.ProbabilityResult
- mercury_ai.models.trading_explanation.TradingExplanation
- typing.Tuple


================================================================================
mercury_ai.brain.institutional_brain
================================================================================

Classes
--------
- InstitutionalBrain

Funções
--------
- _get_all_evidences
- explain

Imports
-------
- mercury_ai.models.analysis_result.AnalysisResult
- mercury_ai.models.evidence.Evidence
- typing.List


================================================================================
mercury_ai.brain.mercury_decision_engine
================================================================================

Classes
--------
- MercuryDecisionEngine

Funções
--------
- __init__
- _analyze_logic
- analyze

Imports
-------
- hashlib
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
- mercury_ai.analysis.confluence_engine.ConfluenceEngine
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine
- mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine
- mercury_ai.analysis.narrative_engine.NarrativeEngine
- mercury_ai.analysis.validation_engine.ValidationEngine
- mercury_ai.brain.probability_engine.ProbabilityEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.decision_result.DecisionResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- mercury_ai.models.version_metadata.VersionMetadata
- typing.List
- typing.Optional


================================================================================
mercury_ai.brain.probability_engine
================================================================================

Classes
--------
- ProbabilityEngine

Funções
--------
- __init__
- analyze

Imports
-------
- mercury_ai.models.probability_result.ProbabilityResult
- typing.Any
- typing.Dict
- typing.Optional


================================================================================
mercury_ai.brain.scanner
================================================================================

Classes
--------
- MercuryScanner

Funções
--------
- __init__
- _print_line
- _print_ranking
- _print_report
- _value
- scan

Imports
-------
- mercury_ai.analysis.evidence_query.EvidenceQuery
- mercury_ai.analysis.notification_center.NotificationCenter
- mercury_ai.analysis.ranking_engine.RankingEngine
- mercury_ai.brain.institutional_brain.InstitutionalBrain
- mercury_ai.config.configuration_center.MercuryConfigCenter
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.core.asset_registry.AssetRegistry
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider


================================================================================
mercury_ai.brain.tests.test_explainability_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_explainability_engine_analysis

Imports
-------
- mercury_ai.brain.explainability_engine.ExplainabilityEngine
- mercury_ai.models.analysis_result.AnalysisDirection
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.probability_result.ProbabilityResult
- unittest.mock.MagicMock


================================================================================
mercury_ai.brain.tests.test_mercury_decision_benchmark
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_decision_engine_benchmark

Imports
-------
- mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.confidence_result.ConfidenceResult
- mercury_ai.models.data_quality_result.DataQualityResult
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- time
- unittest.mock.MagicMock


================================================================================
mercury_ai.brain.tests.test_mercury_decision_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _create_context
- decision_engine
- test_decision_engine_buy_scenario
- test_decision_engine_low_quality_scenario
- test_decision_engine_sell_scenario
- test_decision_engine_wait_scenario

Imports
-------
- mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.models.confidence_result.ConfidenceResult
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.probability_result.ProbabilityResult
- mercury_ai.models.trading_explanation.TradingExplanation
- pytest
- unittest.mock.MagicMock


================================================================================
mercury_ai.brain.tests.test_probability_engine
================================================================================

Classes
--------
- MockRiskContext

Funções
--------
- __init__
- test_probability_engine_calculation

Imports
-------
- mercury_ai.brain.probability_engine.ProbabilityEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- pytest
- unittest.mock.MagicMock


================================================================================
mercury_ai.calendar.economic_calendar
================================================================================

Classes
--------
- EconomicCalendar

Funções
--------
- get_events

Imports
-------
- datetime.datetime


================================================================================
mercury_ai.calendar.tests.test_economic_calendar
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.calendar.economic_calendar.EconomicCalendar


================================================================================
mercury_ai.config.configuration_center
================================================================================

Classes
--------
- MercuryConfigCenter

Funções
--------
- __init__
- _load_from_file
- get
- save

Imports
-------
- json
- mercury_ai.config.settings
- os


================================================================================
mercury_ai.core.analysis_pipeline
================================================================================

Classes
--------
- AnalysisPipeline

Funções
--------
- __init__
- _record_telemetry
- analyze

Imports
-------
- dataclasses.replace
- json
- mercury_ai.analysis.candlestick_engine.CandlestickEngine
- mercury_ai.analysis.confluence_engine.ConfluenceEngine
- mercury_ai.analysis.context_engine.ContextEngine
- mercury_ai.analysis.context_intelligence_engine.ContextIntelligenceEngine
- mercury_ai.analysis.evidence_engine.EvidenceEngine
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine
- mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine
- mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine
- mercury_ai.analysis.institutional_trade_filter_engine.InstitutionalTradeFilterEngine
- mercury_ai.analysis.market_condition_engine.MarketConditionEngine
- mercury_ai.analysis.market_context_builder.MarketContextBuilder
- mercury_ai.analysis.market_regime_engine.MarketRegimeEngine
- mercury_ai.analysis.market_state_engine.MarketStateEngine
- mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine
- mercury_ai.analysis.mtf_engine.MTFEngine
- mercury_ai.analysis.price_action_analyzer.PriceActionAnalyzer
- mercury_ai.analysis.risk_engine.RiskEngine
- mercury_ai.analysis.session_engine.SessionEngine
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine
- mercury_ai.analysis.smart_money.smart_money_engine.SmartMoneyEngine
- mercury_ai.analysis.support_resistance_analyzer.SupportResistanceAnalyzer
- mercury_ai.analysis.trend_analyzer.TrendAnalyzer
- mercury_ai.analysis.volatility_engine.VolatilityEngine
- mercury_ai.analysis.volume_intelligence_engine.VolumeIntelligenceEngine
- mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
- mercury_ai.config.timeframes.DEFAULT_TIMEFRAME
- mercury_ai.core.exceptions.MarketClosedException
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.core.runtime_report.RuntimeReport
- mercury_ai.core.runtime_report.TelemetryData
- mercury_ai.data.data_quality_engine.DataQualityEngine
- mercury_ai.data.indicator_engine.IndicatorEngine
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- mercury_ai.models.analysis_result.AnalysisResult
- mercury_ai.models.decision_result.DecisionResult
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.version_metadata.VersionMetadata
- mercury_ai.providers.base_provider.MarketDataProvider
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.Dict
- typing.List
- typing.Optional
- uuid


================================================================================
mercury_ai.core.asset_registry
================================================================================

Classes
--------
- Asset
- AssetRegistry

Funções
--------
- __init__
- _load_from_file
- filter_assets
- get_assets_for_broker
- get_enabled_assets
- register_asset
- save
- search_assets
- set_enabled
- set_priority
- update_asset_stats

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- json
- os
- time
- typing.Dict
- typing.List
- typing.Optional


================================================================================
mercury_ai.core.audit_sink
================================================================================

Classes
--------
- AuditEvent
- AuditSink
- MemoryAuditSink

Funções
--------
- __init__
- get_events
- log
- log

Imports
-------
- abc.ABC
- abc.abstractmethod
- dataclasses.dataclass
- typing.List


================================================================================
mercury_ai.core.auto_health
================================================================================

Classes
--------
- MercuryAutoHealth

Funções
--------
- __init__
- run_all_checks

Imports
-------
- logging
- mercury_ai.core.asset_registry.AssetRegistry
- mercury_ai.core.health_center.HealthCenter
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- os


================================================================================
mercury_ai.core.banner
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- show_banner

Imports
-------
(nenhum)


================================================================================
mercury_ai.core.base_engine
================================================================================

Classes
--------
- BaseEngine
- EngineResult

Funções
--------
- analyze

Imports
-------
- abc.ABC
- abc.abstractmethod
- dataclasses.dataclass
- typing.Tuple


================================================================================
mercury_ai.core.data_quality_gate
================================================================================

Classes
--------
- DataQualityGate
- DataQualityResult

Funções
--------
- evaluate

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.core.exceptions
================================================================================

Classes
--------
- MarketClosedException

Funções
--------
(nenhuma)

Imports
-------
(nenhum)


================================================================================
mercury_ai.core.export_center
================================================================================

Classes
--------
- ExportCenter

Funções
--------
- __init__
- export_data
- export_history
- export_snapshots

Imports
-------
- json
- mercury_ai.analysis.data_exporter.DataExporter
- os
- pandas
- pathlib.Path
- typing.Any
- typing.Callable
- typing.Dict
- typing.List
- typing.Optional
- zipfile


================================================================================
mercury_ai.core.health_center
================================================================================

Classes
--------
- HealthCenter

Funções
--------
- __init__
- get_component_health
- get_system_metrics

Imports
-------
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- psutil
- time
- typing.Any
- typing.Dict


================================================================================
mercury_ai.core.job_manager
================================================================================

Classes
--------
- JobManager

Funções
--------
- __init__
- _execute_tasks
- _job_loop
- pause
- resume
- start
- stop

Imports
-------
- mercury_ai.analysis.health_checker.HealthChecker
- mercury_ai.analysis.performance_statistics.PerformanceStatistics
- mercury_ai.config.assets.SUPPORTED_ASSETS
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- threading
- time
- typing.Any
- typing.Dict
- typing.List
- typing.Optional


================================================================================
mercury_ai.core.observability_center
================================================================================

Classes
--------
- ObservabilityCenter

Funções
--------
- __init__
- get_metrics
- record_asset_time
- record_engine_time
- record_provider_latency

Imports
-------
- psutil
- time
- typing.Any
- typing.Dict


================================================================================
mercury_ai.core.pipeline_audit_middleware
================================================================================

Classes
--------
- PipelineAuditMiddleware

Funções
--------
- __call__
- __init__

Imports
-------
- datetime.datetime
- mercury_ai.core.audit_sink.AuditEvent
- mercury_ai.core.audit_sink.AuditSink
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- typing.Any
- typing.Callable


================================================================================
mercury_ai.core.pipeline_executor
================================================================================

Classes
--------
- PipelineContractError
- PipelineExecutor

Funções
--------
- __init__
- execute
- stage

Imports
-------
- contextlib.nullcontext
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- typing.Any
- typing.Callable
- typing.Dict
- typing.List
- typing.Optional
- typing.Type


================================================================================
mercury_ai.core.pipeline_profiler
================================================================================

Classes
--------
- PipelineProfiler
- _StageBuilder

Funções
--------
- __init__
- __init__
- end_pipeline
- end_stage
- finalize
- json
- pretty_print
- stage
- start_pipeline
- start_stage
- summary

Imports
-------
- contextlib.contextmanager
- dataclasses.asdict
- gc
- json
- mercury_ai.models.profiler_models.PipelineProfile
- mercury_ai.models.profiler_models.StageProfile
- threading
- time
- tracemalloc
- typing.List


================================================================================
mercury_ai.core.read_only
================================================================================

Classes
--------
- ReadOnlyViolation

Funções
--------
- check_read_only

Imports
-------
(nenhum)


================================================================================
mercury_ai.core.runtime_report
================================================================================

Classes
--------
- RuntimeReport
- TelemetryData

Funções
--------
- to_dict

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Any
- typing.Dict
- typing.List
- typing.Optional


================================================================================
mercury_ai.core.security_center
================================================================================

Classes
--------
- AuditEvent
- SecurityCenter

Funções
--------
- __init__
- generate_audit_trail
- generate_security_report
- log_event

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- json
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.core.session_manager
================================================================================

Classes
--------
- SessionManager

Funções
--------
- __init__
- get_info

Imports
-------
- mercury_ai.config.settings
- mercury_ai.utils.deterministic_clock.DeterministicClock
- uuid


================================================================================
mercury_ai.core.startup
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- start

Imports
-------
- mercury_ai.config.settings
- mercury_ai.core.banner.show_banner
- mercury_ai.providers.provider.MarketProvider


================================================================================
mercury_ai.data.data_normalizer
================================================================================

Classes
--------
- DataNormalizer

Funções
--------
- normalize

Imports
-------
- pandas


================================================================================
mercury_ai.data.data_quality_engine
================================================================================

Classes
--------
- DataQualityEngine

Funções
--------
- validate

Imports
-------
- pandas
- typing.Tuple


================================================================================
mercury_ai.data.indicator_engine
================================================================================

Classes
--------
- IndicatorEngine

Funções
--------
- calculate

Imports
-------
- numpy
- pandas


================================================================================
mercury_ai.data.market_data
================================================================================

Classes
--------
- MarketDataService

Funções
--------
- __init__
- _normalize_dataframe
- get_data

Imports
-------
- mercury_ai.core.exceptions.MarketClosedException
- mercury_ai.data.data_normalizer.DataNormalizer
- pandas
- typing.List


================================================================================
mercury_ai.data.market_data_provider
================================================================================

Classes
--------
- MarketDataProvider

Funções
--------
- get_data

Imports
-------
- pandas
- typing.Protocol


================================================================================
mercury_ai.data.mercury_data_provider
================================================================================

Classes
--------
- AlphaVantageProvider
- BaseProvider
- BinanceProvider
- IMercuryDataProvider
- MercuryDataProvider
- MetaTrader5Provider
- PolygonProvider
- ProviderHealth
- ProviderMetrics
- ProviderPriority
- ProviderRegistry
- ProviderStatus
- TwelveDataProvider
- YahooProvider

Funções
--------
- __init__
- __init__
- __init__
- __init__
- __init__
- __init__
- __init__
- __init__
- _get_best_provider
- connect
- connect
- connect
- get_candles
- get_candles
- get_candles
- get_history
- get_history
- get_history
- get_last_price
- get_last_price
- get_last_price
- get_symbols
- health
- health
- health
- healthcheck
- market_status
- market_status
- market_status
- register_provider
- trigger_failover

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- enum.Enum
- functools.lru_cache
- logging
- pandas
- time
- typing.Any
- typing.Dict
- typing.List
- typing.Optional
- typing.Protocol


================================================================================
mercury_ai.data.providers.historical_data_provider
================================================================================

Classes
--------
- HistoricalDataProvider

Funções
--------
- __init__
- get_data
- is_available
- max_history
- set_index
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
- pandas


================================================================================
mercury_ai.data.replay_data_provider
================================================================================

Classes
--------
- ReplayDataProvider

Funções
--------
- __init__
- get_data

Imports
-------
- os
- pandas


================================================================================
mercury_ai.database.history_logger
================================================================================

Classes
--------
- HistoryLogger

Funções
--------
- __init__
- save

Imports
-------
- csv
- datetime.datetime
- pathlib.Path


================================================================================
mercury_ai.database.replay_storage
================================================================================

Classes
--------
- ReplayMetrics
- ReplayStorage

Funções
--------
- __init__
- save

Imports
-------
- dataclasses.dataclass
- json
- os
- typing.Any


================================================================================
mercury_ai.database.snapshot_logger
================================================================================

Classes
--------
- DecisionSnapshotLogger

Funções
--------
- __init__
- list_snapshots
- load_snapshot
- save

Imports
-------
- dataclasses.asdict
- functools.lru_cache
- json
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- pathlib.Path
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.indicators.rsi
================================================================================

Classes
--------
- RSIIndicator

Funções
--------
- calculate

Imports
-------
(nenhum)


================================================================================
mercury_ai.main
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- mercury_ai.brain.scanner.MercuryScanner


================================================================================
mercury_ai.market.market_engine
================================================================================

Classes
--------
- MarketEngine

Funções
--------
- __init__
- show_market

Imports
-------
- mercury_ai.config.settings.ASSET
- mercury_ai.providers.market_provider.MarketProvider


================================================================================
mercury_ai.models.analysis_result
================================================================================

Classes
--------
- AnalysisDirection
- AnalysisResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- enum.Enum
- mercury_ai.config.settings
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.Any
- typing.List


================================================================================
mercury_ai.models.benchmark_report
================================================================================

Classes
--------
- BenchmarkReport
- BenchmarkRunResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.analysis.metric_calculator.PerformanceMetrics
- mercury_ai.models.decision_result.DecisionResult
- typing.Tuple


================================================================================
mercury_ai.models.candlestick_analysis
================================================================================

Classes
--------
- CandlestickAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.List
- typing.Optional


================================================================================
mercury_ai.models.confidence_result
================================================================================

Classes
--------
- ConfidenceResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.confluence_result
================================================================================

Classes
--------
- ConfluenceResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.analysis_result.AnalysisDirection
- typing.Any
- typing.Tuple


================================================================================
mercury_ai.models.confluence_score
================================================================================

Classes
--------
- ConfluenceScore

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.data_quality_result
================================================================================

Classes
--------
- DataQualityResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Tuple


================================================================================
mercury_ai.models.decision_input
================================================================================

Classes
--------
- DecisionInput

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.List


================================================================================
mercury_ai.models.decision_node
================================================================================

Classes
--------
- DecisionNode

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Optional


================================================================================
mercury_ai.models.decision_outcome
================================================================================

Classes
--------
- DecisionOutcome

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Any
- typing.Dict


================================================================================
mercury_ai.models.decision_result
================================================================================

Classes
--------
- DecisionResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.decision_trace.DecisionTrace
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.trading_explanation.TradingExplanation
- mercury_ai.models.version_metadata.VersionMetadata
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.models.decision_snapshot
================================================================================

Classes
--------
- DecisionSnapshot

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.config.settings
- mercury_ai.models.decision_result.DecisionResult
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.version_metadata.VersionMetadata
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.models.decision_trace
================================================================================

Classes
--------
- DecisionTrace

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.decision_node.DecisionNode
- typing.Tuple


================================================================================
mercury_ai.models.evidence
================================================================================

Classes
--------
- Evidence

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.config.timeframes.DEFAULT_TIMEFRAME
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.Any
- typing.Dict


================================================================================
mercury_ai.models.evidence_ranking
================================================================================

Classes
--------
- EvidenceRankingResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.evidence.Evidence
- typing.List
- typing.Optional


================================================================================
mercury_ai.models.fair_value_gap_analysis
================================================================================

Classes
--------
- FairValueGapAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.evidence.Evidence
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.models.liquidity_analysis
================================================================================

Classes
--------
- LiquidityAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.evidence.Evidence
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.models.liquidity_event_enum
================================================================================

Classes
--------
- LiquidityEventType

Funções
--------
(nenhuma)

Imports
-------
- enum.Enum


================================================================================
mercury_ai.models.liquidity_profile
================================================================================

Classes
--------
- LiquidityProfile

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.liquidity_result
================================================================================

Classes
--------
- LiquidityResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Any
- typing.Tuple


================================================================================
mercury_ai.models.market_condition
================================================================================

Classes
--------
- MarketCondition

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Optional


================================================================================
mercury_ai.models.market_context
================================================================================

Classes
--------
- MarketContext

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.liquidity_profile.LiquidityProfile
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.price_action.PriceActionAnalysis
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
- typing.List
- typing.Optional


================================================================================
mercury_ai.models.market_data
================================================================================

Classes
--------
- MarketData

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.market_evidence_bundle
================================================================================

Classes
--------
- MarketEvidenceBundle

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.evidence.Evidence
- typing.Tuple


================================================================================
mercury_ai.models.market_regime
================================================================================

Classes
--------
- MarketRegime

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- typing.List


================================================================================
mercury_ai.models.market_regime_enum
================================================================================

Classes
--------
- MarketRegimeEnum

Funções
--------
(nenhuma)

Imports
-------
- enum.Enum


================================================================================
mercury_ai.models.market_state
================================================================================

Classes
--------
- MarketState

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.market_state_enum.MarketStateEnum


================================================================================
mercury_ai.models.market_state_enum
================================================================================

Classes
--------
- MarketStateEnum

Funções
--------
(nenhuma)

Imports
-------
- enum.Enum


================================================================================
mercury_ai.models.market_structure
================================================================================

Classes
--------
- MarketStructure

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field


================================================================================
mercury_ai.models.market_structure_profile
================================================================================

Classes
--------
- MarketStructureProfile

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.swing_analysis.Swing
- typing.List
- typing.Optional


================================================================================
mercury_ai.models.market_thesis
================================================================================

Classes
--------
- MarketThesis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.confidence_result.ConfidenceResult
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.risk_assessment.RiskAssessment
- typing.List


================================================================================
mercury_ai.models.memory_audit
================================================================================

Classes
--------
- MemoryAuditResult
- MemorySnapshot

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- time
- tracemalloc
- typing.List


================================================================================
mercury_ai.models.momentum_analysis
================================================================================

Classes
--------
- MomentumAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.evidence.Evidence
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.models.mtf_consensus
================================================================================

Classes
--------
- MTFConsensus

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.performance
================================================================================

Classes
--------
- HotspotReport
- PipelineMetric
- StageMetric

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Tuple


================================================================================
mercury_ai.models.performance_metrics
================================================================================

Classes
--------
- PerformanceMetrics

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Any
- typing.Dict


================================================================================
mercury_ai.models.price_action
================================================================================

Classes
--------
- PriceActionAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.price_action_analysis
================================================================================

Classes
--------
- PriceActionAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.models.probability_result
================================================================================

Classes
--------
- ProbabilityResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Any
- typing.Dict


================================================================================
mercury_ai.models.professional_thesis
================================================================================

Classes
--------
- ProfessionalThesis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.models.profiler_models
================================================================================

Classes
--------
- HotspotSummary
- PipelineProfile
- StageProfile

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Tuple


================================================================================
mercury_ai.models.regression
================================================================================

Classes
--------
- BenchmarkMetrics
- RegressionResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Any


================================================================================
mercury_ai.models.risk_assessment
================================================================================

Classes
--------
- RiskAssessment

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.session_analysis
================================================================================

Classes
--------
- SessionAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Optional


================================================================================
mercury_ai.models.signal
================================================================================

Classes
--------
- Signal

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.config.timeframes.DEFAULT_TIMEFRAME
- typing.List


================================================================================
mercury_ai.models.smart_money
================================================================================

Classes
--------
- SmartMoneyAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.market_structure.MarketStructure


================================================================================
mercury_ai.models.stress_test
================================================================================

Classes
--------
- StressTestResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.market_data.MarketData
- typing.List


================================================================================
mercury_ai.models.support_resistance
================================================================================

Classes
--------
- SupportResistanceAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.support_resistance_analysis
================================================================================

Classes
--------
- SupportResistanceAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- typing.Optional


================================================================================
mercury_ai.models.swing_analysis
================================================================================

Classes
--------
- Swing
- SwingSequenceResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.List
- typing.Optional


================================================================================
mercury_ai.models.trade_memory
================================================================================

Classes
--------
- TradeMemory

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.models.trade_permission
================================================================================

Classes
--------
- TradePermission

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Optional


================================================================================
mercury_ai.models.trading_explanation
================================================================================

Classes
--------
- TradingExplanation

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.decision_result.DecisionResult
- typing.Any
- typing.Dict
- typing.TYPE_CHECKING
- typing.Tuple


================================================================================
mercury_ai.models.trend_analysis
================================================================================

Classes
--------
- TrendAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.models.version_metadata
================================================================================

Classes
--------
- VersionMetadata

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.volatility_analysis
================================================================================

Classes
--------
- VolatilityAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- mercury_ai.models.evidence.Evidence
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.models.volume_analysis
================================================================================

Classes
--------
- VolumeAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.evidence.Evidence
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.models.volume_profile
================================================================================

Classes
--------
- VolumeProfile

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass


================================================================================
mercury_ai.models.vwap_analysis
================================================================================

Classes
--------
- VWAPAnalysis

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.models.evidence.Evidence
- typing.Any
- typing.Dict
- typing.Tuple


================================================================================
mercury_ai.news.news_provider
================================================================================

Classes
--------
- NewsProvider

Funções
--------
- get_news

Imports
-------
- datetime.datetime


================================================================================
mercury_ai.news.tests.test_news_provider
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.news.news_provider.NewsProvider


================================================================================
mercury_ai.operations.demo_manager
================================================================================

Classes
--------
- DemoOperationsManager

Funções
--------
- __init__
- run_simulation

Imports
-------
- mercury_ai.config.assets.SUPPORTED_ASSETS
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- mercury_ai.utils.deterministic_clock.DeterministicClock
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.presentation.signal_formatter
================================================================================

Classes
--------
- SignalFormatter

Funções
--------
- format

Imports
-------
(nenhum)


================================================================================
mercury_ai.providers.base_provider
================================================================================

Classes
--------
- MarketDataProvider

Funções
--------
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
- pandas
- typing.Protocol


================================================================================
mercury_ai.providers.data_adapters
================================================================================

Classes
--------
- AlphaVantageAdapter
- BaseAdapter
- BinanceAdapter
- MetaTrader5Adapter
- PolygonAdapter
- TwelveDataAdapter
- YahooAdapter

Funções
--------
- __init__
- __init__
- __init__
- __init__
- __init__
- __init__
- __init__
- check_health
- get_data
- get_data

Imports
-------
- mercury_ai.providers.data_interfaces.IDataProvider
- pandas
- yfinance


================================================================================
mercury_ai.providers.data_interfaces
================================================================================

Classes
--------
- IDataProvider

Funções
--------
- check_health
- get_data

Imports
-------
- pandas
- typing.List
- typing.Protocol


================================================================================
mercury_ai.providers.future_broker_provider
================================================================================

Classes
--------
- FutureBrokerProvider

Funções
--------
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
(nenhum)


================================================================================
mercury_ai.providers.future_polygon_provider
================================================================================

Classes
--------
- FuturePolygonProvider

Funções
--------
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
(nenhum)


================================================================================
mercury_ai.providers.future_tradingview_provider
================================================================================

Classes
--------
- FutureTradingViewProvider

Funções
--------
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
(nenhum)


================================================================================
mercury_ai.providers.historical_replay_provider
================================================================================

Classes
--------
- HistoricalReplayProvider

Funções
--------
- __init__
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
- mercury_ai.providers.base_provider.MarketDataProvider
- os
- pandas


================================================================================
mercury_ai.providers.market_provider
================================================================================

Classes
--------
- MercuryDataProvider

Funções
--------
- __init__
- _get_best_provider
- _healthy_providers
- best_provider
- connect
- get_candles
- get_history
- get_last_price
- health
- market_status
- register_provider
- trigger_failover

Imports
-------
- functools.lru_cache
- logging
- mercury_ai.providers.data_adapters.AlphaVantageAdapter
- mercury_ai.providers.data_adapters.BinanceAdapter
- mercury_ai.providers.data_adapters.MetaTrader5Adapter
- mercury_ai.providers.data_adapters.PolygonAdapter
- mercury_ai.providers.data_adapters.TwelveDataAdapter
- mercury_ai.providers.data_adapters.YahooAdapter
- mercury_ai.providers.data_interfaces.IDataProvider
- pandas
- time
- typing.Dict


================================================================================
mercury_ai.providers.mercury_data_provider
================================================================================

Classes
--------
- MercuryDataProvider

Funções
--------
- __init__
- _get_best_provider
- best_provider
- connect
- get_candles
- get_data
- get_history
- get_last_price
- health
- is_available
- market_status
- register_provider

Imports
-------
- functools.lru_cache
- logging
- mercury_ai.providers.data_adapters.AlphaVantageAdapter
- mercury_ai.providers.data_adapters.BinanceAdapter
- mercury_ai.providers.data_adapters.MetaTrader5Adapter
- mercury_ai.providers.data_adapters.PolygonAdapter
- mercury_ai.providers.data_adapters.TwelveDataAdapter
- mercury_ai.providers.data_adapters.YahooAdapter
- mercury_ai.providers.data_interfaces.IDataProvider
- pandas
- time
- typing.Dict


================================================================================
mercury_ai.providers.provider
================================================================================

Classes
--------
- MarketProvider

Funções
--------
- get_market_status
- get_name

Imports
-------
(nenhum)


================================================================================
mercury_ai.providers.tests.test_market_provider
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.providers.market_provider.MarketProvider


================================================================================
mercury_ai.providers.yahoo_finance_provider
================================================================================

Classes
--------
- YahooFinanceProvider

Funções
--------
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
- mercury_ai.core.exceptions.MarketClosedException
- mercury_ai.providers.base_provider.MarketDataProvider
- pandas
- yfinance


================================================================================
mercury_ai.sessions.market_sessions
================================================================================

Classes
--------
- MarketSessions

Funções
--------
- get_current_session
- is_high_liquidity

Imports
-------
- datetime.datetime
- mercury_ai.config.sessions


================================================================================
mercury_ai.sessions.tests.test_market_sessions
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.sessions.market_sessions.MarketSessions


================================================================================
mercury_ai.utils.deterministic_clock
================================================================================

Classes
--------
- DeterministicClock

Funções
--------
- set_time
- utcnow

Imports
-------
- datetime.datetime
- datetime.timezone


================================================================================
mercury_ai.utils.memory_auditor
================================================================================

Classes
--------
- MemoryAuditor

Funções
--------
- __enter__
- __exit__
- __init__
- _compare
- _take_snapshot

Imports
-------
- gc
- mercury_ai.models.memory_audit.MemoryAuditResult
- mercury_ai.models.memory_audit.MemorySnapshot
- tracemalloc
- typing.Optional


================================================================================
mercury_ai.utils.performance_collector
================================================================================

Classes
--------
- PerformanceCollector
- _StageBuilder

Funções
--------
- __init__
- __init__
- _flatten_stages
- collect
- finalize
- stage

Imports
-------
- contextlib.contextmanager
- gc
- mercury_ai.models.performance.HotspotReport
- mercury_ai.models.performance.PipelineMetric
- mercury_ai.models.performance.StageMetric
- statistics
- time
- tracemalloc
- typing.List
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.utils.regression_detector
================================================================================

Classes
--------
- RegressionDetector

Funções
--------
- __init__
- _load_history
- detect
- save_history

Imports
-------
- json
- mercury_ai.models.regression.BenchmarkMetrics
- mercury_ai.models.regression.RegressionResult
- typing.Dict
- typing.List
- typing.Optional


================================================================================
mercury_ai.utils.report_generator
================================================================================

Classes
--------
- BenchmarkReportGenerator

Funções
--------
- __init__
- generate_csv
- generate_html
- generate_json
- generate_markdown

Imports
-------
- csv
- datetime
- json
- mercury_ai.models.performance.PipelineMetric
- mercury_ai.models.regression.RegressionResult
- mercury_ai.models.stress_test.StressTestResult
- platform
- sys
- typing.Any
- typing.Dict
- typing.List


================================================================================
mercury_ai.utils.stress_tester
================================================================================

Classes
--------
- StressTester

Funções
--------
- __init__
- register_generator
- run

Imports
-------
- mercury_ai.models.stress_test.StressTestResult
- random
- time
- tracemalloc
- typing.Any
- typing.Callable
- typing.Dict
- typing.List


================================================================================
mercury_ai.utils.system_monitor
================================================================================

Classes
--------
- SystemMonitor

Funções
--------
- get_metrics

Imports
-------
- psutil
- time


================================================================================
run_deterministic_replay_scenarios
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- generate_deterministic_data
- run_replay_scenario

Imports
-------
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- numpy
- pandas


================================================================================
run_institutional_replay
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- load_local_data
- run_institutional_replay

Imports
-------
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- os
- pandas


================================================================================
run_instrumented
================================================================================

Classes
--------
- MockProvider

Funções
--------
- get_data
- is_available
- max_history
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- pandas


================================================================================
stress_test_replay
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- generate_mock_data
- run_stress_test

Imports
-------
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- numpy
- os
- pandas
- shutil
- time
- tracemalloc


================================================================================
test_mercury_signal
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.presentation.signal_formatter.SignalFormatter
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider


================================================================================
teste_gemini
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- google.genai
- os


================================================================================
teste_llm
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- perguntar_llm

Imports
-------
- openai.OpenAI
- os


================================================================================
teste_openrouter
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- openai.OpenAI
- os


================================================================================
tests.test_adaptive_weighting
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- base_context
- test_adaptive_weighting_impact

Imports
-------
- mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_asset_registry
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_asset_registry_crud
- test_scanner_integration

Imports
-------
- json
- mercury_ai.brain.scanner.MercuryScanner
- mercury_ai.core.asset_registry.AssetRegistry
- os
- pytest


================================================================================
tests.test_auto_health
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_auto_health_checks

Imports
-------
- mercury_ai.core.asset_registry.AssetRegistry
- mercury_ai.core.auto_health.MercuryAutoHealth
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- pytest


================================================================================
tests.test_benchmark_integration
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- create_mock_swing
- test_external_benchmark_run

Imports
-------
- mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup
- mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- mercury_ai.models.swing_analysis.Swing
- pandas
- pytest
- typing.List
- typing.Tuple


================================================================================
tests.test_broker_filtering
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_scanner_broker_filtering

Imports
-------
- json
- mercury_ai.brain.scanner.MercuryScanner
- mercury_ai.core.asset_registry.AssetRegistry
- os
- pytest


================================================================================
tests.test_confidence_calibration
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- base_context
- test_confidence_calibration_optimal
- test_confidence_calibration_pessimistic
- test_confidence_calibration_reproducibility

Imports
-------
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state_enum.MarketStateEnum
- mercury_ai.models.mtf_consensus.MTFConsensus
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_confidence_calibration_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_confidence_calibration_auditor

Imports
-------
- mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor


================================================================================
tests.test_configuration_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_configuration_center_new_structure

Imports
-------
- mercury_ai.config.configuration_center.MercuryConfigCenter
- os
- pytest


================================================================================
tests.test_conflict_resolution
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_conflict_resolution_consensus
- test_conflict_resolution_multiple_engines
- test_conflict_resolution_simple_conflict

Imports
-------
- mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_data_exporter
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_data_exporter

Imports
-------
- mercury_ai.analysis.data_exporter.DataExporter
- pathlib.Path
- shutil


================================================================================
tests.test_data_provider_manager
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_data_provider_manager

Imports
-------
- mercury_ai.data.mercury_data_provider.BinanceProvider
- mercury_ai.data.mercury_data_provider.MercuryDataProvider
- mercury_ai.data.mercury_data_provider.YahooProvider
- pytest


================================================================================
tests.test_data_quality_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_data_quality_engine_issues
- test_data_quality_engine_perfect_data

Imports
-------
- mercury_ai.analysis.data_quality_engine.DataQualityEngine
- numpy
- pandas
- pytest


================================================================================
tests.test_demo_operations
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_demo_simulation

Imports
-------
- mercury_ai.operations.demo_manager.DemoOperationsManager


================================================================================
tests.test_demo_page
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_demo_execution_logic

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider


================================================================================
tests.test_determinism
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_determinism

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- pytest


================================================================================
tests.test_engine_performance_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_engine_performance_auditor

Imports
-------
- mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor


================================================================================
tests.test_evidence_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_evidence_engine_agreement
- test_evidence_engine_deduplication
- test_evidence_engine_normalization

Imports
-------
- mercury_ai.analysis.evidence_engine.EvidenceEngine
- mercury_ai.models.evidence.Evidence
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_evidence_quality_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_evidence_quality_engine_conflict
- test_evidence_quality_engine_independence
- test_evidence_quality_engine_redundancy
- test_evidence_quality_engine_redundancy_and_conflict

Imports
-------
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.models.evidence.Evidence
- pytest


================================================================================
tests.test_export_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_export_center_functionality

Imports
-------
- json
- mercury_ai.core.export_center.ExportCenter
- os
- pandas
- pytest


================================================================================
tests.test_health_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_health_auditor

Imports
-------
- mercury_ai.analysis.health_auditor.HealthAuditor


================================================================================
tests.test_health_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_health_center_data
- test_health_center_panel_load

Imports
-------
- app.dashboard.health_center_panel.render_health_center_panel
- mercury_ai.core.health_center.HealthCenter
- mercury_ai.providers.mercury_data_provider.MercuryDataProviderManager
- pytest


================================================================================
tests.test_health_checker
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_health_checker

Imports
-------
- mercury_ai.analysis.health_checker.HealthChecker


================================================================================
tests.test_institutional_report_generator
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_institutional_report_generator

Imports
-------
- mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator


================================================================================
tests.test_integrity_checker
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_integrity_checker

Imports
-------
- mercury_ai.analysis.integrity_checker.IntegrityChecker


================================================================================
tests.test_job_manager
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_job_manager

Imports
-------
- mercury_ai.core.job_manager.JobManager
- time


================================================================================
tests.test_live_monitor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_live_monitor_cycle

Imports
-------
- mercury_ai.analysis.live_monitor.LiveMonitor


================================================================================
tests.test_main_dashboard
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_main_dashboard_initialization

Imports
-------
- app.dashboard.main_dashboard.main
- pytest


================================================================================
tests.test_market_resilience
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_market_service_raises_on_empty_df
- test_market_service_raises_on_insufficient_candles
- test_pipeline_handles_market_closed

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.core.exceptions.MarketClosedException
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- pandas
- pytest
- unittest.mock.MagicMock
- yfinance


================================================================================
tests.test_notification_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_notification_center_features

Imports
-------
- mercury_ai.analysis.notification_center.NotificationCenter
- os
- pytest


================================================================================
tests.test_observability_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_observability_center

Imports
-------
- mercury_ai.core.observability_center.ObservabilityCenter
- pytest


================================================================================
tests.test_observability_panel
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_observability_dashboard_binding

Imports
-------
- app.dashboard.observability_panel.render_observability_dashboard
- pytest


================================================================================
tests.test_operational_history
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_operational_history_query

Imports
-------
- mercury_ai.analysis.operational_history.OperationalHistory


================================================================================
tests.test_performance_analytics
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_performance_analytics

Imports
-------
- mercury_ai.analysis.performance_analytics.PerformanceAnalytics


================================================================================
tests.test_performance_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_performance_center

Imports
-------
- mercury_ai.analysis.performance_center.PerformanceCenter


================================================================================
tests.test_performance_collector
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_performance_collector_integration

Imports
-------
- mercury_ai.utils.performance_collector.PerformanceCollector
- pytest
- time


================================================================================
tests.test_performance_statistics
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_performance_statistics

Imports
-------
- mercury_ai.analysis.performance_statistics.PerformanceStatistics


================================================================================
tests.test_pipeline_persistence
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_pipeline_snapshot_persistence

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider
- numpy
- pandas
- pathlib.Path
- pytest
- shutil


================================================================================
tests.test_probability_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_probability_calculation

Imports
-------
- mercury_ai.brain.probability_engine.ProbabilityEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_provider_priority_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_provider_priority_engine_ranking

Imports
-------
- mercury_ai.analysis.provider_priority_engine.ProviderPriorityEngine
- mercury_ai.data.mercury_data_provider.AlphaVantageProvider
- mercury_ai.data.mercury_data_provider.BinanceProvider
- mercury_ai.data.mercury_data_provider.MercuryDataProvider
- mercury_ai.data.mercury_data_provider.MetaTrader5Provider
- mercury_ai.data.mercury_data_provider.PolygonProvider
- mercury_ai.data.mercury_data_provider.TwelveDataProvider
- mercury_ai.data.mercury_data_provider.YahooProvider
- pytest


================================================================================
tests.test_read_only
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_read_only_mode

Imports
-------
- mercury_ai.core.read_only.ReadOnlyViolation
- mercury_ai.core.read_only.check_read_only
- pytest


================================================================================
tests.test_robustness
================================================================================

Classes
--------
- RobustnessMarketDataProvider

Funções
--------
- __init__
- get_data
- is_available
- source_name
- supports_symbol
- test_pipeline_robustness

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.data.market_data_provider.MarketDataProvider
- numpy
- pandas
- pytest
- typing.List


================================================================================
tests.test_scanner_priority
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_scanner_smart_priority_sorting

Imports
-------
- mercury_ai.brain.scanner.MercuryScanner
- mercury_ai.core.asset_registry.AssetRegistry
- pytest


================================================================================
tests.test_scanner_recovery
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_scanner_auto_recovery_triggers_failover

Imports
-------
- mercury_ai.brain.scanner.MercuryScanner
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_security_center
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_security_center_functionality

Imports
-------
- mercury_ai.core.security_center.SecurityCenter
- pytest


================================================================================
tests.test_session_id
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_session_id_consistency

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider


================================================================================
tests.test_session_manager
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_session_manager

Imports
-------
- mercury_ai.core.session_manager.SessionManager


================================================================================
tests.test_statistical_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_statistical_auditor

Imports
-------
- mercury_ai.analysis.statistical_auditor.StatisticalAuditor


================================================================================
tests.test_trade_outcome_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_trade_outcome_engine

Imports
-------
- mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine


================================================================================
tests.test_validation_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_validation_context_consistency_failure
- test_validation_evidence_consistency_failure
- validation_engine

Imports
-------
- mercury_ai.analysis.validation_engine.ValidationEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- pytest
- unittest.mock.MagicMock


================================================================================
tests.test_versioning
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_versioning

Imports
-------
- mercury_ai.config.settings
- mercury_ai.models.analysis_result.AnalysisResult
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- unittest.mock.MagicMock


================================================================================
tests.test_weight_simulator
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- test_weight_simulator

Imports
-------
- mercury_ai.analysis.weight_simulator.WeightSimulator


================================================================================
tools.project_mapper.architecture_audit
================================================================================

Classes
--------
- ArchitectureAudit

Funções
--------
- run

Imports
-------
- config.PROJECT_ROOT
- json
- pathlib.Path


================================================================================
tools.project_mapper.ast_parser
================================================================================

Classes
--------
- ASTParser

Funções
--------
- parse

Imports
-------
- ast
- pathlib.Path


================================================================================
tools.project_mapper.call_graph_builder
================================================================================

Classes
--------
- CallGraphBuilder

Funções
--------
- run

Imports
-------
- ast
- config.PROJECT_ROOT
- json
- pathlib.Path


================================================================================
tools.project_mapper.config
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- pathlib.Path


================================================================================
tools.project_mapper.dependency_builder
================================================================================

Classes
--------
- DependencyBuilder

Funções
--------
- run

Imports
-------
- collections.defaultdict
- config.PROJECT_ROOT
- json
- pathlib.Path


================================================================================
tools.project_mapper.main
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- architecture_audit.ArchitectureAudit
- call_graph_builder.CallGraphBuilder
- dependency_builder.DependencyBuilder
- module_index.ModuleIndexBuilder
- python_indexer.PythonIndexer
- scanner.ProjectScanner
- snapshot_builder.SnapshotBuilder
- writer.InventoryWriter


================================================================================
tools.project_mapper.models
================================================================================

Classes
--------
- FileInfo
- Inventory

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field


================================================================================
tools.project_mapper.module_index
================================================================================

Classes
--------
- ModuleIndexBuilder

Funções
--------
- run

Imports
-------
- collections.defaultdict
- config.PROJECT_ROOT
- json
- pathlib.Path


================================================================================
tools.project_mapper.python_indexer
================================================================================

Classes
--------
- PythonIndexer

Funções
--------
- run

Imports
-------
- ast
- config.PROJECT_ROOT
- json
- pathlib.Path


================================================================================
tools.project_mapper.scanner
================================================================================

Classes
--------
- ProjectScanner

Funções
--------
- scan

Imports
-------
- ast_parser.ASTParser
- config.IGNORE_DIRS
- config.IGNORE_FILES
- config.PROJECT_ROOT
- config.SOURCE_EXTENSIONS
- models.FileInfo
- models.Inventory
- pathlib.Path


================================================================================
tools.project_mapper.snapshot_builder
================================================================================

Classes
--------
- SnapshotBuilder

Funções
--------
- __init__
- _load_json
- _load_text
- build

Imports
-------
- json
- pathlib.Path


================================================================================
tools.project_mapper.writer
================================================================================

Classes
--------
- InventoryWriter

Funções
--------
- save

Imports
-------
- config.PROJECT_ROOT
- dataclasses.asdict
- json
- pathlib.Path


================================================================================
verify_assets
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- verify_assets

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

