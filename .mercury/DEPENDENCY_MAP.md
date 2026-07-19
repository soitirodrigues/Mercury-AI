# Mercury AI - Dependency Map

================================================================================
app.dashboard.asset_registry_panel
================================================================================
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider
 -> pandas
 -> streamlit

================================================================================
app.dashboard.dashboard
================================================================================
 -> app.ui_utils.apply_design_system
 -> app.ui_utils.display_metric
 -> mercury_ai.analysis.data_exporter.DataExporter
 -> mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator
 -> mercury_ai.analysis.notification_center.NotificationCenter
 -> mercury_ai.analysis.operational_history.OperationalHistory
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> mercury_ai.brain.scanner.Scanner
 -> mercury_ai.config.configuration_center.MercuryConfigCenter
 -> mercury_ai.config.settings
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys
 -> time

================================================================================
app.dashboard.health_center_panel
================================================================================
 -> mercury_ai.core.health_center.HealthCenter
 -> streamlit

================================================================================
app.dashboard.main_dashboard
================================================================================
 -> app.dashboard.asset_registry_panel.render_asset_registry_dashboard
 -> app.dashboard.health_center_panel.render_health_center_panel
 -> app.dashboard.market_map_panel.render_market_map_panel
 -> app.dashboard.observability_panel.render_observability_dashboard
 -> app.dashboard.provider_health_panel.render_provider_health_dashboard
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> mercury_ai.core.health_center.HealthCenter
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider
 -> streamlit

================================================================================
app.dashboard.market_map_panel
================================================================================
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> pandas
 -> plotly.express
 -> streamlit

================================================================================
app.dashboard.observability_panel
================================================================================
 -> mercury_ai.providers.manager.MercuryProviderManager
 -> psutil
 -> streamlit
 -> time

================================================================================
app.dashboard.operation_center
================================================================================
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> mercury_ai.analysis.integrity_checker.IntegrityChecker
 -> mercury_ai.analysis.operational_history.OperationalHistory
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> mercury_ai.brain.scanner.Scanner
 -> mercury_ai.config.settings
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys

================================================================================
app.dashboard.provider_health_panel
================================================================================
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider
 -> streamlit

================================================================================
app.launcher
================================================================================
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> os
 -> streamlit
 -> sys

================================================================================
app.terminal.pages.01_Scanner
================================================================================
 -> mercury_ai.brain.scanner.MercuryScanner
 -> mercury_ai.config.settings
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys
 -> time

================================================================================
app.terminal.pages.02_Dashboard
================================================================================
 -> mercury_ai.brain.scanner.Scanner
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys

================================================================================
app.terminal.pages.03_Historico_Estatisticas
================================================================================
 -> mercury_ai.analysis.operational_history.OperationalHistory
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys

================================================================================
app.terminal.pages.04_Auditoria_Configuracoes
================================================================================
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> mercury_ai.analysis.integrity_checker.IntegrityChecker
 -> mercury_ai.config.settings
 -> pathlib.Path
 -> streamlit
 -> sys

================================================================================
app.terminal.pages.05_Replay
================================================================================
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys

================================================================================
app.terminal.pages.06_Demo
================================================================================
 -> mercury_ai.analysis.operational_history.OperationalHistory
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> mercury_ai.config.assets.SUPPORTED_ASSETS
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> pandas
 -> pathlib.Path
 -> streamlit
 -> sys

================================================================================
app.terminal.pages.07_Observabilidade
================================================================================
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> mercury_ai.utils.system_monitor.SystemMonitor
 -> pandas
 -> streamlit
 -> time

================================================================================
app.terminal.terminal
================================================================================
 -> app.ui_utils.apply_design_system
 -> app.ui_utils.display_card
 -> app.ui_utils.display_status
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> mercury_ai.config.settings
 -> streamlit

================================================================================
app.ui_utils
================================================================================
 -> streamlit

================================================================================
calculate_institutional_stats
================================================================================
 -> json
 -> os
 -> pandas

================================================================================
main
================================================================================
 -> mercury_ai.brain.scanner.MercuryScanner

================================================================================
mercury_ai.ai.llm
================================================================================
 -> openai.OpenAI
 -> os

================================================================================
mercury_ai.analysis.adaptive_weight_engine
================================================================================
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum
 -> typing.Dict

================================================================================
mercury_ai.analysis.benchmark_framework
================================================================================
 -> mercury_ai.analysis.metric_calculator.MetricCalculator
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.models.benchmark_report.BenchmarkReport
 -> mercury_ai.models.benchmark_report.BenchmarkRunResult
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> os
 -> psutil
 -> time
 -> tracemalloc
 -> typing.List

================================================================================
mercury_ai.analysis.calibration_analyzer
================================================================================
 -> json
 -> os
 -> typing.Dict

================================================================================
mercury_ai.analysis.candlestick_engine
================================================================================
 -> mercury_ai.analysis.evidence_query.EvidenceQuery
 -> mercury_ai.core.base_engine.BaseEngine
 -> mercury_ai.core.base_engine.EngineResult
 -> mercury_ai.models.candlestick_analysis.CandlestickAnalysis
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_condition.MarketCondition
 -> mercury_ai.models.market_data.MarketData
 -> pandas
 -> time
 -> typing.List
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.analysis.confidence_calibration_auditor
================================================================================
 -> mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> numpy
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.confidence_engine
================================================================================
 -> mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
 -> mercury_ai.analysis.evidence_query.EvidenceQuery
 -> mercury_ai.models.confidence_result.ConfidenceResult
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.market_state_enum.MarketStateEnum

================================================================================
mercury_ai.analysis.conflict_resolution_engine
================================================================================
 -> dataclasses.replace
 -> mercury_ai.analysis.adaptive_weight_engine.AdaptiveWeightEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.confluence_engine
================================================================================
 -> mercury_ai.analysis.decision_trace_engine.DecisionTraceEngine
 -> mercury_ai.analysis.market_thesis_builder.MarketThesisBuilder
 -> mercury_ai.models.analysis_result.AnalysisDirection
 -> mercury_ai.models.confluence_result.ConfluenceResult
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle

================================================================================
mercury_ai.analysis.confluence_score_engine
================================================================================
 -> mercury_ai.analysis.evidence_query.EvidenceQuery
 -> mercury_ai.models.confluence_score.ConfluenceScore
 -> mercury_ai.models.market_context.MarketContext

================================================================================
mercury_ai.analysis.context_engine
================================================================================
 -> dataclasses.replace
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> typing.List

================================================================================
mercury_ai.analysis.context_intelligence_engine
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> typing.List

================================================================================
mercury_ai.analysis.data_exporter
================================================================================
 -> json
 -> mercury_ai.analysis.operational_history.OperationalHistory
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> pandas
 -> pathlib.Path
 -> typing.Any
 -> typing.Dict
 -> typing.List
 -> zipfile

================================================================================
mercury_ai.analysis.data_quality_engine
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> datetime.datetime
 -> numpy
 -> pandas
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.decision_trace_engine
================================================================================
 -> dataclasses.replace
 -> mercury_ai.models.decision_trace.DecisionNode
 -> mercury_ai.models.decision_trace.DecisionTrace

================================================================================
mercury_ai.analysis.engine_performance_auditor
================================================================================
 -> collections.defaultdict
 -> mercury_ai.analysis.performance_analytics.PerformanceAnalytics
 -> mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.evidence_engine
================================================================================
 -> dataclasses.replace
 -> mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
 -> mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.analysis.evidence_quality_engine
================================================================================
 -> dataclasses.replace
 -> mercury_ai.models.evidence.Evidence
 -> typing.List

================================================================================
mercury_ai.analysis.evidence_query
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> typing.List

================================================================================
mercury_ai.analysis.evidence_ranking_engine
================================================================================
 -> dataclasses.replace
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.evidence_ranking.EvidenceRankingResult
 -> typing.List

================================================================================
mercury_ai.analysis.fair_value_gap_engine
================================================================================
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis
 -> pandas
 -> typing.Optional

================================================================================
mercury_ai.analysis.health_auditor
================================================================================
 -> mercury_ai.analysis.confidence_engine.ConfidenceEngine
 -> mercury_ai.analysis.narrative_engine.NarrativeEngine
 -> mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
 -> mercury_ai.brain.probability_engine.ProbabilityEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> os
 -> pathlib.Path

================================================================================
mercury_ai.analysis.health_checker
================================================================================
 -> dataclasses.asdict
 -> dataclasses.dataclass
 -> mercury_ai.analysis.confidence_engine.ConfidenceEngine
 -> mercury_ai.analysis.narrative_engine.NarrativeEngine
 -> mercury_ai.analysis.operational_history.OperationalHistory
 -> mercury_ai.analysis.statistical_auditor.StatisticalAuditor
 -> mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
 -> mercury_ai.brain.probability_engine.ProbabilityEngine
 -> mercury_ai.config.settings
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> pathlib.Path
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.historical_replay_engine
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.database.replay_storage.ReplayMetrics
 -> mercury_ai.database.replay_storage.ReplayStorage
 -> mercury_ai.providers.historical_replay_provider.HistoricalReplayProvider
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> pandas

================================================================================
mercury_ai.analysis.institutional_analytics_engine
================================================================================
 -> json
 -> os
 -> pandas
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.institutional_context_builder
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.analysis.institutional_memory_engine
================================================================================
 -> hashlib
 -> json
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> os

================================================================================
mercury_ai.analysis.institutional_report
================================================================================
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> pytest
 -> subprocess

================================================================================
mercury_ai.analysis.institutional_report_generator
================================================================================
 -> mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor
 -> mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor
 -> mercury_ai.analysis.performance_analytics.PerformanceAnalytics
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.institutional_trade_filter_engine
================================================================================
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.integrity_checker
================================================================================
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> re
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.learning_engine
================================================================================
 -> collections.defaultdict
 -> json
 -> os
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.live_monitor
================================================================================
 -> mercury_ai.config.assets.SUPPORTED_ASSETS
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> time
 -> typing.List

================================================================================
mercury_ai.analysis.market_condition_engine
================================================================================
 -> mercury_ai.models.market_condition.MarketCondition
 -> mercury_ai.models.market_data.MarketData
 -> typing.List

================================================================================
mercury_ai.analysis.market_context_builder
================================================================================
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_state.MarketState
 -> mercury_ai.models.market_state.MarketStateEnum
 -> mercury_ai.models.mtf_consensus.MTFConsensus
 -> mercury_ai.models.risk_assessment.RiskAssessment

================================================================================
mercury_ai.analysis.market_regime_engine
================================================================================
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum

================================================================================
mercury_ai.analysis.market_state_engine
================================================================================
 -> mercury_ai.models.market_data.MarketData
 -> mercury_ai.models.market_state.MarketState
 -> mercury_ai.models.market_state_enum.MarketStateEnum
 -> mercury_ai.models.session_analysis.SessionAnalysis
 -> typing.Optional

================================================================================
mercury_ai.analysis.market_structure_intelligence_engine
================================================================================
 -> mercury_ai.analysis.swing_engine.SwingEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_structure_profile.MarketStructureProfile
 -> pandas
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.market_thesis_builder
================================================================================
 -> mercury_ai.analysis.confidence_engine.ConfidenceEngine
 -> mercury_ai.analysis.confluence_score_engine.ConfluenceScoreEngine
 -> mercury_ai.analysis.market_state_engine.MarketStateEngine
 -> mercury_ai.analysis.risk_engine.RiskEngine
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.market_thesis.MarketThesis

================================================================================
mercury_ai.analysis.metric_calculator
================================================================================
 -> dataclasses.dataclass
 -> numpy
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.momentum_engine
================================================================================
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.momentum_analysis.MomentumAnalysis
 -> pandas
 -> typing.Optional

================================================================================
mercury_ai.analysis.mtf_engine
================================================================================
 -> mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.analysis.trend_analyzer.TrendAnalyzer
 -> mercury_ai.analysis.volatility_engine.VolatilityEngine
 -> mercury_ai.config.timeframes.YFINANCE_INTERVALS
 -> mercury_ai.data.indicator_engine.IndicatorEngine
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_data.MarketData
 -> mercury_ai.models.mtf_consensus.MTFConsensus
 -> mercury_ai.providers.base_provider.MarketDataProvider
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.narrative_engine
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.trading_explanation.TradingExplanation
 -> typing.List

================================================================================
mercury_ai.analysis.notification_center
================================================================================
 -> csv
 -> dataclasses.dataclass
 -> dataclasses.field
 -> json
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.analysis.operational_history
================================================================================
 -> mercury_ai.analysis.performance_analytics.PerformanceAnalytics
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.performance_analytics
================================================================================
 -> datetime.datetime
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> pathlib.Path
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.performance_center
================================================================================
 -> collections.Counter
 -> mercury_ai.analysis.performance_analytics.PerformanceAnalytics
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> pandas
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.performance_statistics
================================================================================
 -> mercury_ai.analysis.performance_analytics.PerformanceAnalytics
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.post_decision_evaluation_engine
================================================================================
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> mercury_ai.models.performance_metrics.PerformanceMetrics
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.price_action_analyzer
================================================================================
 -> mercury_ai.models.price_action.PriceActionAnalysis

================================================================================
mercury_ai.analysis.price_action_engine
================================================================================
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.price_action_analysis.PriceActionAnalysis
 -> pandas
 -> typing.Optional

================================================================================
mercury_ai.analysis.provider_priority_engine
================================================================================
 -> logging
 -> mercury_ai.data.mercury_data_provider.IMercuryDataProvider
 -> mercury_ai.data.mercury_data_provider.MercuryDataProvider
 -> typing.Optional

================================================================================
mercury_ai.analysis.ranking_engine
================================================================================
 -> mercury_ai.models.analysis_result.AnalysisResult
 -> typing.List

================================================================================
mercury_ai.analysis.risk_engine
================================================================================
 -> mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.risk_assessment.RiskAssessment

================================================================================
mercury_ai.analysis.session_engine
================================================================================
 -> mercury_ai.config.sessions
 -> mercury_ai.models.session_analysis.SessionAnalysis
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.List

================================================================================
mercury_ai.analysis.smart_money.bos_engine
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.market_structure.MarketStructure

================================================================================
mercury_ai.analysis.smart_money.choch_engine
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.market_structure.MarketStructure

================================================================================
mercury_ai.analysis.smart_money.liquidity_engine
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.replace
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.liquidity_analysis.LiquidityAnalysis
 -> mercury_ai.models.liquidity_result.LiquidityResult
 -> mercury_ai.models.market_structure_profile.MarketStructureProfile
 -> mercury_ai.models.swing_analysis.Swing
 -> numpy
 -> pandas
 -> typing.List
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.analysis.smart_money.liquidity_event_engine
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.liquidity_event_enum.LiquidityEventType
 -> pandas
 -> typing.List

================================================================================
mercury_ai.analysis.smart_money.market_structure_engine
================================================================================
 -> mercury_ai.models.market_structure.MarketStructure
 -> pandas

================================================================================
mercury_ai.analysis.smart_money.order_block_engine
================================================================================
 -> pandas
 -> typing.Dict
 -> typing.Optional

================================================================================
mercury_ai.analysis.smart_money.smart_money_engine
================================================================================
 -> mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine
 -> mercury_ai.analysis.smart_money.bos_engine.BOSEngine
 -> mercury_ai.analysis.smart_money.choch_engine.CHOCHEngine
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.analysis.smart_money.market_structure_engine.MarketStructureEngine
 -> mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.smart_money.SmartMoneyAnalysis
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases
================================================================================
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.models.swing_analysis.Swing
 -> numpy
 -> pytest

================================================================================
mercury_ai.analysis.smart_money.tests.test_liquidity_engine
================================================================================
 -> mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup
 -> mercury_ai.analysis.smart_money.liquidity_engine.EqualHighMetrics
 -> mercury_ai.analysis.smart_money.liquidity_engine.EqualHighScore
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_structure_profile.MarketStructureProfile
 -> mercury_ai.models.swing_analysis.Swing
 -> pandas
 -> pytest
 -> random
 -> typing.List

================================================================================
mercury_ai.analysis.smart_money.tests.test_liquidity_stress
================================================================================
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.models.swing_analysis.Swing
 -> pytest
 -> random

================================================================================
mercury_ai.analysis.statistical_auditor
================================================================================
 -> collections.Counter
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.analysis.support_resistance_analyzer
================================================================================
 -> mercury_ai.models.support_resistance_analysis.SupportResistanceAnalysis
 -> numpy
 -> pandas
 -> ta.volatility.AverageTrueRange
 -> typing.List
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.analysis.swing_engine
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.swing_analysis.Swing
 -> mercury_ai.models.swing_analysis.SwingSequenceResult
 -> pandas
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.tests.test_benchmark_framework
================================================================================
 -> mercury_ai.analysis.benchmark_framework.MercuryBenchmarkFramework

================================================================================
mercury_ai.analysis.tests.test_candlestick_engine
================================================================================
 -> mercury_ai.analysis.candlestick_engine.CandlestickEngine
 -> mercury_ai.models.market_condition.MarketCondition
 -> mercury_ai.models.market_data.MarketData
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_context_engine
================================================================================
 -> mercury_ai.analysis.context_engine.ContextEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_data.MarketData
 -> unittest.mock.Mock

================================================================================
mercury_ai.analysis.tests.test_fvg_engine
================================================================================
 -> mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.fair_value_gap_analysis.FairValueGapAnalysis
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_market_regime_engine
================================================================================
 -> mercury_ai.analysis.market_regime_engine.MarketRegimeEngine
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum
 -> unittest.mock.MagicMock

================================================================================
mercury_ai.analysis.tests.test_market_structure_engine
================================================================================
 -> mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_momentum_engine
================================================================================
 -> mercury_ai.analysis.momentum_engine.MomentumEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.momentum_analysis.MomentumAnalysis
 -> numpy
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_price_action_engine
================================================================================
 -> mercury_ai.analysis.price_action_engine.PriceActionEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.price_action_analysis.PriceActionAnalysis
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_trend_engine
================================================================================
 -> mercury_ai.analysis.trend_analyzer.TrendAnalyzer
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_data.MarketData
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_volume_engine
================================================================================
 -> mercury_ai.analysis.volume_engine.VolumeEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.volume_analysis.VolumeAnalysis
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.tests.test_vwap_engine
================================================================================
 -> mercury_ai.analysis.vwap_engine.VWAPEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.vwap_analysis.VWAPAnalysis
 -> pandas
 -> pytest

================================================================================
mercury_ai.analysis.trade_memory_engine
================================================================================
 -> mercury_ai.models.trade_memory.TradeMemory
 -> os
 -> pandas
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.trade_outcome_engine
================================================================================
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.analysis.trend_analyzer
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_data.MarketData
 -> typing.List

================================================================================
mercury_ai.analysis.validation_engine
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> pandas
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.volatility_engine
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_data.MarketData
 -> mercury_ai.models.volatility_analysis.VolatilityAnalysis
 -> pandas
 -> ta.volatility.AverageTrueRange
 -> typing.List

================================================================================
mercury_ai.analysis.volume_engine
================================================================================
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.volume_analysis.VolumeAnalysis
 -> pandas
 -> typing.Optional

================================================================================
mercury_ai.analysis.volume_intelligence_engine
================================================================================
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.volume_profile.VolumeProfile
 -> pandas
 -> typing.List
 -> typing.Tuple

================================================================================
mercury_ai.analysis.vwap_engine
================================================================================
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.vwap_analysis.VWAPAnalysis
 -> pandas
 -> typing.Optional

================================================================================
mercury_ai.analysis.weight_simulator
================================================================================
 -> mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.brain.explainability_engine
================================================================================
 -> mercury_ai.models.analysis_result.AnalysisDirection
 -> mercury_ai.models.analysis_result.AnalysisResult
 -> mercury_ai.models.confluence_result.ConfluenceResult
 -> mercury_ai.models.probability_result.ProbabilityResult
 -> mercury_ai.models.trading_explanation.TradingExplanation
 -> typing.Tuple

================================================================================
mercury_ai.brain.institutional_brain
================================================================================
 -> mercury_ai.models.analysis_result.AnalysisResult
 -> mercury_ai.models.evidence.Evidence
 -> typing.List

================================================================================
mercury_ai.brain.mercury_decision_engine
================================================================================
 -> hashlib
 -> mercury_ai.analysis.confidence_engine.ConfidenceEngine
 -> mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
 -> mercury_ai.analysis.confluence_engine.ConfluenceEngine
 -> mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
 -> mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine
 -> mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine
 -> mercury_ai.analysis.narrative_engine.NarrativeEngine
 -> mercury_ai.analysis.validation_engine.ValidationEngine
 -> mercury_ai.brain.probability_engine.ProbabilityEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.decision_result.DecisionResult
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum
 -> mercury_ai.models.version_metadata.VersionMetadata
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.brain.probability_engine
================================================================================
 -> mercury_ai.models.probability_result.ProbabilityResult
 -> typing.Any
 -> typing.Dict
 -> typing.Optional

================================================================================
mercury_ai.brain.scanner
================================================================================
 -> mercury_ai.analysis.evidence_query.EvidenceQuery
 -> mercury_ai.analysis.notification_center.NotificationCenter
 -> mercury_ai.analysis.ranking_engine.RankingEngine
 -> mercury_ai.brain.institutional_brain.InstitutionalBrain
 -> mercury_ai.config.configuration_center.MercuryConfigCenter
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider

================================================================================
mercury_ai.brain.tests.test_explainability_engine
================================================================================
 -> mercury_ai.brain.explainability_engine.ExplainabilityEngine
 -> mercury_ai.models.analysis_result.AnalysisDirection
 -> mercury_ai.models.confluence_result.ConfluenceResult
 -> mercury_ai.models.probability_result.ProbabilityResult
 -> unittest.mock.MagicMock

================================================================================
mercury_ai.brain.tests.test_mercury_decision_benchmark
================================================================================
 -> mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.confidence_result.ConfidenceResult
 -> mercury_ai.models.data_quality_result.DataQualityResult
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.evidence_ranking.EvidenceRankingResult
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> time
 -> unittest.mock.MagicMock

================================================================================
mercury_ai.brain.tests.test_mercury_decision_engine
================================================================================
 -> mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.models.confidence_result.ConfidenceResult
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.evidence_ranking.EvidenceRankingResult
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.probability_result.ProbabilityResult
 -> mercury_ai.models.trading_explanation.TradingExplanation
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
mercury_ai.brain.tests.test_probability_engine
================================================================================
 -> mercury_ai.brain.probability_engine.ProbabilityEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
mercury_ai.calendar.economic_calendar
================================================================================
 -> datetime.datetime

================================================================================
mercury_ai.calendar.tests.test_economic_calendar
================================================================================
 -> mercury_ai.calendar.economic_calendar.EconomicCalendar

================================================================================
mercury_ai.config.configuration_center
================================================================================
 -> json
 -> mercury_ai.config.settings
 -> os

================================================================================
mercury_ai.core.analysis_pipeline
================================================================================
 -> dataclasses.replace
 -> json
 -> mercury_ai.analysis.candlestick_engine.CandlestickEngine
 -> mercury_ai.analysis.confluence_engine.ConfluenceEngine
 -> mercury_ai.analysis.context_engine.ContextEngine
 -> mercury_ai.analysis.context_intelligence_engine.ContextIntelligenceEngine
 -> mercury_ai.analysis.evidence_engine.EvidenceEngine
 -> mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
 -> mercury_ai.analysis.evidence_ranking_engine.EvidenceRankingEngine
 -> mercury_ai.analysis.fair_value_gap_engine.FairValueGapEngine
 -> mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine
 -> mercury_ai.analysis.institutional_trade_filter_engine.InstitutionalTradeFilterEngine
 -> mercury_ai.analysis.market_condition_engine.MarketConditionEngine
 -> mercury_ai.analysis.market_context_builder.MarketContextBuilder
 -> mercury_ai.analysis.market_regime_engine.MarketRegimeEngine
 -> mercury_ai.analysis.market_state_engine.MarketStateEngine
 -> mercury_ai.analysis.market_structure_intelligence_engine.MarketStructureIntelligenceEngine
 -> mercury_ai.analysis.mtf_engine.MTFEngine
 -> mercury_ai.analysis.price_action_analyzer.PriceActionAnalyzer
 -> mercury_ai.analysis.risk_engine.RiskEngine
 -> mercury_ai.analysis.session_engine.SessionEngine
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.analysis.smart_money.order_block_engine.OrderBlockEngine
 -> mercury_ai.analysis.smart_money.smart_money_engine.SmartMoneyEngine
 -> mercury_ai.analysis.support_resistance_analyzer.SupportResistanceAnalyzer
 -> mercury_ai.analysis.trend_analyzer.TrendAnalyzer
 -> mercury_ai.analysis.volatility_engine.VolatilityEngine
 -> mercury_ai.analysis.volume_intelligence_engine.VolumeIntelligenceEngine
 -> mercury_ai.brain.mercury_decision_engine.MercuryDecisionEngine
 -> mercury_ai.config.timeframes.DEFAULT_TIMEFRAME
 -> mercury_ai.core.exceptions.MarketClosedException
 -> mercury_ai.core.pipeline_executor.PipelineExecutor
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.core.runtime_report.RuntimeReport
 -> mercury_ai.core.runtime_report.TelemetryData
 -> mercury_ai.data.data_quality_engine.DataQualityEngine
 -> mercury_ai.data.indicator_engine.IndicatorEngine
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.database.snapshot_logger.DecisionSnapshotLogger
 -> mercury_ai.models.analysis_result.AnalysisResult
 -> mercury_ai.models.decision_result.DecisionResult
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> mercury_ai.models.market_data.MarketData
 -> mercury_ai.models.version_metadata.VersionMetadata
 -> mercury_ai.providers.base_provider.MarketDataProvider
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.Dict
 -> typing.List
 -> typing.Optional
 -> uuid

================================================================================
mercury_ai.core.asset_registry
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> json
 -> os
 -> time
 -> typing.Dict
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.core.audit_sink
================================================================================
 -> abc.ABC
 -> abc.abstractmethod
 -> dataclasses.dataclass
 -> typing.List

================================================================================
mercury_ai.core.auto_health
================================================================================
 -> logging
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> mercury_ai.core.health_center.HealthCenter
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider
 -> os

================================================================================
mercury_ai.core.base_engine
================================================================================
 -> abc.ABC
 -> abc.abstractmethod
 -> dataclasses.dataclass
 -> typing.Tuple

================================================================================
mercury_ai.core.data_quality_gate
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.core.export_center
================================================================================
 -> json
 -> mercury_ai.analysis.data_exporter.DataExporter
 -> os
 -> pandas
 -> pathlib.Path
 -> typing.Any
 -> typing.Callable
 -> typing.Dict
 -> typing.List
 -> typing.Optional
 -> zipfile

================================================================================
mercury_ai.core.health_center
================================================================================
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider
 -> psutil
 -> time
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.core.job_manager
================================================================================
 -> mercury_ai.analysis.health_checker.HealthChecker
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics
 -> mercury_ai.config.assets.SUPPORTED_ASSETS
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> threading
 -> time
 -> typing.Any
 -> typing.Dict
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.core.observability_center
================================================================================
 -> psutil
 -> time
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.core.pipeline_audit_middleware
================================================================================
 -> datetime.datetime
 -> mercury_ai.core.audit_sink.AuditEvent
 -> mercury_ai.core.audit_sink.AuditSink
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> typing.Any
 -> typing.Callable

================================================================================
mercury_ai.core.pipeline_executor
================================================================================
 -> contextlib.nullcontext
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> typing.Any
 -> typing.Callable
 -> typing.Dict
 -> typing.List
 -> typing.Optional
 -> typing.Type

================================================================================
mercury_ai.core.pipeline_profiler
================================================================================
 -> contextlib.contextmanager
 -> dataclasses.asdict
 -> gc
 -> json
 -> mercury_ai.models.profiler_models.PipelineProfile
 -> mercury_ai.models.profiler_models.StageProfile
 -> threading
 -> time
 -> tracemalloc
 -> typing.List

================================================================================
mercury_ai.core.runtime_report
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Any
 -> typing.Dict
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.core.security_center
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> json
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.core.session_manager
================================================================================
 -> mercury_ai.config.settings
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> uuid

================================================================================
mercury_ai.core.startup
================================================================================
 -> mercury_ai.config.settings
 -> mercury_ai.core.banner.show_banner
 -> mercury_ai.providers.provider.MarketProvider

================================================================================
mercury_ai.data.data_normalizer
================================================================================
 -> pandas

================================================================================
mercury_ai.data.data_quality_engine
================================================================================
 -> pandas
 -> typing.Tuple

================================================================================
mercury_ai.data.indicator_engine
================================================================================
 -> numpy
 -> pandas

================================================================================
mercury_ai.data.market_data
================================================================================
 -> mercury_ai.core.exceptions.MarketClosedException
 -> mercury_ai.data.data_normalizer.DataNormalizer
 -> pandas
 -> typing.List

================================================================================
mercury_ai.data.market_data_provider
================================================================================
 -> pandas
 -> typing.Protocol

================================================================================
mercury_ai.data.mercury_data_provider
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> enum.Enum
 -> functools.lru_cache
 -> logging
 -> pandas
 -> time
 -> typing.Any
 -> typing.Dict
 -> typing.List
 -> typing.Optional
 -> typing.Protocol

================================================================================
mercury_ai.data.providers.historical_data_provider
================================================================================
 -> pandas

================================================================================
mercury_ai.data.replay_data_provider
================================================================================
 -> os
 -> pandas

================================================================================
mercury_ai.database.history_logger
================================================================================
 -> csv
 -> datetime.datetime
 -> pathlib.Path

================================================================================
mercury_ai.database.replay_storage
================================================================================
 -> dataclasses.dataclass
 -> json
 -> os
 -> typing.Any

================================================================================
mercury_ai.database.snapshot_logger
================================================================================
 -> dataclasses.asdict
 -> functools.lru_cache
 -> json
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> pathlib.Path
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.main
================================================================================
 -> mercury_ai.brain.scanner.MercuryScanner

================================================================================
mercury_ai.market.market_engine
================================================================================
 -> mercury_ai.config.settings.ASSET
 -> mercury_ai.providers.market_provider.MarketProvider

================================================================================
mercury_ai.models.analysis_result
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> enum.Enum
 -> mercury_ai.config.settings
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_data.MarketData
 -> mercury_ai.models.smart_money.SmartMoneyAnalysis
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.Any
 -> typing.List

================================================================================
mercury_ai.models.benchmark_report
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.analysis.metric_calculator.PerformanceMetrics
 -> mercury_ai.models.decision_result.DecisionResult
 -> typing.Tuple

================================================================================
mercury_ai.models.candlestick_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.models.confidence_result
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.confluence_result
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.analysis_result.AnalysisDirection
 -> typing.Any
 -> typing.Tuple

================================================================================
mercury_ai.models.confluence_score
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.data_quality_result
================================================================================
 -> dataclasses.dataclass
 -> typing.Tuple

================================================================================
mercury_ai.models.decision_input
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.List

================================================================================
mercury_ai.models.decision_node
================================================================================
 -> dataclasses.dataclass
 -> typing.Optional

================================================================================
mercury_ai.models.decision_outcome
================================================================================
 -> dataclasses.dataclass
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.models.decision_result
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.decision_trace.DecisionTrace
 -> mercury_ai.models.evidence_ranking.EvidenceRankingResult
 -> mercury_ai.models.market_regime.MarketRegime
 -> mercury_ai.models.mtf_consensus.MTFConsensus
 -> mercury_ai.models.trading_explanation.TradingExplanation
 -> mercury_ai.models.version_metadata.VersionMetadata
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.models.decision_snapshot
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.config.settings
 -> mercury_ai.models.decision_result.DecisionResult
 -> mercury_ai.models.evidence_ranking.EvidenceRankingResult
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.version_metadata.VersionMetadata
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.models.decision_trace
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.decision_node.DecisionNode
 -> typing.Tuple

================================================================================
mercury_ai.models.evidence
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.config.timeframes.DEFAULT_TIMEFRAME
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.models.evidence_ranking
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.evidence.Evidence
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.models.fair_value_gap_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.evidence.Evidence
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.models.liquidity_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.evidence.Evidence
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.models.liquidity_event_enum
================================================================================
 -> enum.Enum

================================================================================
mercury_ai.models.liquidity_profile
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.liquidity_result
================================================================================
 -> dataclasses.dataclass
 -> typing.Any
 -> typing.Tuple

================================================================================
mercury_ai.models.market_condition
================================================================================
 -> dataclasses.dataclass
 -> typing.Optional

================================================================================
mercury_ai.models.market_context
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.liquidity_profile.LiquidityProfile
 -> mercury_ai.models.market_data.MarketData
 -> mercury_ai.models.market_regime.MarketRegime
 -> mercury_ai.models.market_state.MarketState
 -> mercury_ai.models.mtf_consensus.MTFConsensus
 -> mercury_ai.models.price_action.PriceActionAnalysis
 -> mercury_ai.models.risk_assessment.RiskAssessment
 -> mercury_ai.models.smart_money.SmartMoneyAnalysis
 -> mercury_ai.models.support_resistance.SupportResistanceAnalysis
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.models.market_data
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.market_evidence_bundle
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.evidence.Evidence
 -> typing.Tuple

================================================================================
mercury_ai.models.market_regime
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum
 -> typing.List

================================================================================
mercury_ai.models.market_regime_enum
================================================================================
 -> enum.Enum

================================================================================
mercury_ai.models.market_state
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.market_state_enum.MarketStateEnum

================================================================================
mercury_ai.models.market_state_enum
================================================================================
 -> enum.Enum

================================================================================
mercury_ai.models.market_structure
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field

================================================================================
mercury_ai.models.market_structure_profile
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.swing_analysis.Swing
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.models.market_thesis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.confidence_result.ConfidenceResult
 -> mercury_ai.models.market_state.MarketState
 -> mercury_ai.models.risk_assessment.RiskAssessment
 -> typing.List

================================================================================
mercury_ai.models.memory_audit
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> time
 -> tracemalloc
 -> typing.List

================================================================================
mercury_ai.models.momentum_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.evidence.Evidence
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.models.mtf_consensus
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.performance
================================================================================
 -> dataclasses.dataclass
 -> typing.Tuple

================================================================================
mercury_ai.models.performance_metrics
================================================================================
 -> dataclasses.dataclass
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.models.price_action
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.price_action_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.models.probability_result
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Any
 -> typing.Dict

================================================================================
mercury_ai.models.professional_thesis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.models.profiler_models
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Tuple

================================================================================
mercury_ai.models.regression
================================================================================
 -> dataclasses.dataclass
 -> typing.Any

================================================================================
mercury_ai.models.risk_assessment
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.session_analysis
================================================================================
 -> dataclasses.dataclass
 -> typing.Optional

================================================================================
mercury_ai.models.signal
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.config.timeframes.DEFAULT_TIMEFRAME
 -> typing.List

================================================================================
mercury_ai.models.smart_money
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.market_structure.MarketStructure

================================================================================
mercury_ai.models.stress_test
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.market_data.MarketData
 -> typing.List

================================================================================
mercury_ai.models.support_resistance
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.support_resistance_analysis
================================================================================
 -> dataclasses.dataclass
 -> typing.Optional

================================================================================
mercury_ai.models.swing_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.models.trade_memory
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.models.trade_permission
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Optional

================================================================================
mercury_ai.models.trading_explanation
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.decision_result.DecisionResult
 -> typing.Any
 -> typing.Dict
 -> typing.TYPE_CHECKING
 -> typing.Tuple

================================================================================
mercury_ai.models.trend_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.models.version_metadata
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.volatility_analysis
================================================================================
 -> dataclasses.dataclass
 -> mercury_ai.models.evidence.Evidence
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.models.volume_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.evidence.Evidence
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.models.volume_profile
================================================================================
 -> dataclasses.dataclass

================================================================================
mercury_ai.models.vwap_analysis
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field
 -> mercury_ai.models.evidence.Evidence
 -> typing.Any
 -> typing.Dict
 -> typing.Tuple

================================================================================
mercury_ai.news.news_provider
================================================================================
 -> datetime.datetime

================================================================================
mercury_ai.news.tests.test_news_provider
================================================================================
 -> mercury_ai.news.news_provider.NewsProvider

================================================================================
mercury_ai.operations.demo_manager
================================================================================
 -> mercury_ai.config.assets.SUPPORTED_ASSETS
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> mercury_ai.utils.deterministic_clock.DeterministicClock
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.providers.base_provider
================================================================================
 -> pandas
 -> typing.Protocol

================================================================================
mercury_ai.providers.data_adapters
================================================================================
 -> mercury_ai.providers.data_interfaces.IDataProvider
 -> pandas
 -> yfinance

================================================================================
mercury_ai.providers.data_interfaces
================================================================================
 -> pandas
 -> typing.List
 -> typing.Protocol

================================================================================
mercury_ai.providers.historical_replay_provider
================================================================================
 -> mercury_ai.providers.base_provider.MarketDataProvider
 -> os
 -> pandas

================================================================================
mercury_ai.providers.market_provider
================================================================================
 -> functools.lru_cache
 -> logging
 -> mercury_ai.providers.data_adapters.AlphaVantageAdapter
 -> mercury_ai.providers.data_adapters.BinanceAdapter
 -> mercury_ai.providers.data_adapters.MetaTrader5Adapter
 -> mercury_ai.providers.data_adapters.PolygonAdapter
 -> mercury_ai.providers.data_adapters.TwelveDataAdapter
 -> mercury_ai.providers.data_adapters.YahooAdapter
 -> mercury_ai.providers.data_interfaces.IDataProvider
 -> pandas
 -> time
 -> typing.Dict

================================================================================
mercury_ai.providers.mercury_data_provider
================================================================================
 -> functools.lru_cache
 -> logging
 -> mercury_ai.providers.data_adapters.AlphaVantageAdapter
 -> mercury_ai.providers.data_adapters.BinanceAdapter
 -> mercury_ai.providers.data_adapters.MetaTrader5Adapter
 -> mercury_ai.providers.data_adapters.PolygonAdapter
 -> mercury_ai.providers.data_adapters.TwelveDataAdapter
 -> mercury_ai.providers.data_adapters.YahooAdapter
 -> mercury_ai.providers.data_interfaces.IDataProvider
 -> pandas
 -> time
 -> typing.Dict

================================================================================
mercury_ai.providers.tests.test_market_provider
================================================================================
 -> mercury_ai.providers.market_provider.MarketProvider

================================================================================
mercury_ai.providers.yahoo_finance_provider
================================================================================
 -> mercury_ai.core.exceptions.MarketClosedException
 -> mercury_ai.providers.base_provider.MarketDataProvider
 -> pandas
 -> yfinance

================================================================================
mercury_ai.sessions.market_sessions
================================================================================
 -> datetime.datetime
 -> mercury_ai.config.sessions

================================================================================
mercury_ai.sessions.tests.test_market_sessions
================================================================================
 -> mercury_ai.sessions.market_sessions.MarketSessions

================================================================================
mercury_ai.utils.deterministic_clock
================================================================================
 -> datetime.datetime
 -> datetime.timezone

================================================================================
mercury_ai.utils.memory_auditor
================================================================================
 -> gc
 -> mercury_ai.models.memory_audit.MemoryAuditResult
 -> mercury_ai.models.memory_audit.MemorySnapshot
 -> tracemalloc
 -> typing.Optional

================================================================================
mercury_ai.utils.performance_collector
================================================================================
 -> contextlib.contextmanager
 -> gc
 -> mercury_ai.models.performance.HotspotReport
 -> mercury_ai.models.performance.PipelineMetric
 -> mercury_ai.models.performance.StageMetric
 -> statistics
 -> time
 -> tracemalloc
 -> typing.List
 -> typing.Optional
 -> typing.Tuple

================================================================================
mercury_ai.utils.regression_detector
================================================================================
 -> json
 -> mercury_ai.models.regression.BenchmarkMetrics
 -> mercury_ai.models.regression.RegressionResult
 -> typing.Dict
 -> typing.List
 -> typing.Optional

================================================================================
mercury_ai.utils.report_generator
================================================================================
 -> csv
 -> datetime
 -> json
 -> mercury_ai.models.performance.PipelineMetric
 -> mercury_ai.models.regression.RegressionResult
 -> mercury_ai.models.stress_test.StressTestResult
 -> platform
 -> sys
 -> typing.Any
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.utils.stress_tester
================================================================================
 -> mercury_ai.models.stress_test.StressTestResult
 -> random
 -> time
 -> tracemalloc
 -> typing.Any
 -> typing.Callable
 -> typing.Dict
 -> typing.List

================================================================================
mercury_ai.utils.system_monitor
================================================================================
 -> psutil
 -> time

================================================================================
run_deterministic_replay_scenarios
================================================================================
 -> mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
 -> numpy
 -> pandas

================================================================================
run_institutional_replay
================================================================================
 -> mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
 -> os
 -> pandas

================================================================================
run_instrumented
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> pandas

================================================================================
stress_test_replay
================================================================================
 -> mercury_ai.analysis.historical_replay_engine.HistoricalReplayEngine
 -> numpy
 -> os
 -> pandas
 -> shutil
 -> time
 -> tracemalloc

================================================================================
test_mercury_signal
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.presentation.signal_formatter.SignalFormatter
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider

================================================================================
teste_gemini
================================================================================
 -> google.genai
 -> os

================================================================================
teste_llm
================================================================================
 -> openai.OpenAI
 -> os

================================================================================
teste_openrouter
================================================================================
 -> openai.OpenAI
 -> os

================================================================================
tests.test_adaptive_weighting
================================================================================
 -> mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_regime.MarketRegime
 -> mercury_ai.models.market_regime_enum.MarketRegimeEnum
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_asset_registry
================================================================================
 -> json
 -> mercury_ai.brain.scanner.MercuryScanner
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> os
 -> pytest

================================================================================
tests.test_auto_health
================================================================================
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> mercury_ai.core.auto_health.MercuryAutoHealth
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProvider
 -> pytest

================================================================================
tests.test_benchmark_integration
================================================================================
 -> mercury_ai.analysis.smart_money.liquidity_engine.EqualHighGroup
 -> mercury_ai.analysis.smart_money.liquidity_engine.LiquidityEngine
 -> mercury_ai.core.pipeline_profiler.PipelineProfiler
 -> mercury_ai.models.market_structure_profile.MarketStructureProfile
 -> mercury_ai.models.swing_analysis.Swing
 -> pandas
 -> pytest
 -> typing.List
 -> typing.Tuple

================================================================================
tests.test_broker_filtering
================================================================================
 -> json
 -> mercury_ai.brain.scanner.MercuryScanner
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> os
 -> pytest

================================================================================
tests.test_confidence_calibration
================================================================================
 -> mercury_ai.analysis.confidence_engine.ConfidenceEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> mercury_ai.models.market_state.MarketState
 -> mercury_ai.models.market_state_enum.MarketStateEnum
 -> mercury_ai.models.mtf_consensus.MTFConsensus
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_confidence_calibration_auditor
================================================================================
 -> mercury_ai.analysis.confidence_calibration_auditor.ConfidenceCalibrationAuditor

================================================================================
tests.test_configuration_center
================================================================================
 -> mercury_ai.config.configuration_center.MercuryConfigCenter
 -> os
 -> pytest

================================================================================
tests.test_conflict_resolution
================================================================================
 -> mercury_ai.analysis.conflict_resolution_engine.ConflictResolutionEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_data_exporter
================================================================================
 -> mercury_ai.analysis.data_exporter.DataExporter
 -> pathlib.Path
 -> shutil

================================================================================
tests.test_data_provider_manager
================================================================================
 -> mercury_ai.data.mercury_data_provider.BinanceProvider
 -> mercury_ai.data.mercury_data_provider.MercuryDataProvider
 -> mercury_ai.data.mercury_data_provider.YahooProvider
 -> pytest

================================================================================
tests.test_data_quality_engine
================================================================================
 -> mercury_ai.analysis.data_quality_engine.DataQualityEngine
 -> numpy
 -> pandas
 -> pytest

================================================================================
tests.test_demo_operations
================================================================================
 -> mercury_ai.operations.demo_manager.DemoOperationsManager

================================================================================
tests.test_demo_page
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

================================================================================
tests.test_determinism
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> pytest

================================================================================
tests.test_engine_performance_auditor
================================================================================
 -> mercury_ai.analysis.engine_performance_auditor.EnginePerformanceAuditor

================================================================================
tests.test_evidence_engine
================================================================================
 -> mercury_ai.analysis.evidence_engine.EvidenceEngine
 -> mercury_ai.models.evidence.Evidence
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_evidence_quality_engine
================================================================================
 -> mercury_ai.analysis.evidence_quality_engine.EvidenceQualityEngine
 -> mercury_ai.models.evidence.Evidence
 -> pytest

================================================================================
tests.test_export_center
================================================================================
 -> json
 -> mercury_ai.core.export_center.ExportCenter
 -> os
 -> pandas
 -> pytest

================================================================================
tests.test_health_auditor
================================================================================
 -> mercury_ai.analysis.health_auditor.HealthAuditor

================================================================================
tests.test_health_center
================================================================================
 -> app.dashboard.health_center_panel.render_health_center_panel
 -> mercury_ai.core.health_center.HealthCenter
 -> mercury_ai.providers.mercury_data_provider.MercuryDataProviderManager
 -> pytest

================================================================================
tests.test_health_checker
================================================================================
 -> mercury_ai.analysis.health_checker.HealthChecker

================================================================================
tests.test_institutional_report_generator
================================================================================
 -> mercury_ai.analysis.institutional_report_generator.InstitutionalReportGenerator

================================================================================
tests.test_integrity_checker
================================================================================
 -> mercury_ai.analysis.integrity_checker.IntegrityChecker

================================================================================
tests.test_job_manager
================================================================================
 -> mercury_ai.core.job_manager.JobManager
 -> time

================================================================================
tests.test_live_monitor
================================================================================
 -> mercury_ai.analysis.live_monitor.LiveMonitor

================================================================================
tests.test_main_dashboard
================================================================================
 -> app.dashboard.main_dashboard.main
 -> pytest

================================================================================
tests.test_market_resilience
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.core.exceptions.MarketClosedException
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
 -> pandas
 -> pytest
 -> unittest.mock.MagicMock
 -> yfinance

================================================================================
tests.test_notification_center
================================================================================
 -> mercury_ai.analysis.notification_center.NotificationCenter
 -> os
 -> pytest

================================================================================
tests.test_observability_center
================================================================================
 -> mercury_ai.core.observability_center.ObservabilityCenter
 -> pytest

================================================================================
tests.test_observability_panel
================================================================================
 -> app.dashboard.observability_panel.render_observability_dashboard
 -> pytest

================================================================================
tests.test_operational_history
================================================================================
 -> mercury_ai.analysis.operational_history.OperationalHistory

================================================================================
tests.test_performance_analytics
================================================================================
 -> mercury_ai.analysis.performance_analytics.PerformanceAnalytics

================================================================================
tests.test_performance_center
================================================================================
 -> mercury_ai.analysis.performance_center.PerformanceCenter

================================================================================
tests.test_performance_collector
================================================================================
 -> mercury_ai.utils.performance_collector.PerformanceCollector
 -> pytest
 -> time

================================================================================
tests.test_performance_statistics
================================================================================
 -> mercury_ai.analysis.performance_statistics.PerformanceStatistics

================================================================================
tests.test_pipeline_persistence
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.data.providers.historical_data_provider.HistoricalDataProvider
 -> numpy
 -> pandas
 -> pathlib.Path
 -> pytest
 -> shutil

================================================================================
tests.test_probability_engine
================================================================================
 -> mercury_ai.brain.probability_engine.ProbabilityEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_provider_priority_engine
================================================================================
 -> mercury_ai.analysis.provider_priority_engine.ProviderPriorityEngine
 -> mercury_ai.data.mercury_data_provider.AlphaVantageProvider
 -> mercury_ai.data.mercury_data_provider.BinanceProvider
 -> mercury_ai.data.mercury_data_provider.MercuryDataProvider
 -> mercury_ai.data.mercury_data_provider.MetaTrader5Provider
 -> mercury_ai.data.mercury_data_provider.PolygonProvider
 -> mercury_ai.data.mercury_data_provider.TwelveDataProvider
 -> mercury_ai.data.mercury_data_provider.YahooProvider
 -> pytest

================================================================================
tests.test_read_only
================================================================================
 -> mercury_ai.core.read_only.ReadOnlyViolation
 -> mercury_ai.core.read_only.check_read_only
 -> pytest

================================================================================
tests.test_robustness
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.data.market_data_provider.MarketDataProvider
 -> numpy
 -> pandas
 -> pytest
 -> typing.List

================================================================================
tests.test_scanner_priority
================================================================================
 -> mercury_ai.brain.scanner.MercuryScanner
 -> mercury_ai.core.asset_registry.AssetRegistry
 -> pytest

================================================================================
tests.test_scanner_recovery
================================================================================
 -> mercury_ai.brain.scanner.MercuryScanner
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_security_center
================================================================================
 -> mercury_ai.core.security_center.SecurityCenter
 -> pytest

================================================================================
tests.test_session_id
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider

================================================================================
tests.test_session_manager
================================================================================
 -> mercury_ai.core.session_manager.SessionManager

================================================================================
tests.test_statistical_auditor
================================================================================
 -> mercury_ai.analysis.statistical_auditor.StatisticalAuditor

================================================================================
tests.test_trade_outcome_engine
================================================================================
 -> mercury_ai.analysis.trade_outcome_engine.TradeOutcomeEngine

================================================================================
tests.test_validation_engine
================================================================================
 -> mercury_ai.analysis.validation_engine.ValidationEngine
 -> mercury_ai.models.evidence.Evidence
 -> mercury_ai.models.market_context.MarketContext
 -> mercury_ai.models.market_evidence_bundle.MarketEvidenceBundle
 -> pytest
 -> unittest.mock.MagicMock

================================================================================
tests.test_versioning
================================================================================
 -> mercury_ai.config.settings
 -> mercury_ai.models.analysis_result.AnalysisResult
 -> mercury_ai.models.decision_snapshot.DecisionSnapshot
 -> unittest.mock.MagicMock

================================================================================
tests.test_weight_simulator
================================================================================
 -> mercury_ai.analysis.weight_simulator.WeightSimulator

================================================================================
tools.project_mapper.architecture_audit
================================================================================
 -> config.PROJECT_ROOT
 -> json
 -> pathlib.Path

================================================================================
tools.project_mapper.ast_parser
================================================================================
 -> ast
 -> pathlib.Path

================================================================================
tools.project_mapper.call_graph_builder
================================================================================
 -> ast
 -> config.PROJECT_ROOT
 -> json
 -> pathlib.Path

================================================================================
tools.project_mapper.config
================================================================================
 -> pathlib.Path

================================================================================
tools.project_mapper.dependency_builder
================================================================================
 -> collections.defaultdict
 -> config.PROJECT_ROOT
 -> json
 -> pathlib.Path

================================================================================
tools.project_mapper.main
================================================================================
 -> architecture_audit.ArchitectureAudit
 -> call_graph_builder.CallGraphBuilder
 -> dependency_builder.DependencyBuilder
 -> module_index.ModuleIndexBuilder
 -> python_indexer.PythonIndexer
 -> scanner.ProjectScanner
 -> snapshot_builder.SnapshotBuilder
 -> writer.InventoryWriter

================================================================================
tools.project_mapper.models
================================================================================
 -> dataclasses.dataclass
 -> dataclasses.field

================================================================================
tools.project_mapper.module_index
================================================================================
 -> collections.defaultdict
 -> config.PROJECT_ROOT
 -> json
 -> pathlib.Path

================================================================================
tools.project_mapper.python_indexer
================================================================================
 -> ast
 -> config.PROJECT_ROOT
 -> json
 -> pathlib.Path

================================================================================
tools.project_mapper.scanner
================================================================================
 -> ast_parser.ASTParser
 -> config.IGNORE_DIRS
 -> config.IGNORE_FILES
 -> config.PROJECT_ROOT
 -> config.SOURCE_EXTENSIONS
 -> models.FileInfo
 -> models.Inventory
 -> pathlib.Path

================================================================================
tools.project_mapper.snapshot_builder
================================================================================
 -> json
 -> pathlib.Path

================================================================================
tools.project_mapper.writer
================================================================================
 -> config.PROJECT_ROOT
 -> dataclasses.asdict
 -> json
 -> pathlib.Path

================================================================================
verify_assets
================================================================================
 -> mercury_ai.core.analysis_pipeline.AnalysisPipeline
 -> mercury_ai.data.market_data.MarketDataService
 -> mercury_ai.providers.yahoo_finance_provider.YahooFinanceProvider
