"""Liquidity Sweep Reversal — reversão em sweep de liquidez (SMC/ICT).

Edge medido (2026-09-17, 60d M5, split treino/teste 60/40):
  GBPUSD: treino 55.7% (n=61) / teste 54.8% (n=42) — combinada c/ 2 gales 92.9%
  GBPJPY: teste 55.2% (n=87) — combinada 87.4%
  Crypto (BTC/ETH/XRP/SOL/BNB): sem edge (base ~47-50%) — NÃO operar.

Padrão (somente velas FECHADAS):
  sweep     = pavio da vela N ROMPE o swing de 20 velas (high/low) mas o
              FECHAMENTO volta para dentro do range -> liquidez capturada,
              stop dos breakout-traders engatilhado na direção oposta.
  rejeição  = pavio do lado do sweep >= 40% do range E vela fecha na
              direção da reversão (corpo contra o sweep).
  sessão    = somente 06h-16h UTC (Tokyo/London/NY) — fora disso o sweep
              é ruído de liquidez fina.

Este motor é um GERADOR de candidato a sinal (direção + nível), não um
filtro bloqueante do pipeline. Integra-se ao reentry_engine para o plano
G1/G2 e ao outcome engine para feedback WIN/LOSS.

Determinístico: sem rede, sem clock, sem RNG.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

SWING_LOOKBACK = 20
REJECTION_WICK_MIN = 0.40
SESSION_START_UTC = 6   # Tokyo
SESSION_END_UTC = 16    # fim de NY (exclusive)

# Ativos com edge validado por walk-forward (2026-09-17, 2 janelas de 30d):
#   GBPUSD: 58.2%/52.1% VALIDATED | ETH: 56.2%/55.8% VALIDATED
#   GBPJPY/USDJPY/XRP: OBSERVAR (1 janela abaixo) | EURUSD/BTC: REMOVER
# Atualizar SOMENTE via walkforward_sweep_validation.py.
VALIDATED_ASSETS = frozenset({"GBPUSD=X", "GBPUSD", "ETH-USD", "ETHUSD", "ETH"})


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def detect_sweep_reversal(df_closed: Any, ts: Any = None) -> Dict[str, Any]:
    """Detecta sweep+reversão na ÚLTIMA vela fechada de df_closed.

    Retorna dict com:
      direction: "BUY" | "SELL" | "NONE"
      swept_level: preço do swing varrido (nível da liquidez)
      wick_ratio: fração do range no pavio de rejeição
      in_session: bool
      reason: texto auditável
    """
    out: Dict[str, Any] = {
        "direction": "NONE", "swept_level": None, "wick_ratio": 0.0,
        "in_session": False, "reason": "",
    }
    try:
        if df_closed is None or len(df_closed) < SWING_LOOKBACK + 2:
            out["reason"] = "df insuficiente"
            return out
        n = len(df_closed)
        row = df_closed.iloc[-1]
        o, h, l, c = _f(row["Open"]), _f(row["High"]), _f(row["Low"]), _f(row["Close"])
        rng = h - l
        if rng <= 0:
            out["reason"] = "range zero"
            return out
        swing_h = float(df_closed["High"].iloc[-SWING_LOOKBACK - 1:-1].max())
        swing_l = float(df_closed["Low"].iloc[-SWING_LOOKBACK - 1:-1].min())
        idx = df_closed.index[-1]
        hr = getattr(idx, "hour", None)
        in_sess = hr is not None and SESSION_START_UTC <= hr < SESSION_END_UTC
        out["in_session"] = in_sess

        wick_up = (h - max(o, c)) / rng
        wick_dn = (min(o, c) - l) / rng
        sweep_h = h > swing_h and c < swing_h  # varreu topo e voltou
        sweep_l = l < swing_l and c > swing_l  # varreu fundo e voltou

        if sweep_h and wick_up >= REJECTION_WICK_MIN and c < o:
            out.update(direction="SELL", swept_level=swing_h, wick_ratio=wick_up,
                       reason=f"sweep topo {swing_h:.5f} + rejeição {wick_up:.0%}")
        elif sweep_l and wick_dn >= REJECTION_WICK_MIN and c > o:
            out.update(direction="BUY", swept_level=swing_l, wick_ratio=wick_dn,
                       reason=f"sweep fundo {swing_l:.5f} + rejeição {wick_dn:.0%}")
        else:
            out["reason"] = "sem sweep+rejeição"
        if out["direction"] != "NONE" and not in_sess:
            out["reason"] += " (FORA de sessão — downgrade)"
        return out
    except Exception as exc:  # nunca quebra o pipeline
        out["reason"] = f"erro: {exc}"
        return out


def _norm(symbol: str) -> str:
    """Normaliza símbolo para comparação: GBPUSD=X -> GBPUSD, ETH-USD -> ETHUSD."""
    return (str(symbol or "").upper()
            .replace("=X", "").replace("=J", "JPY")
            .replace("-", "").replace("/", "").replace("=", ""))


def asset_validated(symbol: str) -> bool:
    """True se o ativo tem edge medido fora da amostra para este padrão."""
    s = _norm(symbol)
    return any(s == _norm(a) or s.startswith(_norm(a)) for a in VALIDATED_ASSETS)
