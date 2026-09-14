"""Filtro institucional de noticias — evita operar contra calendario economico.

Regra quant/SMC (mesmo padrao audit-only do resto do M5):
- NUNCA altera decisao/score/ranking do motor. Retorna observavel puro
  (BLOCK / CAUTION / CLEAR) para o Signal propagar e o dashboard exibir.
- Estrelas do investing.com: 3★=High (evitar), 2★=Medium (forca nas velas
  = volatilidade/expansao: exige cautela), 1★=Low (ignorar).
- Janelas (America/Sao_Paulo-friendly, tudo em UTC):
    3★ (High):   ±30 min do horario do evento  -> BLOCK (nao operar o par)
    2★ (Medium): ±30 min -> CAUTION (vela com forca: so entrar com
                 confirmacao extra — sweep+FVG+zona ou displacement)
    1★ (Low):    sem restricao -> CLEAR.
- Moedas por simbolo (universo 27 FOREX + 12 CRYPTO):
    FOREX "EURUSD=X" -> {EUR, USD}; CRYPTO "BTC-USD" -> {USD} (driver macro
    e USD: NFP/FOMC/CPI movem crypto junto via dolar + risk-on/off).
    Evento bloqueia o simbolo SSE alguma moeda do evento estiver na
    exposicao do simbolo.
- Fonte: EconomicCalendar.get_events() (hoje estatico: NFP + FOMC) com
  fallback honesto. Operador pode alimentar `data/economic_calendar.json`
  copiado do https://br.investing.com/economic-calendar (ver loader abaixo):
  [{"country":"USD","event":"CPI","impact":"High","stars":3,
    "time":"09:30","date":"2026-09-15"}]. Sem arquivo => usa o calendario
  embutido (2 eventos) e marca source="builtin".

Sem rede, sem broker, sem motores. Nunca levanta (retorna CLEAR/UNKNOWN).
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

CALENDAR_JSON = Path("data/economic_calendar.json")

IMPACT_STARS = {"High": 3, "Medium": 2, "Low": 1}
BLOCK_MINUTES = 30
CAUTION_MINUTES = 30


def _stars(ev: Dict[str, Any]) -> int:
    try:
        s = ev.get("stars")
        if s is not None:
            return max(1, min(3, int(s)))
    except (TypeError, ValueError):
        pass
    return IMPACT_STARS.get(str(ev.get("impact", "")), 1)


def symbol_currencies(symbol: str) -> List[str]:
    """Moedas que movem o simbolo (para cruzar com o calendario)."""
    s = str(symbol or "").upper().strip()
    if not s:
        return []
    try:
        if s.endswith("=X") and len(s) >= 8:
            core = s[:-2]  # EURUSD
            if len(core) == 6:
                return [core[:3], core[3:]]
            return [core]
        if s.endswith("-USD"):
            base = s[:-4]
            # Crypto: driver e o USD macro (+ o proprio ativo).
            return [base, "USD"]
    except Exception:
        return []
    return [s]


def _event_dt(ev: Dict[str, Any]) -> Optional[datetime]:
    try:
        d = str(ev.get("date", "")).strip()
        t = str(ev.get("time", "")).strip()
        if not d or not t or ":" not in t:
            return None
        dt = datetime.strptime(f"{d} {t}", "%Y-%m-%d %H:%M")
        return dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def load_events() -> Dict[str, Any]:
    """Carrega eventos: JSON do operador (investing) ou builtin. Nunca levanta."""
    try:
        from mercury_ai.calendar.economic_calendar import EconomicCalendar
        builtin = EconomicCalendar().get_events() or []
    except Exception:
        builtin = []
    if CALENDAR_JSON.exists():
        try:
            raw = json.loads(CALENDAR_JSON.read_text(encoding="utf-8"))
            if isinstance(raw, list) and raw:
                return {"events": raw, "source": "investing_json"}
        except Exception:
            pass
    return {"events": builtin, "source": "builtin"}


def assess_symbol(symbol: str, events: Optional[List[Dict[str, Any]]] = None,
                 now: Optional[datetime] = None) -> Dict[str, Any]:
    """Risco de noticia para UM simbolo. Retorna dict observavel (sem bloquear)."""
    out: Dict[str, Any] = {
        "risk": "CLEAR", "blocked": False, "caution": False,
        "stars": 0, "event": None, "minutes_to": None, "detail": "",
    }
    try:
        curs = set(symbol_currencies(symbol))
        if not curs:
            out.update(risk="UNKNOWN", detail="simbolo sem moeda mapeavel")
            return out
        evs = events if events is not None else load_events()["events"]
        base = now or datetime.now(timezone.utc)
        if base.tzinfo is None:
            base = base.replace(tzinfo=timezone.utc)
        worst = None
        for ev in evs or []:
            ev_cur = str(ev.get("country", "")).upper().strip()
            if ev_cur not in curs:
                continue
            dt = _event_dt(ev)
            if dt is None:
                continue
            stars = _stars(ev)
            window = BLOCK_MINUTES if stars >= 3 else CAUTION_MINUTES
            delta_min = (dt - base).total_seconds() / 60.0
            if abs(delta_min) <= window and stars >= 2:
                rank = (stars, -abs(delta_min))
                if worst is None or rank > worst[0]:
                    worst = (rank, ev, stars, delta_min)
        if worst is None:
            out["detail"] = "sem evento 2★/3★ na janela"
            return out
        _, ev, stars, delta_min = worst
        name = f"{ev.get('event')} ({ev.get('country')} {stars}★ {ev.get('time')})"
        if stars >= 3:
            out.update(risk="BLOCK", blocked=True, stars=stars, event=name,
                       minutes_to=round(delta_min, 1),
                       detail=f"EVITAR {symbol}: {name} a {delta_min:+.0f}min (janela ±{BLOCK_MINUTES}min)")
        else:
            out.update(risk="CAUTION", caution=True, stars=stars, event=name,
                       minutes_to=round(delta_min, 1),
                       detail=f"CAUTELA {symbol}: {name} a {delta_min:+.0f}min — vela com forca, exigir confirmacao extra")
        return out
    except Exception:
        out.update(risk="UNKNOWN", detail="erro interno (nunca bloqueia)")
        return out
