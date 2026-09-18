"""Filtros institucionais M5 — observáveis puros (SIGNAL-ONLY, sem decisão).

Problema auditado (55 ciclos PASS, 127 TOP3, velas Yahoo reais):
  G0 direcional puro = 49.6% (moeda). Nenhum filtro isolado testado elevou
  G0 a 85%: EMA200 a favor 50.5% vs contra 47.2%; ATR<=2.0 50.6%;
  trigger body>=0.40 54.4%; trigger alinhada 40.3% (PIOR que desalinhada
  60.0%); displacement 25.0%; CONFIRMED 41.3% vs EXPIRED 58.8-63.2%.

Por isso este módulo NÃO bloqueia nada: calcula observáveis sobre df_closed
(velas fechadas, nunca a em formação) para o Signal propagar e o dashboard
exibir/auditar. Gates bloqueantes exigiriam validação forward em 100+
ciclos — ver scripts/top3_m5_audit.py.

Parâmetros exatos (escala M5, medidos na amostra):
  TRIGGER_BODY_MIN = 0.25  (corpo/range da trigger N; p25 WIN 0.439 vs LOSS 0.300)
  ATR_CAP = 2.0            (range_N / ATR14; p75 WIN 1.495 vs LOSS 1.082)
  EMA_SPAN = 200           (tendência principal; alinhamento close_N vs EMA200)
  ATR_SPAN = 14            (TR médio clássico, só fechadas)
  IDM_LOOKBACK = 5         (janela curta p/ inducement; sweep estrutural usa 20)
  ZONE_LOOKBACK = 48       (perna local ~4h p/ fib 50% premium/discount)

Medição 2026-09-14 (128 TOP3, G0 base 49.2% — sem lookahead, só fechadas):
  FVG a favor ............. 55.3% (cob 59%) | FVG+IDM ....... 59.3% (cob 42%)
  FVG+IDM+zona ............ 83.3% (5/6, cob 4.7%, p~0.097 n.s., halves 3/3+2/3)
  => NENHUM vira bloqueio: FVG+IDM+zona é LINHA DE ESTUDO (n=6, 1 dia).
  Bloqueios propostos e REFUTADOS: MTF>=75 (cob 0% — max real 50),
  trigger-alinhada (manter = 40.3% vs bloquear = 60.7%), zona (40.7% vs
  51.5% contra), sweep-ok (44.9%), EMA200 (50.5% vs 47.2%).

Sem rede, sem broker, sem motores. Nunca altera decisão/score/ranking.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

TRIGGER_BODY_MIN = 0.25
ATR_CAP = 2.0
EMA_SPAN = 200
ATR_SPAN = 14
IDM_LOOKBACK = 5
ZONE_LOOKBACK = 48
# RSI+ADX audit-only (2026-09-15, 38 ativos M5, sem lookahead):
# RSI-14 Wilder, ADX-14 Wilder +DI/-DI. Gate APROVADO como observavel,
# REFUTADO como bloqueio (agregado 48.98% -> 48.46% = -0.52pp, -74.6% sinais).
# TOP3 linha de estudo: NZDCAD 53.09% (+4.82pp), AUDCHF 52.55%, GBPCHF 52.12%.
# NUNCA bloquear: rsi_adx_approved e puro observavel (bool|None).
RSI_SPAN = 14
ADX_SPAN = 14
ADX_MIN_TREND = 20.0
RSI_BUY_LO = 50.0
RSI_BUY_HI = 70.0
RSI_SELL_LO = 30.0
RSI_SELL_HI = 50.0
# Prompt-analise M5 audit-only (2026-09-15, mesmo padrao rsi_adx_approved):
# 5 observaveis novos (bollinger_pos, rsi_value, reversal_candle,
# sr_distance, band_expansion). NUNCA bloqueiam: só painel/logs/auditoria.
# BB 20/2 canonico (IndicatorEngine usa 14/2; aqui padrao industria 20/2).
# S/R = swings pivot(janela 3) nos ultimos 48 fechadas (~4h M5).
BB_SPAN = 20
BB_STD_MULT = 2.0
SR_LOOKBACK = 48
SR_PIVOT = 3
SMC_REVERSAL_MIN_SCORE = 80.0
SMC_EVENT_MAX_AGE = 3


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def trigger_body_ratio(df_closed: Any) -> Optional[float]:
    """Corpo/range da trigger N (última fechada). None se incalculável."""
    try:
        if df_closed is None or len(df_closed) < 1:
            return None
        row = df_closed.iloc[-1]
        o, h, lo, c = _f(row["Open"]), _f(row["High"]), _f(row["Low"]), _f(row["Close"])
        rng = h - lo
        if rng <= 0:
            return None
        return round(abs(c - o) / rng, 4)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def trigger_aligned(df_closed: Any, decision: str) -> Optional[bool]:
    """True se a trigger N fechou na direção da decisão; None se incalculável."""
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return None
    try:
        if df_closed is None or len(df_closed) < 1:
            return None
        row = df_closed.iloc[-1]
        o, c = _f(row["Open"]), _f(row["Close"])
        if c == o:
            return None  # doji: sem direção
        return (c > o) if dec == "BUY" else (c < o)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def atr14(df_closed: Any, span: int = ATR_SPAN) -> Optional[float]:
    """ATR clássico sobre fechadas. None se incalculável."""
    try:
        if df_closed is None or len(df_closed) < span + 1:
            return None
        h = df_closed["High"].astype(float)
        l = df_closed["Low"].astype(float)
        c = df_closed["Close"].astype(float)
        tr = (h - l).abs().combine(
            (h - c.shift()).abs(), max).combine(
            (l - c.shift()).abs(), max)
        val = float(tr.rolling(span).mean().iloc[-1])
        return val if val > 0 else None
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def trigger_range_atr(df_closed: Any) -> Optional[float]:
    """range_N / ATR14 (pré-entrada, só fechadas). None se incalculável."""
    try:
        atr = atr14(df_closed)
        if atr is None or atr <= 0:
            return None
        row = df_closed.iloc[-1]
        rng = _f(row["High"]) - _f(row["Low"])
        if rng <= 0:
            return None
        return round(rng / atr, 3)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def ema200_side(df_closed: Any, decision: str) -> Dict[str, Any]:
    """Lado do preço vs EMA200 (tendência principal).

    Retorna {"aligned": bool|None, "dist_atr": float|None}.
    aligned True = preço a favor da decisão (close_N > EMA200 p/ BUY).
    None quando df < 200 fechadas ou incalculável (nunca bloqueia).
    """
    out: Dict[str, Any] = {"aligned": None, "dist_atr": None}
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return out
    try:
        if df_closed is None or len(df_closed) < EMA_SPAN:
            return out
        cl = df_closed["Close"].astype(float)
        ema = float(cl.ewm(span=EMA_SPAN, adjust=False).mean().iloc[-1])
        px = float(cl.iloc[-1])
        out["aligned"] = (px > ema) if dec == "BUY" else (px < ema)
        atr = atr14(df_closed)
        if atr and atr > 0:
            out["dist_atr"] = round(abs(px - ema) / atr, 2)
        return out
    except (KeyError, IndexError, TypeError, ValueError):
        return out


def rsi14(df_closed: Any, span: int = RSI_SPAN) -> Optional[float]:
    """RSI-14 Wilder sobre fechadas (audit-only). None se incalculavel."""
    try:
        if df_closed is None or len(df_closed) < span + 1:
            return None
        c = df_closed["Close"].astype(float)
        d = c.diff()
        g = d.clip(lower=0.0)
        loss = -d.clip(upper=0.0)
        ag = g.ewm(alpha=1.0 / span, adjust=False).mean()
        al = loss.ewm(alpha=1.0 / span, adjust=False).mean()
        rs = ag / al.replace(0.0, float("nan"))
        val = float((100.0 - 100.0 / (1.0 + rs)).fillna(50.0).iloc[-1])
        return round(val, 2)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def adx_dmi(df_closed: Any, span: int = ADX_SPAN) -> Dict[str, Any]:
    """ADX-14 Wilder + DI+/DI- sobre fechadas (audit-only, sem rede).

    Retorna {"adx": float|None, "plus_di": float|None, "minus_di": float|None}.
    Nones honestos quando df insuficiente (<span+1) ou range nulo.
    Matematica identica a IndicatorEngine (Wilder ewm alpha=1/14).
    """
    out: Dict[str, Any] = {"adx": None, "plus_di": None, "minus_di": None}
    try:
        if df_closed is None or len(df_closed) < span + 1:
            return out
        h = df_closed["High"].astype(float)
        lo = df_closed["Low"].astype(float)
        c = df_closed["Close"].astype(float)
        up = h.diff().clip(lower=0.0)
        dn = (-lo.diff()).clip(lower=0.0)
        import pandas as _pd
        pm = _pd.Series([u if u > d else 0.0 for u, d in zip(up.tolist(), dn.tolist())],
                        index=df_closed.index)
        mm = _pd.Series([d if d > u else 0.0 for u, d in zip(up.tolist(), dn.tolist())],
                        index=df_closed.index)
        tr = (h - lo).abs().combine((h - c.shift()).abs(), max).combine(
            (lo - c.shift()).abs(), max)
        atrw = tr.ewm(alpha=1.0 / span, adjust=False).mean()
        if float(atrw.iloc[-1] or 0.0) <= 0:
            return out
        pdi = 100.0 * (pm.ewm(alpha=1.0 / span, adjust=False).mean() / atrw.replace(0, float("nan")))
        mdi = 100.0 * (mm.ewm(alpha=1.0 / span, adjust=False).mean() / atrw.replace(0, float("nan")))
        denom = (pdi + mdi).replace(0, float("nan"))
        dx = (100.0 * (pdi - mdi).abs() / denom).fillna(0.0)
        adx = dx.ewm(alpha=1.0 / span, adjust=False).mean().fillna(0.0)
        out["adx"] = round(float(adx.iloc[-1]), 2)
        out["plus_di"] = round(float(pdi.fillna(0.0).iloc[-1]), 2)
        out["minus_di"] = round(float(mdi.fillna(0.0).iloc[-1]), 2)
        return out
    except (KeyError, IndexError, TypeError, ValueError):
        return out


def rsi_adx_approved(df_closed: Any, decision: str) -> Optional[bool]:
    """Flag audit-only RSI+ADX (NUNCA bloqueia; None = incalculavel).

    BUY  aprova SE ADX>=20 E +DI>-DI E 50<=RSI<=70.
    SELL aprova SE ADX>=20 E -DI>+DI E 30<=RSI<=50.
    ADX<20 (lateral) ou RSI exaustao (>70/<30) => False.
    """
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return None
    try:
        rsi = rsi14(df_closed)
        dmi = adx_dmi(df_closed)
        adx, pdi, mdi = dmi.get("adx"), dmi.get("plus_di"), dmi.get("minus_di")
        if rsi is None or adx is None or pdi is None or mdi is None:
            return None
        if adx < ADX_MIN_TREND:
            return False
        if dec == "BUY":
            return bool(pdi > mdi and RSI_BUY_LO <= rsi <= RSI_BUY_HI)
        return bool(mdi > pdi and RSI_SELL_LO <= rsi <= RSI_SELL_HI)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def rsi_value(df_closed: Any, span: int = RSI_SPAN) -> Optional[float]:
    """Alias nominal do prompt (rsi_value == rsi14). Audit-only, None-safe."""
    return rsi14(df_closed, span=span)


def bollinger_bands(df_closed: Any, span: int = BB_SPAN,
                    std_mult: float = BB_STD_MULT) -> Dict[str, Any]:
    """BB 20/2 sobre fechadas. Retorna {middle,upper,lower,bandwidth}|Nones."""
    out: Dict[str, Any] = {"middle": None, "upper": None,
                            "lower": None, "bandwidth": None}
    try:
        if df_closed is None or len(df_closed) < span:
            return out
        cl = df_closed["Close"].astype(float)
        mid = cl.rolling(span).mean()
        std = cl.rolling(span).std()
        m, s = float(mid.iloc[-1]), float(std.iloc[-1])
        if not (m > 0) or not (s >= 0):
            return out
        upper, lower = m + std_mult * s, m - std_mult * s
        bw = (upper - lower) / m if m else None
        out["middle"] = round(m, 5)
        out["upper"] = round(float(upper), 5)
        out["lower"] = round(float(lower), 5)
        out["bandwidth"] = round(float(bw), 5) if bw is not None else None
        return out
    except (KeyError, IndexError, TypeError, ValueError):
        return out


def bollinger_pos(df_closed: Any, span: int = BB_SPAN,
                  std_mult: float = BB_STD_MULT) -> Optional[str]:
    """Posicao do close_N vs BB (audit-only).

    ABOVE_UPPER | TOUCH_UPPER | INSIDE | TOUCH_LOWER | BELOW_LOWER.
    TOUCH = pavio encosta na banda mas close fecha dentro (rejeicao).
    None se incalculavel. NUNCA bloqueia.
    """
    try:
        if df_closed is None or len(df_closed) < span:
            return None
        bb = bollinger_bands(df_closed, span=span, std_mult=std_mult)
        upper, lower = bb.get("upper"), bb.get("lower")
        if upper is None or lower is None:
            return None
        row = df_closed.iloc[-1]
        o, h, lo, c = (_f(row["Open"]), _f(row["High"]),
                        _f(row["Low"]), _f(row["Close"]))
        if c > upper:
            return "ABOVE_UPPER"
        if c < lower:
            return "BELOW_LOWER"
        if h >= upper:
            return "TOUCH_UPPER"
        if lo <= lower:
            return "TOUCH_LOWER"
        return "INSIDE"
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def band_expansion(df_closed: Any, span: int = BB_SPAN,
                   std_mult: float = BB_STD_MULT) -> Optional[bool]:
    """True = bandas expandindo (volatilidade abre); False = contraindo.

    Compara bandwidth_N vs bandwidth_N-1 (penultima janela fechada).
    None se incalculavel. Audit-only.
    """
    try:
        if df_closed is None or len(df_closed) < span + 1:
            return None
        b_now = bollinger_bands(df_closed, span=span, std_mult=std_mult).get("bandwidth")
        b_prev = bollinger_bands(df_closed.iloc[:-1], span=span,
                                 std_mult=std_mult).get("bandwidth")
        if b_now is None or b_prev is None:
            return None
        return bool(b_now > b_prev)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def reversal_candle(df_closed: Any) -> Optional[str]:
    """Candle de reversao confirmado no M5 (trigger N fechada).

    BULLISH_REVERSAL: martelo (pavio inf >= 2x corpo, close>open) ou
      engolfo altista vs N-1. BEARISH_REVERSAL: espelho.
    NONE = sem padrao. None = incalculavel (doji/range nulo/df curto).
    Audit-only, nunca bloqueia.
    """
    try:
        if df_closed is None or len(df_closed) < 2:
            return None
        r0, r1 = df_closed.iloc[-2], df_closed.iloc[-1]
        o0, c0 = _f(r0["Open"]), _f(r0["Close"])
        o1, h1, l1, c1 = (_f(r1["Open"]), _f(r1["High"]),
                          _f(r1["Low"]), _f(r1["Close"]))
        rng = h1 - l1
        body = abs(c1 - o1)
        if rng <= 0 or body <= 0:
            return None  # doji/range nulo: sem direcao honesta
        up_wick = h1 - max(o1, c1)
        lo_wick = min(o1, c1) - l1
        bull_hammer = (c1 > o1) and (lo_wick >= 2.0 * body)
        bear_shoot = (c1 < o1) and (up_wick >= 2.0 * body)
        bull_eng = (c0 < o0) and (c1 > o1) and (c1 >= o0) and (o1 <= c0)
        bear_eng = (c0 > o0) and (c1 < o1) and (c1 <= o0) and (o1 >= c0)
        if bull_hammer or bull_eng:
            return "BULLISH_REVERSAL"
        if bear_shoot or bear_eng:
            return "BEARISH_REVERSAL"
        return "NONE"
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def sr_distance(df_closed: Any, lookback: int = SR_LOOKBACK,
                window: int = SR_PIVOT) -> Optional[float]:
    """Distancia ao S/R mais proximo em multiplos de ATR14 (audit-only).

    Niveis = pivots high/low (janela `window`) nas ultimas `lookback`
    fechadas (mesma matematica do next_candle_predictor._swings).
    Retorna min(|close-nivel|)/ATR14, round 3. None se sem nivel/ATR/df.
    """
    try:
        if df_closed is None or len(df_closed) < 15:
            return None
        win = df_closed.iloc[-lookback:] if len(df_closed) >= lookback else df_closed
        h = [_f(v) for v in win["High"].tolist()]
        lo = [_f(v) for v in win["Low"].tolist()]
        n = len(h)
        levels = []
        for i in range(window, n - window):
            seg_h = h[i - window:i + window + 1]
            seg_l = lo[i - window:i + window + 1]
            if h[i] >= max(seg_h) and (seg_h.count(h[i]) == 1
                                       or seg_h.index(h[i]) == window):
                levels.append(h[i])
            if lo[i] <= min(seg_l) and (seg_l.count(lo[i]) == 1
                                        or seg_l.index(lo[i]) == window):
                levels.append(lo[i])
        if not levels:
            return None
        atr = atr14(df_closed)
        if atr is None or atr <= 0:
            return None
        px = float(df_closed["Close"].astype(float).iloc[-1])
        return round(min(abs(px - lv) for lv in levels) / atr, 3)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def institutional_flags(df_closed: Any, decision: str) -> Dict[str, Any]:
    """Pacote observável completo (tudo None-safe).

    Inclui as 4 métricas SMC pedidas (tarefa 2): has_liquidity_sweep,
    in_premium_discount_zone, has_fvg, has_inducement — todas sobre
    df_closed (só fechadas), alinhadas à decisão (BULLISH p/ BUY).
    Sweep usa lookback estrutural 20; inducement usa janela curta 5.
    Zona = fib 50% da perna local (48 fechadas ~4h M5).
    """
    ema = ema200_side(df_closed, decision)
    smc = smc_flags(df_closed, decision)
    dmi = adx_dmi(df_closed)
    bb = bollinger_bands(df_closed)
    try:
        from mercury_ai.signals.trendlines import trendline_flags as _tl_flags
        _tl = _tl_flags(df_closed, decision)
    except Exception:
        _tl = {}
    return {
        "trigger_body_ratio": trigger_body_ratio(df_closed),
        "trigger_aligned": trigger_aligned(df_closed, decision),
        "trigger_range_atr": trigger_range_atr(df_closed),
        "ema200_aligned": ema.get("aligned"),
        "ema200_dist_atr": ema.get("dist_atr"),
        "has_liquidity_sweep": smc.get("has_liquidity_sweep"),
        "in_premium_discount_zone": smc.get("in_premium_discount_zone"),
        "has_fvg": smc.get("has_fvg"),
        "has_inducement": smc.get("has_inducement"),
        "rsi": rsi14(df_closed),
        "adx": dmi.get("adx"),
        "plus_di": dmi.get("plus_di"),
        "minus_di": dmi.get("minus_di"),
        "rsi_adx_approved": rsi_adx_approved(df_closed, decision),
        "bollinger_pos": bollinger_pos(df_closed),
        "rsi_value": rsi_value(df_closed),
        "reversal_candle": reversal_candle(df_closed),
        "sr_distance": sr_distance(df_closed),
        "band_expansion": band_expansion(df_closed),
        "bb_upper": bb.get("upper"),
        "bb_middle": bb.get("middle"),
        "bb_lower": bb.get("lower"),
        "bb_bandwidth": bb.get("bandwidth"),
        "lta_exists": (_tl or {}).get("lta_exists"),
        "ltb_exists": (_tl or {}).get("ltb_exists"),
        "trendline_bias": (_tl or {}).get("trendline_bias"),
        "trendline_aligned": (_tl or {}).get("trendline_aligned"),
        "trendline_distance_atr": (_tl or {}).get("trendline_distance_atr"),
        "trendline_detail": (_tl or {}).get("trendline_detail", ""),
    }


def smc_reversal_flags(df_closed: Any, decision: str) -> Dict[str, Any]:
    """Calcula somente as flags consumidas pelo gate de reversao SMC.

    Mantem a mesma matematica de ``smc_flags`` e dos detectores de trigger,
    mas evita observaveis de painel que nao influenciam a aprovacao.
    """
    smc = smc_flags(df_closed, decision)
    sweep_age = None
    fvg_age = None
    inducement_age = None
    try:
        from mercury_ai.analysis.institutional_confirmation import (
            atr14 as _atr14,
            detect_fvg as _fvg,
            detect_liquidity_sweep as _sweep,
        )
        from mercury_ai.analysis.institutional_confirmation import SWEEP_LOOKBACK as _SWEEP_LOOKBACK
        atr = _atr14(df_closed)
        if atr and atr > 0:
            recent_start = max(0, len(df_closed) - (_SWEEP_LOOKBACK + SMC_EVENT_MAX_AGE + 2))
            sweep = _sweep(df_closed.iloc[recent_start:], atr)
            fvg = _fvg(df_closed, atr)
            last_index = len(df_closed) - 1
            if sweep.get("detected") and sweep.get("direction") == ("BULLISH" if str(decision).upper() == "BUY" else "BEARISH"):
                sweep_age = len(df_closed.iloc[recent_start:]) - 1 - int(sweep["index"])
            if fvg.get("detected") and fvg.get("direction") == ("BULLISH" if str(decision).upper() == "BUY" else "BEARISH"):
                fvg_age = last_index - int(fvg["index"])
            win = df_closed.iloc[-12:-1] if len(df_closed) >= 13 else df_closed
            inducement = _sweep(win, atr, lookback=IDM_LOOKBACK)
            if inducement.get("detected") and inducement.get("direction") == ("BULLISH" if str(decision).upper() == "BUY" else "BEARISH"):
                inducement_age = (len(df_closed) - 2) - int(inducement["index"])
    except (KeyError, IndexError, TypeError, ValueError):
        pass
    return {
        "has_liquidity_sweep": smc.get("has_liquidity_sweep"),
        "in_premium_discount_zone": smc.get("in_premium_discount_zone"),
        "has_fvg": smc.get("has_fvg"),
        "has_inducement": smc.get("has_inducement"),
        "sweep_age": sweep_age,
        "fvg_age": fvg_age,
        "inducement_age": inducement_age,
        "reversal_candle": reversal_candle(df_closed),
        "trigger_aligned": trigger_aligned(df_closed, decision),
        "trigger_body_ratio": trigger_body_ratio(df_closed),
        "trigger_range_atr": trigger_range_atr(df_closed),
    }


def smc_reversal_setup(flags: Dict[str, Any], decision: str) -> Dict[str, Any]:
    """Avalia uma reversao SMC estrita a partir de flags ja calculadas.

    O resultado e opt-in: ele descreve a qualidade da oportunidade, mas nao
    altera a decisao principal. A aprovacao exige sweep, zona, candle de
    reversao, alinhamento da trigger, range controlado e confirmacao FVG/IDM.
    """
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return {"score": 0.0, "approved": False, "reasons": ("invalid_direction",)}

    expected_reversal = (
        "BULLISH_REVERSAL" if dec == "BUY" else "BEARISH_REVERSAL"
    )
    score = 0.0
    reasons = []

    if flags.get("has_liquidity_sweep") is True:
        sweep_age = flags.get("sweep_age")
        if sweep_age is None or _f(sweep_age) <= SMC_EVENT_MAX_AGE:
            score += 25.0
        else:
            reasons.append("liquidity_sweep_stale")
    else:
        reasons.append("liquidity_sweep_missing")

    if flags.get("in_premium_discount_zone") is True:
        score += 15.0
    else:
        reasons.append("premium_discount_zone_missing")

    if flags.get("reversal_candle") == expected_reversal:
        score += 20.0
    else:
        reasons.append("reversal_candle_missing")

    if flags.get("trigger_aligned") is True:
        score += 10.0
    else:
        reasons.append("trigger_not_aligned")

    body_ratio = flags.get("trigger_body_ratio")
    if body_ratio is not None and _f(body_ratio) >= TRIGGER_BODY_MIN:
        score += 10.0
    else:
        reasons.append("trigger_body_below_minimum")

    range_atr = flags.get("trigger_range_atr")
    if range_atr is not None and _f(range_atr) <= ATR_CAP:
        score += 10.0
    else:
        reasons.append("trigger_range_above_atr_cap")

    fvg_age = flags.get("fvg_age")
    inducement_age = flags.get("inducement_age")
    confirmation_recent = (
        (flags.get("has_fvg") is True and (fvg_age is None or _f(fvg_age) <= SMC_EVENT_MAX_AGE))
        or (flags.get("has_inducement") is True and (inducement_age is None or _f(inducement_age) <= SMC_EVENT_MAX_AGE))
    )
    if confirmation_recent:
        score += 10.0
    else:
        reasons.append("fvg_or_inducement_missing_or_stale")

    required = (
        flags.get("has_liquidity_sweep") is True
        and (flags.get("sweep_age") is None or _f(flags.get("sweep_age")) <= SMC_EVENT_MAX_AGE)
        and flags.get("in_premium_discount_zone") is True
        and flags.get("reversal_candle") == expected_reversal
        and flags.get("trigger_aligned") is True
        and body_ratio is not None
        and _f(body_ratio) >= TRIGGER_BODY_MIN
        and range_atr is not None
        and _f(range_atr) <= ATR_CAP
        and confirmation_recent
    )
    return {
        "score": round(score, 2),
        "approved": bool(required and score >= SMC_REVERSAL_MIN_SCORE),
        "reasons": tuple(reasons),
    }


def n3_flags(df_closed: Any, decision: str, symbol: str = "") -> Dict[str, Any]:
    """Selo N3 (observavel, sem bloquear). Nones honestos se sem zona."""
    try:
        from mercury_ai.signals.n3_seal import n3_seal as _seal
        return dict(_seal(df_closed, decision, symbol))
    except Exception:
        return {"n3_touches": None, "n3_level": None, "n3_tight": None,
                "n3_rejection": None, "n3_wr_hist": None, "n3_score": None,
                "n3_detail": ""}


def smc_flags(df_closed: Any, decision: str) -> Dict[str, Any]:
    """4 métricas SMC (observáveis, sem bloquear).

    Retorna Nones honestos quando df insuficiente. Reusa os detectores
    de institutional_confirmation (sem duplicar matemática) + fib 50%
    local. Custo O(n) por detector sobre ~60-500 fechadas: cabe no scan
    sem timeout (sem rede, sem TF extra).
    """
    out: Dict[str, Any] = {
        "has_liquidity_sweep": None,
        "in_premium_discount_zone": None,
        "has_fvg": None,
        "has_inducement": None,
    }
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return out
    want = "BULLISH" if dec == "BUY" else "BEARISH"
    try:
        from mercury_ai.analysis.institutional_confirmation import (
            atr14 as _atr14,
            detect_fvg as _fvg,
            detect_liquidity_sweep as _sweep,
        )
        if df_closed is None or len(df_closed) < 15:
            return out
        atr = _atr14(df_closed)
        if not atr or atr <= 0:
            return out
        sw = _sweep(df_closed, atr)
        out["has_liquidity_sweep"] = bool(sw.get("detected")) and sw.get("direction") == want
        fv = _fvg(df_closed, atr)
        out["has_fvg"] = bool(fv.get("detected")) and fv.get("direction") == want
        win = df_closed.iloc[-12:-1] if len(df_closed) >= 13 else df_closed
        idm = _sweep(win, atr, lookback=IDM_LOOKBACK)
        out["has_inducement"] = (
            bool(idm.get("detected")) and idm.get("direction") == want
        )
        leg = df_closed.iloc[-ZONE_LOOKBACK:] if len(df_closed) >= ZONE_LOOKBACK else df_closed
        try:
            hi = float(leg["High"].max())
            lo = float(leg["Low"].min())
            px = float(df_closed["Close"].iloc[-1])
        except (KeyError, IndexError, TypeError, ValueError):
            return out
        if hi <= lo:
            return out
        fib50 = (hi + lo) / 2.0
        if px == fib50:
            out["in_premium_discount_zone"] = None  # equilibrium: sem lado
        elif dec == "BUY":
            out["in_premium_discount_zone"] = bool(px < fib50)
        else:
            out["in_premium_discount_zone"] = bool(px > fib50)
        return out
    except Exception:
        return out
