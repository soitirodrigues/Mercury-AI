from typing import List, Optional
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.evidence import Evidence
from mercury_ai.analysis.smart_money.market_structure_engine import MarketStructureEngine as LegacyMarketStructureEngine
from mercury_ai.analysis.smart_money.bos_engine import BOSEngine
from mercury_ai.analysis.smart_money.choch_engine import CHOCHEngine
from mercury_ai.analysis.smart_money.order_block_engine import OrderBlockEngine

from mercury_ai.analysis.fair_value_gap_engine import FairValueGapEngine
from mercury_ai.analysis.smart_money.liquidity_engine import LiquidityEngine
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

class SmartMoneyEngine:

    def __init__(self, executor: Optional[PipelineExecutor] = None, profiler: Optional[PipelineProfiler] = None):
        self.executor = executor or PipelineExecutor(profiler)
        self.profiler = profiler
        self.legacy_structure = LegacyMarketStructureEngine()
        self.bos_engine = BOSEngine()
        self.choch_engine = CHOCHEngine()
        self.fvg_engine = FairValueGapEngine(self.executor, profiler)
        self.liquidity_engine = LiquidityEngine(self.executor, profiler)
        self.ob_engine = OrderBlockEngine()

    def analyze(self, df, swings=None, profile=None):
        structure = self.legacy_structure.analyze(df)

        # Scoring Institucional
        institutional_score = 0.0

        # BOS/CHOCH
        bos = self.bos_engine.analyze(structure)
        if bos.detected: institutional_score += 15.0

        choch = self.choch_engine.analyze(structure)
        if choch.detected: institutional_score += 15.0

        # FVG (V1)
        fvg = self.fvg_engine.analyze(df)
        if fvg.is_bullish_fvg or fvg.is_bearish_fvg: institutional_score += 20.0

        # Liquidity (V1)
        liquidity = self.liquidity_engine.analyze(df, swings, profile)
        if len(liquidity.evidences) > 0: institutional_score += 20.0

        # OB
        ob = self.ob_engine.analyze(df)
        if ob is not None: institutional_score += 30.0

        # Score Existente (Preservado)
        explanation = []
        score = 0
        if structure.trend == "BULLISH":
            score += 40
            explanation.append("Estrutura Bullish")
        elif structure.trend == "BEARISH":
            score -= 40
            explanation.append("Estrutura Bearish")
        confidence = abs(score)

        return SmartMoneyAnalysis(
            structure=structure,
            score=score,
            confidence=float(confidence),
            institutional_score=institutional_score,
            explanation=explanation
        )

    def get_evidences(self, df, swings=None, profile=None) -> List[Evidence]:
        evidences = []
        structure = self.legacy_structure.analyze(df)

        # BOS/CHOCH
        bos = self.bos_engine.analyze(structure)
        if bos.detected: 
            evidences.append(Evidence("SmartMoney", f"BOS {bos.direction}", bos.direction, 50.0, float(bos.confidence), ", ".join(bos.explanation), 15.0))

        choch = self.choch_engine.analyze(structure)
        if choch.detected: 
            evidences.append(Evidence("SmartMoney", f"CHOCH {choch.direction}", choch.direction, 50.0, float(choch.confidence), ", ".join(choch.explanation), 15.0))

        # FVG (V1)
        fvg = self.fvg_engine.analyze(df)
        evidences.extend(fvg.evidences)

        # Liquidity (V1)
        liquidity = self.liquidity_engine.analyze(df, swings, profile)
        evidences.extend(liquidity.evidences)

        # OB
        ob = self.ob_engine.analyze(df)
        if ob is not None: 
            evidences.append(Evidence("SmartMoney", "OrderBlock", "NEUTRAL", 50.0, 80.0, f"OB detectado", 30.0))

        return evidences