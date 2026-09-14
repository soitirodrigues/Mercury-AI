"""Mede edge N+1 de S/R + EMA21 (walk-forward, sem lookahead).

Regras testadas (mesma matematica do motor):
  SR: SupportResistanceAnalyzer (pivot 5, cluster 0.3 ATR) sobre df[:i+1];
      AT_SUPPORT (dist<0.3 ATR) => espera up; AT_RESISTANCE => espera down.
  EMA21: close vs EMA21 (só fechadas); acima => up, abaixo => down.
  COMBO: S/R a favor + lado EMA21 a favor (confluencia horizontal+dinamica).
  COMBO+FORCA: combo + corpo trigger >=0.40 range (corta micro-range).
Mede vela i+1 (close vs open). Uso: python scripts/measure_sr_ema21_edge.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SYMBOLS = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "EURJPY=X", "GBPJPY=X",
           "AUDUSD=X", "USDCAD=X", "EURGBP=X", "BTC-USD", "ETH-USD"]
N_BARS = 400


def main():
    import yfinance as yf
    from mercury_ai.analysis.support_resistance_analyzer import SupportResistanceAnalyzer
    sr = SupportResistanceAnalyzer()
    tot = [0, 0]
    at_s = [0, 0]
    at_r = [0, 0]
    e_up = [0, 0]
    e_dn = [0, 0]
    combo = [0, 0]
    combo_f = [0, 0]
    per = {}
    for sym in SYMBOLS:
        df = yf.download(sym, period="5d", interval="5m", progress=False, auto_adjust=False)
        if df is None or len(df) < 80:
            print(f"{sym}: sem dados")
            continue
        try:
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        except Exception:
            pass
        s = {"n": 0, "sr": 0, "sr_ok": 0, "ema": 0, "ema_ok": 0, "combo": 0, "combo_ok": 0}
        lo = max(61, len(df) - N_BARS - 1)
        for i in range(lo, len(df) - 1):
            past = df.iloc[:i + 1]
            nxt = df.iloc[i + 1]
            try:
                o1, c1 = float(nxt["Open"]), float(nxt["Close"])
                h1, l1 = float(nxt["High"]), float(nxt["Low"])
            except Exception:
                continue
            if c1 == o1:
                continue
            up = c1 > o1
            tot[0] += 1
            tot[1] += up
            s["n"] += 1
            # S/R (mesma engine do motor)
            try:
                res = sr.analyze(past)
            except Exception:
                continue
            loc = sr._detect_price_location(
                float(past["Close"].iloc[-1]),
                {"center": res.support} if res.support else None,
                {"center": res.resistance} if res.resistance else None,
                float(past["Close"].rolling(14).std().iloc[-1] or 0) or None,
            ) if False else None
            # localizacao manual (evita ATR interno instavel em slice curto)
            try:
                import pandas as _pd
                tr = (past["High"] - past["Low"]).abs()
                atr = float(tr.rolling(14).mean().iloc[-1])
                px = float(past["Close"].iloc[-1])
            except Exception:
                continue
            if not atr or atr <= 0:
                continue
            at_sup = res.support and abs(px - res.support) < 0.3 * atr
            at_res = res.resistance and abs(px - res.resistance) < 0.3 * atr
            sr_dir = "UP" if at_sup and not at_res else ("DOWN" if at_res and not at_sup else None)
            if at_sup:
                at_s[0] += 1
                at_s[1] += up
            if at_res:
                at_r[0] += 1
                at_r[1] += (not up)
            if sr_dir:
                s["sr"] += 1
                s["sr_ok"] += (up if sr_dir == "UP" else (not up))
            # EMA21
            try:
                ema21 = float(past["Close"].ewm(span=21, adjust=False).mean().iloc[-1])
            except Exception:
                continue
            ema_dir = "UP" if px > ema21 else ("DOWN" if px < ema21 else None)
            if ema_dir == "UP":
                e_up[0] += 1
                e_up[1] += up
            elif ema_dir == "DOWN":
                e_dn[0] += 1
                e_dn[1] += (not up)
            if ema_dir:
                s["ema"] += 1
                s["ema_ok"] += (up if ema_dir == "UP" else (not up))
            # Combo
            if sr_dir and ema_dir and sr_dir == ema_dir:
                combo[0] += 1
                ok = up if sr_dir == "UP" else (not up)
                combo[1] += ok
                s["combo"] += 1
                s["combo_ok"] += ok
                rng = h1 - l1 if False else None  # corpo medido na trigger (past)
                try:
                    r0 = past.iloc[-1]
                    body = abs(float(r0["Close"]) - float(r0["Open"]))
                    rng0 = float(r0["High"]) - float(r0["Low"])
                    strong = rng0 > 0 and body / rng0 >= 0.40
                except Exception:
                    strong = False
                if strong:
                    combo_f[0] += 1
                    combo_f[1] += ok
        per[sym] = s

    def pct(a, b):
        return f"{100.0 * a / b:.1f}%" if b else "n/a"
    print(f"base UP: {pct(tot[1], tot[0])} (n={tot[0]})")
    print(f"AT_SUPPORT -> up: {pct(at_s[1], at_s[0])} (n={at_s[0]})")
    print(f"AT_RESISTANCE -> down: {pct(at_r[1], at_r[0])} (n={at_r[0]})")
    print(f"EMA21 acima -> up: {pct(e_up[1], e_up[0])} (n={e_up[0]})")
    print(f"EMA21 abaixo -> down: {pct(e_dn[1], e_dn[0])} (n={e_dn[0]})")
    print(f"COMBO S/R+EMA21 -> dir: {pct(combo[1], combo[0])} (n={combo[0]})")
    print(f"COMBO+FORCA corpo>=0.40 -> dir: {pct(combo_f[1], combo_f[0])} (n={combo_f[0]})")
    print("--- por simbolo (n, sr, ema, combo) ---")
    for sym, s in per.items():
        print(f"{sym}: n={s['n']} sr={pct(s['sr_ok'], s['sr'])}(n={s['sr']}) "
              f"ema={pct(s['ema_ok'], s['ema'])}(n={s['ema']}) "
              f"combo={pct(s['combo_ok'], s['combo'])}(n={s['combo']})")


if __name__ == "__main__":
    main()
