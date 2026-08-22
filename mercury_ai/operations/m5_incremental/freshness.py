"""Freshness Gate — validação explícita de atualidade da decisão.

Regra:
  decision_candle_timestamp  comparado com  latest_available_candle_timestamp
  Se stale: STATUS = STALE (não reutilizar silenciosamente)
  Se fresh: STATUS = FRESH
  Se provider sem candle novo: STATUS = DATA_UNAVAILABLE ou STALE conforme contrato

Não converter STALE em REAL_SIGNAL.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional

import pandas as pd

from .temporal import decision_candle_timestamp_from_df, _ensure_utc, floor_m5


@dataclass(frozen=True)
class FreshnessResult:
    is_fresh: bool
    status: str  # FRESH | STALE | DATA_UNAVAILABLE
    decision_candle: Optional[datetime]
    latest_candle: Optional[datetime]
    age_seconds: Optional[float]
    reason: str


class FreshnessGate:
    """Gate explícito de freshness para decisões M5."""

    # Tolerância para considerar vela ainda válida (mesmo open) como fresh
    # durante o intervalo de formação da vela. Uma vela M5 tem 300s de vida.
    # Se decision_candle == latest_candle, é fresh independentemente da idade.
    # Se decision_candle < latest_candle, é stale (nova vela disponível não usada).
    STALE_TOLERANCE_S = 0  # sem tolerância: qualquer vela nova => stale

    def check(
        self,
        df: Optional[pd.DataFrame],
        decision_candle: Optional[datetime] = None,
        latest_candle: Optional[datetime] = None,
        now: Optional[datetime] = None,
    ) -> FreshnessResult:
        """Valida freshness.

        Args:
            df: DataFrame real usado na decisão (para extrair latest_candle se não fornecido)
            decision_candle: open da vela que gerou a decisão (UTC aware)
            latest_candle: open da última vela disponível no provider (UTC aware)
            now: relógio wall (UTC aware) para calcular age

        Lógica:
          - Se df vazio ou latest None => DATA_UNAVAILABLE
          - Se decision_candle is None => STALE (sem candle de referência)
          - Se decision_candle == latest_candle => FRESH
          - Se decision_candle <  latest_candle => STALE (nova vela existe mas decisão não a usou)
          - Se decision_candle >  latest_candle => STALE (inconsistente — candle futuro, tratar como stale)
        """
        if now is None:
            now = datetime.now(timezone.utc)
        now = _ensure_utc(now)

        # Resolver latest_candle a partir do df se não fornecido
        if latest_candle is None and df is not None:
            latest_candle = decision_candle_timestamp_from_df(df)

        # Resolver decision_candle a partir do df se não fornecido e fresh check é sobre o mesmo df
        # (para primeiro scan, decision_candle == latest_candle)

        # Normalizar para UTC
        if decision_candle is not None:
            decision_candle = _ensure_utc(decision_candle)
            # Truncar para fronteira M5 para comparação robusta (ignora segundos residuais)
            decision_candle = floor_m5(decision_candle)
        if latest_candle is not None:
            latest_candle = _ensure_utc(latest_candle)
            latest_candle = floor_m5(latest_candle)

        # Caso DATA_UNAVAILABLE
        if latest_candle is None:
            return FreshnessResult(
                is_fresh=False,
                status="DATA_UNAVAILABLE",
                decision_candle=decision_candle,
                latest_candle=None,
                age_seconds=None,
                reason="latest_available_candle is None (provider sem dados / df vazio)",
            )

        if decision_candle is None:
            # Sem candle de decisão => não há decisão válida para comparar => stale
            age = (now - latest_candle).total_seconds() if latest_candle else None
            return FreshnessResult(
                is_fresh=False,
                status="STALE",
                decision_candle=None,
                latest_candle=latest_candle,
                age_seconds=age,
                reason="decision_candle is None (sem decisão prévia)",
            )

        age = (now - decision_candle).total_seconds()

        if decision_candle == latest_candle:
            return FreshnessResult(
                is_fresh=True,
                status="FRESH",
                decision_candle=decision_candle,
                latest_candle=latest_candle,
                age_seconds=age,
                reason=f"decision_candle == latest_candle ({decision_candle.isoformat()})",
            )

        if decision_candle < latest_candle:
            delta_candles = int((latest_candle - decision_candle).total_seconds() / 300)
            return FreshnessResult(
                is_fresh=False,
                status="STALE",
                decision_candle=decision_candle,
                latest_candle=latest_candle,
                age_seconds=age,
                reason=f"decision_candle {decision_candle.isoformat()} < latest {latest_candle.isoformat()} ({delta_candles} vela(s) atrás)",
            )

        # decision_candle > latest (futuro) — inconsistência
        return FreshnessResult(
            is_fresh=False,
            status="STALE",
            decision_candle=decision_candle,
            latest_candle=latest_candle,
            age_seconds=age,
            reason=f"decision_candle {decision_candle.isoformat()} > latest {latest_candle.isoformat()} (inconsistente/futuro)",
        )

    def check_state(
        self,
        state_decision_candle_iso: Optional[str],
        latest_candle: Optional[datetime],
        now: Optional[datetime] = None,
    ) -> FreshnessResult:
        """Conveniência: check a partir do ISO string guardado no AssetScanState."""
        dec = None
        if state_decision_candle_iso:
            try:
                dec = datetime.fromisoformat(state_decision_candle_iso.replace("Z", "+00:00"))
                dec = _ensure_utc(dec)
            except Exception:
                dec = None
        return self.check(df=None, decision_candle=dec, latest_candle=latest_candle, now=now)
