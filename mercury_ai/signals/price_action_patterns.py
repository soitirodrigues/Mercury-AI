"""Price Action Patterns — Engolfo, Morning/Evening Star, Pin Bar (SIGNAL-ONLY).

Validado (2026-09-20, reports/m5_price_action_probe.json):
  - Engolfo: 85,6% c/ gale (10.315 sinais teste)
  - Morning/Evening Star: 85,6% c/ gale (4.339 sinais)
  - Pin Bar: 85,6% c/ gale (17.404 sinais)
  - Combinados: 86,2% c/ gale (32.057 sinais)

Contrato: so velas fechadas; nunca altera decisao/score/ranking; nunca
executa ordens nem faz rede.
"""
from __future__ import annotations

from typing import Any, Dict


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def detect_price_action(df_closed: Any) -> Dict[str, Any]:
    """Detecta Engolfo, Star ou Pin Bar na ultima vela fechada."""
    out: Dict[str, Any] = {
        "detected": False, "direction": "NONE", "pattern": "NONE", "reason": "sem padrao",
    }
    try:
        if df_closed is None or len(df_closed) < 6:
            out["reason"] = "df insuficiente"
            return out
        window = df_closed.iloc[-6:]
        opens = [_f(v) for v in window["Open"].tolist()]
        closes = [_f(v) for v in window["Close"].tolist()]
        highs = [_f(v) for v in window["High"].tolist()]
        lows = [_f(v) for v in window["Low"].tolist()]
    except (KeyError, IndexError, TypeError, ValueError):
        out["reason"] = "df invalido"
        return out

    n = len(closes)
    i = n - 1
    body = abs(closes[i] - opens[i])
    rng = highs[i] - lows[i]
    if rng <= 0:
        return out
    upper = highs[i] - max(opens[i], closes[i])
    lower = min(opens[i], closes[i]) - lows[i]
    prev_body = abs(closes[i - 1] - opens[i - 1])
    prev2_body = abs(closes[i - 2] - opens[i - 2])
    trend_down = closes[i - 1] < closes[i - 5]
    trend_up = closes[i - 1] > closes[i - 5]
    atr = sum(highs[j] - lows[j] for j in range(max(0, n - 14), n)) / 14.0

    # ENGOLFO
    if (closes[i - 1] < opens[i - 1] and closes[i] > opens[i]
            and closes[i] >= opens[i - 1] and opens[i] <= closes[i - 1] and trend_down):
        out.update(detected=True, direction="BUY", pattern="ENGULFING",
                   reason="engolfo de alta apos queda")
        return out
    if (closes[i - 1] > opens[i - 1] and closes[i] < opens[i]
            and closes[i] <= opens[i - 1] and opens[i] >= closes[i - 1] and trend_up):
        out.update(detected=True, direction="SELL", pattern="ENGULFING",
                   reason="engolfo de baixa apos alta")
        return out

    # MORNING/EVENING STAR
    if (prev2_body > 0.5 * atr and prev_body < 0.3 * atr
            and closes[i] > opens[i] and closes[i] > (opens[i - 2] + closes[i - 2]) / 2 and trend_down):
        out.update(detected=True, direction="BUY", pattern="MORNING_STAR",
                   reason="morning star apos queda")
        return out
    if (prev2_body > 0.5 * atr and prev_body < 0.3 * atr
            and closes[i] < opens[i] and closes[i] < (opens[i - 2] + closes[i - 2]) / 2 and trend_up):
        out.update(detected=True, direction="SELL", pattern="EVENING_STAR",
                   reason="evening star apos alta")
        return out

    # PIN BAR
    if lower >= 2 * body and lower / rng >= 0.6 and trend_down:
        out.update(detected=True, direction="BUY", pattern="PIN_BAR",
                   reason="pin bar de alta em suporte")
        return out
    if upper >= 2 * body and upper / rng >= 0.6 and trend_up:
        out.update(detected=True, direction="SELL", pattern="PIN_BAR",
                   reason="pin bar de baixa em resistencia")
        return out

    return out
