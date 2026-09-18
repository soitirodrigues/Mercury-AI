"""Avaliacao walk-forward de setups M5 sem lookahead.

Este modulo e deliberadamente separado do pipeline de decisao. Ele mede o
filtro SMC sobre candles fechados e so consulta o candle seguinte para rotular
o resultado, permitindo auditar cobertura, acuracia e retorno liquido.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple

import pandas as pd

from mercury_ai.signals.m5_institutional_filters import (
    TRIGGER_BODY_MIN,
    smc_reversal_flags,
    smc_reversal_setup,
)


FlagProvider = Callable[[pd.DataFrame, str], Mapping[str, Any]]


@dataclass(frozen=True)
class SetupObservation:
    """Resultado de uma oportunidade avaliada em um candle fechado."""

    index: int
    timestamp: str
    decision: str
    approved: bool
    hit: bool
    net_result: float


def wilson_interval(wins: int, total: int, z: float = 1.96) -> Tuple[float, float]:
    """Retorna o intervalo Wilson de 95% para uma taxa binomial."""
    if total <= 0 or wins < 0 or wins > total:
        raise ValueError("wins/total invalidos")
    if z <= 0:
        raise ValueError("z deve ser positivo")
    p = wins / total
    denominator = 1.0 + z * z / total
    centre = (p + z * z / (2.0 * total)) / denominator
    margin = (
        z
        * ((p * (1.0 - p) / total + z * z / (4.0 * total * total)) ** 0.5)
        / denominator
    )
    return max(0.0, centre - margin), min(1.0, centre + margin)


def _summary(observations: Iterable[SetupObservation]) -> Dict[str, Any]:
    rows = list(observations)
    total = len(rows)
    wins = sum(1 for row in rows if row.hit)
    net = sum(row.net_result for row in rows)
    loss_streak = 0
    max_loss_streak = 0
    for row in rows:
        if row.hit:
            loss_streak = 0
        else:
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)
    low, high = wilson_interval(wins, total) if total else (None, None)
    return {
        "signals": total,
        "wins": wins,
        "losses": total - wins,
        "hit_rate": wins / total if total else None,
        "wilson_low_95": low,
        "wilson_high_95": high,
        "coverage": total,
        "net_result": net,
        "average_net_result": net / total if total else None,
        "max_loss_streak": max_loss_streak,
    }


def _normalise_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        raise ValueError("frame OHLCV vazio ou invalido")
    renamed = {str(column).lower(): column for column in frame.columns}
    required = {"open", "high", "low", "close"}
    if not required.issubset(renamed):
        missing = sorted(required - set(renamed))
        raise ValueError(f"colunas OHLC ausentes: {missing}")
    out = frame.rename(columns={value: key for key, value in renamed.items()}).copy()
    out = out.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    })
    out = out.sort_index()
    if out.index.has_duplicates or not out.index.is_monotonic_increasing:
        raise ValueError("indice deve ser crescente e sem duplicatas")
    return out


def _cheap_trigger_gate(data: pd.DataFrame) -> pd.Series:
    """Pre-calcula o requisito barato e obrigatorio de corpo minimo."""
    high = data["High"].astype(float)
    low = data["Low"].astype(float)
    close = data["Close"].astype(float)
    open_ = data["Open"].astype(float)
    price_range = high - low
    body_ratio = (close - open_).abs().div(price_range.where(price_range > 0))
    return body_ratio


def evaluate_walk_forward(
    frame: pd.DataFrame,
    *,
    min_history: int = 60,
    horizon: int = 1,
    train_ratio: float = 0.60,
    validation_ratio: float = 0.20,
    payout: float = 0.80,
    cost: float = 0.0,
    flag_provider: Optional[FlagProvider] = None,
) -> Dict[str, Any]:
    """Avalia setups com cortes temporais fixos e sem consultar candles futuros.

    A decisao usa exclusivamente ``frame.iloc[:index + 1]``. O candle em
    ``index + horizon`` serve apenas como rotulo posterior. ``payout`` e o
    lucro de uma vitoria por unidade apostada; uma perda vale -1.0.
    """
    if min_history < 2 or horizon < 1:
        raise ValueError("min_history/horizon invalidos")
    if not 0.0 < train_ratio < 1.0:
        raise ValueError("train_ratio invalido")
    if not 0.0 <= validation_ratio < 1.0:
        raise ValueError("validation_ratio invalido")
    if train_ratio + validation_ratio >= 1.0:
        raise ValueError("train + validation devem deixar teste")
    if payout < 0 or cost < 0:
        raise ValueError("payout/cost invalidos")

    data = _normalise_ohlcv(frame)
    provider = flag_provider or smc_reversal_flags
    first_test_index = int(len(data) * train_ratio)
    first_holdout_index = int(len(data) * (train_ratio + validation_ratio))
    observations: List[SetupObservation] = []
    body_ratio = _cheap_trigger_gate(data)

    last_decision_index = len(data) - horizon
    for index in range(min_history, last_decision_index):
        closed = data.iloc[: index + 1]
        candle = data.iloc[index]
        if float(candle["Close"]) == float(candle["Open"]):
            continue
        if (
            pd.isna(body_ratio.iloc[index])
            or float(body_ratio.iloc[index]) < TRIGGER_BODY_MIN
        ):
            continue
        decision = "BUY" if float(candle["Close"]) > float(candle["Open"]) else "SELL"
        flags = provider(closed, decision)
        setup = smc_reversal_setup(dict(flags), decision)
        if not setup["approved"]:
            continue

        entry_candle = data.iloc[index + horizon]
        entry = float(entry_candle["Open"])
        exit_price = float(entry_candle["Close"])
        hit = exit_price > entry if decision == "BUY" else exit_price < entry
        net_result = (payout if hit else -1.0) - cost
        timestamp = str(data.index[index])
        observations.append(
            SetupObservation(index, timestamp, decision, True, hit, net_result)
        )

    splits = {
        "train": [row for row in observations if row.index < first_test_index],
        "validation": [
            row for row in observations
            if first_test_index <= row.index < first_holdout_index
        ],
        "test": [row for row in observations if row.index >= first_holdout_index],
    }
    return {
        "contract": {
            "entry": "open_of_outcome_candle",
            "outcome": f"close_after_{horizon}_candle(s)",
            "lookahead": False,
            "payout": payout,
            "cost": cost,
        },
        "dataset": {
            "candles": len(data),
            "min_history": min_history,
            "decision_indices": max(0, last_decision_index - min_history),
            "train_ratio": train_ratio,
            "validation_ratio": validation_ratio,
            "test_ratio": 1.0 - train_ratio - validation_ratio,
        },
        "overall": _summary(observations),
        "splits": {name: _summary(rows) for name, rows in splits.items()},
        "observations": observations,
    }
