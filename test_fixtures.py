from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.trade_filter_result import TradeFilterResult
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.market_regime_enum import MarketRegimeEnum
from mercury_ai.models.market_state_enum import MarketStateEnum

# Create minimal evidence using the factory method
evidence1 = Evidence.create(
    engine_name="Trend",
    evidence_name="trend_engine",
    direction="BULLISH",
    strength=80,
    confidence=0.8,
    description="Trend analysis bullish",
    weight=0.5
)

evidence2 = Evidence.create(
    engine_name="StructureEngine",
    evidence_name="structure_engine",
    direction="BULLISH",
    strength=70,
    confidence=0.7,
    description="Structure analysis bullish",
    weight=0.5
)

# Create evidence bundle
evidence_bundle = MarketEvidenceBundle(
    evidences=(evidence1, evidence2),
    timestamp="2024-01-01T00:00:00Z",
    asset="BTC-USD",
    timeframe="1h"
)

# Create market data (note: no 'open' field in MarketData)
market_data = MarketData(
    symbol="BTC-USD",
    timeframe="1h",
    close=105.0,
    ema9=104.0,
    ema21=103.0,
    ema50=101.0,
    rsi=65.0,
    atr=0.0015,
    adx=25.0,
    macd=2.0,
    macd_signal=1.5,
    bollinger_upper=108.0,
    bollinger_lower=102.0,
    volume=1000.0
)

# Create market regime with correct parameters (using available enum)
market_regime = MarketRegime(
    regime=MarketRegimeEnum.CONSOLIDATION,
    confidence=0.8,
    supporting_evidences=(evidence1,)
)

# Create market context
market_context = MarketContext(
    market=market_data,
    trend=[],
    mtf_consensus=None,
    structure=[],
    risk_assessment=None,
    market_regime=market_regime,
    market_state=MarketStateEnum.OPEN,
    concentration=0.5
)

# Create trade filter result (allowed=True means no blockage)
trade_filter_result = TradeFilterResult(
    allowed=True,
    reasons=(),
    quality_score=80.0,
    quality_level="B"
)

print("Fixtures created successfully!")
print(f"Evidence bundle has {len(evidence_bundle.evidences)} evidences")
print(f"Trade filter allowed: {trade_filter_result.allowed}")