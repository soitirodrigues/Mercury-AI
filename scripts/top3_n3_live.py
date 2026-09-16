"""Top-3 N3 ao vivo: zonas N>=3 ativas agora + score de confluencia.

Score = toques x win_rate_hist_do_ativo x bonus_rejeicao (pinbar/engolfo=1.2,
so toque=1.0). Win rate historico vem de reports/n3_reversal_result.json
(backtest); sem backtest => usa 50%.
R:R fixo 1:2 (TP_R=2.0). Uso: python scripts/top3_n3_live.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.backtest_n3_reversal import _pivots, _zones, _rejection, _engulf, _atr, ZONE_LOOKBACK, TOUCH_TOL_PCT


def live_scan(symbols=None):
    import yfinance as yf
    import json
    from mercury_ai.config.universe import ALL_SYMBOLS
    wr_hist = {}
    try:
        bt = json.loads(Path("reports/n3_reversal_result.json").read_text(encoding="utf-8"))
        for s, m in bt["per_asset"].items():
            if m.get("n", 0) >= 5:
                wr_hist[s] = m["win_rate"] / 100.0
    except Exception:
        pass
    syms = symbols or list(ALL_SYMBOLS)
    rows = []
    for sym in syms:
        try:
            df = yf.download(sym, period="5d", interval="5m", progress=False, auto_adjust=False)
            if df is None or len(df) < 80:
                continue
            try:
                df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
            except Exception:
                pass
            o = df["Open"].astype(float).tolist()
            h = df["High"].astype(float).tolist()
            lo = df["Low"].astype(float).tolist()
            c = df["Close"].astype(float).tolist()
            win_o, win_h, win_l, win_c = o[-ZONE_LOOKBACK:], h[-ZONE_LOOKBACK:], \
                lo[-ZONE_LOOKBACK:], c[-ZONE_LOOKBACK:]
            tops, bots = _pivots(win_h, win_l)
            atr = _atr(win_h, win_l, win_c)
            if not atr:
                continue
            i = len(win_c) - 1  # vela atual (em formacao: usa como toque potencial)
            for z in _zones(tops, "RES") + _zones(bots, "SUP"):
                lvl = z["level"]
                first = z["touches"][0][0]
                broken = any((cc > lvl * (1 + TOUCH_TOL_PCT)) if z["kind"] == "RES"
                             else (cc < lvl * (1 - TOUCH_TOL_PCT))
                             for cc in win_c[first:])
                if broken:
                    continue
                direction = "VENDA" if z["kind"] == "RES" else "COMPRA"
                px = win_c[-1]
                dist_atr = abs(px - lvl) / atr
                rej = _rejection(win_o[-1], win_h[-1], win_l[-1], win_c[-1],
                                 "SELL" if direction == "VENDA" else "BUY")
                eng = _engulf(win_o[-2], win_c[-2], win_o[-1], win_c[-1],
                              "SELL" if direction == "VENDA" else "BUY")
                wr = wr_hist.get(sym, 0.50)
                bonus = 1.2 if (rej or eng) else 1.0
                score = len(z["touches"]) * wr * bonus * (1.5 if dist_atr <= 0.3 else 1.0)
                rows.append({"ativo": sym, "direcao": direction,
                             "zona": round(lvl, 5), "toques": len(z["touches"]),
                             "wr_hist": round(wr * 100, 1), "rr": "1:2",
                             "score": round(score, 2),
                             "gatilho": "REJEICAO" if (rej or eng) else "TOQUE",
                             "dist_atr": round(dist_atr, 2), "px": round(px, 5)})
        except Exception:
            continue
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows[:3], rows


def main():
    top3, allr = live_scan()
    print(f"zonas ativas: {len(allr)} | Top-3:")
    print("| Ativo | Direcao | Zona | Toques | WR hist | R:R | Score |")
    for r in top3:
        print(f"| {r['ativo']} | {r['direcao']} | {r['zona']} | {r['toques']} | "
              f"{r['wr_hist']}% | {r['rr']} | {r['score']} | ({r['gatilho']}, {r['dist_atr']} ATR)")
    import json
    Path("reports").mkdir(exist_ok=True)
    Path("reports/n3_live_top3.json").write_text(
        json.dumps({"top3": top3, "n_zonas": len(allr)}, ensure_ascii=False, indent=2),
        encoding="utf-8")


if __name__ == "__main__":
    main()
