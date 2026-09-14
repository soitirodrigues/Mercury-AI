"""Acumulador de assertividade Top-3 (observavel, sem alterar motor).

Cada execucao: roda scan real 39 ativos (workers=4), filtra Top-3,
valida forward N+1..N+4 via Yahoo e ACUMULA em
reports/top3_assertividade_historico.jsonl (1 linha por sinal).
Com 50-100 sinais: taxa direcional, hit SL/TP, por estrutura/LTA/noticia.
Uso: python scripts/accumulate_top3.py [--cycles N] [--workers 4]
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

HIST = Path("reports/top3_assertividade_historico.jsonl")


def one_cycle(workers=4):
    from mercury_ai.brain.scanner import MercuryScanner
    from mercury_ai.signals.top3_selector import select_top3, setup_label
    sc = MercuryScanner()
    ranked = sc.scan(workers=workers, cycle_timeout_s=290.0)
    d = sc.last_scan_report.to_dict()
    top3 = select_top3(d)
    rows = []
    for e in top3:
        s = e.get("signal", {}) or {}
        rows.append({
            "ts": s.get("signal_ts"), "scan_id": d.get("scan_id"),
            "symbol": e.get("symbol"), "decision": e.get("decision"),
            "score": e.get("score"), "rr": s.get("risk_reward"),
            "forward": s.get("forward_state"),
            "next_structure": s.get("next_structure"),
            "next_agrees": s.get("next_agrees"),
            "trendline_bias": s.get("trendline_bias"),
            "trendline_aligned": s.get("trendline_aligned"),
            "sweep": s.get("has_liquidity_sweep"), "fvg": s.get("has_fvg"),
            "idm": s.get("has_inducement"),
            "news": s.get("news_risk"),
            "entry": s.get("entry_price"), "sl": s.get("stop_loss"),
            "tp": s.get("take_profit"), "next_m5": s.get("next_m5_ts"),
            "label": setup_label(e),
        })
    return d, rows


def validate_forward(rows):
    import yfinance as yf
    import pandas as pd
    for r in rows:
        try:
            df = yf.download(r["symbol"], period="1d", interval="5m",
                             progress=False, auto_adjust=False)
            if df is None or len(df) == 0:
                r["fwd_error"] = "no data"
                continue
            try:
                df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
            except Exception:
                pass
            nxt = pd.Timestamp(r["next_m5"])
            if nxt.tzinfo is None:
                nxt = nxt.tz_localize("UTC")
            try:
                idx = df.index.tz_convert("UTC")
            except Exception:
                idx = df.index
            fwd = df[idx >= nxt].head(4)
            is_buy = str(r["decision"]).upper() == "BUY"
            pip = 0.01 if str(r["symbol"]).endswith("JPY=X") else 0.0001
            entry = float(r["entry"])
            c0 = fwd.iloc[0]
            c = float(c0["Close"])
            r["n1_close"] = round(c, 5)
            r["n1_dir_ok"] = bool(c > entry) if is_buy else bool(c < entry)
            r["n1_fav_pips"] = round(((float(c0["High"]) - entry) / pip if is_buy
                                      else (entry - float(c0["Low"])) / pip), 1)
        except Exception as e:
            r["fwd_error"] = str(e)[:200]
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycles", type=int, default=1)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--sleep-s", type=float, default=300.0)
    a = ap.parse_args()
    HIST.parent.mkdir(exist_ok=True)
    for i in range(a.cycles):
        t0 = time.perf_counter()
        d, rows = one_cycle(a.workers)
        rows = validate_forward(rows)
        with open(HIST, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"cycle {i+1}/{a.cycles}: scan={d['status']} "
              f"{d['symbols_completed']}/{d['symbols_total']} "
              f"top3={len(rows)} dir_ok={[r.get('n1_dir_ok') for r in rows]} "
              f"({time.perf_counter()-t0:.0f}s) -> {HIST}")
        if i < a.cycles - 1:
            time.sleep(a.sleep_s)


if __name__ == "__main__":
    main()
