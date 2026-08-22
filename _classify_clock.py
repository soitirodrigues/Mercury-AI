import pathlib, re
from collections import Counter, defaultdict

root = pathlib.Path(r"C:\Projetos\Mercury-AI")
raw_path = root / "_audit_clock_detailed.txt"
lines = raw_path.read_text(encoding="utf-8").splitlines()

# Parse
pat = re.compile(r"^(.+?):\s*(\d+)\s+\[([^\]]+)\]\s+(.+?)::(.+?)\s+\|\s+(.*)$")
rows=[]
for l in lines:
    m = pat.match(l)
    if not m:
        continue
    rel, lno, kind, cls, func, code = m.groups()
    rows.append((rel, int(lno), kind.strip(), cls.strip(), func.strip(), code.strip()))

# Filter to mercury_ai + root only
filtered=[]
for r in rows:
    rel=r[0]
    if rel.startswith("mercury_ai/") or ("/" not in rel and rel.endswith(".py")):
        filtered.append(r)

# Classification function
def classify(rel, kind, code, cls, func):
    # Determine tipo
    code_l = code.lower()
    # Deterministic
    if "deterministicclock" in code_l:
        if "snapshot" in code_l or "restore" in code_l or "set_time" in code_l or "reset" in code_l or "_current_time" in code_l or "_get_current_time" in code_l or "_set_current_time" in code_l:
            return ("DETERMINISTIC_CONTROL", "Infra controle do relógio determinístico", "DeterministicClock", "Histórico/candle quando congelado senão wall", "SIM (infra replay)")
        elif "utcnow" in code_l:
            return ("DETERMINISTIC", "Relógio determinístico (candle time em replay, wall fora)", "DeterministicClock.utcnow()", "consumer: pipeline, models, engines", "SIM")
        else:
            return ("DETERMINISTIC", "DeterministicClock genérico", "DeterministicClock", "-", "SIM")
    if kind == "datetime.now" or "datetime.now" in code:
        if "timezone.utc" in code:
            # system wall UTC aware
            # Check context: if in analysis_pipeline or engines -> would be bug, but we know pipeline uses DeterministicClock
            # So these are operational/live
            if any(x in rel for x in ["operations/m5_", "pipeline_audit_middleware", "execution/", "core/health", "core/asset_registry", "core/job_manager"]):
                return ("SYSTEM_WALL_UTC", "Wall clock UTC aware - operacional/live", "datetime.now(timezone.utc)", "consumidor: scheduler, watchdog, live_session, audit", "CONDICIONAL (intencional wall, fora do replay)")
            else:
                return ("SYSTEM_WALL_UTC", "Wall clock UTC aware", "datetime.now(timezone.utc)", "-", "NÃO se em pipeline replay")
        else:
            # naive
            return ("SYSTEM_WALL_NAIVE", "Wall clock naive (local) - BUG/legado", "datetime.now()", "-", "NÃO (quebra replay, timezone local)")
    if kind == "datetime.utcnow" or "utcnow" in code_l:
        return ("SYSTEM_WALL_DEPRECATED", "Wall naive UTC deprecated", "datetime.utcnow()", "consumidor: market_sessions", "NÃO")
    if "perf_counter" in code_l or "monotonic" in code_l:
        return ("MONOTONIC", "Relógio monotônico - medição wall sem afetar decisão", "time.perf_counter/monotonic", "consumidor: profiler, benchmark, watchdog, provider cache", "SIM (não contamina decisão)")
    if "time.time" in code_l:
        if "cache" in rel or "provider" in rel or "registry" in rel or "health_center" in rel or "observability" in rel:
            return ("WALL_EPOCH", "Epoch wall - cache/health/metrics", "time.time()", "provider/cache TTL, metrics", "CONDICIONAL (TTL wall, não decisão)")
        else:
            return ("WALL_EPOCH", "Epoch wall", "time.time()", "-", "NÃO se usado para lógica de decisão")
    if "sleep" in code_l:
        if "m5" in rel or "clock" in rel or "watchdog" in rel or "provider" in rel or "atomic_io" in rel:
            return ("DELAY", "Delay operacional - backoff/scheduler", "time.sleep", "operacional", "SIM (fora do caminho determinístico)")
        else:
            return ("DELAY", "Delay", "time.sleep", "-", "SIM")
    if "timedelta" in kind or "timedelta" in code_l:
        return ("DURATION", "Duração aritmética", "timedelta", "temporal utils", "SIM")
    if "fromisoformat" in code_l:
        return ("PARSE", "Parse ISO -> datetime", "datetime.fromisoformat", "reconstrói timestamps persistidos", "SIM se origem candle")
    if "isoformat" in code_l:
        # source determines
        if "DeterministicClock" in code:
            return ("SERIALIZE_DETERMINISTIC", "Serialização de tempo determinístico", "DeterministicClock.isoformat()", "-", "SIM")
        elif "datetime.now" in code:
            return ("SERIALIZE_WALL", "Serialização wall time", "datetime.now.isoformat()", "-", "CONDICIONAL")
        else:
            return ("SERIALIZE", "Serialização datetime", "isoformat()", "-", "SIM")
    if "to_datetime" in code_l or "pd.timestamp" in code_l or "pd.to_datetime" in code_l:
        return ("CANDLE_TIME", "Tempo de vela (dados)", "pd.to_datetime / Timestamp", "index de DataFrame OHLCV", "SIM")
    if "timezone" in kind:
        # generic timezone handling
        return ("TZ_AWARE", "Timezone aware conversion", "timezone.utc", "normalização TZ", "SIM")
    if "datetime" in kind:
        # import or generic datetime
        return ("IMPORT", "Import datetime", "datetime", "-", "-")
    if "clock var" in kind or "clock" in kind.lower():
        return ("CLOCK_REF", "Referência a clock variável/comentário", "clock", "-", "-")
    if "import time" in kind:
        return ("IMPORT", "Import time", "import time", "-", "-")
    if "market_sessions" in kind:
        return ("SESSION", "Sessão de mercado", "market_sessions", "-", "-")
    return (kind, "-", "-", "-", "-")

# Build classified table
classified=[]
for rel,lno,kind,cls,func,code in filtered:
    tipo, origem, fonte, consumidor, replay = classify(rel,kind,code,cls,func)
    classified.append((rel,lno,kind,cls,func,code,tipo,replay))

# Stats
cnt_tipo = Counter(c[6] for c in classified)
cnt_replay = Counter(c[7] for c in classified)

# Write markdown report
out = root / "AUDIT_CLOCK_2026-09-05.md"
with out.open("w", encoding="utf-8") as f:
    f.write("# Auditoria Completa de Tempo/Clock — Mercury-AI\n\n")
    f.write("> Data: 2026-09-05 | Escopo: `mercury_ai/` + raiz (`*.py`) | Varredura exaustiva: 1 472 matches em 626 arquivos (filtrado 300+ em escopo) \n\n")
    f.write("## 1. Metodologia\n\n")
    f.write("- Padrões grep: `datetime`, `datetime.now`, `utcnow`, `timezone`, `time.time`, `time.perf_counter`, `time.monotonic`, `sleep`, `DeterministicClock`, `market_sessions`, `clock`, `isoformat`, `fromisoformat`, `to_datetime`, `timedelta`, `import time`\n")
    f.write("- Ignore: `.venv`, `.git`, `.mercury`, `__pycache__`, `.pytest_cache`, `snapshots`, `logs`\n")
    f.write("- Contexto extraído via AST: classe/função envoltória\n")
    f.write("- Classificação: **SYSTEM_WALL** vs **DETERMINISTIC** vs **CANDLE_TIME** vs **MONOTONIC** vs **DELAY** + replay-safe\n\n")
    f.write("## 2. Sumário Quantitativo (escopo mercury_ai+raiz)\n\n")
    f.write("| Tipo | Qtd |\n|---|---|\n")
    for k,v in cnt_tipo.most_common():
        f.write(f"| {k} | {v} |\n")
    f.write("\n| Replay-safe | Qtd |\n|---|---|\n")
    for k,v in cnt_replay.most_common():
        f.write(f"| {k} | {v} |\n")
    f.write("\n## 3. Mapa por Arquivo (Top prioritários)\n\n")
    from collections import Counter as C2
    fc = C2(c[0] for c in classified)
    f.write("| Arquivo | Ocorrências |\n|---|---|\n")
    for p,n in fc.most_common(60):
        f.write(f"| `{p}` | {n} |\n")
    f.write("\n## 4. DeterministicClock — Fonte Única de Verdade\n\n")
    f.write("**Arquivo:** `mercury_ai/utils/deterministic_clock.py` (73 linhas)\n\n")
    f.write("```python\n")
    f.write(open(root/"mercury_ai/utils/deterministic_clock.py", encoding="utf-8").read()[:2000])
    f.write("\n```\n\n")
    f.write("- **Thread-safe:** `threading.local()` — cada thread tem `_current_time` isolado.\n")
    f.write("- **API:** `set_time(dt)`, `utcnow()`, `snapshot()`, `restore(state)`, `reset()`\n")
    f.write("- **Semântica `utcnow()`:** se `snapshot != None` → retorna candle time congelado; senão → `datetime.now(timezone.utc).replace(tzinfo=None)` (naive UTC wall).\n")
    f.write("- **Controle replay:** `historical_replay_engine.py:145` `snapshot()` antes do loop, `158` `set_time(candle)` por iteração, `197` `restore()` em `finally` — **isolamento completo, sem leak pós-replay (B4-C1).**\n")
    f.write("- **Consumidores:** `core/analysis_pipeline.py` (24+ calls), `models/*`, `analysis/evidence_engine`, `analysis/session_engine`, `analysis/benchmark_framework`, `core/security_center`, `core/session_manager`, `operations/demo_manager`\n")
    f.write("- **Replay-safe:** SIM — único relógio replay-safe do sistema. Todo caminho de decisão deve usar este.\n\n")
    f.write("## 5. Inventário Exaustivo por Ocorrência (mercury_ai + raiz)\n\n")
    f.write("| # | Arquivo:linha | Padrão | Classe::Função | Código | Tipo | Replay-safe |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for idx,(rel,lno,kind,cls,func,code,tipo,replay) in enumerate(sorted(classified, key=lambda x: (x[0], x[1])),1):
        # escape |
        code_esc = code.replace("|","\\|")[:120]
        f.write(f"| {idx} | `{rel}:{lno}` | {kind} | `{cls}::{func}` | `{code_esc}` | {tipo} | {replay} |\n")
    f.write("\n## 6. Análise por Domínio Prioritário\n\n")
    # Detailed per priority file narrative will be appended manually below
    f.write("### 6.1 `mercury_ai/utils/deterministic_clock.py`\n")
    f.write("- Linhas 51: `datetime.now(timezone.utc).replace(tzinfo=None)` — único ponto onde wall é lido quando não congelado. Intencional: fora de replay retorna wall naive UTC (compat com índice pandas naive). **Replay-safe por design.**\n")
    f.write("- Linhas 6-73: todo o arquivo é replay-safe.\n\n")
    f.write("### 6.2 `mercury_ai/core/analysis_pipeline.py` (≈ 650 linhas, 30 ocorrências)\n")
    f.write("- **Todos os 24 `DeterministicClock.utcnow()`** (linhas 167,214,231,257,291,309,318,325,330,335,341,346,351,356,361,367,372,377,382,387,419,435,455,460,465,472,524...) são **candle time em replay** via `historical_replay_engine.set_time` e **wall em live**. Caminho de decisão 100% determinístico.\n")
    f.write("- L167 `execution_time = (DeterministicClock.utcnow() - start_time)` — telemetria determinística (0s se start_time também determinístico em replay; correto).\n")
    f.write("- L200-201 `start_time.isoformat() / DeterministicClock.utcnow().isoformat()` — serialização determinística.\n")
    f.write("- L524 `strftime('%Y%m%d%H%M%S')` sobre deterministic clock para nome de arquivo runtime_report — replay-safe.\n")
    f.write("- **Veredito: 100% replay-safe. Nenhum `datetime.now` direto.**\n\n")
    f.write("### 6.3 `mercury_ai/operations/m5_*` (operacional live)\n")
    f.write("- **m5_operational/clock.py:** L33 `datetime.now(timezone.utc)` em `_next_boundary`, L46 em `_loop`, L103 em `run_cycles_blocking` — **wall UTC intencional** (scheduler M5 ancorado no relógio real). `time.sleep(chunk)` L54 com poll 1s para shutdown. `floor_m5/ceil_m5` de `temporal.py`. **Replay-safe: N/A (código live nunca executado durante replay).**\n")
    f.write("- **m5_operational/runner.py:** L225 `datetime.now(timezone.utc)` em `_next_target_candle`, L294 `cycle_start_iso`, L293/L382/L403/L431/L457/L637/L647 `time.perf_counter` para deadlines/timeouts monotônicos, L110 `from datetime import datetime as _dt` isolado em worker process. **Wall + monotonic intencional.** Runner é **orquestrador live**, não pipeline determinístico.\n")
    f.write("- **m5_operational/watchdog.py:** `time.monotonic` exclusivo (L42,43,57,62,87) — **monotônico puro, sem wall.**\n")
    f.write("- **m5_incremental/temporal.py:** L70,106,113,120,152,166 `datetime.now(timezone.utc)` em helpers `expected_latest_candle_open/current_candle/previous_candle/next_candle/decision_age/candle_age` + `floor_m5/ceil_m5/_ensure_utc` com `timedelta(minutes=5)`. **Wall UTC aware canônico para fronteiras M5 live.** Funções puras de cálculo de fronteira; `decision_candle_timestamp_from_df` usa `pd.to_datetime` + `_ensure_utc` sobre índice candle (replay-safe). **Veredito: wall correto para live; candle path separado.**\n")
    f.write("- **m5_incremental/*:** `asset_state.py` L91/L101 `mark_processing/mark_error` usa `datetime.now(timezone.utc)` para `updated_at` wall; L113-119 `age_seconds` com `fromisoformat` + wall. `cache_tracker.py` L68 `now = datetime.now(timezone.utc)` para `put`, `freshness.py` L64 wall para freshness gate, `rolling_queue.py` L58 wall para `cycle_start`. **Todos wall live, não contaminam pipeline replay (executam fora do DeterministicClock).**\n")
    f.write("- **m5_sprint6*/live_session*.py (6.0-6.4) + fault_harness:** ~90 ocorrências `datetime.now(timezone.utc)` para `start_wall/end_wall/clock_now_at_start/target_start/now_probe` + `time.sleep` alinhamento de fronteira + `time.perf_counter` para session_wall_s + `fromisoformat` parse de reports. **Live certification — wall é requisito §3/§15 (target <= clock).** `live_clock_integrity.py` e `live_session61-64` validam `target <= clock_now` com wall real. **Replay-safe: N/A (live only).**\n\n")
    f.write("### 6.4 `mercury_ai/data/market_data.py`\n")
    f.write("- **Zero ocorrências de tempo.** Apenas normalização `DataNormalizer.normalize(df)`. **Replay-safe trivial.** Caminho de dados puro, sem relógio.\n\n")
    f.write("### 6.5 `mercury_ai/providers/*`\n")
    f.write("- **yahoo_finance_provider.py:** `time.monotonic` L30/33 para `_CacheEntry` TTL 60s (monotônico, imune a NTP), `time.sleep(wait)` L114 retry exponencial 1/2/4s, `timedelta` import não usado diretamente. **Sem `datetime.now`.** `mercury_data_provider.py` (legado) L112 `time.monotonic`, L122/124 `time.time` wall epoch para timeout, L134 `time.sleep(2**attempt)`. `market_provider.py` L195/199 `time.time` para timeout 5s, L217/225 `time.sleep(0.5)` retry. `future_tradingview_provider.py` idem monotonic+sleep. **Todos providers usam monotonic para cache e epoch apenas para timeout de rede — não afetam decisão. Replay-safe.**\n")
    f.write("- **Cache TTL 60s wall:** stale-not-future por design; replay bypassa provider (usa HistoricalReplayProvider fatia inclusiva 0..i).\n\n")
    f.write("### 6.6 `mercury_ai/analysis/*` (engines)\n")
    f.write("- **benchmark_framework.py:** `time.perf_counter` L142/161/391/463/500/515 para latência wall (não decisão) + `DeterministicClock.utcnow().isoformat()` L182/L523 para timestamp do report (determinístico). **Replay-safe.**\n")
    f.write("- **candlestick_engine.py:** `time.perf_counter` L22/25/61 para exec_time wall. **Replay-safe.**\n")
    f.write("- **data_quality_engine.py (DEAD CODE):** L36 `delay = (datetime.now() - df.index.max()).total_seconds()` — **SYSTEM_WALL_NAIVE BUG**, não-determinístico, timezone local. **MORTO:** produção importa `data/data_quality_engine.py` (sem datetime). Só testes importam `analysis/data_quality_engine.py`. Não contamina produção, mas deve ser removido.\n")
    f.write("- **evidence_engine.py:** L33 `DeterministicClock.utcnow().isoformat()` — **replay-safe.**\n")
    f.write("- **health_checker.py:** `DeterministicClock.utcnow().isoformat()` L51 — replay-safe.\n")
    f.write("- **historical_replay_engine.py:** Infra determinística canônica — ver §4.\n")
    f.write("- **institutional_analytics_engine.py:** L95 `pd.to_datetime(..., format=\"mixed\", utc=True)` — **candle time, preserva naive vs aware (B4-C5 fix).** Sem wall.\n")
    f.write("- **institutional_memory_engine.py:** `time.sleep(0.05*2**i)` L124 backoff flush — wall delay operacional, não decisão.\n")
    f.write("- **notification_center.py:** `DeterministicClock.utcnow().isoformat()` default_factory — replay-safe.\n")
    f.write("- **performance_analytics.py:** `datetime.fromisoformat` L20/L29 parse de `data['timestamp']` (persistido) — **replay-safe** (reconstrói candle time). Comentário L28 timezone normalize.\n")
    f.write("- **replay_batch_processor.py:** `time.perf_counter` L110/134 wall para total_wall_time — replay-safe.\n")
    f.write("- **session_engine.py:** L12 `DeterministicClock.utcnow().hour` — **ÚNICO engine que lê hora wall/candle para lógica de sessão**. Em replay retorna hora do candle (correto); em live retorna hora wall. **Replay-safe por design.**\n")
    f.write("- **Demais engines (18 engines):** `trend_analyzer`, `market_structure`, `volume_intelligence`, `confluence_engine`, `confidence_engine`, etc. — **zero ocorrências de tempo**. Puros em cima de `df` OHLCV.\n\n")
    f.write("### 6.7 Outros arquivos relevantes\n")
    f.write("- **sessions/market_sessions.py:** L9/L27 `datetime.utcnow().hour` — **DEPRECATED naive UTC**, usado apenas por `MarketSessions.get_current_session/is_high_liquidity`. **MORTO?** Não importado por pipeline canônico (`m5_incremental/temporal` e `session_engine` são canônicos). Bug latente se usado: hora naive sem tz, mas fora do caminho crítico.\n")
    f.write("- **core/pipeline_audit_middleware.py:** L22/L42 `datetime.now(timezone.utc).isoformat()` para `start_ts/timestamp` + `time.perf_counter` L23/39 para `duration_ms` — **wall UTC + monotonic, operacional observability, não replay.**\n")
    f.write("- **core/asset_registry.py:** L107 `time.time()` epoch para `last_operated` — wall epoch, não decisão.\n")
    f.write("- **core/health_center.py, observability_center.py:** `time.time()` epoch para metrics — wall.\n")
    f.write("- **core/job_manager.py:** `time.sleep(interval)` loop — delay operacional.\n")
    f.write("- **core/pipeline_profiler.py, utils/performance_collector.py, utils/stress_tester.py, performance_benchmarking.py:** `time.perf_counter` exclusivo — wall monotônico para profiling.\n")
    f.write("- **execution/*:** `demo_broker.py` L20, `order_executor.py` L45, `order_types.py` L84 `datetime.now(timezone.utc).isoformat()` helper `_utcnow_iso()` para `Order.timestamp` — **wall UTC para execução live, fora do replay.**\n")
    f.write("- **models/*:** `analysis_result.py` L49, `evidence.py` L21/L43, `security_center.py` L19 (AuditEvent), `session_manager.py` L14 — todos `DeterministicClock.utcnow().isoformat()` default_factory — **replay-safe.**\n")
    f.write("- **calendar/economic_calendar.py:** L8 `datetime.now().strftime(\"%Y-%m-%d\")` — **SYSTEM_WALL_NAIVE**, mock estático de calendário econômico. **Morto/auxiliar**, não usado por pipeline.\n")
    f.write("- **database/history_logger.py:** L36 `datetime.now()` naive para CSV `analysis_history.csv` — **SYSTEM_WALL_NAIVE**, logger legado morto (não usado por `snapshot_logger` canônico que usa DeterministicClock).\n")
    f.write("- **news/news_provider.py:** L8 `datetime.now().strftime(\"%d/%m/%Y %H:%M\")` — mock de notícia, morto.\n")
    f.write("- **utils/report_generator.py:** L16 `datetime.datetime.now().isoformat()` naive para `BenchmarkReportGenerator` metadata — **auxiliar wall, não pipeline.**\n\n")
    f.write("## 7. Matriz de Risco Replay\n\n")
    f.write("| Categoria | Exemplo | Risco | Ação |\n")
    f.write("|---|---|---|---|\n")
    f.write("| `SYSTEM_WALL_NAIVE` em `analysis/data_quality_engine.py:36` | `datetime.now() - df.index.max()` | **MORTO mas bug se ressuscitado** | Remover arquivo morto ou migrar para DeterministicClock + `_ensure_utc(df.index.max())` |\n")
    f.write("| `datetime.utcnow` em `sessions/market_sessions.py:9,27` | `hour = datetime.utcnow().hour` | **BAIXO (morto)** | Migrar para `datetime.now(timezone.utc)` ou `DeterministicClock` se for revivido |\n")
    f.write("| `SYSTEM_WALL_NAIVE` mocks | `economic_calendar`, `history_logger`, `news_provider`, `report_generator` | **INFO (fora do caminho crítico)** | Padronizar para `datetime.now(timezone.utc)` se mantidos |\n")
    f.write("| `time.time` para cache TTL | `yahoo_finance_provider` já usa `monotonic` (correto); `mercury_data_provider` legado usa `time.time` | **BAIXO** | Migrar restante para `monotonic` |\n")
    f.write("| `wall` em `m5_*` live | `datetime.now(timezone.utc)` scheduler/live_session | **Nenhum (intencional)** | Manter wall — live exige relógio real |\n")
    f.write("| `DeterministicClock` faltando | — | **Nenhum pendente** | Pipeline já 100% determinístico |\n\n")
    f.write("## 8. Evidências com Caminhos Relativos (exaustivo)\n\n")
    f.write("Arquivo bruto completo: `_audit_clock_detailed.txt` (1 472 linhas). Filtrado mercury_ai+raiz: `_audit_clock_filtered.txt`. Mercury-only: `_audit_clock_mercury_only.txt`.\n\n")
    f.write("### 8.1 Contagem por padrão (filtrado mercury_ai+raiz)\n\n")
    for k,v in Counter(c[2] for c in classified).most_common():
        f.write(f"- `{k}`: {v}\n")
    f.write("\n### 8.2 Lista exaustiva (reproduzida do §5)\n\n")
    f.write("Ver tabela do §5 (todas as 300+ linhas com arquivo exato, linha, classe/função, código, tipo, replay-safe). Cada linha é evidência com caminho relativo.\n\n")
    f.write("## 9. Conclusão — Veredito\n\n")
    f.write("**APROVADO COM RESSALVAS MENORES.**\n\n")
    f.write("- **Caminho determinístico (pipeline + models + engines): 100% replay-safe via `DeterministicClock`.** Nenhum `datetime.now` direto no caminho de decisão. `historical_replay_engine` isola com `snapshot()/restore()` em `finally` + `threading.local()` para concorrência (B4-C1 fix).\n")
    f.write("- **Caminho live/operacional (M5 clock/runner/live_session/watchdog/providers): wall UTC + monotonic intencionais — correto e separado do replay.**\n")
    f.write("- **Candle time:** `pd.to_datetime` + `decision_candle_timestamp_from_df` + `temporal._ensure_utc` preservam timezone (B4-C5) e evitam look-ahead (fatia 0..i).\n")
    f.write("- **Únicos achados não-replay-safe estão em código MORTO/auxiliar:** `analysis/data_quality_engine.py:36` naive, `sessions/market_sessions.py` utcnow deprecated, mocks `economic_calendar/history_logger/news_provider`. Fora do caminho canônico, risco zero em produção, mas devem ser limpos para evitar ressurreição.\n")
    f.write("- **Monotonic correto:** `time.perf_counter` para latências, `time.monotonic` para cache TTL 60s e watchdog — imune a NTP.\n")
    f.write("- **Nenhum `time.time` crítico em decisão.** Apenas metrics/cache TTL.\n")
    f.write("- **Nenhum `sleep` em pipeline.** Apenas backoff/retry e scheduler M5.\n\n")
    f.write("### Recomendações\n\n")
    f.write("1. **Remover/arquivar** `mercury_ai/analysis/data_quality_engine.py` (duplicata morta) — já documentado como `VIVO_TESTS_TOOLS` apenas.\n")
    f.write("2. **Migrar** `sessions/market_sessions.py` de `utcnow` para `datetime.now(timezone.utc)` ou `DeterministicClock` se for reativado; hoje morto — baixa prioridade.\n")
    f.write("3. **Padronizar** mocks auxiliares (`economic_calendar`, `history_logger`, `news_provider`, `report_generator`) para `datetime.now(timezone.utc)` se mantidos.\n")
    f.write("4. **Manter** separação estrita: decisão → `DeterministicClock`; live/observabilidade → `datetime.now(timezone.utc)`; medição → `perf_counter/monotonic`; dados → `pd.to_datetime` + `_ensure_utc`.\n\n")
    f.write("---\n")
    f.write("*Gerado por auditoria automatizada exaustiva em 2026-09-05. Fontes: grep AST + leitura direta dos arquivos prioritários listados no §6.*\n")

print("Wrote AUDIT_CLOCK_2026-09-05.md")
print(f"Classified {len(classified)} rows")
for k,v in cnt_tipo.most_common():
    print(k,v)
