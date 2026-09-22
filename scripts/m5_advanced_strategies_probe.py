#!/usr/bin/env python3
"""Probe: Order Block+FVG, Micro-Divergencia RSI, Session VWAP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
    frame.columns = [str(c).lower() for c in frame.columns]
    frame.index = pd.to_datetime(frame.index, utc=True, format="mixed")
    return frame.sort_index()


def evaluate(frame: pd.DataFrame, max_gales: int = 2) -> dict:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    volume = frame["volume"].astype(float).to_numpy() if "volume" in frame.columns else np.ones(n)
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    rsi = (100 - 100 / (1 + gain / loss.replace(0, np.nan))).fillna(50.0).to_numpy()
    # VWAP por sessao (dia)
    dates = frame.index.date
    vwap = np.full(n, np.nan)
    for d in np.unique(dates):
        mask = dates == d
        pv = (closes[mask] * volume[mask]).cumsum()
        vv = volume[mask].cumsum()
        vwap[mask] = pv / np.where(vv > 0, vv, np.nan)
    results = {"ob_fvg": [], "rsi_divergence": [], "vwap_reversal": []}
    for i in range(30, n - (max_gales + 2)):
        if not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0:
            continue
        # ORDER BLOCK + FVG: vela de impulso seguida de FVG, retorno ao OB
        if i >= 3:
            imp_up = closes[i-2] > opens[i-2] and (closes[i-2] - opens[i-2]) > 0.8 * atr[i]
            fvg_up = lows[i] > highs[i-2]
            if imp_up and fvg_up and closes[i] > opens[i]:
                results["ob_fvg"].append((i, "BUY"))
            imp_dn = closes[i-2] < opens[i-2] and (opens[i-2] - closes[i-2]) > 0.8 * atr[i]
            fvg_dn = highs[i] < lows[i-2]
            if imp_dn and fvg_dn and closes[i] < opens[i]:
                results["ob_fvg"].append((i, "SELL"))
        # MICRO-DIVERGENCIA RSI: preco faz novo low mas RSI nao
        if i >= 10:
            price_low = lows[i] < lows[i-5:i].min()
            rsi_higher = rsi[i] > rsi[i-5:i].min()
            if price_low and rsi_higher and closes[i] > opens[i]:
                results["rsi_divergence"].append((i, "BUY"))
            price_high = highs[i] > highs[i-5:i].max()
            rsi_lower = rsi[i] < rsi[i-5:i].max()
            if price_high and rsi_lower and closes[i] < opens[i]:
                results["rsi_divergence"].append((i, "SELL"))
        # VWAP REVERSAL: preco desvia > 1.5 ATR do VWAP e reverte
        if np.isfinite(vwap[i]):
            dev = (closes[i] - vwap[i]) / atr[i]
            if dev < -1.5 and closes[i] > opens[i]:
                results["vwap_reversal"].append((i, "BUY"))
            elif dev > 1.5 and closes[i] < opens[i]:
                results["vwap_reversal"].append((i, "SELL"))
    out = {}
    for name, rows in results.items():
        obs = []
        for i, direction in rows:
            outcomes = []
            for leg in range(1, max_gales + 2):
                entry = opens[i + leg]
                exit_ = closes[i + leg]
                hit = exit_ > entry if direction == "BUY" else exit_ < entry
                outcomes.append(bool(hit))
                if hit:
                    break
            obs.append({"index": int(i), "direction": direction, "outcomes": outcomes, "hit": bool(outcomes[-1])})
        out[name] = obs
    return out


def _metrics(rows: list[dict]) -> dict:
    total = len(rows)
    wins = sum(row["hit"] for row in rows)
    direct = sum(row["outcomes"][0] for row in rows)
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "direct_hit_rate": direct / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe estrategias avancadas M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_advanced_strategies.json")
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    all_results = {"ob_fvg": [], "rsi_divergence": [], "vwap_reversal": []}
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        res = evaluate(_load(path), args.max_gales)
        for name in all_results:
            all_results[name].extend(res[name])
    summary = {}
    for name, rows in all_results.items():
        split = int(len(rows) * 0.8)
        summary[name] = {"train": _metrics(rows[:split]), "test": _metrics(rows[split:])}
    combined = all_results["ob_fvg"] + all_results["rsi_divergence"] + all_results["vwap_reversal"]
    split = int(len(combined) * 0.8)
    summary["combined"] = {"train": _metrics(combined[:split]), "test": _metrics(combined[split:])}
    output = {"schema": "mercury.m5.advanced-strategies.v1", "summary": summary}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
