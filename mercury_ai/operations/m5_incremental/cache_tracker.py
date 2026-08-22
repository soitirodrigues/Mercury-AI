"""Cache seguro — validação por freshness, não por TTL cego.

Regra:
  VALID:   cached_last_candle == required_decision_candle
  INVALID: cached_last_candle <  required_decision_candle  -> REFRESH REQUIRED
  STALE:   cached_last_candle é anterior à última disponível -> CACHE_STALE

Registrar: CACHE_HIT, CACHE_MISS, CACHE_STALE, CACHE_REFRESH
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional
from enum import Enum


class CacheStatus(str, Enum):
    HIT = "CACHE_HIT"
    MISS = "CACHE_MISS"
    STALE = "CACHE_STALE"
    REFRESH = "CACHE_REFRESH"


@dataclass
class CacheEntry:
    symbol: str
    cached_last_candle: Optional[datetime]  # open da última vela cacheada (UTC aware, floored M5)
    cached_at: datetime
    decision_audit_id: Optional[str] = None


@dataclass
class CacheDecision:
    status: CacheStatus
    reason: str
    cached_last_candle: Optional[datetime]
    required_candle: Optional[datetime]


class CacheTracker:
    """Cache validado por candle, não por TTL.

    O cache só é HIT se cached_last_candle == required_decision_candle.
    Se cached < required, é STALE e exige REFRESH.
    Se não há entrada, é MISS.
    """

    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}
        # Contadores para relatório
        self.hits = 0
        self.misses = 0
        self.stales = 0
        self.refreshes = 0

    def get(self, symbol: str) -> Optional[CacheEntry]:
        return self._store.get(symbol)

    def put(
        self,
        symbol: str,
        last_candle: Optional[datetime],
        audit_id: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> None:
        if now is None:
            now = datetime.now(timezone.utc)
        from .temporal import floor_m5, _ensure_utc
        if last_candle is not None:
            last_candle = floor_m5(_ensure_utc(last_candle))
        self._store[symbol] = CacheEntry(
            symbol=symbol,
            cached_last_candle=last_candle,
            cached_at=now,
            decision_audit_id=audit_id,
        )

    def check(
        self,
        symbol: str,
        required_candle: Optional[datetime],
        latest_available: Optional[datetime] = None,
    ) -> CacheDecision:
        """Verifica se cache pode ser reutilizado.

        Args:
            symbol: ativo
            required_candle: vela M5 esperada para decisão (UTC aware)
            latest_available: última vela disponível no provider (se None, assume required)

        Returns:
            CacheDecision com status HIT/MISS/STALE/REFRESH
        """
        from .temporal import floor_m5, _ensure_utc

        if required_candle is not None:
            required_candle = floor_m5(_ensure_utc(required_candle))
        if latest_available is not None:
            latest_available = floor_m5(_ensure_utc(latest_available))

        entry = self._store.get(symbol)

        if entry is None:
            self.misses += 1
            return CacheDecision(
                status=CacheStatus.MISS,
                reason="no cache entry",
                cached_last_candle=None,
                required_candle=required_candle,
            )

        cached = entry.cached_last_candle
        if cached is not None:
            cached = floor_m5(_ensure_utc(cached))

        # Sem required => não podemos validar => MISS
        if required_candle is None:
            self.misses += 1
            return CacheDecision(
                status=CacheStatus.MISS,
                reason="required_candle is None",
                cached_last_candle=cached,
                required_candle=None,
            )

        if cached is None:
            self.stales += 1
            return CacheDecision(
                status=CacheStatus.STALE,
                reason="cached_last_candle is None",
                cached_last_candle=None,
                required_candle=required_candle,
            )

        if cached == required_candle:
            # Ainda precisa verificar se latest_available avançou além do cache
            # Se latest > cached, cache está stale embora == required antigo
            effective_required = latest_available if latest_available is not None else required_candle
            if effective_required is not None and cached < effective_required:
                self.stales += 1
                return CacheDecision(
                    status=CacheStatus.STALE,
                    reason=f"cached {cached.isoformat()} < latest {effective_required.isoformat()} (nova vela disponível)",
                    cached_last_candle=cached,
                    required_candle=effective_required,
                )
            self.hits += 1
            return CacheDecision(
                status=CacheStatus.HIT,
                reason=f"cached == required ({cached.isoformat()})",
                cached_last_candle=cached,
                required_candle=required_candle,
            )

        if cached < required_candle:
            self.stales += 1
            return CacheDecision(
                status=CacheStatus.STALE,
                reason=f"cached {cached.isoformat()} < required {required_candle.isoformat()} — REFRESH REQUIRED",
                cached_last_candle=cached,
                required_candle=required_candle,
            )

        # cached > required (futuro) — inconsistente, tratar como STALE
        self.stales += 1
        return CacheDecision(
            status=CacheStatus.STALE,
            reason=f"cached {cached.isoformat()} > required {required_candle.isoformat()} (inconsistente)",
            cached_last_candle=cached,
            required_candle=required_candle,
        )

    def mark_refresh(self, symbol: str) -> None:
        self.refreshes += 1

    def stats(self) -> Dict[str, int]:
        return {
            "CACHE_HIT": self.hits,
            "CACHE_MISS": self.misses,
            "CACHE_STALE": self.stales,
            "CACHE_REFRESH": self.refreshes,
        }

    def clear(self) -> None:
        self._store.clear()
        self.hits = self.misses = self.stales = self.refreshes = 0
