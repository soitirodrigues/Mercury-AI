"""
Probe B2 — Verifica a divergência entre o UNIVERSO OFICIAL e o
YahooFinanceProvider (regex de sanitização de símbolo).

Uso: python probe_b2_divergence.py
"""
import mercury_ai.config.universe as u
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider


def main():
    allsyms = list(u.ALL_SYMBOLS)
    print("ALL_SYMBOLS count:", len(allsyms))

    eq_syms = [s for s in allsyms if "=" in s]
    print('Simbolos com "=" (forex/commodity):', len(eq_syms))
    print("Exemplos:", eq_syms[:8])

    p = YahooFinanceProvider()
    supported = []
    rejected = []
    for s in allsyms:
        if p.supports_symbol(s):
            supported.append(s)
        else:
            rejected.append(s)

    print("---")
    print("Suportados pelo YahooFinanceProvider:", len(supported))
    print("REJEITADOS pelo YahooFinanceProvider:", len(rejected))
    print("Exemplos rejeitados:", rejected[:12])

    # Detalhe por mercado
    from mercury_ai.config.universe import (
        FOREX_SYMBOLS,
        CRYPTO_SYMBOLS,
        STOCK_SYMBOLS,
        COMMODITY_SYMBOLS,
    )
    for nome, lista in [
        ("FOREX", FOREX_SYMBOLS),
        ("CRYPTO", CRYPTO_SYMBOLS),
        ("STOCKS", STOCK_SYMBOLS),
        ("COMMODITIES", COMMODITY_SYMBOLS),
    ]:
        rej = [s for s in lista if not p.supports_symbol(s)]
        print(f"  {nome}: {len(lista)} totais, {len(rej)} rejeitados -> {rej[:5]}")

    # Testa o sanitize direto para EURUSD=X
    try:
        clean = p._sanitize_symbol("EURUSD=X")
        print("Sanitize EURUSD=X OK:", clean)
    except Exception as e:
        print("Sanitize EURUSD=X FALHOU:", type(e).__name__, e)

    try:
        clean = p._sanitize_symbol("GC=F")
        print("Sanitize GC=F OK:", clean)
    except Exception as e:
        print("Sanitize GC=F FALHOU:", type(e).__name__, e)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
