import os

from mercury_ai.brain.scanner import MercuryScanner


# Mapeamento Hezilex -> símbolo interno (whitelist anti-injeção).
# Operador digita "EUR/USD" ou "EURUSD=X"; resolve p/ universo canônico.
def _resolve_operator_symbols(raw: str):
    from mercury_ai.config.universe import OPERATIONAL_UNIVERSE
    if not raw or not raw.strip():
        return []
    wanted = [s.strip().upper().replace("/", "") for s in raw.split(",") if s.strip()]
    table = {}
    for sym in OPERATIONAL_UNIVERSE:
        table[sym.upper()] = sym
        table[sym.upper().replace("/", "")] = sym
        table[sym.upper().replace("=X", "").replace("-USD", "")] = sym
    out, seen = [], set()
    for w in wanted:
        hit = table.get(w) or table.get(w.replace("=X", "")) or table.get(w.replace("-USD", ""))
        if hit and hit not in seen:
            seen.add(hit)
            out.append(hit)
    return out


def main():

    # Operacional Hezilex (env-driven, defaults preservam testes/replay):
    # MERCURY_WORKERS=1 -> path sequencial legado (deterministico).
    # MERCURY_WORKERS>1 -> path paralelo com deadline global + worker timeout.
    # Dashboard :8000 exporta MERCURY_WORKERS=8, CYCLE=280s, WORKER_TIMEOUT=90s.
    # MERCURY_SYMBOLS="LTC-USD,XRP-USD,SOL-USD" -> análise dirigida do operador
    #   (SMC confirm: varre SÓ os ativos que você viu oportunidade; vazio = 39).
    workers = int(os.getenv("MERCURY_WORKERS", "1"))
    cycle_timeout_s = float(os.getenv("MERCURY_CYCLE_TIMEOUT_S", "290"))
    _wt = os.getenv("MERCURY_WORKER_TIMEOUT_S")
    worker_timeout_s = float(_wt) if _wt not in (None, "") else None
    only = _resolve_operator_symbols(os.getenv("MERCURY_SYMBOLS", ""))

    scanner = MercuryScanner()

    ranked = scanner.scan(
        workers=workers,
        cycle_timeout_s=cycle_timeout_s,
        worker_timeout_s=worker_timeout_s,
        only_symbols=only or None,
    )

    # Relatório estruturado p/ o dashboard :8000 (parse 100% confiável).
    # Impresso em stdout como bloco MACHINE_JSON (o parser do dashboard lê
    # este bloco primeiro; fallback = parse textual legado).
    try:
        import json as _json

        rep = scanner.last_scan_report
        payload = rep.to_dict() if rep is not None else {"ranked": [], "top3": []}
        print("MACHINE_JSON_BEGIN")
        print(_json.dumps(payload, default=str))
        print("MACHINE_JSON_END")
    except Exception as _e:
        print(f"MACHINE_JSON_ERROR: {_e}")


if __name__ == "__main__":

    main()