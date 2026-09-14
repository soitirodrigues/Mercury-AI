"""Backtest estendido: BASE vs MELHORIAS (TP1+BE, gate sessao, displacement, time-stop).

Custo Hezilex: 0.05R por trade debitado (spread+slippage).
TP1+BE: parcial 50% em 1R, stop->breakeven, resto busca 2R em 12 velas.
Gate sessao: SYDNEY/OFF vetados (pula setup).
Displacement: exige displacement no trigger (N) — sem fallback de N-1 alinhado.
Time-stop: se nao atinge +0.5R em 3 velas apos entrada, encerra no preco atual.
Custo: -0.05R por trade.
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import pandas as pd
import yfinance as yf

SYMS = ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD", "DOGE-USD"]
PERIOD, INTERVAL = "1mo", "5m"
HOLD, COST_R = 12, 0.05

def atr14(h, l, c):
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()

def session_of(ts):
    h = ts.hour
    if 21 <= h or h < 6: return "SYDNEY"
    if 6 <= h < 7: return "TOKYO"
    if 7 <= h < 12: return "LONDON"
    if 12 <= h < 16: return "NY"
    return "OFF"

def run(df, mode):
    o = df["Open"].astype(float); h = df["High"].astype(float)
    lo = df["Low"].astype(float); c = df["Close"].astype(float)
    atr = atr14(h, lo, c)
    R = []
    for i in range(30, len(df) - HOLD - 1):
        a = float(atr.iloc[i])
        if not (a > 0): continue
        sess = session_of(df.index[i+1])
        if mode in ("GATE_SESS", "FULL") and sess in ("SYDNEY", "OFF"):
            continue
        oN, hN, lN, cN = (float(o.iloc[i]), float(h.iloc[i]), float(lo.iloc[i]), float(c.iloc[i]))
        oP, cP = float(o.iloc[i-1]), float(c.iloc[i-1])
        rng = hN - lN
        if rng <= 0: continue
        body = abs(cN - oN)
        prev_bull, prev_bear = cP > oP, cP < oP
        trig_bull, trig_bear = cN > oN, cN < oN
        disp_b = body >= 0.5*rng and cN >= hN - 0.34*rng
        disp_s = body >= 0.5*rng and cN <= lN + 0.34*rng
        exh_b = (hN - max(oN, cN))/rng > 0.6 or body < 0.25*rng
        exh_s = (min(oN, cN) - lN)/rng > 0.6 or body < 0.25*rng
        setups = []
        if mode in ("DISP", "FULL"):
            if trig_bull and disp_b and not exh_b: setups.append("BUY")
            if trig_bear and disp_s and not exh_s: setups.append("SELL")
        else:
            if trig_bull and (prev_bull or disp_b) and not exh_b: setups.append("BUY")
            if trig_bear and (prev_bear or disp_s) and not exh_s: setups.append("SELL")
        for d in setups:
            entry = float(o.iloc[i+1])
            risk = 1.5*a
            sl = entry - risk if d == "BUY" else entry + risk
            tp1 = entry + risk if d == "BUY" else entry - risk
            tp2 = entry + 2*risk if d == "BUY" else entry - 2*risk
            out = "TIMEOUT"; pnl = 0.0
            if mode in ("TP1BE", "FULL"):
                # parcial 50% em 1R + BE + runner 2R; time-stop +0.5R em 3 velas
                partial = False; be = sl; tstop = False
                for k in range(1, HOLD+1):
                    j = i+k; hj, lj, cj = float(h.iloc[j]), float(lo.iloc[j]), float(c.iloc[j])
                    cur = (cj-entry) if d == "BUY" else (entry-cj)
                    if not partial and ((hj >= tp1) if d == "BUY" else (lj <= tp1)):
                        partial = True; be = entry  # stop -> BE
                    lo_hit = (lj <= be) if d == "BUY" else (hj >= be)
                    if partial and lo_hit:
                        pnl = 0.5*1.0 + 0.5*0.0; out = "BE_AFTER_TP1"; break
                    if not partial and ((lj <= sl) if d == "BUY" else (hj >= sl)):
                        pnl = -1.0; out = "LOSS"; break
                    if mode == "FULL" and k == 3 and cur < 0.5*risk:
                        pnl = cur/risk; out = "TIMESTOP"; break
                    if partial and ((hj >= tp2) if d == "BUY" else (lj <= tp2)):
                        pnl = 0.5*1.0 + 0.5*2.0; out = "WIN2R"; break
                else:
                    if partial: pnl = 0.5*1.0 + 0.5*((float(c.iloc[i+HOLD])-entry)/risk if d == "BUY" else (entry-float(c.iloc[i+HOLD]))/risk); out = "RUNNER_TO"
                    else: pnl = ((float(c.iloc[i+HOLD])-entry)/risk if d == "BUY" else (entry-float(c.iloc[i+HOLD]))/risk); out = "TIMEOUT"
                pnl -= COST_R
            else:
                for j in range(i+1, i+1+HOLD):
                    hj, lj = float(h.iloc[j]), float(lo.iloc[j])
                    if d == "BUY": ht, hs = hj >= tp2, lj <= sl
                    else: ht, hs = lj <= tp2, hj >= sl
                    if ht and hs: out = "LOSS_AMB"; pnl = -1.0; break
                    if ht: out = "WIN"; pnl = 2.0; break
                    if hs: out = "LOSS"; pnl = -1.0; break
                pnl -= COST_R
            R.append({"dir": d, "out": out, "pnl": pnl, "sess": sess, "ts": str(df.index[i+1])})
    return pd.DataFrame(R)

MODES = ["BASE", "GATE_SESS", "DISP", "TP1BE", "FULL"]
tot_ev = {}
for sym in SYMS:
    df = yf.download(sym, period=PERIOD, interval=INTERVAL, progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex): df.columns = [c2[0] for c2 in df.columns]
    df.columns = [str(c2).strip().lower() for c2 in df.columns]
    df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"})
    print(f"== {sym} n={len(df)} {df.index[0]} -> {df.index[-1]}")
    for m in MODES:
        r = run(df, m)
        if len(r) == 0:
            print(f"  {m}: sem setups"); continue
        n = len(r); ev = r.pnl.mean(); win = (r.pnl > 0).mean()
        tot_ev.setdefault(m, []).append((n, ev))
        print(f"  {m}: n={n} win+={win:.1%} EV={ev:+.4f}R/sinal")
        if m == "FULL":
            print("   outs:", r.out.value_counts().to_dict())
            print("   por sessao:", {s: f"{g.pnl.mean():+.3f}R n={len(g)}" for s, g in r.groupby("sess")})
print("== EV medio 5 ativos ==")
for m, v in tot_ev.items():
    n = sum(x[0] for x in v); ev = sum(x[0]*x[1] for x in v)/n
    print(f"  {m}: n={n} EV={ev:+.4f}R/sinal")
