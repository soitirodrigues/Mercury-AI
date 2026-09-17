"""Compara entrada a MERCADO vs LIMITE no nível varrido (sweep reversal)."""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import yfinance as yf


def atr14(h, l, c):
    import pandas as pd
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def run(df, limit_entry):
    o, h, l, c = df["Open"].astype(float), df["High"].astype(float), df["Low"].astype(float), df["Close"].astype(float)
    atr = atr14(h, l, c)
    res = {"base": [0, 0], "g1": [0, 0], "g2": [0, 0], "fills": 0, "sigs": 0}
    for i in range(60, len(df) - 6):
        a = float(atr.iloc[i])
        if not a > 0:
            continue
        hr = df.index[i].hour
        if not (6 <= hr < 16):
            continue
        swing_h = float(h.iloc[i - 20:i].max())
        swing_l = float(l.iloc[i - 20:i].min())
        oN, hN, lN, cN = float(o.iloc[i]), float(h.iloc[i]), float(l.iloc[i]), float(c.iloc[i])
        rng = hN - lN
        if rng <= 0:
            continue
        wick_up = (hN - max(oN, cN)) / rng
        wick_dn = (min(oN, cN) - lN) / rng
        sweep_h = hN > swing_h and cN < swing_h
        sweep_l = lN < swing_l and cN > swing_l
        d = 0
        lvl = None
        if sweep_h and wick_up >= 0.4 and cN < oN:
            d, lvl = -1, swing_h
        elif sweep_l and wick_dn >= 0.4 and cN > oN:
            d, lvl = 1, swing_l
        if d == 0:
            continue
        res["sigs"] += 1
        if limit_entry:
            for j in range(i + 1, min(i + 4, len(df) - 2)):
                hj, lj = float(h.iloc[j]), float(l.iloc[j])
                if (d == -1 and hj >= lvl) or (d == 1 and lj <= lvl):
                    res["fills"] += 1
                    entry = lvl
                    c1 = float(c.iloc[j])
                    win = (c1 - entry) * d > 0
                    res["base"][0] += win
                    res["base"][1] += 1
                    if not win and j + 2 < len(df):
                        c2 = float(c.iloc[j + 1])
                        w2 = (c2 - c1) * d > 0
                        res["g1"][0] += w2
                        res["g1"][1] += 1
                        if not w2:
                            c3 = float(c.iloc[j + 2])
                            res["g2"][0] += ((c3 - c2) * d > 0)
                            res["g2"][1] += 1
                    break
        else:
            entry = cN
            c1 = float(c.iloc[i + 1])
            win = (c1 - entry) * d > 0
            res["base"][0] += win
            res["base"][1] += 1
            if not win:
                c2 = float(c.iloc[i + 2])
                w2 = (c2 - c1) * d > 0
                res["g1"][0] += w2
                res["g1"][1] += 1
                if not w2:
                    c3 = float(c.iloc[i + 3])
                    res["g2"][0] += ((c3 - c2) * d > 0)
                    res["g2"][1] += 1
    return res


def m(res):
    b, g1, g2 = res["base"], res["g1"], res["g2"]
    if b[1] < 10:
        return None
    p = b[0] / b[1]
    q1 = g1[0] / max(g1[1], 1)
    q2 = g2[0] / max(g2[1], 1)
    return p, b[1], p + (1 - p) * q1 + (1 - p) * (1 - q1) * q2


for sym in ["GBPUSD=X", "GBPJPY=X"]:
    df = yf.download(sym, period="60d", interval="5m", progress=False, auto_adjust=True)
    if isinstance(df.columns, __import__("pandas").MultiIndex):
        df.columns = [c2[0] for c2 in df.columns]
    rm = run(df, False)
    rl = run(df, True)
    mm = m(rm)
    ml = m(rl)
    print(sym)
    if mm:
        print(f"  MERCADO: base={mm[0]:.1%} n={mm[1]} COMB={mm[2]:.1%}")
    if ml:
        print(f"  LIMITE:  base={ml[0]:.1%} n={ml[1]} COMB={ml[2]:.1%} fills={rl['fills']}/{rl['sigs']}")
