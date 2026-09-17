"""Varredura completa de confluências — camada por camada, M5 e M1.

Objetivo: encontrar a combinação que eleva a BASE (sem gale) acima de 52%,
idealmente rumo a 70%+, medindo o delta de cada camada separadamente.

Camadas (cumulativas):
  L0 sweep+rejeição (base SMC)
  L1 + sessão (06-16 UTC)
  L2 + FVG aberto a favor (gap >= 0.2*ATR não preenchido)
  L3 + tendência H1 a favor (EMA50 do H1 via resample)
  L4 + volatilidade mínima (ATR >= mediana móvel — evita mercado morto)
  L5 + corpo da vela de sweep >= 30% do range (convicção na reversão)

Saída: base win rate + n por camada, por ativo, em M5 (60d) e M1 (7d).
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import pandas as pd
import yfinance as yf

ASSETS_M5 = ["GBPUSD=X", "ETH-USD", "GBPJPY=X", "USDJPY=X", "XRP-USD"]
ASSETS_M1 = ["GBPUSD=X", "ETH-USD"]


def atr14(h, l, c):
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def h1_trend(df):
    """EMA50 do H1 (resample) reindexada para o timeframe original."""
    h1 = df["Close"].resample("1h").last().dropna()
    ema = h1.ewm(span=50).mean()
    return ema.reindex(df.index, method="ffill")


def has_fvg(df, i, d, atr_val):
    """FVG clássico de 3 velas a favor, nas últimas 8 velas (existência).

    Bullish FVG em k: low[k] > high[k-2]. Bearish: high[k] < low[k-2].
    Critério relaxado: basta o gap existir com tamanho >= 0.2*ATR —
    não exige "não preenchido" (reversões frequentemente preenchem).
    """
    h, l = df["High"].astype(float), df["Low"].astype(float)
    for k in range(max(2, i - 8), i + 1):
        if d == 1 and float(l.iloc[k]) - float(h.iloc[k - 2]) >= 0.2 * atr_val:
            return True
        if d == -1 and float(l.iloc[k - 2]) - float(h.iloc[k]) >= 0.2 * atr_val:
            return True
    return False


def run_layers(df, swing_lb=20):
    o = df["Open"].astype(float)
    h, l, c = df["High"].astype(float), df["Low"].astype(float), df["Close"].astype(float)
    atr = atr14(h, l, c)
    atr_med = atr.rolling(100).median()
    ema_h1 = h1_trend(df)
    layers = {k: [0, 0] for k in ["L0", "L1", "L2", "L3", "L4", "L5"]}
    for i in range(120, len(df) - 2):
        a = float(atr.iloc[i])
        if not a > 0:
            continue
        swing_h = float(h.iloc[i - swing_lb:i].max())
        swing_l = float(l.iloc[i - swing_lb:i].min())
        oN, hN, lN, cN = float(o.iloc[i]), float(h.iloc[i]), float(l.iloc[i]), float(c.iloc[i])
        rng = hN - lN
        if rng <= 0:
            continue
        wick_up = (hN - max(oN, cN)) / rng
        wick_dn = (min(oN, cN) - lN) / rng
        d = 0
        if hN > swing_h and cN < swing_h and wick_up >= 0.4 and cN < oN:
            d = -1
        elif lN < swing_l and cN > swing_l and wick_dn >= 0.4 and cN > oN:
            d = 1
        if d == 0:
            continue
        c1 = float(c.iloc[i + 1])
        win = (c1 - cN) * d > 0
        # L0: sweep puro
        layers["L0"][0] += win; layers["L0"][1] += 1
        # L1: + sessão
        hr = df.index[i].hour
        if not (6 <= hr < 16):
            continue
        layers["L1"][0] += win; layers["L1"][1] += 1
        # L2: + FVG a favor
        if not has_fvg(df, i, d, a):
            continue
        layers["L2"][0] += win; layers["L2"][1] += 1
        # L3: + tendência H1
        e = ema_h1.iloc[i]
        if pd.isna(e) or (d == 1 and cN < e) or (d == -1 and cN > e):
            continue
        layers["L3"][0] += win; layers["L3"][1] += 1
        # L4: + volatilidade mínima
        am = atr_med.iloc[i]
        if pd.isna(am) or a < am:
            continue
        layers["L4"][0] += win; layers["L4"][1] += 1
        # L5: + corpo com convicção
        if abs(cN - oN) < 0.3 * rng:
            continue
        layers["L5"][0] += win; layers["L5"][1] += 1
    return layers


def show(sym, tf, layers):
    print(f"-- {sym} {tf}")
    for k in ["L0", "L1", "L2", "L3", "L4", "L5"]:
        w, n = layers[k]
        if n >= 5:
            print(f"   {k}: base={w/n:.1%} (n={n})")
        else:
            print(f"   {k}: n={n} (insuficiente)")


def main():
    print("=" * 50)
    print("M5 — 60 dias")
    print("=" * 50)
    for sym in ASSETS_M5:
        df = yf.download(sym, period="60d", interval="5m", progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c2[0] for c2 in df.columns]
        if len(df) < 2000:
            print(f"{sym}: dados insuficientes")
            continue
        show(sym, "M5", run_layers(df))
    print("=" * 50)
    print("M1 — 7 dias (limite do provedor)")
    print("=" * 50)
    for sym in ASSETS_M1:
        df = yf.download(sym, period="7d", interval="1m", progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c2[0] for c2 in df.columns]
        if len(df) < 2000:
            print(f"{sym}: dados insuficientes")
            continue
        show(sym, "M1", run_layers(df, swing_lb=20))


if __name__ == "__main__":
    main()
