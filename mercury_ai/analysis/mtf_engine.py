from typing import List, Tuple
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.base_provider import MarketDataProvider
from mercury_ai.data.indicator_engine import IndicatorEngine
from mercury_ai.analysis.trend_analyzer import TrendAnalyzer
from mercury_ai.analysis.smart_money.liquidity_engine import LiquidityEngine
from mercury_ai.analysis.volatility_engine import VolatilityEngine
from mercury_ai.analysis.market_structure_intelligence_engine import MarketStructureIntelligenceEngine
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.config.timeframes import YFINANCE_INTERVALS

class MTFEngine:
    """
    Motor institucional de análise multi-timeframe.
    """
    def __init__(self, providers: List[MarketDataProvider]):
        self.market_service = MarketDataService(providers=providers)
        self.indicators = IndicatorEngine()
        self.trend = TrendAnalyzer()
        self.liquidity = LiquidityEngine()
        self.volatility = VolatilityEngine()
        self.structure = MarketStructureIntelligenceEngine()

    def analyze(self, symbol: str) -> Tuple[List[Evidence], MTFConsensus]:
        all_evidences = []
        # Combina timeframes institucionais relevantes
        timeframes = ["M1", "M5", "M15", "H1", "H4"]
        
        # Structure to hold evidences grouped by engine for consensus
        # engine_results[engine_name][timeframe] = direction
        engine_results = {
            "Trend": {},
            "Liquidity": {},
            "Volatility": {},
            "Structure": {}
        }
        
        for tf in timeframes:
            interval = YFINANCE_INTERVALS[tf]
            try:
                df = self.market_service.get_data(symbol, interval=interval, period="1mo")
                if len(df) < 20:
                    continue
                    
                indicator_data = self.indicators.calculate(df)
                market = MarketData(symbol=symbol, timeframe=tf, **indicator_data)
                
                # Get evidences
                trend_evs = self.trend.analyze(market)
                liq_evs = self.liquidity.analyze(df, confirmed_swings=[], structure=None).evidences 
                vol_evs = self.volatility.analyze(df, market).evidences
                _, str_evs = self.structure.evaluate(df)
                
                # Helper to add evs and store direction
                for evs, engine_name in [(trend_evs, "Trend"), (liq_evs, "Liquidity"), (vol_evs, "Volatility"), (str_evs, "Structure")]:
                    direction = self._determine_trend(evs)
                    engine_results[engine_name][tf] = direction
                    for e in evs:
                        e.engine_name = f"{tf} - {e.engine_name}"
                        e.timeframe = tf
                        all_evidences.append(e)

            except Exception:
                continue
                
        return all_evidences, self._build_consensus(engine_results)

    def _build_consensus(self, engine_results: dict) -> MTFConsensus:
        def calculate_factor_alignment(results: dict) -> float:
            trends = list(results.values())
            bullish = trends.count("BULLISH")
            bearish = trends.count("BEARISH")
            total = len(trends)
            return (max(bullish, bearish) / total) * 100 if total > 0 else 0
            
        trend_alignment = calculate_factor_alignment(engine_results["Trend"])
        liquidity_alignment = calculate_factor_alignment(engine_results["Liquidity"])
        volatility_alignment = calculate_factor_alignment(engine_results["Volatility"])
        structure_alignment = calculate_factor_alignment(engine_results["Structure"])
        
        # Aggregate overall
        all_trends = []
        for engine_data in engine_results.values():
            all_trends.extend(list(engine_data.values()))
            
        bullish = all_trends.count("BULLISH")
        bearish = all_trends.count("BEARISH")
        total = len(all_trends)
        
        global_bias = "BULLISH" if bullish > bearish else "BEARISH"
        alignment_score = (max(bullish, bearish) / total) * 100 if total > 0 else 0
        conflict_score = (min(bullish, bearish) / total) * 100 if total > 0 else 0
        
        return MTFConsensus(
            global_bias=global_bias,
            local_bias=engine_results["Trend"].get("M1", "NEUTRAL"),
            conflict_detected=bullish > 0 and bearish > 0,
            alignment_score=alignment_score,
            conflict_score=conflict_score,
            trend_alignment=trend_alignment,
            liquidity_alignment=liquidity_alignment,
            structure_alignment=structure_alignment,
            volatility_alignment=volatility_alignment,
            dominant_trend=global_bias,
            institutional_consensus_strength=float(abs(bullish - bearish)),
            summary=f"Bias: {global_bias}. Alignment: {alignment_score:.1f}%. Conflict: {conflict_score:.1f}%."
        )
