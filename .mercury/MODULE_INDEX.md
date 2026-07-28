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
- mercury_ai.brain.scanner.MercuryScanner
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
- mercury_ai.providers.market_provider.MercuryDataProvider
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
- mercury_ai.brain.scanner.MercuryScanner
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
- mercury_ai.data.mercury_data_provider.ProviderStatus
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
- mercury_ai.brain.scanner.MercuryScanner
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
- _run_scan
- main

Imports
-------
- logging
- mercury_ai.brain.scanner.MercuryScanner
- sys
- threading


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
- BuyAndHoldBaseline
- EnhancedBenchmarkReport
- MercuryBenchmarkFramework
- StatisticalTestResult

Funções
--------
- __init__
- _apply_warm_cool_filter
- _compute_buy_and_hold
- _get_real_outcome
- _run_single_symbol
- _run_statistical_tests
- norm_sf
- run_benchmark
- run_quick_benchmark

Imports
-------
- concurrent.futures.ThreadPoolExecutor
- concurrent.futures.as_completed
- dataclasses.dataclass
- dataclasses.field
- logging
- math.erf
- math.sqrt
- mercury_ai.analysis.metric_calculator.MetricCalculator
- mercury_ai.analysis.metric_calculator.PerformanceMetrics
- mercury_ai.analysis.performance_engine.PerformanceEngine
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.models.benchmark_report.BenchmarkReport
- mercury_ai.models.benchmark_report.BenchmarkRunResult
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
- mercury_ai.utils.deterministic_clock.DeterministicClock
- numpy
- os
- psutil
- scipy.stats
- time
- tracemalloc
- typing.Dict
- typing.List
- typing.Optional
- typing.Tuple


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


================================================================================
mercury_ai.analysis.confidence_engine
================================================================================

Classes
--------
- ConfidenceComponents
- ConfidenceEngine

Funções
--------
- _get_grade
- calculate
- calibrate

Imports
-------
- dataclasses.dataclass
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
- mercury_ai.analysis.confluence_helpers.clamp_score
- mercury_ai.analysis.confluence_helpers.dominant_direction
- mercury_ai.analysis.confluence_helpers.has_conflict
- mercury_ai.analysis.decision_trace_engine.DecisionTraceEngine
- mercury_ai.analysis.institutional_contribution.InstitutionalContribution
- mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle


================================================================================
mercury_ai.analysis.confluence_helpers
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- clamp_score
- dominant_direction
- has_conflict

Imports
-------
- mercury_ai.models.direction.AnalysisDirection


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
- mercury_ai.analysis.confluence_helpers.clamp_score
- mercury_ai.analysis.confluence_helpers.has_conflict
- mercury_ai.analysis.evidence_query.EvidenceQuery
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS
- mercury_ai.models.confluence_score.ConfluenceScore
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_state_enum.MarketStateEnum


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
- dataclasses.replace
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
- logging
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
mercury_ai.analysis.decision_explainability
================================================================================

Classes
--------
- DecisionExplainability

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- mercury_ai.analysis.institutional_contribution.InstitutionalContribution
- typing.Tuple


================================================================================
mercury_ai.analysis.decision_resolver_engine
================================================================================

Classes
--------
- DecisionResolverEngine
- DecisionResolverResult

Funções
--------
- resolve

Imports
-------
- dataclasses.dataclass
- typing.Optional


================================================================================
mercury_ai.analysis.decision_result_builder
================================================================================

Classes
--------
- DecisionResultBuilder

Funções
--------
- build

Imports
-------
- hashlib
- mercury_ai.analysis.decision_explainability.DecisionExplainability
- mercury_ai.models.confidence_result.ConfidenceResult
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.decision_result.DecisionResult
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.probability_result.ProbabilityResult
- mercury_ai.models.trading_explanation.TradingExplanation
- mercury_ai.models.version_metadata.VersionMetadata
- typing.List
- typing.Optional
- typing.Tuple


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
- __init__
- cache
- replay_stats
- run_replay

Imports
-------
- mercury_ai.analysis.replay_cache.ReplayCache
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.database.replay_storage.ReplayStorage
- mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider
- mercury_ai.utils.deterministic_clock.DeterministicClock
- pandas
- time
- typing.Dict
- typing.List
- typing.Optional


================================================================================
mercury_ai.analysis.institutional_analytics_engine
================================================================================

Classes
--------
- InstitutionalAnalyticsEngine

Funções
--------
- __init__
- _attribution_analysis
- _confidence_analysis
- _engine_contribution
- _load_data
- _load_replay_metrics
- _max_consecutive
- _overview_stats
- _pattern_analysis
- _recent_trend
- _risk_metrics
- _temporal_analysis
- _win_rate_analysis
- export_report_json
- export_report_summary
- generate_quality_report

Imports
-------
- collections.defaultdict
- datetime.datetime
- datetime.timedelta
- json
- numpy
- os
- pandas
- typing.Any
- typing.Dict
- typing.List
- typing.Optional
- typing.Tuple


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
mercury_ai.analysis.institutional_contribution
================================================================================

Classes
--------
- InstitutionalContribution

Funções
--------
(nenhuma)

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
- __new__
- _get_setup_key
- _initialize_memory
- _load_into_cache
- _load_memory
- _save_memory
- flush
- get_consistency_score
- record_decision
- record_outcome

Imports
-------
- hashlib
- json
- logging
- mercury_ai.models.decision_snapshot.DecisionSnapshot
- os
- threading
- time


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
mercury_ai.analysis.institutional_score_engine
================================================================================

Classes
--------
- InstitutionalScoreEngine
- InstitutionalScoreResult

Funções
--------
- calculate

Imports
-------
- dataclasses.dataclass


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
- mercury_ai.models.trade_filter_result.TradeFilterResult
- typing.List


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
- is_running
- start
- stop

Imports
-------
- logging
- time


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
- build

Imports
-------
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.liquidity_profile.LiquidityProfile
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state.MarketStateEnum
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.price_action.PriceActionAnalysis
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
- typing.List


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
- mercury_ai.models.market_regime.MarketRegime
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
- _determine_trend
- analyze
- calculate_factor_alignment

Imports
-------
- dataclasses.replace
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
- mercury_ai.core.exceptions.MarketClosedException
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
- mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
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
mercury_ai.analysis.performance_engine
================================================================================

Classes
--------
- PerformanceEngine

Funções
--------
- __init__
- _calculate_drawdown
- _calculate_sharpe
- _calculate_sortino
- _empty_asset_performance
- calculate_asset_performance
- calculate_universe_performance

Imports
-------
- mercury_ai.analysis.historical_replay_engine.ReplayMetrics
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- numpy
- pandas
- typing.Dict
- typing.List
- typing.Tuple


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
- rank

Imports
-------
- mercury_ai.models.analysis_result.AnalysisResult
- typing.List


================================================================================
mercury_ai.analysis.replay_batch_processor
================================================================================

Classes
--------
- BatchReplayReport
- BatchReplayResult
- ReplayBatchProcessor

Funções
--------
- __init__
- _aggregate_cache_stats
- _run_single_symbol
- run_batch

Imports
-------
- concurrent.futures.ThreadPoolExecutor
- concurrent.futures.TimeoutError
- concurrent.futures.as_completed
- dataclasses.dataclass
- dataclasses.field
- logging
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine
- mercury_ai.analysis.performance_engine.PerformanceEngine
- mercury_ai.analysis.replay_cache.ReplayCache
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- pandas
- threading
- time
- typing.Dict
- typing.List
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.analysis.replay_cache
================================================================================

Classes
--------
- ReplayCache

Funções
--------
- __contains__
- __init__
- __len__
- clear
- get
- hit_rate
- put
- size
- stats

Imports
-------
- collections.OrderedDict
- threading
- typing.Any
- typing.Optional
- typing.Tuple


================================================================================
mercury_ai.analysis.risk_engine
================================================================================

Classes
--------
- RiskEngine

Funções
--------
- __init__
- _compute_correlation_matrix
- _compute_kelly
- _compute_stress_test
- _compute_var_cvar
- _pearson_correlation
- assess
- assess_simple

Imports
-------
- math
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.config.risk.KELLY_DEFAULT_PAYOFF
- mercury_ai.config.risk.KELLY_DEFAULT_WIN_RATE
- mercury_ai.config.risk.KELLY_MAX_FRACTION
- mercury_ai.config.risk.STRESS_SCENARIOS
- mercury_ai.config.risk.VAR_CONFIDENCE_95
- mercury_ai.config.risk.VAR_CONFIDENCE_99
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.liquidity_profile.LiquidityProfile
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state_enum.MarketStateEnum
- mercury_ai.models.market_structure.MarketStructure
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.price_action.PriceActionAnalysis
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
- typing.Dict
- typing.List
- typing.Optional
- typing.Tuple


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
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
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
- TestMercuryBenchmarkFramework

Funções
--------
- test_benchmark_framework_execution
- test_buy_and_hold_baseline
- test_enhanced_report_fields
- test_multiple_symbols
- test_quick_benchmark_compatibility
- test_statistical_test_result
- test_warm_cool_filter

Imports
-------
- mercury_ai.analysis.benchmark_framework.BuyAndHoldBaseline
- mercury_ai.analysis.benchmark_framework.EnhancedBenchmarkReport
- mercury_ai.analysis.benchmark_framework.MercuryBenchmarkFramework
- mercury_ai.analysis.benchmark_framework.StatisticalTestResult
- pytest


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
(nenhuma)

Imports
-------
- mercury_ai.analysis.context_engine.ContextEngine
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.liquidity_profile.LiquidityProfile
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state_enum.MarketStateEnum
- mercury_ai.models.market_structure.MarketStructure
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.price_action.PriceActionAnalysis
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
- unittest.mock.MagicMock
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
mercury_ai.analysis.tests.test_historical_replay_engine
================================================================================

Classes
--------
- TestHistoricalReplayEngineBasic
- TestHistoricalReplayEngineConstructor
- TestReplayCacheIntegration
- TestReplayEdgeCases
- TestSilentMode

Funções
--------
- sample_df
- test_cache_populated_after_run
- test_custom_cache
- test_default_cache
- test_different_symbols_separate_cache
- test_metrics_have_expected_fields
- test_n_candles_large
- test_replay_stats_after_insufficient_data
- test_replay_stats_initial
- test_run_replay_empty_dataframe
- test_run_replay_insufficient_data_returns_empty
- test_run_replay_returns_list
- test_run_replay_returns_replay_metrics
- test_run_replay_updates_stats
- test_second_run_uses_cache
- test_silent_mode_no_output
- test_verbose_mode_has_output

Imports
-------
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- mercury_ai.analysis.replay_cache.ReplayCache
- mercury_ai.database.replay_storage.ReplayMetrics
- numpy
- pandas
- pytest
- unittest.mock.MagicMock
- unittest.mock.PropertyMock
- unittest.mock.patch


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
mercury_ai.analysis.tests.test_replay_batch_processor
================================================================================

Classes
--------
- TestBatchProcessorErrorHandling
- TestBatchReplayReport
- TestBatchReplayResult
- TestCacheAggregation
- TestReplayBatchProcessorBasic

Funções
--------
- sample_data_map
- test_aggregate_cache_stats_present
- test_constructor
- test_constructor_defaults
- test_creation
- test_creation
- test_frozen
- test_frozen
- test_partial_failure_mixed_results
- test_run_batch_all_success_no_errors
- test_run_batch_empty_data_map
- test_run_batch_multiple_symbols
- test_run_batch_single_symbol
- test_successful_and_failed_counts
- test_symbol_error_is_captured
- test_total_wall_time
- test_with_error

Imports
-------
- mercury_ai.analysis.replay_batch_processor.BatchReplayReport
- mercury_ai.analysis.replay_batch_processor.BatchReplayResult
- mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- numpy
- pandas
- pytest
- unittest.mock.MagicMock
- unittest.mock.patch


================================================================================
mercury_ai.analysis.tests.test_replay_cache
================================================================================

Classes
--------
- TestCacheStats
- TestReplayCacheBasic
- TestReplayCacheEdgeCases
- TestReplayCacheLRU
- TestReplayCacheThreadSafety

Funções
--------
- put_entries
- reader
- test_clear_empty_cache
- test_clear_resets_stats
- test_concurrent_gets_and_puts
- test_concurrent_puts
- test_contains
- test_different_symbols_same_index
- test_evicts_oldest_when_full
- test_get_miss_returns_none
- test_get_refreshes_lru_order
- test_hit_rate
- test_hit_rate_all_hits
- test_hit_rate_zero_requests
- test_initial_stats
- test_large_number_of_entries
- test_len
- test_maxsize_one
- test_maxsize_zero_clamped_to_one
- test_negative_maxsize_clamped_to_one
- test_overwrite_existing_key
- test_put_and_get
- test_put_refreshes_lru_order
- test_same_symbol_different_index
- writer

Imports
-------
- mercury_ai.analysis.replay_cache.ReplayCache
- pytest
- threading


================================================================================
mercury_ai.analysis.tests.test_risk_engine
================================================================================

Classes
--------
- TestAssessIntegration
- TestCorrelationMatrix
- TestEdgeCases
- TestKellyCriterion
- TestPearsonCorrelation
- TestStressTesting
- TestVaRCVaR

Funções
--------
- engine
- mock_context
- mock_evidence_bundle
- sample_returns_negative
- sample_returns_normal
- sample_returns_positive
- test_assess_basic
- test_assess_bearish_trend
- test_assess_empty_evidence_bundle
- test_assess_full
- test_assess_no_volatility_evidence
- test_assess_risk_assessment_is_frozen
- test_assess_with_correlation
- test_assess_with_historical_returns
- test_assess_with_kelly_params
- test_assess_zero_atr
- test_assess_zero_price
- test_constant_vector
- test_correlation_empty_map
- test_correlation_insufficient_data
- test_correlation_single_asset
- test_correlation_three_assets
- test_correlation_two_assets_perfect_negative
- test_correlation_two_assets_perfect_positive
- test_correlation_unequal_lengths
- test_kelly_breakeven
- test_kelly_capped_at_max
- test_kelly_default_params
- test_kelly_extreme_values
- test_kelly_high_win_rate
- test_kelly_low_win_rate
- test_kelly_negative_win_rate_clamped
- test_kelly_win_rate_clamped
- test_kelly_zero_payoff
- test_no_correlation
- test_pearson_identical_vectors
- test_perfect_negative
- test_perfect_positive
- test_single_element
- test_stress_capped_at_80_percent
- test_stress_high_volatility
- test_stress_low_volatility
- test_stress_negative_volatility
- test_stress_normal_volatility
- test_stress_zero_volatility
- test_var_cvar_empty_returns
- test_var_cvar_insufficient_returns
- test_var_cvar_single_outlier
- test_var_cvar_with_negative_returns
- test_var_cvar_with_normal_returns
- test_var_cvar_with_positive_returns
- test_var_cvar_zero_variance

Imports
-------
- math
- mercury_ai.analysis.risk_engine.RiskEngine
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_structure.MarketStructure
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- pytest
- unittest.mock.MagicMock


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
- mercury_ai.models.analysis_result.AnalysisResult
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.direction.AnalysisDirection
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
- explain

Imports
-------
- mercury_ai.models.analysis_result.AnalysisResult


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
- logging
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
- mercury_ai.analysis.confluence_engine.ConfluenceEngine
- mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine
- mercury_ai.analysis.decision_explainability.DecisionExplainability
- mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine
- mercury_ai.analysis.decision_result_builder.DecisionResultBuilder
- mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
- mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine
- mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine
- mercury_ai.analysis.institutional_score_engine.InstitutionalScoreEngine
- mercury_ai.analysis.market_state_engine.MarketStateEngine
- mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder
- mercury_ai.analysis.narrative_engine.NarrativeEngine
- mercury_ai.analysis.risk_engine.RiskEngine
- mercury_ai.analysis.validation_engine.ValidationEngine
- mercury_ai.brain.probability_engine.ProbabilityEngine
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED
- mercury_ai.core.pipeline_executor.PipelineExecutor
- mercury_ai.core.pipeline_profiler.PipelineProfiler
- mercury_ai.models.confidence_result.ConfidenceResult
- mercury_ai.models.decision_result.DecisionResult
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.trade_filter_result.TradeFilterResult
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
- mercury_ai.models.market_context.MarketContext
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
- logging
- mercury_ai.analysis.notification_center.NotificationCenter
- mercury_ai.analysis.ranking_engine.RankingEngine
- mercury_ai.brain.institutional_brain.InstitutionalBrain
- mercury_ai.config.configuration_center.MercuryConfigCenter
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.core.asset_registry.AssetRegistry
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.providers.mercury_data_provider.MercuryDataProvider
- traceback


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
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.direction.AnalysisDirection
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
- mercury_ai.models.trade_filter_result.TradeFilterResult
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
- mercury_ai.models.liquidity_profile.LiquidityProfile
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_regime_enum.MarketRegimeEnum
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_state_enum.MarketStateEnum
- mercury_ai.models.market_structure.MarketStructure
- mercury_ai.models.mtf_consensus.MTFConsensus
- mercury_ai.models.price_action.PriceActionAnalysis
- mercury_ai.models.probability_result.ProbabilityResult
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
- mercury_ai.models.trade_filter_result.TradeFilterResult
- mercury_ai.models.trading_explanation.TradingExplanation
- pytest
- unittest.mock.MagicMock


================================================================================
mercury_ai.brain.tests.test_probability_engine
================================================================================

Classes
--------
(nenhuma)

Funções
--------
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
mercury_ai.config.__init__
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_NORMALIZED
- mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS_SUM


================================================================================
mercury_ai.config.assets
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.config.universe.ALL_SYMBOLS
- mercury_ai.config.universe.COMMODITY_SYMBOLS
- mercury_ai.config.universe.COMMODITY_UNIVERSE
- mercury_ai.config.universe.CRYPTO_SYMBOLS
- mercury_ai.config.universe.CRYPTO_UNIVERSE
- mercury_ai.config.universe.FOREX_SYMBOLS
- mercury_ai.config.universe.FOREX_UNIVERSE
- mercury_ai.config.universe.OPERATIONAL_UNIVERSE
- mercury_ai.config.universe.STOCK_SYMBOLS
- mercury_ai.config.universe.STOCK_UNIVERSE
- mercury_ai.config.universe.SUPPORTED_ASSETS
- mercury_ai.config.universe.UniverseAsset
- mercury_ai.config.universe.get_all_provider_symbols
- mercury_ai.config.universe.get_asset
- mercury_ai.config.universe.get_enabled_symbols
- mercury_ai.config.universe.universe_summary
- mercury_ai.config.universe.validate_symbol


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
mercury_ai.config.universe
================================================================================

Classes
--------
- UniverseAsset

Funções
--------
- get_all_provider_symbols
- get_asset
- get_enabled_symbols
- universe_summary
- validate_symbol

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Dict
- typing.List
- typing.Optional


================================================================================
mercury_ai.core._stage_builder
================================================================================

Classes
--------
- _StageBuilder

Funções
--------
- __init__
- duration
- memory_delta
- percentage_of

Imports
-------
- __future__.annotations
- typing.List


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
- logging
- mercury_ai.analysis.candlestick_engine.CandlestickEngine
- mercury_ai.analysis.confidence_engine.ConfidenceEngine
- mercury_ai.analysis.confluence_engine.ConfluenceEngine
- mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine
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
- mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder
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
- mercury_ai.models.risk_assessment.RiskAssessment
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
- datetime.timezone
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

Funções
--------
- __init__
- _finalize_stage
- end_pipeline
- end_stage
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
- mercury_ai.core._stage_builder._StageBuilder
- mercury_ai.models.profiler_models.PipelineProfile
- mercury_ai.models.profiler_models.StageProfile
- threading
- time
- tracemalloc


================================================================================
mercury_ai.core.project_state
================================================================================

Classes
--------
- ProjectState

Funções
--------
- __init__
- documents
- get
- has
- json
- metadata
- statistics
- summary

Imports
-------
- __future__.annotations
- json
- pathlib.Path
- typing.Any


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
- best_provider
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
- healthcheck
- list_providers
- market_status
- market_status
- market_status
- provider_status
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
- mercury_ai.providers.market_provider.MercuryDataProvider


================================================================================
mercury_ai.models.analysis_result
================================================================================

Classes
--------
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
- mercury_ai.models.candlestick_analysis.CandlestickAnalysis
- mercury_ai.models.confluence_result.ConfluenceResult
- mercury_ai.models.decision_result.DecisionResult
- mercury_ai.models.evidence.Evidence
- mercury_ai.models.evidence_ranking.EvidenceRankingResult
- mercury_ai.models.liquidity_result.LiquidityResult
- mercury_ai.models.market_condition.MarketCondition
- mercury_ai.models.market_context.MarketContext
- mercury_ai.models.market_data.MarketData
- mercury_ai.models.market_regime.MarketRegime
- mercury_ai.models.market_state.MarketState
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- mercury_ai.models.risk_assessment.RiskAssessment
- mercury_ai.models.session_analysis.SessionAnalysis
- mercury_ai.models.smart_money.SmartMoneyAnalysis
- mercury_ai.models.support_resistance.SupportResistanceAnalysis
- mercury_ai.models.volatility_analysis.VolatilityAnalysis
- mercury_ai.models.volume_analysis.VolumeAnalysis
- mercury_ai.utils.deterministic_clock.DeterministicClock
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
- mercury_ai.models.direction.AnalysisDirection
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
- mercury_ai.analysis.decision_explainability.DecisionExplainability
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
mercury_ai.models.direction
================================================================================

Classes
--------
- AnalysisDirection

Funções
--------
(nenhuma)

Imports
-------
- enum.Enum


================================================================================
mercury_ai.models.equity_metrics
================================================================================

Classes
--------
- AssetPerformance
- UniversePerformance

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- pandas
- typing.Dict
- typing.List
- typing.Optional
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
- dataclasses.field
- typing.Dict
- typing.Optional
- typing.Tuple


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
mercury_ai.models.trade_filter_result
================================================================================

Classes
--------
- TradeFilterResult

Funções
--------
(nenhuma)

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- typing.Tuple


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
- logging
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
- logging
- mercury_ai.config.universe.ALL_SYMBOLS
- mercury_ai.config.universe.CRYPTO_SYMBOLS
- mercury_ai.config.universe.FOREX_SYMBOLS
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
- set_data
- set_index
- source_name
- supports_market
- supports_symbol
- supports_timeframe

Imports
-------
- os
- pandas
- typing.Optional


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
- get_data
- get_history
- get_last_price
- health
- healthcheck
- is_available
- list_providers
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
mercury_ai.providers.mercury_data_provider
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- mercury_ai.providers.market_provider.MercuryDataProvider


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
- mercury_ai.providers.market_provider.MercuryDataProvider


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

Funções
--------
- __init__
- _finalize_metric
- _flatten_stages
- collect
- stage

Imports
-------
- contextlib.contextmanager
- gc
- mercury_ai.core._stage_builder._StageBuilder
- mercury_ai.models.performance.HotspotReport
- mercury_ai.models.performance.PipelineMetric
- mercury_ai.models.performance.StageMetric
- time
- tracemalloc
- typing.List
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
- time
- tracemalloc
- typing.Any
- typing.Callable
- typing.Dict


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


================================================================================
parity_check
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- pandas
- yfinance


================================================================================
resolve_merge_conflicts
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _has_real_markers
- main
- resolve_conflicts_in_file

Imports
-------
- glob
- os
- re


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
- generate_performance_report
- load_local_data
- run_institutional_replay

Imports
-------
- datetime.datetime
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- mercury_ai.analysis.performance_engine.PerformanceEngine
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- os
- pandas
- typing.Dict
- typing.List


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
scripts.generate_benchmark_framework
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- os


================================================================================
scripts.prepare_replay_data
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- download_and_save
- prepare_all_assets

Imports
-------
- argparse
- datetime.datetime
- datetime.timedelta
- mercury_ai.config.universe.ALL_SYMBOLS
- mercury_ai.config.universe.CRYPTO_SYMBOLS
- mercury_ai.config.universe.FOREX_SYMBOLS
- os
- pandas
- sys
- yfinance


================================================================================
scripts.run_replay_3500
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- datetime.datetime
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- mercury_ai.analysis.performance_engine.PerformanceEngine
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- os
- pandas
- sys
- time


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
test_bloco7_scenarios
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main
- run_all_scenarios
- validate_consistency

Imports
-------
- mercury_ai.analysis.decision_resolver_engine.DecisionResolverEngine
- mercury_ai.analysis.decision_resolver_engine.DecisionResolverResult
- os
- sys
- traceback


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
test_replay_quick
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- mercury_ai.analysis.performance_engine.PerformanceEngine
- mercury_ai.database.replay_storage.ReplayMetrics
- os
- pandas
- sys


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
- pathlib.Path
- pytest
- shutil


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
- mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider
- numpy
- pandas
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
tests.test_institutional_backtest
================================================================================

Classes
--------
- TestIntegrationBatchToUniverse
- TestIntegrationEndToEnd
- TestIntegrationExtremeScenarios
- TestIntegrationReplayToCache
- TestIntegrationReplayToMetrics
- TestIntegrationReplayToPerformance
- TestIntegrationRiskAndReplay

Funções
--------
- _make_multi_symbol_data
- _make_ohlcv_df
- build_data_symbol_data
- build_multi_symbol_data
- test_batch_produces_universe_performance
- test_batch_results_have_cache_stats
- test_cache_populated_after_replay
- test_flat_market
- test_full_pipeline_multi_symbol
- test_full_pipeline_single_symbol
- test_high_volatility
- test_performance_fields_are_finite
- test_performance_from_replay_metrics
- test_pipeline_with_risk_on_all_symbols
- test_replay_metrics_are_finite
- test_replay_produces_metrics
- test_replay_updates_stats
- test_risk_assessment_fields_are_finite
- test_risk_assessment_from_replay
- test_second_run_hits_cache
- test_single_candle_dataframe

Imports
-------
- math
- mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
- mercury_ai.analysis.performance_engine.PerformanceEngine
- mercury_ai.analysis.replay_batch_processor.BatchReplayReport
- mercury_ai.analysis.replay_batch_processor.BatchReplayResult
- mercury_ai.analysis.replay_batch_processor.ReplayBatchProcessor
- mercury_ai.analysis.replay_cache.ReplayCache
- mercury_ai.analysis.risk_engine.RiskEngine
- mercury_ai.database.replay_storage.ReplayMetrics
- mercury_ai.models.equity_metrics.AssetPerformance
- mercury_ai.models.equity_metrics.UniversePerformance
- mercury_ai.models.risk_assessment.RiskAssessment
- numpy
- pandas
- pytest
- time


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
- test_live_monitor_import
- test_live_monitor_instantiation

Imports
-------
- mercury_ai.analysis.live_monitor.LiveMonitor
- pytest


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
tests.test_performance_engine
================================================================================

Classes
--------
- TestPerformanceEngine

Funções
--------
- setUp
- test_asset_performance_basic
- test_calculate_drawdown
- test_calculate_sharpe
- test_calculate_sortino
- test_universe_performance

Imports
-------
- mercury_ai.analysis.historical_replay_engine.ReplayMetrics
- mercury_ai.analysis.performance_engine.PerformanceEngine
- numpy
- unittest


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
- json
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
tests.test_regression_sprint18
================================================================================

Classes
--------
- TestRegressionBug1MarketStructureProfileTrend
- TestRegressionBug2AnalysisPipelineInit
- TestRegressionBug3HistoricalReplayProvider

Funções
--------
- test_constructor_missing_providers_raises
- test_constructor_with_providers
- test_get_data_without_set_data
- test_set_data_and_set_index_workflow
- test_set_data_exists
- test_set_index_exists
- test_set_index_zero
- test_trend_field_bearish
- test_trend_field_custom_value
- test_trend_field_exists_default
- test_trend_field_is_frozen

Imports
-------
- mercury_ai.core.analysis_pipeline.AnalysisPipeline
- mercury_ai.data.market_data.MarketDataService
- mercury_ai.models.market_structure_profile.MarketStructureProfile
- mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider
- pandas
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
- mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider
- numpy
- pandas


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
tools.main
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- main

Imports
-------
- scanner.ProjectScanner
- writer.InventoryWriter


================================================================================
tools.mercury_integrity_auditor.auditors.__init__
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- .contract_auditor
- .coverage_auditor
- .decision_auditor
- .dependency_auditor
- .flow_auditor
- .integrity_auditor
- .masking_auditor
- .report
- .runtime_auditor
- .static_auditor
- .test_auditor


================================================================================
tools.mercury_integrity_auditor.auditors.backtest_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_data_leakage
- _check_execution_simulation
- _check_monte_carlo
- _check_out_of_sample
- _check_overfitting
- _check_performance_metrics
- _check_position_sizing_risk
- _check_survivorship_bias
- _check_transaction_costs
- _check_walk_forward
- run

Imports
-------
- pathlib.Path
- re
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.config.TESTS_DIR
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.contract_auditor
================================================================================

Classes
--------
- DataclassContractChecker

Funções
--------
- __init__
- run
- visit_ClassDef

Imports
-------
- ast
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.coverage_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _analyze_coverage_data
- _find_untested_modules
- _run_coverage
- run

Imports
-------
- json
- pathlib.Path
- subprocess
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.config.TESTS_DIR
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.data_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_data_drift_detection
- _check_data_lineage
- _check_data_schema_validation
- _check_missing_data_handling
- _check_pii_handling
- _check_train_test_leakage
- run

Imports
-------
- json
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.decision_auditor
================================================================================

Classes
--------
- DecisionPathAnalyzer

Funções
--------
- __init__
- _analyze_decision_file
- run
- visit_Call
- visit_If

Imports
-------
- ast
- json
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.dependency_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _collect_imports
- _get_installed_packages
- _parse_requirements
- run

Imports
-------
- ast
- importlib.metadata
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.determinism_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_deterministic_replay
- _check_environment_isolation
- _check_external_dependencies
- _check_fixed_seeds
- _check_floating_point
- _check_non_deterministic_ops
- run

Imports
-------
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.explainability_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_counterfactual_explanations
- _check_decision_logging
- _check_feature_importance
- _check_model_cards
- run

Imports
-------
- json
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.flow_auditor
================================================================================

Classes
--------
- ComponentChecker

Funções
--------
- __init__
- _find_class_in_project
- run
- visit_ClassDef
- visit_FunctionDef

Imports
-------
- ast
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.global_state_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_global_config
- _check_global_variables
- _check_runtime_state
- _check_singletons
- _check_state_persistence
- _check_thread_safety
- run

Imports
-------
- json
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.integrity_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_checksums
- _check_config_integrity
- _check_dot_mercury_integrity
- _check_models_integrity
- _check_runtime_reports_integrity
- run

Imports
-------
- hashlib
- json
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.DOT_MERCURY_DIR
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.masking_auditor
================================================================================

Classes
--------
- MaskingDetector

Funções
--------
- __init__
- run
- visit_Call
- visit_ExceptHandler
- visit_Import
- visit_ImportFrom

Imports
-------
- ast
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.performance_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_algorithmic_complexity
- _check_caching
- _check_critical_latency
- _check_database_performance
- _check_io_blocking
- _check_memory_usage
- _check_profiling_benchmarking
- _check_resource_utilization
- run

Imports
-------
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.report
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- generate_consolidated_metrics
- generate_executive_summary
- generate_html_report
- run
- save_all_reports

Imports
-------
- datetime.datetime
- json
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.AUDIT_OUTPUT_DIR
- tools.mercury_integrity_auditor.config.AUDIT_TIMESTAMP
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditReport
- tools.mercury_integrity_auditor.models.AuditSection
- typing.Any


================================================================================
tools.mercury_integrity_auditor.auditors.runtime_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- run

Imports
-------
- pathlib.Path
- subprocess
- sys
- time
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.static_auditor
================================================================================

Classes
--------
- StaticAnalyzer

Funções
--------
- __init__
- _count_lines
- _find_python_files
- _is_stub
- _parse_file
- run
- visit_AsyncFunctionDef
- visit_ClassDef
- visit_ExceptHandler
- visit_FunctionDef
- visit_Import
- visit_ImportFrom

Imports
-------
- ast
- os
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.test_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- run

Imports
-------
- pathlib.Path
- re
- subprocess
- sys
- time
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.auditors.universe_auditor
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- _check_corporate_actions
- _check_data_coverage
- _check_liquidity_filters
- _check_sector_diversification
- _check_universe_definition
- _check_universe_rebalancing
- run

Imports
-------
- pathlib.Path
- sys
- tools.mercury_integrity_auditor.config.CRITICAL
- tools.mercury_integrity_auditor.config.HIGH
- tools.mercury_integrity_auditor.config.LOW
- tools.mercury_integrity_auditor.config.MEDIUM
- tools.mercury_integrity_auditor.config.MERCURY_AI_DIR
- tools.mercury_integrity_auditor.config.PROJECT_ROOT
- tools.mercury_integrity_auditor.config.STATUS_FAIL
- tools.mercury_integrity_auditor.config.STATUS_INCONCLUSIVE
- tools.mercury_integrity_auditor.config.STATUS_INFO
- tools.mercury_integrity_auditor.config.STATUS_PASS
- tools.mercury_integrity_auditor.config.STATUS_WARNING
- tools.mercury_integrity_auditor.models.AuditFinding
- tools.mercury_integrity_auditor.models.AuditSection


================================================================================
tools.mercury_integrity_auditor.config
================================================================================

Classes
--------
(nenhuma)

Funções
--------
(nenhuma)

Imports
-------
- datetime.datetime
- os
- pathlib.Path
- sys


================================================================================
tools.mercury_integrity_auditor.main
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- compute_verdict
- ensure_output_dir
- generate_markdown_report
- main
- run_audit_phase

Imports
-------
- auditors.backtest_auditor
- auditors.contract_auditor
- auditors.coverage_auditor
- auditors.data_auditor
- auditors.decision_auditor
- auditors.dependency_auditor
- auditors.determinism_auditor
- auditors.explainability_auditor
- auditors.flow_auditor
- auditors.global_state_auditor
- auditors.integrity_auditor
- auditors.masking_auditor
- auditors.performance_auditor
- auditors.report
- auditors.runtime_auditor
- auditors.static_auditor
- auditors.test_auditor
- auditors.universe_auditor
- config.AUDIT_OUTPUT_DIR
- config.AUDIT_TIMESTAMP
- config.CRITICAL
- config.HIGH
- config.LOW
- config.MEDIUM
- config.MERCURY_AI_DIR
- config.PROJECT_ROOT
- config.REPORT_JSON
- config.REPORT_MD
- config.STATUS_FAIL
- config.STATUS_INCONCLUSIVE
- config.STATUS_INFO
- config.STATUS_PASS
- config.STATUS_WARNING
- config.TESTS_DIR
- json
- models.AuditFinding
- models.AuditReport
- models.AuditSection
- pathlib.Path
- subprocess
- sys
- time


================================================================================
tools.mercury_integrity_auditor.models
================================================================================

Classes
--------
- AuditFinding
- AuditReport
- AuditSection

Funções
--------
- fail_count
- inconclusive_count
- info_count
- pass_count
- total_critical
- total_fail
- total_findings
- total_pass
- total_warning
- warning_count

Imports
-------
- dataclasses.dataclass
- dataclasses.field
- datetime.datetime
- typing.Optional


================================================================================
tools.models
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
tools.scanner
================================================================================

Classes
--------
- ProjectScanner

Funções
--------
- scan

Imports
-------
- config.IGNORE_DIRS
- config.IGNORE_FILES
- config.PROJECT_ROOT
- config.SOURCE_EXTENSIONS
- models.FileInfo
- models.Inventory
- pathlib.Path


================================================================================
tools.writer
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
validate_universe_parity
================================================================================

Classes
--------
(nenhuma)

Funções
--------
- validate_universe

Imports
-------
- mercury_ai.config.universe.ALL_SYMBOLS
- yfinance


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

