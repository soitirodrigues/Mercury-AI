"""Backtest Fase 3 — entrada a LIMITE no nível (estilo manual: topo/fundo).

Diferença crucial vs. backtests anteriores: a entrada NÃO é a mercado na
abertura da próxima vela. O sinal coloca uma ordem LIMITE no nível
(topo/fundo do pavio de rejeição ou 50% do pavio) e só entra se o preço
RETORNAR ao nível — replicando o operador manual que "espera o preço
voltar". Win = vela seguinte ao fill fecha a favor do preço de entrada.

Split treino/teste: primeiros 60% dos dados = treino (seleção de config),
últimos 40% = teste (validação honesta, sem overfit).
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import pandas as pd
import yfinance as yf

SYMS = ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD", "BNB-USD"]
PERIOD, INTERVAL = "60d", "5m"


def atr14(h, l, c):
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def run(df, wick_min, sess_filter, limit_mode, trend_ema=None):
    """limit_mode: 'wick50' = limite em 50% do pavio; 'level' = no extremo do swing."""
    o, h, lo, c = df["Open"].astype(float), df["High"].astype(float), df["Low"].astype(float), df["Close"].astype(float)
    atr = atr14(h, lo, c)
    ema = c.ewm(span=trend_ema).mean() if trend_ema else None
    res = {"base": [0, 0], "g1": [0, 0], "g2": [0, 0], "fills": 0, "signals": 0}
    for i in range(60, len(df) - 6):
        a = float(atr.iloc[i])
        if not a > 0:
            continue
        hr = df.index[i].hour
        if sess_filter and not (6 <= hr < 16):
            continue
        swing_h = float(h.iloc[i - 20:i].max())
        swing_l = float(lo.iloc[i - 20:i].min())
        oN, hN, lN, cN = float(o.iloc[i]), float(h.iloc[i]), float(lo.iloc[i]), float(c.iloc[i])
        rng = hN - lN
        if rng <= 0:
            continue
        touch_h = hN >= swing_h - 0.1 * a
        touch_l = lN <= swing_l + 0.1 * a
        wick_up = (hN - max(oN, cN)) / rng
        wick_dn = (min(oN, cN) - lN) / rng
        d = 0
        if touch_h and wick_up >= wick_min and cN < oN:
            d = -1
        elif touch_l and wick_dn >= wick_min and cN > oN:
            d = 1
        if d == 0:
            continue
        if ema is not None:
            e = float(ema.iloc[i])
            if d == -1 and cN > e:
                continue
            if d == 1 and cN < e:
                continue
        res["signals"] += 1
        # Preço limite
        if limit_mode == "wick50":
            limit = (hN + max(oN, cN)) / 2 if d == -1 else (lN + min(oN, cN)) / 2
        else:  # level
            limit = hN if d == -1 else lN
        # Janela de fill: próximas 3 velas; entrada quando o preço toca o limite
        filled = False
        for j in range(i + 1, min(i + 4, len(df) - 2)):
            hj, lj = float(h.iloc[j]), float(lo.iloc[j])
            if d == -1 and hj >= limit:
                filled = True
            elif d == 1 and lj <= limit:
                filled = True
            if filled:
                res["fills"] += 1
                entry = limit
                c1 = float(c.iloc[j])  # fecha a favor do preço limite?
                win = (c1 - entry) * d > 0
                res["base"][0] += win
                res["base"][1] += 1
                if not win and j + 1 < len(df):
                    c2 = float(c.iloc[j + 1])
                    w2 = (c2 - c1) * d > 0
                    res["g1"][0] += w2
                    res["g1"][1] += 1
                    if not w2 and j + 2 < len(df):
                        c3 = float(c.iloc[j + 2])
                        res["g2"][0] += ((c3 - c2) * d > 0)
                        res["g2"][1] += 1
                break
    return res


def metrics(res):
    b, g1, g2 = res["base"], res["g1"], res["g2"]
    if b[1] < 10:
        return None
    p = b[0] / b[1]
    q1 = g1[0] / max(g1[1], 1)
    q2 = g2[0] / max(g2[1], 1)
    comb = p + (1 - p) * q1 + (1 - p) * (1 - q1) * q2
    return p, b[1], q1, q2, comb, res["fills"], res["signals"]


def main():
    configs = [
        (0.4, True, "wick50", None, "wick40+sess+lim50%"),
        (0.4, True, "wick50", 50, "wick40+sess+lim50%+EMA50"),
        (0.4, True, "level", None, "wick40+sess+limNIVEL"),
        (0.5, True, "wick50", 50, "wick50+sess+lim50%+EMA50"),
        (0.3, True, "wick50", 50, "wick30+sess+lim50%+EMA50"),
    ]
    for sym in SYMS:
        df = yf.download(sym, period=PERIOD, interval=INTERVAL, progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c2[0] for c2 in df.columns]
        n = len(df)
        cut = int(n * 0.6)
        df_train, df_test = df.iloc[:cut], df.iloc[cut:]
        print(f"== {sym} (treino n={len(df_train)}, teste n={len(df_test)})")
        for wick, sess, lmode, ema, tag in configs:
            rt = run(df_train, wick, sess, lmode, ema)
            mt = metrics(rt)
            rs = run(df_test, wick, sess, lmode, ema)
            ms = metrics(rs)
            tr = f"base={mt[0]:.1%} n={mt[1]}" if mt else "s/ sinais"
            te = f"base={ms[0]:.1%} n={ms[1]} COMB={ms[4]:.1%} fill={ms[5]}/{ms[6]}" if ms else "s/ sinais"
            print(f"  {tag:28s} TREINO[{tr}]  TESTE[{te}]")


if __name__ == "__main__":
    main()
