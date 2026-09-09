import pandas as pd
import yfinance as yf
import logging
import threading
import time

from mercury_ai.providers.data_interfaces import IDataProvider
from mercury_ai.config.universe import ALL_SYMBOLS, FOREX_SYMBOLS, CRYPTO_SYMBOLS


class BaseAdapter:

    def __init__(
        self,
        name,
        timeframes,
        markets,
        assets,
        limit,
        priority
    ):

        self.name = name
        self.supported_timeframes = timeframes
        self.supported_markets = markets
        self.supported_assets = assets
        self.request_limit = limit
        self.priority = priority
        # Apenas adapters com implementação real de get_data são "implemented".
        # Stubs (herdeiros que não sobrescrevem get_data) são indisponíveis.
        self.is_implemented = False


    def check_health(self):

        # Saúde honesta: um adapter sem implementação real (stub) NÃO está
        # disponível, mesmo que registrado no catálogo de providers.
        return self.is_implemented



    def get_data(
        self,
        symbol,
        interval="5m"
    ):

        return pd.DataFrame()



class YahooAdapter(BaseAdapter):

    def __init__(self, cache_ttl_s: float = 60.0):

        super().__init__(
            "Yahoo",
            [
                "1m",
                "5m",
                "15m",
                "1h"
            ],
            [
                "Forex",
                "Stocks",
                "Commodities",
                "Crypto"
            ],
            ALL_SYMBOLS,
            1000,
            1
        )

        # Único adapter com implementação real de get_data no V1.
        self.is_implemented = True

        # S33-E.2 P2 — cache semanticamente seguro (só este cache S33-E;
        # YahooFinanceProvider é pré-existente e está FORA deste escopo).
        # A chave representa TODOS os parâmetros que podem alterar o dataset
        # (symbol/interval/period/start/end/auto_adjust). TTL sozinho NÃO é
        # prova de segurança: além do TTL, a entrada é invalidada ao cruzar
        # a fronteira M5 (floor_m5, mesma autoridade temporal do runner), de
        # modo que o dataset da vela anterior nunca é servido como se fosse
        # da vela atual. Somente DataFrames NÃO-vazios são cacheados (vazio =
        # erro/transiente e não deve mascarar recuperação). Retorna sempre
        # cópias para o caller nunca mutar o cache (DataNormalizer muta df).
        self._cache_ttl_s = float(cache_ttl_s)
        self._cache: dict = {}
        self._cache_lock = threading.Lock()
        self._cache_hits = 0
        self._cache_misses = 0
        self._downloads = 0

    def _current_m5_boundary(self) -> str:
        """Fronteira M5 atual (UTC) — autoridade temporal do runner (floor_m5).

        Método separado para permitir controle determinístico em testes.
        """
        try:
            from datetime import datetime, timezone
            from mercury_ai.operations.m5_incremental.temporal import floor_m5
            return floor_m5(datetime.now(timezone.utc)).isoformat()
        except Exception:
            try:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                return now.replace(
                    minute=(now.minute // 5) * 5, second=0, microsecond=0
                ).isoformat()
            except Exception:
                return ""

    def get_cache_stats(self) -> dict:
        """Contadores observáveis (Fase 6): downloads reais, hits, misses."""
        with self._cache_lock:
            return {
                "downloads": self._downloads,
                "hits": self._cache_hits,
                "misses": self._cache_misses,
                "entries": len(self._cache),
            }

    def clear_cache(self) -> None:
        """Limpa o cache (uso em testes)."""
        with self._cache_lock:
            self._cache.clear()
            self._cache_hits = 0
            self._cache_misses = 0
            self._downloads = 0


    def get_data(
        self,
        symbol,
        interval="5m",
        period="5d",
        start=None,
        end=None,
        auto_adjust=None,
    ):

        key = f"{symbol}|{interval}|{period}|{start}|{end}|{auto_adjust}"
        m5_boundary = self._current_m5_boundary()
        now = time.monotonic()
        with self._cache_lock:
            entry = self._cache.get(key)
            # S33-E.2 P2: TTL NÃO basta — entrada de fronteira M5 anterior
            # nunca é servida como FRESH ("este dataset ainda representa o
            # candle que o scan atual deve processar?").
            if entry is not None and (now >= entry[1] or entry[2] != m5_boundary):
                del self._cache[key]
                entry = None
            if entry is not None:
                self._cache_hits += 1
                return entry[0].copy()
            self._cache_misses += 1

        logging.debug(
            f"Yahoo buscando {symbol}"
        )

        with self._cache_lock:
            self._downloads += 1

        # S33-E.2 P2 — fetch INTACTO (proibido alterar quantidade de dados):
        # period fixo "5d"; start/end/auto_adjust NÃO são repassados à rede
        # porque nenhum chamador atual os utiliza (verificado: MarketDataService
        # e MTFEngine passam só interval/period). A chave os inclui de forma
        # defensiva: se um dia forem utilizados, nunca colidem com entradas
        # antigas. Pedidos com period distinto (ex: MTF "1mo" vs pipeline "5d")
        # nunca compartilham entrada — cada um busca o próprio dataset.
        df = yf.download(
            symbol,
            period="5d",
            interval=interval,
            progress=False
        )


        if df.empty:
            return pd.DataFrame()


        if isinstance(df.columns, pd.MultiIndex):

            df.columns = df.columns.get_level_values(0)


        df = df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }
        )

        # S33-E.2: cacheia somente sucesso (não-vazio); retorna cópia.
        # Tupla (df, expira_em, fronteira_m5): TTL + boundary autoritativo.
        with self._cache_lock:
            self._cache[key] = (df, time.monotonic() + self._cache_ttl_s, self._current_m5_boundary())

        return df.copy()



class PolygonAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "Polygon",
            ["1m","5m","1h"],
            ["Stocks","Crypto"],
            CRYPTO_SYMBOLS,
            500,
            2
        )



class TwelveDataAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "TwelveData",
            ["1m","5m","1h"],
            ["Forex","Stocks"],
            FOREX_SYMBOLS,
            800,
            3
        )



class AlphaVantageAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "AlphaVantage",
            ["5m","1h","1d"],
            ["Stocks"],
            ALL_SYMBOLS,
            500,
            4
        )



class BinanceAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "Binance",
            ["1m","5m","1h"],
            ["Crypto"],
            CRYPTO_SYMBOLS,
            1200,
            1
        )



class MetaTrader5Adapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "MetaTrader5",
            ["1m","5m","1h","1d"],
            ["Forex","Commodities"],
            FOREX_SYMBOLS,
            9999,
            5
        )