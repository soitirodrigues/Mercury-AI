ASSET = "BTC-USD"

TIMEFRAME = "5m"

PERIOD = "5d"

MIN_CONFIDENCE = 70

VERSION = "0.1"

READ_ONLY = True

MONITORING_INTERVAL = 60

SNAPSHOT_PATH = "mercury_ai/database/snapshots"

THEME = "dark"

BROKER = "PaperTrading"

ACCOUNT_TYPE = "Demo"

CAPITAL = 10000.0

DAILY_STOP = 500.0

DAILY_TARGET = 1000.0

LOG_PATH = "logs"

OPERATOR = "Institutional_Admin"

# ============================================================
# Dynamic WAIT cap — Confluência mínima adaptativa por regime
# ============================================================
# Threshold base de confluência institucional para permitir entrada.
# Abaixo deste valor, o DecisionResolver emite WAIT.
CONFLUENCE_MIN_THRESHOLD = 40.0

# Multiplicadores aplicados ao threshold base conforme o regime de mercado.
# Regimes de tendência exigem MENOS confluência (sinal já é forte).
# Regimes de consolidação exigem MAIS confluência (muito ruído direcional).
# Regimes de expansão exigem MAIS confluência (alta volatilidade = risco).
CONFLUENCE_THRESHOLD_MULTIPLIERS = {
    "STRONG_UPTREND": 0.80,      # 40 * 0.80 = 32 — tendência forte, basta menos
    "WEAK_UPTREND": 0.90,        # 40 * 0.90 = 36
    "STRONG_DOWNTREND": 0.80,
    "WEAK_DOWNTREND": 0.90,
    "CONSOLIDATION": 1.30,       # 40 * 1.30 = 52 — ruído alto, exigir mais
    "COMPRESSION": 1.25,         # 40 * 1.25 = 50
    "EXPANSION": 1.20,           # 40 * 1.20 = 48 — volatilidade alta
    "ACCUMULATION": 1.15,        # 40 * 1.15 = 46
    "DISTRIBUTION": 1.15,
    "REVERSAL_TRANSITION": 1.10, # 40 * 1.10 = 44
    "UNKNOWN": 1.00,             # 40 * 1.00 = 40 — neutro
}

# Floor (mínimo absoluto) e cap (máximo absoluto) do threshold dinâmico.
CONFLUENCE_THRESHOLD_FLOOR = 25.0
CONFLUENCE_THRESHOLD_CAP = 60.0
