"""Backfill: aplica feedback de reentrada (G1/G2) ao histórico existente.

Lê reports/top3_assertividade_historico.jsonl, baixa as velas N+1..N+4 de
cada sinal (mesma janela do validate_forward) e grava
reports/top3_assertividade_historico_fb.jsonl com reentry_result/resultado.
Não altera o arquivo original.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SRC = Path("reports/top3_assertividade_historico.jsonl")
DST = Path("reports/top3_assertividade_historico_fb.jsonl")


def main():
    import pandas as pd
    import yfinance as yf
    from mercury_ai.signals.reentry_engine import signal_feedback

    rows = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
    cache = {}
    out = []
    for r in rows:
        sym = r["symbol"]
        try:
            if sym not in cache:
                df = yf.download(sym, period="5d", interval="5m", progress=False, auto_adjust=False)
                if df is not None and len(df):
                    try:
                        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
                    except Exception:
                        pass
                cache[sym] = df
            df = cache[sym]
            if df is None or len(df) == 0:
                r["fwd_error"] = "no data"
                out.append(r)
                continue
            nxt = pd.Timestamp(r["next_m5"])
            if nxt.tzinfo is None:
                nxt = nxt.tz_localize("UTC")
            try:
                idx = df.index.tz_convert("UTC")
            except Exception:
                idx = df.index
            fwd = df[idx >= nxt].head(4)
            if len(fwd) == 0:
                r["fwd_error"] = "no fwd candles"
                out.append(r)
                continue
            fb = signal_feedback(fwd, r["decision"], 0)
            r["reentry_result"] = fb["result"]
            r["reentry_gales_used"] = fb["gales_used"]
            r["reentry_reason"] = fb["reason"]
            r["reentry_attempts"] = fb["attempts"]
            r["resultado"] = "GANHO" if fb["result"] in ("WIN", "REENTRY_G1", "REENTRY_G2") else "PERDA"
        except Exception as e:
            r["fwd_error"] = str(e)[:200]
        out.append(r)

    with open(DST, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    res = {}
    for r in out:
        k = r.get("reentry_result")
        if k:
            res[k] = res.get(k, 0) + 1
    n = sum(res.values())
    print(f"gravado {DST} ({len(out)} linhas, {n} com feedback)")
    if n:
        comb = (res.get("WIN", 0) + res.get("REENTRY_G1", 0) + res.get("REENTRY_G2", 0)) / n
        print(f"WIN={res.get('WIN',0)/n:.1%} G1={res.get('REENTRY_G1',0)/n:.1%} "
              f"G2={res.get('REENTRY_G2',0)/n:.1%} LOSS={res.get('LOSS_FINAL',0)/n:.1%}")
        print(f"ASSERTIVIDADE COMBINADA: {comb:.1%}")


if __name__ == "__main__":
    main()
