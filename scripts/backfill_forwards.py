"""Backfill forwards do historico Top-3 (revalida sinais sem dado).

Rele reports/top3_assertividade_historico.jsonl, baixa M5 Yahoo para
sinais com n1_dir_ok None/fwd_error e preenche n1_*. Salva no lugar
(backup .bak). Uso: python scripts/backfill_forwards.py
"""
import json
from pathlib import Path

HIST = Path("reports/top3_assertividade_historico.jsonl")
BAK = Path("reports/top3_assertividade_historico.jsonl.bak")

lines = HIST.read_text(encoding="utf-8").splitlines()
rows = [json.loads(line) for line in lines if line.strip()]
BAK.write_text("\n".join(lines) + "\n", encoding="utf-8")

import yfinance as yf
import pandas as pd

need = [r for r in rows if r.get("n1_dir_ok") is None]
print(f"sinais: {len(rows)} | a revalidar: {len(need)}")
fixed = 0
for r in need:
    try:
        df = yf.download(r["symbol"], period="1d", interval="5m",
                         progress=False, auto_adjust=False)
        if df is None or len(df) == 0:
            r["fwd_error"] = "no data (backfill)"
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
        fwd = df[idx >= nxt].head(1)
        if len(fwd) == 0:
            r["fwd_error"] = "candle N+1 ainda nao existe"
            continue
        is_buy = str(r["decision"]).upper() == "BUY"
        pip = 0.01 if str(r["symbol"]).endswith("JPY=X") else 0.0001
        entry = float(r["entry"])
        c0 = fwd.iloc[0]
        c = float(c0["Close"])
        r["n1_close"] = round(c, 5)
        r["n1_dir_ok"] = bool(c > entry) if is_buy else bool(c < entry)
        r["n1_fav_pips"] = round(((float(c0["High"]) - entry) / pip if is_buy
                                  else (entry - float(c0["Low"])) / pip), 1)
        r.pop("fwd_error", None)
        fixed += 1
    except Exception as e:
        r["fwd_error"] = str(e)[:200]

HIST.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                encoding="utf-8")
print(f"backfill: {fixed}/{len(need)} recuperados -> {HIST} (backup {BAK})")
