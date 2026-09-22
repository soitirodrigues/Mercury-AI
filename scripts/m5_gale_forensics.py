#!/usr/bin/env python3
"""Gale Forensics: analisa G0 losers e recuperacao G1/G2."""
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


def evaluate(frame: pd.DataFrame, max_gales: int = 2) -> pd.DataFrame:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    # Zonas de toque de corpo
    lookback, tolerance = 60, 0.0005
    zone_sup = np.full(n, np.nan)
    zone_res = np.full(n, np.nan)
    for i in range(lookback, n):
        bodies = np.concatenate([opens[i - lookback:i], closes[i - lookback:i]])
        sorted_b = np.sort(bodies)
        clusters = []
        cluster = [sorted_b[0]]
        for price in sorted_b[1:]:
            if abs(price - cluster[-1]) / cluster[-1] <= tolerance:
                cluster.append(price)
            else:
                if len(cluster) >= 2:
                    clusters.append(float(np.mean(cluster)))
                cluster = [price]
        if len(cluster) >= 2:
            clusters.append(float(np.mean(cluster)))
        current = closes[i]
        sup = [z for z in clusters if z < current]
        res = [z for z in clusters if z > current]
        if sup:
            zone_sup[i] = max(sup)
        if res:
            zone_res[i] = min(res)
    rows = []
    for i in range(lookback, n - (max_gales + 2)):
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0 or not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        upper = highs[i] - max(opens[i], closes[i])
        lower = min(opens[i], closes[i]) - lows[i]
        direction = None
        if np.isfinite(zone_res[i]) and (abs(closes[i] - zone_res[i]) / zone_res[i] <= 0.001 or highs[i] >= zone_res[i] * 0.9995):
            if closes[i] < opens[i] and upper >= 1.2 * body:
                direction = "SELL"
        if direction is None and np.isfinite(zone_sup[i]) and (abs(closes[i] - zone_sup[i]) / zone_sup[i] <= 0.001 or lows[i] <= zone_sup[i] * 1.0005):
            if closes[i] > opens[i] and lower >= 1.2 * body:
                direction = "BUY"
        if direction is None:
            continue
        # Medir G0, G1, G2 com MAE/MFE
        legs = []
        for leg in range(1, max_gales + 2):
            entry = opens[i + leg]
            exit_ = closes[i + leg]
            hit = exit_ > entry if direction == "BUY" else exit_ < entry
            # MAE/MFE durante a vela
            if direction == "BUY":
                mae = (lows[i + leg] - entry) / entry
                mfe = (highs[i + leg] - entry) / entry
            else:
                mae = (entry - highs[i + leg]) / entry
                mfe = (entry - lows[i + leg]) / entry
            legs.append({"leg": leg, "hit": bool(hit), "mae": float(mae), "mfe": float(mfe)})
            if hit:
                break
        rows.append({
            "index": i,
            "direction": direction,
            "g0_hit": legs[0]["hit"],
            "g1_hit": legs[1]["hit"] if len(legs) > 1 else None,
            "g2_hit": legs[2]["hit"] if len(legs) > 2 else None,
            "final_hit": legs[-1]["hit"],
            "g0_mae": legs[0]["mae"],
            "g0_mfe": legs[0]["mfe"],
            "g1_mae": legs[1]["mae"] if len(legs) > 1 else None,
            "g1_mfe": legs[1]["mfe"] if len(legs) > 1 else None,
            "g2_mae": legs[2]["mae"] if len(legs) > 2 else None,
            "g2_mfe": legs[2]["mfe"] if len(legs) > 2 else None,
            "legs_used": len(legs),
        })
    return pd.DataFrame(rows)


def _metrics(df: pd.DataFrame) -> dict:
    total = len(df)
    g0_wins = int(df["g0_hit"].sum())
    g0_losses = total - g0_wins
    g1_wins = int(df["g1_hit"].sum()) if "g1_hit" in df else 0
    g2_wins = int(df["g2_hit"].sum()) if "g2_hit" in df else 0
    final_wins = int(df["final_hit"].sum())
    return {
        "total": total,
        "g0_win_rate": g0_wins / total if total else None,
        "g0_loss_rate": g0_losses / total if total else None,
        "g1_win_rate": g1_wins / g0_losses if g0_losses else None,
        "g2_win_rate": g2_wins / (g0_losses - g1_wins) if (g0_losses - g1_wins) else None,
        "final_win_rate": final_wins / total if total else None,
        "avg_g0_mae": float(df["g0_mae"].mean()) if total else None,
        "avg_g0_mfe": float(df["g0_mfe"].mean()) if total else None,
        "avg_g1_mae": float(df["g1_mae"].dropna().mean()) if "g1_mae" in df else None,
        "avg_g1_mfe": float(df["g1_mfe"].dropna().mean()) if "g1_mfe" in df else None,
        "avg_g2_mae": float(df["g2_mae"].dropna().mean()) if "g2_mae" in df else None,
        "avg_g2_mfe": float(df["g2_mfe"].dropna().mean()) if "g2_mfe" in df else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gale Forensics M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_gale_forensics.json")
    args = parser.parse_args()
    frames = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        part = evaluate(_load(path))
        part["symbol"] = path.stem
        frames.append(part)
    data = pd.concat(frames, ignore_index=True)
    split = int(len(data) * 0.8)
    train, test = data.iloc[:split], data.iloc[split:]
    output = {
        "schema": "mercury.m5.gale-forensics.v1",
        "train": _metrics(train),
        "test": _metrics(test),
        "g0_losers_analysis": {
            "count": int((~test["g0_hit"]).sum()),
            "g1_recovery_rate": float(test.loc[~test["g0_hit"], "g1_hit"].mean()) if (~test["g0_hit"]).any() else None,
            "g2_recovery_rate": float(test.loc[~test["g0_hit"] & ~test["g1_hit"].fillna(False), "g2_hit"].mean()) if (~test["g0_hit"] & ~test["g1_hit"].fillna(False)).any() else None,
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "test": output["test"], "g0_losers": output["g0_losers_analysis"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
