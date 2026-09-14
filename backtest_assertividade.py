"""Backtest assertividade — logica de entrada SMC M5 (CONFIRMED-like) sobre 30d reais.

Espelha forward_bias: trigger N fechada, N-1 alinhado OU displacement N,
filtro de exaustao, entrada na abertura da proxima vela, SL=1.5*ATR, TP=2R,
janela de 12 velas (1h). Sem pipeline, sem replay — pandas + Yahoo direto.
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import pandas as pd
import yfinance as yf

SYMS = ["BTC-USD", "ETH-USD", "XRP-USD"]
PERIOD, INTERVAL = "1mo", "5m"
HOLD = 12  # velas

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

def run(df, use_exhaust=True, tp_r=2.0):
    o = df["Open"].astype(float); h = df["High"].astype(float)
    lo = df["Low"].astype(float); c = df["Close"].astype(float)
    atr = atr14(h, lo, c)
    R = []
    for i in range(30, len(df) - HOLD - 1):
        a = float(atr.iloc[i])
        if not (a > 0): continue
        oN, hN, lN, cN = (float(o.iloc[i]), float(h.iloc[i]), float(lo.iloc[i]), float(c.iloc[i]))
        oP, cP = float(o.iloc[i-1]), float(c.iloc[i-1])
        rng = hN - lN
        if rng <= 0: continue
        body = abs(cN - oN)
        prev_bull = cP > oP; prev_bear = cP < oP
        trig_bull = cN > oN; trig_bear = cN < oN
        disp_bull = body >= 0.5*rng and cN >= hN - 0.34*rng
        disp_bear = body >= 0.5*rng and cN <= lN + 0.34*rng
        opp_wick_b = (hN - max(oN, cN))/rng; opp_wick_s = (min(oN, cN) - lN)/rng
        exh_b = opp_wick_b > 0.6 or body < 0.25*rng
        exh_s = opp_wick_s > 0.6 or body < 0.25*rng
        setups = []
        if trig_bull and (prev_bull or disp_bull) and not (use_exhaust and exh_b):
            setups.append("BUY")
        if trig_bear and (prev_bear or disp_bear) and not (use_exhaust and exh_s):
            setups.append("SELL")
        for d in setups:
            entry = float(o.iloc[i+1]); sl = entry - 1.5*a if d == "BUY" else entry + 1.5*a
            tp = entry + tp_r*1.5*a if d == "BUY" else entry - tp_r*1.5*a
            out = "TIMEOUT"; mfe = 0.0; mae = 0.0
            for j in range(i+1, i+1+HOLD):
                hj, lj = float(h.iloc[j]), float(lo.iloc[j])
                if d == "BUY":
                    mfe = max(mfe, hj-entry); mae = max(mae, entry-lj)
                    ht, hs = hj >= tp, lj <= sl
                else:
                    mfe = max(mfe, entry-lj); mae = max(mae, hj-entry)
                    ht, hs = lj <= tp, hj >= sl
                if ht and hs: out = "LOSS_AMB"; break
                if ht: out = "WIN"; break
                if hs: out = "LOSS"; break
            R.append({"dir": d, "out": out, "mfe_r": mfe/(1.5*a), "mae_r": mae/(1.5*a),
                      "sess": session_of(df.index[i+1]), "ts": str(df.index[i+1])})
    return pd.DataFrame(R)

for sym in SYMS:
    df = yf.download(sym, period=PERIOD, interval=INTERVAL, progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex): df.columns = [c2[0] for c2 in df.columns]
    df.columns = [str(c2).strip().lower() for c2 in df.columns]
    mp = {"open": "Open", "high": "High", "low": "Low", "close": "Close"}
    df = df.rename(columns={k: v for k, v in mp.items() if k in df.columns})
    print(f"== {sym} n={len(df)} {df.index[0]} -> {df.index[-1]}")
    for use_exhaust, tp_r, tag in [(True, 2.0, "BASE_CONFIRMED_TP2R"), (False, 2.0, "SEM_EXAUST_TP2R"), (True, 1.0, "CONFIRMED_TP1R")]:
        r = run(df, use_exhaust, tp_r)
        if len(r) == 0:
            print(f"  {tag}: sem setups"); continue
        tot = len(r); w = int((r.out == "WIN").sum()); l = int(r.out.isin(["LOSS", "LOSS_AMB"]).sum())
        t = tot - w - l
        ev = (w*tp_r - l*1.0)/tot
        print(f"  {tag}: n={tot} WIN={w} LOSS={l} TO={t} win={w/tot:.1%} EV={ev:+.3f}R/sinal")
        by = r.groupby("sess")["out"].agg(n="count", win=lambda s: (s == "WIN").sum())
        for s, row in by.iterrows():
            sub = r[r.sess == s]; ww = int((sub.out == "WIN").sum()); ll = int(sub.out.isin(["LOSS", "LOSS_AMB"]).sum())
            print(f"    {s}: n={len(sub)} win={ww/len(sub):.1%} loss={ll/len(sub):.1%} EV={(ww*tp_r-ll)/len(sub):+.3f}R")
