"""
Script para baixar dados históricos e preparar para o replay institucional.
Usa yfinance para baixar dados e salva como parquet em data/replay/{asset}/data.parquet.
"""

import pandas as pd
import yfinance as yf
import os
import sys
from datetime import datetime, timedelta

# Adiciona a raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mercury_ai.config.universe import ALL_SYMBOLS, FOREX_SYMBOLS, CRYPTO_SYMBOLS


def download_and_save(
    symbol: str,
    period: str = "1mo",
    interval: str = "5m",
    output_dir: str = "data/replay"
):
    """
    Baixa dados históricos de um símbolo e salva como parquet.
    
    Args:
        symbol: Símbolo para baixar (ex: EURUSD=X)
        period: Período (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Intervalo (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        output_dir: Diretório de saída
    """
    asset_dir = os.path.join(output_dir, symbol)
    os.makedirs(asset_dir, exist_ok=True)
    
    filepath = os.path.join(asset_dir, "data.parquet")
    
    print(f"Baixando {symbol} (period={period}, interval={interval})...")
    
    try:
        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False,
            multi_level_index=False
        )
    except Exception as e:
        print(f"  ERRO ao baixar {symbol}: {e}")
        return False
    
    if df.empty:
        print(f"  AVISO: Dados vazios para {symbol}")
        return False
    
    # Achata MultiIndex columns se necessário
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Padroniza nomes das colunas para minúsculas (formato esperado pelo IndicatorEngine)
    rename_map = {
        'open': 'open', 'high': 'high', 'low': 'low',
        'close': 'close', 'volume': 'volume',
        'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Volume': 'volume',
        'Adj Close': 'close', 'adj close': 'close',
    }
    df = df.rename(columns=rename_map)
    
    # Remove colunas duplicadas (ex: 'close' pode vir de 'Close' e 'Adj Close')
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Garante que as colunas necessárias existam
    required = ['open', 'high', 'low', 'close', 'volume']
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"  AVISO: Colunas ausentes em {symbol}: {missing}")
        return False
    
    # Salva como parquet
    df.to_parquet(filepath)
    
    print(f"  OK: {len(df)} candles salvos em {filepath}")
    return True


def prepare_all_assets(
    symbols=None,
    period: str = "1mo",
    interval: str = "5m"
):
    """Baixa dados para múltiplos ativos."""
    if symbols is None:
        # Usa FOREX_SYMBOLS como padrão
        symbols = FOREX_SYMBOLS
    
    if isinstance(symbols, str):
        symbols = [symbols]
    
    success = 0
    failed = 0
    
    for symbol in symbols:
        if download_and_save(symbol, period=period, interval=interval):
            success += 1
        else:
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Resumo: {success} ativos baixados, {failed} falhas")
    return success, failed


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepara dados para replay institucional")
    parser.add_argument("--symbols", nargs="+", help="Símbolos para baixar (ex: EURUSD=X GBPUSD=X)")
    parser.add_argument("--period", default="1mo", help="Período (default: 1mo)")
    parser.add_argument("--interval", default="5m", help="Intervalo (default: 5m)")
    parser.add_argument("--all-forex", action="store_true", help="Baixar todos os FOREX")
    parser.add_argument("--all-crypto", action="store_true", help="Baixar todos os Crypto")
    parser.add_argument("--all", action="store_true", help="Baixar todos os ativos")
    
    args = parser.parse_args()
    
    symbols = args.symbols
    
    if args.all:
        symbols = ALL_SYMBOLS
    elif args.all_forex:
        symbols = FOREX_SYMBOLS
    elif args.all_crypto:
        symbols = CRYPTO_SYMBOLS
    elif not symbols:
        # Default: apenas EURUSD=X para teste rápido
        symbols = ["EURUSD=X"]
        print("Nenhum símbolo especificado. Usando default: EURUSD=X")
        print("Use --symbols para especificar, ou --all / --all-forex / --all-crypto")
    
    prepare_all_assets(symbols, period=args.period, interval=args.interval)