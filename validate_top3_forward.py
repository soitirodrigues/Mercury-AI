"""Validacao forward do Top-3 real (observavel, sem alterar motor).

Le reports/top3_assertividade_real.json, baixa M5 Yahoo e mede na(s)
vela(s) a partir de next_m5_ts: hit de SL/TP, excursao favoravel/adversa
em ATRs e pips, direcao do close vs entrada. Salva em
reports/top3_forward_validation.json. Uso: 1 scan nao prova taxa.
"""
import json
import sys
from pathlib import Path
from datetime import timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))

SRC = Path("reports/top3_assertividade_real.json")
DST = Path("reports/top3_forward_validation.json")

d = json.loads(SRC.read_text(encoding="utf-8"))
out = {"signals": []}

import yfinance as yf
import pandas as pd


def flat(df):
    try:
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    except Exception:
        pass
    return df


for e in d["top3"]:
    s = e["signal"]
    sym = e["symbol"]
    entry = float(s["entry_price"])
    sl = float(s["stop_loss"]) if s.get("stop_loss") else None
    tp = float(s["take_profit"]) if s.get("take_profit") else None
    dec = (e.get("decision") or "").upper()
    is_buy = dec == "BUY"
    nxt = pd.Timestamp(s["next_m5_ts"])
    if nxt.tzinfo is None:
        nxt = nxt.tz_localize("UTC")
    df = yf.download(sym, period="1d", interval="5m", progress=False, auto_adjust=False)
    rec = {"symbol": sym, "decision": dec, "entry": entry, "sl": sl, "tp": tp,
           "next_m5": s["next_m5_ts"], "candles": []}
    if df is None or len(df) == 0:
        rec["error"] = "no data"
        out["signals"].append(rec)
        continue
    df = flat(df)
    idx = df.index
    # localiza primeira vela >= next_m5 (tol 1min, tz-aware compare em UTC)
    try:
        idx_utc = idx.tz_convert("UTC")
    except Exception:
        idx_utc = idx
    fwd = df[idx_utc >= nxt.tz_convert("UTC")].head(6)
    pip = 0.01 if sym.endswith("JPY=X") else (0.0001 if "=X" in sym else 0.01)
    for ts, row in fwd.iterrows():
        o, h, lo, c = (float(row["Open"]), float(row["High"]),
                       float(row["Low"]), float(row["Close"]))
        if is_buy:
            sl_hit = sl is not None and lo <= sl
            tp_hit = tp is not None and h >= tp
            fav = (h - entry) / pip
            adv = (entry - lo) / pip
            dir_ok = c > entry
        else:
            sl_hit = sl is not None and h >= sl
            tp_hit = tp is not None and lo <= tp
            fav = (entry - lo) / pip
            adv = (h - entry) / pip
            dir_ok = c < entry
        rec["candles"].append({
            "ts": str(ts), "o": round(o, 5), "h": round(h, 5),
            "l": round(lo, 5), "c": round(c, 5),
            "sl_hit": bool(sl_hit), "tp_hit": bool(tp_hit),
            "fav_pips": round(fav, 1), "adv_pips": round(adv, 1),
            "dir_ok": bool(dir_ok),
        })
    if rec["candles"]:
        c0 = rec["candles"][0]
        rec["n1_summary"] = (f"{sym} {dec}: entry {entry} -> "
                             f"O {c0['o']} C {c0['c']} "
                             f"fav {c0['fav_pips']}pips adv {c0['adv_pips']}pips "
                             f"SL {'HIT' if c0['sl_hit'] else 'ok'} / "
                             f"TP {'HIT' if c0['tp_hit'] else 'ok'}")
        print(rec["n1_summary"])
    out["signals"].append(rec)

DST.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("saved", DST)
