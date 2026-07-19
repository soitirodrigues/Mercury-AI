from typing import List, Optional, Dict
import uuid
from dataclasses import replace

from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.data.data_quality_engine import DataQualityEngine
from mercury_ai.providers.base_provider import MarketDataProvider
from mercury_ai.data.indicator_engine import IndicatorEngine
from mercury_ai.core.exceptions import MarketClosedException

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.analysis_result import AnalysisResult
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.version_metadata import VersionMetadata

from mercury_ai.analysis.context_engine import ContextEngine
from mercury_ai.brain.mercury_decision_engine import MercuryDecisionEngine
from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

from mercury_ai.analysis.market_context_builder import MarketContextBuilder
from mercury_ai.analysis.confluence_engine import ConfluenceEngine
from mercury_ai.analysis.smart_money.smart_money_engine import SmartMoneyEngine
from mercury_ai.analysis.trend_analyzer import TrendAnalyzer
from mercury_ai.analysis.market_condition_engine import MarketConditionEngine
from mercury_ai.analysis.market_regime_engine import MarketRegimeEngine
from mercury_ai.analysis.mtf_engine import MTFEngine
from mercury_ai.analysis.candlestick_engine import CandlestickEngine
from mercury_ai.analysis.volatility_engine import VolatilityEngine
from mercury_ai.analysis.session_engine import SessionEngine
from mercury_ai.analysis.support_resistance_analyzer import SupportResistanceAnalyzer
from mercury_ai.analysis.smart_money.liquidity_engine import LiquidityEngine
from mercury_ai.analysis.risk_engine import RiskEngine
from mercury_ai.analysis.market_state_engine import MarketStateEngine
from mercury_ai.analysis.evidence_ranking_engine import EvidenceRankingEngine
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine
from mercury_ai.analysis.evidence_engine import EvidenceEngine
from mercury_ai.analysis.context_intelligence_engine import ContextIntelligenceEngine
from mercury_ai.analysis.volume_intelligence_engine import VolumeIntelligenceEngine
from mercury_ai.analysis.market_structure_intelligence_engine import MarketStructureIntelligenceEngine
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME
from mercury_ai.analysis.institutional_trade_filter_engine import InstitutionalTradeFilterEngine
from mercury_ai.analysis.price_action_analyzer import PriceActionAnalyzer
from mercury_ai.analysis.fair_value_gap_engine import FairValueGapEngine
from mercury_ai.analysis.smart_money.order_block_engine import OrderBlockEngine
from mercury_ai.core.runtime_report import RuntimeReport, TelemetryData
...
class AnalysisPipeline:

    def __init__(self, market_service: MarketDataService, providers: List[MarketDataProvider]):

        self.market_service = market_service
        self.indicators = IndicatorEngine()
        self.quality_engine = DataQualityEngine()
        self.executor = PipelineExecutor()
        self.profiler = PipelineProfiler("AnalysisPipeline")

        self.runtime_report: Optional[RuntimeReport] = None

        self.context_engine = ContextEngine(self.executor, self.profiler)
        self.evidence_engine = EvidenceEngine()
        self.decision_engine = MercuryDecisionEngine(self.executor, self.profiler)
        self.snapshot_logger = DecisionSnapshotLogger()
        self.last_snapshot: Optional[DecisionSnapshot] = None
        self.last_snapshots: Dict[str, DecisionSnapshot] = {}
        self.session_id = str(uuid.uuid4())

        # Base Engines
        self.trend = TrendAnalyzer()
        self.mtf_engine = MTFEngine(providers=providers)
        self.sr_engine = SupportResistanceAnalyzer()
        self.price_action = PriceActionAnalyzer()
        self.liquidity_engine = LiquidityEngine()
        self.smart_money = SmartMoneyEngine()
        self.fvg = FairValueGapEngine(executor=self.executor)
        self.ob = OrderBlockEngine()
        self.regime_engine = MarketRegimeEngine()
        self.session_engine = SessionEngine()
        self.state_engine = MarketStateEngine()
        self.volume_engine = VolumeIntelligenceEngine()
        self.volatility_engine = VolatilityEngine()
        self.market_condition_engine = MarketConditionEngine()
        self.candlestick_engine = CandlestickEngine()
        self.structure_intel_engine = MarketStructureIntelligenceEngine()
        
        # Coordination & Filtering
        self.confluence = ConfluenceEngine()
        self.risk_engine = RiskEngine()
        self.trade_filter = InstitutionalTradeFilterEngine()
        self.ranking_engine = EvidenceRankingEngine()
        self.evidence_quality_engine = EvidenceQualityEngine()
        self.context_intel_engine = ContextIntelligenceEngine()
        self.memory = InstitutionalMemoryEngine()

        self.context_builder = MarketContextBuilder(
            trend=self.trend,
            sr=self.sr_engine,
            price_action=self.price_action,
            liquidity=self.liquidity_engine,
            smart_money=self.smart_money,
            fvg=self.fvg,
            ob=self.ob,
            regime=self.regime_engine
        )

    def _record_telemetry(self, stage_name, start_time, input_obj, output_obj, **metrics):
        if self.runtime_report is None:
            self.runtime_report = RuntimeReport(symbol="UNKNOWN")
            
        execution_time = (DeterministicClock.utcnow() - start_time).total_seconds()
        
        # Inference map for roles
        roles = {
            "DataLoading": {"creator": "MarketDataService"},
            "DataQuality": {"consumer": "DataQualityEngine"},
            "Indicators": {"creator": "IndicatorEngine"},
            "TrendAnalysis": {"creator": "TrendAnalyzer"},
            "MTFAnalysis": {"creator": "MTFEngine"},
            "StructureAnalysis": {"creator": "MarketStructureEngine"},
            "SmartMoneyAnalysis": {"creator": "SmartMoneyEngine"},
            "SessionAnalysis": {"creator": "SessionEngine"},
            "MarketStateAnalysis": {"creator": "MarketStateEngine"},
            "RegimeAnalysis": {"creator": "RegimeEngine"},
            "LiquidityAnalysis": {"creator": "LiquidityEngine"},
            "VolumeAnalysis": {"creator": "VolumeEngine"},
            "VolatilityAnalysis": {"creator": "VolatilityEngine"},
            "ContextBuilding": {"creator": "MarketContextBuilder"},
            "EvidenceComposition": {"creator": "EvidenceEngine"},
            "ContextAnalysis": {"modifier": "ContextEngine"},
            "TradeFilter": {"consumer": "TradeFilterEngine"},
            "DecisionEngine": {"creator": "DecisionResult"},
            "Persistence": {"persister": "SnapshotLogger"},
            "RiskAnalysis": {"creator": "RiskEngine"},
            "ConfluenceAnalysis": {"creator": "ConfluenceEngine"},
            "ConditionAnalysis": {"creator": "MarketConditionEngine"},
            "CandlestickAnalysis": {"creator": "CandlestickEngine"},
            "SRAnalysis": {"creator": "SupportResistanceAnalyzer"}
        }
        
        role_map = roles.get(stage_name, {})
        
        telemetry = TelemetryData(
            engine_name=stage_name,
            start_time=start_time.isoformat(),
            end_time=DeterministicClock.utcnow().isoformat(),
            execution_time=execution_time,
            input_object=str(type(input_obj)),
            output_object=str(type(output_obj)),
            **{**role_map, **metrics}
        )
        self.runtime_report.stages.append(telemetry)

    def analyze(self, symbol="GC=F", avg_volume=None, avg_body=None):
        self.profiler.start_pipeline()
        
        try:
            # 1. Load Data
            start = DeterministicClock.utcnow()
            with self.profiler.stage("DataLoading"):
                df = self.market_service.get_data(symbol)
            self._record_telemetry("DataLoading", start, symbol, df, dataframe_size=len(df))
                
            start = DeterministicClock.utcnow()
            with self.profiler.stage("DataQuality"):
                is_valid, quality_score, reason = self.quality_engine.validate(df)
                if not is_valid:
                    print(f"Data quality issue for {symbol}: {reason} (Score: {quality_score})")
            self._record_telemetry("DataQuality", start, df, is_valid)

            start = DeterministicClock.utcnow()
            with self.profiler.stage("Indicators"):
                indicator_data = self.indicators.calculate(df)
            self._record_telemetry("Indicators", start, df, indicator_data)

            market = MarketData(symbol=symbol, timeframe=DEFAULT_TIMEFRAME, **indicator_data)

            # 2. Execute Engines
            # Structure & Base (Necessary for others)
            start = DeterministicClock.utcnow()
            with self.profiler.stage("StructureAnalysis"):
                structure, structure_evidences = self.structure_intel_engine.evaluate(df, avg_volume=avg_volume, avg_body=avg_body)
                confirmed_swings = self.structure_intel_engine.swing_engine.detect_swings(df)[0]
            self._record_telemetry("StructureAnalysis", start, df, structure, evidence_count=len(structure_evidences))
            
            # Parallelizable/Independent Analyses
            start = DeterministicClock.utcnow()
            with self.profiler.stage("TrendAnalysis"):
                trend_evidences = self.trend.analyze(market)
            self._record_telemetry("TrendAnalysis", start, market, trend_evidences, evidence_count=len(trend_evidences))

            start = DeterministicClock.utcnow()
            with self.profiler.stage("MTFAnalysis"):
                mtf_evidences, mtf_consensus = self.mtf_engine.analyze(symbol)
            self._record_telemetry("MTFAnalysis", start, symbol, mtf_evidences, evidence_count=len(mtf_evidences))

            start = DeterministicClock.utcnow()
            with self.profiler.stage("SmartMoneyAnalysis"):
                smart_money = self.smart_money.analyze(df, confirmed_swings, structure)
                smart_money_evidences = self.smart_money.get_evidences(df, confirmed_swings, structure)
            self._record_telemetry("SmartMoneyAnalysis", start, df, smart_money, evidence_count=len(smart_money_evidences))
                
            start = DeterministicClock.utcnow()
            with self.profiler.stage("SessionAnalysis"):
                session = self.session_engine.analyze() 
            self._record_telemetry("SessionAnalysis", start, df, session)
                
            start = DeterministicClock.utcnow()
            with self.profiler.stage("MarketStateAnalysis"):
                market_state = self.state_engine.analyze(market, session) 
            self._record_telemetry("MarketStateAnalysis", start, market, market_state)
                
            start = DeterministicClock.utcnow()
            with self.profiler.stage("RegimeAnalysis"):
                regime = self.regime_engine.analyze(market, smart_money, structure, indicator_data.get('volume'))
            self._record_telemetry("RegimeAnalysis", start, market, regime)
            
            start = DeterministicClock.utcnow()
            with self.profiler.stage("LiquidityAnalysis"):
                liquidity = self.liquidity_engine.analyze(df, confirmed_swings, structure)
                liquidity_evidences = list(liquidity.evidences)
            self._record_telemetry("LiquidityAnalysis", start, df, liquidity, evidence_count=len(liquidity_evidences))
            
            start = DeterministicClock.utcnow()
            with self.profiler.stage("VolumeAnalysis"):
                volume, volume_evidences = self.volume_engine.evaluate(df)
            self._record_telemetry("VolumeAnalysis", start, df, volume, evidence_count=len(volume_evidences))

            start = DeterministicClock.utcnow()
            with self.profiler.stage("VolatilityAnalysis"):
                volatility = self.volatility_engine.analyze(df, market)
            self._record_telemetry("VolatilityAnalysis", start, df, volatility)

            start = DeterministicClock.utcnow()
            with self.profiler.stage("ConditionAnalysis"):
                market_condition = self.market_condition_engine.analyze(market)
            self._record_telemetry("ConditionAnalysis", start, market, market_condition)
            
            start = DeterministicClock.utcnow()
            with self.profiler.stage("CandlestickAnalysis"):
                candlestick = self.candlestick_engine.analyze(df, market, trend_evidences, market_condition)
            self._record_telemetry("CandlestickAnalysis", start, df, candlestick)
            
            start = DeterministicClock.utcnow()
            with self.profiler.stage("SRAnalysis"):
                sr = self.sr_engine.analyze(df)
            self._record_telemetry("SRAnalysis", start, df, sr)

            # 3. Build Context
            start = DeterministicClock.utcnow()
            with self.profiler.stage("ContextBuilding"):
                context = self.context_builder.build(
                    dataframe=df,
                    market=market,
                    smart_money=smart_money,
                    market_state=market_state,
                    liquidity=liquidity,
                    regime=regime
                )
                context = replace(context, mtf_consensus=mtf_consensus)
            self._record_telemetry("ContextBuilding", start, df, context)
            
            # 4. Build Evidences
            start = DeterministicClock.utcnow()
            evidence_bundle = self.evidence_engine.compose(
                asset=symbol,
                timeframe=DEFAULT_TIMEFRAME,
                context=context,
                trend=trend_evidences,
                mtf=mtf_evidences,
                smart_money=smart_money_evidences,
                volume=volume_evidences,
                structure=structure_evidences,
                liquidity=liquidity_evidences,
                volatility=list(volatility.evidences)
            )
            self._record_telemetry("EvidenceComposition", start, None, evidence_bundle, evidence_count=len(evidence_bundle.evidences))
            
            # 5. Risk, Refinement & Decision
            start = DeterministicClock.utcnow()
            with self.profiler.stage("RiskAnalysis"):
                risk_assessment = self.risk_engine.assess(context, evidence_bundle)
            self._record_telemetry("RiskAnalysis", start, context, risk_assessment)

            # Update context with risk assessment before final refinement and decision
            context = replace(context, risk_assessment=risk_assessment)

            start = DeterministicClock.utcnow()
            with self.profiler.stage("ContextAnalysis"):
                context = self.context_engine.analyze(context=context,evidences=list(evidence_bundle.evidences))
            self._record_telemetry("ContextAnalysis", start, evidence_bundle, context)
                
            start = DeterministicClock.utcnow()
            with self.profiler.stage("TradeFilter"):
                trade_allowed, block_reasons, quality_score, quality_level = self.trade_filter.evaluate(context, evidence_bundle)
            self._record_telemetry("TradeFilter", start, context, trade_allowed, warnings=len(block_reasons))
            
            start = DeterministicClock.utcnow()
            with self.profiler.stage("DecisionEngine"):
                decision = self.decision_engine.analyze(context, evidence_bundle, trade_allowed, block_reasons, quality_score, quality_level)
            self._record_telemetry("DecisionEngine", start, context, decision, warnings=len(decision.warnings), conflicts=len(decision.blockers))

            start = DeterministicClock.utcnow()
            with self.profiler.stage("ConfluenceAnalysis"):
                confluence = self.confluence.analyze(context, evidence_bundle)
            self._record_telemetry("ConfluenceAnalysis", start, context, confluence)

            # 6. Persist
            start = DeterministicClock.utcnow()
            with self.profiler.stage("Persistence"):
                snapshot = DecisionSnapshot(
                    timestamp=DeterministicClock.utcnow().isoformat(),
                    asset=symbol,
                    timeframe=DEFAULT_TIMEFRAME,
                    context=context,
                    evidence_bundle=evidence_bundle,
                    decision_result=decision,
                    version_metadata=decision.version_metadata,
                    audit_events=("Data quality issue detected",) if not is_valid else (),
                    evidence_ranking=decision.evidence_ranking,
                    session_id=self.session_id
                )
                self.snapshot_logger.save(snapshot)
                self.memory.record_decision(snapshot)
                self.last_snapshot = snapshot
                self.last_snapshots[symbol] = snapshot
                self._record_telemetry("Persistence", start, decision, snapshot)


            # Final Result Assembly
            result = AnalysisResult(
                market=market,
                context=context,
                trend=trend_evidences,
                mtf_evidences=mtf_evidences,
                smart_money=smart_money,
                market_regime=regime,
                confluence=confluence,
                market_condition=market_condition,
                market_state=market_state,
                candlestick_analysis=candlestick,
                volatility_analysis=volatility,
                session_analysis=session,
                support_resistance=sr,
                liquidity_analysis=liquidity,
                risk_assessment=risk_assessment,
                evidence_ranking=decision.evidence_ranking,
                volume_analysis=volume,
                structure_analysis=structure,
                decision=decision
            )
            self.profiler.end_pipeline()
            
            if self.runtime_report:
                import json
                with open(f"runtime_report_{symbol}_{DeterministicClock.utcnow().strftime('%Y%m%d%H%M%S')}.json", "w") as f:
                    json.dump(self.runtime_report.to_dict(), f, indent=4)
            
            return result

        except MarketClosedException as e:
            # Decision for Market Closed (Simplified, logic remains identical)
            decision = DecisionResult(
                decision='WAIT', grade='N/A', confidence=0.0, clarity=0.0, risk_score=0.0, score=0.0, quality=0.0,
                expected_strength=0.0, buy_probability=0.0, sell_probability=0.0, wait_probability=1.0,
                expected_risk=0.0, expected_reward=0.0, expected_drawdown=0.0, audit_id='MARKET_CLOSED',
                version_metadata=VersionMetadata(engine_version='1.0.0', pipeline_version='1.0.0', context_version='1.0.0', weights_version='1.0.0'),
                summary=str(e),
                explanation="Market is currently closed."
            )
            dummy_market = MarketData(symbol=symbol, timeframe=DEFAULT_TIMEFRAME, close=0.0, ema9=0.0, ema21=0.0, ema50=0.0,
                                      rsi=0.0, atr=0.0, adx=0.0, macd=0.0, macd_signal=0.0,
                                      bollinger_upper=0.0, bollinger_lower=0.0, volume=0.0)
            snapshot = DecisionSnapshot(
                timestamp=DeterministicClock.utcnow().isoformat(), asset=symbol, timeframe=DEFAULT_TIMEFRAME,
                context=None, evidence_bundle=None, decision_result=decision,
                version_metadata=VersionMetadata(engine_version='1.0.0', pipeline_version='1.0.0', context_version='1.0.0', weights_version='1.0.0'),
                audit_events=("Market Closed",),
                session_id=self.session_id
            )
            self.snapshot_logger.save(snapshot)
            self.last_snapshot = snapshot
            self.profiler.end_pipeline()
            return AnalysisResult(
                market=dummy_market, context=None, trend=[], mtf_evidences=[], smart_money=None,
                market_regime=None, confluence=None, market_condition=None, market_state=None,
                candlestick_analysis=None, volatility_analysis=None, session_analysis=None,
                support_resistance=None, liquidity_analysis=None, risk_assessment=None,
                evidence_ranking=None, volume_analysis=None, structure_analysis=None, decision=decision
            )
