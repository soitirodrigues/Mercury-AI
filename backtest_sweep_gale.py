"""Backtest: sweep de liquidez + rejeição (SMC) com G1/G2 protegidos, M5.

Hipótese: o gerador atual (trigger+alinhamento) é permissivo demais (~48% base).
O padrão que o usuário opera manualmente é SWEEP de topo/fundo + pavio de
rejeição + reentrada na mesma direção com até 2 gales.

Aqui medimos esse padrão PURO, com e sem filtros (sessão, tendência H1),
e com gales protegidos (reentrada na próxima vela se a anterior falhou mas
deixou pavio de rejeição na direção original).

Saída: win direto, win com G1, win com G2, assertividade combinada, EV em
payout de binárias (0.87) e em R (TP=1R, SL=1R na vela seguinte — estilo M1/M5).
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import pandas as pd
import yfinance as yf

ASSETS = ["GBPUSD=X", "EURUSD=X", "USDJPY=X", "GBPJPY=X",
          "BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD"]
PAYOUT = 0.87
MAX_GALE = 2


def atr14(h, l, c):
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def h1_ema(df):
    h1 = df["Close"].resample("1h").last().dropna()
    return h1.ewm(span=50).mean().reindex(df.index, method="ffill")


def sweep_signal(df, i, swing_lb=20):
    """Retorna +1 (BUY) / -1 (SELL) / 0. Sweep + rejeição na vela i."""
    o, h, l, c = (df[k].astype(float) for k in ("Open", "High", "Low", "Close"))
    hN, lN, oN, cN = float(h.iloc[i]), float(l.iloc[i]), float(o.iloc[i]), float(c.iloc[i])
    rng = hN - lN
    if rng <= 0:
        return 0
    swing_h = float(h.iloc[i - swing_lb:i].max())
    swing_l = float(l.iloc[i - swing_lb:i].min())
    wick_up = (hN - max(oN, cN)) / rng
    wick_dn = (min(oN, cN) - lN) / rng
    if hN > swing_h and cN < swing_h and wick_up >= 0.4 and cN < oN:
        return -1
    if lN < swing_l and cN > swing_l and wick_dn >= 0.4 and cN > oN:
        return 1
    return 0


def rejection_wick(df, i, d):
    """Vela i tem pavio de rejeição >= 40% na direção d? (proteção do gale)"""
    o, h, l, c = (df[k].astype(float) for k in ("Open", "High", "Low", "Close"))
    oN, hN, lN, cN = float(o.iloc[i]), float(h.iloc[i]), float(l.iloc[i]), float(c.iloc[i])
    rng = hN - lN
    if rng <= 0:
        return False
    if d == 1:
        return (min(oN, cN) - lN) / rng >= 0.4
    return (hN - max(oN, cN)) / rng >= 0.4


def run(df, use_session=True, use_h1=False):
    ema = h1_ema(df) if use_h1 else None
    c = df["Close"].astype(float)
    res = {"WIN": 0, "G1": 0, "G2": 0, "LOSS": 0}
    for i in range(120, len(df) - (MAX_GALE + 2)):
        d = sweep_signal(df, i)
        if d == 0:
            continue
        if use_session and not (6 <= df.index[i].hour < 16):
            continue
        if use_h1:
            e = ema.iloc[i]
            if pd.isna(e) or (d == 1 and float(c.iloc[i]) < e) or (d == -1 and float(c.iloc[i]) > e):
                continue
        # entrada na abertura da vela seguinte; vitória = vela fechar a favor
        entry_i = i + 1
        won = False
        for g in range(MAX_GALE + 1):
            j = entry_i + g
            if j >= len(df):
                break
            cj = float(c.iloc[j])
            oj = float(df["Open"].astype(float).iloc[j])
            if (cj - oj) * d > 0:
                res["WIN" if g == 0 else f"G{g}"] += 1
                won = True
                break
            # perdeu a vela: só reentra se houver pavio de rejeição (proteção)
            if g < MAX_GALE and rejection_wick(df, j, d):
                continue
            break
        if not won:
            res["LOSS"] += 1
    return res


def report(tag, res):
    n = sum(res.values())
    if n == 0:
        print(f"  {tag}: sem sinais")
        return
    comb = (res["WIN"] + res["G1"] + res["G2"]) / n
    # EV binárias: stake 1, 2, 4; ganha payout no nível que vencer
    ev = 0.0
    ev += res["WIN"] * PAYOUT
    ev += res["G1"] * (-1 + 2 * PAYOUT)
    ev += res["G2"] * (-1 - 2 + 4 * PAYOUT)
    ev += res["LOSS"] * (-1 - 2 - 4)
    ev /= n
    print(f"  {tag}: n={n} WIN={res['WIN']/n:.1%} G1={res['G1']/n:.1%} "
          f"G2={res['G2']/n:.1%} LOSS={res['LOSS']/n:.1%} "
          f"COMB={comb:.1%} EV={ev:+.3f} stakes")


def main():
    for sym in ASSETS:
        df = yf.download(sym, period="60d", interval="5m", progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [x[0] for x in df.columns]
        if len(df) < 2000:
            print(f"{sym}: dados insuficientes")
            continue
        print(f"== {sym} n={len(df)}")
        report("SWEEP puro      ", run(df, use_session=False, use_h1=False))
        report("SWEEP+SESS      ", run(df, use_session=True, use_h1=False))
        report("SWEEP+SESS+H1   ", run(df, use_session=True, use_h1=True))


if __name__ == "__main__":
    main()
