"""Mede edge direcional N+1 de LTA/LTB + estrutura topos/fundos (walk-forward, sem lookahead).

Para cada simbolo: baixa M5 Yahoo (5d), percorre as ultimas ~400 velas
fechadas; em cada i calcula sobre df[:i+1] (so passado):
  - estrutura do next_candle_predictor (UP/DOWN/RANGE)
  - trendlines() bias + trendline_flags alinhamento p/ BUY e p/ SELL
Depois mede a vela i+1: up se close>open.
Taxas: P(up|bias BULLISH), P(down|bias BEARISH), P(up|UP), P(down|DOWN),
P(up|LTA aligned BUY), acordo estrutura x diagonal.
Uso: python scripts/measure_trendline_edge.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SYMBOLS = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "EURJPY=X", "GBPJPY=X",
           "AUDUSD=X", "USDCAD=X", "EURGBP=X", "BTC-USD", "ETH-USD"]
N_BARS = 400

from mercury_ai.signals.next_candle_predictor import predict_next_candle
from mercury_ai.signals.trendlines import trendlines, trendline_flags


def main():
    import yfinance as yf
    tot = {"n": 0, "up": 0}
    bull = {"n": 0, "up": 0}
    bear = {"n": 0, "down": 0}
    s_up = {"n": 0, "up": 0}
    s_dn = {"n": 0, "down": 0}
    lta_buy = {"n": 0, "up": 0}
    ltb_sell = {"n": 0, "down": 0}
    agree = {"n_struct": 0, "agree": 0}
    per_sym = {}
    for sym in SYMBOLS:
        df = yf.download(sym, period="5d", interval="5m", progress=False, auto_adjust=False)
        if df is None or len(df) < 80:
            print(f"{sym}: sem dados ({0 if df is None else len(df)})")
            continue
        try:
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        except Exception:
            pass
        lo = max(61, len(df) - N_BARS - 1)
        s = {"n": 0, "up": 0, "bull_up": 0, "bull_n": 0, "bear_dn": 0, "bear_n": 0,
             "lta_up": 0, "lta_n": 0, "ltb_dn": 0, "ltb_n": 0}
        for i in range(lo, len(df) - 1):
            past = df.iloc[:i + 1]
            nxt = df.iloc[i + 1]
            try:
                o1, c1 = float(nxt["Open"]), float(nxt["Close"])
            except Exception:
                continue
            if c1 == o1:
                continue
            is_up = c1 > o1
            tot["n"] += 1
            tot["up"] += is_up
            s["n"] += 1
            s["up"] += is_up
            try:
                pred = predict_next_candle(past)
                tl = trendlines(past)
            except Exception:
                continue
            struct = pred.get("structure")
            bias = tl.get("bias")
            if bias == "BULLISH":
                bull["n"] += 1
                bull["up"] += is_up
                s["bull_n"] += 1
                s["bull_up"] += is_up
            elif bias == "BEARISH":
                bear["n"] += 1
                bear["down"] += (not is_up)
                s["bear_n"] += 1
                s["bear_dn"] += (not is_up)
            if struct == "UP":
                s_up["n"] += 1
                s_up["up"] += is_up
            elif struct == "DOWN":
                s_dn["n"] += 1
                s_dn["down"] += (not is_up)
            if struct in ("UP", "DOWN"):
                agree["n_struct"] += 1
                want = "BULLISH" if struct == "UP" else "BEARISH"
                if bias == want:
                    agree["agree"] += 1
            try:
                fb = trendline_flags(past, "BUY")
                fs = trendline_flags(past, "SELL")
            except Exception:
                fb, fs = {}, {}
            if fb.get("trendline_aligned") is True:
                lta_buy["n"] += 1
                lta_buy["up"] += is_up
                s["lta_n"] += 1
                s["lta_up"] += is_up
            if fs.get("trendline_aligned") is True:
                ltb_sell["n"] += 1
                ltb_sell["down"] += (not is_up)
                s["ltb_n"] += 1
                s["ltb_dn"] += (not is_up)
        per_sym[sym] = s

    def pct(a, b):
        return f"{100.0 * a / b:.1f}%" if b else "n/a"
    print(f"base UP: {pct(tot['up'], tot['n'])} (n={tot['n']})")
    print(f"LTA/LTB bias BULLISH -> up: {pct(bull['up'], bull['n'])} (n={bull['n']})")
    print(f"LTA/LTB bias BEARISH -> down: {pct(bear['down'], bear['n'])} (n={bear['n']})")
    print(f"estrutura UP -> up: {pct(s_up['up'], s_up['n'])} (n={s_up['n']})")
    print(f"estrutura DOWN -> down: {pct(s_dn['down'], s_dn['n'])} (n={s_dn['n']})")
    print(f"LTA aligned BUY -> up: {pct(lta_buy['up'], lta_buy['n'])} (n={lta_buy['n']})")
    print(f"LTB aligned SELL -> down: {pct(ltb_sell['down'], ltb_sell['n'])} (n={ltb_sell['n']})")
    print(f"acordo estrutura x diagonal: {pct(agree['agree'], agree['n_struct'])} (n={agree['n_struct']})")
    print("--- por simbolo (n, baseUP, bull->up, bear->down, LTA->up, LTB->down) ---")
    for sym, s in per_sym.items():
        print(f"{sym}: n={s['n']} base={pct(s['up'], s['n'])} "
              f"bull={pct(s['bull_up'], s['bull_n'])}(n={s['bull_n']}) "
              f"bear={pct(s['bear_dn'], s['bear_n'])}(n={s['bear_n']}) "
              f"LTA={pct(s['lta_up'], s['lta_n'])}(n={s['lta_n']}) "
              f"LTB={pct(s['ltb_dn'], s['ltb_n'])}(n={s['ltb_n']})")


if __name__ == "__main__":
    main()
