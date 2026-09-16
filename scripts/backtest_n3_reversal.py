"""Backtest Reversao em Topos/Fundos Multiplos N>=3 (walk-forward, sem lookahead).

Estrategia especificada:
  - Zona S/R: >=3 toques (pivots janela 3, ultimos 60 fechadas), amplitude
    dos toques <= 0.1% do preco (tolerancia teccnica), sem close alem da
    zona antes do gatilho (sem rompimento previo).
  - Gatilho: na 3a+ visita, rejeicao = pinbar (pavio >= 2x corpo, close do
    lado certo) ou engolfo contra a perna de chegada.
  - Direcao: resistencia -> SELL; suporte -> BUY.
  - Risco: SL = extremo da zona + 0.2*ATR; TP = 2R (minimo 1:2).
  - Saida: primeira vela que toca SL ou TP (ordem: se ambas na mesma vela,
    assume-se o pior (SL) — conservador); max 12 velas (timeout = exit a mercado).
Metricas por ativo e portfólio: win rate, profit factor, payoff, max DD
(sequencia de retornos em R), freq sinais/semana, Sharpe (retornos/R).
Comparacao baseline: Top-3 atual (37.0% N+1, n=27) vs N3.
Uso: python scripts/backtest_n3_reversal.py (fundo) — salva
reports/n3_reversal_result.json + imprime matriz.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

UNIVERSE = None  # 38 ativos do universo (SUI off)
N_BARS = 1500  # ~5d M5 por ativo (limite Yahoo)
PIVOT_W = 3
ZONE_LOOKBACK = 60
MIN_TOUCHES = 3
TOUCH_TOL_PCT = 0.001  # +-0.1%
SL_ATR_BUF = 0.2
TP_R = 2.0
MAX_HOLD = 12


def _atr(h, l, c, span=14):
    import pandas as pd
    hh, ll, cc = pd.Series(h), pd.Series(l), pd.Series(c)
    tr = (hh - ll).abs().combine((hh - cc.shift()).abs(), max).combine(
        (ll - cc.shift()).abs(), max)
    v = float(tr.rolling(span).mean().iloc[-1])
    return v if v > 0 else None


def _pivots(h, lo, w=PIVOT_W):
    tops, bots = [], []
    n = len(h)
    for i in range(w, n - w):
        sh, sl = h[i - w:i + w + 1], lo[i - w:i + w + 1]
        if h[i] >= max(sh) and (sh.count(h[i]) == 1 or sh.index(h[i]) == w):
            if not tops or i - tops[-1][0] >= w:
                tops.append((i, h[i]))
        if lo[i] <= min(sl) and (sl.count(lo[i]) == 1 or sl.index(lo[i]) == w):
            if not bots or i - bots[-1][0] >= w:
                bots.append((i, lo[i]))
    return tops, bots


def _zones(pivots, kind):
    """Agrupa pivots por tolerancia 0.1%: cluster se |p-c|/c <= 0.001."""
    zones = []
    for i, p in pivots:
        placed = False
        for z in zones:
            if abs(p - z["level"]) / z["level"] <= TOUCH_TOL_PCT:
                z["touches"].append((i, p))
                z["level"] = sum(t[1] for t in z["touches"]) / len(z["touches"])
                placed = True
                break
        if not placed:
            zones.append({"level": p, "touches": [(i, p)], "kind": kind})
    return [z for z in zones if len(z["touches"]) >= MIN_TOUCHES]


def _rejection(o, h, lo, c, direction):
    rng = h - lo
    body = abs(c - o)
    if rng <= 0 or body <= 0:
        return False
    if direction == "SELL":  # resistencia: pavio sup >= 2x corpo, close baixo
        return c < o and (h - max(o, c)) >= 2.0 * body
    return c > o and (min(o, c) - lo) >= 2.0 * body


def _engulf(o0, c0, o1, c1, direction):
    if direction == "SELL":
        return (c0 > o0) and (c1 < o1) and (c1 <= o0) and (o1 >= c0)
    return (c0 < o0) and (c1 > o1) and (c1 >= o0) and (o1 <= c0)


def backtest_symbol(df):
    o = df["Open"].astype(float).tolist()
    h = df["High"].astype(float).tolist()
    lo = df["Low"].astype(float).tolist()
    c = df["Close"].astype(float).tolist()
    n = len(c)
    trades = []
    i = 60
    while i < n - 2:
        win_o, win_h, win_l, win_c = o[i - ZONE_LOOKBACK:i + 1], h[i - ZONE_LOOKBACK:i + 1], \
            lo[i - ZONE_LOOKBACK:i + 1], c[i - ZONE_LOOKBACK:i + 1]
        tops, bots = _pivots(win_h, win_l)
        atr = _atr(win_h, win_l, win_c)
        if not atr:
            i += 1
            continue
        cands = []
        for z in _zones(tops, "RES") + _zones(bots, "SUP"):
            # indices dos pivots sao relativos a janela [i-60, i];
            # converte p/ global: g = (i-60) + rel
            base = i - ZONE_LOOKBACK
            last_touch_g = base + z["touches"][-1][0]
            if last_touch_g < i - 5:  # zona velha (>5 velas sem revisita): pula
                continue
            # sem rompimento previo: nenhum close alem da zona apos o 1o toque
            lvl = z["level"]
            first_g = base + z["touches"][0][0]
            broken = any((c[k] > lvl * (1 + TOUCH_TOL_PCT)) if z["kind"] == "RES"
                         else (c[k] < lvl * (1 - TOUCH_TOL_PCT))
                         for k in range(first_g, i + 1))
            if broken:
                continue
            direction = "SELL" if z["kind"] == "RES" else "BUY"
            # gatilho na vela i (3a+ visita): rejeicao ou engolfo
            trig = _rejection(o[i], h[i], lo[i], c[i], direction) or \
                _engulf(o[i - 1], c[i - 1], o[i], c[i], direction)
            # toque recente: minimo ou maximo da trigger encosta na zona (0.1%)
            touched = abs((h[i] if direction == "SELL" else lo[i]) - lvl) / lvl <= TOUCH_TOL_PCT * 3
            if trig and touched:
                cands.append((z, direction, lvl))
        if not cands:
            i += 1
            continue
        z, direction, lvl = max(cands, key=lambda t: len(t[0]["touches"]))
        if direction == "SELL":
            sl = max(h[i], lvl) + SL_ATR_BUF * atr
            risk = sl - c[i]
            tp = c[i] - TP_R * risk
        else:
            sl = min(lo[i], lvl) - SL_ATR_BUF * atr
            risk = c[i] - sl
            tp = c[i] + TP_R * risk
        if risk <= 0:
            i += 1
            continue
        # forward: SL/TP/worst-first, timeout 12
        res = None
        for j in range(i + 1, min(i + 1 + MAX_HOLD, n)):
            if direction == "SELL":
                hit_sl = h[j] >= sl
                hit_tp = lo[j] <= tp
            else:
                hit_sl = lo[j] <= sl
                hit_tp = h[j] >= tp
            if hit_sl and hit_tp:
                res = -1.0  # conservador: pior
                break
            if hit_sl:
                res = -1.0
                break
            if hit_tp:
                res = TP_R
                break
        if res is None:  # timeout: exit a mercado em R
            res = ((c[min(i + MAX_HOLD, n - 1)] - c[i]) / risk) if direction == "BUY" \
                else ((c[i] - c[min(i + MAX_HOLD, n - 1)]) / risk)
            res = round(res, 3)
        trades.append({"i": i, "dir": direction, "touches": len(z["touches"]),
                       "level": round(lvl, 5), "r": res})
        i += MAX_HOLD  # sem sobreposicao
    return trades


def metrics(trades):
    import math
    if not trades:
        return {"n": 0}
    rs = [t["r"] for t in trades]
    wins = [r for r in rs if r > 0]
    loss = [-r for r in rs if r <= 0]
    gp, gl = sum(wins), sum(loss)
    eq, peak, mdd = 0.0, 0.0, 0.0
    for r in rs:
        eq += r
        peak = max(peak, eq)
        mdd = min(mdd, eq - peak)
    mu = sum(rs) / len(rs)
    sd = (sum((r - mu) ** 2 for r in rs) / len(rs)) ** 0.5
    return {"n": len(trades), "win_rate": round(100 * len(wins) / len(rs), 1),
            "profit_factor": round(gp / gl, 2) if gl > 0 else 99.99,
            "payoff": round((gp / len(wins)) / (gl / len(loss)), 2) if wins and loss else 0.0,
            "total_r": round(sum(rs), 1), "max_dd_r": round(mdd, 1),
            "sharpe_r": round(mu / sd * (len(rs) ** 0.5), 2) if sd > 0 else 0.0}


def main():
    import yfinance as yf
    from mercury_ai.config.universe import ALL_SYMBOLS
    import json
    syms = list(ALL_SYMBOLS)
    print(f"universo: {len(syms)} ativos")
    per, all_r = {}, []
    t0 = time.time()
    for k, sym in enumerate(syms):
        try:
            df = yf.download(sym, period="5d", interval="5m", progress=False, auto_adjust=False)
            if df is None or len(df) < 100:
                per[sym] = {"n": 0, "err": "no data"}
                continue
            try:
                df.columns = [c2[0] if isinstance(c2, tuple) else c2 for c2 in df.columns]
            except Exception:
                pass
            tr = backtest_symbol(df.tail(N_BARS))
            m = metrics(tr)
            m["trades"] = tr[-5:]
            per[sym] = m
            all_r += [t["r"] for t in tr]
            print(f"[{k + 1}/{len(syms)}] {sym}: n={m['n']} wr={m.get('win_rate')} pf={m.get('profit_factor')}")
        except Exception as e:
            per[sym] = {"n": 0, "err": str(e)[:120]}
    port = metrics([{"r": r} for r in all_r])
    # freq/semana: 5d ~ 1 semana por ativo
    freq = round(sum(v.get("n", 0) for v in per.values()) / max(len(syms), 1), 2)
    out = {"per_asset": per, "portfolio": port, "freq_per_asset_week": freq,
           "params": {"min_touches": MIN_TOUCHES, "tol_pct": TOUCH_TOL_PCT,
                      "sl_atr": SL_ATR_BUF, "tp_r": TP_R, "max_hold": MAX_HOLD},
           "elapsed_s": round(time.time() - t0, 1)}
    Path("reports").mkdir(exist_ok=True)
    Path("reports/n3_reversal_result.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PORTFOLIO: {port} freq={freq}/ativo/semana elapsed={out['elapsed_s']}s")
    print("saved reports/n3_reversal_result.json")


if __name__ == "__main__":
    main()
