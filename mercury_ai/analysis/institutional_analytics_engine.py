import json
import os
import numpy as np
from mercury_ai.utils.atomic_io import atomic_json_write
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd


class InstitutionalAnalyticsEngine:
    """
    Institutional-grade analytics engine for Mercury-AI.
    
    Provides comprehensive performance analysis, risk metrics,
    attribution analysis, and quality reporting for institutional
    backtesting and live trading evaluation.
    """

    def __init__(
        self,
        snapshot_dir: str = "mercury_ai/database/snapshots",
        replay_dir: str = "data/replay_results",
        risk_free_rate: float = 0.05,
        min_periods: int = 20
    ):
        self.snapshot_dir = snapshot_dir
        self.replay_dir = replay_dir
        self.risk_free_rate = risk_free_rate
        self.min_periods = min_periods

    # ------------------------------------------------------------------ #
    #  DATA LOADING
    # ------------------------------------------------------------------ #

    def _load_data(self) -> pd.DataFrame:
        """Load and merge snapshot + replay data into a single DataFrame."""
        data_records: List[Dict[str, Any]] = []
        replay_metrics = self._load_replay_metrics()

        if not os.path.isdir(self.snapshot_dir):
            return pd.DataFrame()

        for filename in os.listdir(self.snapshot_dir):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self.snapshot_dir, filename)
            try:
                with open(filepath, "r") as f:
                    snapshot = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue

            audit_id = snapshot.get("decision_result", {}).get("audit_id", "")
            if not audit_id or audit_id not in replay_metrics:
                continue

            metrics = replay_metrics[audit_id]
            evidences = snapshot.get("evidence_bundle", {}).get("evidences", [])
            record = {
                "audit_id": audit_id,
                "asset": snapshot.get("asset", "unknown"),
                "timestamp": snapshot.get("timestamp", ""),
                "decision": snapshot.get("decision_result", {}).get("decision", ""),
                "score": snapshot.get("decision_result", {}).get("score", 0.0),
                "confidence": snapshot.get("decision_result", {}).get("confidence", 0.0),
                "evidences": [e.get("evidence_name", "") for e in evidences],
                "engines": list(set(e.get("engine_name", "") for e in evidences)),
                "hit": metrics.get("hit", False),
                "pl": metrics.get("pl", 0.0),
                "return_pct": metrics.get("return_pct", 0.0),
            }
            data_records.append(record)

        df = pd.DataFrame(data_records)
        if not df.empty and "timestamp" in df.columns:
            # Conversão temporal robusta: snapshots podem conter timestamps
            # naive UTC (tempo real) e timezone-aware (replay com dataset
            # tz-aware). `format="mixed"` + `utc=True` parseia cada elemento
            # individualmente e converte aware para UTC preservando o instante
            # (evita que timestamps aware válidos virem NaT — achado R2 do
            # B4-C4). `.dt.tz_localize(None)` normaliza para naive UTC,
            # mantendo o contrato existente (datetime64 naive) dos consumidores.
            # Timestamps inválidos continuam virando NaT (detectáveis), pois
            # errors='coerce' é mantido intencionalmente (resiliência a dados
            # corrompidos; _temporal_analysis já faz dropna).
            df["timestamp"] = pd.to_datetime(
                df["timestamp"], errors="coerce", format="mixed", utc=True
            ).dt.tz_localize(None)
            df = df.sort_values("timestamp").reset_index(drop=True)
        return df

    def _load_replay_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Load replay result files keyed by audit_id."""
        replay_metrics: Dict[str, Dict[str, Any]] = {}
        if not os.path.isdir(self.replay_dir):
            return replay_metrics
        for filename in os.listdir(self.replay_dir):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self.replay_dir, filename)
            try:
                with open(filepath, "r") as f:
                    replay_metrics[filename.replace(".json", "")] = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue
        return replay_metrics

    # ------------------------------------------------------------------ #
    #  CORE QUALITY REPORT
    # ------------------------------------------------------------------ #

    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate a comprehensive institutional-quality report."""
        df = self._load_data()
        if df.empty:
            return {"error": "No data available", "status": "empty"}

        report = {
            "overview": self._overview_stats(df),
            "win_rate_analysis": self._win_rate_analysis(df),
            "risk_metrics": self._risk_metrics(df),
            "engine_contribution": self._engine_contribution(df),
            "pattern_analysis": self._pattern_analysis(df),
            "temporal_analysis": self._temporal_analysis(df),
            "confidence_analysis": self._confidence_analysis(df),
            "attribution": self._attribution_analysis(df),
            "status": "success",
        }
        return report

    # ------------------------------------------------------------------ #
    #  OVERVIEW STATISTICS
    # ------------------------------------------------------------------ #

    def _overview_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        total = len(df)
        wins = df["hit"].sum()
        loss = total - wins
        total_pl = df["pl"].sum()
        return {
            "total_decisions": int(total),
            "total_wins": int(wins),
            "total_losses": int(loss),
            "win_rate": float(wins / total) if total > 0 else 0.0,
            "total_pl": float(total_pl),
            "avg_pl_per_trade": float(df["pl"].mean()),
            "unique_assets": int(df["asset"].nunique()),
            "date_range": {
                "start": str(df["timestamp"].min()) if "timestamp" in df else "",
                "end": str(df["timestamp"].max()) if "timestamp" in df else "",
            },
        }

    # ------------------------------------------------------------------ #
    #  WIN RATE ANALYSIS
    # ------------------------------------------------------------------ #

    def _win_rate_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Per-asset and overall win-rate breakdowns."""
        overall = float(df["hit"].mean()) if len(df) > 0 else 0.0
        per_asset = df.groupby("asset")["hit"].agg(["mean", "count"]).to_dict("index")
        per_asset_clean = {}
        for asset, vals in per_asset.items():
            per_asset_clean[asset] = {
                "win_rate": float(vals["mean"]),
                "trades": int(vals["count"]),
            }

        # Win rate by decision type
        per_decision = {}
        if "decision" in df.columns:
            for decision, grp in df.groupby("decision"):
                per_decision[decision] = {
                    "win_rate": float(grp["hit"].mean()),
                    "trades": int(len(grp)),
                    "avg_score": float(grp["score"].mean()),
                }

        return {
            "overall_win_rate": overall,
            "per_asset": per_asset_clean,
            "per_decision": per_decision,
        }

    # ------------------------------------------------------------------ #
    #  RISK METRICS  (institutional-grade)
    # ------------------------------------------------------------------ #

    def _risk_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute Sharpe, Sortino, Calmar, max drawdown, and more."""
        if df.empty or "pl" not in df.columns:
            return {}

        pl_series = df["pl"].values
        returns = df["return_pct"].values if "return_pct" in df.columns else pl_series
        total_pl = float(pl_series.sum())

        # --- Basic stats ---
        mean_return = float(np.mean(returns)) if len(returns) > 0 else 0.0
        std_return = float(np.std(returns, ddof=1)) if len(returns) > 1 else 0.0

        # --- Sharpe Ratio (annualized, assuming ~252 trading days) ---
        sharpe = 0.0
        if std_return > 1e-10:
            excess = mean_return - (self.risk_free_rate / 252)
            sharpe = float(np.sqrt(252) * excess / std_return)

        # --- Sortino Ratio (downside deviation) ---
        downside = returns[returns < 0]
        downside_std = float(np.std(downside, ddof=1)) if len(downside) > 1 else 0.0
        sortino = 0.0
        if downside_std > 1e-10:
            excess = mean_return - (self.risk_free_rate / 252)
            sortino = float(np.sqrt(252) * excess / downside_std)

        # --- Max Drawdown ---
        cumulative = np.cumsum(pl_series)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = cumulative - running_max
        max_drawdown = float(np.min(drawdown)) if len(drawdown) > 0 else 0.0

        # --- Calmar Ratio ---
        calmar = 0.0
        if abs(max_drawdown) > 1e-10:
            calmar = float(total_pl / abs(max_drawdown))

        # --- Win/Loss stats ---
        wins = pl_series[pl_series > 0]
        losses = pl_series[pl_series < 0]
        avg_win = float(np.mean(wins)) if len(wins) > 0 else 0.0
        avg_loss = float(np.mean(losses)) if len(losses) > 0 else 0.0
        profit_factor = float(abs(np.sum(wins) / np.sum(losses))) if np.sum(losses) != 0 else float("inf")

        # --- Consecutive wins/losses ---
        hits = df["hit"].values if "hit" in df.columns else (pl_series > 0)
        max_consec_wins = self._max_consecutive(hits, True)
        max_consec_losses = self._max_consecutive(hits, False)

        return {
            "total_pl": total_pl,
            "mean_return_per_trade": mean_return,
            "std_return": std_return,
            "sharpe_ratio": round(sharpe, 4),
            "sortino_ratio": round(sortino, 4),
            "calmar_ratio": round(calmar, 4),
            "max_drawdown": round(max_drawdown, 4),
            "profit_factor": round(profit_factor, 4),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
            "win_loss_ratio": float(avg_win / abs(avg_loss)) if abs(avg_loss) > 1e-10 else 0.0,
            "max_consecutive_wins": int(max_consec_wins),
            "max_consecutive_losses": int(max_consec_losses),
        }

    @staticmethod
    def _max_consecutive(arr: np.ndarray, value: bool) -> int:
        """Return the longest run of `value` in boolean array `arr`."""
        best = 0
        cur = 0
        for v in arr:
            if bool(v) == value:
                cur += 1
                best = max(best, cur)
            else:
                cur = 0
        return best

    # ------------------------------------------------------------------ #
    #  ENGINE CONTRIBUTION
    # ------------------------------------------------------------------ #

    def _engine_contribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Contribution analysis per decision engine."""
        all_engines: set = set()
        for engines in df["engines"]:
            all_engines.update(engines)

        contributions = {}
        for engine in sorted(all_engines):
            mask = df["engines"].apply(lambda x: engine in x)
            subset = df[mask]
            if len(subset) == 0:
                continue
            contributions[engine] = {
                "win_rate": float(subset["hit"].mean()),
                "trades": int(len(subset)),
                "total_pl": float(subset["pl"].sum()),
                "avg_pl": float(subset["pl"].mean()),
                "pct_of_total": float(len(subset) / len(df) * 100),
            }
        return contributions

    # ------------------------------------------------------------------ #
    #  PATTERN ANALYSIS
    # ------------------------------------------------------------------ #

    def _pattern_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify top-performing evidence patterns."""
        df_copy = df.copy()
        df_copy["pattern"] = df_copy["evidences"].apply(lambda x: tuple(sorted(x)))
        pattern_grp = df_copy.groupby("pattern")["hit"].agg(["mean", "count"])
        pattern_grp = pattern_grp[pattern_grp["count"] >= 3]  # min frequency
        top_patterns = pattern_grp.nlargest(10, "mean")

        result = {}
        for pattern, row in top_patterns.iterrows():
            result[" + ".join(pattern)] = {
                "win_rate": float(row["mean"]),
                "occurrences": int(row["count"]),
            }
        return result

    # ------------------------------------------------------------------ #
    #  TEMPORAL ANALYSIS
    # ------------------------------------------------------------------ #

    def _temporal_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Performance trends over time (monthly/weekly)."""
        if "timestamp" not in df.columns or df["timestamp"].isna().all():
            return {}

        df = df.dropna(subset=["timestamp"]).copy()
        df["month"] = df["timestamp"].dt.to_period("M").astype(str)
        df["week"] = df["timestamp"].dt.isocalendar().week.astype(str)
        df["year"] = df["timestamp"].dt.year.astype(str)

        monthly = (
            df.groupby("month")
            .agg(win_rate=("hit", "mean"), trades=("hit", "count"), total_pl=("pl", "sum"))
            .to_dict("index")
        )
        monthly_clean = {}
        for m, vals in monthly.items():
            monthly_clean[m] = {k: float(v) if isinstance(v, (np.floating, float)) else int(v) for k, v in vals.items()}

        return {
            "monthly": monthly_clean,
            "recent_trend": self._recent_trend(df),
        }

    def _recent_trend(self, df: pd.DataFrame) -> Dict[str, float]:
        """Compare recent performance (last 20%) vs earlier."""
        if len(df) < self.min_periods:
            return {"note": "insufficient data for trend analysis"}
        split = int(len(df) * 0.8)
        early = df.iloc[:split]
        late = df.iloc[split:]
        return {
            "early_win_rate": float(early["hit"].mean()),
            "recent_win_rate": float(late["hit"].mean()),
            "early_avg_pl": float(early["pl"].mean()),
            "recent_avg_pl": float(late["pl"].mean()),
            "trend_direction": "improving"
            if late["hit"].mean() > early["hit"].mean()
            else "declining" if late["hit"].mean() < early["hit"].mean()
            else "stable",
        }

    # ------------------------------------------------------------------ #
    #  CONFIDENCE ANALYSIS
    # ------------------------------------------------------------------ #

    def _confidence_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze relationship between confidence scores and outcomes."""
        if "confidence" not in df.columns:
            return {}
        bins = [0, 0.3, 0.5, 0.7, 0.85, 1.0]
        labels = ["0-30%", "30-50%", "50-70%", "70-85%", "85-100%"]
        df_copy = df.copy()
        df_copy["conf_bin"] = pd.cut(df_copy["confidence"], bins=bins, labels=labels)
        conf_grp = df_copy.groupby("conf_bin", observed=True)["hit"].agg(["mean", "count", "sum"])
        result = {}
        for label, row in conf_grp.iterrows():
            result[str(label)] = {
                "win_rate": float(row["mean"]),
                "trades": int(row["count"]),
                "wins": int(row["sum"]),
            }
        return result

    # ------------------------------------------------------------------ #
    #  ATTRIBUTION ANALYSIS
    # ------------------------------------------------------------------ #

    def _attribution_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Decompose P&L contribution by asset and decision type."""
        if df.empty:
            return {}

        # By asset
        by_asset = (
            df.groupby("asset")
            .agg(
                trades=("pl", "count"),
                total_pl=("pl", "sum"),
                avg_pl=("pl", "mean"),
                win_rate=("hit", "mean"),
            )
            .sort_values("total_pl", ascending=False)
        )
        asset_contrib = {}
        for asset, row in by_asset.iterrows():
            asset_contrib[asset] = {
                "trades": int(row["trades"]),
                "total_pl": float(row["total_pl"]),
                "avg_pl": float(row["avg_pl"]),
                "win_rate": float(row["win_rate"]),
            }

        # By decision type
        by_decision = {}
        if "decision" in df.columns:
            for decision, grp in df.groupby("decision"):
                by_decision[decision] = {
                    "trades": int(len(grp)),
                    "total_pl": float(grp["pl"].sum()),
                    "avg_pl": float(grp["pl"].mean()),
                    "win_rate": float(grp["hit"].mean()),
                }

        return {
            "by_asset": asset_contrib,
            "by_decision": by_decision,
        }

    # ------------------------------------------------------------------ #
    #  EXPORT HELPERS
    # ------------------------------------------------------------------ #

    def export_report_json(self, output_path: str) -> str:
        """Generate and export the quality report to a JSON file."""
        report = self.generate_quality_report()
        atomic_json_write(output_path, report, indent=2, default=str)
        return output_path

    def export_report_summary(self, output_path: str) -> str:
        """Generate a human-readable summary text file."""
        report = self.generate_quality_report()
        if "error" in report:
            with open(output_path, "w") as f:
                f.write(f"Error: {report['error']}\n")
            return output_path

        lines: List[str] = []
        lines.append("=" * 60)
        lines.append("  MERCURY-AI INSTITUTIONAL ANALYTICS REPORT")
        lines.append("=" * 60)
        lines.append("")

        ov = report.get("overview", {})
        lines.append(f"Period        : {ov.get('date_range', {}).get('start', 'N/A')}  ->  {ov.get('date_range', {}).get('end', 'N/A')}")
        lines.append(f"Total Trades  : {ov.get('total_decisions', 0)}")
        lines.append(f"Unique Assets : {ov.get('unique_assets', 0)}")
        lines.append(f"Win Rate      : {ov.get('win_rate', 0):.2%}")
        lines.append(f"Total P&L     : {ov.get('total_pl', 0):.2f}")
        lines.append("")

        risk = report.get("risk_metrics", {})
        lines.append("--- Risk Metrics ---")
        lines.append(f"Sharpe Ratio  : {risk.get('sharpe_ratio', 'N/A')}")
        lines.append(f"Sortino Ratio : {risk.get('sortino_ratio', 'N/A')}")
        lines.append(f"Calmar Ratio  : {risk.get('calmar_ratio', 'N/A')}")
        lines.append(f"Max Drawdown  : {risk.get('max_drawdown', 'N/A')}")
        lines.append(f"Profit Factor : {risk.get('profit_factor', 'N/A')}")
        lines.append(f"Avg Win       : {risk.get('avg_win', 0):.2f}")
        lines.append(f"Avg Loss      : {risk.get('avg_loss', 0):.2f}")
        lines.append(f"Max Consec W  : {risk.get('max_consecutive_wins', 0)}")
        lines.append(f"Max Consec L  : {risk.get('max_consecutive_losses', 0)}")
        lines.append("")

        eng = report.get("engine_contribution", {})
        if eng:
            lines.append("--- Engine Contribution ---")
            for name, stats in sorted(eng.items(), key=lambda x: x[1]["total_pl"], reverse=True):
                lines.append(f"  {name:20s}  WR={stats['win_rate']:.2%}  P&L={stats['total_pl']:+.2f}  Trades={stats['trades']}")
            lines.append("")

        attr = report.get("attribution", {}).get("by_asset", {})
        if attr:
            lines.append("--- Top Assets by P&L ---")
            for asset, stats in list(attr.items())[:5]:
                lines.append(f"  {asset:20s}  P&L={stats['total_pl']:+.2f}  WR={stats['win_rate']:.2%}  Trades={stats['trades']}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("  END OF REPORT")
        lines.append("=" * 60)

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path
