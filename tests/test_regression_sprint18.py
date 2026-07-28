"""
Testes de Regressão — Sprint 1.8 (Bloco 6, Sprint 1.9)

Garante que os 3 bugs críticos corrigidos na Sprint 1.8 não regridam:
  1. MarketStructureProfile.trend — AttributeError
  2. AnalysisPipeline.__init__() — TypeError: missing 'providers'
  3. HistoricalReplayProvider — AttributeError: 'set_index' / 'set_data'
"""

import pandas as pd
import pytest

from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.providers.historical_replay_provider import HistoricalReplayProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService


# ---------------------------------------------------------------------------
# Bug #1: MarketStructureProfile.trend
# Correção: campo 'trend: str = "NEUTRAL"' adicionado ao dataclass
# ---------------------------------------------------------------------------

class TestRegressionBug1MarketStructureProfileTrend:
    """Garante que MarketStructureProfile.trend existe e é acessível."""

    def test_trend_field_exists_default(self):
        """Bug #1: 'MarketStructureProfile' object has no attribute 'trend'."""
        profile = MarketStructureProfile()
        assert hasattr(profile, "trend")
        assert profile.trend == "NEUTRAL"

    def test_trend_field_custom_value(self):
        """Trend deve aceitar valores BULLISH/BEARISH/NEUTRAL."""
        profile = MarketStructureProfile(trend="BULLISH")
        assert profile.trend == "BULLISH"

    def test_trend_field_bearish(self):
        """Trend deve aceitar BEARISH."""
        profile = MarketStructureProfile(trend="BEARISH")
        assert profile.trend == "BEARISH"

    def test_trend_field_is_frozen(self):
        """MarketStructureProfile é frozen — trend não pode ser alterado."""
        profile = MarketStructureProfile(trend="BULLISH")
        with pytest.raises(Exception):
            profile.trend = "BEARISH"  # type: ignore


# ---------------------------------------------------------------------------
# Bug #2: AnalysisPipeline.__init__() missing 'providers'
# ---------------------------------------------------------------------------

class TestRegressionBug2AnalysisPipelineInit:
    """Regression: AnalysisPipeline exige 'providers' no construtor."""

    def test_constructor_with_providers(self):
        """Bug #2: TypeError missing 'providers' — deve aceitar providers."""
        provider = HistoricalReplayProvider()
        pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]),
            providers=[provider],
        )
        assert pipeline is not None

    def test_constructor_missing_providers_raises(self):
        """Sem 'providers' deve levantar TypeError (não AttributeError)."""
        provider = HistoricalReplayProvider()
        with pytest.raises(TypeError):
            AnalysisPipeline(
                market_service=MarketDataService(providers=[provider])
            )


# ---------------------------------------------------------------------------
# Bug #3: HistoricalReplayProvider.set_data / set_index
# ---------------------------------------------------------------------------

class TestRegressionBug3HistoricalReplayProvider:
    """Regressione: HistoricalReplayProvider tem set_data() e set_index()."""

    def test_set_data_exists(self):
        """AttributeError: 'HistoricalReplayProvider' object has no attribute 'set_data'."""
        provider = HistoricalReplayProvider()
        assert hasattr(provider, "set_data")
        assert callable(provider.set_data)

    def test_set_index_exists(self):
        """AttributeError: 'HistoricalReplayProvider' object has no attribute 'set_index'."""
        provider = HistoricalReplayProvider()
        assert hasattr(provider, "set_index")
        assert callable(provider.set_index)

    def test_set_data_and_set_index_workflow(self):
        """Fluxo completo: set_data → set_index → get_data."""
        provider = HistoricalReplayProvider()
        df = pd.DataFrame({
            "open": [10, 11, 12],
            "high": [13, 14, 15],
            "low": [9, 10, 11],
            "close": [12, 13, 14],
            "volume": [100, 200, 300],
        })
        provider.set_data(df)
        provider.set_index(1)  # índice 1 → retorna linhas 0 e 1

        result = provider.get_data("TEST=X")
        assert result is not None
        assert len(result) == 2  # iloc[:2] → 2 linhas

    def test_set_index_zero(self):
        """set_index(0) → get_data retorna 1 linha."""
        provider = HistoricalReplayProvider()
        df = pd.DataFrame({
            "open": [10, 11],
            "high": [13, 14],
            "low": [9, 10],
            "close": [12, 13],
            "volume": [100, 200],
        })
        provider.set_data(df)
        provider.set_index(0)
        result = provider.get_data("BTCUSDT")
        assert len(result) == 1

    def test_get_data_without_set_data(self):
        """Sem set_data, get_data tenta carregar do disco (FileNotFoundError)."""
        provider = HistoricalReplayProvider(data_path="data/nonexistent")
        with pytest.raises(FileNotFoundError):
            provider.get_data("NONEXISTENT_SYMBOL_XYZ")