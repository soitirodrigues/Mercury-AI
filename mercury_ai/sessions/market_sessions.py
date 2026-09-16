from datetime import datetime, timezone
from typing import Optional

from mercury_ai.config import sessions
from mercury_ai.utils.deterministic_clock import DeterministicClock


class MarketSessions:
    """Sessao de mercado + elegibilidade operacional por classe de ativo (S7.X-F2).

    Contrato F2 (UTC, via DeterministicClock):
      FOREX  -> elegivel em dias uteis (Mon-Fri), NAO elegivel no weekend (Sat/Sun)
      CRYPTO -> sempre elegivel (24/7)

    Distingue SESSION ELIGIBILITY (regra operacional) de PROVIDER DATA AVAILABILITY.
    Esta classe decide apenas elegibilidade; disponibilidade de dados continua a
    cargo do provider/pipeline (DATA_PROVIDER_UNAVAILABLE vs MARKET_CLOSED).

    Timezone: UTC explicito (DeterministicClock.utcnow() ou datetime.now(timezone.utc)).
    Replay: quando DeterministicClock estiver congelado (is_frozen), esta classe
    observa o tempo congelado — portanto NÃO usar MarketSessions para decidir
    elegibilidade dentro de replay historico; replay deve isolar/bypassar a
    checagem de sessao live (ver Scanner/M5Operational).
    """

    # Mercado por classe — fonte canonica e universe.py (FOREX/CRYPTO)
    FOREX_MARKET = "FOREX"
    CRYPTO_MARKET = "CRYPTO"

    def get_current_session(self):

        hour = DeterministicClock.utcnow().hour

        if 22 <= hour or hour < 7:
            return sessions.SYDNEY

        elif 0 <= hour < 9:
            return sessions.TOKYO

        elif 7 <= hour < 16:
            return sessions.LONDON

        elif 13 <= hour < 22:
            return sessions.NEW_YORK

        return sessions.CLOSED

    def is_high_liquidity(self):

        hour = DeterministicClock.utcnow().hour

        return 13 <= hour < 16

    # -------------------------------------------------------------
    # F2 — Elegibilidade operacional (Contrato Forex weekend / Crypto 24/7)
    # -------------------------------------------------------------
    @staticmethod
    def _utc_weekday(now: Optional[datetime] = None) -> int:
        """Retorna weekday UTC 0=Mon ... 6=Sun, usando DeterministicClock quando possivel."""
        if now is not None:
            dt = now
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt.weekday()
        # Live path: DetermisticClock ja retorna UTC (naive frozen ou real)
        dc_now = DeterministicClock.utcnow()
        if dc_now.tzinfo is None:
            dc_now = dc_now.replace(tzinfo=timezone.utc)
        return dc_now.weekday()

    @staticmethod
    def _is_weekend_utc(now: Optional[datetime] = None) -> bool:
        return MarketSessions._utc_weekday(now) >= 5  # 5=Sat, 6=Sun

    def is_market_eligible(self, market: str, now: Optional[datetime] = None) -> bool:
        """Retorna True se o mercado esta elegivel para analise live no instante now (UTC).

        Regra F2:
          FOREX  -> False no weekend (Sat/Sun UTC), True caso contrario
          CRYPTO -> True sempre (24/7)
          STOCK/COMMODITY/unknown -> False se weekend? Contrato F2 preserva 39 ativos;
            para compatibilidade, trata STOCK/COMMODITY como nao elegivel no weekend
            e elegivel em weekday (nao operacionais no F1, mas regra clara).
        """
        m = (market or "").strip().upper()
        if m == self.CRYPTO_MARKET or m == "CRIPTO":
            return True
        # FOREX (e STOCK/COMMODITY por extensao) fechado no weekend UTC
        if self._is_weekend_utc(now):
            return False
        return True

    def is_symbol_eligible(self, symbol: str, now: Optional[datetime] = None) -> bool:
        """Conveniencia: resolve market via universe.py e delega para is_market_eligible."""
        try:
            from mercury_ai.config.universe import get_asset, FOREX_UNIVERSE, CRYPTO_UNIVERSE
            asset = get_asset(symbol)
            if asset is not None:
                return self.is_market_eligible(asset.market, now)
            # Fallback por lista (caso simbolo legado sem UniverseAsset)
            if symbol in FOREX_UNIVERSE:
                return self.is_market_eligible("FOREX", now)
            if symbol in CRYPTO_UNIVERSE:
                return self.is_market_eligible("CRYPTO", now)
        except Exception:
            pass
        # Unknown symbol: conservador — aplica regra Forex (weekday=True)
        return self.is_market_eligible("FOREX", now)

    def eligibility_reason(self, market: str, now: Optional[datetime] = None) -> str:
        """Retorna razao legivel para observabilidade (nao altera decisao)."""
        m = (market or "").strip().upper()
        wd = self._utc_weekday(now)
        wd_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][wd]
        eligible = self.is_market_eligible(market, now)
        if m in (self.CRYPTO_MARKET, "CRIPTO"):
            return f"{m} 24/7 eligible ({wd_name} UTC) -> {eligible}"
        if wd >= 5:
            return f"{m} CLOSED weekend ({wd_name} UTC) -> {eligible}"
        return f"{m} OPEN weekday ({wd_name} UTC) -> {eligible}"

    # -------------------------------------------------------------
    # Killzones institucionais (observavel; NAO bloqueia scanner)
    # Londres 07-11h UTC, Nova York 12-16h UTC, Overlap 12-16h.
    # Sydney/Asia (21-07h) = fora de killzone p/ Forex majors.
    # Crypto: sempre em killzone (24/7, sem sessao fina estrutural).
    # Medicao 2026-09-16 (n=30, 100% madrugada): sem amostra Londres/NY
    # para comparar — por isso OBSERVAVEL por 2 semanas antes de gate.
    # -------------------------------------------------------------
    KILLZONES_UTC = {
        "LONDON": (7, 11),
        "NEW_YORK": (12, 16),
    }
    THIN_HOURS_UTC = set(list(range(21, 24)) + list(range(0, 7)))

    @staticmethod
    def _utc_hour(now: Optional[datetime] = None) -> int:
        if now is not None:
            dt = now
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt.hour
        dc_now = DeterministicClock.utcnow()
        if dc_now.tzinfo is None:
            dc_now = dc_now.replace(tzinfo=timezone.utc)
        return dc_now.hour

    def is_in_killzone(self, symbol: str, now: Optional[datetime] = None) -> bool:
        """True se o simbolo esta em killzone operacional (Londres/NY p/ Forex)."""
        try:
            from mercury_ai.config.universe import get_asset
            asset = get_asset(symbol)
            market = (asset.market if asset is not None else "").upper()
        except Exception:
            market = ""
        if market == self.CRYPTO_MARKET or market == "CRIPTO":
            return True
        return self._utc_hour(now) not in self.THIN_HOURS_UTC

    def killzone_reason(self, symbol: str, now: Optional[datetime] = None) -> str:
        """Razao legivel p/ observabilidade (SKIPPED_OUTSIDE_KILLZONE futuro)."""
        h = self._utc_hour(now)
        inside = self.is_in_killzone(symbol, now)
        if inside:
            return f"{symbol} IN_KILLZONE ({h:02d}h UTC: Londres 07-11/NY 12-16)"
        return (f"{symbol} OUTSIDE_KILLZONE ({h:02d}h UTC: Sydney/Asia fina "
                f"21-07h — observar 2 semanas antes de bloquear)")