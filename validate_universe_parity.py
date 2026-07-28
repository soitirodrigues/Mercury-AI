import yfinance as yf
from mercury_ai.config.universe import ALL_SYMBOLS

def validate_universe():
    print(f"--- VALIDAÇÃO DE PARIDADE: UNIVERSO OPERACIONAL ({len(ALL_SYMBOLS)} ativos) ---")
    success_count = 0
    failures = []

    for symbol in ALL_SYMBOLS:
        try:
            ticker = yf.Ticker(symbol)
            # Captura um pequeno volume de dados para validar conectividade
            df = ticker.history(period='1d', interval='5m')
            
            if not df.empty:
                print(f"[OK] {symbol}")
                success_count += 1
            else:
                print(f"[EMPTY] {symbol} - Sem dados disponíveis")
                failures.append((symbol, "Sem dados"))
        except Exception as e:
            print(f"[ERROR] {symbol} - {str(e)}")
            failures.append((symbol, str(e)))

    print("\n" + "="*50)
    print(f"RESULTADO FINAL: {success_count}/{len(ALL_SYMBOLS)} ativos validados")
    print("="*50)

    if failures:
        print("\nAtivos com falha:")
        for sym, err in failures:
            print(f"- {sym}: {err}")
    else:
        print("\nTodos os ativos do universo estão operacionais!")

if __name__ == "__main__":
    validate_universe()
