"""Probe B2 - FASE 6: valida OFFLINE do fix da regex no YahooFinanceProvider.

Nao faz chamada de rede. Apenas verifica:
- _sanitize_symbol aceita simbolos oficiais forex/commodity com '='
- supports_symbol retorna True para esses simbolos
- path traversal (/ \\ ..) e caracteres especiais continuam rejeitados
- divergencia antes/depois: todos os 64 simbolos do universo agora sao suportados
"""
import sys
from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

prov = YahooFinanceProvider()

# 1) Simbolos oficiais representativos
oficial = ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "BRL=X", "CL=F", "SI=F", "GC=F", "BTC-USD", "ETH-USD", "AAPL", "PETR4.SA"]
print("== 1) Simbolos oficiais ==")
for s in oficial:
    try:
        ok = prov.supports_symbol(s)
        print(f"  {s:12s} supports_symbol={ok}")
    except Exception as e:
        print(f"  {s:12s} ERRO: {type(e).__name__}: {e}")

# 2) Path traversal / especiais devem continuar rejeitados
print("== 2) Rejeicoes de seguranca (devem ser False) ==")
for s in ["../etc/passwd", "..\\..\\x", "A/B", "A\\B", "SYMBOL;DROP", "A$B", "AB CD", "A#B", "A*B"]:
    ok = prov.supports_symbol(s)
    print(f"  {s:16s} supports_symbol={ok}  (esperado False)")

# 3) Cobertura do universo oficial (sem rede)
print("== 3) Cobertura do universo oficial (64 simbolos) ==")
suportados = [s for s in ALL_SYMBOLS if prov.supports_symbol(s)]
rejeitados = [s for s in ALL_SYMBOLS if not prov.supports_symbol(s)]
print(f"  TOTAL={len(ALL_SYMBOLS)}  SUPPORTED={len(suportados)}  REJECTED={len(rejeitados)}")
print(f"  REJECTED_LIST={rejeitados}")

# 4) Exemplo dos snapshots que quebravam o teste
print("== 4) Simbolos de snapshot do teste (EURUSD_X etc.) ==")
for s in ["EURUSD=X", "EURUSD_X", "SYM-A", "TEST", "BTC-USD"]:
    print(f"  {s:12s} supports_symbol={prov.supports_symbol(s)}")

verdict = "OK" if len(rejeitados) == 0 and all(not prov.supports_symbol(x) for x in ["../etc/passwd", "A/B", "A\\B", "A$B", "AB CD"]) else "FALHA"
print(f"VEREDITO_PROBE={verdict}")
sys.exit(0 if verdict == "OK" else 1)
