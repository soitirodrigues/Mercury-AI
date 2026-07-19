import yfinance as yf
import pandas as pd

symbols = ['EURUSD=X', 'GBPJPY=X', 'BTC-USD']
print("--- CAPTURA DE DADOS PARA VALIDAÇÃO (FASE 5) ---")
for s in symbols:
    try:
        ticker = yf.Ticker(s)
        df = ticker.history(period='1d', interval='5m')
        if not df.empty:
            last = df.iloc[-1]
            print(f"\nAtivo: {s}")
            print(f"Time:  {df.index[-1]}")
            print(f"Open:  {last.Open:.5f}")
            print(f"High:  {last.High:.5f}")
            print(f"Low:   {last.Low:.5f}")
            print(f"Close: {last.Close:.5f}")
        else:
            print(f"\nAtivo: {s} - Sem dados disponíveis.")
    except Exception as e:
        print(f"\nAtivo: {s} - Erro: {e}")
print("\n----------------------------------------------")
