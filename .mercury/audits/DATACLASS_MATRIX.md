# DATACLASS CONTRACT MATRIX

**Project:** Mercury AI V1
**Audit:** SPRINT 1.9 BLOCO 2/10 - Contract Certification
**Generated:** 2026-08-01T19:59:12.825741
**Total Dataclasses:** 101

## Producer-Consumer Matrix

| Dataclass | Producer Module | Consumer Modules | Field Count |
|-----------|-----------------|------------------|-------------|
| BuyAndHoldBaseline | mercury_ai.analysis.benchmark_framework | None | 5 |
| EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework | None | 12 |
| StatisticalTestResult | mercury_ai.analysis.benchmark_framework | None | 8 |
| ConfidenceComponents | mercury_ai.analysis.confidence_engine | None | 5 |
| QualityReport | mercury_ai.analysis.data_quality_engine | None | 8 |
| DecisionExplainability | mercury_ai.analysis.decision_explainability | mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.mercury_decision_engine | 10 |
| DecisionResolverResult | mercury_ai.analysis.decision_resolver_engine | None | 3 |
| HealthStatus | mercury_ai.analysis.health_checker | None | 3 |
| InstitutionalContext | mercury_ai.analysis.institutional_context_builder | None | 7 |
| InstitutionalContribution | mercury_ai.analysis.institutional_contribution | mercury_ai.analysis.confluence_engine | 7 |
| InstitutionalScoreResult | mercury_ai.analysis.institutional_score_engine | None | 8 |
| PerformanceMetrics | mercury_ai.analysis.metric_calculator | mercury_ai.analysis.post_decision_evaluation_engine | 15 |
| Notification | mercury_ai.analysis.notification_center | None | 3 |
| BatchReplayReport | mercury_ai.analysis.replay_batch_processor | mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor | 9 |
| BatchReplayResult | mercury_ai.analysis.replay_batch_processor | mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor | 6 |
| BOSResult | mercury_ai.analysis.smart_money.bos_engine | None | 4 |
| CHOCHResult | mercury_ai.analysis.smart_money.choch_engine | None | 4 |
| EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine | mercury_ai.analysis.smart_money.tests.test_liquidity_engine | 6 |
| EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine | mercury_ai.analysis.smart_money.tests.test_liquidity_engine | 16 |
| EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine | mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine | 12 |
| LiquidityEvent | mercury_ai.analysis.smart_money.liquidity_event_engine | None | 5 |
| UniverseAsset | mercury_ai.config.universe | None | 9 |
| Asset | mercury_ai.core.asset_registry | None | 17 |
| AuditEvent | mercury_ai.core.audit_sink | mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.security_center | 2 |
| EngineResult | mercury_ai.core.base_engine | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.candlestick_engine | 5 |
| DataQualityResult | mercury_ai.core.data_quality_gate | None | 3 |
| RuntimeReport | mercury_ai.core.runtime_report | mercury_ai.core.analysis_pipeline | 2 |
| TelemetryData | mercury_ai.core.runtime_report | mercury_ai.core.analysis_pipeline | 16 |
| AuditEvent | mercury_ai.core.security_center | mercury_ai.core.pipeline_audit_middleware | 5 |
| ProviderHealth | mercury_ai.data.mercury_data_provider | None | 3 |
| ProviderMetrics | mercury_ai.data.mercury_data_provider | None | 3 |
| ProviderPriority | mercury_ai.data.mercury_data_provider | None | 0 |
| ProviderRegistry | mercury_ai.data.mercury_data_provider | None | 5 |
| ReplayMetrics | mercury_ai.database.replay_storage | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.historical_replay_engine, tests.test_performance_engine, tests.test_performance_engine, tests.test_performance_engine, tests.test_performance_engine, tests.test_performance_engine | 4 |
| AnalysisResult | mercury_ai.models.analysis_result | mercury_ai.core.analysis_pipeline, mercury_ai.core.analysis_pipeline, tests.test_versioning | 21 |
| BenchmarkReport | mercury_ai.models.benchmark_report | mercury_ai.analysis.benchmark_framework | 4 |
| BenchmarkRunResult | mercury_ai.models.benchmark_report | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.benchmark_framework | 5 |
| CandlestickAnalysis | mercury_ai.models.candlestick_analysis | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.candlestick_engine | 11 |
| ConfidenceResult | mercury_ai.models.confidence_result | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine | 8 |
| ConfluenceResult | mercury_ai.models.confluence_result | mercury_ai.analysis.confluence_engine, mercury_ai.brain.tests.test_explainability_engine | 11 |
| ConfluenceScore | mercury_ai.models.confluence_score | mercury_ai.analysis.confluence_score_engine | 5 |
| DataQualityResult | mercury_ai.models.data_quality_result | mercury_ai.core.data_quality_gate, mercury_ai.core.data_quality_gate | 5 |
| DecisionInput | mercury_ai.models.decision_input | None | 9 |
| DecisionNode | mercury_ai.models.decision_node | mercury_ai.analysis.decision_trace_engine | 6 |
| DecisionOutcome | mercury_ai.models.decision_outcome | None | 4 |
| DecisionResult | mercury_ai.models.decision_result | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline | 32 |
| DecisionSnapshot | mercury_ai.models.decision_snapshot | mercury_ai.core.analysis_pipeline, mercury_ai.core.analysis_pipeline, tests.test_versioning | 11 |
| DecisionTrace | mercury_ai.models.decision_trace | mercury_ai.analysis.decision_trace_engine | 3 |
| AssetPerformance | mercury_ai.models.equity_metrics | mercury_ai.analysis.performance_engine, mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor | 13 |
| UniversePerformance | mercury_ai.models.equity_metrics | mercury_ai.analysis.performance_engine | 9 |
| Evidence | mercury_ai.models.evidence | mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_conflict_resolution, tests.test_conflict_resolution, tests.test_conflict_resolution, tests.test_conflict_resolution, tests.test_conflict_resolution, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_engine, tests.test_evidence_engine, tests.test_evidence_engine, tests.test_evidence_engine, tests.test_evidence_engine, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_probability_engine, tests.test_probability_engine, tests.test_probability_engine, tests.test_probability_engine, tests.test_probability_engine, tests.test_validation_engine | 13 |
| EvidenceRankingResult | mercury_ai.models.evidence_ranking | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine | 14 |
| FairValueGapAnalysis | mercury_ai.models.fair_value_gap_analysis | mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.fair_value_gap_engine | 10 |
| LiquidityAnalysis | mercury_ai.models.liquidity_analysis | mercury_ai.analysis.smart_money.liquidity_engine | 12 |
| LiquidityProfile | mercury_ai.models.liquidity_profile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine | 7 |
| LiquidityResult | mercury_ai.models.liquidity_result | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_engine | 5 |
| MarketCondition | mercury_ai.models.market_condition | mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_candlestick_engine | 4 |
| MarketContext | mercury_ai.models.market_context | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine, mercury_ai.brain.tests.test_mercury_decision_engine | 10 |
| MarketData | mercury_ai.models.market_data | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, mercury_ai.core.analysis_pipeline | 14 |
| MarketEvidenceBundle | mercury_ai.models.market_evidence_bundle | mercury_ai.analysis.evidence_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_confidence_calibration, tests.test_probability_engine, tests.test_validation_engine, tests.test_validation_engine | 4 |
| MarketRegime | mercury_ai.models.market_regime | mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.risk_engine, tests.test_adaptive_weighting, tests.test_adaptive_weighting | 3 |
| MarketState | mercury_ai.models.market_state | mercury_ai.analysis.market_state_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration, tests.test_confidence_calibration | 2 |
| MarketStructure | mercury_ai.models.market_structure | mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine | 9 |
| MarketStructureProfile | mercury_ai.models.market_structure_profile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18, tests.test_regression_sprint18, tests.test_regression_sprint18, tests.test_regression_sprint18 | 54 |
| MarketThesis | mercury_ai.models.market_thesis | mercury_ai.analysis.market_thesis_builder | 9 |
| MemoryAuditResult | mercury_ai.models.memory_audit | mercury_ai.utils.memory_auditor | 5 |
| MemorySnapshot | mercury_ai.models.memory_audit | mercury_ai.utils.memory_auditor | 3 |
| MomentumAnalysis | mercury_ai.models.momentum_analysis | mercury_ai.analysis.momentum_engine, mercury_ai.analysis.momentum_engine | 12 |
| MTFConsensus | mercury_ai.models.mtf_consensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration | 12 |
| HotspotReport | mercury_ai.models.performance | mercury_ai.utils.performance_collector | 3 |
| PipelineMetric | mercury_ai.models.performance | mercury_ai.utils.performance_collector | 3 |
| StageMetric | mercury_ai.models.performance | mercury_ai.utils.performance_collector | 5 |
| PerformanceMetrics | mercury_ai.models.performance_metrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine | 10 |
| PriceActionAnalysis | mercury_ai.models.price_action | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine | 4 |
| PriceActionAnalysis | mercury_ai.models.price_action_analysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine | 16 |
| ProbabilityResult | mercury_ai.models.probability_result | mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine | 7 |
| ProfessionalThesis | mercury_ai.models.professional_thesis | None | 10 |
| HotspotSummary | mercury_ai.models.profiler_models | None | 2 |
| PipelineProfile | mercury_ai.models.profiler_models | mercury_ai.core.pipeline_profiler, mercury_ai.core.pipeline_profiler | 3 |
| StageProfile | mercury_ai.models.profiler_models | mercury_ai.core.pipeline_profiler | 6 |
| BenchmarkMetrics | mercury_ai.models.regression | mercury_ai.utils.regression_detector | 5 |
| RegressionResult | mercury_ai.models.regression | mercury_ai.utils.regression_detector, mercury_ai.utils.regression_detector | 6 |
| RiskAssessment | mercury_ai.models.risk_assessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.risk_engine, mercury_ai.core.analysis_pipeline | 17 |
| SessionAnalysis | mercury_ai.models.session_analysis | mercury_ai.analysis.session_engine | 5 |
| Signal | mercury_ai.models.signal | None | 11 |
| SmartMoneyAnalysis | mercury_ai.models.smart_money | mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_risk_engine | 5 |
| StressTestResult | mercury_ai.models.stress_test | mercury_ai.utils.stress_tester | 9 |
| SupportResistanceAnalysis | mercury_ai.models.support_resistance | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer, mercury_ai.analysis.support_resistance_analyzer | 5 |
| SupportResistanceAnalysis | mercury_ai.models.support_resistance_analysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer, mercury_ai.analysis.support_resistance_analyzer | 10 |
| Swing | mercury_ai.models.swing_analysis | mercury_ai.analysis.swing_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, tests.test_benchmark_integration | 10 |
| SwingSequenceResult | mercury_ai.models.swing_analysis | mercury_ai.analysis.swing_engine, mercury_ai.analysis.swing_engine | 8 |
| TradeFilterResult | mercury_ai.models.trade_filter_result | mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine | 4 |
| TradeMemory | mercury_ai.models.trade_memory | None | 12 |
| TradePermission | mercury_ai.models.trade_permission | None | 3 |
| TradingExplanation | mercury_ai.models.trading_explanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine | 30 |
| TrendAnalysis | mercury_ai.models.trend_analysis | None | 15 |
| VersionMetadata | mercury_ai.models.version_metadata | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline, mercury_ai.core.analysis_pipeline | 4 |
| VolatilityAnalysis | mercury_ai.models.volatility_analysis | mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volatility_engine | 5 |
| VolumeAnalysis | mercury_ai.models.volume_analysis | mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_engine | 12 |
| VolumeProfile | mercury_ai.models.volume_profile | mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.volume_intelligence_engine | 14 |
| VWAPAnalysis | mercury_ai.models.vwap_analysis | mercury_ai.analysis.vwap_engine, mercury_ai.analysis.vwap_engine | 11 |

## Field Contract Matrix

| Dataclass | Field | Type | Required | Optional | Default | Frozen | Line |
|-----------|-------|------|----------|----------|---------|--------|------|
| BuyAndHoldBaseline | symbol | str | ✓ |  |  | True | 53 |
| BuyAndHoldBaseline | total_return_pct | float | ✓ |  |  | True | 54 |
| BuyAndHoldBaseline | max_drawdown_pct | float | ✓ |  |  | True | 55 |
| BuyAndHoldBaseline | sharpe_ratio | float | ✓ |  |  | True | 56 |
| BuyAndHoldBaseline | benchmark_outperformance_pct | float | ✓ |  |  | True | 57 |
| EnhancedBenchmarkReport | version | str | ✓ |  |  | True | 63 |
| EnhancedBenchmarkReport | results | Tuple[BenchmarkRunResult, ...] | ✓ |  |  | True | 64 |
| EnhancedBenchmarkReport | average_execution_time | float | ✓ |  |  | True | 65 |
| EnhancedBenchmarkReport | performance_metrics | PerformanceMetrics | ✓ |  |  | True | 66 |
| EnhancedBenchmarkReport | asset_performances | Dict[str, AssetPerformance] | ✓ |  |  | True | 68 |
| EnhancedBenchmarkReport | universe_performance | Optional[UniversePerformance] |  | ✓ |  | True | 69 |
| EnhancedBenchmarkReport | buy_and_hold_baselines | Dict[str, BuyAndHoldBaseline] | ✓ |  |  | True | 70 |
| EnhancedBenchmarkReport | statistical_tests | Dict[str, StatisticalTestResult] | ✓ |  |  | True | 71 |
| EnhancedBenchmarkReport | warm_up_trades_excluded | int | ✓ |  |  | True | 72 |
| EnhancedBenchmarkReport | cool_down_trades_excluded | int | ✓ |  |  | True | 73 |
| EnhancedBenchmarkReport | total_wall_time | float | ✓ |  |  | True | 74 |
| EnhancedBenchmarkReport | parallel_workers | int | ✓ |  |  | True | 75 |
| StatisticalTestResult | t_statistic | float | ✓ |  |  | True | 40 |
| StatisticalTestResult | p_value | float | ✓ |  |  | True | 41 |
| StatisticalTestResult | is_significant_95 | bool | ✓ |  |  | True | 42 |
| StatisticalTestResult | bootstrap_ci_lower | float | ✓ |  |  | True | 43 |
| StatisticalTestResult | bootstrap_ci_upper | float | ✓ |  |  | True | 44 |
| StatisticalTestResult | bootstrap_samples | int | ✓ |  |  | True | 45 |
| StatisticalTestResult | mean_return | float | ✓ |  |  | True | 46 |
| StatisticalTestResult | std_return | float | ✓ |  |  | True | 47 |
| ConfidenceComponents | quality_factor | float | ✓ |  |  | True | 11 |
| ConfidenceComponents | consensus_factor | float | ✓ |  |  | True | 12 |
| ConfidenceComponents | market_factor | float | ✓ |  |  | True | 13 |
| ConfidenceComponents | confirmation_count | int | ✓ |  |  | True | 14 |
| ConfidenceComponents | final_score | float | ✓ |  |  | True | 15 |
| QualityReport | missing_candles | int |  |  | 0 | False | 9 |
| QualityReport | price_gaps | int |  |  | 0 | False | 10 |
| QualityReport | delay_seconds | float |  |  | 0.0 | False | 11 |
| QualityReport | volume_issues | int |  |  | 0 | False | 12 |
| QualityReport | integrity_issues | int |  |  | 0 | False | 13 |
| QualityReport | consistency_issues | int |  |  | 0 | False | 14 |
| QualityReport | duplicity_issues | int |  |  | 0 | False | 15 |
| QualityReport | quality_score | float |  |  | 1.0 | False | 16 |
| DecisionExplainability | decision | str | ✓ |  |  | True | 29 |
| DecisionExplainability | reason | str | ✓ |  |  | True | 30 |
| DecisionExplainability | dominant_direction | str | ✓ |  |  | True | 31 |
| DecisionExplainability | opportunity_grade | str | ✓ |  |  | True | 32 |
| DecisionExplainability | conflicting_signals | bool | ✓ |  |  | True | 33 |
| DecisionExplainability | institutional_score | float | ✓ |  |  | True | 34 |
| DecisionExplainability | confidence | float | ✓ |  |  | True | 35 |
| DecisionExplainability | triggered_rule | int | ✓ |  |  | True | 36 |
| DecisionExplainability | contributions | Tuple[InstitutionalContribution, ...] |  |  | field(default_factory=tuple) | True | 37 |
| DecisionExplainability | decision_chain | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 38 |
| DecisionResolverResult | decision | str | ✓ |  |  | True | 7 |
| DecisionResolverResult | confidence_override | Optional[float] |  | ✓ |  | True | 8 |
| DecisionResolverResult | triggered_rule | int | ✓ |  |  | True | 9 |
| HealthStatus | system_ready | bool | ✓ |  |  | False | 13 |
| HealthStatus | components | Dict[str, str] | ✓ |  |  | False | 14 |
| HealthStatus | timestamp | str | ✓ |  |  | False | 15 |
| InstitutionalContext | market_state | str | ✓ |  |  | False | 6 |
| InstitutionalContext | session | str | ✓ |  |  | False | 8 |
| InstitutionalContext | volatility | float | ✓ |  |  | False | 10 |
| InstitutionalContext | liquidity | float | ✓ |  |  | False | 12 |
| InstitutionalContext | institutional_bias | str | ✓ |  |  | False | 14 |
| InstitutionalContext | confidence | float | ✓ |  |  | False | 16 |
| InstitutionalContext | explanation | str | ✓ |  |  | False | 18 |
| InstitutionalContribution | engine_name | str | ✓ |  |  | True | 21 |
| InstitutionalContribution | weight | float | ✓ |  |  | True | 22 |
| InstitutionalContribution | raw_score | float | ✓ |  |  | True | 23 |
| InstitutionalContribution | weighted_score | float | ✓ |  |  | True | 24 |
| InstitutionalContribution | direction | str | ✓ |  |  | True | 25 |
| InstitutionalContribution | confidence | float | ✓ |  |  | True | 26 |
| InstitutionalContribution | explanation | str | ✓ |  |  | True | 27 |
| InstitutionalScoreResult | institutional_score | float | ✓ |  |  | True | 6 |
| InstitutionalScoreResult | probability_score | float | ✓ |  |  | True | 7 |
| InstitutionalScoreResult | confluence_score | float | ✓ |  |  | True | 8 |
| InstitutionalScoreResult | confidence_score | float | ✓ |  |  | True | 9 |
| InstitutionalScoreResult | trade_quality_score | float | ✓ |  |  | True | 10 |
| InstitutionalScoreResult | resolved_quality_score | float | ✓ |  |  | True | 11 |
| InstitutionalScoreResult | risk_score | float | ✓ |  |  | True | 12 |
| InstitutionalScoreResult | conflict_penalty | float | ✓ |  |  | True | 13 |
| PerformanceMetrics | accuracy | float | ✓ |  |  | True | 7 |
| PerformanceMetrics | precision_buy | float | ✓ |  |  | True | 8 |
| PerformanceMetrics | precision_sell | float | ✓ |  |  | True | 9 |
| PerformanceMetrics | recall | float | ✓ |  |  | True | 10 |
| PerformanceMetrics | f1_score | float | ✓ |  |  | True | 11 |
| PerformanceMetrics | balanced_accuracy | float | ✓ |  |  | True | 12 |
| PerformanceMetrics | mcc | float | ✓ |  |  | True | 13 |
| PerformanceMetrics | profit_factor | float | ✓ |  |  | True | 14 |
| PerformanceMetrics | expectancy | float | ✓ |  |  | True | 15 |
| PerformanceMetrics | win_rate | float | ✓ |  |  | True | 16 |
| PerformanceMetrics | avg_win | float | ✓ |  |  | True | 17 |
| PerformanceMetrics | avg_loss | float | ✓ |  |  | True | 18 |
| PerformanceMetrics | max_drawdown | float | ✓ |  |  | True | 19 |
| PerformanceMetrics | sharpe_simplified | float | ✓ |  |  | True | 20 |
| PerformanceMetrics | score_distribution | Dict[str, float] | ✓ |  |  | True | 21 |
| Notification | type | str | ✓ |  |  | False | 9 |
| Notification | message | str | ✓ |  |  | False | 10 |
| Notification | timestamp | str |  |  | field(default_factory=lambda: DeterministicClock.utcnow().isoformat()) | False | 11 |
| BatchReplayReport | version | str |  |  | '2.0' | True | 47 |
| BatchReplayReport | total_symbols | int |  |  | 0 | True | 48 |
| BatchReplayReport | successful | int |  |  | 0 | True | 49 |
| BatchReplayReport | failed | int |  |  | 0 | True | 50 |
| BatchReplayReport | total_wall_time | float |  |  | 0.0 | True | 51 |
| BatchReplayReport | results | Tuple[BatchReplayResult, ...] |  |  | () | True | 52 |
| BatchReplayReport | universe_performance | Optional[UniversePerformance] |  | ✓ | None | True | 53 |
| BatchReplayReport | aggregate_cache_stats | Dict[str, float] |  |  | field(default_factory=dict) | True | 54 |
| BatchReplayReport | errors | Tuple[str, ...] |  |  | () | True | 55 |
| BatchReplayResult | symbol | str | ✓ |  |  | True | 36 |
| BatchReplayResult | metrics | Tuple[ReplayMetrics, ...] | ✓ |  |  | True | 37 |
| BatchReplayResult | asset_performance | AssetPerformance | ✓ |  |  | True | 38 |
| BatchReplayResult | wall_time | float | ✓ |  |  | True | 39 |
| BatchReplayResult | cache_stats | dict | ✓ |  |  | True | 40 |
| BatchReplayResult | error | Optional[str] |  | ✓ | None | True | 41 |
| BOSResult | detected | bool | ✓ |  |  | True | 8 |
| BOSResult | direction | str | ✓ |  |  | True | 9 |
| BOSResult | confidence | int | ✓ |  |  | True | 10 |
| BOSResult | explanation | list[str] | ✓ |  |  | True | 11 |
| CHOCHResult | detected | bool | ✓ |  |  | True | 9 |
| CHOCHResult | direction | str | ✓ |  |  | True | 10 |
| CHOCHResult | confidence | int | ✓ |  |  | True | 11 |
| CHOCHResult | explanation | list[str] | ✓ |  |  | True | 12 |
| EqualHighGroup | touches | List[Swing] | ✓ |  |  | True | 16 |
| EqualHighGroup | prices | List[float] | ✓ |  |  | True | 17 |
| EqualHighGroup | timestamps | List[str] | ✓ |  |  | True | 18 |
| EqualHighGroup | indices | List[int] | ✓ |  |  | True | 19 |
| EqualHighGroup | strengths | List[float] | ✓ |  |  | True | 20 |
| EqualHighGroup | ATRs | List[float] | ✓ |  |  | True | 21 |
| EqualHighMetrics | touch_count | int | ✓ |  |  | True | 25 |
| EqualHighMetrics | average_price | float | ✓ |  |  | True | 26 |
| EqualHighMetrics | minimum_price | float | ✓ |  |  | True | 27 |
| EqualHighMetrics | maximum_price | float | ✓ |  |  | True | 28 |
| EqualHighMetrics | price_deviation | float | ✓ |  |  | True | 29 |
| EqualHighMetrics | average_strength | float | ✓ |  |  | True | 30 |
| EqualHighMetrics | minimum_strength | float | ✓ |  |  | True | 31 |
| EqualHighMetrics | maximum_strength | float | ✓ |  |  | True | 32 |
| EqualHighMetrics | average_ATR | float | ✓ |  |  | True | 33 |
| EqualHighMetrics | ATR_consistency | float | ✓ |  |  | True | 34 |
| EqualHighMetrics | first_timestamp | str | ✓ |  |  | True | 35 |
| EqualHighMetrics | last_timestamp | str | ✓ |  |  | True | 36 |
| EqualHighMetrics | first_index | int | ✓ |  |  | True | 37 |
| EqualHighMetrics | last_index | int | ✓ |  |  | True | 38 |
| EqualHighMetrics | age_in_swings | int | ✓ |  |  | True | 39 |
| EqualHighMetrics | cluster_width | int | ✓ |  |  | True | 40 |
| EqualHighScore | touch_score | float | ✓ |  |  | True | 44 |
| EqualHighScore | strength_score | float | ✓ |  |  | True | 45 |
| EqualHighScore | atr_score | float | ✓ |  |  | True | 46 |
| EqualHighScore | deviation_score | float | ✓ |  |  | True | 47 |
| EqualHighScore | density_score | float | ✓ |  |  | True | 48 |
| EqualHighScore | final_score | float | ✓ |  |  | True | 49 |
| EqualHighScore | touch_count | int | ✓ |  |  | True | 50 |
| EqualHighScore | average_price | float | ✓ |  |  | True | 51 |
| EqualHighScore | average_strength | float | ✓ |  |  | True | 52 |
| EqualHighScore | average_ATR | float | ✓ |  |  | True | 53 |
| EqualHighScore | age_in_swings | int | ✓ |  |  | True | 54 |
| EqualHighScore | cluster_density | float | ✓ |  |  | True | 55 |
| LiquidityEvent | event_type | LiquidityEventType | ✓ |  |  | True | 9 |
| LiquidityEvent | price | float | ✓ |  |  | True | 10 |
| LiquidityEvent | strength | float | ✓ |  |  | True | 11 |
| LiquidityEvent | confidence | float | ✓ |  |  | True | 12 |
| LiquidityEvent | explanation | str | ✓ |  |  | True | 13 |
| UniverseAsset | symbol | str | ✓ |  |  | True | 37 |
| UniverseAsset | display_name | str | ✓ |  |  | True | 38 |
| UniverseAsset | market | str | ✓ |  |  | True | 39 |
| UniverseAsset | provider_symbol | str | ✓ |  |  | True | 40 |
| UniverseAsset | enabled | bool |  |  | True | True | 41 |
| UniverseAsset | volatility | str |  |  | 'MEDIUM' | True | 42 |
| UniverseAsset | precision | int |  |  | 5 | True | 43 |
| UniverseAsset | priority | int |  |  | 1 | True | 44 |
| UniverseAsset | notes | str |  |  | '' | True | 45 |
| Asset | symbol | str | ✓ |  |  | False | 9 |
| Asset | category | str | ✓ |  |  | False | 10 |
| Asset | priority | int | ✓ |  |  | False | 11 |
| Asset | profile | str | ✓ |  |  | False | 12 |
| Asset | enabled | bool |  |  | True | False | 13 |
| Asset | provider | str |  |  | 'Yahoo' | False | 14 |
| Asset | fallback_provider | str |  |  | 'Polygon' | False | 15 |
| Asset | market | str |  |  | 'Stocks' | False | 16 |
| Asset | timeframe | str |  |  | '5m' | False | 17 |
| Asset | tick_size | float |  |  | 0.01 | False | 18 |
| Asset | pip_size | float |  |  | 0.0001 | False | 19 |
| Asset | trading_session | str |  |  | 'Standard' | False | 20 |
| Asset | liquidity | float |  |  | 1.0 | False | 21 |
| Asset | spread | float |  |  | 0.01 | False | 22 |
| Asset | favorite | bool |  |  | False | False | 23 |
| Asset | last_operated | float |  |  | 0.0 | False | 24 |
| Asset | previous_score | float |  |  | 0.0 | False | 25 |
| AuditEvent | stage_name | str | ✓ |  |  | True | 7 |
| AuditEvent | timestamp | str | ✓ |  |  | True | 8 |
| EngineResult | score | float | ✓ |  |  | True | 7 |
| EngineResult | confidence | float | ✓ |  |  | True | 8 |
| EngineResult | evidences | Tuple[str, ...] | ✓ |  |  | True | 9 |
| EngineResult | warnings | Tuple[str, ...] | ✓ |  |  | True | 10 |
| EngineResult | execution_time | float | ✓ |  |  | True | 11 |
| DataQualityResult | score | float | ✓ |  |  | False | 7 |
| DataQualityResult | allowed | bool | ✓ |  |  | False | 8 |
| DataQualityResult | warnings | list | ✓ |  |  | False | 9 |
| RuntimeReport | symbol | str | ✓ |  |  | False | 25 |
| RuntimeReport | stages | List[TelemetryData] |  |  | field(default_factory=list) | False | 26 |
| TelemetryData | engine_name | str | ✓ |  |  | False | 6 |
| TelemetryData | start_time | str | ✓ |  |  | False | 7 |
| TelemetryData | end_time | str | ✓ |  |  | False | 8 |
| TelemetryData | execution_time | float | ✓ |  |  | False | 9 |
| TelemetryData | input_object | Any | ✓ |  |  | False | 10 |
| TelemetryData | output_object | Any | ✓ |  |  | False | 11 |
| TelemetryData | creator | Optional[str] |  | ✓ | None | False | 12 |
| TelemetryData | modifier | Optional[str] |  | ✓ | None | False | 13 |
| TelemetryData | consumer | Optional[str] |  | ✓ | None | False | 14 |
| TelemetryData | disposer | Optional[str] |  | ✓ | None | False | 15 |
| TelemetryData | persister | Optional[str] |  | ✓ | None | False | 16 |
| TelemetryData | evidence_count | int |  |  | 0 | False | 17 |
| TelemetryData | warnings | int |  |  | 0 | False | 18 |
| TelemetryData | conflicts | int |  |  | 0 | False | 19 |
| TelemetryData | dataframe_size | Optional[int] |  | ✓ | None | False | 20 |
| TelemetryData | memory_usage | Optional[float] |  | ✓ | None | False | 21 |
| AuditEvent | user | str | ✓ |  |  | False | 7 |
| AuditEvent | action | str | ✓ |  |  | False | 8 |
| AuditEvent | target | str | ✓ |  |  | False | 9 |
| AuditEvent | severity | str | ✓ |  |  | False | 10 |
| AuditEvent | timestamp | str |  |  | field(default_factory=lambda: DeterministicClock.utcnow().isoformat()) | False | 11 |
| ProviderHealth | status | ProviderStatus |  |  | ProviderStatus.INACTIVE | False | 26 |
| ProviderHealth | last_check | float |  |  | 0.0 | False | 27 |
| ProviderHealth | error_count | int |  |  | 0 | False | 28 |
| ProviderMetrics | latency_ms | float |  |  | 0.0 | False | 20 |
| ProviderMetrics | quality_score | float |  |  | 1.0 | False | 21 |
| ProviderMetrics | uptime_percentage | float |  |  | 100.0 | False | 22 |
| ProviderRegistry | name | str | ✓ |  |  | False | 38 |
| ProviderRegistry | priority | ProviderPriority | ✓ |  |  | False | 39 |
| ProviderRegistry | instance | Any | ✓ |  |  | False | 40 |
| ProviderRegistry | health | ProviderHealth |  |  | field(default_factory=ProviderHealth) | False | 41 |
| ProviderRegistry | metrics | ProviderMetrics |  |  | field(default_factory=ProviderMetrics) | False | 42 |
| ReplayMetrics | mae | float | ✓ |  |  | True | 8 |
| ReplayMetrics | mfe | float | ✓ |  |  | True | 9 |
| ReplayMetrics | pl | float | ✓ |  |  | True | 10 |
| ReplayMetrics | hit | bool | ✓ |  |  | True | 11 |
| AnalysisResult | market | MarketData | ✓ |  |  | True | 30 |
| AnalysisResult | context | MarketContext | ✓ |  |  | True | 31 |
| AnalysisResult | trend | List[Evidence] | ✓ |  |  | True | 32 |
| AnalysisResult | mtf_evidences | List[Evidence] | ✓ |  |  | True | 33 |
| AnalysisResult | smart_money | SmartMoneyAnalysis | ✓ |  |  | True | 34 |
| AnalysisResult | market_regime | MarketRegime | ✓ |  |  | True | 35 |
| AnalysisResult | confluence | ConfluenceResult | ✓ |  |  | True | 36 |
| AnalysisResult | market_condition | MarketCondition | ✓ |  |  | True | 37 |
| AnalysisResult | market_state | MarketState | ✓ |  |  | True | 38 |
| AnalysisResult | candlestick_analysis | CandlestickAnalysis | ✓ |  |  | True | 39 |
| AnalysisResult | volatility_analysis | VolatilityAnalysis | ✓ |  |  | True | 40 |
| AnalysisResult | session_analysis | SessionAnalysis | ✓ |  |  | True | 41 |
| AnalysisResult | support_resistance | SupportResistanceAnalysis | ✓ |  |  | True | 42 |
| AnalysisResult | liquidity_analysis | LiquidityResult | ✓ |  |  | True | 43 |
| AnalysisResult | risk_assessment | RiskAssessment | ✓ |  |  | True | 44 |
| AnalysisResult | evidence_ranking | EvidenceRankingResult | ✓ |  |  | True | 45 |
| AnalysisResult | volume_analysis | VolumeAnalysis | ✓ |  |  | True | 46 |
| AnalysisResult | structure_analysis | MarketStructureProfile | ✓ |  |  | True | 47 |
| AnalysisResult | decision | DecisionResult | ✓ |  |  | True | 48 |
| AnalysisResult | timestamp | str |  |  | field(default_factory=lambda: DeterministicClock.utcnow().isoformat()) | True | 49 |
| AnalysisResult | version | str |  |  | field(default_factory=lambda: settings.VERSION) | True | 50 |
| BenchmarkReport | version | str | ✓ |  |  | True | 16 |
| BenchmarkReport | results | Tuple[BenchmarkRunResult, ...] | ✓ |  |  | True | 17 |
| BenchmarkReport | average_execution_time | float | ✓ |  |  | True | 18 |
| BenchmarkReport | performance_metrics | PerformanceMetrics | ✓ |  |  | True | 19 |
| BenchmarkRunResult | timestamp | str | ✓ |  |  | True | 8 |
| BenchmarkRunResult | symbol | str | ✓ |  |  | True | 9 |
| BenchmarkRunResult | decision_result | DecisionResult | ✓ |  |  | True | 10 |
| BenchmarkRunResult | execution_time | float | ✓ |  |  | True | 11 |
| BenchmarkRunResult | memory_usage | float | ✓ |  |  | True | 12 |
| CandlestickAnalysis | pattern | Optional[str] |  | ✓ | None | True | 6 |
| CandlestickAnalysis | body_strength | Optional[float] |  | ✓ | None | True | 7 |
| CandlestickAnalysis | upper_wick | Optional[float] |  | ✓ | None | True | 8 |
| CandlestickAnalysis | lower_wick | Optional[float] |  | ✓ | None | True | 9 |
| CandlestickAnalysis | rejection | Optional[bool] |  | ✓ | None | True | 10 |
| CandlestickAnalysis | engulfing | Optional[bool] |  | ✓ | None | True | 11 |
| CandlestickAnalysis | continuation | Optional[bool] |  | ✓ | None | True | 12 |
| CandlestickAnalysis | explanation | Optional[str] |  | ✓ | None | True | 13 |
| CandlestickAnalysis | context | Optional[str] |  | ✓ | None | True | 14 |
| CandlestickAnalysis | context_score | Optional[float] |  | ✓ | None | True | 15 |
| CandlestickAnalysis | evidences | List[str] |  |  | field(default_factory=list) | True | 16 |
| ConfidenceResult | confidence_score | float | ✓ |  |  | True | 14 |
| ConfidenceResult | final_confidence | float | ✓ |  |  | True | 17 |
| ConfidenceResult | confidence_grade | str | ✓ |  |  | True | 20 |
| ConfidenceResult | is_high | bool | ✓ |  |  | True | 23 |
| ConfidenceResult | average_quality | float | ✓ |  |  | True | 29 |
| ConfidenceResult | consensus_score | float | ✓ |  |  | True | 31 |
| ConfidenceResult | market_score | float | ✓ |  |  | True | 33 |
| ConfidenceResult | confirmation_count | int | ✓ |  |  | True | 35 |
| ConfluenceResult | buy_score | float | ✓ |  |  | True | 7 |
| ConfluenceResult | sell_score | float | ✓ |  |  | True | 8 |
| ConfluenceResult | neutral_score | float | ✓ |  |  | True | 9 |
| ConfluenceResult | agreement_percentage | float | ✓ |  |  | True | 10 |
| ConfluenceResult | conflicting_signals | bool | ✓ |  |  | True | 11 |
| ConfluenceResult | independent_confirmations | int | ✓ |  |  | True | 12 |
| ConfluenceResult | weighted_score | float | ✓ |  |  | True | 13 |
| ConfluenceResult | confidence | float | ✓ |  |  | True | 14 |
| ConfluenceResult | dominant_direction | AnalysisDirection | ✓ |  |  | True | 15 |
| ConfluenceResult | evidences | Tuple[Any, ...] | ✓ |  |  | True | 16 |
| ConfluenceResult | warnings | Tuple[str, ...] | ✓ |  |  | True | 17 |
| ConfluenceScore | confluence_score | float | ✓ |  |  | True | 5 |
| ConfluenceScore | clarity_score | float | ✓ |  |  | True | 6 |
| ConfluenceScore | bullish_score | float | ✓ |  |  | True | 7 |
| ConfluenceScore | bearish_score | float | ✓ |  |  | True | 8 |
| ConfluenceScore | conflict_penalty | float | ✓ |  |  | True | 9 |
| DataQualityResult | score | float | ✓ |  |  | True | 9 |
| DataQualityResult | warnings | Tuple[str, ...] | ✓ |  |  | True | 10 |
| DataQualityResult | missing_inputs | Tuple[str, ...] | ✓ |  |  | True | 11 |
| DataQualityResult | stale_data | bool | ✓ |  |  | True | 12 |
| DataQualityResult | quality_level | str | ✓ |  |  | True | 13 |
| DecisionInput | market_bias | str | ✓ |  |  | True | 6 |
| DecisionInput | confluence_score | float | ✓ |  |  | True | 7 |
| DecisionInput | confidence | float | ✓ |  |  | True | 8 |
| DecisionInput | risk_score | float | ✓ |  |  | True | 9 |
| DecisionInput | market_state | str | ✓ |  |  | True | 10 |
| DecisionInput | warnings | List[str] |  |  | field(default_factory=list) | True | 11 |
| DecisionInput | blockers | List[str] |  |  | field(default_factory=list) | True | 12 |
| DecisionInput | opportunity_grade | str |  |  | 'C' | True | 13 |
| DecisionInput | institutional_alignment | bool |  |  | False | True | 14 |
| DecisionNode | engine | str | ✓ |  |  | True | 6 |
| DecisionNode | evidence | str | ✓ |  |  | True | 7 |
| DecisionNode | weight | float | ✓ |  |  | True | 8 |
| DecisionNode | score | float | ✓ |  |  | True | 9 |
| DecisionNode | influence | str | ✓ |  |  | True | 10 |
| DecisionNode | result | str | ✓ |  |  | True | 11 |
| DecisionOutcome | audit_id | str | ✓ |  |  | True | 6 |
| DecisionOutcome | outcome | float | ✓ |  |  | True | 7 |
| DecisionOutcome | timestamp | str | ✓ |  |  | True | 8 |
| DecisionOutcome | meta | Dict[str, Any] | ✓ |  |  | True | 9 |
| DecisionResult | decision | str | ✓ |  |  | True | 13 |
| DecisionResult | grade | str | ✓ |  |  | True | 14 |
| DecisionResult | confidence | float | ✓ |  |  | True | 15 |
| DecisionResult | clarity | float | ✓ |  |  | True | 16 |
| DecisionResult | risk_score | float | ✓ |  |  | True | 17 |
| DecisionResult | score | float | ✓ |  |  | True | 18 |
| DecisionResult | quality | float | ✓ |  |  | True | 19 |
| DecisionResult | expected_strength | float | ✓ |  |  | True | 20 |
| DecisionResult | buy_probability | float | ✓ |  |  | True | 21 |
| DecisionResult | sell_probability | float | ✓ |  |  | True | 22 |
| DecisionResult | wait_probability | float | ✓ |  |  | True | 23 |
| DecisionResult | expected_risk | float | ✓ |  |  | True | 24 |
| DecisionResult | expected_reward | float | ✓ |  |  | True | 25 |
| DecisionResult | expected_drawdown | float | ✓ |  |  | True | 26 |
| DecisionResult | audit_id | str | ✓ |  |  | True | 27 |
| DecisionResult | version_metadata | VersionMetadata | ✓ |  |  | True | 28 |
| DecisionResult | explanation | TradingExplanation | ✓ |  |  | True | 29 |
| DecisionResult | mtf_consensus | Optional[MTFConsensus] |  | ✓ | None | True | 30 |
| DecisionResult | market_regime | Optional[MarketRegime] |  | ✓ | None | True | 31 |
| DecisionResult | trade_allowed | bool |  |  | True | True | 32 |
| DecisionResult | trade_block_reasons | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 33 |
| DecisionResult | trade_quality_score | float |  |  | 0.0 | True | 34 |
| DecisionResult | trade_quality_level | str |  |  | 'N/A' | True | 35 |
| DecisionResult | trace | Optional[DecisionTrace] |  | ✓ | None | True | 36 |
| DecisionResult | warnings | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 37 |
| DecisionResult | weaknesses | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 38 |
| DecisionResult | blockers | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 39 |
| DecisionResult | summary | str |  |  | '' | True | 40 |
| DecisionResult | technical_reason | str |  |  | '' | True | 41 |
| DecisionResult | institutional_alignment | bool |  |  | False | True | 42 |
| DecisionResult | evidence_ranking | Optional[EvidenceRankingResult] |  | ✓ | None | True | 43 |
| DecisionResult | explainability | Optional[DecisionExplainability] |  | ✓ | None | True | 44 |
| DecisionSnapshot | timestamp | str | ✓ |  |  | True | 15 |
| DecisionSnapshot | asset | str | ✓ |  |  | True | 16 |
| DecisionSnapshot | timeframe | str | ✓ |  |  | True | 17 |
| DecisionSnapshot | context | MarketContext | ✓ |  |  | True | 18 |
| DecisionSnapshot | evidence_bundle | MarketEvidenceBundle | ✓ |  |  | True | 19 |
| DecisionSnapshot | decision_result | DecisionResult | ✓ |  |  | True | 20 |
| DecisionSnapshot | version_metadata | VersionMetadata | ✓ |  |  | True | 21 |
| DecisionSnapshot | audit_events | Tuple[str, ...] | ✓ |  |  | True | 22 |
| DecisionSnapshot | session_id | str | ✓ |  |  | True | 23 |
| DecisionSnapshot | evidence_ranking | Optional[EvidenceRankingResult] |  | ✓ | None | True | 24 |
| DecisionSnapshot | version | str |  |  | field(default_factory=lambda: settings.VERSION) | True | 25 |
| DecisionTrace | nodes | Tuple[DecisionNode, ...] |  |  | field(default_factory=tuple) | True | 7 |
| DecisionTrace | final_score | float |  |  | 0.0 | True | 8 |
| DecisionTrace | final_decision | str |  |  | '' | True | 9 |
| AssetPerformance | asset | str | ✓ |  |  | True | 8 |
| AssetPerformance | total_trades | int | ✓ |  |  | True | 9 |
| AssetPerformance | pnl_accumulated | float | ✓ |  |  | True | 10 |
| AssetPerformance | win_rate | float | ✓ |  |  | True | 11 |
| AssetPerformance | profit_factor | float | ✓ |  |  | True | 12 |
| AssetPerformance | expectancy | float | ✓ |  |  | True | 13 |
| AssetPerformance | avg_win | float | ✓ |  |  | True | 14 |
| AssetPerformance | avg_loss | float | ✓ |  |  | True | 15 |
| AssetPerformance | max_drawdown | float | ✓ |  |  | True | 16 |
| AssetPerformance | recovery_time_candles | int | ✓ |  |  | True | 17 |
| AssetPerformance | sharpe_ratio | float | ✓ |  |  | True | 18 |
| AssetPerformance | sortino_ratio | float | ✓ |  |  | True | 19 |
| AssetPerformance | equity_curve | Tuple[float, ...] | ✓ |  |  | True | 20 |
| UniversePerformance | total_assets | int | ✓ |  |  | True | 25 |
| UniversePerformance | global_pnl | float | ✓ |  |  | True | 26 |
| UniversePerformance | global_win_rate | float | ✓ |  |  | True | 27 |
| UniversePerformance | global_profit_factor | float | ✓ |  |  | True | 28 |
| UniversePerformance | global_max_drawdown | float | ✓ |  |  | True | 29 |
| UniversePerformance | global_sharpe | float | ✓ |  |  | True | 30 |
| UniversePerformance | global_sortino | float | ✓ |  |  | True | 31 |
| UniversePerformance | asset_stats | Dict[str, AssetPerformance] | ✓ |  |  | True | 32 |
| UniversePerformance | consolidated_equity_curve | Tuple[float, ...] | ✓ |  |  | True | 33 |
| Evidence | engine_name | str | ✓ |  |  | True | 8 |
| Evidence | evidence_name | str | ✓ |  |  | True | 9 |
| Evidence | direction | str | ✓ |  |  | True | 10 |
| Evidence | strength | float | ✓ |  |  | True | 11 |
| Evidence | confidence | float | ✓ |  |  | True | 12 |
| Evidence | description | str | ✓ |  |  | True | 13 |
| Evidence | weight | float | ✓ |  |  | True | 14 |
| Evidence | contribution_score | float |  |  | 0.0 | True | 15 |
| Evidence | quality_score | float |  |  | 100.0 | True | 16 |
| Evidence | context_score | float |  |  | 100.0 | True | 17 |
| Evidence | timeframe | str |  |  | DEFAULT_TIMEFRAME | True | 18 |
| Evidence | timestamp | str |  |  | field(default_factory=lambda: DeterministicClock.utcnow().isoformat()) | True | 19 |
| Evidence | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 20 |
| EvidenceRankingResult | ranked_evidences | List[Evidence] | ✓ |  |  | True | 7 |
| EvidenceRankingResult | contribution_percentage | dict | ✓ |  |  | True | 8 |
| EvidenceRankingResult | strongest_evidence | Evidence | ✓ |  |  | True | 9 |
| EvidenceRankingResult | weakest_evidence | Evidence | ✓ |  |  | True | 10 |
| EvidenceRankingResult | total_weight | float | ✓ |  |  | True | 11 |
| EvidenceRankingResult | bullish_weight | float | ✓ |  |  | True | 12 |
| EvidenceRankingResult | bearish_weight | float | ✓ |  |  | True | 13 |
| EvidenceRankingResult | neutral_weight | float | ✓ |  |  | True | 14 |
| EvidenceRankingResult | bullish_score | float | ✓ |  |  | True | 15 |
| EvidenceRankingResult | bearish_score | float | ✓ |  |  | True | 16 |
| EvidenceRankingResult | neutral_score | float | ✓ |  |  | True | 17 |
| EvidenceRankingResult | top_bullish_evidence | Optional[Evidence] |  | ✓ | None | True | 18 |
| EvidenceRankingResult | top_bearish_evidence | Optional[Evidence] |  | ✓ | None | True | 19 |
| EvidenceRankingResult | top_neutral_evidence | Optional[Evidence] |  | ✓ | None | True | 20 |
| FairValueGapAnalysis | engine_name | str |  |  | 'FairValueGapEngine' | True | 7 |
| FairValueGapAnalysis | is_bullish_fvg | bool |  |  | False | True | 8 |
| FairValueGapAnalysis | is_bearish_fvg | bool |  |  | False | True | 9 |
| FairValueGapAnalysis | is_filled | bool |  |  | False | True | 10 |
| FairValueGapAnalysis | is_open | bool |  |  | False | True | 11 |
| FairValueGapAnalysis | fvg_quality | float |  |  | 0.0 | True | 12 |
| FairValueGapAnalysis | confidence | float |  |  | 0.0 | True | 13 |
| FairValueGapAnalysis | quality | float |  |  | 0.0 | True | 14 |
| FairValueGapAnalysis | evidences | Tuple[Evidence, ...] |  |  | field(default_factory=tuple) | True | 15 |
| FairValueGapAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 16 |
| LiquidityAnalysis | engine_name | str |  |  | 'LiquidityEngine' | True | 7 |
| LiquidityAnalysis | has_equal_highs | bool |  |  | False | True | 8 |
| LiquidityAnalysis | has_equal_lows | bool |  |  | False | True | 9 |
| LiquidityAnalysis | has_liquidity_sweep | bool |  |  | False | True | 10 |
| LiquidityAnalysis | has_stop_hunt | bool |  |  | False | True | 11 |
| LiquidityAnalysis | has_liquidity_void | bool |  |  | False | True | 12 |
| LiquidityAnalysis | is_premium | bool |  |  | False | True | 13 |
| LiquidityAnalysis | is_discount | bool |  |  | False | True | 14 |
| LiquidityAnalysis | confidence | float |  |  | 0.0 | True | 15 |
| LiquidityAnalysis | quality | float |  |  | 0.0 | True | 16 |
| LiquidityAnalysis | evidences | Tuple[Evidence, ...] |  |  | field(default_factory=tuple) | True | 17 |
| LiquidityAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 18 |
| LiquidityProfile | internal_liquidity | float |  |  | 0.0 | True | 5 |
| LiquidityProfile | external_liquidity | float |  |  | 0.0 | True | 6 |
| LiquidityProfile | liquidity_sweep | bool |  |  | False | True | 7 |
| LiquidityProfile | equal_highs | bool |  |  | False | True | 8 |
| LiquidityProfile | equal_lows | bool |  |  | False | True | 9 |
| LiquidityProfile | stop_hunt_probability | float |  |  | 0.0 | True | 10 |
| LiquidityProfile | liquidity_density | float |  |  | 0.0 | True | 11 |
| LiquidityResult | evidences | Tuple[Any, ...] | ✓ |  |  | True | 6 |
| LiquidityResult | score | float | ✓ |  |  | True | 7 |
| LiquidityResult | confidence | float | ✓ |  |  | True | 8 |
| LiquidityResult | strength | float | ✓ |  |  | True | 9 |
| LiquidityResult | metadata | dict | ✓ |  |  | True | 10 |
| MarketCondition | trend | Optional[str] |  | ✓ | None | True | 6 |
| MarketCondition | trend_strength | Optional[float] |  | ✓ | None | True | 7 |
| MarketCondition | market_state | Optional[str] |  | ✓ | None | True | 8 |
| MarketCondition | explanation | Optional[str] |  | ✓ | None | True | 9 |
| MarketContext | market | MarketData | ✓ |  |  | True | 19 |
| MarketContext | trend | List[Evidence] | ✓ |  |  | True | 21 |
| MarketContext | price_action | PriceActionAnalysis | ✓ |  |  | True | 23 |
| MarketContext | support_resistance | SupportResistanceAnalysis | ✓ |  |  | True | 25 |
| MarketContext | smart_money | SmartMoneyAnalysis | ✓ |  |  | True | 27 |
| MarketContext | liquidity | LiquidityProfile | ✓ |  |  | True | 29 |
| MarketContext | market_state | MarketState | ✓ |  |  | True | 31 |
| MarketContext | market_regime | MarketRegime | ✓ |  |  | True | 33 |
| MarketContext | mtf_consensus | MTFConsensus | ✓ |  |  | True | 35 |
| MarketContext | risk_assessment | RiskAssessment | ✓ |  |  | True | 37 |
| MarketData | symbol | str | ✓ |  |  | True | 6 |
| MarketData | timeframe | str | ✓ |  |  | True | 7 |
| MarketData | close | float | ✓ |  |  | True | 9 |
| MarketData | ema9 | float | ✓ |  |  | True | 11 |
| MarketData | ema21 | float | ✓ |  |  | True | 12 |
| MarketData | ema50 | float | ✓ |  |  | True | 13 |
| MarketData | rsi | float | ✓ |  |  | True | 15 |
| MarketData | atr | float | ✓ |  |  | True | 17 |
| MarketData | adx | float | ✓ |  |  | True | 18 |
| MarketData | macd | float | ✓ |  |  | True | 20 |
| MarketData | macd_signal | float | ✓ |  |  | True | 21 |
| MarketData | bollinger_upper | float | ✓ |  |  | True | 23 |
| MarketData | bollinger_lower | float | ✓ |  |  | True | 24 |
| MarketData | volume | float | ✓ |  |  | True | 26 |
| MarketEvidenceBundle | evidences | Tuple[Evidence, ...] | ✓ |  |  | True | 10 |
| MarketEvidenceBundle | timestamp | str | ✓ |  |  | True | 11 |
| MarketEvidenceBundle | asset | str | ✓ |  |  | True | 12 |
| MarketEvidenceBundle | timeframe | str | ✓ |  |  | True | 13 |
| MarketRegime | regime | MarketRegimeEnum | ✓ |  |  | True | 8 |
| MarketRegime | confidence | float | ✓ |  |  | True | 9 |
| MarketRegime | supporting_evidences | List[Evidence] | ✓ |  |  | True | 10 |
| MarketState | state | MarketStateEnum | ✓ |  |  | True | 6 |
| MarketState | explanation | str | ✓ |  |  | True | 7 |
| MarketStructure | trend | str |  |  | 'RANGE' | True | 7 |
| MarketStructure | higher_high | bool |  |  | False | True | 9 |
| MarketStructure | higher_low | bool |  |  | False | True | 10 |
| MarketStructure | lower_high | bool |  |  | False | True | 12 |
| MarketStructure | lower_low | bool |  |  | False | True | 13 |
| MarketStructure | swing_highs | int |  |  | 0 | True | 15 |
| MarketStructure | swing_lows | int |  |  | 0 | True | 16 |
| MarketStructure | confidence | int |  |  | 0 | True | 18 |
| MarketStructure | explanation | list[str] |  |  | field(default_factory=list) | True | 20 |
| MarketStructureProfile | classification | str |  |  | 'UNKNOWN' | True | 7 |
| MarketStructureProfile | trend | str |  |  | 'NEUTRAL' | True | 8 |
| MarketStructureProfile | trend_strength | float |  |  | 0.0 | True | 9 |
| MarketStructureProfile | bos_detected | bool |  |  | False | True | 10 |
| MarketStructureProfile | choch_detected | bool |  |  | False | True | 11 |
| MarketStructureProfile | hh_count | int |  |  | 0 | True | 12 |
| MarketStructureProfile | hl_count | int |  |  | 0 | True | 13 |
| MarketStructureProfile | lh_count | int |  |  | 0 | True | 14 |
| MarketStructureProfile | ll_count | int |  |  | 0 | True | 15 |
| MarketStructureProfile | expansion | bool |  |  | False | True | 16 |
| MarketStructureProfile | compression | bool |  |  | False | True | 17 |
| MarketStructureProfile | confidence_score | float |  |  | 0.0 | True | 18 |
| MarketStructureProfile | trap_detected | bool |  |  | False | True | 19 |
| MarketStructureProfile | liquidity_sweep | bool |  |  | False | True | 20 |
| MarketStructureProfile | breakout | bool |  |  | False | True | 21 |
| MarketStructureProfile | false_breakout | bool |  |  | False | True | 22 |
| MarketStructureProfile | market_shift | bool |  |  | False | True | 23 |
| MarketStructureProfile | pullback | bool |  |  | False | True | 24 |
| MarketStructureProfile | retracement_quality | float |  |  | 0.0 | True | 25 |
| MarketStructureProfile | impulse_strength | float |  |  | 0.0 | True | 26 |
| MarketStructureProfile | equal_highs | bool |  |  | False | True | 27 |
| MarketStructureProfile | equal_lows | bool |  |  | False | True | 28 |
| MarketStructureProfile | internal_bos | bool |  |  | False | True | 29 |
| MarketStructureProfile | external_bos | bool |  |  | False | True | 30 |
| MarketStructureProfile | last_confirmed_high | float |  |  | 0.0 | True | 31 |
| MarketStructureProfile | last_confirmed_low | float |  |  | 0.0 | True | 32 |
| MarketStructureProfile | current_sequence | List[str] |  |  | field(default_factory=list) | True | 33 |
| MarketStructureProfile | bos | bool |  |  | False | True | 35 |
| MarketStructureProfile | choch | bool |  |  | False | True | 36 |
| MarketStructureProfile | mss | bool |  |  | False | True | 37 |
| MarketStructureProfile | break_strength | float |  |  | 0.0 | True | 38 |
| MarketStructureProfile | break_price | float |  |  | 0.0 | True | 39 |
| MarketStructureProfile | break_timestamp | str |  |  | '' | True | 40 |
| MarketStructureProfile | current_swing | Optional[Swing] |  | ✓ | None | True | 41 |
| MarketStructureProfile | previous_swing | Optional[Swing] |  | ✓ | None | True | 42 |
| MarketStructureProfile | stop_hunt | bool |  |  | False | True | 45 |
| MarketStructureProfile | false_break | bool |  |  | False | True | 46 |
| MarketStructureProfile | reclaim | bool |  |  | False | True | 47 |
| MarketStructureProfile | buy_side_liquidity | float |  |  | 0.0 | True | 48 |
| MarketStructureProfile | sell_side_liquidity | float |  |  | 0.0 | True | 49 |
| MarketStructureProfile | internal_liquidity | float |  |  | 0.0 | True | 50 |
| MarketStructureProfile | external_liquidity | float |  |  | 0.0 | True | 51 |
| MarketStructureProfile | liquidity_cluster | float |  |  | 0.0 | True | 52 |
| MarketStructureProfile | correction_strength | float |  |  | 0.0 | True | 55 |
| MarketStructureProfile | expansion_ratio | float |  |  | 0.0 | True | 56 |
| MarketStructureProfile | compression_ratio | float |  |  | 0.0 | True | 57 |
| MarketStructureProfile | momentum_state | str |  |  | 'NEUTRAL' | True | 58 |
| MarketStructureProfile | displacement | bool |  |  | False | True | 61 |
| MarketStructureProfile | displacement_strength | float |  |  | 0.0 | True | 62 |
| MarketStructureProfile | displacement_direction | str |  |  | 'NEUTRAL' | True | 63 |
| MarketStructureProfile | premium_zone | float |  |  | 0.0 | True | 66 |
| MarketStructureProfile | discount_zone | float |  |  | 0.0 | True | 67 |
| MarketStructureProfile | equilibrium | float |  |  | 0.0 | True | 68 |
| MarketStructureProfile | ote | float |  |  | 0.0 | True | 69 |
| MarketThesis | market_bias | str | ✓ |  |  | True | 9 |
| MarketThesis | confluence_score | float | ✓ |  |  | True | 10 |
| MarketThesis | confidence | ConfidenceResult | ✓ |  |  | True | 11 |
| MarketThesis | risk | RiskAssessment | ✓ |  |  | True | 12 |
| MarketThesis | market_state | MarketState | ✓ |  |  | True | 13 |
| MarketThesis | confirmations | List[str] |  |  | field(default_factory=list) | True | 14 |
| MarketThesis | conflicts | List[str] |  |  | field(default_factory=list) | True | 15 |
| MarketThesis | institutional_alignment | bool |  |  | False | True | 16 |
| MarketThesis | opportunity_grade | str |  |  | 'C' | True | 17 |
| MemoryAuditResult | peak_memory_diff | int | ✓ |  |  | True | 14 |
| MemoryAuditResult | allocation_diff_size | int | ✓ |  |  | True | 15 |
| MemoryAuditResult | allocation_diff_count | int | ✓ |  |  | True | 16 |
| MemoryAuditResult | gc_count_diff | int | ✓ |  |  | True | 17 |
| MemoryAuditResult | top_stats | List[str] | ✓ |  |  | True | 18 |
| MemorySnapshot | snapshot | tracemalloc.Snapshot | ✓ |  |  | True | 8 |
| MemorySnapshot | gc_count | int | ✓ |  |  | True | 9 |
| MemorySnapshot | timestamp | float |  |  | field(default_factory=time.time) | True | 10 |
| MomentumAnalysis | engine_name | str |  |  | 'MomentumEngine' | True | 7 |
| MomentumAnalysis | rsi | float |  |  | 0.0 | True | 8 |
| MomentumAnalysis | macd | float |  |  | 0.0 | True | 9 |
| MomentumAnalysis | macd_signal | float |  |  | 0.0 | True | 10 |
| MomentumAnalysis | roc | float |  |  | 0.0 | True | 11 |
| MomentumAnalysis | strength | float |  |  | 0.0 | True | 12 |
| MomentumAnalysis | is_divergence | bool |  |  | False | True | 13 |
| MomentumAnalysis | is_exhaustion | bool |  |  | False | True | 14 |
| MomentumAnalysis | confidence | float |  |  | 0.0 | True | 15 |
| MomentumAnalysis | quality | float |  |  | 0.0 | True | 16 |
| MomentumAnalysis | evidences | Tuple[Evidence, ...] |  |  | field(default_factory=tuple) | True | 17 |
| MomentumAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 18 |
| MTFConsensus | global_bias | str | ✓ |  |  | True | 5 |
| MTFConsensus | local_bias | str | ✓ |  |  | True | 6 |
| MTFConsensus | conflict_detected | bool | ✓ |  |  | True | 7 |
| MTFConsensus | alignment_score | float | ✓ |  |  | True | 8 |
| MTFConsensus | conflict_score | float |  |  | 0.0 | True | 9 |
| MTFConsensus | trend_alignment | float |  |  | 0.0 | True | 10 |
| MTFConsensus | liquidity_alignment | float |  |  | 0.0 | True | 11 |
| MTFConsensus | structure_alignment | float |  |  | 0.0 | True | 12 |
| MTFConsensus | volatility_alignment | float |  |  | 0.0 | True | 13 |
| MTFConsensus | dominant_trend | str |  |  | 'NEUTRAL' | True | 14 |
| MTFConsensus | institutional_consensus_strength | float |  |  | 0.0 | True | 15 |
| MTFConsensus | summary | str |  |  | '' | True | 16 |
| HotspotReport | pipeline_name | str | ✓ |  |  | True | 20 |
| HotspotReport | total_duration | float | ✓ |  |  | True | 21 |
| HotspotReport | hotspots | Tuple[str, ...] | ✓ |  |  | True | 22 |
| PipelineMetric | pipeline_name | str | ✓ |  |  | True | 14 |
| PipelineMetric | total_duration | float | ✓ |  |  | True | 15 |
| PipelineMetric | stage_metrics | Tuple[StageMetric, ...] | ✓ |  |  | True | 16 |
| StageMetric | name | str | ✓ |  |  | True | 6 |
| StageMetric | duration | float | ✓ |  |  | True | 7 |
| StageMetric | memory_delta | int | ✓ |  |  | True | 8 |
| StageMetric | percentage_total | float | ✓ |  |  | True | 9 |
| StageMetric | nested_metrics | Tuple['StageMetric', ...] | ✓ |  |  | True | 10 |
| PerformanceMetrics | total_trades | int | ✓ |  |  | True | 6 |
| PerformanceMetrics | correct | int | ✓ |  |  | True | 7 |
| PerformanceMetrics | incorrect | int | ✓ |  |  | True | 8 |
| PerformanceMetrics | late_entries | int | ✓ |  |  | True | 9 |
| PerformanceMetrics | early_entries | int | ✓ |  |  | True | 10 |
| PerformanceMetrics | missed_trades | int | ✓ |  |  | True | 11 |
| PerformanceMetrics | false_positives | int | ✓ |  |  | True | 12 |
| PerformanceMetrics | false_negatives | int | ✓ |  |  | True | 13 |
| PerformanceMetrics | engine_responsibility | Dict[str, int] | ✓ |  |  | True | 14 |
| PerformanceMetrics | evidence_responsibility | Dict[str, int] | ✓ |  |  | True | 15 |
| PriceActionAnalysis | trend_structure | str | ✓ |  |  | True | 7 |
| PriceActionAnalysis | last_event | str | ✓ |  |  | True | 8 |
| PriceActionAnalysis | confidence | int | ✓ |  |  | True | 9 |
| PriceActionAnalysis | explanation | list[str] | ✓ |  |  | True | 10 |
| PriceActionAnalysis | engine_name | str |  |  | 'PriceActionEngine' | True | 6 |
| PriceActionAnalysis | is_strong_candle | bool |  |  | False | True | 7 |
| PriceActionAnalysis | is_weak_candle | bool |  |  | False | True | 8 |
| PriceActionAnalysis | is_engulfing | bool |  |  | False | True | 9 |
| PriceActionAnalysis | is_pin_bar | bool |  |  | False | True | 10 |
| PriceActionAnalysis | is_inside_bar | bool |  |  | False | True | 11 |
| PriceActionAnalysis | is_outside_bar | bool |  |  | False | True | 12 |
| PriceActionAnalysis | is_false_breakout | bool |  |  | False | True | 13 |
| PriceActionAnalysis | is_pullback | bool |  |  | False | True | 14 |
| PriceActionAnalysis | is_rejection | bool |  |  | False | True | 15 |
| PriceActionAnalysis | is_continuation | bool |  |  | False | True | 16 |
| PriceActionAnalysis | is_exhaustion | bool |  |  | False | True | 17 |
| PriceActionAnalysis | confidence | float |  |  | 0.0 | True | 18 |
| PriceActionAnalysis | quality | float |  |  | 0.0 | True | 19 |
| PriceActionAnalysis | evidences | Tuple[Any, ...] |  |  | field(default_factory=tuple) | True | 20 |
| PriceActionAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 21 |
| ProbabilityResult | buy_probability | float | ✓ |  |  | True | 6 |
| ProbabilityResult | sell_probability | float | ✓ |  |  | True | 7 |
| ProbabilityResult | neutral_probability | float | ✓ |  |  | True | 8 |
| ProbabilityResult | expected_risk | float | ✓ |  |  | True | 9 |
| ProbabilityResult | opportunity_grade | str | ✓ |  |  | True | 10 |
| ProbabilityResult | institutional_confidence | float | ✓ |  |  | True | 11 |
| ProbabilityResult | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 12 |
| ProfessionalThesis | market_bias | str | ✓ |  |  | True | 6 |
| ProfessionalThesis | opportunity_grade | str | ✓ |  |  | True | 7 |
| ProfessionalThesis | confidence | int | ✓ |  |  | True | 8 |
| ProfessionalThesis | institutional_alignment | bool | ✓ |  |  | True | 9 |
| ProfessionalThesis | confirmations | List[str] |  |  | field(default_factory=list) | True | 10 |
| ProfessionalThesis | conflicts | List[str] |  |  | field(default_factory=list) | True | 11 |
| ProfessionalThesis | risk_factors | List[str] |  |  | field(default_factory=list) | True | 12 |
| ProfessionalThesis | summary | str |  |  | '' | True | 13 |
| ProfessionalThesis | full_report | str |  |  | '' | True | 14 |
| ProfessionalThesis | decision_tree | Dict[str, Any] |  |  | field(default_factory=dict) | True | 15 |
| HotspotSummary | pipeline_name | str | ✓ |  |  | True | 21 |
| HotspotSummary | hotspots | Tuple[str, ...] | ✓ |  |  | True | 22 |
| PipelineProfile | pipeline_name | str | ✓ |  |  | True | 15 |
| PipelineProfile | total_duration | float | ✓ |  |  | True | 16 |
| PipelineProfile | stage_profiles | Tuple[StageProfile, ...] | ✓ |  |  | True | 17 |
| StageProfile | name | str | ✓ |  |  | True | 6 |
| StageProfile | duration | float | ✓ |  |  | True | 7 |
| StageProfile | memory_peak | int | ✓ |  |  | True | 8 |
| StageProfile | memory_delta | int | ✓ |  |  | True | 9 |
| StageProfile | percentage_total | float | ✓ |  |  | True | 10 |
| StageProfile | nested_stages | Tuple['StageProfile', ...] |  |  | field(default_factory=tuple) | True | 11 |
| BenchmarkMetrics | timestamp | float | ✓ |  |  | True | 6 |
| BenchmarkMetrics | duration | float | ✓ |  |  | True | 7 |
| BenchmarkMetrics | peak_memory | int | ✓ |  |  | True | 8 |
| BenchmarkMetrics | allocation_count | int | ✓ |  |  | True | 9 |
| BenchmarkMetrics | gc_count | int | ✓ |  |  | True | 10 |
| RegressionResult | is_regression | bool | ✓ |  |  | True | 14 |
| RegressionResult | performance_delta | float | ✓ |  |  | True | 15 |
| RegressionResult | memory_delta | float | ✓ |  |  | True | 16 |
| RegressionResult | allocation_delta | float | ✓ |  |  | True | 17 |
| RegressionResult | gc_delta | float | ✓ |  |  | True | 18 |
| RegressionResult | message | str | ✓ |  |  | True | 19 |
| RiskAssessment | suggested_stop | float | ✓ |  |  | True | 8 |
| RiskAssessment | suggested_take_profit | float | ✓ |  |  | True | 9 |
| RiskAssessment | risk_reward_ratio | float | ✓ |  |  | True | 10 |
| RiskAssessment | expected_drawdown | float | ✓ |  |  | True | 11 |
| RiskAssessment | expected_volatility | float | ✓ |  |  | True | 12 |
| RiskAssessment | trade_quality | float | ✓ |  |  | True | 13 |
| RiskAssessment | max_exposure | float | ✓ |  |  | True | 14 |
| RiskAssessment | invalidation_point | float | ✓ |  |  | True | 15 |
| RiskAssessment | institutional_risk_score | float | ✓ |  |  | True | 16 |
| RiskAssessment | var_95 | float |  |  | 0.0 | True | 19 |
| RiskAssessment | var_99 | float |  |  | 0.0 | True | 20 |
| RiskAssessment | cvar_95 | float |  |  | 0.0 | True | 21 |
| RiskAssessment | kelly_fraction | float |  |  | 0.0 | True | 24 |
| RiskAssessment | kelly_half | float |  |  | 0.0 | True | 25 |
| RiskAssessment | kelly_quarter | float |  |  | 0.0 | True | 26 |
| RiskAssessment | correlation_matrix | Optional[Tuple[Tuple[float, ...], ...]] |  | ✓ | None | True | 29 |
| RiskAssessment | stress_test_loss | float |  |  | 0.0 | True | 30 |
| SessionAnalysis | session | Optional[str] |  | ✓ | None | True | 6 |
| SessionAnalysis | overlap | Optional[bool] |  | ✓ | None | True | 7 |
| SessionAnalysis | quality | Optional[float] |  | ✓ | None | True | 8 |
| SessionAnalysis | liquidity_score | Optional[float] |  | ✓ | None | True | 9 |
| SessionAnalysis | explanation | Optional[str] |  | ✓ | None | True | 10 |
| Signal | asset | str | ✓ |  |  | True | 12 |
| Signal | action | str | ✓ |  |  | True | 14 |
| Signal | confidence | float | ✓ |  |  | True | 16 |
| Signal | score | float | ✓ |  |  | True | 18 |
| Signal | entry | float | None |  |  | None | True | 20 |
| Signal | stop_loss | float | None |  |  | None | True | 22 |
| Signal | take_profit | float | None |  |  | None | True | 24 |
| Signal | timeframe | str |  |  | DEFAULT_TIMEFRAME | True | 26 |
| Signal | strategy | str |  |  | '' | True | 28 |
| Signal | evidences | List[str] |  |  | field(default_factory=list) | True | 30 |
| Signal | explanation | str |  |  | '' | True | 32 |
| SmartMoneyAnalysis | structure | MarketStructure | ✓ |  |  | True | 9 |
| SmartMoneyAnalysis | score | int |  |  | 0 | True | 11 |
| SmartMoneyAnalysis | confidence | int |  |  | 0 | True | 12 |
| SmartMoneyAnalysis | institutional_score | float |  |  | 0.0 | True | 13 |
| SmartMoneyAnalysis | explanation | list[str] |  |  | field(default_factory=list) | True | 14 |
| StressTestResult | pipeline_name | str | ✓ |  |  | True | 7 |
| StressTestResult | scenario | str | ✓ |  |  | True | 8 |
| StressTestResult | dataset_size | int | ✓ |  |  | True | 9 |
| StressTestResult | repetitions | int | ✓ |  |  | True | 10 |
| StressTestResult | runtimes | List[float] | ✓ |  |  | True | 11 |
| StressTestResult | peak_memory | List[int] | ✓ |  |  | True | 12 |
| StressTestResult | exceptions | List[Exception] | ✓ |  |  | True | 13 |
| StressTestResult | is_deterministic | bool | ✓ |  |  | True | 14 |
| StressTestResult | failure_count | int | ✓ |  |  | True | 15 |
| SupportResistanceAnalysis | support | float | ✓ |  |  | True | 7 |
| SupportResistanceAnalysis | resistance | float | ✓ |  |  | True | 8 |
| SupportResistanceAnalysis | distance_support | float | ✓ |  |  | True | 9 |
| SupportResistanceAnalysis | distance_resistance | float | ✓ |  |  | True | 10 |
| SupportResistanceAnalysis | explanation | list[str] | ✓ |  |  | True | 11 |
| SupportResistanceAnalysis | support | Optional[float] |  | ✓ | None | True | 6 |
| SupportResistanceAnalysis | resistance | Optional[float] |  | ✓ | None | True | 7 |
| SupportResistanceAnalysis | nearest_support | Optional[float] |  | ✓ | None | True | 8 |
| SupportResistanceAnalysis | nearest_resistance | Optional[float] |  | ✓ | None | True | 9 |
| SupportResistanceAnalysis | distance_to_support_atr | Optional[float] |  | ✓ | None | True | 10 |
| SupportResistanceAnalysis | distance_to_resistance_atr | Optional[float] |  | ✓ | None | True | 11 |
| SupportResistanceAnalysis | support_strength | Optional[float] |  | ✓ | None | True | 12 |
| SupportResistanceAnalysis | resistance_strength | Optional[float] |  | ✓ | None | True | 13 |
| SupportResistanceAnalysis | price_location | Optional[str] |  | ✓ | None | True | 14 |
| SupportResistanceAnalysis | explanation | Optional[str] |  | ✓ | None | True | 15 |
| Swing | type | str | ✓ |  |  | True | 6 |
| Swing | classification | str | ✓ |  |  | True | 7 |
| Swing | price | float | ✓ |  |  | True | 8 |
| Swing | timestamp | str | ✓ |  |  | True | 9 |
| Swing | index | int | ✓ |  |  | True | 10 |
| Swing | atr | float | ✓ |  |  | True | 11 |
| Swing | strength | float | ✓ |  |  | True | 12 |
| Swing | volume | float | ✓ |  |  | True | 13 |
| Swing | confirmed | bool |  |  | True | True | 14 |
| Swing | distance_from_previous | float |  |  | 0.0 | True | 15 |
| SwingSequenceResult | current_swing | Optional[Swing] |  | ✓ | None | True | 19 |
| SwingSequenceResult | previous_swing | Optional[Swing] |  | ✓ | None | True | 20 |
| SwingSequenceResult | sequence | List[str] |  |  | field(default_factory=list) | True | 21 |
| SwingSequenceResult | sequence_length | int |  |  | 0 | True | 22 |
| SwingSequenceResult | sequence_quality | float |  |  | 0.0 | True | 23 |
| SwingSequenceResult | sequence_confidence | float |  |  | 0.0 | True | 24 |
| SwingSequenceResult | trend_direction | str |  |  | 'NEUTRAL' | True | 25 |
| SwingSequenceResult | trend_transition | bool |  |  | False | True | 26 |
| TradeFilterResult | allowed | bool | ✓ |  |  | True | 15 |
| TradeFilterResult | reasons | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 18 |
| TradeFilterResult | quality_score | float |  |  | 0.0 | True | 21 |
| TradeFilterResult | quality_level | str |  |  | 'N/A' | True | 24 |
| TradeMemory | timestamp | str | ✓ |  |  | True | 7 |
| TradeMemory | context_snapshot | Dict[str, Any] | ✓ |  |  | True | 8 |
| TradeMemory | evidences | List[str] | ✓ |  |  | True | 9 |
| TradeMemory | decision | str | ✓ |  |  | True | 10 |
| TradeMemory | result | str | ✓ |  |  | True | 11 |
| TradeMemory | mae | float | ✓ |  |  | True | 12 |
| TradeMemory | mfe | float | ✓ |  |  | True | 13 |
| TradeMemory | drawdown | float | ✓ |  |  | True | 14 |
| TradeMemory | profit | float | ✓ |  |  | True | 15 |
| TradeMemory | time_to_close | float | ✓ |  |  | True | 16 |
| TradeMemory | session | str | ✓ |  |  | True | 17 |
| TradeMemory | regime | str | ✓ |  |  | True | 18 |
| TradePermission | status | Optional[str] |  | ✓ | None | True | 6 |
| TradePermission | confidence | Optional[float] |  | ✓ | None | True | 7 |
| TradePermission | reasons | list[str] |  |  | field(default_factory=list) | True | 8 |
| TradingExplanation | exec_summary | str | ✓ |  |  | True | 9 |
| TradingExplanation | decision_rationale | str | ✓ |  |  | True | 10 |
| TradingExplanation | market_context | str | ✓ |  |  | True | 11 |
| TradingExplanation | trend_context | str | ✓ |  |  | True | 12 |
| TradingExplanation | liquidity_context | str | ✓ |  |  | True | 13 |
| TradingExplanation | structure_context | str | ✓ |  |  | True | 14 |
| TradingExplanation | momentum_context | str | ✓ |  |  | True | 15 |
| TradingExplanation | volume_context | str | ✓ |  |  | True | 16 |
| TradingExplanation | smart_money_context | str | ✓ |  |  | True | 17 |
| TradingExplanation | confluence_context | str | ✓ |  |  | True | 18 |
| TradingExplanation | risk_assessment | str | ✓ |  |  | True | 19 |
| TradingExplanation | confidence_rationale | str | ✓ |  |  | True | 20 |
| TradingExplanation | strong_evidences | Tuple[str, ...] |  |  | () | True | 21 |
| TradingExplanation | weak_evidences | Tuple[str, ...] |  |  | () | True | 22 |
| TradingExplanation | missing_confirmations | Tuple[str, ...] |  |  | () | True | 23 |
| TradingExplanation | detected_risks | Tuple[str, ...] |  |  | () | True | 24 |
| TradingExplanation | bullish_factors | Tuple[str, ...] |  |  | () | True | 25 |
| TradingExplanation | bearish_factors | Tuple[str, ...] |  |  | () | True | 26 |
| TradingExplanation | neutral_factors | Tuple[str, ...] |  |  | () | True | 27 |
| TradingExplanation | conflicts | Tuple[str, ...] |  |  | () | True | 28 |
| TradingExplanation | logical_sequence | Tuple[str, ...] |  |  | () | True | 29 |
| TradingExplanation | risk_analysis | str |  |  | '' | True | 30 |
| TradingExplanation | institutional_context | str |  |  | '' | True | 31 |
| TradingExplanation | suggested_entry | Any |  |  | None | True | 32 |
| TradingExplanation | suggested_stop | Any |  |  | None | True | 33 |
| TradingExplanation | suggested_targets | Tuple[Any, ...] |  |  | () | True | 34 |
| TradingExplanation | confidence_explanation | str |  |  | '' | True | 35 |
| TradingExplanation | machine_readable | Dict[str, Any] |  |  | field(default_factory=dict) | True | 36 |
| TradingExplanation | engine_weights | Dict[str, float] |  |  | field(default_factory=dict) | True | 37 |
| TradingExplanation | warnings | Tuple[str, ...] |  |  | () | True | 38 |
| TrendAnalysis | engine_name | str |  |  | 'TrendEngine' | True | 6 |
| TrendAnalysis | is_hh_hl | bool |  |  | False | True | 7 |
| TrendAnalysis | is_lh_ll | bool |  |  | False | True | 8 |
| TrendAnalysis | ema20 | float |  |  | 0.0 | True | 9 |
| TrendAnalysis | ema50 | float |  |  | 0.0 | True | 10 |
| TrendAnalysis | ema200 | float |  |  | 0.0 | True | 11 |
| TrendAnalysis | adx | float |  |  | 0.0 | True | 12 |
| TrendAnalysis | trend_strength | float |  |  | 0.0 | True | 13 |
| TrendAnalysis | trend_quality | float |  |  | 0.0 | True | 14 |
| TrendAnalysis | trend_confidence | float |  |  | 0.0 | True | 15 |
| TrendAnalysis | is_consolidation | bool |  |  | False | True | 16 |
| TrendAnalysis | is_expansion | bool |  |  | False | True | 17 |
| TrendAnalysis | evidences | Tuple[Any, ...] |  |  | field(default_factory=tuple) | True | 18 |
| TrendAnalysis | warnings | Tuple[str, ...] |  |  | field(default_factory=tuple) | True | 19 |
| TrendAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 20 |
| VersionMetadata | engine_version | str | ✓ |  |  | True | 5 |
| VersionMetadata | pipeline_version | str | ✓ |  |  | True | 6 |
| VersionMetadata | context_version | str | ✓ |  |  | True | 7 |
| VersionMetadata | weights_version | str | ✓ |  |  | True | 8 |
| VolatilityAnalysis | state | Optional[str] |  | ✓ | None | True | 7 |
| VolatilityAnalysis | score | Optional[float] |  | ✓ | None | True | 8 |
| VolatilityAnalysis | expanding | Optional[bool] |  | ✓ | None | True | 9 |
| VolatilityAnalysis | contracting | Optional[bool] |  | ✓ | None | True | 10 |
| VolatilityAnalysis | evidences | Tuple[Evidence, ...] |  |  | () | True | 11 |
| VolumeAnalysis | engine_name | str |  |  | 'VolumeEngine' | True | 7 |
| VolumeAnalysis | relative_volume | float |  |  | 0.0 | True | 8 |
| VolumeAnalysis | is_volume_spike | bool |  |  | False | True | 9 |
| VolumeAnalysis | is_absorption | bool |  |  | False | True | 10 |
| VolumeAnalysis | is_distribution | bool |  |  | False | True | 11 |
| VolumeAnalysis | is_accumulation | bool |  |  | False | True | 12 |
| VolumeAnalysis | is_climax | bool |  |  | False | True | 13 |
| VolumeAnalysis | volume_trend | str |  |  | 'NEUTRAL' | True | 14 |
| VolumeAnalysis | confidence | float |  |  | 0.0 | True | 15 |
| VolumeAnalysis | quality | float |  |  | 0.0 | True | 16 |
| VolumeAnalysis | evidences | Tuple[Evidence, ...] |  |  | field(default_factory=tuple) | True | 17 |
| VolumeAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 18 |
| VolumeProfile | relative_volume | float |  |  | 1.0 | True | 5 |
| VolumeProfile | volume_spike | bool |  |  | False | True | 6 |
| VolumeProfile | buying_climax | bool |  |  | False | True | 7 |
| VolumeProfile | selling_climax | bool |  |  | False | True | 8 |
| VolumeProfile | absorption | bool |  |  | False | True | 9 |
| VolumeProfile | effort_vs_result | float |  |  | 0.0 | True | 10 |
| VolumeProfile | dry_volume | bool |  |  | False | True | 11 |
| VolumeProfile | trend_confirmation | bool |  |  | False | True | 12 |
| VolumeProfile | volume_divergence | bool |  |  | False | True | 13 |
| VolumeProfile | institutional_participation | float |  |  | 0.0 | True | 14 |
| VolumeProfile | confidence_score | float |  |  | 0.0 | True | 15 |
| VolumeProfile | participation_quality | float |  |  | 0.0 | True | 16 |
| VolumeProfile | volume_consistency | float |  |  | 0.0 | True | 17 |
| VolumeProfile | exhaustion_volume | bool |  |  | False | True | 18 |
| VWAPAnalysis | engine_name | str |  |  | 'VWAPEngine' | True | 7 |
| VWAPAnalysis | vwap | float |  |  | 0.0 | True | 8 |
| VWAPAnalysis | distance_to_vwap | float |  |  | 0.0 | True | 9 |
| VWAPAnalysis | is_accepted | bool |  |  | False | True | 10 |
| VWAPAnalysis | is_rejected | bool |  |  | False | True | 11 |
| VWAPAnalysis | is_mean_reversion | bool |  |  | False | True | 12 |
| VWAPAnalysis | institutional_bias | str |  |  | 'NEUTRAL' | True | 13 |
| VWAPAnalysis | confidence | float |  |  | 0.0 | True | 14 |
| VWAPAnalysis | quality | float |  |  | 0.0 | True | 15 |
| VWAPAnalysis | evidences | Tuple[Evidence, ...] |  |  | field(default_factory=tuple) | True | 16 |
| VWAPAnalysis | metadata | Dict[str, Any] |  |  | field(default_factory=dict) | True | 17 |

## Serialization Contract Matrix

| Dataclass | __post_init__ | to_dict | from_dict | Asymmetric |
|-----------|---------------|---------|-----------|------------|
| BuyAndHoldBaseline |  |  |  |  |
| EnhancedBenchmarkReport |  |  |  |  |
| StatisticalTestResult |  |  |  |  |
| ConfidenceComponents |  |  |  |  |
| QualityReport |  |  |  |  |
| DecisionExplainability |  |  |  |  |
| DecisionResolverResult |  |  |  |  |
| HealthStatus |  |  |  |  |
| InstitutionalContext |  |  |  |  |
| InstitutionalContribution |  |  |  |  |
| InstitutionalScoreResult |  |  |  |  |
| PerformanceMetrics |  |  |  |  |
| Notification |  |  |  |  |
| BatchReplayReport |  |  |  |  |
| BatchReplayResult |  |  |  |  |
| BOSResult |  |  |  |  |
| CHOCHResult |  |  |  |  |
| EqualHighGroup |  |  |  |  |
| EqualHighMetrics |  |  |  |  |
| EqualHighScore |  |  |  |  |
| LiquidityEvent |  |  |  |  |
| UniverseAsset |  |  |  |  |
| Asset |  |  |  |  |
| AuditEvent |  |  |  |  |
| EngineResult |  |  |  |  |
| DataQualityResult |  |  |  |  |
| RuntimeReport |  | ✓ |  | ⚠️ |
| TelemetryData |  |  |  |  |
| AuditEvent |  |  |  |  |
| ProviderHealth |  |  |  |  |
| ProviderMetrics |  |  |  |  |
| ProviderPriority |  |  |  |  |
| ProviderRegistry |  |  |  |  |
| ReplayMetrics |  |  |  |  |
| AnalysisResult |  |  |  |  |
| BenchmarkReport |  |  |  |  |
| BenchmarkRunResult |  |  |  |  |
| CandlestickAnalysis |  |  |  |  |
| ConfidenceResult |  |  |  |  |
| ConfluenceResult |  |  |  |  |
| ConfluenceScore |  |  |  |  |
| DataQualityResult |  |  |  |  |
| DecisionInput |  |  |  |  |
| DecisionNode |  |  |  |  |
| DecisionOutcome |  |  |  |  |
| DecisionResult |  |  |  |  |
| DecisionSnapshot |  |  |  |  |
| DecisionTrace |  |  |  |  |
| AssetPerformance |  |  |  |  |
| UniversePerformance |  |  |  |  |
| Evidence |  |  |  |  |
| EvidenceRankingResult |  |  |  |  |
| FairValueGapAnalysis |  |  |  |  |
| LiquidityAnalysis |  |  |  |  |
| LiquidityProfile |  |  |  |  |
| LiquidityResult |  |  |  |  |
| MarketCondition |  |  |  |  |
| MarketContext |  |  |  |  |
| MarketData |  |  |  |  |
| MarketEvidenceBundle |  |  |  |  |
| MarketRegime |  |  |  |  |
| MarketState |  |  |  |  |
| MarketStructure |  |  |  |  |
| MarketStructureProfile |  |  |  |  |
| MarketThesis |  |  |  |  |
| MemoryAuditResult |  |  |  |  |
| MemorySnapshot |  |  |  |  |
| MomentumAnalysis |  |  |  |  |
| MTFConsensus |  |  |  |  |
| HotspotReport |  |  |  |  |
| PipelineMetric |  |  |  |  |
| StageMetric |  |  |  |  |
| PerformanceMetrics |  |  |  |  |
| PriceActionAnalysis |  |  |  |  |
| PriceActionAnalysis |  |  |  |  |
| ProbabilityResult |  |  |  |  |
| ProfessionalThesis |  |  |  |  |
| HotspotSummary |  |  |  |  |
| PipelineProfile |  |  |  |  |
| StageProfile |  |  |  |  |
| BenchmarkMetrics |  |  |  |  |
| RegressionResult |  |  |  |  |
| RiskAssessment |  |  |  |  |
| SessionAnalysis |  |  |  |  |
| Signal |  |  |  |  |
| SmartMoneyAnalysis |  |  |  |  |
| StressTestResult |  |  |  |  |
| SupportResistanceAnalysis |  |  |  |  |
| SupportResistanceAnalysis |  |  |  |  |
| Swing |  |  |  |  |
| SwingSequenceResult |  |  |  |  |
| TradeFilterResult |  |  |  |  |
| TradeMemory |  |  |  |  |
| TradePermission |  |  |  |  |
| TradingExplanation |  |  |  |  |
| TrendAnalysis |  |  |  |  |
| VersionMetadata |  |  |  |  |
| VolatilityAnalysis |  |  |  |  |
| VolumeAnalysis |  |  |  |  |
| VolumeProfile |  |  |  |  |
| VWAPAnalysis |  |  |  |  |

## Field Usage Across Modules

| Field | Defined In | Used In Modules |
|-------|------------|-----------------|
| ATR_consistency | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| ATRs | EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| absorption | VolumeProfile | mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.volume_intelligence_engine |
| action | AuditEvent, Signal | mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.security_center |
| adx | MarketData, TrendAnalysis | mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| age_in_swings | EqualHighMetrics, EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| aggregate_cache_stats | BatchReplayReport | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor |
| agreement_percentage | ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| alignment_score | MTFConsensus | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| allocation_count | BenchmarkMetrics | mercury_ai.utils.regression_detector |
| allocation_delta | RegressionResult | mercury_ai.utils.regression_detector |
| allocation_diff_count | MemoryAuditResult | mercury_ai.utils.memory_auditor |
| allocation_diff_size | MemoryAuditResult | mercury_ai.utils.memory_auditor |
| allowed | DataQualityResult, TradeFilterResult | mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| asset | DecisionSnapshot, AssetPerformance, MarketEvidenceBundle, Signal | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, mercury_ai.database.snapshot_logger, tests.test_confidence_calibration, tests.test_institutional_backtest, tests.test_probability_engine, tests.test_validation_engine, tests.test_versioning |
| asset_performance | BatchReplayResult | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| asset_performances | EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| asset_stats | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, tests.test_institutional_backtest |
| atr | MarketData, Swing | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_benchmark_integration |
| atr_score | EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| audit_events | DecisionSnapshot | mercury_ai.core.analysis_pipeline, tests.test_robustness, tests.test_versioning |
| audit_id | DecisionOutcome, DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.historical_replay_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_determinism |
| average_ATR | EqualHighMetrics, EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| average_execution_time | EnhancedBenchmarkReport, BenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| average_price | EqualHighMetrics, EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| average_quality | ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| average_strength | EqualHighMetrics, EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| avg_loss | PerformanceMetrics, AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor |
| avg_win | PerformanceMetrics, AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor |
| bearish_factors | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| bearish_score | ConfluenceScore, EvidenceRankingResult | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.market_thesis_builder, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| bearish_weight | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| benchmark_outperformance_pct | BuyAndHoldBaseline | mercury_ai.analysis.benchmark_framework |
| blockers | DecisionInput, DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| body_strength | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine |
| bollinger_lower | MarketData | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| bollinger_upper | MarketData | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| bootstrap_ci_lower | StatisticalTestResult | mercury_ai.analysis.benchmark_framework |
| bootstrap_ci_upper | StatisticalTestResult | mercury_ai.analysis.benchmark_framework |
| bootstrap_samples | StatisticalTestResult | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| bos | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| bos_detected | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| break_price | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| break_strength | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| break_timestamp | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| breakout | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| bullish_factors | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.presentation.signal_formatter |
| bullish_score | ConfluenceScore, EvidenceRankingResult | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.market_thesis_builder, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| bullish_weight | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| buy_and_hold_baselines | EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| buy_probability | DecisionResult, ProbabilityResult | app.dashboard.dashboard, app.terminal.pages.01_Scanner, app.terminal.pages.06_Demo, mercury_ai.analysis.decision_result_builder, mercury_ai.brain.explainability_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, tests.test_determinism, tests.test_probability_engine, tests.test_scanner_recovery |
| buy_score | ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| buy_side_liquidity | MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| buying_climax | VolumeProfile | mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.volume_intelligence_engine |
| cache_stats | BatchReplayResult | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| candlestick_analysis | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| category | Asset | app.dashboard.asset_registry_panel, app.dashboard.market_map_panel, mercury_ai.core.asset_registry, tools.mercury_integrity_auditor.main |
| choch | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| choch_detected | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| clarity | DecisionResult | app.dashboard.dashboard, app.terminal.pages.01_Scanner, mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| clarity_score | ConfluenceScore | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_thesis_builder |
| classification | MarketStructureProfile, Swing | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| close | MarketData | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| cluster_density | EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| cluster_width | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| components | HealthStatus | app.dashboard.operation_center, mercury_ai.analysis.health_checker, tests.test_health_checker |
| compression | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| compression_ratio | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| confidence | DecisionExplainability, InstitutionalContext, InstitutionalContribution, BOSResult, CHOCHResult, LiquidityEvent, EngineResult, ConfluenceResult, DecisionInput, DecisionResult, Evidence, FairValueGapAnalysis, LiquidityAnalysis, LiquidityResult, MarketRegime, MarketStructure, MarketThesis, MomentumAnalysis, PriceActionAnalysis, PriceActionAnalysis, ProfessionalThesis, Signal, SmartMoneyAnalysis, TradePermission, VolumeAnalysis, VWAPAnalysis | app.dashboard.dashboard, app.dashboard.operation_center, app.terminal.pages.01_Scanner, app.terminal.pages.02_Dashboard, app.terminal.pages.06_Demo, mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.health_auditor, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.market_thesis_builder, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.validation_engine, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, mercury_ai.database.history_logger, mercury_ai.database.replay_storage, mercury_ai.operations.demo_manager, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_determinism, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_scanner_recovery, tests.test_validation_engine |
| confidence_explanation | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| confidence_grade | ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, tests.test_confidence_calibration |
| confidence_override | DecisionResolverResult | mercury_ai.analysis.decision_resolver_engine, mercury_ai.brain.mercury_decision_engine, test_bloco7_scenarios |
| confidence_rationale | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| confidence_score | InstitutionalScoreResult, ConfidenceResult, MarketStructureProfile, VolumeProfile | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.institutional_score_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.market_thesis_builder, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, tests.test_benchmark_integration, tests.test_confidence_calibration, tests.test_regression_sprint18 |
| confirmation_count | ConfidenceComponents, ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| confirmations | MarketThesis, ProfessionalThesis | mercury_ai.analysis.confluence_engine, mercury_ai.analysis.market_thesis_builder |
| confirmed | Swing | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration |
| conflict_detected | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| conflict_penalty | InstitutionalScoreResult, ConfluenceScore | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.institutional_score_engine, mercury_ai.brain.mercury_decision_engine |
| conflict_score | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| conflicting_signals | DecisionExplainability, ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| conflicts | TelemetryData, MarketThesis, ProfessionalThesis, TradingExplanation | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.market_thesis_builder, mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| confluence | AnalysisResult | mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, mercury_ai.database.history_logger, tests.test_versioning |
| confluence_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| confluence_score | InstitutionalScoreResult, ConfluenceScore, DecisionInput, MarketThesis | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.institutional_score_engine, mercury_ai.analysis.market_thesis_builder, mercury_ai.brain.mercury_decision_engine |
| consensus_factor | ConfidenceComponents | mercury_ai.analysis.confidence_engine |
| consensus_score | ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| consistency_issues | QualityReport | mercury_ai.analysis.data_quality_engine, tests.test_data_quality_engine |
| consolidated_equity_curve | UniversePerformance | mercury_ai.analysis.performance_engine |
| consumer | TelemetryData | mercury_ai.core.analysis_pipeline |
| context | AnalysisResult, CandlestickAnalysis, DecisionSnapshot | mercury_ai.analysis.candlestick_engine, mercury_ai.core.analysis_pipeline, tests.test_market_resilience, tests.test_versioning |
| context_score | CandlestickAnalysis, Evidence | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| context_version | VersionMetadata | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| continuation | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine |
| contracting | VolatilityAnalysis | mercury_ai.analysis.volatility_engine |
| contribution_percentage | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| contribution_score | Evidence | mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| contributions | DecisionExplainability | mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner |
| cool_down_trades_excluded | EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| correct | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| correction_strength | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| correlation_matrix | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| creator | TelemetryData | mercury_ai.core.analysis_pipeline |
| current_sequence | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| current_swing | MarketStructureProfile, SwingSequenceResult | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| cvar_95 | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline, tests.test_institutional_backtest |
| dataframe_size | TelemetryData | mercury_ai.core.analysis_pipeline |
| dataset_size | StressTestResult | mercury_ai.utils.stress_tester |
| decision | DecisionExplainability, DecisionResolverResult, AnalysisResult, DecisionResult, TradeMemory | app.dashboard.dashboard, app.dashboard.operation_center, app.terminal.pages.01_Scanner, app.terminal.pages.02_Dashboard, app.terminal.pages.06_Demo, mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.historical_replay_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.analysis.ranking_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, mercury_ai.database.history_logger, mercury_ai.database.replay_storage, mercury_ai.operations.demo_manager, mercury_ai.presentation.signal_formatter, test_bloco7_scenarios, tests.test_demo_page, tests.test_determinism, tests.test_market_resilience, tests.test_scanner_recovery, tests.test_versioning, verify_assets |
| decision_chain | DecisionExplainability | mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner |
| decision_rationale | TradingExplanation | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| decision_result | BenchmarkRunResult, DecisionSnapshot | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.historical_replay_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.core.analysis_pipeline, mercury_ai.database.replay_storage, tests.test_determinism, tests.test_versioning |
| delay_seconds | QualityReport | mercury_ai.analysis.data_quality_engine |
| density_score | EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| description | Evidence | mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine, tools.mercury_integrity_auditor.auditors.report, tools.mercury_integrity_auditor.main |
| detected | BOSResult, CHOCHResult | mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.smart_money_engine |
| detected_risks | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| deviation_score | EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| direction | InstitutionalContribution, BOSResult, CHOCHResult, Evidence | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.conflict_resolution_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.evidence_quality_engine, mercury_ai.analysis.evidence_query, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| discount_zone | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| displacement | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| displacement_direction | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| displacement_strength | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| display_name | UniverseAsset | mercury_ai.config.assets, mercury_ai.config.universe |
| disposer | TelemetryData | mercury_ai.core.analysis_pipeline |
| distance_from_previous | Swing | mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration |
| distance_to_resistance_atr | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| distance_to_support_atr | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| distance_to_vwap | VWAPAnalysis | mercury_ai.analysis.vwap_engine |
| dominant_direction | DecisionExplainability, ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| dominant_trend | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| dry_volume | VolumeProfile | mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.volume_intelligence_engine |
| duplicity_issues | QualityReport | mercury_ai.analysis.data_quality_engine, tests.test_data_quality_engine |
| duration | StageMetric, StageProfile, BenchmarkMetrics | mercury_ai.core._stage_builder, mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector, mercury_ai.utils.regression_detector |
| early_entries | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| effort_vs_result | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| ema21 | MarketData | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| ema50 | MarketData, TrendAnalysis | mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| ema9 | MarketData | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| enabled | UniverseAsset, Asset | app.dashboard.asset_registry_panel, mercury_ai.brain.scanner, mercury_ai.config.assets, mercury_ai.config.universe, mercury_ai.core.asset_registry, tests.test_broker_filtering, tests.test_scanner_priority |
| end_time | TelemetryData | mercury_ai.core._stage_builder, mercury_ai.core.analysis_pipeline, mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector |
| engine | DecisionNode | mercury_ai.analysis.decision_trace_engine, mercury_ai.utils.stress_tester, tests.test_performance_engine |
| engine_name | InstitutionalContribution, TelemetryData, Evidence, FairValueGapAnalysis, LiquidityAnalysis, MomentumAnalysis, PriceActionAnalysis, TrendAnalysis, VolumeAnalysis, VWAPAnalysis | app.dashboard.dashboard, mercury_ai.analysis.confidence_engine, mercury_ai.analysis.conflict_resolution_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.evidence_quality_engine, mercury_ai.analysis.evidence_query, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| engine_responsibility | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| engine_version | VersionMetadata | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| engine_weights | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| engulfing | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine |
| equal_highs | LiquidityProfile, MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| equal_lows | LiquidityProfile, MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| equilibrium | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| equity_curve | AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor |
| error | BatchReplayResult | main, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.brain.scanner, mercury_ai.operations.demo_manager, mercury_ai.providers.market_provider, tests.test_institutional_backtest |
| errors | BatchReplayReport | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor |
| event_type | LiquidityEvent | mercury_ai.analysis.smart_money.liquidity_event_engine |
| evidence | DecisionNode | mercury_ai.analysis.decision_trace_engine, tools.mercury_integrity_auditor.auditors.contract_certification_auditor, tools.mercury_integrity_auditor.auditors.report, tools.mercury_integrity_auditor.main |
| evidence_bundle | DecisionSnapshot | mercury_ai.analysis.institutional_memory_engine, mercury_ai.core.analysis_pipeline, tests.test_determinism, tests.test_versioning |
| evidence_count | TelemetryData | mercury_ai.core.analysis_pipeline |
| evidence_name | Evidence | app.dashboard.dashboard, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.evidence_query, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_momentum_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| evidence_ranking | AnalysisResult, DecisionResult, DecisionSnapshot | app.dashboard.dashboard, mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline, tests.test_determinism, tests.test_versioning |
| evidence_responsibility | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| evidences | EngineResult, CandlestickAnalysis, ConfluenceResult, FairValueGapAnalysis, LiquidityAnalysis, LiquidityResult, MarketEvidenceBundle, MomentumAnalysis, PriceActionAnalysis, Signal, TradeMemory, TrendAnalysis, VolatilityAnalysis, VolumeAnalysis, VWAPAnalysis | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_fvg_engine, mercury_ai.analysis.tests.test_momentum_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_volume_engine, mercury_ai.analysis.validation_engine, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, tests.test_confidence_calibration, tests.test_evidence_engine, tests.test_probability_engine, tests.test_validation_engine |
| exceptions | StressTestResult | mercury_ai.utils.stress_tester |
| exec_summary | TradingExplanation | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| execution_time | EngineResult, TelemetryData, BenchmarkRunResult | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.core.analysis_pipeline |
| exhaustion_volume | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| expanding | VolatilityAnalysis | mercury_ai.analysis.volatility_engine |
| expansion | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| expansion_ratio | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| expectancy | PerformanceMetrics, AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, tests.test_performance_engine |
| expected_drawdown | DecisionResult, RiskAssessment | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| expected_reward | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| expected_risk | DecisionResult, ProbabilityResult | mercury_ai.analysis.decision_result_builder, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline |
| expected_strength | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| expected_volatility | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| explainability | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.brain.scanner, mercury_ai.core.analysis_pipeline |
| explanation | InstitutionalContext, InstitutionalContribution, BOSResult, CHOCHResult, LiquidityEvent, CandlestickAnalysis, DecisionResult, MarketCondition, MarketState, MarketStructure, PriceActionAnalysis, SessionAnalysis, Signal, SmartMoneyAnalysis, SupportResistanceAnalysis, SupportResistanceAnalysis | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.session_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.support_resistance_analyzer, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_confidence_calibration |
| external_bos | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| external_liquidity | LiquidityProfile, MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| failed | BatchReplayReport | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| failure_count | StressTestResult | mercury_ai.utils.stress_tester |
| fallback_provider | Asset | app.dashboard.asset_registry_panel, mercury_ai.core.asset_registry |
| false_break | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| false_breakout | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| false_negatives | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| false_positives | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| favorite | Asset | mercury_ai.brain.scanner, mercury_ai.core.asset_registry |
| final_confidence | ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| final_decision | DecisionTrace | mercury_ai.analysis.decision_trace_engine |
| final_score | ConfidenceComponents, EqualHighScore, DecisionTrace | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.decision_trace_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| first_index | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| first_timestamp | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| fvg_quality | FairValueGapAnalysis | mercury_ai.analysis.fair_value_gap_engine |
| gc_count | MemorySnapshot, BenchmarkMetrics | mercury_ai.utils.memory_auditor, mercury_ai.utils.regression_detector |
| gc_count_diff | MemoryAuditResult | mercury_ai.utils.memory_auditor |
| gc_delta | RegressionResult | mercury_ai.utils.regression_detector |
| global_bias | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| global_max_drawdown | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick |
| global_pnl | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick, tests.test_institutional_backtest, tests.test_performance_engine |
| global_profit_factor | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick, tests.test_performance_engine |
| global_sharpe | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick |
| global_sortino | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick |
| global_win_rate | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick, tests.test_performance_engine |
| grade | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| has_equal_highs | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration |
| has_equal_lows | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine |
| has_liquidity_sweep | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine |
| has_liquidity_void | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine |
| has_stop_hunt | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine |
| health | ProviderRegistry | app.dashboard.provider_health_panel, mercury_ai.core.job_manager, mercury_ai.data.mercury_data_provider |
| hh_count | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| higher_high | MarketStructure | mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine |
| higher_low | MarketStructure | mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine |
| hit | ReplayMetrics | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.historical_replay_engine, mercury_ai.database.replay_storage, run_institutional_replay, scripts.run_replay_3500, test_replay_quick, tests.test_performance_engine |
| hl_count | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| hotspots | HotspotReport, HotspotSummary | mercury_ai.utils.performance_collector, tests.test_performance_collector |
| impulse_strength | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| incorrect | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| independent_confirmations | ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_explainability_engine |
| index | Swing | mercury_ai.analysis.data_quality_engine, mercury_ai.analysis.historical_replay_engine, mercury_ai.analysis.performance_analytics, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, mercury_ai.data.data_quality_engine, mercury_ai.data.indicator_engine, parity_check, scripts.run_replay_3500, test_replay_quick, tests.test_benchmark_integration, tests.test_institutional_backtest |
| indices | EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| influence | DecisionNode | mercury_ai.analysis.decision_trace_engine |
| input_object | TelemetryData | mercury_ai.core.analysis_pipeline |
| institutional_alignment | DecisionInput, DecisionResult, MarketThesis, ProfessionalThesis | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.market_thesis_builder, mercury_ai.core.analysis_pipeline |
| institutional_bias | InstitutionalContext, VWAPAnalysis | mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.tests.test_vwap_engine, mercury_ai.analysis.vwap_engine |
| institutional_confidence | ProbabilityResult | mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_probability_engine |
| institutional_consensus_strength | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| institutional_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| institutional_participation | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| institutional_risk_score | RiskAssessment | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, tests.test_probability_engine |
| institutional_score | DecisionExplainability, InstitutionalScoreResult, SmartMoneyAnalysis | mercury_ai.analysis.institutional_score_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner |
| integrity_issues | QualityReport | mercury_ai.analysis.data_quality_engine, tests.test_data_quality_engine |
| internal_bos | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| internal_liquidity | LiquidityProfile, MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| invalidation_point | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| is_absorption | VolumeAnalysis | mercury_ai.analysis.volume_engine |
| is_accepted | VWAPAnalysis | mercury_ai.analysis.vwap_engine |
| is_accumulation | VolumeAnalysis | mercury_ai.analysis.volume_engine |
| is_bearish_fvg | FairValueGapAnalysis | mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.smart_money.smart_money_engine |
| is_bullish_fvg | FairValueGapAnalysis | mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_fvg_engine |
| is_climax | VolumeAnalysis | mercury_ai.analysis.volume_engine |
| is_continuation | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_deterministic | StressTestResult | mercury_ai.utils.stress_tester |
| is_discount | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine |
| is_distribution | VolumeAnalysis | mercury_ai.analysis.volume_engine |
| is_divergence | MomentumAnalysis | mercury_ai.analysis.momentum_engine |
| is_engulfing | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_price_action_engine |
| is_exhaustion | MomentumAnalysis, PriceActionAnalysis | mercury_ai.analysis.momentum_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_false_breakout | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_filled | FairValueGapAnalysis | mercury_ai.analysis.fair_value_gap_engine |
| is_high | ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, tests.test_confidence_calibration |
| is_inside_bar | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_mean_reversion | VWAPAnalysis | mercury_ai.analysis.vwap_engine |
| is_open | FairValueGapAnalysis | mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.tests.test_fvg_engine |
| is_outside_bar | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_pin_bar | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_premium | LiquidityAnalysis | mercury_ai.analysis.smart_money.liquidity_engine |
| is_pullback | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_regression | RegressionResult | mercury_ai.utils.regression_detector |
| is_rejected | VWAPAnalysis | mercury_ai.analysis.vwap_engine |
| is_rejection | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_significant_95 | StatisticalTestResult | mercury_ai.analysis.benchmark_framework |
| is_strong_candle | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| is_volume_spike | VolumeAnalysis | mercury_ai.analysis.tests.test_volume_engine, mercury_ai.analysis.volume_engine |
| is_weak_candle | PriceActionAnalysis | mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine |
| kelly_fraction | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline, tests.test_institutional_backtest |
| kelly_half | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| kelly_quarter | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| last_confirmed_high | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| last_confirmed_low | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| last_index | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| last_operated | Asset | mercury_ai.brain.scanner, mercury_ai.core.asset_registry |
| last_timestamp | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| late_entries | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| latency_ms | ProviderMetrics | app.dashboard.provider_health_panel |
| lh_count | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| liquidity | InstitutionalContext, Asset, MarketContext | app.dashboard.market_map_panel, mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.asset_registry, tests.test_scanner_priority |
| liquidity_alignment | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| liquidity_analysis | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| liquidity_cluster | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| liquidity_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| liquidity_density | LiquidityProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine |
| liquidity_score | SessionAnalysis | mercury_ai.analysis.market_state_engine, mercury_ai.analysis.session_engine |
| liquidity_sweep | LiquidityProfile, MarketStructureProfile | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| ll_count | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| local_bias | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| logical_sequence | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| lower_high | MarketStructure | mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine |
| lower_low | MarketStructure | mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.bos_engine, mercury_ai.analysis.smart_money.choch_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine |
| lower_wick | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine |
| macd | MarketData, MomentumAnalysis | mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| macd_signal | MarketData, MomentumAnalysis | mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| machine_readable | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| mae | ReplayMetrics, TradeMemory | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.historical_replay_engine, mercury_ai.database.replay_storage, tests.test_institutional_backtest, tests.test_performance_engine |
| market | UniverseAsset, Asset, AnalysisResult, MarketContext | app.dashboard.asset_registry_panel, app.dashboard.dashboard, app.dashboard.operation_center, app.terminal.pages.01_Scanner, mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.validation_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.config.assets, mercury_ai.config.universe, mercury_ai.core.analysis_pipeline, mercury_ai.core.asset_registry, mercury_ai.database.history_logger, tests.test_scanner_recovery, tests.test_validation_engine, tests.test_versioning |
| market_bias | DecisionInput, MarketThesis, ProfessionalThesis | mercury_ai.analysis.market_thesis_builder |
| market_condition | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| market_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.presentation.signal_formatter |
| market_factor | ConfidenceComponents | mercury_ai.analysis.confidence_engine |
| market_regime | AnalysisResult, DecisionResult, MarketContext | app.dashboard.dashboard, app.dashboard.operation_center, app.terminal.pages.01_Scanner, mercury_ai.analysis.adaptive_weight_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_scanner_recovery, tests.test_versioning |
| market_score | ConfidenceResult | mercury_ai.analysis.confidence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| market_shift | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| market_state | InstitutionalContext, AnalysisResult, DecisionInput, MarketCondition, MarketContext, MarketThesis | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_thesis_builder, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_versioning |
| max_drawdown | PerformanceMetrics, AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, run_institutional_replay, scripts.run_replay_3500 |
| max_drawdown_pct | BuyAndHoldBaseline | mercury_ai.analysis.benchmark_framework |
| max_exposure | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.core.analysis_pipeline |
| maximum_price | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| maximum_strength | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| mean_return | StatisticalTestResult | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| memory_delta | StageMetric, StageProfile, RegressionResult | mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector, mercury_ai.utils.regression_detector |
| memory_peak | StageProfile | mercury_ai.core.pipeline_profiler |
| memory_usage | TelemetryData, BenchmarkRunResult | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework, mercury_ai.core.analysis_pipeline |
| message | Notification, RegressionResult | mercury_ai.ai.llm, mercury_ai.analysis.notification_center, mercury_ai.utils.regression_detector, teste_llm, teste_openrouter, tools.mercury_integrity_auditor.auditors.contract_certification_auditor |
| metadata | Evidence, FairValueGapAnalysis, LiquidityAnalysis, LiquidityResult, MomentumAnalysis, PriceActionAnalysis, ProbabilityResult, TrendAnalysis, VolumeAnalysis, VWAPAnalysis | mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.utils.report_generator, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine, tools.mercury_integrity_auditor.auditors.dependency_auditor |
| metrics | BatchReplayResult, ProviderRegistry | app.dashboard.provider_health_panel, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.core.observability_center |
| mfe | ReplayMetrics, TradeMemory | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.historical_replay_engine, mercury_ai.database.replay_storage, tests.test_institutional_backtest, tests.test_performance_engine |
| minimum_price | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| minimum_strength | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| missed_trades | PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.post_decision_evaluation_engine |
| missing_candles | QualityReport | mercury_ai.analysis.data_quality_engine, tests.test_data_quality_engine |
| missing_confirmations | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.presentation.signal_formatter |
| missing_inputs | DataQualityResult | mercury_ai.core.data_quality_gate |
| modifier | TelemetryData | mercury_ai.core.analysis_pipeline |
| momentum_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| momentum_state | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| mss | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| mtf_consensus | DecisionResult, MarketContext | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_confidence_calibration |
| mtf_evidences | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| name | ProviderRegistry, StageMetric, StageProfile | app.terminal.pages.05_Replay, mercury_ai.analysis.integrity_checker, mercury_ai.analysis.provider_priority_engine, mercury_ai.core._stage_builder, mercury_ai.core.pipeline_profiler, mercury_ai.data.mercury_data_provider, mercury_ai.providers.data_adapters, mercury_ai.providers.market_provider, mercury_ai.utils.performance_collector, tests.test_data_provider_manager, tests.test_performance_collector, tests.test_provider_priority_engine, tools.mercury_integrity_auditor.auditors.contract_auditor, tools.mercury_integrity_auditor.auditors.contract_certification_auditor, tools.mercury_integrity_auditor.auditors.coverage_auditor, tools.mercury_integrity_auditor.auditors.dependency_auditor, tools.mercury_integrity_auditor.auditors.flow_auditor, tools.mercury_integrity_auditor.auditors.integrity_auditor, tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.report, tools.mercury_integrity_auditor.auditors.static_auditor, tools.mercury_integrity_auditor.main, tools.project_mapper.ast_parser, tools.project_mapper.python_indexer, tools.project_mapper.scanner, tools.project_mapper.snapshot_builder, tools.scanner |
| nearest_resistance | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| nearest_support | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| nested_metrics | StageMetric | mercury_ai.utils.performance_collector, tests.test_performance_collector |
| nested_stages | StageProfile | mercury_ai.core.pipeline_profiler |
| neutral_factors | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| neutral_probability | ProbabilityResult | mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_probability_engine |
| neutral_score | ConfluenceResult, EvidenceRankingResult | mercury_ai.analysis.confluence_engine, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| neutral_weight | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| nodes | DecisionTrace | mercury_ai.analysis.decision_trace_engine |
| notes | UniverseAsset | mercury_ai.config.universe |
| opportunity_grade | DecisionExplainability, DecisionInput, MarketThesis, ProbabilityResult, ProfessionalThesis | mercury_ai.analysis.market_thesis_builder, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_probability_engine |
| ote | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| output_object | TelemetryData | mercury_ai.core.analysis_pipeline |
| overlap | SessionAnalysis | mercury_ai.analysis.market_state_engine, mercury_ai.analysis.session_engine |
| p_value | StatisticalTestResult | mercury_ai.analysis.benchmark_framework |
| parallel_workers | EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| participation_quality | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| pattern | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.tests.test_candlestick_engine |
| peak_memory | BenchmarkMetrics, StressTestResult | mercury_ai.utils.regression_detector, mercury_ai.utils.stress_tester |
| peak_memory_diff | MemoryAuditResult | mercury_ai.utils.memory_auditor |
| percentage_total | StageMetric, StageProfile | mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector, tests.test_performance_collector |
| performance_delta | RegressionResult | mercury_ai.utils.regression_detector |
| performance_metrics | EnhancedBenchmarkReport, BenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| persister | TelemetryData | mercury_ai.core.analysis_pipeline |
| pip_size | Asset | mercury_ai.core.asset_registry |
| pipeline_name | PipelineMetric, HotspotReport, PipelineProfile, HotspotSummary, StressTestResult | mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector, mercury_ai.utils.report_generator, mercury_ai.utils.stress_tester, tests.test_performance_collector |
| pipeline_version | VersionMetadata | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| pl | ReplayMetrics | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.historical_replay_engine, mercury_ai.analysis.performance_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.database.replay_storage, run_institutional_replay, scripts.run_replay_3500, test_replay_quick, tests.test_institutional_backtest, tests.test_performance_engine |
| pnl_accumulated | AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, run_institutional_replay, scripts.run_replay_3500, tests.test_institutional_backtest, tests.test_performance_engine |
| precision | UniverseAsset | mercury_ai.config.assets, mercury_ai.config.universe |
| premium_zone | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| previous_score | Asset | app.dashboard.market_map_panel, mercury_ai.brain.scanner, mercury_ai.core.asset_registry |
| previous_swing | MarketStructureProfile, SwingSequenceResult | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| price | LiquidityEvent, Swing | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration |
| price_action | MarketContext | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| price_deviation | EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| price_gaps | QualityReport | mercury_ai.analysis.data_quality_engine |
| price_location | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| prices | EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| priority | UniverseAsset, Asset, ProviderRegistry | app.dashboard.asset_registry_panel, mercury_ai.analysis.provider_priority_engine, mercury_ai.brain.scanner, mercury_ai.config.assets, mercury_ai.config.universe, mercury_ai.core.asset_registry, mercury_ai.data.mercury_data_provider, mercury_ai.providers.data_adapters, mercury_ai.providers.market_provider, tests.test_asset_registry, tests.test_data_provider_manager, tests.test_scanner_priority |
| probability_score | InstitutionalScoreResult | mercury_ai.analysis.institutional_score_engine, mercury_ai.brain.mercury_decision_engine |
| profile | Asset | app.dashboard.asset_registry_panel, mercury_ai.brain.scanner, mercury_ai.core.asset_registry, tests.test_broker_filtering |
| profit_factor | PerformanceMetrics, AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, tests.test_performance_engine |
| provider | Asset | app.dashboard.asset_registry_panel, mercury_ai.brain.scanner, mercury_ai.core.asset_registry, mercury_ai.market.market_engine |
| provider_symbol | UniverseAsset | mercury_ai.config.universe |
| pullback | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| quality | DecisionResult, FairValueGapAnalysis, LiquidityAnalysis, MomentumAnalysis, PriceActionAnalysis, SessionAnalysis, VolumeAnalysis, VWAPAnalysis | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.price_action_analyzer, mercury_ai.analysis.price_action_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.session_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| quality_factor | ConfidenceComponents | mercury_ai.analysis.confidence_engine |
| quality_level | DataQualityResult, TradeFilterResult | mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.data_quality_gate |
| quality_score | QualityReport, ProviderMetrics, Evidence, TradeFilterResult | app.dashboard.provider_health_panel, mercury_ai.analysis.confidence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.data_quality_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_quality_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_data_quality_engine, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| ranked_evidences | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| raw_score | InstitutionalContribution | mercury_ai.analysis.confluence_engine, mercury_ai.brain.scanner |
| reason | DecisionExplainability | mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner |
| reasons | TradeFilterResult, TradePermission | mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| reclaim | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| recovery_time_candles | AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor |
| regime | MarketRegime, TradeMemory | app.dashboard.dashboard, app.dashboard.operation_center, app.terminal.pages.01_Scanner, mercury_ai.analysis.adaptive_weight_engine, mercury_ai.analysis.institutional_trade_filter_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_benchmark, tests.test_adaptive_weighting, tests.test_scanner_recovery |
| rejection | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine |
| relative_volume | VolumeAnalysis, VolumeProfile | mercury_ai.analysis.tests.test_volume_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine |
| repetitions | StressTestResult | mercury_ai.utils.stress_tester |
| resistance | SupportResistanceAnalysis, SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| resistance_strength | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| resolved_quality_score | InstitutionalScoreResult | mercury_ai.analysis.institutional_score_engine, mercury_ai.brain.mercury_decision_engine |
| result | DecisionNode, TradeMemory | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.decision_trace_engine, mercury_ai.analysis.replay_batch_processor, mercury_ai.utils.memory_auditor |
| results | EnhancedBenchmarkReport, BatchReplayReport, BenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_benchmark_framework, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| retracement_quality | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| risk | MarketThesis | mercury_ai.analysis.market_thesis_builder |
| risk_analysis | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| risk_assessment | AnalysisResult, MarketContext, TradingExplanation | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, tests.test_confidence_calibration, tests.test_probability_engine, tests.test_versioning |
| risk_reward_ratio | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| risk_score | InstitutionalScoreResult, DecisionInput, DecisionResult | app.dashboard.dashboard, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.institutional_score_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.core.analysis_pipeline, mercury_ai.operations.demo_manager |
| roc | MomentumAnalysis | mercury_ai.analysis.momentum_engine |
| rsi | MarketData, MomentumAnalysis | mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_momentum_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| runtimes | StressTestResult | mercury_ai.utils.stress_tester |
| scenario | StressTestResult | mercury_ai.utils.stress_tester |
| score | EngineResult, DataQualityResult, DataQualityResult, DecisionNode, DecisionResult, LiquidityResult, Signal, SmartMoneyAnalysis, VolatilityAnalysis | app.dashboard.dashboard, app.terminal.pages.01_Scanner, mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.decision_trace_engine, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.ranking_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.volatility_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.scanner, mercury_ai.core.analysis_pipeline, mercury_ai.core.data_quality_gate, mercury_ai.database.history_logger, tests.test_scanner_recovery |
| sell_probability | DecisionResult, ProbabilityResult | app.dashboard.dashboard, app.terminal.pages.01_Scanner, mercury_ai.analysis.decision_result_builder, mercury_ai.brain.explainability_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.probability_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, tests.test_probability_engine, tests.test_scanner_recovery |
| sell_score | ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| sell_side_liquidity | MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| selling_climax | VolumeProfile | mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.volume_intelligence_engine |
| sequence | SwingSequenceResult | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.swing_engine |
| sequence_confidence | SwingSequenceResult | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.swing_engine |
| sequence_length | SwingSequenceResult | mercury_ai.analysis.swing_engine |
| sequence_quality | SwingSequenceResult | mercury_ai.analysis.swing_engine |
| session | InstitutionalContext, SessionAnalysis, TradeMemory | mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.session_engine |
| session_analysis | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| session_id | DecisionSnapshot | mercury_ai.core.analysis_pipeline, mercury_ai.core.session_manager, tests.test_session_id, tests.test_versioning |
| severity | AuditEvent | mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.security_center, tools.mercury_integrity_auditor.auditors.contract_certification_auditor, tools.mercury_integrity_auditor.auditors.report, tools.mercury_integrity_auditor.main, tools.mercury_integrity_auditor.models |
| sharpe_ratio | BuyAndHoldBaseline, AssetPerformance | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, run_institutional_replay, scripts.run_replay_3500 |
| smart_money | AnalysisResult, MarketContext | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_versioning |
| smart_money_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| snapshot | MemorySnapshot | mercury_ai.utils.memory_auditor |
| sortino_ratio | AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, run_institutional_replay, scripts.run_replay_3500 |
| spread | Asset | app.dashboard.asset_registry_panel, app.dashboard.market_map_panel, mercury_ai.brain.scanner, mercury_ai.core.asset_registry, tests.test_scanner_priority |
| stage_metrics | PipelineMetric | mercury_ai.utils.performance_collector, tests.test_performance_collector |
| stage_profiles | PipelineProfile | mercury_ai.core.pipeline_profiler, tests.test_benchmark_integration |
| stages | RuntimeReport | mercury_ai.core.analysis_pipeline, mercury_ai.core.runtime_report |
| stale_data | DataQualityResult | mercury_ai.core.data_quality_gate |
| start_time | TelemetryData | mercury_ai.core._stage_builder, mercury_ai.core.analysis_pipeline, mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector |
| state | MarketState, VolatilityAnalysis | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.market_state_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.volatility_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, tests.test_confidence_calibration |
| statistical_tests | EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| status | ProviderHealth, TradePermission | app.dashboard.provider_health_panel, tools.mercury_integrity_auditor.auditors.backtest_auditor, tools.mercury_integrity_auditor.auditors.contract_auditor, tools.mercury_integrity_auditor.auditors.coverage_auditor, tools.mercury_integrity_auditor.auditors.data_auditor, tools.mercury_integrity_auditor.auditors.decision_auditor, tools.mercury_integrity_auditor.auditors.dependency_auditor, tools.mercury_integrity_auditor.auditors.determinism_auditor, tools.mercury_integrity_auditor.auditors.explainability_auditor, tools.mercury_integrity_auditor.auditors.flow_auditor, tools.mercury_integrity_auditor.auditors.global_state_auditor, tools.mercury_integrity_auditor.auditors.integrity_auditor, tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.performance_auditor, tools.mercury_integrity_auditor.auditors.report, tools.mercury_integrity_auditor.auditors.runtime_auditor, tools.mercury_integrity_auditor.auditors.static_auditor, tools.mercury_integrity_auditor.auditors.test_auditor, tools.mercury_integrity_auditor.auditors.universe_auditor, tools.mercury_integrity_auditor.main, tools.mercury_integrity_auditor.models |
| std_return | StatisticalTestResult | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| stop_hunt | MarketStructureProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| stop_hunt_probability | LiquidityProfile | mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine |
| strength | LiquidityEvent, Evidence, LiquidityResult, MomentumAnalysis, Swing | mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.evidence_query, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.validation_engine, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_benchmark_integration, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| strength_score | EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| strengths | EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| stress_test_loss | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| strong_evidences | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| strongest_evidence | EvidenceRankingResult | app.dashboard.dashboard, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| structure | SmartMoneyAnalysis | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark |
| structure_alignment | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| structure_analysis | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| structure_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.presentation.signal_formatter |
| successful | BatchReplayReport | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| suggested_entry | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| suggested_stop | RiskAssessment, TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| suggested_take_profit | RiskAssessment | mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| suggested_targets | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| summary | DecisionResult, MTFConsensus, ProfessionalThesis | app.dashboard.dashboard, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, mercury_ai.core.pipeline_profiler, tests.test_benchmark_integration, tests.test_confidence_calibration, tests.test_determinism, tests.test_market_resilience, verify_assets |
| support | SupportResistanceAnalysis, SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| support_resistance | AnalysisResult, MarketContext | mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.risk_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_versioning |
| support_strength | SupportResistanceAnalysis | mercury_ai.analysis.risk_engine, mercury_ai.analysis.support_resistance_analyzer |
| supporting_evidences | MarketRegime | mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.risk_engine, tests.test_adaptive_weighting |
| swing_highs | MarketStructure | mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine |
| swing_lows | MarketStructure | mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.tests.test_risk_engine |
| symbol | BuyAndHoldBaseline, BatchReplayResult, UniverseAsset, Asset, RuntimeReport, BenchmarkRunResult, MarketData | app.dashboard.asset_registry_panel, app.dashboard.dashboard, app.dashboard.market_map_panel, app.dashboard.operation_center, app.terminal.pages.01_Scanner, mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_benchmark_framework, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.config.assets, mercury_ai.config.universe, mercury_ai.core.analysis_pipeline, mercury_ai.core.asset_registry, mercury_ai.core.runtime_report, mercury_ai.database.history_logger, tests.test_broker_filtering, tests.test_institutional_backtest, tests.test_scanner_priority, tests.test_scanner_recovery |
| system_ready | HealthStatus | app.dashboard.dashboard, app.launcher, app.terminal.pages.07_Observabilidade, app.terminal.terminal, mercury_ai.analysis.health_checker, tests.test_health_checker |
| t_statistic | StatisticalTestResult | mercury_ai.analysis.benchmark_framework |
| target | AuditEvent | mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.security_center, tools.mercury_integrity_auditor.auditors.contract_auditor, tools.mercury_integrity_auditor.auditors.contract_certification_auditor |
| technical_reason | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.brain.institutional_brain, mercury_ai.core.analysis_pipeline, tests.test_determinism |
| tick_size | Asset | mercury_ai.core.asset_registry |
| timeframe | Asset, DecisionSnapshot, Evidence, MarketData, MarketEvidenceBundle, Signal | mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, mercury_ai.core.asset_registry, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine, tests.test_versioning |
| timestamp | HealthStatus, Notification, AuditEvent, AuditEvent, AnalysisResult, BenchmarkRunResult, DecisionOutcome, DecisionSnapshot, Evidence, MarketEvidenceBundle, MemorySnapshot, BenchmarkMetrics, Swing, TradeMemory | app.dashboard.dashboard, app.dashboard.operation_center, app.terminal.pages.01_Scanner, app.terminal.pages.06_Demo, mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.evidence_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.health_checker, mercury_ai.analysis.institutional_memory_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.notification_center, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, mercury_ai.core.analysis_pipeline, mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.security_center, mercury_ai.core.session_manager, mercury_ai.database.replay_storage, mercury_ai.database.snapshot_logger, mercury_ai.utils.memory_auditor, mercury_ai.utils.regression_detector, tests.test_adaptive_weighting, tests.test_benchmark_integration, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_scanner_recovery, tests.test_validation_engine, tests.test_versioning |
| timestamps | EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| top_bearish_evidence | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| top_bullish_evidence | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| top_neutral_evidence | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| top_stats | MemoryAuditResult | mercury_ai.utils.memory_auditor |
| total_assets | UniversePerformance | mercury_ai.analysis.performance_engine, run_institutional_replay, scripts.run_replay_3500, test_replay_quick, tests.test_institutional_backtest, tests.test_performance_engine |
| total_duration | PipelineMetric, HotspotReport, PipelineProfile | mercury_ai.core.pipeline_profiler, mercury_ai.utils.performance_collector, tests.test_benchmark_integration, tests.test_performance_collector |
| total_return_pct | BuyAndHoldBaseline | mercury_ai.analysis.benchmark_framework |
| total_symbols | BatchReplayReport | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| total_trades | AssetPerformance, PerformanceMetrics | mercury_ai.analysis.metric_calculator, mercury_ai.analysis.performance_engine, mercury_ai.analysis.post_decision_evaluation_engine, mercury_ai.analysis.replay_batch_processor, run_institutional_replay, scripts.run_replay_3500, tests.test_institutional_backtest, tests.test_performance_engine |
| total_wall_time | EnhancedBenchmarkReport, BatchReplayReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_benchmark_framework, mercury_ai.analysis.tests.test_replay_batch_processor |
| total_weight | EvidenceRankingResult | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| touch_count | EqualHighMetrics, EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| touch_score | EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| touches | EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine |
| trace | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.decision_trace_engine, mercury_ai.core.analysis_pipeline |
| trade_allowed | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| trade_block_reasons | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| trade_quality | RiskAssessment | mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| trade_quality_level | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| trade_quality_score | InstitutionalScoreResult, DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.institutional_score_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| trading_session | Asset | mercury_ai.core.asset_registry |
| trap_detected | MarketStructureProfile | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| trend | AnalysisResult, MarketCondition, MarketContext, MarketStructure, MarketStructureProfile | mercury_ai.analysis.confidence_engine, mercury_ai.analysis.confluence_score_engine, mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_context_builder, mercury_ai.analysis.market_regime_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.mtf_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.market_structure_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_market_regime_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_benchmark_integration, tests.test_confidence_calibration, tests.test_regression_sprint18, tests.test_versioning |
| trend_alignment | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| trend_confirmation | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| trend_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.presentation.signal_formatter |
| trend_direction | SwingSequenceResult | mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.swing_engine |
| trend_strength | MarketCondition, MarketStructureProfile, TrendAnalysis | mercury_ai.analysis.market_condition_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.tests.test_candlestick_engine, tests.test_benchmark_integration, tests.test_regression_sprint18 |
| trend_transition | SwingSequenceResult | mercury_ai.analysis.swing_engine |
| triggered_rule | DecisionExplainability, DecisionResolverResult | mercury_ai.analysis.decision_resolver_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, test_bloco7_scenarios |
| type | Notification, Swing | mercury_ai.analysis.notification_center, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, tests.test_benchmark_integration, tools.mercury_integrity_auditor.auditors.contract_certification_auditor, tools.mercury_integrity_auditor.auditors.masking_auditor, tools.mercury_integrity_auditor.auditors.static_auditor |
| universe_performance | EnhancedBenchmarkReport, BatchReplayReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_benchmark_framework, mercury_ai.analysis.tests.test_replay_batch_processor, tests.test_institutional_backtest |
| upper_wick | CandlestickAnalysis | mercury_ai.analysis.candlestick_engine |
| uptime_percentage | ProviderMetrics | app.dashboard.provider_health_panel |
| user | AuditEvent | mercury_ai.core.pipeline_audit_middleware, mercury_ai.core.security_center |
| var_95 | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline, tests.test_institutional_backtest |
| var_99 | RiskAssessment | mercury_ai.analysis.risk_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.core.analysis_pipeline |
| version | EnhancedBenchmarkReport, BatchReplayReport, AnalysisResult, BenchmarkReport, DecisionSnapshot | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_benchmark_framework, mercury_ai.analysis.tests.test_replay_batch_processor, mercury_ai.core.analysis_pipeline, mercury_ai.core.session_manager, mercury_ai.utils.report_generator, tests.test_versioning, tools.mercury_integrity_auditor.auditors.dependency_auditor |
| version_metadata | DecisionResult, DecisionSnapshot | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline, tests.test_versioning |
| volatility | InstitutionalContext, UniverseAsset | mercury_ai.analysis.institutional_context_builder, mercury_ai.analysis.mtf_engine, mercury_ai.config.assets, mercury_ai.config.universe |
| volatility_alignment | MTFConsensus | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, tests.test_confidence_calibration |
| volatility_analysis | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| volume | MarketData, Swing | mercury_ai.analysis.mtf_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_stress, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.tests.test_trend_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, tests.test_benchmark_integration |
| volume_analysis | AnalysisResult | mercury_ai.core.analysis_pipeline, tests.test_versioning |
| volume_consistency | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| volume_context | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| volume_divergence | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| volume_issues | QualityReport | mercury_ai.analysis.data_quality_engine, tests.test_data_quality_engine |
| volume_spike | VolumeProfile | mercury_ai.analysis.volume_intelligence_engine |
| volume_trend | VolumeAnalysis | mercury_ai.analysis.volume_engine |
| vwap | VWAPAnalysis | mercury_ai.analysis.tests.test_vwap_engine, mercury_ai.analysis.vwap_engine |
| wait_probability | DecisionResult | app.dashboard.dashboard, app.terminal.pages.01_Scanner, mercury_ai.analysis.decision_result_builder, mercury_ai.brain.institutional_brain, mercury_ai.brain.scanner, mercury_ai.core.analysis_pipeline, tests.test_scanner_recovery |
| wall_time | BatchReplayResult | mercury_ai.analysis.replay_batch_processor, mercury_ai.analysis.tests.test_replay_batch_processor |
| warm_up_trades_excluded | EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework, mercury_ai.analysis.tests.test_benchmark_framework |
| warnings | EngineResult, DataQualityResult, TelemetryData, ConfluenceResult, DataQualityResult, DecisionInput, DecisionResult, TradingExplanation, TrendAnalysis | mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.decision_result_builder, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.tests.test_candlestick_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.institutional_brain, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline, mercury_ai.core.data_quality_gate |
| weak_evidences | TradingExplanation | mercury_ai.analysis.narrative_engine, mercury_ai.brain.explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| weakest_evidence | EvidenceRankingResult | mercury_ai.analysis.evidence_ranking_engine, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine |
| weaknesses | DecisionResult | mercury_ai.analysis.decision_result_builder, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.core.analysis_pipeline |
| weight | InstitutionalContribution, DecisionNode, Evidence | mercury_ai.analysis.conflict_resolution_engine, mercury_ai.analysis.confluence_engine, mercury_ai.analysis.context_engine, mercury_ai.analysis.context_intelligence_engine, mercury_ai.analysis.decision_trace_engine, mercury_ai.analysis.evidence_ranking_engine, mercury_ai.analysis.fair_value_gap_engine, mercury_ai.analysis.market_structure_intelligence_engine, mercury_ai.analysis.momentum_engine, mercury_ai.analysis.narrative_engine, mercury_ai.analysis.risk_engine, mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.smart_money_engine, mercury_ai.analysis.swing_engine, mercury_ai.analysis.tests.test_risk_engine, mercury_ai.analysis.trend_analyzer, mercury_ai.analysis.volatility_engine, mercury_ai.analysis.volume_engine, mercury_ai.analysis.volume_intelligence_engine, mercury_ai.analysis.vwap_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_mercury_decision_benchmark, mercury_ai.brain.tests.test_mercury_decision_engine, mercury_ai.brain.tests.test_probability_engine, tests.test_adaptive_weighting, tests.test_confidence_calibration, tests.test_conflict_resolution, tests.test_evidence_engine, tests.test_evidence_quality_engine, tests.test_probability_engine, tests.test_validation_engine |
| weighted_score | InstitutionalContribution, ConfluenceResult | mercury_ai.analysis.confluence_engine, mercury_ai.brain.mercury_decision_engine, mercury_ai.brain.scanner, mercury_ai.brain.tests.test_explainability_engine, mercury_ai.brain.tests.test_mercury_decision_engine |
| weights_version | VersionMetadata | mercury_ai.analysis.decision_result_builder, mercury_ai.core.analysis_pipeline |
| win_rate | PerformanceMetrics, AssetPerformance | mercury_ai.analysis.performance_engine, mercury_ai.analysis.replay_batch_processor, run_institutional_replay, scripts.run_replay_3500, tests.test_institutional_backtest, tests.test_performance_engine |
