# CONTRACT CERTIFICATION REPORT

**Project:** Mercury AI V1
**Audit:** SPRINT 1.9 BLOCO 2/10 - Contract Certification
**Verdict:** FAIL
**Total Findings:** 908
**FAIL:** 5
**WARNING:** 661
**INFO:** 242
**Dataclasses Analyzed:** 101

## Summary by Category

| Category | Count | Severity |
|----------|-------|----------|
| ASYMMETRIC_SERIALIZATION | 1 | WARNING |
| DATACLASS_FIELD_DIVERGENCE | 5 | FAIL |
| ENGINE_NOT_CONSUMED_BY_MODEL | 11 | WARNING |
| FIELD_NAMING_CONVENTION | 1 | INFO |
| FROZEN_WITH_MUTABLE_FIELD | 60 | WARNING |
| MODEL_NOT_CONSUMED | 8 | WARNING |
| NO_SERIALIZATION | 99 | WARNING |
| OPTIONAL_NO_DEFAULT | 2 | INFO |
| REQUIRED_FIELDS_NEED_VERIFICATION | 239 | INFO |
| REQUIRED_FIELD_NO_DEFAULT | 482 | WARNING |

## Dataclass Inventory

| Dataclass | Module | Fields | Frozen | Serialization |
|-----------|--------|--------|--------|---------------|
| BuyAndHoldBaseline | mercury_ai.analysis.benchmark_framework | 5 | True | None |
| EnhancedBenchmarkReport | mercury_ai.analysis.benchmark_framework | 12 | True | None |
| StatisticalTestResult | mercury_ai.analysis.benchmark_framework | 8 | True | None |
| ConfidenceComponents | mercury_ai.analysis.confidence_engine | 5 | True | None |
| QualityReport | mercury_ai.analysis.data_quality_engine | 8 | False | None |
| DecisionExplainability | mercury_ai.analysis.decision_explainability | 10 | True | None |
| DecisionResolverResult | mercury_ai.analysis.decision_resolver_engine | 3 | True | None |
| HealthStatus | mercury_ai.analysis.health_checker | 3 | False | None |
| InstitutionalContext | mercury_ai.analysis.institutional_context_builder | 7 | False | None |
| InstitutionalContribution | mercury_ai.analysis.institutional_contribution | 7 | True | None |
| InstitutionalScoreResult | mercury_ai.analysis.institutional_score_engine | 8 | True | None |
| PerformanceMetrics | mercury_ai.analysis.metric_calculator | 15 | True | None |
| Notification | mercury_ai.analysis.notification_center | 3 | False | None |
| BatchReplayReport | mercury_ai.analysis.replay_batch_processor | 9 | True | None |
| BatchReplayResult | mercury_ai.analysis.replay_batch_processor | 6 | True | None |
| BOSResult | mercury_ai.analysis.smart_money.bos_engine | 4 | True | None |
| CHOCHResult | mercury_ai.analysis.smart_money.choch_engine | 4 | True | None |
| EqualHighGroup | mercury_ai.analysis.smart_money.liquidity_engine | 6 | True | None |
| EqualHighMetrics | mercury_ai.analysis.smart_money.liquidity_engine | 16 | True | None |
| EqualHighScore | mercury_ai.analysis.smart_money.liquidity_engine | 12 | True | None |
| LiquidityEvent | mercury_ai.analysis.smart_money.liquidity_event_engine | 5 | True | None |
| UniverseAsset | mercury_ai.config.universe | 9 | True | None |
| Asset | mercury_ai.core.asset_registry | 17 | False | None |
| AuditEvent | mercury_ai.core.audit_sink | 2 | True | None |
| EngineResult | mercury_ai.core.base_engine | 5 | True | None |
| DataQualityResult | mercury_ai.core.data_quality_gate | 3 | False | None |
| RuntimeReport | mercury_ai.core.runtime_report | 2 | False | to_dict |
| TelemetryData | mercury_ai.core.runtime_report | 16 | False | None |
| AuditEvent | mercury_ai.core.security_center | 5 | False | None |
| ProviderHealth | mercury_ai.data.mercury_data_provider | 3 | False | None |
| ProviderMetrics | mercury_ai.data.mercury_data_provider | 3 | False | None |
| ProviderPriority | mercury_ai.data.mercury_data_provider | 0 | False | None |
| ProviderRegistry | mercury_ai.data.mercury_data_provider | 5 | False | None |
| ReplayMetrics | mercury_ai.database.replay_storage | 4 | True | None |
| AnalysisResult | mercury_ai.models.analysis_result | 21 | True | None |
| BenchmarkReport | mercury_ai.models.benchmark_report | 4 | True | None |
| BenchmarkRunResult | mercury_ai.models.benchmark_report | 5 | True | None |
| CandlestickAnalysis | mercury_ai.models.candlestick_analysis | 11 | True | None |
| ConfidenceResult | mercury_ai.models.confidence_result | 8 | True | None |
| ConfluenceResult | mercury_ai.models.confluence_result | 11 | True | None |
| ConfluenceScore | mercury_ai.models.confluence_score | 5 | True | None |
| DataQualityResult | mercury_ai.models.data_quality_result | 5 | True | None |
| DecisionInput | mercury_ai.models.decision_input | 9 | True | None |
| DecisionNode | mercury_ai.models.decision_node | 6 | True | None |
| DecisionOutcome | mercury_ai.models.decision_outcome | 4 | True | None |
| DecisionResult | mercury_ai.models.decision_result | 32 | True | None |
| DecisionSnapshot | mercury_ai.models.decision_snapshot | 11 | True | None |
| DecisionTrace | mercury_ai.models.decision_trace | 3 | True | None |
| AssetPerformance | mercury_ai.models.equity_metrics | 13 | True | None |
| UniversePerformance | mercury_ai.models.equity_metrics | 9 | True | None |
| Evidence | mercury_ai.models.evidence | 13 | True | None |
| EvidenceRankingResult | mercury_ai.models.evidence_ranking | 14 | True | None |
| FairValueGapAnalysis | mercury_ai.models.fair_value_gap_analysis | 10 | True | None |
| LiquidityAnalysis | mercury_ai.models.liquidity_analysis | 12 | True | None |
| LiquidityProfile | mercury_ai.models.liquidity_profile | 7 | True | None |
| LiquidityResult | mercury_ai.models.liquidity_result | 5 | True | None |
| MarketCondition | mercury_ai.models.market_condition | 4 | True | None |
| MarketContext | mercury_ai.models.market_context | 10 | True | None |
| MarketData | mercury_ai.models.market_data | 14 | True | None |
| MarketEvidenceBundle | mercury_ai.models.market_evidence_bundle | 4 | True | None |
| MarketRegime | mercury_ai.models.market_regime | 3 | True | None |
| MarketState | mercury_ai.models.market_state | 2 | True | None |
| MarketStructure | mercury_ai.models.market_structure | 9 | True | None |
| MarketStructureProfile | mercury_ai.models.market_structure_profile | 54 | True | None |
| MarketThesis | mercury_ai.models.market_thesis | 9 | True | None |
| MemoryAuditResult | mercury_ai.models.memory_audit | 5 | True | None |
| MemorySnapshot | mercury_ai.models.memory_audit | 3 | True | None |
| MomentumAnalysis | mercury_ai.models.momentum_analysis | 12 | True | None |
| MTFConsensus | mercury_ai.models.mtf_consensus | 12 | True | None |
| HotspotReport | mercury_ai.models.performance | 3 | True | None |
| PipelineMetric | mercury_ai.models.performance | 3 | True | None |
| StageMetric | mercury_ai.models.performance | 5 | True | None |
| PerformanceMetrics | mercury_ai.models.performance_metrics | 10 | True | None |
| PriceActionAnalysis | mercury_ai.models.price_action | 4 | True | None |
| PriceActionAnalysis | mercury_ai.models.price_action_analysis | 16 | True | None |
| ProbabilityResult | mercury_ai.models.probability_result | 7 | True | None |
| ProfessionalThesis | mercury_ai.models.professional_thesis | 10 | True | None |
| HotspotSummary | mercury_ai.models.profiler_models | 2 | True | None |
| PipelineProfile | mercury_ai.models.profiler_models | 3 | True | None |
| StageProfile | mercury_ai.models.profiler_models | 6 | True | None |
| BenchmarkMetrics | mercury_ai.models.regression | 5 | True | None |
| RegressionResult | mercury_ai.models.regression | 6 | True | None |
| RiskAssessment | mercury_ai.models.risk_assessment | 17 | True | None |
| SessionAnalysis | mercury_ai.models.session_analysis | 5 | True | None |
| Signal | mercury_ai.models.signal | 11 | True | None |
| SmartMoneyAnalysis | mercury_ai.models.smart_money | 5 | True | None |
| StressTestResult | mercury_ai.models.stress_test | 9 | True | None |
| SupportResistanceAnalysis | mercury_ai.models.support_resistance | 5 | True | None |
| SupportResistanceAnalysis | mercury_ai.models.support_resistance_analysis | 10 | True | None |
| Swing | mercury_ai.models.swing_analysis | 10 | True | None |
| SwingSequenceResult | mercury_ai.models.swing_analysis | 8 | True | None |
| TradeFilterResult | mercury_ai.models.trade_filter_result | 4 | True | None |
| TradeMemory | mercury_ai.models.trade_memory | 12 | True | None |
| TradePermission | mercury_ai.models.trade_permission | 3 | True | None |
| TradingExplanation | mercury_ai.models.trading_explanation | 30 | True | None |
| TrendAnalysis | mercury_ai.models.trend_analysis | 15 | True | None |
| VersionMetadata | mercury_ai.models.version_metadata | 4 | True | None |
| VolatilityAnalysis | mercury_ai.models.volatility_analysis | 5 | True | None |
| VolumeAnalysis | mercury_ai.models.volume_analysis | 12 | True | None |
| VolumeProfile | mercury_ai.models.volume_profile | 14 | True | None |
| VWAPAnalysis | mercury_ai.models.vwap_analysis | 11 | True | None |

## Detailed Findings

### ASYMMETRIC_SERIALIZATION (1 findings)

#### WARNING: RuntimeReport (mercury_ai.core.runtime_report)

**Message:** Dataclass has to_dict but no from_dict/from_json

**Evidence:** Dataclass 'RuntimeReport' in mercury_ai\core\runtime_report.py:24 can serialize but not deserialize

**Location:** mercury_ai\core\runtime_report.py:24

### DATACLASS_FIELD_DIVERGENCE (5 findings)

#### FAIL: PerformanceMetrics (mercury_ai.analysis.metric_calculator, mercury_ai.models.performance_metrics)

**Message:** Dataclass 'PerformanceMetrics' defined in multiple modules with different fields

**Evidence:** Dataclass 'PerformanceMetrics' exists in 2 modules (mercury_ai.analysis.metric_calculator, mercury_ai.models.performance_metrics) with different field sets

**Location:** mercury_ai\analysis\metric_calculator.py:6

#### FAIL: AuditEvent (mercury_ai.core.audit_sink, mercury_ai.core.security_center)

**Message:** Dataclass 'AuditEvent' defined in multiple modules with different fields

**Evidence:** Dataclass 'AuditEvent' exists in 2 modules (mercury_ai.core.audit_sink, mercury_ai.core.security_center) with different field sets

**Location:** mercury_ai\core\audit_sink.py:6

#### FAIL: DataQualityResult (mercury_ai.core.data_quality_gate, mercury_ai.models.data_quality_result)

**Message:** Dataclass 'DataQualityResult' defined in multiple modules with different fields

**Evidence:** Dataclass 'DataQualityResult' exists in 2 modules (mercury_ai.core.data_quality_gate, mercury_ai.models.data_quality_result) with different field sets

**Location:** mercury_ai\core\data_quality_gate.py:5

#### FAIL: PriceActionAnalysis (mercury_ai.models.price_action, mercury_ai.models.price_action_analysis)

**Message:** Dataclass 'PriceActionAnalysis' defined in multiple modules with different fields

**Evidence:** Dataclass 'PriceActionAnalysis' exists in 2 modules (mercury_ai.models.price_action, mercury_ai.models.price_action_analysis) with different field sets

**Location:** mercury_ai\models\price_action.py:5

#### FAIL: SupportResistanceAnalysis (mercury_ai.models.support_resistance, mercury_ai.models.support_resistance_analysis)

**Message:** Dataclass 'SupportResistanceAnalysis' defined in multiple modules with different fields

**Evidence:** Dataclass 'SupportResistanceAnalysis' exists in 2 modules (mercury_ai.models.support_resistance, mercury_ai.models.support_resistance_analysis) with different field sets

**Location:** mercury_ai\models\support_resistance.py:5

### ENGINE_NOT_CONSUMED_BY_MODEL (11 findings)

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Message:** Engine dataclass 'ConfidenceComponents' not consumed by any model module

**Evidence:** Engine dataclass 'ConfidenceComponents' in mercury_ai.analysis.confidence_engine is used by: mercury_ai.analysis.confidence_engine

**Location:** mercury_ai\analysis\confidence_engine.py:10

#### WARNING: QualityReport (mercury_ai.analysis.data_quality_engine)

**Message:** Engine dataclass 'QualityReport' not consumed by any model module

**Evidence:** Engine dataclass 'QualityReport' in mercury_ai.analysis.data_quality_engine is used by: mercury_ai.analysis.data_quality_engine, mercury_ai.analysis.data_quality_engine

**Location:** mercury_ai\analysis\data_quality_engine.py:8

#### WARNING: DecisionResolverResult (mercury_ai.analysis.decision_resolver_engine)

**Message:** Engine dataclass 'DecisionResolverResult' not consumed by any model module

**Evidence:** Engine dataclass 'DecisionResolverResult' in mercury_ai.analysis.decision_resolver_engine is used by: mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_resolver_engine, mercury_ai.analysis.decision_resolver_engine

**Location:** mercury_ai\analysis\decision_resolver_engine.py:6

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Message:** Engine dataclass 'InstitutionalScoreResult' not consumed by any model module

**Evidence:** Engine dataclass 'InstitutionalScoreResult' in mercury_ai.analysis.institutional_score_engine is used by: mercury_ai.analysis.institutional_score_engine

**Location:** mercury_ai\analysis\institutional_score_engine.py:5

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Message:** Engine dataclass 'BOSResult' not consumed by any model module

**Evidence:** Engine dataclass 'BOSResult' in mercury_ai.analysis.smart_money.bos_engine is used by: mercury_ai.analysis.smart_money.bos_engine

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:7

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Message:** Engine dataclass 'CHOCHResult' not consumed by any model module

**Evidence:** Engine dataclass 'CHOCHResult' in mercury_ai.analysis.smart_money.choch_engine is used by: mercury_ai.analysis.smart_money.choch_engine

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:7

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Engine dataclass 'EqualHighGroup' not consumed by any model module

**Evidence:** Engine dataclass 'EqualHighGroup' in mercury_ai.analysis.smart_money.liquidity_engine is used by: mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Engine dataclass 'EqualHighMetrics' not consumed by any model module

**Evidence:** Engine dataclass 'EqualHighMetrics' in mercury_ai.analysis.smart_money.liquidity_engine is used by: mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:24

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Engine dataclass 'EqualHighScore' not consumed by any model module

**Evidence:** Engine dataclass 'EqualHighScore' in mercury_ai.analysis.smart_money.liquidity_engine is used by: mercury_ai.analysis.smart_money.liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine, mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Message:** Engine dataclass 'LiquidityEvent' not consumed by any model module

**Evidence:** Engine dataclass 'LiquidityEvent' in mercury_ai.analysis.smart_money.liquidity_event_engine is used by: mercury_ai.analysis.smart_money.liquidity_event_engine, mercury_ai.analysis.smart_money.liquidity_event_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:8

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Message:** Engine dataclass 'EngineResult' not consumed by any model module

**Evidence:** Engine dataclass 'EngineResult' in mercury_ai.core.base_engine is used by: mercury_ai.analysis.candlestick_engine, mercury_ai.analysis.candlestick_engine

**Location:** mercury_ai\core\base_engine.py:6

### FIELD_NAMING_CONVENTION (1 findings)

#### INFO: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** ATRs
**Message:** Field 'ATRs' may not follow snake_case convention

**Evidence:** Field 'ATRs' at line 21 in mercury_ai\analysis\smart_money\liquidity_engine.py appears to use camelCase or PascalCase

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:21

### FROZEN_WITH_MUTABLE_FIELD (60 findings)

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** asset_performances
**Message:** Frozen dataclass has mutable field 'asset_performances'

**Evidence:** Frozen dataclass 'EnhancedBenchmarkReport' at line 61 in mercury_ai\analysis\benchmark_framework.py contains mutable field 'asset_performances: Dict[str, AssetPerformance]'

**Location:** mercury_ai\analysis\benchmark_framework.py:61

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** buy_and_hold_baselines
**Message:** Frozen dataclass has mutable field 'buy_and_hold_baselines'

**Evidence:** Frozen dataclass 'EnhancedBenchmarkReport' at line 61 in mercury_ai\analysis\benchmark_framework.py contains mutable field 'buy_and_hold_baselines: Dict[str, BuyAndHoldBaseline]'

**Location:** mercury_ai\analysis\benchmark_framework.py:61

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** statistical_tests
**Message:** Frozen dataclass has mutable field 'statistical_tests'

**Evidence:** Frozen dataclass 'EnhancedBenchmarkReport' at line 61 in mercury_ai\analysis\benchmark_framework.py contains mutable field 'statistical_tests: Dict[str, StatisticalTestResult]'

**Location:** mercury_ai\analysis\benchmark_framework.py:61

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** score_distribution
**Message:** Frozen dataclass has mutable field 'score_distribution'

**Evidence:** Frozen dataclass 'PerformanceMetrics' at line 6 in mercury_ai\analysis\metric_calculator.py contains mutable field 'score_distribution: Dict[str, float]'

**Location:** mercury_ai\analysis\metric_calculator.py:6

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** asset_performance
**Message:** Frozen dataclass has mutable field 'asset_performance'

**Evidence:** Frozen dataclass 'BatchReplayResult' at line 34 in mercury_ai\analysis\replay_batch_processor.py contains mutable field 'asset_performance: AssetPerformance'

**Location:** mercury_ai\analysis\replay_batch_processor.py:34

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** cache_stats
**Message:** Frozen dataclass has mutable field 'cache_stats'

**Evidence:** Frozen dataclass 'BatchReplayResult' at line 34 in mercury_ai\analysis\replay_batch_processor.py contains mutable field 'cache_stats: dict'

**Location:** mercury_ai\analysis\replay_batch_processor.py:34

#### WARNING: BatchReplayReport (mercury_ai.analysis.replay_batch_processor)

**Field:** aggregate_cache_stats
**Message:** Frozen dataclass has mutable field 'aggregate_cache_stats'

**Evidence:** Frozen dataclass 'BatchReplayReport' at line 45 in mercury_ai\analysis\replay_batch_processor.py contains mutable field 'aggregate_cache_stats: Dict[str, float]'

**Location:** mercury_ai\analysis\replay_batch_processor.py:45

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Field:** explanation
**Message:** Frozen dataclass has mutable field 'explanation'

**Evidence:** Frozen dataclass 'BOSResult' at line 7 in mercury_ai\analysis\smart_money\bos_engine.py contains mutable field 'explanation: list[str]'

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:7

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Field:** explanation
**Message:** Frozen dataclass has mutable field 'explanation'

**Evidence:** Frozen dataclass 'CHOCHResult' at line 7 in mercury_ai\analysis\smart_money\choch_engine.py contains mutable field 'explanation: list[str]'

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:7

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** touches
**Message:** Frozen dataclass has mutable field 'touches'

**Evidence:** Frozen dataclass 'EqualHighGroup' at line 15 in mercury_ai\analysis\smart_money\liquidity_engine.py contains mutable field 'touches: List[Swing]'

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** prices
**Message:** Frozen dataclass has mutable field 'prices'

**Evidence:** Frozen dataclass 'EqualHighGroup' at line 15 in mercury_ai\analysis\smart_money\liquidity_engine.py contains mutable field 'prices: List[float]'

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** timestamps
**Message:** Frozen dataclass has mutable field 'timestamps'

**Evidence:** Frozen dataclass 'EqualHighGroup' at line 15 in mercury_ai\analysis\smart_money\liquidity_engine.py contains mutable field 'timestamps: List[str]'

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** indices
**Message:** Frozen dataclass has mutable field 'indices'

**Evidence:** Frozen dataclass 'EqualHighGroup' at line 15 in mercury_ai\analysis\smart_money\liquidity_engine.py contains mutable field 'indices: List[int]'

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** strengths
**Message:** Frozen dataclass has mutable field 'strengths'

**Evidence:** Frozen dataclass 'EqualHighGroup' at line 15 in mercury_ai\analysis\smart_money\liquidity_engine.py contains mutable field 'strengths: List[float]'

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** ATRs
**Message:** Frozen dataclass has mutable field 'ATRs'

**Evidence:** Frozen dataclass 'EqualHighGroup' at line 15 in mercury_ai\analysis\smart_money\liquidity_engine.py contains mutable field 'ATRs: List[float]'

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** trend
**Message:** Frozen dataclass has mutable field 'trend'

**Evidence:** Frozen dataclass 'AnalysisResult' at line 29 in mercury_ai\models\analysis_result.py contains mutable field 'trend: List[Evidence]'

**Location:** mercury_ai\models\analysis_result.py:29

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** mtf_evidences
**Message:** Frozen dataclass has mutable field 'mtf_evidences'

**Evidence:** Frozen dataclass 'AnalysisResult' at line 29 in mercury_ai\models\analysis_result.py contains mutable field 'mtf_evidences: List[Evidence]'

**Location:** mercury_ai\models\analysis_result.py:29

#### WARNING: CandlestickAnalysis (mercury_ai.models.candlestick_analysis)

**Field:** evidences
**Message:** Frozen dataclass has mutable field 'evidences'

**Evidence:** Frozen dataclass 'CandlestickAnalysis' at line 5 in mercury_ai\models\candlestick_analysis.py contains mutable field 'evidences: List[str]'

**Location:** mercury_ai\models\candlestick_analysis.py:5

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** warnings
**Message:** Frozen dataclass has mutable field 'warnings'

**Evidence:** Frozen dataclass 'DecisionInput' at line 5 in mercury_ai\models\decision_input.py contains mutable field 'warnings: List[str]'

**Location:** mercury_ai\models\decision_input.py:5

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** blockers
**Message:** Frozen dataclass has mutable field 'blockers'

**Evidence:** Frozen dataclass 'DecisionInput' at line 5 in mercury_ai\models\decision_input.py contains mutable field 'blockers: List[str]'

**Location:** mercury_ai\models\decision_input.py:5

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Field:** meta
**Message:** Frozen dataclass has mutable field 'meta'

**Evidence:** Frozen dataclass 'DecisionOutcome' at line 5 in mercury_ai\models\decision_outcome.py contains mutable field 'meta: Dict[str, Any]'

**Location:** mercury_ai\models\decision_outcome.py:5

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** asset_stats
**Message:** Frozen dataclass has mutable field 'asset_stats'

**Evidence:** Frozen dataclass 'UniversePerformance' at line 23 in mercury_ai\models\equity_metrics.py contains mutable field 'asset_stats: Dict[str, AssetPerformance]'

**Location:** mercury_ai\models\equity_metrics.py:23

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'Evidence' at line 7 in mercury_ai\models\evidence.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\evidence.py:7

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** ranked_evidences
**Message:** Frozen dataclass has mutable field 'ranked_evidences'

**Evidence:** Frozen dataclass 'EvidenceRankingResult' at line 6 in mercury_ai\models\evidence_ranking.py contains mutable field 'ranked_evidences: List[Evidence]'

**Location:** mercury_ai\models\evidence_ranking.py:6

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** contribution_percentage
**Message:** Frozen dataclass has mutable field 'contribution_percentage'

**Evidence:** Frozen dataclass 'EvidenceRankingResult' at line 6 in mercury_ai\models\evidence_ranking.py contains mutable field 'contribution_percentage: dict'

**Location:** mercury_ai\models\evidence_ranking.py:6

#### WARNING: FairValueGapAnalysis (mercury_ai.models.fair_value_gap_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'FairValueGapAnalysis' at line 6 in mercury_ai\models\fair_value_gap_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\fair_value_gap_analysis.py:6

#### WARNING: LiquidityAnalysis (mercury_ai.models.liquidity_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'LiquidityAnalysis' at line 6 in mercury_ai\models\liquidity_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\liquidity_analysis.py:6

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'LiquidityResult' at line 5 in mercury_ai\models\liquidity_result.py contains mutable field 'metadata: dict'

**Location:** mercury_ai\models\liquidity_result.py:5

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** trend
**Message:** Frozen dataclass has mutable field 'trend'

**Evidence:** Frozen dataclass 'MarketContext' at line 17 in mercury_ai\models\market_context.py contains mutable field 'trend: List[Evidence]'

**Location:** mercury_ai\models\market_context.py:17

#### WARNING: MarketRegime (mercury_ai.models.market_regime)

**Field:** supporting_evidences
**Message:** Frozen dataclass has mutable field 'supporting_evidences'

**Evidence:** Frozen dataclass 'MarketRegime' at line 7 in mercury_ai\models\market_regime.py contains mutable field 'supporting_evidences: List[Evidence]'

**Location:** mercury_ai\models\market_regime.py:7

#### WARNING: MarketStructure (mercury_ai.models.market_structure)

**Field:** explanation
**Message:** Frozen dataclass has mutable field 'explanation'

**Evidence:** Frozen dataclass 'MarketStructure' at line 5 in mercury_ai\models\market_structure.py contains mutable field 'explanation: list[str]'

**Location:** mercury_ai\models\market_structure.py:5

#### WARNING: MarketStructureProfile (mercury_ai.models.market_structure_profile)

**Field:** current_sequence
**Message:** Frozen dataclass has mutable field 'current_sequence'

**Evidence:** Frozen dataclass 'MarketStructureProfile' at line 6 in mercury_ai\models\market_structure_profile.py contains mutable field 'current_sequence: List[str]'

**Location:** mercury_ai\models\market_structure_profile.py:6

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** confirmations
**Message:** Frozen dataclass has mutable field 'confirmations'

**Evidence:** Frozen dataclass 'MarketThesis' at line 8 in mercury_ai\models\market_thesis.py contains mutable field 'confirmations: List[str]'

**Location:** mercury_ai\models\market_thesis.py:8

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** conflicts
**Message:** Frozen dataclass has mutable field 'conflicts'

**Evidence:** Frozen dataclass 'MarketThesis' at line 8 in mercury_ai\models\market_thesis.py contains mutable field 'conflicts: List[str]'

**Location:** mercury_ai\models\market_thesis.py:8

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Field:** top_stats
**Message:** Frozen dataclass has mutable field 'top_stats'

**Evidence:** Frozen dataclass 'MemoryAuditResult' at line 13 in mercury_ai\models\memory_audit.py contains mutable field 'top_stats: List[str]'

**Location:** mercury_ai\models\memory_audit.py:13

#### WARNING: MomentumAnalysis (mercury_ai.models.momentum_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'MomentumAnalysis' at line 6 in mercury_ai\models\momentum_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\momentum_analysis.py:6

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** engine_responsibility
**Message:** Frozen dataclass has mutable field 'engine_responsibility'

**Evidence:** Frozen dataclass 'PerformanceMetrics' at line 5 in mercury_ai\models\performance_metrics.py contains mutable field 'engine_responsibility: Dict[str, int]'

**Location:** mercury_ai\models\performance_metrics.py:5

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** evidence_responsibility
**Message:** Frozen dataclass has mutable field 'evidence_responsibility'

**Evidence:** Frozen dataclass 'PerformanceMetrics' at line 5 in mercury_ai\models\performance_metrics.py contains mutable field 'evidence_responsibility: Dict[str, int]'

**Location:** mercury_ai\models\performance_metrics.py:5

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action)

**Field:** explanation
**Message:** Frozen dataclass has mutable field 'explanation'

**Evidence:** Frozen dataclass 'PriceActionAnalysis' at line 5 in mercury_ai\models\price_action.py contains mutable field 'explanation: list[str]'

**Location:** mercury_ai\models\price_action.py:5

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'PriceActionAnalysis' at line 5 in mercury_ai\models\price_action_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\price_action_analysis.py:5

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'ProbabilityResult' at line 5 in mercury_ai\models\probability_result.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\probability_result.py:5

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** confirmations
**Message:** Frozen dataclass has mutable field 'confirmations'

**Evidence:** Frozen dataclass 'ProfessionalThesis' at line 5 in mercury_ai\models\professional_thesis.py contains mutable field 'confirmations: List[str]'

**Location:** mercury_ai\models\professional_thesis.py:5

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** conflicts
**Message:** Frozen dataclass has mutable field 'conflicts'

**Evidence:** Frozen dataclass 'ProfessionalThesis' at line 5 in mercury_ai\models\professional_thesis.py contains mutable field 'conflicts: List[str]'

**Location:** mercury_ai\models\professional_thesis.py:5

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** risk_factors
**Message:** Frozen dataclass has mutable field 'risk_factors'

**Evidence:** Frozen dataclass 'ProfessionalThesis' at line 5 in mercury_ai\models\professional_thesis.py contains mutable field 'risk_factors: List[str]'

**Location:** mercury_ai\models\professional_thesis.py:5

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** decision_tree
**Message:** Frozen dataclass has mutable field 'decision_tree'

**Evidence:** Frozen dataclass 'ProfessionalThesis' at line 5 in mercury_ai\models\professional_thesis.py contains mutable field 'decision_tree: Dict[str, Any]'

**Location:** mercury_ai\models\professional_thesis.py:5

#### WARNING: Signal (mercury_ai.models.signal)

**Field:** evidences
**Message:** Frozen dataclass has mutable field 'evidences'

**Evidence:** Frozen dataclass 'Signal' at line 7 in mercury_ai\models\signal.py contains mutable field 'evidences: List[str]'

**Location:** mercury_ai\models\signal.py:7

#### WARNING: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Field:** explanation
**Message:** Frozen dataclass has mutable field 'explanation'

**Evidence:** Frozen dataclass 'SmartMoneyAnalysis' at line 7 in mercury_ai\models\smart_money.py contains mutable field 'explanation: list[str]'

**Location:** mercury_ai\models\smart_money.py:7

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** runtimes
**Message:** Frozen dataclass has mutable field 'runtimes'

**Evidence:** Frozen dataclass 'StressTestResult' at line 6 in mercury_ai\models\stress_test.py contains mutable field 'runtimes: List[float]'

**Location:** mercury_ai\models\stress_test.py:6

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** peak_memory
**Message:** Frozen dataclass has mutable field 'peak_memory'

**Evidence:** Frozen dataclass 'StressTestResult' at line 6 in mercury_ai\models\stress_test.py contains mutable field 'peak_memory: List[int]'

**Location:** mercury_ai\models\stress_test.py:6

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** exceptions
**Message:** Frozen dataclass has mutable field 'exceptions'

**Evidence:** Frozen dataclass 'StressTestResult' at line 6 in mercury_ai\models\stress_test.py contains mutable field 'exceptions: List[Exception]'

**Location:** mercury_ai\models\stress_test.py:6

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Field:** explanation
**Message:** Frozen dataclass has mutable field 'explanation'

**Evidence:** Frozen dataclass 'SupportResistanceAnalysis' at line 5 in mercury_ai\models\support_resistance.py contains mutable field 'explanation: list[str]'

**Location:** mercury_ai\models\support_resistance.py:5

#### WARNING: SwingSequenceResult (mercury_ai.models.swing_analysis)

**Field:** sequence
**Message:** Frozen dataclass has mutable field 'sequence'

**Evidence:** Frozen dataclass 'SwingSequenceResult' at line 18 in mercury_ai\models\swing_analysis.py contains mutable field 'sequence: List[str]'

**Location:** mercury_ai\models\swing_analysis.py:18

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** context_snapshot
**Message:** Frozen dataclass has mutable field 'context_snapshot'

**Evidence:** Frozen dataclass 'TradeMemory' at line 6 in mercury_ai\models\trade_memory.py contains mutable field 'context_snapshot: Dict[str, Any]'

**Location:** mercury_ai\models\trade_memory.py:6

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** evidences
**Message:** Frozen dataclass has mutable field 'evidences'

**Evidence:** Frozen dataclass 'TradeMemory' at line 6 in mercury_ai\models\trade_memory.py contains mutable field 'evidences: List[str]'

**Location:** mercury_ai\models\trade_memory.py:6

#### WARNING: TradePermission (mercury_ai.models.trade_permission)

**Field:** reasons
**Message:** Frozen dataclass has mutable field 'reasons'

**Evidence:** Frozen dataclass 'TradePermission' at line 5 in mercury_ai\models\trade_permission.py contains mutable field 'reasons: list[str]'

**Location:** mercury_ai\models\trade_permission.py:5

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** machine_readable
**Message:** Frozen dataclass has mutable field 'machine_readable'

**Evidence:** Frozen dataclass 'TradingExplanation' at line 8 in mercury_ai\models\trading_explanation.py contains mutable field 'machine_readable: Dict[str, Any]'

**Location:** mercury_ai\models\trading_explanation.py:8

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** engine_weights
**Message:** Frozen dataclass has mutable field 'engine_weights'

**Evidence:** Frozen dataclass 'TradingExplanation' at line 8 in mercury_ai\models\trading_explanation.py contains mutable field 'engine_weights: Dict[str, float]'

**Location:** mercury_ai\models\trading_explanation.py:8

#### WARNING: TrendAnalysis (mercury_ai.models.trend_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'TrendAnalysis' at line 5 in mercury_ai\models\trend_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\trend_analysis.py:5

#### WARNING: VolumeAnalysis (mercury_ai.models.volume_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'VolumeAnalysis' at line 6 in mercury_ai\models\volume_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\volume_analysis.py:6

#### WARNING: VWAPAnalysis (mercury_ai.models.vwap_analysis)

**Field:** metadata
**Message:** Frozen dataclass has mutable field 'metadata'

**Evidence:** Frozen dataclass 'VWAPAnalysis' at line 6 in mercury_ai\models\vwap_analysis.py contains mutable field 'metadata: Dict[str, Any]'

**Location:** mercury_ai\models\vwap_analysis.py:6

### MODEL_NOT_CONSUMED (8 findings)

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Message:** Model dataclass 'DecisionInput' not consumed by any external module

**Evidence:** Model dataclass 'DecisionInput' in mercury_ai.models.decision_input has no external consumers

**Location:** mercury_ai\models\decision_input.py:5

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Message:** Model dataclass 'DecisionOutcome' not consumed by any external module

**Evidence:** Model dataclass 'DecisionOutcome' in mercury_ai.models.decision_outcome has no external consumers

**Location:** mercury_ai\models\decision_outcome.py:5

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Message:** Model dataclass 'ProfessionalThesis' not consumed by any external module

**Evidence:** Model dataclass 'ProfessionalThesis' in mercury_ai.models.professional_thesis has no external consumers

**Location:** mercury_ai\models\professional_thesis.py:5

#### WARNING: HotspotSummary (mercury_ai.models.profiler_models)

**Message:** Model dataclass 'HotspotSummary' not consumed by any external module

**Evidence:** Model dataclass 'HotspotSummary' in mercury_ai.models.profiler_models has no external consumers

**Location:** mercury_ai\models\profiler_models.py:20

#### WARNING: Signal (mercury_ai.models.signal)

**Message:** Model dataclass 'Signal' not consumed by any external module

**Evidence:** Model dataclass 'Signal' in mercury_ai.models.signal has no external consumers

**Location:** mercury_ai\models\signal.py:7

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Message:** Model dataclass 'TradeMemory' not consumed by any external module

**Evidence:** Model dataclass 'TradeMemory' in mercury_ai.models.trade_memory has no external consumers

**Location:** mercury_ai\models\trade_memory.py:6

#### WARNING: TradePermission (mercury_ai.models.trade_permission)

**Message:** Model dataclass 'TradePermission' not consumed by any external module

**Evidence:** Model dataclass 'TradePermission' in mercury_ai.models.trade_permission has no external consumers

**Location:** mercury_ai\models\trade_permission.py:5

#### WARNING: TrendAnalysis (mercury_ai.models.trend_analysis)

**Message:** Model dataclass 'TrendAnalysis' not consumed by any external module

**Evidence:** Model dataclass 'TrendAnalysis' in mercury_ai.models.trend_analysis has no external consumers

**Location:** mercury_ai\models\trend_analysis.py:5

### NO_SERIALIZATION (99 findings)

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Message:** Dataclass has 8 fields but no serialization methods

**Evidence:** Dataclass 'StatisticalTestResult' in mercury_ai\analysis\benchmark_framework.py:38 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\benchmark_framework.py:38

#### WARNING: BuyAndHoldBaseline (mercury_ai.analysis.benchmark_framework)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'BuyAndHoldBaseline' in mercury_ai\analysis\benchmark_framework.py:51 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\benchmark_framework.py:51

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'EnhancedBenchmarkReport' in mercury_ai\analysis\benchmark_framework.py:61 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\benchmark_framework.py:61

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'ConfidenceComponents' in mercury_ai\analysis\confidence_engine.py:10 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\confidence_engine.py:10

#### WARNING: QualityReport (mercury_ai.analysis.data_quality_engine)

**Message:** Dataclass has 8 fields but no serialization methods

**Evidence:** Dataclass 'QualityReport' in mercury_ai\analysis\data_quality_engine.py:8 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\data_quality_engine.py:8

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'DecisionExplainability' in mercury_ai\analysis\decision_explainability.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\decision_explainability.py:7

#### WARNING: DecisionResolverResult (mercury_ai.analysis.decision_resolver_engine)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'DecisionResolverResult' in mercury_ai\analysis\decision_resolver_engine.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\decision_resolver_engine.py:6

#### WARNING: HealthStatus (mercury_ai.analysis.health_checker)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'HealthStatus' in mercury_ai\analysis\health_checker.py:12 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\health_checker.py:12

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Message:** Dataclass has 7 fields but no serialization methods

**Evidence:** Dataclass 'InstitutionalContext' in mercury_ai\analysis\institutional_context_builder.py:4 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\institutional_context_builder.py:4

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Message:** Dataclass has 7 fields but no serialization methods

**Evidence:** Dataclass 'InstitutionalContribution' in mercury_ai\analysis\institutional_contribution.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\institutional_contribution.py:5

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Message:** Dataclass has 8 fields but no serialization methods

**Evidence:** Dataclass 'InstitutionalScoreResult' in mercury_ai\analysis\institutional_score_engine.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\institutional_score_engine.py:5

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Message:** Dataclass has 15 fields but no serialization methods

**Evidence:** Dataclass 'PerformanceMetrics' in mercury_ai\analysis\metric_calculator.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\metric_calculator.py:6

#### WARNING: Notification (mercury_ai.analysis.notification_center)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'Notification' in mercury_ai\analysis\notification_center.py:8 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\notification_center.py:8

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Message:** Dataclass has 6 fields but no serialization methods

**Evidence:** Dataclass 'BatchReplayResult' in mercury_ai\analysis\replay_batch_processor.py:34 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\replay_batch_processor.py:34

#### WARNING: BatchReplayReport (mercury_ai.analysis.replay_batch_processor)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'BatchReplayReport' in mercury_ai\analysis\replay_batch_processor.py:45 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\replay_batch_processor.py:45

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'BOSResult' in mercury_ai\analysis\smart_money\bos_engine.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:7

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'CHOCHResult' in mercury_ai\analysis\smart_money\choch_engine.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:7

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass has 6 fields but no serialization methods

**Evidence:** Dataclass 'EqualHighGroup' in mercury_ai\analysis\smart_money\liquidity_engine.py:15 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass has 16 fields but no serialization methods

**Evidence:** Dataclass 'EqualHighMetrics' in mercury_ai\analysis\smart_money\liquidity_engine.py:24 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:24

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'EqualHighScore' in mercury_ai\analysis\smart_money\liquidity_engine.py:43 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'LiquidityEvent' in mercury_ai\analysis\smart_money\liquidity_event_engine.py:8 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:8

#### WARNING: UniverseAsset (mercury_ai.config.universe)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'UniverseAsset' in mercury_ai\config\universe.py:35 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\config\universe.py:35

#### WARNING: Asset (mercury_ai.core.asset_registry)

**Message:** Dataclass has 17 fields but no serialization methods

**Evidence:** Dataclass 'Asset' in mercury_ai\core\asset_registry.py:8 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\core\asset_registry.py:8

#### WARNING: AuditEvent (mercury_ai.core.audit_sink)

**Message:** Dataclass has 2 fields but no serialization methods

**Evidence:** Dataclass 'AuditEvent' in mercury_ai\core\audit_sink.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\core\audit_sink.py:6

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'EngineResult' in mercury_ai\core\base_engine.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\core\base_engine.py:6

#### WARNING: DataQualityResult (mercury_ai.core.data_quality_gate)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'DataQualityResult' in mercury_ai\core\data_quality_gate.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\core\data_quality_gate.py:5

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Message:** Dataclass has 16 fields but no serialization methods

**Evidence:** Dataclass 'TelemetryData' in mercury_ai\core\runtime_report.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\core\runtime_report.py:5

#### WARNING: AuditEvent (mercury_ai.core.security_center)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'AuditEvent' in mercury_ai\core\security_center.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\core\security_center.py:6

#### WARNING: ProviderMetrics (mercury_ai.data.mercury_data_provider)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'ProviderMetrics' in mercury_ai\data\mercury_data_provider.py:19 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\data\mercury_data_provider.py:19

#### WARNING: ProviderHealth (mercury_ai.data.mercury_data_provider)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'ProviderHealth' in mercury_ai\data\mercury_data_provider.py:25 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\data\mercury_data_provider.py:25

#### WARNING: ProviderRegistry (mercury_ai.data.mercury_data_provider)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'ProviderRegistry' in mercury_ai\data\mercury_data_provider.py:37 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\data\mercury_data_provider.py:37

#### WARNING: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'ReplayMetrics' in mercury_ai\database\replay_storage.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\database\replay_storage.py:7

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Message:** Dataclass has 21 fields but no serialization methods

**Evidence:** Dataclass 'AnalysisResult' in mercury_ai\models\analysis_result.py:29 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\analysis_result.py:29

#### WARNING: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'BenchmarkRunResult' in mercury_ai\models\benchmark_report.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\benchmark_report.py:7

#### WARNING: BenchmarkReport (mercury_ai.models.benchmark_report)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'BenchmarkReport' in mercury_ai\models\benchmark_report.py:15 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\benchmark_report.py:15

#### WARNING: CandlestickAnalysis (mercury_ai.models.candlestick_analysis)

**Message:** Dataclass has 11 fields but no serialization methods

**Evidence:** Dataclass 'CandlestickAnalysis' in mercury_ai\models\candlestick_analysis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\candlestick_analysis.py:5

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Message:** Dataclass has 8 fields but no serialization methods

**Evidence:** Dataclass 'ConfidenceResult' in mercury_ai\models\confidence_result.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\confidence_result.py:5

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Message:** Dataclass has 11 fields but no serialization methods

**Evidence:** Dataclass 'ConfluenceResult' in mercury_ai\models\confluence_result.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\confluence_result.py:6

#### WARNING: ConfluenceScore (mercury_ai.models.confluence_score)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'ConfluenceScore' in mercury_ai\models\confluence_score.py:4 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\confluence_score.py:4

#### WARNING: DataQualityResult (mercury_ai.models.data_quality_result)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'DataQualityResult' in mercury_ai\models\data_quality_result.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\data_quality_result.py:5

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'DecisionInput' in mercury_ai\models\decision_input.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\decision_input.py:5

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Message:** Dataclass has 6 fields but no serialization methods

**Evidence:** Dataclass 'DecisionNode' in mercury_ai\models\decision_node.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\decision_node.py:5

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'DecisionOutcome' in mercury_ai\models\decision_outcome.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\decision_outcome.py:5

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Message:** Dataclass has 32 fields but no serialization methods

**Evidence:** Dataclass 'DecisionResult' in mercury_ai\models\decision_result.py:12 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\decision_result.py:12

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Message:** Dataclass has 11 fields but no serialization methods

**Evidence:** Dataclass 'DecisionSnapshot' in mercury_ai\models\decision_snapshot.py:11 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\decision_snapshot.py:11

#### WARNING: DecisionTrace (mercury_ai.models.decision_trace)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'DecisionTrace' in mercury_ai\models\decision_trace.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\decision_trace.py:6

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Message:** Dataclass has 13 fields but no serialization methods

**Evidence:** Dataclass 'AssetPerformance' in mercury_ai\models\equity_metrics.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\equity_metrics.py:6

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'UniversePerformance' in mercury_ai\models\equity_metrics.py:23 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\equity_metrics.py:23

#### WARNING: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass has 13 fields but no serialization methods

**Evidence:** Dataclass 'Evidence' in mercury_ai\models\evidence.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\evidence.py:7

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Message:** Dataclass has 14 fields but no serialization methods

**Evidence:** Dataclass 'EvidenceRankingResult' in mercury_ai\models\evidence_ranking.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\evidence_ranking.py:6

#### WARNING: FairValueGapAnalysis (mercury_ai.models.fair_value_gap_analysis)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'FairValueGapAnalysis' in mercury_ai\models\fair_value_gap_analysis.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\fair_value_gap_analysis.py:6

#### WARNING: LiquidityAnalysis (mercury_ai.models.liquidity_analysis)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'LiquidityAnalysis' in mercury_ai\models\liquidity_analysis.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\liquidity_analysis.py:6

#### WARNING: LiquidityProfile (mercury_ai.models.liquidity_profile)

**Message:** Dataclass has 7 fields but no serialization methods

**Evidence:** Dataclass 'LiquidityProfile' in mercury_ai\models\liquidity_profile.py:4 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\liquidity_profile.py:4

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'LiquidityResult' in mercury_ai\models\liquidity_result.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\liquidity_result.py:5

#### WARNING: MarketCondition (mercury_ai.models.market_condition)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'MarketCondition' in mercury_ai\models\market_condition.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_condition.py:5

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'MarketContext' in mercury_ai\models\market_context.py:17 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_context.py:17

#### WARNING: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass has 14 fields but no serialization methods

**Evidence:** Dataclass 'MarketData' in mercury_ai\models\market_data.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_data.py:5

#### WARNING: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'MarketEvidenceBundle' in mercury_ai\models\market_evidence_bundle.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### WARNING: MarketRegime (mercury_ai.models.market_regime)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'MarketRegime' in mercury_ai\models\market_regime.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_regime.py:7

#### WARNING: MarketState (mercury_ai.models.market_state)

**Message:** Dataclass has 2 fields but no serialization methods

**Evidence:** Dataclass 'MarketState' in mercury_ai\models\market_state.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_state.py:5

#### WARNING: MarketStructure (mercury_ai.models.market_structure)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'MarketStructure' in mercury_ai\models\market_structure.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_structure.py:5

#### WARNING: MarketStructureProfile (mercury_ai.models.market_structure_profile)

**Message:** Dataclass has 54 fields but no serialization methods

**Evidence:** Dataclass 'MarketStructureProfile' in mercury_ai\models\market_structure_profile.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_structure_profile.py:6

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'MarketThesis' in mercury_ai\models\market_thesis.py:8 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\market_thesis.py:8

#### WARNING: MemorySnapshot (mercury_ai.models.memory_audit)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'MemorySnapshot' in mercury_ai\models\memory_audit.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\memory_audit.py:7

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'MemoryAuditResult' in mercury_ai\models\memory_audit.py:13 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\memory_audit.py:13

#### WARNING: MomentumAnalysis (mercury_ai.models.momentum_analysis)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'MomentumAnalysis' in mercury_ai\models\momentum_analysis.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\momentum_analysis.py:6

#### WARNING: MTFConsensus (mercury_ai.models.mtf_consensus)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'MTFConsensus' in mercury_ai\models\mtf_consensus.py:4 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\mtf_consensus.py:4

#### WARNING: StageMetric (mercury_ai.models.performance)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'StageMetric' in mercury_ai\models\performance.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\performance.py:5

#### WARNING: PipelineMetric (mercury_ai.models.performance)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'PipelineMetric' in mercury_ai\models\performance.py:13 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\performance.py:13

#### WARNING: HotspotReport (mercury_ai.models.performance)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'HotspotReport' in mercury_ai\models\performance.py:19 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\performance.py:19

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'PerformanceMetrics' in mercury_ai\models\performance_metrics.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\performance_metrics.py:5

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'PriceActionAnalysis' in mercury_ai\models\price_action.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\price_action.py:5

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action_analysis)

**Message:** Dataclass has 16 fields but no serialization methods

**Evidence:** Dataclass 'PriceActionAnalysis' in mercury_ai\models\price_action_analysis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\price_action_analysis.py:5

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass has 7 fields but no serialization methods

**Evidence:** Dataclass 'ProbabilityResult' in mercury_ai\models\probability_result.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\probability_result.py:5

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'ProfessionalThesis' in mercury_ai\models\professional_thesis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\professional_thesis.py:5

#### WARNING: StageProfile (mercury_ai.models.profiler_models)

**Message:** Dataclass has 6 fields but no serialization methods

**Evidence:** Dataclass 'StageProfile' in mercury_ai\models\profiler_models.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\profiler_models.py:5

#### WARNING: PipelineProfile (mercury_ai.models.profiler_models)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'PipelineProfile' in mercury_ai\models\profiler_models.py:14 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\profiler_models.py:14

#### WARNING: HotspotSummary (mercury_ai.models.profiler_models)

**Message:** Dataclass has 2 fields but no serialization methods

**Evidence:** Dataclass 'HotspotSummary' in mercury_ai\models\profiler_models.py:20 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\profiler_models.py:20

#### WARNING: BenchmarkMetrics (mercury_ai.models.regression)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'BenchmarkMetrics' in mercury_ai\models\regression.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\regression.py:5

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Message:** Dataclass has 6 fields but no serialization methods

**Evidence:** Dataclass 'RegressionResult' in mercury_ai\models\regression.py:13 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\regression.py:13

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Message:** Dataclass has 17 fields but no serialization methods

**Evidence:** Dataclass 'RiskAssessment' in mercury_ai\models\risk_assessment.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\risk_assessment.py:5

#### WARNING: SessionAnalysis (mercury_ai.models.session_analysis)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'SessionAnalysis' in mercury_ai\models\session_analysis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\session_analysis.py:5

#### WARNING: Signal (mercury_ai.models.signal)

**Message:** Dataclass has 11 fields but no serialization methods

**Evidence:** Dataclass 'Signal' in mercury_ai\models\signal.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\signal.py:7

#### WARNING: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'SmartMoneyAnalysis' in mercury_ai\models\smart_money.py:7 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\smart_money.py:7

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Message:** Dataclass has 9 fields but no serialization methods

**Evidence:** Dataclass 'StressTestResult' in mercury_ai\models\stress_test.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\stress_test.py:6

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'SupportResistanceAnalysis' in mercury_ai\models\support_resistance.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\support_resistance.py:5

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance_analysis)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'SupportResistanceAnalysis' in mercury_ai\models\support_resistance_analysis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\support_resistance_analysis.py:5

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass has 10 fields but no serialization methods

**Evidence:** Dataclass 'Swing' in mercury_ai\models\swing_analysis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\swing_analysis.py:5

#### WARNING: SwingSequenceResult (mercury_ai.models.swing_analysis)

**Message:** Dataclass has 8 fields but no serialization methods

**Evidence:** Dataclass 'SwingSequenceResult' in mercury_ai\models\swing_analysis.py:18 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\swing_analysis.py:18

#### WARNING: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'TradeFilterResult' in mercury_ai\models\trade_filter_result.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\trade_filter_result.py:6

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'TradeMemory' in mercury_ai\models\trade_memory.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\trade_memory.py:6

#### WARNING: TradePermission (mercury_ai.models.trade_permission)

**Message:** Dataclass has 3 fields but no serialization methods

**Evidence:** Dataclass 'TradePermission' in mercury_ai\models\trade_permission.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\trade_permission.py:5

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Message:** Dataclass has 30 fields but no serialization methods

**Evidence:** Dataclass 'TradingExplanation' in mercury_ai\models\trading_explanation.py:8 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\trading_explanation.py:8

#### WARNING: TrendAnalysis (mercury_ai.models.trend_analysis)

**Message:** Dataclass has 15 fields but no serialization methods

**Evidence:** Dataclass 'TrendAnalysis' in mercury_ai\models\trend_analysis.py:5 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\trend_analysis.py:5

#### WARNING: VersionMetadata (mercury_ai.models.version_metadata)

**Message:** Dataclass has 4 fields but no serialization methods

**Evidence:** Dataclass 'VersionMetadata' in mercury_ai\models\version_metadata.py:4 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\version_metadata.py:4

#### WARNING: VolatilityAnalysis (mercury_ai.models.volatility_analysis)

**Message:** Dataclass has 5 fields but no serialization methods

**Evidence:** Dataclass 'VolatilityAnalysis' in mercury_ai\models\volatility_analysis.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\volatility_analysis.py:6

#### WARNING: VolumeAnalysis (mercury_ai.models.volume_analysis)

**Message:** Dataclass has 12 fields but no serialization methods

**Evidence:** Dataclass 'VolumeAnalysis' in mercury_ai\models\volume_analysis.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\volume_analysis.py:6

#### WARNING: VolumeProfile (mercury_ai.models.volume_profile)

**Message:** Dataclass has 14 fields but no serialization methods

**Evidence:** Dataclass 'VolumeProfile' in mercury_ai\models\volume_profile.py:4 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\volume_profile.py:4

#### WARNING: VWAPAnalysis (mercury_ai.models.vwap_analysis)

**Message:** Dataclass has 11 fields but no serialization methods

**Evidence:** Dataclass 'VWAPAnalysis' in mercury_ai\models\vwap_analysis.py:6 has fields but no __post_init__, to_dict, or from_dict methods

**Location:** mercury_ai\models\vwap_analysis.py:6

### OPTIONAL_NO_DEFAULT (2 findings)

#### INFO: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** universe_performance
**Message:** Optional field 'universe_performance' has no explicit default (implicitly None)

**Evidence:** Field 'universe_performance: Optional[UniversePerformance]' at line 69 in mercury_ai\analysis\benchmark_framework.py is Optional but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:69

#### INFO: DecisionResolverResult (mercury_ai.analysis.decision_resolver_engine)

**Field:** confidence_override
**Message:** Optional field 'confidence_override' has no explicit default (implicitly None)

**Evidence:** Field 'confidence_override: Optional[float]' at line 8 in mercury_ai\analysis\decision_resolver_engine.py is Optional but has no default

**Location:** mercury_ai\analysis\decision_resolver_engine.py:8

### REQUIRED_FIELDS_NEED_VERIFICATION (239 findings)

#### INFO: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Message:** Dataclass 'DecisionExplainability' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['decision', 'reason', 'dominant_direction', 'opportunity_grade', 'conflicting_signals', 'institutional_score', 'confidence', 'triggered_rule']. Consumer: mercury_ai.brain.mercury_decision_engine

**Location:** mercury_ai\analysis\decision_explainability.py:7

#### INFO: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Message:** Dataclass 'DecisionExplainability' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['decision', 'reason', 'dominant_direction', 'opportunity_grade', 'conflicting_signals', 'institutional_score', 'confidence', 'triggered_rule']. Consumer: mercury_ai.brain.mercury_decision_engine

**Location:** mercury_ai\analysis\decision_explainability.py:7

#### INFO: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Message:** Dataclass 'InstitutionalContribution' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'weight', 'raw_score', 'weighted_score', 'direction', 'confidence', 'explanation']. Consumer: mercury_ai.analysis.confluence_engine

**Location:** mercury_ai\analysis\institutional_contribution.py:5

#### INFO: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Message:** Dataclass 'PerformanceMetrics' has 15 required fields - verify consumer provides all

**Evidence:** Required fields: ['accuracy', 'precision_buy', 'precision_sell', 'recall', 'f1_score', 'balanced_accuracy', 'mcc', 'profit_factor', 'expectancy', 'win_rate', 'avg_win', 'avg_loss', 'max_drawdown', 'sharpe_simplified', 'score_distribution']. Consumer: mercury_ai.analysis.post_decision_evaluation_engine

**Location:** mercury_ai\analysis\metric_calculator.py:6

#### INFO: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Message:** Dataclass 'BatchReplayResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'metrics', 'asset_performance', 'wall_time', 'cache_stats']. Consumer: mercury_ai.analysis.tests.test_replay_batch_processor

**Location:** mercury_ai\analysis\replay_batch_processor.py:34

#### INFO: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Message:** Dataclass 'BatchReplayResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'metrics', 'asset_performance', 'wall_time', 'cache_stats']. Consumer: mercury_ai.analysis.tests.test_replay_batch_processor

**Location:** mercury_ai\analysis\replay_batch_processor.py:34

#### INFO: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Message:** Dataclass 'BatchReplayResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'metrics', 'asset_performance', 'wall_time', 'cache_stats']. Consumer: mercury_ai.analysis.tests.test_replay_batch_processor

**Location:** mercury_ai\analysis\replay_batch_processor.py:34

#### INFO: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighGroup' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['touches', 'prices', 'timestamps', 'indices', 'strengths', 'ATRs']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:15

#### INFO: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighMetrics' has 16 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_count', 'average_price', 'minimum_price', 'maximum_price', 'price_deviation', 'average_strength', 'minimum_strength', 'maximum_strength', 'average_ATR', 'ATR_consistency', 'first_timestamp', 'last_timestamp', 'first_index', 'last_index', 'age_in_swings', 'cluster_width']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:24

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Message:** Dataclass 'EqualHighScore' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['touch_score', 'strength_score', 'atr_score', 'deviation_score', 'density_score', 'final_score', 'touch_count', 'average_price', 'average_strength', 'average_ATR', 'age_in_swings', 'cluster_density']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:43

#### INFO: AuditEvent (mercury_ai.core.audit_sink)

**Message:** Dataclass 'AuditEvent' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['stage_name', 'timestamp']. Consumer: mercury_ai.core.pipeline_audit_middleware

**Location:** mercury_ai\core\audit_sink.py:6

#### INFO: AuditEvent (mercury_ai.core.audit_sink)

**Message:** Dataclass 'AuditEvent' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['stage_name', 'timestamp']. Consumer: mercury_ai.core.security_center

**Location:** mercury_ai\core\audit_sink.py:6

#### INFO: EngineResult (mercury_ai.core.base_engine)

**Message:** Dataclass 'EngineResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['score', 'confidence', 'evidences', 'warnings', 'execution_time']. Consumer: mercury_ai.analysis.candlestick_engine

**Location:** mercury_ai\core\base_engine.py:6

#### INFO: EngineResult (mercury_ai.core.base_engine)

**Message:** Dataclass 'EngineResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['score', 'confidence', 'evidences', 'warnings', 'execution_time']. Consumer: mercury_ai.analysis.candlestick_engine

**Location:** mercury_ai\core\base_engine.py:6

#### INFO: TelemetryData (mercury_ai.core.runtime_report)

**Message:** Dataclass 'TelemetryData' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'start_time', 'end_time', 'execution_time', 'input_object', 'output_object']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\core\runtime_report.py:5

#### INFO: RuntimeReport (mercury_ai.core.runtime_report)

**Message:** Dataclass 'RuntimeReport' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\core\runtime_report.py:24

#### INFO: AuditEvent (mercury_ai.core.security_center)

**Message:** Dataclass 'AuditEvent' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['user', 'action', 'target', 'severity']. Consumer: mercury_ai.core.pipeline_audit_middleware

**Location:** mercury_ai\core\security_center.py:6

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: mercury_ai.analysis.benchmark_framework

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: mercury_ai.analysis.benchmark_framework

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: mercury_ai.analysis.historical_replay_engine

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: tests.test_performance_engine

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: tests.test_performance_engine

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: tests.test_performance_engine

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: tests.test_performance_engine

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: ReplayMetrics (mercury_ai.database.replay_storage)

**Message:** Dataclass 'ReplayMetrics' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['mae', 'mfe', 'pl', 'hit']. Consumer: tests.test_performance_engine

**Location:** mercury_ai\database\replay_storage.py:7

#### INFO: AnalysisResult (mercury_ai.models.analysis_result)

**Message:** Dataclass 'AnalysisResult' has 19 required fields - verify consumer provides all

**Evidence:** Required fields: ['market', 'context', 'trend', 'mtf_evidences', 'smart_money', 'market_regime', 'confluence', 'market_condition', 'market_state', 'candlestick_analysis', 'volatility_analysis', 'session_analysis', 'support_resistance', 'liquidity_analysis', 'risk_assessment', 'evidence_ranking', 'volume_analysis', 'structure_analysis', 'decision']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\analysis_result.py:29

#### INFO: AnalysisResult (mercury_ai.models.analysis_result)

**Message:** Dataclass 'AnalysisResult' has 19 required fields - verify consumer provides all

**Evidence:** Required fields: ['market', 'context', 'trend', 'mtf_evidences', 'smart_money', 'market_regime', 'confluence', 'market_condition', 'market_state', 'candlestick_analysis', 'volatility_analysis', 'session_analysis', 'support_resistance', 'liquidity_analysis', 'risk_assessment', 'evidence_ranking', 'volume_analysis', 'structure_analysis', 'decision']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\analysis_result.py:29

#### INFO: AnalysisResult (mercury_ai.models.analysis_result)

**Message:** Dataclass 'AnalysisResult' has 19 required fields - verify consumer provides all

**Evidence:** Required fields: ['market', 'context', 'trend', 'mtf_evidences', 'smart_money', 'market_regime', 'confluence', 'market_condition', 'market_state', 'candlestick_analysis', 'volatility_analysis', 'session_analysis', 'support_resistance', 'liquidity_analysis', 'risk_assessment', 'evidence_ranking', 'volume_analysis', 'structure_analysis', 'decision']. Consumer: tests.test_versioning

**Location:** mercury_ai\models\analysis_result.py:29

#### INFO: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Message:** Dataclass 'BenchmarkRunResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['timestamp', 'symbol', 'decision_result', 'execution_time', 'memory_usage']. Consumer: mercury_ai.analysis.benchmark_framework

**Location:** mercury_ai\models\benchmark_report.py:7

#### INFO: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Message:** Dataclass 'BenchmarkRunResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['timestamp', 'symbol', 'decision_result', 'execution_time', 'memory_usage']. Consumer: mercury_ai.analysis.benchmark_framework

**Location:** mercury_ai\models\benchmark_report.py:7

#### INFO: BenchmarkReport (mercury_ai.models.benchmark_report)

**Message:** Dataclass 'BenchmarkReport' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['version', 'results', 'average_execution_time', 'performance_metrics']. Consumer: mercury_ai.analysis.benchmark_framework

**Location:** mercury_ai\models\benchmark_report.py:15

#### INFO: ConfidenceResult (mercury_ai.models.confidence_result)

**Message:** Dataclass 'ConfidenceResult' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['confidence_score', 'final_confidence', 'confidence_grade', 'is_high', 'average_quality', 'consensus_score', 'market_score', 'confirmation_count']. Consumer: mercury_ai.analysis.confidence_engine

**Location:** mercury_ai\models\confidence_result.py:5

#### INFO: ConfidenceResult (mercury_ai.models.confidence_result)

**Message:** Dataclass 'ConfidenceResult' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['confidence_score', 'final_confidence', 'confidence_grade', 'is_high', 'average_quality', 'consensus_score', 'market_score', 'confirmation_count']. Consumer: mercury_ai.analysis.confidence_engine

**Location:** mercury_ai\models\confidence_result.py:5

#### INFO: ConfidenceResult (mercury_ai.models.confidence_result)

**Message:** Dataclass 'ConfidenceResult' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['confidence_score', 'final_confidence', 'confidence_grade', 'is_high', 'average_quality', 'consensus_score', 'market_score', 'confirmation_count']. Consumer: mercury_ai.brain.mercury_decision_engine

**Location:** mercury_ai\models\confidence_result.py:5

#### INFO: ConfidenceResult (mercury_ai.models.confidence_result)

**Message:** Dataclass 'ConfidenceResult' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['confidence_score', 'final_confidence', 'confidence_grade', 'is_high', 'average_quality', 'consensus_score', 'market_score', 'confirmation_count']. Consumer: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Location:** mercury_ai\models\confidence_result.py:5

#### INFO: ConfidenceResult (mercury_ai.models.confidence_result)

**Message:** Dataclass 'ConfidenceResult' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['confidence_score', 'final_confidence', 'confidence_grade', 'is_high', 'average_quality', 'consensus_score', 'market_score', 'confirmation_count']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\confidence_result.py:5

#### INFO: ConfluenceResult (mercury_ai.models.confluence_result)

**Message:** Dataclass 'ConfluenceResult' has 11 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_score', 'sell_score', 'neutral_score', 'agreement_percentage', 'conflicting_signals', 'independent_confirmations', 'weighted_score', 'confidence', 'dominant_direction', 'evidences', 'warnings']. Consumer: mercury_ai.analysis.confluence_engine

**Location:** mercury_ai\models\confluence_result.py:6

#### INFO: ConfluenceResult (mercury_ai.models.confluence_result)

**Message:** Dataclass 'ConfluenceResult' has 11 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_score', 'sell_score', 'neutral_score', 'agreement_percentage', 'conflicting_signals', 'independent_confirmations', 'weighted_score', 'confidence', 'dominant_direction', 'evidences', 'warnings']. Consumer: mercury_ai.brain.tests.test_explainability_engine

**Location:** mercury_ai\models\confluence_result.py:6

#### INFO: ConfluenceScore (mercury_ai.models.confluence_score)

**Message:** Dataclass 'ConfluenceScore' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['confluence_score', 'clarity_score', 'bullish_score', 'bearish_score', 'conflict_penalty']. Consumer: mercury_ai.analysis.confluence_score_engine

**Location:** mercury_ai\models\confluence_score.py:4

#### INFO: DataQualityResult (mercury_ai.models.data_quality_result)

**Message:** Dataclass 'DataQualityResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['score', 'warnings', 'missing_inputs', 'stale_data', 'quality_level']. Consumer: mercury_ai.core.data_quality_gate

**Location:** mercury_ai\models\data_quality_result.py:5

#### INFO: DataQualityResult (mercury_ai.models.data_quality_result)

**Message:** Dataclass 'DataQualityResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['score', 'warnings', 'missing_inputs', 'stale_data', 'quality_level']. Consumer: mercury_ai.core.data_quality_gate

**Location:** mercury_ai\models\data_quality_result.py:5

#### INFO: DecisionNode (mercury_ai.models.decision_node)

**Message:** Dataclass 'DecisionNode' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine', 'evidence', 'weight', 'score', 'influence', 'result']. Consumer: mercury_ai.analysis.decision_trace_engine

**Location:** mercury_ai\models\decision_node.py:5

#### INFO: DecisionResult (mercury_ai.models.decision_result)

**Message:** Dataclass 'DecisionResult' has 17 required fields - verify consumer provides all

**Evidence:** Required fields: ['decision', 'grade', 'confidence', 'clarity', 'risk_score', 'score', 'quality', 'expected_strength', 'buy_probability', 'sell_probability', 'wait_probability', 'expected_risk', 'expected_reward', 'expected_drawdown', 'audit_id', 'version_metadata', 'explanation']. Consumer: mercury_ai.analysis.decision_result_builder

**Location:** mercury_ai\models\decision_result.py:12

#### INFO: DecisionResult (mercury_ai.models.decision_result)

**Message:** Dataclass 'DecisionResult' has 17 required fields - verify consumer provides all

**Evidence:** Required fields: ['decision', 'grade', 'confidence', 'clarity', 'risk_score', 'score', 'quality', 'expected_strength', 'buy_probability', 'sell_probability', 'wait_probability', 'expected_risk', 'expected_reward', 'expected_drawdown', 'audit_id', 'version_metadata', 'explanation']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\decision_result.py:12

#### INFO: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Message:** Dataclass 'DecisionSnapshot' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['timestamp', 'asset', 'timeframe', 'context', 'evidence_bundle', 'decision_result', 'version_metadata', 'audit_events', 'session_id']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\decision_snapshot.py:11

#### INFO: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Message:** Dataclass 'DecisionSnapshot' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['timestamp', 'asset', 'timeframe', 'context', 'evidence_bundle', 'decision_result', 'version_metadata', 'audit_events', 'session_id']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\decision_snapshot.py:11

#### INFO: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Message:** Dataclass 'DecisionSnapshot' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['timestamp', 'asset', 'timeframe', 'context', 'evidence_bundle', 'decision_result', 'version_metadata', 'audit_events', 'session_id']. Consumer: tests.test_versioning

**Location:** mercury_ai\models\decision_snapshot.py:11

#### INFO: AssetPerformance (mercury_ai.models.equity_metrics)

**Message:** Dataclass 'AssetPerformance' has 13 required fields - verify consumer provides all

**Evidence:** Required fields: ['asset', 'total_trades', 'pnl_accumulated', 'win_rate', 'profit_factor', 'expectancy', 'avg_win', 'avg_loss', 'max_drawdown', 'recovery_time_candles', 'sharpe_ratio', 'sortino_ratio', 'equity_curve']. Consumer: mercury_ai.analysis.performance_engine

**Location:** mercury_ai\models\equity_metrics.py:6

#### INFO: AssetPerformance (mercury_ai.models.equity_metrics)

**Message:** Dataclass 'AssetPerformance' has 13 required fields - verify consumer provides all

**Evidence:** Required fields: ['asset', 'total_trades', 'pnl_accumulated', 'win_rate', 'profit_factor', 'expectancy', 'avg_win', 'avg_loss', 'max_drawdown', 'recovery_time_candles', 'sharpe_ratio', 'sortino_ratio', 'equity_curve']. Consumer: mercury_ai.analysis.performance_engine

**Location:** mercury_ai\models\equity_metrics.py:6

#### INFO: AssetPerformance (mercury_ai.models.equity_metrics)

**Message:** Dataclass 'AssetPerformance' has 13 required fields - verify consumer provides all

**Evidence:** Required fields: ['asset', 'total_trades', 'pnl_accumulated', 'win_rate', 'profit_factor', 'expectancy', 'avg_win', 'avg_loss', 'max_drawdown', 'recovery_time_candles', 'sharpe_ratio', 'sortino_ratio', 'equity_curve']. Consumer: mercury_ai.analysis.replay_batch_processor

**Location:** mercury_ai\models\equity_metrics.py:6

#### INFO: UniversePerformance (mercury_ai.models.equity_metrics)

**Message:** Dataclass 'UniversePerformance' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['total_assets', 'global_pnl', 'global_win_rate', 'global_profit_factor', 'global_max_drawdown', 'global_sharpe', 'global_sortino', 'asset_stats', 'consolidated_equity_curve']. Consumer: mercury_ai.analysis.performance_engine

**Location:** mercury_ai\models\equity_metrics.py:23

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.context_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.context_intelligence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.fair_value_gap_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.market_structure_intelligence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.market_structure_intelligence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.momentum_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.momentum_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.swing_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.swing_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.trend_analyzer

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.trend_analyzer

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.trend_analyzer

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.trend_analyzer

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.trend_analyzer

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.volatility_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.volume_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.volume_intelligence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.volume_intelligence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.vwap_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.smart_money.liquidity_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.smart_money.liquidity_event_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.smart_money.smart_money_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.smart_money.smart_money_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.smart_money.smart_money_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: mercury_ai.brain.tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_adaptive_weighting

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_adaptive_weighting

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_conflict_resolution

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_evidence_quality_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: Evidence (mercury_ai.models.evidence)

**Message:** Dataclass 'Evidence' has 7 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_name', 'evidence_name', 'direction', 'strength', 'confidence', 'description', 'weight']. Consumer: tests.test_validation_engine

**Location:** mercury_ai\models\evidence.py:7

#### INFO: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Message:** Dataclass 'EvidenceRankingResult' has 11 required fields - verify consumer provides all

**Evidence:** Required fields: ['ranked_evidences', 'contribution_percentage', 'strongest_evidence', 'weakest_evidence', 'total_weight', 'bullish_weight', 'bearish_weight', 'neutral_weight', 'bullish_score', 'bearish_score', 'neutral_score']. Consumer: mercury_ai.analysis.evidence_ranking_engine

**Location:** mercury_ai\models\evidence_ranking.py:6

#### INFO: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Message:** Dataclass 'EvidenceRankingResult' has 11 required fields - verify consumer provides all

**Evidence:** Required fields: ['ranked_evidences', 'contribution_percentage', 'strongest_evidence', 'weakest_evidence', 'total_weight', 'bullish_weight', 'bearish_weight', 'neutral_weight', 'bullish_score', 'bearish_score', 'neutral_score']. Consumer: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Location:** mercury_ai\models\evidence_ranking.py:6

#### INFO: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Message:** Dataclass 'EvidenceRankingResult' has 11 required fields - verify consumer provides all

**Evidence:** Required fields: ['ranked_evidences', 'contribution_percentage', 'strongest_evidence', 'weakest_evidence', 'total_weight', 'bullish_weight', 'bearish_weight', 'neutral_weight', 'bullish_score', 'bearish_score', 'neutral_score']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\evidence_ranking.py:6

#### INFO: LiquidityResult (mercury_ai.models.liquidity_result)

**Message:** Dataclass 'LiquidityResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'score', 'confidence', 'strength', 'metadata']. Consumer: mercury_ai.analysis.smart_money.liquidity_engine

**Location:** mercury_ai\models\liquidity_result.py:5

#### INFO: LiquidityResult (mercury_ai.models.liquidity_result)

**Message:** Dataclass 'LiquidityResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'score', 'confidence', 'strength', 'metadata']. Consumer: mercury_ai.analysis.smart_money.liquidity_engine

**Location:** mercury_ai\models\liquidity_result.py:5

#### INFO: LiquidityResult (mercury_ai.models.liquidity_result)

**Message:** Dataclass 'LiquidityResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'score', 'confidence', 'strength', 'metadata']. Consumer: mercury_ai.analysis.smart_money.liquidity_engine

**Location:** mercury_ai\models\liquidity_result.py:5

#### INFO: LiquidityResult (mercury_ai.models.liquidity_result)

**Message:** Dataclass 'LiquidityResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'score', 'confidence', 'strength', 'metadata']. Consumer: mercury_ai.analysis.smart_money.liquidity_engine

**Location:** mercury_ai\models\liquidity_result.py:5

#### INFO: MarketContext (mercury_ai.models.market_context)

**Message:** Dataclass 'MarketContext' has 10 required fields - verify consumer provides all

**Evidence:** Required fields: ['market', 'trend', 'price_action', 'support_resistance', 'smart_money', 'liquidity', 'market_state', 'market_regime', 'mtf_consensus', 'risk_assessment']. Consumer: mercury_ai.analysis.market_context_builder

**Location:** mercury_ai\models\market_context.py:17

#### INFO: MarketContext (mercury_ai.models.market_context)

**Message:** Dataclass 'MarketContext' has 10 required fields - verify consumer provides all

**Evidence:** Required fields: ['market', 'trend', 'price_action', 'support_resistance', 'smart_money', 'liquidity', 'market_state', 'market_regime', 'mtf_consensus', 'risk_assessment']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\market_context.py:17

#### INFO: MarketContext (mercury_ai.models.market_context)

**Message:** Dataclass 'MarketContext' has 10 required fields - verify consumer provides all

**Evidence:** Required fields: ['market', 'trend', 'price_action', 'support_resistance', 'smart_money', 'liquidity', 'market_state', 'market_regime', 'mtf_consensus', 'risk_assessment']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\market_context.py:17

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.mtf_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_candlestick_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_candlestick_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_trend_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.analysis.tests.test_trend_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketData (mercury_ai.models.market_data)

**Message:** Dataclass 'MarketData' has 14 required fields - verify consumer provides all

**Evidence:** Required fields: ['symbol', 'timeframe', 'close', 'ema9', 'ema21', 'ema50', 'rsi', 'atr', 'adx', 'macd', 'macd_signal', 'bollinger_upper', 'bollinger_lower', 'volume']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\market_data.py:5

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.analysis.evidence_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.mercury_decision_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: mercury_ai.brain.tests.test_probability_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: tests.test_probability_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: tests.test_validation_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Message:** Dataclass 'MarketEvidenceBundle' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['evidences', 'timestamp', 'asset', 'timeframe']. Consumer: tests.test_validation_engine

**Location:** mercury_ai\models\market_evidence_bundle.py:6

#### INFO: MarketRegime (mercury_ai.models.market_regime)

**Message:** Dataclass 'MarketRegime' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['regime', 'confidence', 'supporting_evidences']. Consumer: mercury_ai.analysis.market_regime_engine

**Location:** mercury_ai\models\market_regime.py:7

#### INFO: MarketRegime (mercury_ai.models.market_regime)

**Message:** Dataclass 'MarketRegime' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['regime', 'confidence', 'supporting_evidences']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\market_regime.py:7

#### INFO: MarketRegime (mercury_ai.models.market_regime)

**Message:** Dataclass 'MarketRegime' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['regime', 'confidence', 'supporting_evidences']. Consumer: tests.test_adaptive_weighting

**Location:** mercury_ai\models\market_regime.py:7

#### INFO: MarketRegime (mercury_ai.models.market_regime)

**Message:** Dataclass 'MarketRegime' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['regime', 'confidence', 'supporting_evidences']. Consumer: tests.test_adaptive_weighting

**Location:** mercury_ai\models\market_regime.py:7

#### INFO: MarketState (mercury_ai.models.market_state)

**Message:** Dataclass 'MarketState' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['state', 'explanation']. Consumer: mercury_ai.analysis.market_state_engine

**Location:** mercury_ai\models\market_state.py:5

#### INFO: MarketState (mercury_ai.models.market_state)

**Message:** Dataclass 'MarketState' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['state', 'explanation']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\market_state.py:5

#### INFO: MarketState (mercury_ai.models.market_state)

**Message:** Dataclass 'MarketState' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['state', 'explanation']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\market_state.py:5

#### INFO: MarketState (mercury_ai.models.market_state)

**Message:** Dataclass 'MarketState' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['state', 'explanation']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\market_state.py:5

#### INFO: MarketThesis (mercury_ai.models.market_thesis)

**Message:** Dataclass 'MarketThesis' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['market_bias', 'confluence_score', 'confidence', 'risk', 'market_state']. Consumer: mercury_ai.analysis.market_thesis_builder

**Location:** mercury_ai\models\market_thesis.py:8

#### INFO: MemorySnapshot (mercury_ai.models.memory_audit)

**Message:** Dataclass 'MemorySnapshot' has 2 required fields - verify consumer provides all

**Evidence:** Required fields: ['snapshot', 'gc_count']. Consumer: mercury_ai.utils.memory_auditor

**Location:** mercury_ai\models\memory_audit.py:7

#### INFO: MemoryAuditResult (mercury_ai.models.memory_audit)

**Message:** Dataclass 'MemoryAuditResult' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['peak_memory_diff', 'allocation_diff_size', 'allocation_diff_count', 'gc_count_diff', 'top_stats']. Consumer: mercury_ai.utils.memory_auditor

**Location:** mercury_ai\models\memory_audit.py:13

#### INFO: MTFConsensus (mercury_ai.models.mtf_consensus)

**Message:** Dataclass 'MTFConsensus' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['global_bias', 'local_bias', 'conflict_detected', 'alignment_score']. Consumer: mercury_ai.analysis.mtf_engine

**Location:** mercury_ai\models\mtf_consensus.py:4

#### INFO: MTFConsensus (mercury_ai.models.mtf_consensus)

**Message:** Dataclass 'MTFConsensus' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['global_bias', 'local_bias', 'conflict_detected', 'alignment_score']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\mtf_consensus.py:4

#### INFO: MTFConsensus (mercury_ai.models.mtf_consensus)

**Message:** Dataclass 'MTFConsensus' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['global_bias', 'local_bias', 'conflict_detected', 'alignment_score']. Consumer: tests.test_confidence_calibration

**Location:** mercury_ai\models\mtf_consensus.py:4

#### INFO: StageMetric (mercury_ai.models.performance)

**Message:** Dataclass 'StageMetric' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['name', 'duration', 'memory_delta', 'percentage_total', 'nested_metrics']. Consumer: mercury_ai.utils.performance_collector

**Location:** mercury_ai\models\performance.py:5

#### INFO: PipelineMetric (mercury_ai.models.performance)

**Message:** Dataclass 'PipelineMetric' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['pipeline_name', 'total_duration', 'stage_metrics']. Consumer: mercury_ai.utils.performance_collector

**Location:** mercury_ai\models\performance.py:13

#### INFO: HotspotReport (mercury_ai.models.performance)

**Message:** Dataclass 'HotspotReport' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['pipeline_name', 'total_duration', 'hotspots']. Consumer: mercury_ai.utils.performance_collector

**Location:** mercury_ai\models\performance.py:19

#### INFO: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Message:** Dataclass 'PerformanceMetrics' has 10 required fields - verify consumer provides all

**Evidence:** Required fields: ['total_trades', 'correct', 'incorrect', 'late_entries', 'early_entries', 'missed_trades', 'false_positives', 'false_negatives', 'engine_responsibility', 'evidence_responsibility']. Consumer: mercury_ai.analysis.metric_calculator

**Location:** mercury_ai\models\performance_metrics.py:5

#### INFO: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Message:** Dataclass 'PerformanceMetrics' has 10 required fields - verify consumer provides all

**Evidence:** Required fields: ['total_trades', 'correct', 'incorrect', 'late_entries', 'early_entries', 'missed_trades', 'false_positives', 'false_negatives', 'engine_responsibility', 'evidence_responsibility']. Consumer: mercury_ai.analysis.post_decision_evaluation_engine

**Location:** mercury_ai\models\performance_metrics.py:5

#### INFO: PriceActionAnalysis (mercury_ai.models.price_action)

**Message:** Dataclass 'PriceActionAnalysis' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['trend_structure', 'last_event', 'confidence', 'explanation']. Consumer: mercury_ai.analysis.price_action_analyzer

**Location:** mercury_ai\models\price_action.py:5

#### INFO: PriceActionAnalysis (mercury_ai.models.price_action)

**Message:** Dataclass 'PriceActionAnalysis' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['trend_structure', 'last_event', 'confidence', 'explanation']. Consumer: mercury_ai.analysis.price_action_analyzer

**Location:** mercury_ai\models\price_action.py:5

#### INFO: PriceActionAnalysis (mercury_ai.models.price_action)

**Message:** Dataclass 'PriceActionAnalysis' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['trend_structure', 'last_event', 'confidence', 'explanation']. Consumer: mercury_ai.analysis.price_action_engine

**Location:** mercury_ai\models\price_action.py:5

#### INFO: PriceActionAnalysis (mercury_ai.models.price_action)

**Message:** Dataclass 'PriceActionAnalysis' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['trend_structure', 'last_event', 'confidence', 'explanation']. Consumer: mercury_ai.analysis.price_action_engine

**Location:** mercury_ai\models\price_action.py:5

#### INFO: PriceActionAnalysis (mercury_ai.models.price_action)

**Message:** Dataclass 'PriceActionAnalysis' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['trend_structure', 'last_event', 'confidence', 'explanation']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\price_action.py:5

#### INFO: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass 'ProbabilityResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_probability', 'sell_probability', 'neutral_probability', 'expected_risk', 'opportunity_grade', 'institutional_confidence']. Consumer: mercury_ai.brain.probability_engine

**Location:** mercury_ai\models\probability_result.py:5

#### INFO: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass 'ProbabilityResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_probability', 'sell_probability', 'neutral_probability', 'expected_risk', 'opportunity_grade', 'institutional_confidence']. Consumer: mercury_ai.brain.tests.test_explainability_engine

**Location:** mercury_ai\models\probability_result.py:5

#### INFO: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass 'ProbabilityResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_probability', 'sell_probability', 'neutral_probability', 'expected_risk', 'opportunity_grade', 'institutional_confidence']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\probability_result.py:5

#### INFO: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass 'ProbabilityResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_probability', 'sell_probability', 'neutral_probability', 'expected_risk', 'opportunity_grade', 'institutional_confidence']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\probability_result.py:5

#### INFO: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass 'ProbabilityResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_probability', 'sell_probability', 'neutral_probability', 'expected_risk', 'opportunity_grade', 'institutional_confidence']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\probability_result.py:5

#### INFO: ProbabilityResult (mercury_ai.models.probability_result)

**Message:** Dataclass 'ProbabilityResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['buy_probability', 'sell_probability', 'neutral_probability', 'expected_risk', 'opportunity_grade', 'institutional_confidence']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\probability_result.py:5

#### INFO: StageProfile (mercury_ai.models.profiler_models)

**Message:** Dataclass 'StageProfile' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['name', 'duration', 'memory_peak', 'memory_delta', 'percentage_total']. Consumer: mercury_ai.core.pipeline_profiler

**Location:** mercury_ai\models\profiler_models.py:5

#### INFO: PipelineProfile (mercury_ai.models.profiler_models)

**Message:** Dataclass 'PipelineProfile' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['pipeline_name', 'total_duration', 'stage_profiles']. Consumer: mercury_ai.core.pipeline_profiler

**Location:** mercury_ai\models\profiler_models.py:14

#### INFO: PipelineProfile (mercury_ai.models.profiler_models)

**Message:** Dataclass 'PipelineProfile' has 3 required fields - verify consumer provides all

**Evidence:** Required fields: ['pipeline_name', 'total_duration', 'stage_profiles']. Consumer: mercury_ai.core.pipeline_profiler

**Location:** mercury_ai\models\profiler_models.py:14

#### INFO: BenchmarkMetrics (mercury_ai.models.regression)

**Message:** Dataclass 'BenchmarkMetrics' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['timestamp', 'duration', 'peak_memory', 'allocation_count', 'gc_count']. Consumer: mercury_ai.utils.regression_detector

**Location:** mercury_ai\models\regression.py:5

#### INFO: RegressionResult (mercury_ai.models.regression)

**Message:** Dataclass 'RegressionResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['is_regression', 'performance_delta', 'memory_delta', 'allocation_delta', 'gc_delta', 'message']. Consumer: mercury_ai.utils.regression_detector

**Location:** mercury_ai\models\regression.py:13

#### INFO: RegressionResult (mercury_ai.models.regression)

**Message:** Dataclass 'RegressionResult' has 6 required fields - verify consumer provides all

**Evidence:** Required fields: ['is_regression', 'performance_delta', 'memory_delta', 'allocation_delta', 'gc_delta', 'message']. Consumer: mercury_ai.utils.regression_detector

**Location:** mercury_ai\models\regression.py:13

#### INFO: RiskAssessment (mercury_ai.models.risk_assessment)

**Message:** Dataclass 'RiskAssessment' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['suggested_stop', 'suggested_take_profit', 'risk_reward_ratio', 'expected_drawdown', 'expected_volatility', 'trade_quality', 'max_exposure', 'invalidation_point', 'institutional_risk_score']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\risk_assessment.py:5

#### INFO: RiskAssessment (mercury_ai.models.risk_assessment)

**Message:** Dataclass 'RiskAssessment' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['suggested_stop', 'suggested_take_profit', 'risk_reward_ratio', 'expected_drawdown', 'expected_volatility', 'trade_quality', 'max_exposure', 'invalidation_point', 'institutional_risk_score']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\risk_assessment.py:5

#### INFO: RiskAssessment (mercury_ai.models.risk_assessment)

**Message:** Dataclass 'RiskAssessment' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['suggested_stop', 'suggested_take_profit', 'risk_reward_ratio', 'expected_drawdown', 'expected_volatility', 'trade_quality', 'max_exposure', 'invalidation_point', 'institutional_risk_score']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\risk_assessment.py:5

#### INFO: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Message:** Dataclass 'SmartMoneyAnalysis' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['structure']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\smart_money.py:7

#### INFO: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Message:** Dataclass 'SmartMoneyAnalysis' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['structure']. Consumer: mercury_ai.analysis.smart_money.smart_money_engine

**Location:** mercury_ai\models\smart_money.py:7

#### INFO: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Message:** Dataclass 'SmartMoneyAnalysis' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['structure']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\smart_money.py:7

#### INFO: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Message:** Dataclass 'SmartMoneyAnalysis' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['structure']. Consumer: mercury_ai.analysis.tests.test_risk_engine

**Location:** mercury_ai\models\smart_money.py:7

#### INFO: StressTestResult (mercury_ai.models.stress_test)

**Message:** Dataclass 'StressTestResult' has 9 required fields - verify consumer provides all

**Evidence:** Required fields: ['pipeline_name', 'scenario', 'dataset_size', 'repetitions', 'runtimes', 'peak_memory', 'exceptions', 'is_deterministic', 'failure_count']. Consumer: mercury_ai.utils.stress_tester

**Location:** mercury_ai\models\stress_test.py:6

#### INFO: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Message:** Dataclass 'SupportResistanceAnalysis' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['support', 'resistance', 'distance_support', 'distance_resistance', 'explanation']. Consumer: mercury_ai.analysis.risk_engine

**Location:** mercury_ai\models\support_resistance.py:5

#### INFO: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Message:** Dataclass 'SupportResistanceAnalysis' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['support', 'resistance', 'distance_support', 'distance_resistance', 'explanation']. Consumer: mercury_ai.analysis.support_resistance_analyzer

**Location:** mercury_ai\models\support_resistance.py:5

#### INFO: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Message:** Dataclass 'SupportResistanceAnalysis' has 5 required fields - verify consumer provides all

**Evidence:** Required fields: ['support', 'resistance', 'distance_support', 'distance_resistance', 'explanation']. Consumer: mercury_ai.analysis.support_resistance_analyzer

**Location:** mercury_ai\models\support_resistance.py:5

#### INFO: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass 'Swing' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['type', 'classification', 'price', 'timestamp', 'index', 'atr', 'strength', 'volume']. Consumer: mercury_ai.analysis.swing_engine

**Location:** mercury_ai\models\swing_analysis.py:5

#### INFO: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass 'Swing' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['type', 'classification', 'price', 'timestamp', 'index', 'atr', 'strength', 'volume']. Consumer: mercury_ai.analysis.swing_engine

**Location:** mercury_ai\models\swing_analysis.py:5

#### INFO: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass 'Swing' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['type', 'classification', 'price', 'timestamp', 'index', 'atr', 'strength', 'volume']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_edge_cases

**Location:** mercury_ai\models\swing_analysis.py:5

#### INFO: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass 'Swing' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['type', 'classification', 'price', 'timestamp', 'index', 'atr', 'strength', 'volume']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_engine

**Location:** mercury_ai\models\swing_analysis.py:5

#### INFO: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass 'Swing' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['type', 'classification', 'price', 'timestamp', 'index', 'atr', 'strength', 'volume']. Consumer: mercury_ai.analysis.smart_money.tests.test_liquidity_stress

**Location:** mercury_ai\models\swing_analysis.py:5

#### INFO: Swing (mercury_ai.models.swing_analysis)

**Message:** Dataclass 'Swing' has 8 required fields - verify consumer provides all

**Evidence:** Required fields: ['type', 'classification', 'price', 'timestamp', 'index', 'atr', 'strength', 'volume']. Consumer: tests.test_benchmark_integration

**Location:** mercury_ai\models\swing_analysis.py:5

#### INFO: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass 'TradeFilterResult' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['allowed']. Consumer: mercury_ai.analysis.institutional_trade_filter_engine

**Location:** mercury_ai\models\trade_filter_result.py:6

#### INFO: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass 'TradeFilterResult' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['allowed']. Consumer: mercury_ai.brain.tests.test_mercury_decision_benchmark

**Location:** mercury_ai\models\trade_filter_result.py:6

#### INFO: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass 'TradeFilterResult' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['allowed']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\trade_filter_result.py:6

#### INFO: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass 'TradeFilterResult' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['allowed']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\trade_filter_result.py:6

#### INFO: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass 'TradeFilterResult' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['allowed']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\trade_filter_result.py:6

#### INFO: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Message:** Dataclass 'TradeFilterResult' has 1 required fields - verify consumer provides all

**Evidence:** Required fields: ['allowed']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\trade_filter_result.py:6

#### INFO: TradingExplanation (mercury_ai.models.trading_explanation)

**Message:** Dataclass 'TradingExplanation' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['exec_summary', 'decision_rationale', 'market_context', 'trend_context', 'liquidity_context', 'structure_context', 'momentum_context', 'volume_context', 'smart_money_context', 'confluence_context', 'risk_assessment', 'confidence_rationale']. Consumer: mercury_ai.analysis.narrative_engine

**Location:** mercury_ai\models\trading_explanation.py:8

#### INFO: TradingExplanation (mercury_ai.models.trading_explanation)

**Message:** Dataclass 'TradingExplanation' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['exec_summary', 'decision_rationale', 'market_context', 'trend_context', 'liquidity_context', 'structure_context', 'momentum_context', 'volume_context', 'smart_money_context', 'confluence_context', 'risk_assessment', 'confidence_rationale']. Consumer: mercury_ai.brain.explainability_engine

**Location:** mercury_ai\models\trading_explanation.py:8

#### INFO: TradingExplanation (mercury_ai.models.trading_explanation)

**Message:** Dataclass 'TradingExplanation' has 12 required fields - verify consumer provides all

**Evidence:** Required fields: ['exec_summary', 'decision_rationale', 'market_context', 'trend_context', 'liquidity_context', 'structure_context', 'momentum_context', 'volume_context', 'smart_money_context', 'confluence_context', 'risk_assessment', 'confidence_rationale']. Consumer: mercury_ai.brain.tests.test_mercury_decision_engine

**Location:** mercury_ai\models\trading_explanation.py:8

#### INFO: VersionMetadata (mercury_ai.models.version_metadata)

**Message:** Dataclass 'VersionMetadata' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_version', 'pipeline_version', 'context_version', 'weights_version']. Consumer: mercury_ai.analysis.decision_result_builder

**Location:** mercury_ai\models\version_metadata.py:4

#### INFO: VersionMetadata (mercury_ai.models.version_metadata)

**Message:** Dataclass 'VersionMetadata' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_version', 'pipeline_version', 'context_version', 'weights_version']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\version_metadata.py:4

#### INFO: VersionMetadata (mercury_ai.models.version_metadata)

**Message:** Dataclass 'VersionMetadata' has 4 required fields - verify consumer provides all

**Evidence:** Required fields: ['engine_version', 'pipeline_version', 'context_version', 'weights_version']. Consumer: mercury_ai.core.analysis_pipeline

**Location:** mercury_ai\models\version_metadata.py:4

### REQUIRED_FIELD_NO_DEFAULT (482 findings)

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** t_statistic
**Message:** Required field 't_statistic' has no default value

**Evidence:** Field 't_statistic: float' at line 40 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:40

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** p_value
**Message:** Required field 'p_value' has no default value

**Evidence:** Field 'p_value: float' at line 41 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:41

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** is_significant_95
**Message:** Required field 'is_significant_95' has no default value

**Evidence:** Field 'is_significant_95: bool' at line 42 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:42

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** bootstrap_ci_lower
**Message:** Required field 'bootstrap_ci_lower' has no default value

**Evidence:** Field 'bootstrap_ci_lower: float' at line 43 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:43

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** bootstrap_ci_upper
**Message:** Required field 'bootstrap_ci_upper' has no default value

**Evidence:** Field 'bootstrap_ci_upper: float' at line 44 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:44

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** bootstrap_samples
**Message:** Required field 'bootstrap_samples' has no default value

**Evidence:** Field 'bootstrap_samples: int' at line 45 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:45

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** mean_return
**Message:** Required field 'mean_return' has no default value

**Evidence:** Field 'mean_return: float' at line 46 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:46

#### WARNING: StatisticalTestResult (mercury_ai.analysis.benchmark_framework)

**Field:** std_return
**Message:** Required field 'std_return' has no default value

**Evidence:** Field 'std_return: float' at line 47 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:47

#### WARNING: BuyAndHoldBaseline (mercury_ai.analysis.benchmark_framework)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 53 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:53

#### WARNING: BuyAndHoldBaseline (mercury_ai.analysis.benchmark_framework)

**Field:** total_return_pct
**Message:** Required field 'total_return_pct' has no default value

**Evidence:** Field 'total_return_pct: float' at line 54 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:54

#### WARNING: BuyAndHoldBaseline (mercury_ai.analysis.benchmark_framework)

**Field:** max_drawdown_pct
**Message:** Required field 'max_drawdown_pct' has no default value

**Evidence:** Field 'max_drawdown_pct: float' at line 55 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:55

#### WARNING: BuyAndHoldBaseline (mercury_ai.analysis.benchmark_framework)

**Field:** sharpe_ratio
**Message:** Required field 'sharpe_ratio' has no default value

**Evidence:** Field 'sharpe_ratio: float' at line 56 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:56

#### WARNING: BuyAndHoldBaseline (mercury_ai.analysis.benchmark_framework)

**Field:** benchmark_outperformance_pct
**Message:** Required field 'benchmark_outperformance_pct' has no default value

**Evidence:** Field 'benchmark_outperformance_pct: float' at line 57 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:57

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** version
**Message:** Required field 'version' has no default value

**Evidence:** Field 'version: str' at line 63 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:63

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** results
**Message:** Required field 'results' has no default value

**Evidence:** Field 'results: Tuple[BenchmarkRunResult, ...]' at line 64 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:64

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** average_execution_time
**Message:** Required field 'average_execution_time' has no default value

**Evidence:** Field 'average_execution_time: float' at line 65 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:65

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** performance_metrics
**Message:** Required field 'performance_metrics' has no default value

**Evidence:** Field 'performance_metrics: PerformanceMetrics' at line 66 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:66

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** asset_performances
**Message:** Required field 'asset_performances' has no default value

**Evidence:** Field 'asset_performances: Dict[str, AssetPerformance]' at line 68 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:68

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** buy_and_hold_baselines
**Message:** Required field 'buy_and_hold_baselines' has no default value

**Evidence:** Field 'buy_and_hold_baselines: Dict[str, BuyAndHoldBaseline]' at line 70 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:70

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** statistical_tests
**Message:** Required field 'statistical_tests' has no default value

**Evidence:** Field 'statistical_tests: Dict[str, StatisticalTestResult]' at line 71 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:71

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** warm_up_trades_excluded
**Message:** Required field 'warm_up_trades_excluded' has no default value

**Evidence:** Field 'warm_up_trades_excluded: int' at line 72 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:72

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** cool_down_trades_excluded
**Message:** Required field 'cool_down_trades_excluded' has no default value

**Evidence:** Field 'cool_down_trades_excluded: int' at line 73 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:73

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** total_wall_time
**Message:** Required field 'total_wall_time' has no default value

**Evidence:** Field 'total_wall_time: float' at line 74 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:74

#### WARNING: EnhancedBenchmarkReport (mercury_ai.analysis.benchmark_framework)

**Field:** parallel_workers
**Message:** Required field 'parallel_workers' has no default value

**Evidence:** Field 'parallel_workers: int' at line 75 in mercury_ai\analysis\benchmark_framework.py is required but has no default

**Location:** mercury_ai\analysis\benchmark_framework.py:75

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Field:** quality_factor
**Message:** Required field 'quality_factor' has no default value

**Evidence:** Field 'quality_factor: float' at line 11 in mercury_ai\analysis\confidence_engine.py is required but has no default

**Location:** mercury_ai\analysis\confidence_engine.py:11

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Field:** consensus_factor
**Message:** Required field 'consensus_factor' has no default value

**Evidence:** Field 'consensus_factor: float' at line 12 in mercury_ai\analysis\confidence_engine.py is required but has no default

**Location:** mercury_ai\analysis\confidence_engine.py:12

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Field:** market_factor
**Message:** Required field 'market_factor' has no default value

**Evidence:** Field 'market_factor: float' at line 13 in mercury_ai\analysis\confidence_engine.py is required but has no default

**Location:** mercury_ai\analysis\confidence_engine.py:13

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Field:** confirmation_count
**Message:** Required field 'confirmation_count' has no default value

**Evidence:** Field 'confirmation_count: int' at line 14 in mercury_ai\analysis\confidence_engine.py is required but has no default

**Location:** mercury_ai\analysis\confidence_engine.py:14

#### WARNING: ConfidenceComponents (mercury_ai.analysis.confidence_engine)

**Field:** final_score
**Message:** Required field 'final_score' has no default value

**Evidence:** Field 'final_score: float' at line 15 in mercury_ai\analysis\confidence_engine.py is required but has no default

**Location:** mercury_ai\analysis\confidence_engine.py:15

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** decision
**Message:** Required field 'decision' has no default value

**Evidence:** Field 'decision: str' at line 29 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:29

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** reason
**Message:** Required field 'reason' has no default value

**Evidence:** Field 'reason: str' at line 30 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:30

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** dominant_direction
**Message:** Required field 'dominant_direction' has no default value

**Evidence:** Field 'dominant_direction: str' at line 31 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:31

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** opportunity_grade
**Message:** Required field 'opportunity_grade' has no default value

**Evidence:** Field 'opportunity_grade: str' at line 32 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:32

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** conflicting_signals
**Message:** Required field 'conflicting_signals' has no default value

**Evidence:** Field 'conflicting_signals: bool' at line 33 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:33

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** institutional_score
**Message:** Required field 'institutional_score' has no default value

**Evidence:** Field 'institutional_score: float' at line 34 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:34

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 35 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:35

#### WARNING: DecisionExplainability (mercury_ai.analysis.decision_explainability)

**Field:** triggered_rule
**Message:** Required field 'triggered_rule' has no default value

**Evidence:** Field 'triggered_rule: int' at line 36 in mercury_ai\analysis\decision_explainability.py is required but has no default

**Location:** mercury_ai\analysis\decision_explainability.py:36

#### WARNING: DecisionResolverResult (mercury_ai.analysis.decision_resolver_engine)

**Field:** decision
**Message:** Required field 'decision' has no default value

**Evidence:** Field 'decision: str' at line 7 in mercury_ai\analysis\decision_resolver_engine.py is required but has no default

**Location:** mercury_ai\analysis\decision_resolver_engine.py:7

#### WARNING: DecisionResolverResult (mercury_ai.analysis.decision_resolver_engine)

**Field:** triggered_rule
**Message:** Required field 'triggered_rule' has no default value

**Evidence:** Field 'triggered_rule: int' at line 9 in mercury_ai\analysis\decision_resolver_engine.py is required but has no default

**Location:** mercury_ai\analysis\decision_resolver_engine.py:9

#### WARNING: HealthStatus (mercury_ai.analysis.health_checker)

**Field:** system_ready
**Message:** Required field 'system_ready' has no default value

**Evidence:** Field 'system_ready: bool' at line 13 in mercury_ai\analysis\health_checker.py is required but has no default

**Location:** mercury_ai\analysis\health_checker.py:13

#### WARNING: HealthStatus (mercury_ai.analysis.health_checker)

**Field:** components
**Message:** Required field 'components' has no default value

**Evidence:** Field 'components: Dict[str, str]' at line 14 in mercury_ai\analysis\health_checker.py is required but has no default

**Location:** mercury_ai\analysis\health_checker.py:14

#### WARNING: HealthStatus (mercury_ai.analysis.health_checker)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 15 in mercury_ai\analysis\health_checker.py is required but has no default

**Location:** mercury_ai\analysis\health_checker.py:15

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** market_state
**Message:** Required field 'market_state' has no default value

**Evidence:** Field 'market_state: str' at line 6 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:6

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** session
**Message:** Required field 'session' has no default value

**Evidence:** Field 'session: str' at line 8 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:8

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** volatility
**Message:** Required field 'volatility' has no default value

**Evidence:** Field 'volatility: float' at line 10 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:10

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** liquidity
**Message:** Required field 'liquidity' has no default value

**Evidence:** Field 'liquidity: float' at line 12 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:12

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** institutional_bias
**Message:** Required field 'institutional_bias' has no default value

**Evidence:** Field 'institutional_bias: str' at line 14 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:14

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 16 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:16

#### WARNING: InstitutionalContext (mercury_ai.analysis.institutional_context_builder)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: str' at line 18 in mercury_ai\analysis\institutional_context_builder.py is required but has no default

**Location:** mercury_ai\analysis\institutional_context_builder.py:18

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** engine_name
**Message:** Required field 'engine_name' has no default value

**Evidence:** Field 'engine_name: str' at line 21 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:21

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** weight
**Message:** Required field 'weight' has no default value

**Evidence:** Field 'weight: float' at line 22 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:22

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** raw_score
**Message:** Required field 'raw_score' has no default value

**Evidence:** Field 'raw_score: float' at line 23 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:23

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** weighted_score
**Message:** Required field 'weighted_score' has no default value

**Evidence:** Field 'weighted_score: float' at line 24 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:24

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** direction
**Message:** Required field 'direction' has no default value

**Evidence:** Field 'direction: str' at line 25 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:25

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 26 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:26

#### WARNING: InstitutionalContribution (mercury_ai.analysis.institutional_contribution)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: str' at line 27 in mercury_ai\analysis\institutional_contribution.py is required but has no default

**Location:** mercury_ai\analysis\institutional_contribution.py:27

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** institutional_score
**Message:** Required field 'institutional_score' has no default value

**Evidence:** Field 'institutional_score: float' at line 6 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:6

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** probability_score
**Message:** Required field 'probability_score' has no default value

**Evidence:** Field 'probability_score: float' at line 7 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:7

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** confluence_score
**Message:** Required field 'confluence_score' has no default value

**Evidence:** Field 'confluence_score: float' at line 8 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:8

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** confidence_score
**Message:** Required field 'confidence_score' has no default value

**Evidence:** Field 'confidence_score: float' at line 9 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:9

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** trade_quality_score
**Message:** Required field 'trade_quality_score' has no default value

**Evidence:** Field 'trade_quality_score: float' at line 10 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:10

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** resolved_quality_score
**Message:** Required field 'resolved_quality_score' has no default value

**Evidence:** Field 'resolved_quality_score: float' at line 11 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:11

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** risk_score
**Message:** Required field 'risk_score' has no default value

**Evidence:** Field 'risk_score: float' at line 12 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:12

#### WARNING: InstitutionalScoreResult (mercury_ai.analysis.institutional_score_engine)

**Field:** conflict_penalty
**Message:** Required field 'conflict_penalty' has no default value

**Evidence:** Field 'conflict_penalty: float' at line 13 in mercury_ai\analysis\institutional_score_engine.py is required but has no default

**Location:** mercury_ai\analysis\institutional_score_engine.py:13

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** accuracy
**Message:** Required field 'accuracy' has no default value

**Evidence:** Field 'accuracy: float' at line 7 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:7

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** precision_buy
**Message:** Required field 'precision_buy' has no default value

**Evidence:** Field 'precision_buy: float' at line 8 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:8

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** precision_sell
**Message:** Required field 'precision_sell' has no default value

**Evidence:** Field 'precision_sell: float' at line 9 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:9

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** recall
**Message:** Required field 'recall' has no default value

**Evidence:** Field 'recall: float' at line 10 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:10

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** f1_score
**Message:** Required field 'f1_score' has no default value

**Evidence:** Field 'f1_score: float' at line 11 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:11

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** balanced_accuracy
**Message:** Required field 'balanced_accuracy' has no default value

**Evidence:** Field 'balanced_accuracy: float' at line 12 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:12

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** mcc
**Message:** Required field 'mcc' has no default value

**Evidence:** Field 'mcc: float' at line 13 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:13

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** profit_factor
**Message:** Required field 'profit_factor' has no default value

**Evidence:** Field 'profit_factor: float' at line 14 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:14

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** expectancy
**Message:** Required field 'expectancy' has no default value

**Evidence:** Field 'expectancy: float' at line 15 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:15

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** win_rate
**Message:** Required field 'win_rate' has no default value

**Evidence:** Field 'win_rate: float' at line 16 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:16

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** avg_win
**Message:** Required field 'avg_win' has no default value

**Evidence:** Field 'avg_win: float' at line 17 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:17

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** avg_loss
**Message:** Required field 'avg_loss' has no default value

**Evidence:** Field 'avg_loss: float' at line 18 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:18

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** max_drawdown
**Message:** Required field 'max_drawdown' has no default value

**Evidence:** Field 'max_drawdown: float' at line 19 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:19

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** sharpe_simplified
**Message:** Required field 'sharpe_simplified' has no default value

**Evidence:** Field 'sharpe_simplified: float' at line 20 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:20

#### WARNING: PerformanceMetrics (mercury_ai.analysis.metric_calculator)

**Field:** score_distribution
**Message:** Required field 'score_distribution' has no default value

**Evidence:** Field 'score_distribution: Dict[str, float]' at line 21 in mercury_ai\analysis\metric_calculator.py is required but has no default

**Location:** mercury_ai\analysis\metric_calculator.py:21

#### WARNING: Notification (mercury_ai.analysis.notification_center)

**Field:** type
**Message:** Required field 'type' has no default value

**Evidence:** Field 'type: str' at line 9 in mercury_ai\analysis\notification_center.py is required but has no default

**Location:** mercury_ai\analysis\notification_center.py:9

#### WARNING: Notification (mercury_ai.analysis.notification_center)

**Field:** message
**Message:** Required field 'message' has no default value

**Evidence:** Field 'message: str' at line 10 in mercury_ai\analysis\notification_center.py is required but has no default

**Location:** mercury_ai\analysis\notification_center.py:10

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 36 in mercury_ai\analysis\replay_batch_processor.py is required but has no default

**Location:** mercury_ai\analysis\replay_batch_processor.py:36

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** metrics
**Message:** Required field 'metrics' has no default value

**Evidence:** Field 'metrics: Tuple[ReplayMetrics, ...]' at line 37 in mercury_ai\analysis\replay_batch_processor.py is required but has no default

**Location:** mercury_ai\analysis\replay_batch_processor.py:37

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** asset_performance
**Message:** Required field 'asset_performance' has no default value

**Evidence:** Field 'asset_performance: AssetPerformance' at line 38 in mercury_ai\analysis\replay_batch_processor.py is required but has no default

**Location:** mercury_ai\analysis\replay_batch_processor.py:38

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** wall_time
**Message:** Required field 'wall_time' has no default value

**Evidence:** Field 'wall_time: float' at line 39 in mercury_ai\analysis\replay_batch_processor.py is required but has no default

**Location:** mercury_ai\analysis\replay_batch_processor.py:39

#### WARNING: BatchReplayResult (mercury_ai.analysis.replay_batch_processor)

**Field:** cache_stats
**Message:** Required field 'cache_stats' has no default value

**Evidence:** Field 'cache_stats: dict' at line 40 in mercury_ai\analysis\replay_batch_processor.py is required but has no default

**Location:** mercury_ai\analysis\replay_batch_processor.py:40

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Field:** detected
**Message:** Required field 'detected' has no default value

**Evidence:** Field 'detected: bool' at line 8 in mercury_ai\analysis\smart_money\bos_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:8

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Field:** direction
**Message:** Required field 'direction' has no default value

**Evidence:** Field 'direction: str' at line 9 in mercury_ai\analysis\smart_money\bos_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:9

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: int' at line 10 in mercury_ai\analysis\smart_money\bos_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:10

#### WARNING: BOSResult (mercury_ai.analysis.smart_money.bos_engine)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: list[str]' at line 11 in mercury_ai\analysis\smart_money\bos_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\bos_engine.py:11

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Field:** detected
**Message:** Required field 'detected' has no default value

**Evidence:** Field 'detected: bool' at line 9 in mercury_ai\analysis\smart_money\choch_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:9

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Field:** direction
**Message:** Required field 'direction' has no default value

**Evidence:** Field 'direction: str' at line 10 in mercury_ai\analysis\smart_money\choch_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:10

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: int' at line 11 in mercury_ai\analysis\smart_money\choch_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:11

#### WARNING: CHOCHResult (mercury_ai.analysis.smart_money.choch_engine)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: list[str]' at line 12 in mercury_ai\analysis\smart_money\choch_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\choch_engine.py:12

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** touches
**Message:** Required field 'touches' has no default value

**Evidence:** Field 'touches: List[Swing]' at line 16 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:16

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** prices
**Message:** Required field 'prices' has no default value

**Evidence:** Field 'prices: List[float]' at line 17 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:17

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** timestamps
**Message:** Required field 'timestamps' has no default value

**Evidence:** Field 'timestamps: List[str]' at line 18 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:18

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** indices
**Message:** Required field 'indices' has no default value

**Evidence:** Field 'indices: List[int]' at line 19 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:19

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** strengths
**Message:** Required field 'strengths' has no default value

**Evidence:** Field 'strengths: List[float]' at line 20 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:20

#### WARNING: EqualHighGroup (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** ATRs
**Message:** Required field 'ATRs' has no default value

**Evidence:** Field 'ATRs: List[float]' at line 21 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:21

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** touch_count
**Message:** Required field 'touch_count' has no default value

**Evidence:** Field 'touch_count: int' at line 25 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:25

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** average_price
**Message:** Required field 'average_price' has no default value

**Evidence:** Field 'average_price: float' at line 26 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:26

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** minimum_price
**Message:** Required field 'minimum_price' has no default value

**Evidence:** Field 'minimum_price: float' at line 27 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:27

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** maximum_price
**Message:** Required field 'maximum_price' has no default value

**Evidence:** Field 'maximum_price: float' at line 28 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:28

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** price_deviation
**Message:** Required field 'price_deviation' has no default value

**Evidence:** Field 'price_deviation: float' at line 29 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:29

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** average_strength
**Message:** Required field 'average_strength' has no default value

**Evidence:** Field 'average_strength: float' at line 30 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:30

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** minimum_strength
**Message:** Required field 'minimum_strength' has no default value

**Evidence:** Field 'minimum_strength: float' at line 31 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:31

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** maximum_strength
**Message:** Required field 'maximum_strength' has no default value

**Evidence:** Field 'maximum_strength: float' at line 32 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:32

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** average_ATR
**Message:** Required field 'average_ATR' has no default value

**Evidence:** Field 'average_ATR: float' at line 33 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:33

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** ATR_consistency
**Message:** Required field 'ATR_consistency' has no default value

**Evidence:** Field 'ATR_consistency: float' at line 34 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:34

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** first_timestamp
**Message:** Required field 'first_timestamp' has no default value

**Evidence:** Field 'first_timestamp: str' at line 35 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:35

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** last_timestamp
**Message:** Required field 'last_timestamp' has no default value

**Evidence:** Field 'last_timestamp: str' at line 36 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:36

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** first_index
**Message:** Required field 'first_index' has no default value

**Evidence:** Field 'first_index: int' at line 37 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:37

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** last_index
**Message:** Required field 'last_index' has no default value

**Evidence:** Field 'last_index: int' at line 38 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:38

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** age_in_swings
**Message:** Required field 'age_in_swings' has no default value

**Evidence:** Field 'age_in_swings: int' at line 39 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:39

#### WARNING: EqualHighMetrics (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** cluster_width
**Message:** Required field 'cluster_width' has no default value

**Evidence:** Field 'cluster_width: int' at line 40 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:40

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** touch_score
**Message:** Required field 'touch_score' has no default value

**Evidence:** Field 'touch_score: float' at line 44 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:44

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** strength_score
**Message:** Required field 'strength_score' has no default value

**Evidence:** Field 'strength_score: float' at line 45 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:45

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** atr_score
**Message:** Required field 'atr_score' has no default value

**Evidence:** Field 'atr_score: float' at line 46 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:46

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** deviation_score
**Message:** Required field 'deviation_score' has no default value

**Evidence:** Field 'deviation_score: float' at line 47 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:47

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** density_score
**Message:** Required field 'density_score' has no default value

**Evidence:** Field 'density_score: float' at line 48 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:48

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** final_score
**Message:** Required field 'final_score' has no default value

**Evidence:** Field 'final_score: float' at line 49 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:49

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** touch_count
**Message:** Required field 'touch_count' has no default value

**Evidence:** Field 'touch_count: int' at line 50 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:50

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** average_price
**Message:** Required field 'average_price' has no default value

**Evidence:** Field 'average_price: float' at line 51 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:51

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** average_strength
**Message:** Required field 'average_strength' has no default value

**Evidence:** Field 'average_strength: float' at line 52 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:52

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** average_ATR
**Message:** Required field 'average_ATR' has no default value

**Evidence:** Field 'average_ATR: float' at line 53 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:53

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** age_in_swings
**Message:** Required field 'age_in_swings' has no default value

**Evidence:** Field 'age_in_swings: int' at line 54 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:54

#### WARNING: EqualHighScore (mercury_ai.analysis.smart_money.liquidity_engine)

**Field:** cluster_density
**Message:** Required field 'cluster_density' has no default value

**Evidence:** Field 'cluster_density: float' at line 55 in mercury_ai\analysis\smart_money\liquidity_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_engine.py:55

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Field:** event_type
**Message:** Required field 'event_type' has no default value

**Evidence:** Field 'event_type: LiquidityEventType' at line 9 in mercury_ai\analysis\smart_money\liquidity_event_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:9

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Field:** price
**Message:** Required field 'price' has no default value

**Evidence:** Field 'price: float' at line 10 in mercury_ai\analysis\smart_money\liquidity_event_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:10

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Field:** strength
**Message:** Required field 'strength' has no default value

**Evidence:** Field 'strength: float' at line 11 in mercury_ai\analysis\smart_money\liquidity_event_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:11

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 12 in mercury_ai\analysis\smart_money\liquidity_event_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:12

#### WARNING: LiquidityEvent (mercury_ai.analysis.smart_money.liquidity_event_engine)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: str' at line 13 in mercury_ai\analysis\smart_money\liquidity_event_engine.py is required but has no default

**Location:** mercury_ai\analysis\smart_money\liquidity_event_engine.py:13

#### WARNING: UniverseAsset (mercury_ai.config.universe)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 37 in mercury_ai\config\universe.py is required but has no default

**Location:** mercury_ai\config\universe.py:37

#### WARNING: UniverseAsset (mercury_ai.config.universe)

**Field:** display_name
**Message:** Required field 'display_name' has no default value

**Evidence:** Field 'display_name: str' at line 38 in mercury_ai\config\universe.py is required but has no default

**Location:** mercury_ai\config\universe.py:38

#### WARNING: UniverseAsset (mercury_ai.config.universe)

**Field:** market
**Message:** Required field 'market' has no default value

**Evidence:** Field 'market: str' at line 39 in mercury_ai\config\universe.py is required but has no default

**Location:** mercury_ai\config\universe.py:39

#### WARNING: UniverseAsset (mercury_ai.config.universe)

**Field:** provider_symbol
**Message:** Required field 'provider_symbol' has no default value

**Evidence:** Field 'provider_symbol: str' at line 40 in mercury_ai\config\universe.py is required but has no default

**Location:** mercury_ai\config\universe.py:40

#### WARNING: Asset (mercury_ai.core.asset_registry)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 9 in mercury_ai\core\asset_registry.py is required but has no default

**Location:** mercury_ai\core\asset_registry.py:9

#### WARNING: Asset (mercury_ai.core.asset_registry)

**Field:** category
**Message:** Required field 'category' has no default value

**Evidence:** Field 'category: str' at line 10 in mercury_ai\core\asset_registry.py is required but has no default

**Location:** mercury_ai\core\asset_registry.py:10

#### WARNING: Asset (mercury_ai.core.asset_registry)

**Field:** priority
**Message:** Required field 'priority' has no default value

**Evidence:** Field 'priority: int' at line 11 in mercury_ai\core\asset_registry.py is required but has no default

**Location:** mercury_ai\core\asset_registry.py:11

#### WARNING: Asset (mercury_ai.core.asset_registry)

**Field:** profile
**Message:** Required field 'profile' has no default value

**Evidence:** Field 'profile: str' at line 12 in mercury_ai\core\asset_registry.py is required but has no default

**Location:** mercury_ai\core\asset_registry.py:12

#### WARNING: AuditEvent (mercury_ai.core.audit_sink)

**Field:** stage_name
**Message:** Required field 'stage_name' has no default value

**Evidence:** Field 'stage_name: str' at line 7 in mercury_ai\core\audit_sink.py is required but has no default

**Location:** mercury_ai\core\audit_sink.py:7

#### WARNING: AuditEvent (mercury_ai.core.audit_sink)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 8 in mercury_ai\core\audit_sink.py is required but has no default

**Location:** mercury_ai\core\audit_sink.py:8

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 7 in mercury_ai\core\base_engine.py is required but has no default

**Location:** mercury_ai\core\base_engine.py:7

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 8 in mercury_ai\core\base_engine.py is required but has no default

**Location:** mercury_ai\core\base_engine.py:8

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Field:** evidences
**Message:** Required field 'evidences' has no default value

**Evidence:** Field 'evidences: Tuple[str, ...]' at line 9 in mercury_ai\core\base_engine.py is required but has no default

**Location:** mercury_ai\core\base_engine.py:9

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Field:** warnings
**Message:** Required field 'warnings' has no default value

**Evidence:** Field 'warnings: Tuple[str, ...]' at line 10 in mercury_ai\core\base_engine.py is required but has no default

**Location:** mercury_ai\core\base_engine.py:10

#### WARNING: EngineResult (mercury_ai.core.base_engine)

**Field:** execution_time
**Message:** Required field 'execution_time' has no default value

**Evidence:** Field 'execution_time: float' at line 11 in mercury_ai\core\base_engine.py is required but has no default

**Location:** mercury_ai\core\base_engine.py:11

#### WARNING: DataQualityResult (mercury_ai.core.data_quality_gate)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 7 in mercury_ai\core\data_quality_gate.py is required but has no default

**Location:** mercury_ai\core\data_quality_gate.py:7

#### WARNING: DataQualityResult (mercury_ai.core.data_quality_gate)

**Field:** allowed
**Message:** Required field 'allowed' has no default value

**Evidence:** Field 'allowed: bool' at line 8 in mercury_ai\core\data_quality_gate.py is required but has no default

**Location:** mercury_ai\core\data_quality_gate.py:8

#### WARNING: DataQualityResult (mercury_ai.core.data_quality_gate)

**Field:** warnings
**Message:** Required field 'warnings' has no default value

**Evidence:** Field 'warnings: list' at line 9 in mercury_ai\core\data_quality_gate.py is required but has no default

**Location:** mercury_ai\core\data_quality_gate.py:9

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Field:** engine_name
**Message:** Required field 'engine_name' has no default value

**Evidence:** Field 'engine_name: str' at line 6 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:6

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Field:** start_time
**Message:** Required field 'start_time' has no default value

**Evidence:** Field 'start_time: str' at line 7 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:7

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Field:** end_time
**Message:** Required field 'end_time' has no default value

**Evidence:** Field 'end_time: str' at line 8 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:8

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Field:** execution_time
**Message:** Required field 'execution_time' has no default value

**Evidence:** Field 'execution_time: float' at line 9 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:9

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Field:** input_object
**Message:** Required field 'input_object' has no default value

**Evidence:** Field 'input_object: Any' at line 10 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:10

#### WARNING: TelemetryData (mercury_ai.core.runtime_report)

**Field:** output_object
**Message:** Required field 'output_object' has no default value

**Evidence:** Field 'output_object: Any' at line 11 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:11

#### WARNING: RuntimeReport (mercury_ai.core.runtime_report)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 25 in mercury_ai\core\runtime_report.py is required but has no default

**Location:** mercury_ai\core\runtime_report.py:25

#### WARNING: AuditEvent (mercury_ai.core.security_center)

**Field:** user
**Message:** Required field 'user' has no default value

**Evidence:** Field 'user: str' at line 7 in mercury_ai\core\security_center.py is required but has no default

**Location:** mercury_ai\core\security_center.py:7

#### WARNING: AuditEvent (mercury_ai.core.security_center)

**Field:** action
**Message:** Required field 'action' has no default value

**Evidence:** Field 'action: str' at line 8 in mercury_ai\core\security_center.py is required but has no default

**Location:** mercury_ai\core\security_center.py:8

#### WARNING: AuditEvent (mercury_ai.core.security_center)

**Field:** target
**Message:** Required field 'target' has no default value

**Evidence:** Field 'target: str' at line 9 in mercury_ai\core\security_center.py is required but has no default

**Location:** mercury_ai\core\security_center.py:9

#### WARNING: AuditEvent (mercury_ai.core.security_center)

**Field:** severity
**Message:** Required field 'severity' has no default value

**Evidence:** Field 'severity: str' at line 10 in mercury_ai\core\security_center.py is required but has no default

**Location:** mercury_ai\core\security_center.py:10

#### WARNING: ProviderRegistry (mercury_ai.data.mercury_data_provider)

**Field:** name
**Message:** Required field 'name' has no default value

**Evidence:** Field 'name: str' at line 38 in mercury_ai\data\mercury_data_provider.py is required but has no default

**Location:** mercury_ai\data\mercury_data_provider.py:38

#### WARNING: ProviderRegistry (mercury_ai.data.mercury_data_provider)

**Field:** priority
**Message:** Required field 'priority' has no default value

**Evidence:** Field 'priority: ProviderPriority' at line 39 in mercury_ai\data\mercury_data_provider.py is required but has no default

**Location:** mercury_ai\data\mercury_data_provider.py:39

#### WARNING: ProviderRegistry (mercury_ai.data.mercury_data_provider)

**Field:** instance
**Message:** Required field 'instance' has no default value

**Evidence:** Field 'instance: Any' at line 40 in mercury_ai\data\mercury_data_provider.py is required but has no default

**Location:** mercury_ai\data\mercury_data_provider.py:40

#### WARNING: ReplayMetrics (mercury_ai.database.replay_storage)

**Field:** mae
**Message:** Required field 'mae' has no default value

**Evidence:** Field 'mae: float' at line 8 in mercury_ai\database\replay_storage.py is required but has no default

**Location:** mercury_ai\database\replay_storage.py:8

#### WARNING: ReplayMetrics (mercury_ai.database.replay_storage)

**Field:** mfe
**Message:** Required field 'mfe' has no default value

**Evidence:** Field 'mfe: float' at line 9 in mercury_ai\database\replay_storage.py is required but has no default

**Location:** mercury_ai\database\replay_storage.py:9

#### WARNING: ReplayMetrics (mercury_ai.database.replay_storage)

**Field:** pl
**Message:** Required field 'pl' has no default value

**Evidence:** Field 'pl: float' at line 10 in mercury_ai\database\replay_storage.py is required but has no default

**Location:** mercury_ai\database\replay_storage.py:10

#### WARNING: ReplayMetrics (mercury_ai.database.replay_storage)

**Field:** hit
**Message:** Required field 'hit' has no default value

**Evidence:** Field 'hit: bool' at line 11 in mercury_ai\database\replay_storage.py is required but has no default

**Location:** mercury_ai\database\replay_storage.py:11

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** market
**Message:** Required field 'market' has no default value

**Evidence:** Field 'market: MarketData' at line 30 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:30

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** context
**Message:** Required field 'context' has no default value

**Evidence:** Field 'context: MarketContext' at line 31 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:31

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** trend
**Message:** Required field 'trend' has no default value

**Evidence:** Field 'trend: List[Evidence]' at line 32 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:32

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** mtf_evidences
**Message:** Required field 'mtf_evidences' has no default value

**Evidence:** Field 'mtf_evidences: List[Evidence]' at line 33 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:33

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** smart_money
**Message:** Required field 'smart_money' has no default value

**Evidence:** Field 'smart_money: SmartMoneyAnalysis' at line 34 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:34

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** market_regime
**Message:** Required field 'market_regime' has no default value

**Evidence:** Field 'market_regime: MarketRegime' at line 35 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:35

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** confluence
**Message:** Required field 'confluence' has no default value

**Evidence:** Field 'confluence: ConfluenceResult' at line 36 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:36

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** market_condition
**Message:** Required field 'market_condition' has no default value

**Evidence:** Field 'market_condition: MarketCondition' at line 37 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:37

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** market_state
**Message:** Required field 'market_state' has no default value

**Evidence:** Field 'market_state: MarketState' at line 38 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:38

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** candlestick_analysis
**Message:** Required field 'candlestick_analysis' has no default value

**Evidence:** Field 'candlestick_analysis: CandlestickAnalysis' at line 39 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:39

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** volatility_analysis
**Message:** Required field 'volatility_analysis' has no default value

**Evidence:** Field 'volatility_analysis: VolatilityAnalysis' at line 40 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:40

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** session_analysis
**Message:** Required field 'session_analysis' has no default value

**Evidence:** Field 'session_analysis: SessionAnalysis' at line 41 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:41

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** support_resistance
**Message:** Required field 'support_resistance' has no default value

**Evidence:** Field 'support_resistance: SupportResistanceAnalysis' at line 42 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:42

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** liquidity_analysis
**Message:** Required field 'liquidity_analysis' has no default value

**Evidence:** Field 'liquidity_analysis: LiquidityResult' at line 43 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:43

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** risk_assessment
**Message:** Required field 'risk_assessment' has no default value

**Evidence:** Field 'risk_assessment: RiskAssessment' at line 44 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:44

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** evidence_ranking
**Message:** Required field 'evidence_ranking' has no default value

**Evidence:** Field 'evidence_ranking: EvidenceRankingResult' at line 45 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:45

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** volume_analysis
**Message:** Required field 'volume_analysis' has no default value

**Evidence:** Field 'volume_analysis: VolumeAnalysis' at line 46 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:46

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** structure_analysis
**Message:** Required field 'structure_analysis' has no default value

**Evidence:** Field 'structure_analysis: MarketStructureProfile' at line 47 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:47

#### WARNING: AnalysisResult (mercury_ai.models.analysis_result)

**Field:** decision
**Message:** Required field 'decision' has no default value

**Evidence:** Field 'decision: DecisionResult' at line 48 in mercury_ai\models\analysis_result.py is required but has no default

**Location:** mercury_ai\models\analysis_result.py:48

#### WARNING: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 8 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:8

#### WARNING: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 9 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:9

#### WARNING: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Field:** decision_result
**Message:** Required field 'decision_result' has no default value

**Evidence:** Field 'decision_result: DecisionResult' at line 10 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:10

#### WARNING: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Field:** execution_time
**Message:** Required field 'execution_time' has no default value

**Evidence:** Field 'execution_time: float' at line 11 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:11

#### WARNING: BenchmarkRunResult (mercury_ai.models.benchmark_report)

**Field:** memory_usage
**Message:** Required field 'memory_usage' has no default value

**Evidence:** Field 'memory_usage: float' at line 12 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:12

#### WARNING: BenchmarkReport (mercury_ai.models.benchmark_report)

**Field:** version
**Message:** Required field 'version' has no default value

**Evidence:** Field 'version: str' at line 16 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:16

#### WARNING: BenchmarkReport (mercury_ai.models.benchmark_report)

**Field:** results
**Message:** Required field 'results' has no default value

**Evidence:** Field 'results: Tuple[BenchmarkRunResult, ...]' at line 17 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:17

#### WARNING: BenchmarkReport (mercury_ai.models.benchmark_report)

**Field:** average_execution_time
**Message:** Required field 'average_execution_time' has no default value

**Evidence:** Field 'average_execution_time: float' at line 18 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:18

#### WARNING: BenchmarkReport (mercury_ai.models.benchmark_report)

**Field:** performance_metrics
**Message:** Required field 'performance_metrics' has no default value

**Evidence:** Field 'performance_metrics: PerformanceMetrics' at line 19 in mercury_ai\models\benchmark_report.py is required but has no default

**Location:** mercury_ai\models\benchmark_report.py:19

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** confidence_score
**Message:** Required field 'confidence_score' has no default value

**Evidence:** Field 'confidence_score: float' at line 14 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:14

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** final_confidence
**Message:** Required field 'final_confidence' has no default value

**Evidence:** Field 'final_confidence: float' at line 17 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:17

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** confidence_grade
**Message:** Required field 'confidence_grade' has no default value

**Evidence:** Field 'confidence_grade: str' at line 20 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:20

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** is_high
**Message:** Required field 'is_high' has no default value

**Evidence:** Field 'is_high: bool' at line 23 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:23

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** average_quality
**Message:** Required field 'average_quality' has no default value

**Evidence:** Field 'average_quality: float' at line 29 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:29

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** consensus_score
**Message:** Required field 'consensus_score' has no default value

**Evidence:** Field 'consensus_score: float' at line 31 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:31

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** market_score
**Message:** Required field 'market_score' has no default value

**Evidence:** Field 'market_score: float' at line 33 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:33

#### WARNING: ConfidenceResult (mercury_ai.models.confidence_result)

**Field:** confirmation_count
**Message:** Required field 'confirmation_count' has no default value

**Evidence:** Field 'confirmation_count: int' at line 35 in mercury_ai\models\confidence_result.py is required but has no default

**Location:** mercury_ai\models\confidence_result.py:35

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** buy_score
**Message:** Required field 'buy_score' has no default value

**Evidence:** Field 'buy_score: float' at line 7 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:7

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** sell_score
**Message:** Required field 'sell_score' has no default value

**Evidence:** Field 'sell_score: float' at line 8 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:8

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** neutral_score
**Message:** Required field 'neutral_score' has no default value

**Evidence:** Field 'neutral_score: float' at line 9 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:9

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** agreement_percentage
**Message:** Required field 'agreement_percentage' has no default value

**Evidence:** Field 'agreement_percentage: float' at line 10 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:10

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** conflicting_signals
**Message:** Required field 'conflicting_signals' has no default value

**Evidence:** Field 'conflicting_signals: bool' at line 11 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:11

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** independent_confirmations
**Message:** Required field 'independent_confirmations' has no default value

**Evidence:** Field 'independent_confirmations: int' at line 12 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:12

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** weighted_score
**Message:** Required field 'weighted_score' has no default value

**Evidence:** Field 'weighted_score: float' at line 13 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:13

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 14 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:14

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** dominant_direction
**Message:** Required field 'dominant_direction' has no default value

**Evidence:** Field 'dominant_direction: AnalysisDirection' at line 15 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:15

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** evidences
**Message:** Required field 'evidences' has no default value

**Evidence:** Field 'evidences: Tuple[Any, ...]' at line 16 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:16

#### WARNING: ConfluenceResult (mercury_ai.models.confluence_result)

**Field:** warnings
**Message:** Required field 'warnings' has no default value

**Evidence:** Field 'warnings: Tuple[str, ...]' at line 17 in mercury_ai\models\confluence_result.py is required but has no default

**Location:** mercury_ai\models\confluence_result.py:17

#### WARNING: ConfluenceScore (mercury_ai.models.confluence_score)

**Field:** confluence_score
**Message:** Required field 'confluence_score' has no default value

**Evidence:** Field 'confluence_score: float' at line 5 in mercury_ai\models\confluence_score.py is required but has no default

**Location:** mercury_ai\models\confluence_score.py:5

#### WARNING: ConfluenceScore (mercury_ai.models.confluence_score)

**Field:** clarity_score
**Message:** Required field 'clarity_score' has no default value

**Evidence:** Field 'clarity_score: float' at line 6 in mercury_ai\models\confluence_score.py is required but has no default

**Location:** mercury_ai\models\confluence_score.py:6

#### WARNING: ConfluenceScore (mercury_ai.models.confluence_score)

**Field:** bullish_score
**Message:** Required field 'bullish_score' has no default value

**Evidence:** Field 'bullish_score: float' at line 7 in mercury_ai\models\confluence_score.py is required but has no default

**Location:** mercury_ai\models\confluence_score.py:7

#### WARNING: ConfluenceScore (mercury_ai.models.confluence_score)

**Field:** bearish_score
**Message:** Required field 'bearish_score' has no default value

**Evidence:** Field 'bearish_score: float' at line 8 in mercury_ai\models\confluence_score.py is required but has no default

**Location:** mercury_ai\models\confluence_score.py:8

#### WARNING: ConfluenceScore (mercury_ai.models.confluence_score)

**Field:** conflict_penalty
**Message:** Required field 'conflict_penalty' has no default value

**Evidence:** Field 'conflict_penalty: float' at line 9 in mercury_ai\models\confluence_score.py is required but has no default

**Location:** mercury_ai\models\confluence_score.py:9

#### WARNING: DataQualityResult (mercury_ai.models.data_quality_result)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 9 in mercury_ai\models\data_quality_result.py is required but has no default

**Location:** mercury_ai\models\data_quality_result.py:9

#### WARNING: DataQualityResult (mercury_ai.models.data_quality_result)

**Field:** warnings
**Message:** Required field 'warnings' has no default value

**Evidence:** Field 'warnings: Tuple[str, ...]' at line 10 in mercury_ai\models\data_quality_result.py is required but has no default

**Location:** mercury_ai\models\data_quality_result.py:10

#### WARNING: DataQualityResult (mercury_ai.models.data_quality_result)

**Field:** missing_inputs
**Message:** Required field 'missing_inputs' has no default value

**Evidence:** Field 'missing_inputs: Tuple[str, ...]' at line 11 in mercury_ai\models\data_quality_result.py is required but has no default

**Location:** mercury_ai\models\data_quality_result.py:11

#### WARNING: DataQualityResult (mercury_ai.models.data_quality_result)

**Field:** stale_data
**Message:** Required field 'stale_data' has no default value

**Evidence:** Field 'stale_data: bool' at line 12 in mercury_ai\models\data_quality_result.py is required but has no default

**Location:** mercury_ai\models\data_quality_result.py:12

#### WARNING: DataQualityResult (mercury_ai.models.data_quality_result)

**Field:** quality_level
**Message:** Required field 'quality_level' has no default value

**Evidence:** Field 'quality_level: str' at line 13 in mercury_ai\models\data_quality_result.py is required but has no default

**Location:** mercury_ai\models\data_quality_result.py:13

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** market_bias
**Message:** Required field 'market_bias' has no default value

**Evidence:** Field 'market_bias: str' at line 6 in mercury_ai\models\decision_input.py is required but has no default

**Location:** mercury_ai\models\decision_input.py:6

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** confluence_score
**Message:** Required field 'confluence_score' has no default value

**Evidence:** Field 'confluence_score: float' at line 7 in mercury_ai\models\decision_input.py is required but has no default

**Location:** mercury_ai\models\decision_input.py:7

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 8 in mercury_ai\models\decision_input.py is required but has no default

**Location:** mercury_ai\models\decision_input.py:8

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** risk_score
**Message:** Required field 'risk_score' has no default value

**Evidence:** Field 'risk_score: float' at line 9 in mercury_ai\models\decision_input.py is required but has no default

**Location:** mercury_ai\models\decision_input.py:9

#### WARNING: DecisionInput (mercury_ai.models.decision_input)

**Field:** market_state
**Message:** Required field 'market_state' has no default value

**Evidence:** Field 'market_state: str' at line 10 in mercury_ai\models\decision_input.py is required but has no default

**Location:** mercury_ai\models\decision_input.py:10

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Field:** engine
**Message:** Required field 'engine' has no default value

**Evidence:** Field 'engine: str' at line 6 in mercury_ai\models\decision_node.py is required but has no default

**Location:** mercury_ai\models\decision_node.py:6

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Field:** evidence
**Message:** Required field 'evidence' has no default value

**Evidence:** Field 'evidence: str' at line 7 in mercury_ai\models\decision_node.py is required but has no default

**Location:** mercury_ai\models\decision_node.py:7

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Field:** weight
**Message:** Required field 'weight' has no default value

**Evidence:** Field 'weight: float' at line 8 in mercury_ai\models\decision_node.py is required but has no default

**Location:** mercury_ai\models\decision_node.py:8

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 9 in mercury_ai\models\decision_node.py is required but has no default

**Location:** mercury_ai\models\decision_node.py:9

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Field:** influence
**Message:** Required field 'influence' has no default value

**Evidence:** Field 'influence: str' at line 10 in mercury_ai\models\decision_node.py is required but has no default

**Location:** mercury_ai\models\decision_node.py:10

#### WARNING: DecisionNode (mercury_ai.models.decision_node)

**Field:** result
**Message:** Required field 'result' has no default value

**Evidence:** Field 'result: str' at line 11 in mercury_ai\models\decision_node.py is required but has no default

**Location:** mercury_ai\models\decision_node.py:11

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Field:** audit_id
**Message:** Required field 'audit_id' has no default value

**Evidence:** Field 'audit_id: str' at line 6 in mercury_ai\models\decision_outcome.py is required but has no default

**Location:** mercury_ai\models\decision_outcome.py:6

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Field:** outcome
**Message:** Required field 'outcome' has no default value

**Evidence:** Field 'outcome: float' at line 7 in mercury_ai\models\decision_outcome.py is required but has no default

**Location:** mercury_ai\models\decision_outcome.py:7

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 8 in mercury_ai\models\decision_outcome.py is required but has no default

**Location:** mercury_ai\models\decision_outcome.py:8

#### WARNING: DecisionOutcome (mercury_ai.models.decision_outcome)

**Field:** meta
**Message:** Required field 'meta' has no default value

**Evidence:** Field 'meta: Dict[str, Any]' at line 9 in mercury_ai\models\decision_outcome.py is required but has no default

**Location:** mercury_ai\models\decision_outcome.py:9

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** decision
**Message:** Required field 'decision' has no default value

**Evidence:** Field 'decision: str' at line 13 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:13

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** grade
**Message:** Required field 'grade' has no default value

**Evidence:** Field 'grade: str' at line 14 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:14

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 15 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:15

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** clarity
**Message:** Required field 'clarity' has no default value

**Evidence:** Field 'clarity: float' at line 16 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:16

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** risk_score
**Message:** Required field 'risk_score' has no default value

**Evidence:** Field 'risk_score: float' at line 17 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:17

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 18 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:18

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** quality
**Message:** Required field 'quality' has no default value

**Evidence:** Field 'quality: float' at line 19 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:19

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** expected_strength
**Message:** Required field 'expected_strength' has no default value

**Evidence:** Field 'expected_strength: float' at line 20 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:20

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** buy_probability
**Message:** Required field 'buy_probability' has no default value

**Evidence:** Field 'buy_probability: float' at line 21 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:21

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** sell_probability
**Message:** Required field 'sell_probability' has no default value

**Evidence:** Field 'sell_probability: float' at line 22 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:22

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** wait_probability
**Message:** Required field 'wait_probability' has no default value

**Evidence:** Field 'wait_probability: float' at line 23 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:23

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** expected_risk
**Message:** Required field 'expected_risk' has no default value

**Evidence:** Field 'expected_risk: float' at line 24 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:24

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** expected_reward
**Message:** Required field 'expected_reward' has no default value

**Evidence:** Field 'expected_reward: float' at line 25 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:25

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** expected_drawdown
**Message:** Required field 'expected_drawdown' has no default value

**Evidence:** Field 'expected_drawdown: float' at line 26 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:26

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** audit_id
**Message:** Required field 'audit_id' has no default value

**Evidence:** Field 'audit_id: str' at line 27 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:27

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** version_metadata
**Message:** Required field 'version_metadata' has no default value

**Evidence:** Field 'version_metadata: VersionMetadata' at line 28 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:28

#### WARNING: DecisionResult (mercury_ai.models.decision_result)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: TradingExplanation' at line 29 in mercury_ai\models\decision_result.py is required but has no default

**Location:** mercury_ai\models\decision_result.py:29

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 15 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:15

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** asset
**Message:** Required field 'asset' has no default value

**Evidence:** Field 'asset: str' at line 16 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:16

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** timeframe
**Message:** Required field 'timeframe' has no default value

**Evidence:** Field 'timeframe: str' at line 17 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:17

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** context
**Message:** Required field 'context' has no default value

**Evidence:** Field 'context: MarketContext' at line 18 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:18

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** evidence_bundle
**Message:** Required field 'evidence_bundle' has no default value

**Evidence:** Field 'evidence_bundle: MarketEvidenceBundle' at line 19 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:19

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** decision_result
**Message:** Required field 'decision_result' has no default value

**Evidence:** Field 'decision_result: DecisionResult' at line 20 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:20

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** version_metadata
**Message:** Required field 'version_metadata' has no default value

**Evidence:** Field 'version_metadata: VersionMetadata' at line 21 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:21

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** audit_events
**Message:** Required field 'audit_events' has no default value

**Evidence:** Field 'audit_events: Tuple[str, ...]' at line 22 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:22

#### WARNING: DecisionSnapshot (mercury_ai.models.decision_snapshot)

**Field:** session_id
**Message:** Required field 'session_id' has no default value

**Evidence:** Field 'session_id: str' at line 23 in mercury_ai\models\decision_snapshot.py is required but has no default

**Location:** mercury_ai\models\decision_snapshot.py:23

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** asset
**Message:** Required field 'asset' has no default value

**Evidence:** Field 'asset: str' at line 8 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:8

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** total_trades
**Message:** Required field 'total_trades' has no default value

**Evidence:** Field 'total_trades: int' at line 9 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:9

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** pnl_accumulated
**Message:** Required field 'pnl_accumulated' has no default value

**Evidence:** Field 'pnl_accumulated: float' at line 10 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:10

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** win_rate
**Message:** Required field 'win_rate' has no default value

**Evidence:** Field 'win_rate: float' at line 11 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:11

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** profit_factor
**Message:** Required field 'profit_factor' has no default value

**Evidence:** Field 'profit_factor: float' at line 12 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:12

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** expectancy
**Message:** Required field 'expectancy' has no default value

**Evidence:** Field 'expectancy: float' at line 13 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:13

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** avg_win
**Message:** Required field 'avg_win' has no default value

**Evidence:** Field 'avg_win: float' at line 14 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:14

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** avg_loss
**Message:** Required field 'avg_loss' has no default value

**Evidence:** Field 'avg_loss: float' at line 15 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:15

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** max_drawdown
**Message:** Required field 'max_drawdown' has no default value

**Evidence:** Field 'max_drawdown: float' at line 16 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:16

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** recovery_time_candles
**Message:** Required field 'recovery_time_candles' has no default value

**Evidence:** Field 'recovery_time_candles: int' at line 17 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:17

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** sharpe_ratio
**Message:** Required field 'sharpe_ratio' has no default value

**Evidence:** Field 'sharpe_ratio: float' at line 18 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:18

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** sortino_ratio
**Message:** Required field 'sortino_ratio' has no default value

**Evidence:** Field 'sortino_ratio: float' at line 19 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:19

#### WARNING: AssetPerformance (mercury_ai.models.equity_metrics)

**Field:** equity_curve
**Message:** Required field 'equity_curve' has no default value

**Evidence:** Field 'equity_curve: Tuple[float, ...]' at line 20 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:20

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** total_assets
**Message:** Required field 'total_assets' has no default value

**Evidence:** Field 'total_assets: int' at line 25 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:25

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** global_pnl
**Message:** Required field 'global_pnl' has no default value

**Evidence:** Field 'global_pnl: float' at line 26 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:26

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** global_win_rate
**Message:** Required field 'global_win_rate' has no default value

**Evidence:** Field 'global_win_rate: float' at line 27 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:27

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** global_profit_factor
**Message:** Required field 'global_profit_factor' has no default value

**Evidence:** Field 'global_profit_factor: float' at line 28 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:28

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** global_max_drawdown
**Message:** Required field 'global_max_drawdown' has no default value

**Evidence:** Field 'global_max_drawdown: float' at line 29 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:29

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** global_sharpe
**Message:** Required field 'global_sharpe' has no default value

**Evidence:** Field 'global_sharpe: float' at line 30 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:30

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** global_sortino
**Message:** Required field 'global_sortino' has no default value

**Evidence:** Field 'global_sortino: float' at line 31 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:31

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** asset_stats
**Message:** Required field 'asset_stats' has no default value

**Evidence:** Field 'asset_stats: Dict[str, AssetPerformance]' at line 32 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:32

#### WARNING: UniversePerformance (mercury_ai.models.equity_metrics)

**Field:** consolidated_equity_curve
**Message:** Required field 'consolidated_equity_curve' has no default value

**Evidence:** Field 'consolidated_equity_curve: Tuple[float, ...]' at line 33 in mercury_ai\models\equity_metrics.py is required but has no default

**Location:** mercury_ai\models\equity_metrics.py:33

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** engine_name
**Message:** Required field 'engine_name' has no default value

**Evidence:** Field 'engine_name: str' at line 8 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:8

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** evidence_name
**Message:** Required field 'evidence_name' has no default value

**Evidence:** Field 'evidence_name: str' at line 9 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:9

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** direction
**Message:** Required field 'direction' has no default value

**Evidence:** Field 'direction: str' at line 10 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:10

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** strength
**Message:** Required field 'strength' has no default value

**Evidence:** Field 'strength: float' at line 11 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:11

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 12 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:12

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** description
**Message:** Required field 'description' has no default value

**Evidence:** Field 'description: str' at line 13 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:13

#### WARNING: Evidence (mercury_ai.models.evidence)

**Field:** weight
**Message:** Required field 'weight' has no default value

**Evidence:** Field 'weight: float' at line 14 in mercury_ai\models\evidence.py is required but has no default

**Location:** mercury_ai\models\evidence.py:14

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** ranked_evidences
**Message:** Required field 'ranked_evidences' has no default value

**Evidence:** Field 'ranked_evidences: List[Evidence]' at line 7 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:7

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** contribution_percentage
**Message:** Required field 'contribution_percentage' has no default value

**Evidence:** Field 'contribution_percentage: dict' at line 8 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:8

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** strongest_evidence
**Message:** Required field 'strongest_evidence' has no default value

**Evidence:** Field 'strongest_evidence: Evidence' at line 9 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:9

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** weakest_evidence
**Message:** Required field 'weakest_evidence' has no default value

**Evidence:** Field 'weakest_evidence: Evidence' at line 10 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:10

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** total_weight
**Message:** Required field 'total_weight' has no default value

**Evidence:** Field 'total_weight: float' at line 11 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:11

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** bullish_weight
**Message:** Required field 'bullish_weight' has no default value

**Evidence:** Field 'bullish_weight: float' at line 12 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:12

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** bearish_weight
**Message:** Required field 'bearish_weight' has no default value

**Evidence:** Field 'bearish_weight: float' at line 13 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:13

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** neutral_weight
**Message:** Required field 'neutral_weight' has no default value

**Evidence:** Field 'neutral_weight: float' at line 14 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:14

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** bullish_score
**Message:** Required field 'bullish_score' has no default value

**Evidence:** Field 'bullish_score: float' at line 15 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:15

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** bearish_score
**Message:** Required field 'bearish_score' has no default value

**Evidence:** Field 'bearish_score: float' at line 16 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:16

#### WARNING: EvidenceRankingResult (mercury_ai.models.evidence_ranking)

**Field:** neutral_score
**Message:** Required field 'neutral_score' has no default value

**Evidence:** Field 'neutral_score: float' at line 17 in mercury_ai\models\evidence_ranking.py is required but has no default

**Location:** mercury_ai\models\evidence_ranking.py:17

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Field:** evidences
**Message:** Required field 'evidences' has no default value

**Evidence:** Field 'evidences: Tuple[Any, ...]' at line 6 in mercury_ai\models\liquidity_result.py is required but has no default

**Location:** mercury_ai\models\liquidity_result.py:6

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 7 in mercury_ai\models\liquidity_result.py is required but has no default

**Location:** mercury_ai\models\liquidity_result.py:7

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 8 in mercury_ai\models\liquidity_result.py is required but has no default

**Location:** mercury_ai\models\liquidity_result.py:8

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Field:** strength
**Message:** Required field 'strength' has no default value

**Evidence:** Field 'strength: float' at line 9 in mercury_ai\models\liquidity_result.py is required but has no default

**Location:** mercury_ai\models\liquidity_result.py:9

#### WARNING: LiquidityResult (mercury_ai.models.liquidity_result)

**Field:** metadata
**Message:** Required field 'metadata' has no default value

**Evidence:** Field 'metadata: dict' at line 10 in mercury_ai\models\liquidity_result.py is required but has no default

**Location:** mercury_ai\models\liquidity_result.py:10

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** market
**Message:** Required field 'market' has no default value

**Evidence:** Field 'market: MarketData' at line 19 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:19

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** trend
**Message:** Required field 'trend' has no default value

**Evidence:** Field 'trend: List[Evidence]' at line 21 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:21

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** price_action
**Message:** Required field 'price_action' has no default value

**Evidence:** Field 'price_action: PriceActionAnalysis' at line 23 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:23

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** support_resistance
**Message:** Required field 'support_resistance' has no default value

**Evidence:** Field 'support_resistance: SupportResistanceAnalysis' at line 25 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:25

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** smart_money
**Message:** Required field 'smart_money' has no default value

**Evidence:** Field 'smart_money: SmartMoneyAnalysis' at line 27 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:27

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** liquidity
**Message:** Required field 'liquidity' has no default value

**Evidence:** Field 'liquidity: LiquidityProfile' at line 29 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:29

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** market_state
**Message:** Required field 'market_state' has no default value

**Evidence:** Field 'market_state: MarketState' at line 31 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:31

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** market_regime
**Message:** Required field 'market_regime' has no default value

**Evidence:** Field 'market_regime: MarketRegime' at line 33 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:33

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** mtf_consensus
**Message:** Required field 'mtf_consensus' has no default value

**Evidence:** Field 'mtf_consensus: MTFConsensus' at line 35 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:35

#### WARNING: MarketContext (mercury_ai.models.market_context)

**Field:** risk_assessment
**Message:** Required field 'risk_assessment' has no default value

**Evidence:** Field 'risk_assessment: RiskAssessment' at line 37 in mercury_ai\models\market_context.py is required but has no default

**Location:** mercury_ai\models\market_context.py:37

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** symbol
**Message:** Required field 'symbol' has no default value

**Evidence:** Field 'symbol: str' at line 6 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:6

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** timeframe
**Message:** Required field 'timeframe' has no default value

**Evidence:** Field 'timeframe: str' at line 7 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:7

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** close
**Message:** Required field 'close' has no default value

**Evidence:** Field 'close: float' at line 9 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:9

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** ema9
**Message:** Required field 'ema9' has no default value

**Evidence:** Field 'ema9: float' at line 11 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:11

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** ema21
**Message:** Required field 'ema21' has no default value

**Evidence:** Field 'ema21: float' at line 12 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:12

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** ema50
**Message:** Required field 'ema50' has no default value

**Evidence:** Field 'ema50: float' at line 13 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:13

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** rsi
**Message:** Required field 'rsi' has no default value

**Evidence:** Field 'rsi: float' at line 15 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:15

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** atr
**Message:** Required field 'atr' has no default value

**Evidence:** Field 'atr: float' at line 17 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:17

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** adx
**Message:** Required field 'adx' has no default value

**Evidence:** Field 'adx: float' at line 18 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:18

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** macd
**Message:** Required field 'macd' has no default value

**Evidence:** Field 'macd: float' at line 20 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:20

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** macd_signal
**Message:** Required field 'macd_signal' has no default value

**Evidence:** Field 'macd_signal: float' at line 21 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:21

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** bollinger_upper
**Message:** Required field 'bollinger_upper' has no default value

**Evidence:** Field 'bollinger_upper: float' at line 23 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:23

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** bollinger_lower
**Message:** Required field 'bollinger_lower' has no default value

**Evidence:** Field 'bollinger_lower: float' at line 24 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:24

#### WARNING: MarketData (mercury_ai.models.market_data)

**Field:** volume
**Message:** Required field 'volume' has no default value

**Evidence:** Field 'volume: float' at line 26 in mercury_ai\models\market_data.py is required but has no default

**Location:** mercury_ai\models\market_data.py:26

#### WARNING: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Field:** evidences
**Message:** Required field 'evidences' has no default value

**Evidence:** Field 'evidences: Tuple[Evidence, ...]' at line 10 in mercury_ai\models\market_evidence_bundle.py is required but has no default

**Location:** mercury_ai\models\market_evidence_bundle.py:10

#### WARNING: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 11 in mercury_ai\models\market_evidence_bundle.py is required but has no default

**Location:** mercury_ai\models\market_evidence_bundle.py:11

#### WARNING: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Field:** asset
**Message:** Required field 'asset' has no default value

**Evidence:** Field 'asset: str' at line 12 in mercury_ai\models\market_evidence_bundle.py is required but has no default

**Location:** mercury_ai\models\market_evidence_bundle.py:12

#### WARNING: MarketEvidenceBundle (mercury_ai.models.market_evidence_bundle)

**Field:** timeframe
**Message:** Required field 'timeframe' has no default value

**Evidence:** Field 'timeframe: str' at line 13 in mercury_ai\models\market_evidence_bundle.py is required but has no default

**Location:** mercury_ai\models\market_evidence_bundle.py:13

#### WARNING: MarketRegime (mercury_ai.models.market_regime)

**Field:** regime
**Message:** Required field 'regime' has no default value

**Evidence:** Field 'regime: MarketRegimeEnum' at line 8 in mercury_ai\models\market_regime.py is required but has no default

**Location:** mercury_ai\models\market_regime.py:8

#### WARNING: MarketRegime (mercury_ai.models.market_regime)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 9 in mercury_ai\models\market_regime.py is required but has no default

**Location:** mercury_ai\models\market_regime.py:9

#### WARNING: MarketRegime (mercury_ai.models.market_regime)

**Field:** supporting_evidences
**Message:** Required field 'supporting_evidences' has no default value

**Evidence:** Field 'supporting_evidences: List[Evidence]' at line 10 in mercury_ai\models\market_regime.py is required but has no default

**Location:** mercury_ai\models\market_regime.py:10

#### WARNING: MarketState (mercury_ai.models.market_state)

**Field:** state
**Message:** Required field 'state' has no default value

**Evidence:** Field 'state: MarketStateEnum' at line 6 in mercury_ai\models\market_state.py is required but has no default

**Location:** mercury_ai\models\market_state.py:6

#### WARNING: MarketState (mercury_ai.models.market_state)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: str' at line 7 in mercury_ai\models\market_state.py is required but has no default

**Location:** mercury_ai\models\market_state.py:7

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** market_bias
**Message:** Required field 'market_bias' has no default value

**Evidence:** Field 'market_bias: str' at line 9 in mercury_ai\models\market_thesis.py is required but has no default

**Location:** mercury_ai\models\market_thesis.py:9

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** confluence_score
**Message:** Required field 'confluence_score' has no default value

**Evidence:** Field 'confluence_score: float' at line 10 in mercury_ai\models\market_thesis.py is required but has no default

**Location:** mercury_ai\models\market_thesis.py:10

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: ConfidenceResult' at line 11 in mercury_ai\models\market_thesis.py is required but has no default

**Location:** mercury_ai\models\market_thesis.py:11

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** risk
**Message:** Required field 'risk' has no default value

**Evidence:** Field 'risk: RiskAssessment' at line 12 in mercury_ai\models\market_thesis.py is required but has no default

**Location:** mercury_ai\models\market_thesis.py:12

#### WARNING: MarketThesis (mercury_ai.models.market_thesis)

**Field:** market_state
**Message:** Required field 'market_state' has no default value

**Evidence:** Field 'market_state: MarketState' at line 13 in mercury_ai\models\market_thesis.py is required but has no default

**Location:** mercury_ai\models\market_thesis.py:13

#### WARNING: MemorySnapshot (mercury_ai.models.memory_audit)

**Field:** snapshot
**Message:** Required field 'snapshot' has no default value

**Evidence:** Field 'snapshot: tracemalloc.Snapshot' at line 8 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:8

#### WARNING: MemorySnapshot (mercury_ai.models.memory_audit)

**Field:** gc_count
**Message:** Required field 'gc_count' has no default value

**Evidence:** Field 'gc_count: int' at line 9 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:9

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Field:** peak_memory_diff
**Message:** Required field 'peak_memory_diff' has no default value

**Evidence:** Field 'peak_memory_diff: int' at line 14 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:14

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Field:** allocation_diff_size
**Message:** Required field 'allocation_diff_size' has no default value

**Evidence:** Field 'allocation_diff_size: int' at line 15 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:15

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Field:** allocation_diff_count
**Message:** Required field 'allocation_diff_count' has no default value

**Evidence:** Field 'allocation_diff_count: int' at line 16 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:16

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Field:** gc_count_diff
**Message:** Required field 'gc_count_diff' has no default value

**Evidence:** Field 'gc_count_diff: int' at line 17 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:17

#### WARNING: MemoryAuditResult (mercury_ai.models.memory_audit)

**Field:** top_stats
**Message:** Required field 'top_stats' has no default value

**Evidence:** Field 'top_stats: List[str]' at line 18 in mercury_ai\models\memory_audit.py is required but has no default

**Location:** mercury_ai\models\memory_audit.py:18

#### WARNING: MTFConsensus (mercury_ai.models.mtf_consensus)

**Field:** global_bias
**Message:** Required field 'global_bias' has no default value

**Evidence:** Field 'global_bias: str' at line 5 in mercury_ai\models\mtf_consensus.py is required but has no default

**Location:** mercury_ai\models\mtf_consensus.py:5

#### WARNING: MTFConsensus (mercury_ai.models.mtf_consensus)

**Field:** local_bias
**Message:** Required field 'local_bias' has no default value

**Evidence:** Field 'local_bias: str' at line 6 in mercury_ai\models\mtf_consensus.py is required but has no default

**Location:** mercury_ai\models\mtf_consensus.py:6

#### WARNING: MTFConsensus (mercury_ai.models.mtf_consensus)

**Field:** conflict_detected
**Message:** Required field 'conflict_detected' has no default value

**Evidence:** Field 'conflict_detected: bool' at line 7 in mercury_ai\models\mtf_consensus.py is required but has no default

**Location:** mercury_ai\models\mtf_consensus.py:7

#### WARNING: MTFConsensus (mercury_ai.models.mtf_consensus)

**Field:** alignment_score
**Message:** Required field 'alignment_score' has no default value

**Evidence:** Field 'alignment_score: float' at line 8 in mercury_ai\models\mtf_consensus.py is required but has no default

**Location:** mercury_ai\models\mtf_consensus.py:8

#### WARNING: StageMetric (mercury_ai.models.performance)

**Field:** name
**Message:** Required field 'name' has no default value

**Evidence:** Field 'name: str' at line 6 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:6

#### WARNING: StageMetric (mercury_ai.models.performance)

**Field:** duration
**Message:** Required field 'duration' has no default value

**Evidence:** Field 'duration: float' at line 7 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:7

#### WARNING: StageMetric (mercury_ai.models.performance)

**Field:** memory_delta
**Message:** Required field 'memory_delta' has no default value

**Evidence:** Field 'memory_delta: int' at line 8 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:8

#### WARNING: StageMetric (mercury_ai.models.performance)

**Field:** percentage_total
**Message:** Required field 'percentage_total' has no default value

**Evidence:** Field 'percentage_total: float' at line 9 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:9

#### WARNING: StageMetric (mercury_ai.models.performance)

**Field:** nested_metrics
**Message:** Required field 'nested_metrics' has no default value

**Evidence:** Field 'nested_metrics: Tuple['StageMetric', ...]' at line 10 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:10

#### WARNING: PipelineMetric (mercury_ai.models.performance)

**Field:** pipeline_name
**Message:** Required field 'pipeline_name' has no default value

**Evidence:** Field 'pipeline_name: str' at line 14 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:14

#### WARNING: PipelineMetric (mercury_ai.models.performance)

**Field:** total_duration
**Message:** Required field 'total_duration' has no default value

**Evidence:** Field 'total_duration: float' at line 15 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:15

#### WARNING: PipelineMetric (mercury_ai.models.performance)

**Field:** stage_metrics
**Message:** Required field 'stage_metrics' has no default value

**Evidence:** Field 'stage_metrics: Tuple[StageMetric, ...]' at line 16 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:16

#### WARNING: HotspotReport (mercury_ai.models.performance)

**Field:** pipeline_name
**Message:** Required field 'pipeline_name' has no default value

**Evidence:** Field 'pipeline_name: str' at line 20 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:20

#### WARNING: HotspotReport (mercury_ai.models.performance)

**Field:** total_duration
**Message:** Required field 'total_duration' has no default value

**Evidence:** Field 'total_duration: float' at line 21 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:21

#### WARNING: HotspotReport (mercury_ai.models.performance)

**Field:** hotspots
**Message:** Required field 'hotspots' has no default value

**Evidence:** Field 'hotspots: Tuple[str, ...]' at line 22 in mercury_ai\models\performance.py is required but has no default

**Location:** mercury_ai\models\performance.py:22

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** total_trades
**Message:** Required field 'total_trades' has no default value

**Evidence:** Field 'total_trades: int' at line 6 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:6

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** correct
**Message:** Required field 'correct' has no default value

**Evidence:** Field 'correct: int' at line 7 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:7

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** incorrect
**Message:** Required field 'incorrect' has no default value

**Evidence:** Field 'incorrect: int' at line 8 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:8

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** late_entries
**Message:** Required field 'late_entries' has no default value

**Evidence:** Field 'late_entries: int' at line 9 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:9

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** early_entries
**Message:** Required field 'early_entries' has no default value

**Evidence:** Field 'early_entries: int' at line 10 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:10

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** missed_trades
**Message:** Required field 'missed_trades' has no default value

**Evidence:** Field 'missed_trades: int' at line 11 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:11

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** false_positives
**Message:** Required field 'false_positives' has no default value

**Evidence:** Field 'false_positives: int' at line 12 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:12

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** false_negatives
**Message:** Required field 'false_negatives' has no default value

**Evidence:** Field 'false_negatives: int' at line 13 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:13

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** engine_responsibility
**Message:** Required field 'engine_responsibility' has no default value

**Evidence:** Field 'engine_responsibility: Dict[str, int]' at line 14 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:14

#### WARNING: PerformanceMetrics (mercury_ai.models.performance_metrics)

**Field:** evidence_responsibility
**Message:** Required field 'evidence_responsibility' has no default value

**Evidence:** Field 'evidence_responsibility: Dict[str, int]' at line 15 in mercury_ai\models\performance_metrics.py is required but has no default

**Location:** mercury_ai\models\performance_metrics.py:15

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action)

**Field:** trend_structure
**Message:** Required field 'trend_structure' has no default value

**Evidence:** Field 'trend_structure: str' at line 7 in mercury_ai\models\price_action.py is required but has no default

**Location:** mercury_ai\models\price_action.py:7

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action)

**Field:** last_event
**Message:** Required field 'last_event' has no default value

**Evidence:** Field 'last_event: str' at line 8 in mercury_ai\models\price_action.py is required but has no default

**Location:** mercury_ai\models\price_action.py:8

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: int' at line 9 in mercury_ai\models\price_action.py is required but has no default

**Location:** mercury_ai\models\price_action.py:9

#### WARNING: PriceActionAnalysis (mercury_ai.models.price_action)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: list[str]' at line 10 in mercury_ai\models\price_action.py is required but has no default

**Location:** mercury_ai\models\price_action.py:10

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** buy_probability
**Message:** Required field 'buy_probability' has no default value

**Evidence:** Field 'buy_probability: float' at line 6 in mercury_ai\models\probability_result.py is required but has no default

**Location:** mercury_ai\models\probability_result.py:6

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** sell_probability
**Message:** Required field 'sell_probability' has no default value

**Evidence:** Field 'sell_probability: float' at line 7 in mercury_ai\models\probability_result.py is required but has no default

**Location:** mercury_ai\models\probability_result.py:7

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** neutral_probability
**Message:** Required field 'neutral_probability' has no default value

**Evidence:** Field 'neutral_probability: float' at line 8 in mercury_ai\models\probability_result.py is required but has no default

**Location:** mercury_ai\models\probability_result.py:8

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** expected_risk
**Message:** Required field 'expected_risk' has no default value

**Evidence:** Field 'expected_risk: float' at line 9 in mercury_ai\models\probability_result.py is required but has no default

**Location:** mercury_ai\models\probability_result.py:9

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** opportunity_grade
**Message:** Required field 'opportunity_grade' has no default value

**Evidence:** Field 'opportunity_grade: str' at line 10 in mercury_ai\models\probability_result.py is required but has no default

**Location:** mercury_ai\models\probability_result.py:10

#### WARNING: ProbabilityResult (mercury_ai.models.probability_result)

**Field:** institutional_confidence
**Message:** Required field 'institutional_confidence' has no default value

**Evidence:** Field 'institutional_confidence: float' at line 11 in mercury_ai\models\probability_result.py is required but has no default

**Location:** mercury_ai\models\probability_result.py:11

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** market_bias
**Message:** Required field 'market_bias' has no default value

**Evidence:** Field 'market_bias: str' at line 6 in mercury_ai\models\professional_thesis.py is required but has no default

**Location:** mercury_ai\models\professional_thesis.py:6

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** opportunity_grade
**Message:** Required field 'opportunity_grade' has no default value

**Evidence:** Field 'opportunity_grade: str' at line 7 in mercury_ai\models\professional_thesis.py is required but has no default

**Location:** mercury_ai\models\professional_thesis.py:7

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: int' at line 8 in mercury_ai\models\professional_thesis.py is required but has no default

**Location:** mercury_ai\models\professional_thesis.py:8

#### WARNING: ProfessionalThesis (mercury_ai.models.professional_thesis)

**Field:** institutional_alignment
**Message:** Required field 'institutional_alignment' has no default value

**Evidence:** Field 'institutional_alignment: bool' at line 9 in mercury_ai\models\professional_thesis.py is required but has no default

**Location:** mercury_ai\models\professional_thesis.py:9

#### WARNING: StageProfile (mercury_ai.models.profiler_models)

**Field:** name
**Message:** Required field 'name' has no default value

**Evidence:** Field 'name: str' at line 6 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:6

#### WARNING: StageProfile (mercury_ai.models.profiler_models)

**Field:** duration
**Message:** Required field 'duration' has no default value

**Evidence:** Field 'duration: float' at line 7 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:7

#### WARNING: StageProfile (mercury_ai.models.profiler_models)

**Field:** memory_peak
**Message:** Required field 'memory_peak' has no default value

**Evidence:** Field 'memory_peak: int' at line 8 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:8

#### WARNING: StageProfile (mercury_ai.models.profiler_models)

**Field:** memory_delta
**Message:** Required field 'memory_delta' has no default value

**Evidence:** Field 'memory_delta: int' at line 9 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:9

#### WARNING: StageProfile (mercury_ai.models.profiler_models)

**Field:** percentage_total
**Message:** Required field 'percentage_total' has no default value

**Evidence:** Field 'percentage_total: float' at line 10 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:10

#### WARNING: PipelineProfile (mercury_ai.models.profiler_models)

**Field:** pipeline_name
**Message:** Required field 'pipeline_name' has no default value

**Evidence:** Field 'pipeline_name: str' at line 15 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:15

#### WARNING: PipelineProfile (mercury_ai.models.profiler_models)

**Field:** total_duration
**Message:** Required field 'total_duration' has no default value

**Evidence:** Field 'total_duration: float' at line 16 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:16

#### WARNING: PipelineProfile (mercury_ai.models.profiler_models)

**Field:** stage_profiles
**Message:** Required field 'stage_profiles' has no default value

**Evidence:** Field 'stage_profiles: Tuple[StageProfile, ...]' at line 17 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:17

#### WARNING: HotspotSummary (mercury_ai.models.profiler_models)

**Field:** pipeline_name
**Message:** Required field 'pipeline_name' has no default value

**Evidence:** Field 'pipeline_name: str' at line 21 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:21

#### WARNING: HotspotSummary (mercury_ai.models.profiler_models)

**Field:** hotspots
**Message:** Required field 'hotspots' has no default value

**Evidence:** Field 'hotspots: Tuple[str, ...]' at line 22 in mercury_ai\models\profiler_models.py is required but has no default

**Location:** mercury_ai\models\profiler_models.py:22

#### WARNING: BenchmarkMetrics (mercury_ai.models.regression)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: float' at line 6 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:6

#### WARNING: BenchmarkMetrics (mercury_ai.models.regression)

**Field:** duration
**Message:** Required field 'duration' has no default value

**Evidence:** Field 'duration: float' at line 7 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:7

#### WARNING: BenchmarkMetrics (mercury_ai.models.regression)

**Field:** peak_memory
**Message:** Required field 'peak_memory' has no default value

**Evidence:** Field 'peak_memory: int' at line 8 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:8

#### WARNING: BenchmarkMetrics (mercury_ai.models.regression)

**Field:** allocation_count
**Message:** Required field 'allocation_count' has no default value

**Evidence:** Field 'allocation_count: int' at line 9 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:9

#### WARNING: BenchmarkMetrics (mercury_ai.models.regression)

**Field:** gc_count
**Message:** Required field 'gc_count' has no default value

**Evidence:** Field 'gc_count: int' at line 10 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:10

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Field:** is_regression
**Message:** Required field 'is_regression' has no default value

**Evidence:** Field 'is_regression: bool' at line 14 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:14

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Field:** performance_delta
**Message:** Required field 'performance_delta' has no default value

**Evidence:** Field 'performance_delta: float' at line 15 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:15

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Field:** memory_delta
**Message:** Required field 'memory_delta' has no default value

**Evidence:** Field 'memory_delta: float' at line 16 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:16

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Field:** allocation_delta
**Message:** Required field 'allocation_delta' has no default value

**Evidence:** Field 'allocation_delta: float' at line 17 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:17

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Field:** gc_delta
**Message:** Required field 'gc_delta' has no default value

**Evidence:** Field 'gc_delta: float' at line 18 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:18

#### WARNING: RegressionResult (mercury_ai.models.regression)

**Field:** message
**Message:** Required field 'message' has no default value

**Evidence:** Field 'message: str' at line 19 in mercury_ai\models\regression.py is required but has no default

**Location:** mercury_ai\models\regression.py:19

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** suggested_stop
**Message:** Required field 'suggested_stop' has no default value

**Evidence:** Field 'suggested_stop: float' at line 8 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:8

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** suggested_take_profit
**Message:** Required field 'suggested_take_profit' has no default value

**Evidence:** Field 'suggested_take_profit: float' at line 9 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:9

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** risk_reward_ratio
**Message:** Required field 'risk_reward_ratio' has no default value

**Evidence:** Field 'risk_reward_ratio: float' at line 10 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:10

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** expected_drawdown
**Message:** Required field 'expected_drawdown' has no default value

**Evidence:** Field 'expected_drawdown: float' at line 11 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:11

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** expected_volatility
**Message:** Required field 'expected_volatility' has no default value

**Evidence:** Field 'expected_volatility: float' at line 12 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:12

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** trade_quality
**Message:** Required field 'trade_quality' has no default value

**Evidence:** Field 'trade_quality: float' at line 13 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:13

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** max_exposure
**Message:** Required field 'max_exposure' has no default value

**Evidence:** Field 'max_exposure: float' at line 14 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:14

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** invalidation_point
**Message:** Required field 'invalidation_point' has no default value

**Evidence:** Field 'invalidation_point: float' at line 15 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:15

#### WARNING: RiskAssessment (mercury_ai.models.risk_assessment)

**Field:** institutional_risk_score
**Message:** Required field 'institutional_risk_score' has no default value

**Evidence:** Field 'institutional_risk_score: float' at line 16 in mercury_ai\models\risk_assessment.py is required but has no default

**Location:** mercury_ai\models\risk_assessment.py:16

#### WARNING: Signal (mercury_ai.models.signal)

**Field:** asset
**Message:** Required field 'asset' has no default value

**Evidence:** Field 'asset: str' at line 12 in mercury_ai\models\signal.py is required but has no default

**Location:** mercury_ai\models\signal.py:12

#### WARNING: Signal (mercury_ai.models.signal)

**Field:** action
**Message:** Required field 'action' has no default value

**Evidence:** Field 'action: str' at line 14 in mercury_ai\models\signal.py is required but has no default

**Location:** mercury_ai\models\signal.py:14

#### WARNING: Signal (mercury_ai.models.signal)

**Field:** confidence
**Message:** Required field 'confidence' has no default value

**Evidence:** Field 'confidence: float' at line 16 in mercury_ai\models\signal.py is required but has no default

**Location:** mercury_ai\models\signal.py:16

#### WARNING: Signal (mercury_ai.models.signal)

**Field:** score
**Message:** Required field 'score' has no default value

**Evidence:** Field 'score: float' at line 18 in mercury_ai\models\signal.py is required but has no default

**Location:** mercury_ai\models\signal.py:18

#### WARNING: SmartMoneyAnalysis (mercury_ai.models.smart_money)

**Field:** structure
**Message:** Required field 'structure' has no default value

**Evidence:** Field 'structure: MarketStructure' at line 9 in mercury_ai\models\smart_money.py is required but has no default

**Location:** mercury_ai\models\smart_money.py:9

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** pipeline_name
**Message:** Required field 'pipeline_name' has no default value

**Evidence:** Field 'pipeline_name: str' at line 7 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:7

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** scenario
**Message:** Required field 'scenario' has no default value

**Evidence:** Field 'scenario: str' at line 8 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:8

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** dataset_size
**Message:** Required field 'dataset_size' has no default value

**Evidence:** Field 'dataset_size: int' at line 9 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:9

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** repetitions
**Message:** Required field 'repetitions' has no default value

**Evidence:** Field 'repetitions: int' at line 10 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:10

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** runtimes
**Message:** Required field 'runtimes' has no default value

**Evidence:** Field 'runtimes: List[float]' at line 11 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:11

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** peak_memory
**Message:** Required field 'peak_memory' has no default value

**Evidence:** Field 'peak_memory: List[int]' at line 12 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:12

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** exceptions
**Message:** Required field 'exceptions' has no default value

**Evidence:** Field 'exceptions: List[Exception]' at line 13 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:13

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** is_deterministic
**Message:** Required field 'is_deterministic' has no default value

**Evidence:** Field 'is_deterministic: bool' at line 14 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:14

#### WARNING: StressTestResult (mercury_ai.models.stress_test)

**Field:** failure_count
**Message:** Required field 'failure_count' has no default value

**Evidence:** Field 'failure_count: int' at line 15 in mercury_ai\models\stress_test.py is required but has no default

**Location:** mercury_ai\models\stress_test.py:15

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Field:** support
**Message:** Required field 'support' has no default value

**Evidence:** Field 'support: float' at line 7 in mercury_ai\models\support_resistance.py is required but has no default

**Location:** mercury_ai\models\support_resistance.py:7

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Field:** resistance
**Message:** Required field 'resistance' has no default value

**Evidence:** Field 'resistance: float' at line 8 in mercury_ai\models\support_resistance.py is required but has no default

**Location:** mercury_ai\models\support_resistance.py:8

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Field:** distance_support
**Message:** Required field 'distance_support' has no default value

**Evidence:** Field 'distance_support: float' at line 9 in mercury_ai\models\support_resistance.py is required but has no default

**Location:** mercury_ai\models\support_resistance.py:9

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Field:** distance_resistance
**Message:** Required field 'distance_resistance' has no default value

**Evidence:** Field 'distance_resistance: float' at line 10 in mercury_ai\models\support_resistance.py is required but has no default

**Location:** mercury_ai\models\support_resistance.py:10

#### WARNING: SupportResistanceAnalysis (mercury_ai.models.support_resistance)

**Field:** explanation
**Message:** Required field 'explanation' has no default value

**Evidence:** Field 'explanation: list[str]' at line 11 in mercury_ai\models\support_resistance.py is required but has no default

**Location:** mercury_ai\models\support_resistance.py:11

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** type
**Message:** Required field 'type' has no default value

**Evidence:** Field 'type: str' at line 6 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:6

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** classification
**Message:** Required field 'classification' has no default value

**Evidence:** Field 'classification: str' at line 7 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:7

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** price
**Message:** Required field 'price' has no default value

**Evidence:** Field 'price: float' at line 8 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:8

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 9 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:9

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** index
**Message:** Required field 'index' has no default value

**Evidence:** Field 'index: int' at line 10 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:10

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** atr
**Message:** Required field 'atr' has no default value

**Evidence:** Field 'atr: float' at line 11 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:11

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** strength
**Message:** Required field 'strength' has no default value

**Evidence:** Field 'strength: float' at line 12 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:12

#### WARNING: Swing (mercury_ai.models.swing_analysis)

**Field:** volume
**Message:** Required field 'volume' has no default value

**Evidence:** Field 'volume: float' at line 13 in mercury_ai\models\swing_analysis.py is required but has no default

**Location:** mercury_ai\models\swing_analysis.py:13

#### WARNING: TradeFilterResult (mercury_ai.models.trade_filter_result)

**Field:** allowed
**Message:** Required field 'allowed' has no default value

**Evidence:** Field 'allowed: bool' at line 15 in mercury_ai\models\trade_filter_result.py is required but has no default

**Location:** mercury_ai\models\trade_filter_result.py:15

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** timestamp
**Message:** Required field 'timestamp' has no default value

**Evidence:** Field 'timestamp: str' at line 7 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:7

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** context_snapshot
**Message:** Required field 'context_snapshot' has no default value

**Evidence:** Field 'context_snapshot: Dict[str, Any]' at line 8 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:8

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** evidences
**Message:** Required field 'evidences' has no default value

**Evidence:** Field 'evidences: List[str]' at line 9 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:9

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** decision
**Message:** Required field 'decision' has no default value

**Evidence:** Field 'decision: str' at line 10 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:10

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** result
**Message:** Required field 'result' has no default value

**Evidence:** Field 'result: str' at line 11 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:11

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** mae
**Message:** Required field 'mae' has no default value

**Evidence:** Field 'mae: float' at line 12 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:12

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** mfe
**Message:** Required field 'mfe' has no default value

**Evidence:** Field 'mfe: float' at line 13 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:13

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** drawdown
**Message:** Required field 'drawdown' has no default value

**Evidence:** Field 'drawdown: float' at line 14 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:14

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** profit
**Message:** Required field 'profit' has no default value

**Evidence:** Field 'profit: float' at line 15 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:15

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** time_to_close
**Message:** Required field 'time_to_close' has no default value

**Evidence:** Field 'time_to_close: float' at line 16 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:16

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** session
**Message:** Required field 'session' has no default value

**Evidence:** Field 'session: str' at line 17 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:17

#### WARNING: TradeMemory (mercury_ai.models.trade_memory)

**Field:** regime
**Message:** Required field 'regime' has no default value

**Evidence:** Field 'regime: str' at line 18 in mercury_ai\models\trade_memory.py is required but has no default

**Location:** mercury_ai\models\trade_memory.py:18

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** exec_summary
**Message:** Required field 'exec_summary' has no default value

**Evidence:** Field 'exec_summary: str' at line 9 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:9

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** decision_rationale
**Message:** Required field 'decision_rationale' has no default value

**Evidence:** Field 'decision_rationale: str' at line 10 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:10

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** market_context
**Message:** Required field 'market_context' has no default value

**Evidence:** Field 'market_context: str' at line 11 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:11

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** trend_context
**Message:** Required field 'trend_context' has no default value

**Evidence:** Field 'trend_context: str' at line 12 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:12

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** liquidity_context
**Message:** Required field 'liquidity_context' has no default value

**Evidence:** Field 'liquidity_context: str' at line 13 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:13

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** structure_context
**Message:** Required field 'structure_context' has no default value

**Evidence:** Field 'structure_context: str' at line 14 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:14

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** momentum_context
**Message:** Required field 'momentum_context' has no default value

**Evidence:** Field 'momentum_context: str' at line 15 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:15

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** volume_context
**Message:** Required field 'volume_context' has no default value

**Evidence:** Field 'volume_context: str' at line 16 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:16

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** smart_money_context
**Message:** Required field 'smart_money_context' has no default value

**Evidence:** Field 'smart_money_context: str' at line 17 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:17

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** confluence_context
**Message:** Required field 'confluence_context' has no default value

**Evidence:** Field 'confluence_context: str' at line 18 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:18

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** risk_assessment
**Message:** Required field 'risk_assessment' has no default value

**Evidence:** Field 'risk_assessment: str' at line 19 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:19

#### WARNING: TradingExplanation (mercury_ai.models.trading_explanation)

**Field:** confidence_rationale
**Message:** Required field 'confidence_rationale' has no default value

**Evidence:** Field 'confidence_rationale: str' at line 20 in mercury_ai\models\trading_explanation.py is required but has no default

**Location:** mercury_ai\models\trading_explanation.py:20

#### WARNING: VersionMetadata (mercury_ai.models.version_metadata)

**Field:** engine_version
**Message:** Required field 'engine_version' has no default value

**Evidence:** Field 'engine_version: str' at line 5 in mercury_ai\models\version_metadata.py is required but has no default

**Location:** mercury_ai\models\version_metadata.py:5

#### WARNING: VersionMetadata (mercury_ai.models.version_metadata)

**Field:** pipeline_version
**Message:** Required field 'pipeline_version' has no default value

**Evidence:** Field 'pipeline_version: str' at line 6 in mercury_ai\models\version_metadata.py is required but has no default

**Location:** mercury_ai\models\version_metadata.py:6

#### WARNING: VersionMetadata (mercury_ai.models.version_metadata)

**Field:** context_version
**Message:** Required field 'context_version' has no default value

**Evidence:** Field 'context_version: str' at line 7 in mercury_ai\models\version_metadata.py is required but has no default

**Location:** mercury_ai\models\version_metadata.py:7

#### WARNING: VersionMetadata (mercury_ai.models.version_metadata)

**Field:** weights_version
**Message:** Required field 'weights_version' has no default value

**Evidence:** Field 'weights_version: str' at line 8 in mercury_ai\models\version_metadata.py is required but has no default

**Location:** mercury_ai\models\version_metadata.py:8
