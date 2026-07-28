# Default Risk Management Configuration

# Risk Management
DEFAULT_RISK_PER_TRADE = 0.01  # 1%
DEFAULT_REWARD_RATIO = 2.0  # 2:1
DEFAULT_STOP_LOSS_PERCENT = 0.005  # 0.5%
DEFAULT_TAKE_PROFIT_PERCENT = 0.010  # 1.0%

# Portfolio/Daily Limits
MAX_DAILY_LOSS = 0.03  # 3%
MAX_DAILY_GAIN = 0.06  # 6%
POSITION_SIZE_MULTIPLIER = 1.0

# --- Bloco 4: Risk Engine Enhancement ---

# VaR / CVaR
VAR_CONFIDENCE_95 = 1.645   # Z-score para 95% confiança (normal)
VAR_CONFIDENCE_99 = 2.326   # Z-score para 99% confiança (normal)
VAR_LOOKBACK_DAYS = 60      # Janela padrão para VaR histórico

# Kelly Criterion
KELLY_DEFAULT_WIN_RATE = 0.55    # Win rate assumida se não houver dados
KELLY_DEFAULT_PAYOFF = 1.5       # Payoff ratio assumido se não houver dados
KELLY_MAX_FRACTION = 0.25        # Cap máximo para Kelly fraction (25%)

# Stress Testing
STRESS_SCENARIOS = {
    "flash_crash": -0.15,     # -15% em um dia
    "bear_market": -0.30,      # -30% drawdown prolongado
    "black_swan": -0.50,       # -50% evento extremo
    "liquidity_crisis": -0.20, # -20% crise de liquidez
    "correlation_one": -0.40,  # -40% correlação perfeita entre ativos
}

# Correlation
CORRELATION_LOOKBACK_DAYS = 90  # Janela para matriz de correlação
