"""Walk-forward direcional BUY vs SELL (fecha a auditoria do lado vendido).

Para cada vela fechada i (10 ativos M5): calcula smc_flags para BUY e SELL
sobre o MESMO passado e mede a vela i+1. Pergunta: dado que o flag alinhou
(has_sweep=True p/ BUY), a vela seguinte sobe? E o espelho SELL?
Se BUY_ok >> SELL_ok com n grande => assimetria real no mercado ou no flag.
Se ambos ~50% => o problema do n=54 esta na SELECAO (Top-3/gates), nao no detector.
Uso: python scripts/audit_sell_side.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SYMBOLS = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "EURJPY=X", "GBPJPY=X",
           "AUDUSD=X", "USDCAD=X", "EURGBP=X", "BTC-USD", "ETH-USD"]
N_BARS = 400


def main():
    import yfinance as yf
    from mercury_ai.signals.m5_institutional_filters import smc_flags
    agg = {k: [0, 0] for k in
           ["sweep_BUY", "sweep_SELL", "fvg_BUY", "fvg_SELL", "idm", "zona_BUY", "zona_SELL"]}
    for sym in SYMBOLS:
        df = yf.download(sym, period="5d", interval="5m", progress=False, auto_adjust=False)
        if df is None or len(df) < 80:
            print(f"{sym}: sem dados")
            continue
        try:
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        except Exception:
            pass
        lo = max(16, len(df) - N_BARS - 1)
        for i in range(lo, len(df) - 1):
            past = df.iloc[:i + 1]
            nxt = df.iloc[i + 1]
            try:
                o1, c1 = float(nxt["Open"]), float(nxt["Close"])
            except Exception:
                continue
            if c1 == o1:
                continue
            up = c1 > o1
            try:
                fb = smc_flags(past, "BUY")
                fs = smc_flags(past, "SELL")
            except Exception:
                continue
            pairs = [("sweep_BUY", fb.get("has_liquidity_sweep"), up),
                     ("sweep_SELL", fs.get("has_liquidity_sweep"), not up),
                     ("fvg_BUY", fb.get("has_fvg"), up),
                     ("fvg_SELL", fs.get("has_fvg"), not up),
                     ("zona_BUY", fb.get("in_premium_discount_zone"), up),
                     ("zona_SELL", fs.get("in_premium_discount_zone"), not up)]
            for k, flag, ok in pairs:
                if flag is True:
                    agg[k][0] += 1
                    agg[k][1] += ok
            if fb.get("has_inducement"):
                agg["idm"][0] += 1
                agg["idm"][1] += up
    for k, (n, ok) in agg.items():
        print(f"{k}: {ok}/{n}={100.0 * ok / n:.1f}%" if n else f"{k}: n=0")


if __name__ == "__main__":
    main()
