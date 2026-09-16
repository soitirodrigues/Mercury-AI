"""Backtest do Reentry Engine — assertividade real com G1/G2 protegidos.

Mesma geração de sinal do backtest_assertividade.py (trigger + alinhamento/
displacement + exaustão), mas o desfecho é avaliado pelo
mercury_ai.signals.reentry_engine: WIN direto, recuperação em G1/G2 com
proteção (pavio de rejeição/displacement) ou LOSS_FINAL.

Também estima EV por sinal sob payout de opções binárias (stake dobra a
cada gale, payout P sobre o stake vencedor).
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import pandas as pd
import yfinance as yf

from mercury_ai.signals.reentry_engine import evaluate_reentry

SYMS = ["BTC-USD", "ETH-USD", "XRP-USD"]
PERIOD, INTERVAL = "1mo", "5m"
PAYOUT = 0.87  # payout típico de corretora de binárias


def atr14(h, l, c):
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def gen_signals(df):
    o, h, lo, c = df["Open"].astype(float), df["High"].astype(float), df["Low"].astype(float), df["Close"].astype(float)
    atr = atr14(h, lo, c)
    sigs = []
    for i in range(30, len(df) - 4):
        a = float(atr.iloc[i])
        if not a > 0:
            continue
        oN, hN, lN, cN = float(o.iloc[i]), float(h.iloc[i]), float(lo.iloc[i]), float(c.iloc[i])
        oP, cP = float(o.iloc[i - 1]), float(c.iloc[i - 1])
        rng = hN - lN
        if rng <= 0:
            continue
        body = abs(cN - oN)
        if body < 0.3 * rng:
            continue
        prev_bull, prev_bear = cP > oP, cP < oP
        trig_bull, trig_bear = cN > oN, cN < oN
        disp_bull = body >= 0.5 * rng and cN >= hN - 0.34 * rng
        disp_bear = body >= 0.5 * rng and cN <= lN + 0.34 * rng
        wick_up = (hN - max(oN, cN)) / rng
        wick_dn = (min(oN, cN) - lN) / rng
        if trig_bull and (prev_bull or disp_bull) and not (wick_up > 0.6 or body < 0.25 * rng):
            sigs.append((i + 1, "BUY"))
        if trig_bear and (prev_bear or disp_bear) and not (wick_dn > 0.6 or body < 0.25 * rng):
            sigs.append((i + 1, "SELL"))
    return sigs


def main():
    tot = {"WIN": 0, "REENTRY_G1": 0, "REENTRY_G2": 0, "LOSS_FINAL": 0}
    ev_total = 0.0
    n_total = 0
    for sym in SYMS:
        df = yf.download(sym, period=PERIOD, interval=INTERVAL, progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c2[0] for c2 in df.columns]
        sigs = gen_signals(df)
        counts = {"WIN": 0, "REENTRY_G1": 0, "REENTRY_G2": 0, "LOSS_FINAL": 0}
        ev = 0.0
        for entry_i, direction in sigs:
            r = evaluate_reentry(df, direction, entry_i)
            out = r["outcome"]
            if out not in counts:
                continue
            counts[out] += 1
            g = r["gales_used"]
            if out == "LOSS_FINAL":
                ev -= (2 ** (g + 1)) - 1  # perdeu entry + gales (1+2+4...)
            else:
                ev += PAYOUT * (2 ** g) - ((2 ** g) - 1)  # ganha no gale g, recupera anteriores
        n = sum(counts.values())
        wins = n - counts["LOSS_FINAL"]
        print(f"== {sym}: n={n}")
        print(f"   WIN direto={counts['WIN']} ({counts['WIN']/n:.1%})  G1={counts['REENTRY_G1']} ({counts['REENTRY_G1']/n:.1%})  "
              f"G2={counts['REENTRY_G2']} ({counts['REENTRY_G2']/n:.1%})  LOSS_FINAL={counts['LOSS_FINAL']} ({counts['LOSS_FINAL']/n:.1%})")
        print(f"   ASSERTIVIDADE COMBINADA={wins/n:.1%}  EV={ev/n:+.3f} stakes/sinal (payout {PAYOUT:.0%})")
        for k in tot:
            tot[k] += counts[k]
        ev_total += ev
        n_total += n
    n = n_total
    wins = n - tot["LOSS_FINAL"]
    print("\n== CONSOLIDADO ==")
    print(f"   n={n}  WIN={tot['WIN']} G1={tot['REENTRY_G1']} G2={tot['REENTRY_G2']} LOSS={tot['LOSS_FINAL']}")
    print(f"   ASSERTIVIDADE COMBINADA={wins/n:.1%}  EV={ev_total/n:+.3f} stakes/sinal")


if __name__ == "__main__":
    main()
