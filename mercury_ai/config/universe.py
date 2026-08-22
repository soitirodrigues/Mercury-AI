"""
MERCURY AI V1 — UNIVERSO OPERACIONAL OFICIAL
=============================================
Fonte única da verdade para todos os ativos operados pelo Mercury AI.

Operadora: Hezilex
Mercados: FOREX (27 pares) + CRIPTO (12 ativos)
Total: 39 ativos

Símbolos no formato Yahoo Finance:
  - FOREX: {PAR}=X   (ex: EURUSD=X)
  - CRIPTO: {TICKER}-USD (ex: BTC-USD)

Regras de Governança (17 regras — ver docstring completo em OPERATIONAL_GUIDE.md):
  1. Nenhum ativo fora desta lista pode ser analisado pelo Scanner.
  2. Nenhum motor, fórmula, peso ou Model C pode ser alterado.
  3. Qualquer novo ativo deve ser adicionado aqui primeiro e revisado.
  ... (regras completas no documento de especificação)

ATENÇÃO: Este arquivo é a FONTE ÚNICA DA VERDADE.
NÃO duplique listas de ativos em outros módulos.
Todos os consumidores devem importar deste módulo.

S7.X-F1 (2026-09-08): Universo redefinido para 27 FOREX + 12 CRYPTO = 39.
  - STOCKS e COMMODITIES esvaziados (compatibilidade: dicts vazios, não entram em OPERATIONAL_UNIVERSE).
  - Removidos: GBPJPY=X, AUDCAD=X (fora do universo oficial) e POL-USD (delisted, fora).
  - Adicionados: USDAUD=X (Yahoo nativo, sem alias/inversao), LTC-USD, XPL-USD, LINK-USD (Yahoo comprovado).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ============================================================
# TIPOS
# ============================================================

@dataclass(frozen=True)
class UniverseAsset:
    """Representa um ativo no universo operacional do Mercury AI."""
    symbol: str               # Símbolo do provedor (ex: EURUSD=X, BTC-USD)
    display_name: str         # Nome de exibição (ex: EUR/USD, BTC/USD)
    market: str               # FOREX ou CRYPTO
    provider_symbol: str      # Símbolo no provedor principal (Yahoo Finance)
    enabled: bool = True      # Habilitado para operação?
    volatility: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    precision: int = 5        # Casas decimais para cotação
    priority: int = 1         # Prioridade de scanning (1 = máxima)
    notes: str = ""           # Observações (ex: PENDENTE DE CONFIRMAÇÃO)


# ============================================================
# UNIVERSO OFICIAL — 27 FOREX + 12 CRIPTO = 39 ATIVOS
# ============================================================

FOREX_UNIVERSE: Dict[str, UniverseAsset] = {
    "EURUSD=X": UniverseAsset(
        symbol="EURUSD=X", display_name="EUR/USD", market="FOREX",
        provider_symbol="EURUSD=X", volatility="medium", precision=5, priority=1,
        notes="Major — Euro / Dólar Americano"
    ),
    "GBPUSD=X": UniverseAsset(
        symbol="GBPUSD=X", display_name="GBP/USD", market="FOREX",
        provider_symbol="GBPUSD=X", volatility="medium", precision=5, priority=1,
        notes="Major — Libra / Dólar Americano"
    ),
    "USDJPY=X": UniverseAsset(
        symbol="USDJPY=X", display_name="USD/JPY", market="FOREX",
        provider_symbol="USDJPY=X", volatility="medium", precision=3, priority=1,
        notes="Major — Dólar / Iene Japonês"
    ),
    "USDCHF=X": UniverseAsset(
        symbol="USDCHF=X", display_name="USD/CHF", market="FOREX",
        provider_symbol="USDCHF=X", volatility="medium", precision=5, priority=1,
        notes="Major — Dólar / Franco Suíço"
    ),
    "AUDUSD=X": UniverseAsset(
        symbol="AUDUSD=X", display_name="AUD/USD", market="FOREX",
        provider_symbol="AUDUSD=X", volatility="medium", precision=5, priority=1,
        notes="Major — Dólar Australiano / Dólar Americano"
    ),
    "NZDUSD=X": UniverseAsset(
        symbol="NZDUSD=X", display_name="NZD/USD", market="FOREX",
        provider_symbol="NZDUSD=X", volatility="medium", precision=5, priority=1,
        notes="Major — Dólar Neozelandês / Dólar Americano"
    ),
    "USDCAD=X": UniverseAsset(
        symbol="USDCAD=X", display_name="USD/CAD", market="FOREX",
        provider_symbol="USDCAD=X", volatility="medium", precision=5, priority=1,
        notes="Major — Dólar / Dólar Canadense"
    ),
    "EURGBP=X": UniverseAsset(
        symbol="EURGBP=X", display_name="EUR/GBP", market="FOREX",
        provider_symbol="EURGBP=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Euro / Libra"
    ),
    "EURJPY=X": UniverseAsset(
        symbol="EURJPY=X", display_name="EUR/JPY", market="FOREX",
        provider_symbol="EURJPY=X", volatility="medium", precision=3, priority=2,
        notes="Cross — Euro / Iene"
    ),
    "EURCHF=X": UniverseAsset(
        symbol="EURCHF=X", display_name="EUR/CHF", market="FOREX",
        provider_symbol="EURCHF=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Euro / Franco Suíço"
    ),
    "EURAUD=X": UniverseAsset(
        symbol="EURAUD=X", display_name="EUR/AUD", market="FOREX",
        provider_symbol="EURAUD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Euro / Dólar Australiano"
    ),
    "EURNZD=X": UniverseAsset(
        symbol="EURNZD=X", display_name="EUR/NZD", market="FOREX",
        provider_symbol="EURNZD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Euro / Dólar Neozelandês"
    ),
    "EURCAD=X": UniverseAsset(
        symbol="EURCAD=X", display_name="EUR/CAD", market="FOREX",
        provider_symbol="EURCAD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Euro / Dólar Canadense"
    ),
    "GBPCHF=X": UniverseAsset(
        symbol="GBPCHF=X", display_name="GBP/CHF", market="FOREX",
        provider_symbol="GBPCHF=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Libra / Franco Suíço"
    ),
    "GBPAUD=X": UniverseAsset(
        symbol="GBPAUD=X", display_name="GBP/AUD", market="FOREX",
        provider_symbol="GBPAUD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Libra / Dólar Australiano"
    ),
    "GBPNZD=X": UniverseAsset(
        symbol="GBPNZD=X", display_name="GBP/NZD", market="FOREX",
        provider_symbol="GBPNZD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Libra / Dólar Neozelandês"
    ),
    "GBPCAD=X": UniverseAsset(
        symbol="GBPCAD=X", display_name="GBP/CAD", market="FOREX",
        provider_symbol="GBPCAD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Libra / Dólar Canadense"
    ),
    "CHFJPY=X": UniverseAsset(
        symbol="CHFJPY=X", display_name="CHF/JPY", market="FOREX",
        provider_symbol="CHFJPY=X", volatility="medium", precision=3, priority=2,
        notes="Cross — Franco Suíço / Iene"
    ),
    "AUDJPY=X": UniverseAsset(
        symbol="AUDJPY=X", display_name="AUD/JPY", market="FOREX",
        provider_symbol="AUDJPY=X", volatility="medium", precision=3, priority=2,
        notes="Cross — Dólar Australiano / Iene"
    ),
    "AUDCHF=X": UniverseAsset(
        symbol="AUDCHF=X", display_name="AUD/CHF", market="FOREX",
        provider_symbol="AUDCHF=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Dólar Australiano / Franco Suíço"
    ),
    "AUDNZD=X": UniverseAsset(
        symbol="AUDNZD=X", display_name="AUD/NZD", market="FOREX",
        provider_symbol="AUDNZD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Dólar Australiano / Dólar Neozelandês"
    ),
    "NZDJPY=X": UniverseAsset(
        symbol="NZDJPY=X", display_name="NZD/JPY", market="FOREX",
        provider_symbol="NZDJPY=X", volatility="medium", precision=3, priority=2,
        notes="Cross — Dólar Neozelandês / Iene"
    ),
    "NZDCHF=X": UniverseAsset(
        symbol="NZDCHF=X", display_name="NZD/CHF", market="FOREX",
        provider_symbol="NZDCHF=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Dólar Neozelandês / Franco Suíço"
    ),
    "NZDCAD=X": UniverseAsset(
        symbol="NZDCAD=X", display_name="NZD/CAD", market="FOREX",
        provider_symbol="NZDCAD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Dólar Neozelandês / Dólar Canadense"
    ),
    "CADJPY=X": UniverseAsset(
        symbol="CADJPY=X", display_name="CAD/JPY", market="FOREX",
        provider_symbol="CADJPY=X", volatility="medium", precision=3, priority=2,
        notes="Cross — Dólar Canadense / Iene"
    ),
    "CADCHF=X": UniverseAsset(
        symbol="CADCHF=X", display_name="CAD/CHF", market="FOREX",
        provider_symbol="CADCHF=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Dólar Canadense / Franco Suíço"
    ),
    "USDAUD=X": UniverseAsset(
        symbol="USDAUD=X", display_name="USD/AUD", market="FOREX",
        provider_symbol="USDAUD=X", volatility="medium", precision=5, priority=2,
        notes="Cross — Dólar / Dólar Australiano (Yahoo nativo USDAUD=X, sem inversao)"
    ),
}

CRYPTO_UNIVERSE: Dict[str, UniverseAsset] = {
    "BTC-USD": UniverseAsset(
        symbol="BTC-USD", display_name="BTC/USD", market="CRYPTO",
        provider_symbol="BTC-USD", volatility="high", precision=2, priority=1,
        notes="Bitcoin — Principal criptomoeda"
    ),
    "ETH-USD": UniverseAsset(
        symbol="ETH-USD", display_name="ETH/USD", market="CRYPTO",
        provider_symbol="ETH-USD", volatility="high", precision=2, priority=1,
        notes="Ethereum — Smart contracts"
    ),
    "BNB-USD": UniverseAsset(
        symbol="BNB-USD", display_name="BNB/USD", market="CRYPTO",
        provider_symbol="BNB-USD", volatility="high", precision=2, priority=2,
        notes="Binance Coin"
    ),
    "XRP-USD": UniverseAsset(
        symbol="XRP-USD", display_name="XRP/USD", market="CRYPTO",
        provider_symbol="XRP-USD", volatility="high", precision=4, priority=2,
        notes="Ripple"
    ),
    "LTC-USD": UniverseAsset(
        symbol="LTC-USD", display_name="LTC/USD", market="CRYPTO",
        provider_symbol="LTC-USD", volatility="high", precision=2, priority=2,
        notes="Litecoin — Yahoo suporte comprovado"
    ),
    "SOL-USD": UniverseAsset(
        symbol="SOL-USD", display_name="SOL/USD", market="CRYPTO",
        provider_symbol="SOL-USD", volatility="high", precision=2, priority=2,
        notes="Solana"
    ),
    "DOGE-USD": UniverseAsset(
        symbol="DOGE-USD", display_name="DOGE/USD", market="CRYPTO",
        provider_symbol="DOGE-USD", volatility="high", precision=5, priority=3,
        notes="Dogecoin"
    ),
    "AVAX-USD": UniverseAsset(
        symbol="AVAX-USD", display_name="AVAX/USD", market="CRYPTO",
        provider_symbol="AVAX-USD", volatility="high", precision=2, priority=3,
        notes="Avalanche"
    ),
    "SUI-USD": UniverseAsset(
        symbol="SUI-USD", display_name="SUI/USD", market="CRYPTO",
        provider_symbol="SUI-USD", volatility="high", precision=4, priority=3,
        notes="Sui"
    ),
    "XLM-USD": UniverseAsset(
        symbol="XLM-USD", display_name="XLM/USD", market="CRYPTO",
        provider_symbol="XLM-USD", volatility="high", precision=4, priority=3,
        notes="Stellar"
    ),
    "XPL-USD": UniverseAsset(
        symbol="XPL-USD", display_name="XPL/USD", market="CRYPTO",
        provider_symbol="XPL-USD", volatility="high", precision=4, priority=3,
        notes="Plasma (XPL) — Yahoo suporte comprovado"
    ),
    "LINK-USD": UniverseAsset(
        symbol="LINK-USD", display_name="LINK/USD", market="CRYPTO",
        provider_symbol="LINK-USD", volatility="high", precision=2, priority=2,
        notes="Chainlink — Yahoo suporte comprovado"
    ),
}

# ============================================================
# STOCK / COMMODITY — MANTIDOS VAZIOS (compatibilidade)
# S7.X-F1: nao operacionais. Nao incluir em OPERATIONAL_UNIVERSE.
# ============================================================

STOCK_UNIVERSE: Dict[str, UniverseAsset] = {}

COMMODITY_UNIVERSE: Dict[str, UniverseAsset] = {}

# ============================================================
# UNIVERSO COMPLETO (fonte única da verdade)
# ============================================================

OPERATIONAL_UNIVERSE: Dict[str, UniverseAsset] = {
    **FOREX_UNIVERSE,
    **CRYPTO_UNIVERSE,
}

# ============================================================
# LISTAS DERIVADAS (somente leitura — geradas do universo)
# ============================================================

FOREX_SYMBOLS: List[str] = [a.symbol for a in FOREX_UNIVERSE.values() if a.enabled]
CRYPTO_SYMBOLS: List[str] = [a.symbol for a in CRYPTO_UNIVERSE.values() if a.enabled]
STOCK_SYMBOLS: List[str] = [a.symbol for a in STOCK_UNIVERSE.values() if a.enabled]
COMMODITY_SYMBOLS: List[str] = [a.symbol for a in COMMODITY_UNIVERSE.values() if a.enabled]
ALL_SYMBOLS: List[str] = [a.symbol for a in OPERATIONAL_UNIVERSE.values() if a.enabled]

# ============================================================
# SUPORTED_ASSETS (compatibilidade retroativa)
# ============================================================

SUPPORTED_ASSETS: Dict[str, List[str]] = {
    "FOREX": FOREX_SYMBOLS,
    "CRYPTO": CRYPTO_SYMBOLS,
    "COMMODITIES": COMMODITY_SYMBOLS,
    "INDICES": [],
    "STOCKS": STOCK_SYMBOLS,
}

# ============================================================
# FUNÇÕES DE CONSULTA
# ============================================================

def get_asset(symbol: str) -> Optional[UniverseAsset]:
    """Retorna o ativo do universo operacional pelo símbolo."""
    return OPERATIONAL_UNIVERSE.get(symbol)


def get_enabled_symbols(market: Optional[str] = None) -> List[str]:
    """Retorna todos os símbolos habilitados, opcionalmente filtrados por mercado."""
    if market is None:
        return ALL_SYMBOLS
    if market.upper() == "FOREX":
        return FOREX_SYMBOLS
    if market.upper() == "CRYPTO":
        return CRYPTO_SYMBOLS
    if market.upper() == "STOCK":
        return STOCK_SYMBOLS
    if market.upper() == "COMMODITY":
        return COMMODITY_SYMBOLS
    return []


def get_all_provider_symbols() -> List[str]:
    """Retorna todos os símbolos de provedor para registro nos adapters."""
    return [a.provider_symbol for a in OPERATIONAL_UNIVERSE.values() if a.enabled]


def validate_symbol(symbol: str) -> bool:
    """Valida se um símbolo pertence ao universo operacional."""
    return symbol in OPERATIONAL_UNIVERSE


def universe_summary() -> str:
    """Retorna um resumo do universo operacional."""
    forex_count = len(FOREX_SYMBOLS)
    crypto_count = len(CRYPTO_SYMBOLS)
    stock_count = len(STOCK_SYMBOLS)
    commodity_count = len(COMMODITY_SYMBOLS)
    total = forex_count + crypto_count + stock_count + commodity_count
    return (
        f"Universo Operacional Mercury AI V1 — Hezilex\n"
        f"  FOREX:       {forex_count} pares\n"
        f"  CRIPTO:      {crypto_count} ativos\n"
        f"  STOCKS:      {stock_count} ações\n"
        f"  COMMODITIES: {commodity_count} commodities\n"
        f"  TOTAL:       {total} ativos"
    )
