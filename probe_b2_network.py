"""
Probe B2 — Prova por EXECUÇÃO REAL que:
1. Yahoo (yfinance) consegue buscar EURUSD=X (dados reais).
2. YahooAdapter (caminho de producao do scanner) consegue buscar EURUSD=X.
3. YahooFinanceProvider (caminho do PerformanceAnalytics) FALHA por causa da regex.

Uso: python probe_b2_network.py
"""
import traceback


def main():
    print("=" * 78)
    print("PROBE B2 — TESTE REAL DE REDE para EURUSD=X")
    print("=" * 78)

    # 1. yfinance direto
    print("\n[1] yf.download('EURUSD=X', period='5d', interval='5m')")
    try:
        import yfinance as yf
        df = yf.download("EURUSD=X", period="5d", interval="5m", progress=False)
        print(f"    -> retornou {len(df)} linhas, colunas={list(df.columns)[:6]}")
        if not df.empty:
            print(f"    -> Ultimo close: {df['Close'].iloc[-1]:.5f}" if 'Close' in df.columns else "    -> OK, sem coluna Close")
            print("    -> YAHOO SUPORTA EURUSD=X (dados reais disponiveis)")
        else:
            print("    -> DataFrame VAZIO (sem dados de rede)")
    except Exception as e:
        print(f"    -> ERRO: {type(e).__name__}: {e}")

    # 2. YahooAdapter (caminho de producao do scanner)
    print("\n[2] YahooAdapter (data_adapters) suporta EURUSD=X?")
    try:
        from mercury_ai.providers.data_adapters import YahooAdapter
        a = YahooAdapter()
        print(f"    -> supported_assets inclui EURUSD=X: {'EURUSD=X' in a.supported_assets}")
        print(f"    -> is_implemented: {a.is_implemented}, check_health: {a.check_health()}")
        df = a.get_data("EURUSD=X", interval="5m")
        print(f"    -> get_data retornou {len(df)} linhas")
    except Exception as e:
        print(f"    -> ERRO: {type(e).__name__}: {e}")

    # 3. YahooFinanceProvider (caminho do PerformanceAnalytics / teste que falha)
    print("\n[3] YahooFinanceProvider (yahoo_finance_provider) suporta EURUSD=X?")
    try:
        from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
        p = YahooFinanceProvider()
        print(f"    -> supports_symbol('EURUSD=X'): {p.supports_symbol('EURUSD=X')}")
        print(f"    -> supports_symbol('BTC-USD'):  {p.supports_symbol('BTC-USD')}")
        try:
            df = p.get_data("EURUSD=X")
            print(f"    -> get_data retornou {len(df)} linhas")
        except Exception as e:
            print(f"    -> get_data('EURUSD=X') ERRO: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"    -> ERRO: {type(e).__name__}: {e}")

    print("\n" + "=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
