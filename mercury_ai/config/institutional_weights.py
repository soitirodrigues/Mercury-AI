"""
Pesos Institucionais Canônicos — Single Source of Truth.

Este módulo é a ÚNICA fonte de pesos para todas as engines do Mercury AI.
Qualquer alteração nos pesos deve ser feita exclusivamente aqui.

Mapeamento de domínios → pesos (escala 0-100, soma = 100):
  - market_structure: estrutura de mercado (price action, microestrutura)
  - trend: direção e força da tendência
  - smart_money: fluxo institucional / smart money
  - liquidity: varreduras de liquidez, zonas de liquidez
  - support_resistance: proximidade a suportes/resistências
  - volatility: volatilidade (ATR, regime de volatilidade)
  - market_condition: estado do mercado (TRENDING, RANGING, etc.)
  - candlestick: padrões de candlestick / price action events

Usado por:
  - ConfluenceEngine (agregação ponderada de evidências)
  - ConfluenceScoreEngine (cálculo de confluência a partir do MarketContext)
  - ProbabilityEngine (conversão para probabilidades BUY/SELL/WAIT)
"""

# Pesos normalizados (soma = 100) para os 8 domínios institucionais.
INSTITUTIONAL_WEIGHTS: dict[str, float] = {
    "market_structure": 20.0,
    "trend": 18.0,
    "smart_money": 18.0,
    "liquidity": 14.0,
    "support_resistance": 12.0,
    "volatility": 8.0,
    "market_condition": 6.0,
    "candlestick": 4.0,
}

# Versão normalizada para engines que usam escala 0.0–1.0 (ex: ProbabilityEngine).
# Cada peso é dividido pela soma total (100).
INSTITUTIONAL_WEIGHTS_SUM: float = sum(INSTITUTIONAL_WEIGHTS.values())

INSTITUTIONAL_WEIGHTS_NORMALIZED: dict[str, float] = {
    k: v / INSTITUTIONAL_WEIGHTS_SUM for k, v in INSTITUTIONAL_WEIGHTS.items()
}