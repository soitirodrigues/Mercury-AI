# PIPELINE CERTIFICATION REPORT

**Generated:** 2026-08-02T00:59:08.887005Z
**Mercury AI Root:** C:\Projetos\Mercury-AI\mercury_ai
**Total Stages:** 20
**Verdict:** PASS

---

## EXECUTIVE SUMMARY

✅ **PASS** - All pipeline stages verified with complete contracts and evidence.

## FINDINGS SUMMARY

- CONTRACT_OK: Provider implements MarketDataProvider protocol
- CONTRACT_OK: CandlestickEngine extends BaseEngine
- DATA_FLOW: MarketData -> Indicators | Output: pd.DataFrame | Input: (df: pd.DataFrame)
- DATA_FLOW: Trend -> MTF | Output: List[Evidence] | Input: (symbol: str)
- DATA_FLOW: MTF -> SmartMoney | Output: Tuple[List[Evidence], MTFConsensus] | Input: (df, swings, profile)
- DATA_FLOW: Liquidity -> Structure | Output: LiquidityResult | Input: (df: pd.DataFrame, avg_volume: pd.Series, avg_body: pd.Series)
- DATA_FLOW: Structure -> Evidence | Output: Tuple[MarketStructureProfile, List[Evidence]] | Input: (raw_evidences: List[Evidence], asset: str, timeframe: str, context: Optional[MarketContext])
- DATA_FLOW: Evidence -> Confluence | Output: MarketEvidenceBundle | Input: (context: MarketContext, evidence_bundle: MarketEvidenceBundle)
- DATA_FLOW: Confluence -> Probability | Output: tuple[ConfluenceResult, list[InstitutionalContribution]] | Input: (context: MarketContext, evidence_bundle: Any, confluence_score: float, confidence_score: float, dominant_direction: Optional[str])
- DATA_FLOW: Probability -> DecisionResolver | Output: ProbabilityResult | Input: (dominant_direction: str, is_valid: bool, opportunity_grade: str, conflicting_signals: bool)
- DATA_FLOW: DecisionResolver -> Explainability | Output: DecisionResolverResult | Input: (decision: str, evidences: List[Evidence], context: MarketContext, confluence_score: float)
- DATA_FLOW: VolumeIntelligence -> Candlestick | Output: Tuple[VolumeProfile, List[Evidence]] | Input: (df: pd.DataFrame, market: MarketData, trend_evidences: List[Evidence], mc: MarketCondition)
- DATA_FLOW: Candlestick -> Volatility | Output: Tuple[CandlestickAnalysis, EngineResult] | Input: (df: pd.DataFrame, market: MarketData)
- DATA_FLOW: Session -> MarketState | Output: SessionAnalysis | Input: (market: MarketData, session: SessionAnalysis)
- DATA_FLOW: MarketState -> RiskEngine | Output: MarketState | Input: (context: MarketContext, evidence_bundle: MarketEvidenceBundle, historical_returns: Optional[List[float]], win_rate: Optional[float], payoff_ratio: Optional[float], asset_returns_map: Optional[Dict[str, List[float]]])

## STAGE-BY-STAGE CERTIFICATION

### Stage 1: Provider

**Module:** `mercury_ai.providers.market_provider`
**Class:** `MercuryDataProvider`
**Method:** `get_data`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\providers\market_provider.py` (L110-L134)

#### Contract Documentation

- **Entrada:** `(symbol: str, interval: str, period: str)`
- **Saída:** `Any (no annotation)`
- **Tipos:** `error, get_data, info, len, str, warning`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new _get_best_provider(), new _healthy_providers(), new error(), new get_data(), new info(), new len(), new warning(), self._get_best_provider, self._healthy_providers`
- **Contratos:** `implements mercury_ai.providers.base_provider.MarketDataProvider`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L110: def get_data(`
- `Docstring: Obtém dados diretamente do melhor provider (sem cache/retry)....`
- `L118: return provider.get_data(symbol, interval)`
- `L130: return False`
- `L134: return True`

---

### Stage 2: MarketData

**Module:** `mercury_ai.data.market_data`
**Class:** `MarketDataService`
**Method:** `get_data`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\data\market_data.py` (L111-L225)

#### Contract Documentation

- **Entrada:** `(symbol: str, interval: str, period: str)`
- **Saída:** `pd.DataFrame`
- **Tipos:** `Exception, best_provider, get_data, hasattr, is_available, pd.DataFrame, print, str, supports_symbol`
- **Tempo:** `O(n) - single loop`
- **Objetos:** `new Exception(), new _normalize_dataframe(), new best_provider(), new get_data(), new hasattr(), new is_available(), new print(), new supports_symbol(), self._normalize_dataframe, self.provider_manager`
- **Contratos:** `implements N/A (concrete service)`
- **Exceções:** `Exception, catches Exception, catches MarketClosedException`

#### Source Evidence

- `L111: def get_data(`
- `L145: return self._normalize_dataframe(`
- `L199: return self._normalize_dataframe(`
- `L223: raise Exception(`

---

### Stage 3: Indicators

**Module:** `mercury_ai.data.indicator_engine`
**Class:** `IndicatorEngine`
**Method:** `calculate`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\data\indicator_engine.py` (L13-L191)

#### Contract Documentation

- **Entrada:** `(df: pd.DataFrame)`
- **Saída:** `Any (no annotation)`
- **Tipos:** `Series, abs, clip, concat, copy, diff, ewm, float, max, mean`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new Series(), new abs(), new clip(), new concat(), new copy(), new diff(), new ewm(), new float(), new max(), new mean()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L13: def calculate(self, df: pd.DataFrame):`
- `L17: # Handle empty DataFrame - return default values matching MarketData fields`
- `L19: return {`
- `L162: return {`

---

### Stage 4: Trend

**Module:** `mercury_ai.analysis.trend_analyzer`
**Class:** `TrendAnalyzer`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\trend_analyzer.py` (L10-L29)

#### Contract Documentation

- **Entrada:** `(market: MarketData)`
- **Saída:** `List[Evidence]`
- **Tipos:** `Evidence, List[Evidence], MarketData, append, float`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new Evidence(), new append(), new float()`
- **Contratos:** `implements N/A (concrete analyzer)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L10: def analyze(self, market: MarketData) -> List[Evidence]:`
- `L29: return evidences`

---

### Stage 5: MTF

**Module:** `mercury_ai.analysis.mtf_engine`
**Class:** `MTFEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\mtf_engine.py` (L27-L72)

#### Contract Documentation

- **Entrada:** `(symbol: str)`
- **Saída:** `Tuple[List[Evidence], MTFConsensus]`
- **Tipos:** `MarketData, Tuple[List[Evidence], MTFConsensus], analyze, append, calculate, detect_swings, evaluate, get_data, len, replace`
- **Tempo:** `O(n²) or higher - nested loops`
- **Objetos:** `new MarketData(), new _build_consensus(), new _determine_trend(), new analyze(), new append(), new calculate(), new detect_swings(), new evaluate(), new get_data(), new len()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `IndexError, KeyError, ValueError`

#### Source Evidence

- `L27: def analyze(self, symbol: str) -> Tuple[List[Evidence], MTFConsensus]:`
- `L72: return all_evidences, self._build_consensus(engine_results)`

---

### Stage 6: SmartMoney

**Module:** `mercury_ai.analysis.smart_money.smart_money_engine`
**Class:** `SmartMoneyEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\smart_money\smart_money_engine.py` (L26-L68)

#### Contract Documentation

- **Entrada:** `(df, swings, profile)`
- **Saída:** `Any (no annotation)`
- **Tipos:** `SmartMoneyAnalysis, abs, analyze, append, float, len`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new SmartMoneyAnalysis(), new abs(), new analyze(), new append(), new float(), new len(), self.bos_engine, self.choch_engine, self.fvg_engine, self.legacy_structure`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L26: def analyze(self, df, swings=None, profile=None):`
- `L62: return SmartMoneyAnalysis(`

---

### Stage 7: Liquidity

**Module:** `mercury_ai.analysis.smart_money.liquidity_engine`
**Class:** `LiquidityEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\smart_money\liquidity_engine.py` (L245-L288)

#### Contract Documentation

- **Entrada:** `(df: pd.DataFrame, swings: List[Swing], profile: MarketStructureProfile, profiler: Optional[PipelineProfiler])`
- **Saída:** `LiquidityResult`
- **Tipos:** `LiquidityResult, List[Swing], MarketStructureProfile, Optional[PipelineProfiler], PipelineExecutor, TypeError, execute, isinstance, pd.DataFrame, tuple`
- **Tempo:** `I/O bound (network/disk)`
- **Objetos:** `new LiquidityResult(), new PipelineExecutor(), new TypeError(), new execute(), new isinstance(), new tuple(), new type(), self.build_equal_high_groups, self.calculate_metrics, self.calculate_scores`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `TypeError`

#### Source Evidence

- `L245: def analyze(self, df: pd.DataFrame, swings: List[Swing], profile: MarketStructureProfile, profiler: Optional[PipelineProfiler] = None) -> LiquidityResult:`
- `L250: raise TypeError("Input 'swings' must be a list of Swing objects.")`
- `L256: if not groups: return LiquidityResult(evidences=(), score=0.0, confidence=0.0, strength=0.0, metadata={})`
- `L260: if not valid_groups: return LiquidityResult(evidences=(), score=0.0, confidence=0.0, strength=0.0, metadata={})`
- `L270: if not selected: return LiquidityResult(evidences=(), score=0.0, confidence=0.0, strength=0.0, metadata={})`

---

### Stage 8: Structure

**Module:** `mercury_ai.analysis.market_structure_intelligence_engine`
**Class:** `MarketStructureIntelligenceEngine`
**Method:** `evaluate`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\market_structure_intelligence_engine.py` (L17-L220)

#### Contract Documentation

- **Entrada:** `(df: pd.DataFrame, avg_volume: pd.Series, avg_body: pd.Series)`
- **Saída:** `Tuple[MarketStructureProfile, List[Evidence]]`
- **Tipos:** `Evidence, MarketStructureProfile, Tuple[MarketStructureProfile, List[Evidence]], abs, analyze_sequence, append, copy, detect_swings, duplicated, float`
- **Tempo:** `O(n) - single loop`
- **Objetos:** `new Evidence(), new MarketStructureProfile(), new abs(), new analyze_sequence(), new append(), new copy(), new detect_swings(), new duplicated(), new float(), new len()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L17: def evaluate(`
- `L25: return MarketStructureProfile(), []`
- `L220: return profile, evidences`

---

### Stage 9: Evidence

**Module:** `mercury_ai.analysis.evidence_engine`
**Class:** `EvidenceEngine`
**Method:** `process`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\evidence_engine.py` (L15-L36)

#### Contract Documentation

- **Entrada:** `(raw_evidences: List[Evidence], asset: str, timeframe: str, context: Optional[MarketContext])`
- **Saída:** `MarketEvidenceBundle`
- **Tipos:** `List[Evidence], MarketEvidenceBundle, Optional[MarketContext], calculate_agreement, evaluate, isoformat, resolve, str, tuple, utcnow`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new MarketEvidenceBundle(), new _deduplicate(), new _normalize(), new calculate_agreement(), new evaluate(), new isoformat(), new resolve(), new tuple(), new utcnow(), self._deduplicate`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L15: def process(self, raw_evidences: List[Evidence], asset: str, timeframe: str, context: Optional[MarketContext] = None) -> MarketEvidenceBundle:`
- `L31: return MarketEvidenceBundle(`

---

### Stage 10: Confluence

**Module:** `mercury_ai.analysis.confluence_engine`
**Class:** `ConfluenceEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\confluence_engine.py` (L50-L132)

#### Contract Documentation

- **Entrada:** `(context: MarketContext, evidence_bundle: MarketEvidenceBundle)`
- **Saída:** `tuple[ConfluenceResult, list[InstitutionalContribution]]`
- **Tipos:** `ConfluenceResult, InstitutionalContribution, MarketContext, MarketEvidenceBundle, append, build, clamp_score, dominant_direction, get, has_conflict`
- **Tempo:** `I/O bound (network/disk)`
- **Objetos:** `new ConfluenceResult(), new InstitutionalContribution(), new append(), new build(), new clamp_score(), new dominant_direction(), new get(), new has_conflict(), new len(), new max()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L50: def analyze(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> tuple[ConfluenceResult, list[InstitutionalContribution]]:`
- `L117: return (`

---

### Stage 11: Probability

**Module:** `mercury_ai.brain.probability_engine`
**Class:** `ProbabilityEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\brain\probability_engine.py` (L34-L245)

#### Contract Documentation

- **Entrada:** `(context: MarketContext, evidence_bundle: Any, confluence_score: float, confidence_score: float, dominant_direction: Optional[str])`
- **Saída:** `ProbabilityResult`
- **Tipos:** `Any, MarketContext, Optional[str], ProbabilityResult, float, get, len, max, min, round`
- **Tempo:** `I/O bound (network/disk)`
- **Objetos:** `new ProbabilityResult(), new get(), new len(), new max(), new min(), new round(), new str(), new sum(), new upper(), self.weights`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L34: def analyze(`
- `L220: return ProbabilityResult(`

---

### Stage 12: DecisionResolver

**Module:** `mercury_ai.analysis.decision_resolver_engine`
**Class:** `DecisionResolverEngine`
**Method:** `resolve`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\decision_resolver_engine.py` (L47-L110)

#### Contract Documentation

- **Entrada:** `(dominant_direction: str, is_valid: bool, opportunity_grade: str, conflicting_signals: bool)`
- **Saída:** `DecisionResolverResult`
- **Tipos:** `DecisionResolverResult, Optional[float], bool, str`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new DecisionResolverResult()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L47: def resolve(`
- `L59: return DecisionResolverResult(`
- `L67: return DecisionResolverResult(`
- `L75: return DecisionResolverResult(`
- `L83: return DecisionResolverResult(`

---

### Stage 13: Explainability

**Module:** `mercury_ai.analysis.narrative_engine`
**Class:** `NarrativeEngine`
**Method:** `generate`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\narrative_engine.py` (L11-L82)

#### Contract Documentation

- **Entrada:** `(decision: str, evidences: List[Evidence], context: MarketContext, confluence_score: float)`
- **Saída:** `TradingExplanation`
- **Tipos:** `List[Evidence], MarketContext, TradingExplanation, float, len, sort, str, tuple`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new TradingExplanation(), new len(), new sort(), new tuple()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L11: def generate(self, decision: str, evidences: List[Evidence],`
- `L48: return TradingExplanation(`

---

### Stage 14: Scanner

**Module:** `mercury_ai.brain.scanner`
**Class:** `MercuryScanner`
**Method:** `scan`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\brain\scanner.py` (L47-L178)

#### Contract Documentation

- **Entrada:** `()`
- **Saída:** `Any (no annotation)`
- **Tipos:** `analyze, append, debug, error, get, get_assets_for_broker, hasattr, info, print_exc, rank`
- **Tempo:** `I/O bound (network/disk)`
- **Objetos:** `new _print_ranking(), new _print_report(), new analyze(), new append(), new debug(), new error(), new get(), new get_assets_for_broker(), new hasattr(), new info()`
- **Contratos:** `implements N/A (orchestrator)`
- **Exceções:** `catches Exception`

#### Source Evidence

- `L47: def scan(self):`
- `L178: return ranked`

---

### Stage 15: VolumeIntelligence

**Module:** `mercury_ai.analysis.volume_intelligence_engine`
**Class:** `VolumeIntelligenceEngine`
**Method:** `evaluate`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\volume_intelligence_engine.py` (L15-L232)

#### Contract Documentation

- **Entrada:** `(df: pd.DataFrame)`
- **Saída:** `Tuple[VolumeProfile, List[Evidence]]`
- **Tipos:** `Evidence, Tuple[VolumeProfile, List[Evidence]], VolumeProfile, abs, append, copy, diff, duplicated, float, isna`
- **Tempo:** `O(n) - single loop`
- **Objetos:** `new Evidence(), new VolumeProfile(), new abs(), new append(), new copy(), new diff(), new duplicated(), new float(), new isna(), new len()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `pandas NA handling`

#### Source Evidence

- `L15: def evaluate(`
- `L22: return VolumeProfile(), []`
- `L61: return VolumeProfile(), []`
- `L115: return VolumeProfile(), []`
- `L121: return VolumeProfile(), []`

---

### Stage 16: Candlestick

**Module:** `mercury_ai.analysis.candlestick_engine`
**Class:** `CandlestickEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\candlestick_engine.py` (L21-L82)

#### Contract Documentation

- **Entrada:** `(df: pd.DataFrame, market: MarketData, trend_evidences: List[Evidence], mc: MarketCondition)`
- **Saída:** `Tuple[CandlestickAnalysis, EngineResult]`
- **Tipos:** `CandlestickAnalysis, EngineResult, List[Evidence], List[str], MarketCondition, MarketData, Tuple[CandlestickAnalysis, EngineResult], abs, append, join`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new CandlestickAnalysis(), new EngineResult(), new _detect_context(), new _detect_continuation(), new _detect_engulfing(), new _detect_pattern(), new _detect_rejection(), new abs(), new append(), new join()`
- **Contratos:** `extends BaseEngine; implements mercury_ai.core.base_engine.BaseEngine`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L21: def analyze(self, df: pd.DataFrame, market: MarketData, trend_evidences: List[Evidence], mc: MarketCondition) -> Tuple[CandlestickAnalysis, EngineResult]:`
- `L26: return CandlestickAnalysis(pattern="NONE", explanation="Dados insuficientes."), EngineResult(0.0, 0.0, (), ("Dados insuf`
- `L70: return CandlestickAnalysis(`

---

### Stage 17: Volatility

**Module:** `mercury_ai.analysis.volatility_engine`
**Class:** `VolatilityEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\volatility_engine.py` (L20-L241)

#### Contract Documentation

- **Entrada:** `(df: pd.DataFrame, market: MarketData)`
- **Saída:** `VolatilityAnalysis`
- **Tipos:** `AverageTrueRange, Evidence, List[Evidence], MarketData, VolatilityAnalysis, append, average_true_range, bool, copy, duplicated`
- **Tempo:** `O(n²) or higher - nested loops`
- **Objetos:** `new AverageTrueRange(), new Evidence(), new VolatilityAnalysis(), new append(), new average_true_range(), new bool(), new copy(), new duplicated(), new float(), new isna()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `pandas NA handling`

#### Source Evidence

- `L20: def analyze(`
- `L29: return VolatilityAnalysis(`
- `L84: return VolatilityAnalysis(`
- `L229: return VolatilityAnalysis(`

---

### Stage 18: Session

**Module:** `mercury_ai.analysis.session_engine`
**Class:** `SessionEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\session_engine.py` (L11-L27)

#### Contract Documentation

- **Entrada:** `()`
- **Saída:** `SessionAnalysis`
- **Tipos:** `List[str], SessionAnalysis, utcnow`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new SessionAnalysis(), new _build_explanation(), new _calculate_liquidity(), new _calculate_quality(), new _detect_overlap(), new _detect_session(), new utcnow(), self._build_explanation, self._calculate_liquidity, self._calculate_quality`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L11: def analyze(self) -> SessionAnalysis:`
- `L21: return SessionAnalysis(`

---

### Stage 19: MarketState

**Module:** `mercury_ai.analysis.market_state_engine`
**Class:** `MarketStateEngine`
**Method:** `analyze`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\market_state_engine.py` (L13-L83)

#### Contract Documentation

- **Entrada:** `(market: MarketData, session: SessionAnalysis)`
- **Saída:** `MarketState`
- **Tipos:** `MarketData, MarketState, SessionAnalysis, append, join`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new MarketState(), new append(), new join()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L13: def analyze(`
- `L80: return MarketState(`

---

### Stage 20: RiskEngine

**Module:** `mercury_ai.analysis.risk_engine`
**Class:** `RiskEngine`
**Method:** `assess`
**File:** `C:\Projetos\Mercury-AI\mercury_ai\analysis\risk_engine.py` (L42-L129)

#### Contract Documentation

- **Entrada:** `(context: MarketContext, evidence_bundle: MarketEvidenceBundle, historical_returns: Optional[List[float]], win_rate: Optional[float], payoff_ratio: Optional[float], asset_returns_map: Optional[Dict[str, List[float]]])`
- **Saída:** `RiskAssessment`
- **Tipos:** `MarketContext, MarketEvidenceBundle, Optional[Dict[str, List[float]]], Optional[List[float]], Optional[float], RiskAssessment, abs, evaluate, float, len`
- **Tempo:** `O(1) - constant time`
- **Objetos:** `new RiskAssessment(), new _compute_correlation_matrix(), new _compute_kelly(), new _compute_stress_test(), new _compute_var_cvar(), new abs(), new evaluate(), new float(), new len(), new list()`
- **Contratos:** `implements N/A (concrete engine)`
- **Exceções:** `None explicitly raised`

#### Source Evidence

- `L42: def assess(`
- `Docstring: 
        Avaliação completa de risco.

        Args:
            context: Contexto de mercado atual
            evidence_bundle: Bundle de evidências
            historical_returns: Lista de retornos ...`
- `L109: return RiskAssessment(`

---
