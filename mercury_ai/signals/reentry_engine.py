"""Reentry Engine — reentrada com proteção na mesma direção (G1/G2) estilo M1/M5.

Filosofia (espelha a operação manual de topo/fundo com proteção):
  - O sinal primário NUNCA é inventado aqui: entra `direction` (BUY/SELL) já
    decidido pelo pipeline. Este motor só classifica REENTRADAS.
  - Reentrada NÃO é martingale cego: cada gale exige confirmação nova na vela
    que falhou (pavio de rejeição na direção original = absorção) ou
    displacement renovado. Sem confirmação -> STOP, não reentra.
  - Limites duros: MAX_GALES = 2 (G1, G2). Após G2 perdido -> LOSS_FINAL.
  - Proteção "na mesma vela": se a vela de entrada fechar contra mas deixar
    pavio de rejeição >= REJECTION_WICK_MIN do range na direção original,
    a reentrada é autorizada na ABERTURA da vela seguinte (mesma direção).
  - Sessão: gale fora de sessão operável (London/NY/Tokyo) é rebaixado:
    G2 vira proibido fora de sessão (risco de drift sem liquidez).

Determinístico: sem rede, sem clock de parede, sem RNG. Somente velas
FECHADAS passadas pelo chamador. Nunca altera decisão, risco ou score.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

MAX_GALES = 2
REJECTION_WICK_MIN = 0.40   # pavio de rejeição >= 40% do range
DISPLACEMENT_BODY_MIN = 0.50  # corpo >= 50% do range = displacement
MIN_BODY_FRAC = 0.30        # vela sem corpo não confirma nada

# Estados de saída
SIGNAL_WIN = "WIN"
REENTRY_G1 = "REENTRY_G1"
REENTRY_G2 = "REENTRY_G2"
LOSS_FINAL = "LOSS_FINAL"
NO_TRADE = "NO_TRADE"

_SESSION_HOURS = {
    "TOKYO": range(6, 7),
    "LONDON": range(7, 12),
    "NY": range(12, 16),
}


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def _session_of(ts: Any) -> str:
    h = getattr(ts, "hour", None)
    if h is None:
        return "UNKNOWN"
    if 21 <= h or h < 6:
        return "SYDNEY"
    for name, rng in _SESSION_HOURS.items():
        if h in rng:
            return name
    return "OFF"


def _candle(row: Any) -> Dict[str, float]:
    return {
        "o": _f(row["Open"]), "h": _f(row["High"]),
        "l": _f(row["Low"]), "c": _f(row["Close"]),
    }


def _rejection_wick(cd: Dict[str, float], direction: str) -> float:
    """Fração do range ocupada pelo pavio que REJEITA o movimento contrário.

    BUY: pavio inferior (rejeição de queda). SELL: pavio superior.
    """
    rng = cd["h"] - cd["l"]
    if rng <= 0:
        return 0.0
    if direction == "BUY":
        return (min(cd["o"], cd["c"]) - cd["l"]) / rng
    return (cd["h"] - max(cd["o"], cd["c"])) / rng


def _displacement(cd: Dict[str, float], direction: str) -> bool:
    rng = cd["h"] - cd["l"]
    if rng <= 0:
        return False
    body = abs(cd["c"] - cd["o"])
    if body < DISPLACEMENT_BODY_MIN * rng:
        return False
    if direction == "BUY":
        return cd["c"] > cd["o"] and cd["c"] >= cd["h"] - 0.34 * rng
    return cd["c"] < cd["o"] and cd["c"] <= cd["l"] + 0.34 * rng


def _closed_in_direction(cd: Dict[str, float], direction: str) -> bool:
    if direction == "BUY":
        return cd["c"] > cd["o"]
    return cd["c"] < cd["o"]


def evaluate_reentry(
    df_closed: Any,
    direction: str,
    entry_index: int,
    max_gales: int = MAX_GALES,
) -> Dict[str, Any]:
    """Avalia o desfecho de um sinal com reentradas protegidas.

    Parâmetros:
      df_closed  : DataFrame OHLC somente com velas FECHADAS (inclui as
                   velas posteriores à entrada para avaliação).
      direction  : "BUY" | "SELL" (direção decidida pelo pipeline).
      entry_index: índice da vela de ENTRADA (a primeira após o sinal).
      max_gales  : teto de reentradas (default 2 = G1 + G2).

    Retorna dict com outcome final, trilha de tentativas e motivo —
    pronto para ser anexado ao Signal como feedback de ganho/perda.
    """
    out: Dict[str, Any] = {
        "outcome": NO_TRADE,
        "direction": direction,
        "attempts": [],
        "gales_used": 0,
        "reason": "",
    }
    direction = str(direction or "").upper()
    if direction not in ("BUY", "SELL"):
        out["reason"] = "sem direção"
        return out
    try:
        n = len(df_closed)
    except Exception:
        out["reason"] = "df inválido"
        return out
    if entry_index >= n:
        out["reason"] = "entrada fora do range de velas fechadas"
        return out

    attempts: List[Dict[str, Any]] = []
    gale = 0
    i = entry_index
    while True:
        cd = _candle(df_closed.iloc[i])
        ts = df_closed.index[i]
        won = _closed_in_direction(cd, direction)
        attempts.append({
            "label": "ENTRY" if gale == 0 else f"G{gale}",
            "ts": str(ts),
            "session": _session_of(ts),
            "result": "WIN" if won else "LOSS",
        })
        if won:
            out["outcome"] = SIGNAL_WIN if gale == 0 else (REENTRY_G1 if gale == 1 else REENTRY_G2)
            out["gales_used"] = gale
            out["reason"] = "win direto" if gale == 0 else f"recuperado no G{gale}"
            break
        # Perdeu a vela: decidir se reentra com proteção
        if gale >= max_gales:
            out["outcome"] = LOSS_FINAL
            out["gales_used"] = gale
            out["reason"] = f"stop após G{gale} (limite de gales)"
            break
        if i + 1 >= n:
            out["outcome"] = LOSS_FINAL
            out["gales_used"] = gale
            out["reason"] = "sem vela seguinte para reentrada"
            break
        wick = _rejection_wick(cd, direction)
        disp = _displacement(cd, direction)
        session = _session_of(ts)
        # Proteção: exige rejeição (absorção) ou displacement renovado
        protected = wick >= REJECTION_WICK_MIN or disp
        # G2 fora de sessão operável é proibido (drift sem liquidez)
        if gale + 1 >= 2 and session not in ("TOKYO", "LONDON", "NY"):
            out["outcome"] = LOSS_FINAL
            out["gales_used"] = gale
            out["reason"] = f"G2 bloqueado fora de sessão ({session})"
            break
        if not protected:
            out["outcome"] = LOSS_FINAL
            out["gales_used"] = gale
            out["reason"] = f"sem proteção (wick={wick:.2f}, disp={disp}) — não reentra"
            break
        gale += 1
        i += 1  # reentra na abertura da próxima vela, mesma direção

    out["attempts"] = attempts
    return out


def signal_feedback(df_closed: Any, direction: str, entry_index: int) -> Dict[str, Any]:
    """Envelope para o Signal: ganho/perda final + detalhe das tentativas.

    Uso: anexar ao payload do sinal emitido, dando ao operador o retorno
    WIN / REENTRY_G1 / REENTRY_G2 / LOSS_FINAL como na IA de referência.
    """
    res = evaluate_reentry(df_closed, direction, entry_index)
    return {
        "result": res["outcome"],
        "gales_used": res["gales_used"],
        "max_gales": MAX_GALES,
        "attempts": res["attempts"],
        "reason": res["reason"],
    }
