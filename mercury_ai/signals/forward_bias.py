"""Forward-bias M5 — confirmação de continuação p/ a PRÓXIMA vela (puro, sem motores).

Problema auditado: decisão sai da última vela FECHADA (df.index[-1]); o
dashboard só deslocava o HORÁRIO (+5min) sem confirmar se a tendência
sobrevive até a abertura da próxima vela. Isso gera falso positivo quando
a última vela foi martelo/spike já exaurido.

Regra SMC/ICT (somente velas FECHADAS, nunca a em formação):
  trigger   = última vela fechada N (direção d)
  confirma  = vela N-1 precisa estar alinhada OU N precisa ser displacement
              com corpo >= 50% do range no terço direcional
  exaustão  = pavio oposto > 60% do range OU corpo < 25% do range -> DOWNGRADE
  MTF       = M1/M5 precisam concordar com d; H1 contra d -> DOWNGRADE
  veredito  = CONFIRMED (opera) | WEAK (cautela, meio lote) | EXPIRED (pula)

Sem rede, sem broker, sem recalcular score/decisão. Só classifica o sinal
existente. Nunca inventa direção.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

CONFIRMED = "CONFIRMED"
WEAK = "WEAK"
EXPIRED_FWD = "EXPIRED"


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def _dir_of(o: float, c: float) -> str:
    if c > o:
        return "BULLISH"
    if c < o:
        return "BEARISH"
    return "NEUTRAL"


def forward_bias(df_closed: Any, decision: str, mtf_summary: Any = None) -> Dict[str, Any]:
    """Classifica se a direção sobrevive até a próxima vela M5."""
    out: Dict[str, Any] = {
        "state": EXPIRED_FWD, "direction": "NONE", "reason": "sem dados",
        "trigger_close": None, "prev_agree": False, "displacement": False,
        "exhausted": False, "mtf_agree": None,
    }
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        out["reason"] = "sem direção (WAIT/UNKNOWN)"
        return out
    want = "BULLISH" if dec == "BUY" else "BEARISH"
    try:
        if df_closed is None or len(df_closed) < 3:
            out["reason"] = "df insuficiente (<3 fechadas)"
            return out
        df = df_closed.iloc[-3:].copy()
        o = [_f(df["Open"].iloc[i]) for i in range(3)]
        h = [_f(df["High"].iloc[i]) for i in range(3)]
        lo = [_f(df["Low"].iloc[i]) for i in range(3)]
        c = [_f(df["Close"].iloc[i]) for i in range(3)]
    except (KeyError, IndexError, TypeError, ValueError):
        out["reason"] = "df inválido"
        return out
    out["direction"] = want
    out["trigger_close"] = c[-1]
    d_prev = _dir_of(o[-2], c[-2])
    d_trig = _dir_of(o[-1], c[-1])
    out["prev_agree"] = d_prev == want
    rng = h[-1] - lo[-1]
    body = abs(c[-1] - o[-1])
    if rng <= 0:
        out["reason"] = "range nulo"
        return out
    # Displacement: corpo >= 50% no terço direcional
    if want == "BULLISH":
        disp = body >= 0.5 * rng and c[-1] >= h[-1] - 0.34 * rng
        opp_wick = (h[-1] - max(o[-1], c[-1])) / rng
        ex_wick = (min(o[-1], c[-1]) - lo[-1]) / rng
    else:
        disp = body >= 0.5 * rng and c[-1] <= lo[-1] + 0.34 * rng
        opp_wick = (min(o[-1], c[-1]) - lo[-1]) / rng
        ex_wick = (h[-1] - max(o[-1], c[-1])) / rng
    out["displacement"] = bool(disp)
    # Exaustão: pavio oposto dominante ou corpo raquítico
    out["exhausted"] = bool(opp_wick > 0.6 or body < 0.25 * rng)
    # Trigger contra a direção = sinal já morto
    if d_trig != want:
        out["reason"] = f"última fechada {d_trig} contra {want} (sem continuação)"
        return out
    # MTF: M1/M5 a favor; H1 contra = downgrade
    mtf_state, mtf_note = None, ""
    try:
        tf = (mtf_summary or {}).get("timeframes", {}) if isinstance(mtf_summary, dict) else {}
        g = (mtf_summary or {}).get("global_bias") if isinstance(mtf_summary, dict) else None
        m1 = str(tf.get("M1", ""))
        m5 = str(tf.get("M5", ""))
        h1 = str(tf.get("H1", ""))

        def _fav(s: str) -> Optional[bool]:
            s = s.upper()
            if "BULLISH" in s or ("BUY" in s and "SELL" not in s):
                return want == "BULLISH"
            if "BEARISH" in s or ("SELL" in s and "BUY" not in s):
                return want == "BEARISH"
            return None
        votes = [_fav(m1), _fav(m5)]
        votes = [v for v in votes if v is not None]
        h1_against = _fav(h1) is False
        if votes:
            mtf_state = all(votes)
            mtf_note = f"M1/M5 {votes}"
        elif g:
            mtf_state = _fav(str(g))
            mtf_note = f"global {g}"
        if h1_against:
            mtf_note += " + H1 contra (downgrade)"
    except Exception:
        pass
    out["mtf_agree"] = mtf_state
    # Veredito
    if out["exhausted"]:
        out["reason"] = f"exaustão na fechada (pavio oposto {opp_wick:.0%}, corpo {body/rng:.0%})"
        return out
    cont = out["prev_agree"] or disp
    if not cont:
        out["state"] = WEAK
        out["reason"] = "sem continuação (N-1 desalinhado e N sem displacement) — meia posição"
        return out
    if mtf_state is False or (mtf_state is None and h1_against):
        out["state"] = WEAK
        out["reason"] = f"continuação OK mas {mtf_note} — meia posição"
        return out
    out["state"] = CONFIRMED
    out["reason"] = (
        f"continuação confirmada (N-1 {'alinhado' if out['prev_agree'] else '—'}"
        f"{' + displacement' if disp else ''}"
        f"{' + ' + mtf_note if mtf_note else ''})"
    )
    return out
