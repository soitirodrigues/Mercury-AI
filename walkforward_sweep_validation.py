"""Walk-forward contínuo do padrão sweep+rejeição — revalidação do edge.

Regra de governança (Fase 4):
  - Roda janelas deslizantes de 30d sobre os dados disponíveis.
  - Ativo fica VALIDATED se base >= 52% na janela mais recente com n >= 30.
  - Se base < 52% por 2 janelas seguidas -> REMOVER da whitelist (alerta).
  - Saída: tabela por ativo/janela + veredito final por ativo.

Uso: python walkforward_sweep_validation.py
"""
import sys
sys.path.insert(0, r"C:\Projetos\Mercury-AI")
import yfinance as yf

from mercury_ai.signals.liquidity_sweep_engine import (
    REJECTION_WICK_MIN, SESSION_END_UTC, SESSION_START_UTC, SWING_LOOKBACK)

ASSETS = ["GBPUSD=X", "GBPJPY=X", "EURUSD=X", "USDJPY=X",
          "BTC-USD", "ETH-USD", "XRP-USD"]
MIN_BASE = 0.52
MIN_N = 30


def atr14(h, l, c):
    import pandas as pd
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def base_winrate(df):
    o, h, l, c = df["Open"].astype(float), df["High"].astype(float), df["Low"].astype(float), df["Close"].astype(float)
    atr = atr14(h, l, c)
    wins = total = 0
    for i in range(SWING_LOOKBACK + 40, len(df) - 2):
        a = float(atr.iloc[i])
        if not a > 0:
            continue
        hr = df.index[i].hour
        if not (SESSION_START_UTC <= hr < SESSION_END_UTC):
            continue
        swing_h = float(h.iloc[i - SWING_LOOKBACK:i].max())
        swing_l = float(l.iloc[i - SWING_LOOKBACK:i].min())
        oN, hN, lN, cN = float(o.iloc[i]), float(h.iloc[i]), float(l.iloc[i]), float(c.iloc[i])
        rng = hN - lN
        if rng <= 0:
            continue
        wick_up = (hN - max(oN, cN)) / rng
        wick_dn = (min(oN, cN) - lN) / rng
        d = 0
        if hN > swing_h and cN < swing_h and wick_up >= REJECTION_WICK_MIN and cN < oN:
            d = -1
        elif lN < swing_l and cN > swing_l and wick_dn >= REJECTION_WICK_MIN and cN > oN:
            d = 1
        if d == 0:
            continue
        c1 = float(c.iloc[i + 1])
        wins += (c1 - cN) * d > 0
        total += 1
    return wins, total


def main():
    print("Walk-forward sweep+rejeição (janelas de ~30d sobre 60d)")
    print(f"Regra: VALIDATED se base >= {MIN_BASE:.0%} com n >= {MIN_N}\n")
    for sym in ASSETS:
        df = yf.download(sym, period="60d", interval="5m", progress=False, auto_adjust=True)
        if isinstance(df.columns, __import__("pandas").MultiIndex):
            df.columns = [c2[0] for c2 in df.columns]
        if len(df) < 4000:
            print(f"{sym}: dados insuficientes ({len(df)})")
            continue
        half = len(df) // 2
        w1, n1 = base_winrate(df.iloc[:half])
        w2, n2 = base_winrate(df.iloc[half:])
        p1 = w1 / n1 if n1 else 0.0
        p2 = w2 / n2 if n2 else 0.0
        ok1 = p1 >= MIN_BASE and n1 >= MIN_N
        ok2 = p2 >= MIN_BASE and n2 >= MIN_N
        if ok1 and ok2:
            verdict = "VALIDATED"
        elif not ok1 and not ok2:
            verdict = "REMOVER (2 janelas abaixo)"
        else:
            verdict = "OBSERVAR (1 janela abaixo)"
        print(f"{sym}: J1={p1:.1%} (n={n1}) {'OK' if ok1 else 'X'} | "
              f"J2={p2:.1%} (n={n2}) {'OK' if ok2 else 'X'} -> {verdict}")


if __name__ == "__main__":
    main()
