"""
Auditoria de Performance — Fase 16.
Verifica performance, bottlenecks, otimizações:
- Complexidade algorítmica (O(n), O(n²), etc.)
- Uso de memória (memory leaks, objetos grandes)
- I/O blocking (sync vs async, batching)
- Database queries (N+1, índices, connection pooling)
- Caching strategy
- Profiling / benchmarking
- Latência crítica (order execution, signal generation)
- Resource utilization (CPU, RAM, network, disk)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.mercury_integrity_auditor.config import (
    PROJECT_ROOT,
    MERCURY_AI_DIR,
    STATUS_PASS,
    STATUS_FAIL,
    STATUS_WARNING,
    STATUS_INFO,
    STATUS_INCONCLUSIVE,
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW,
)
from tools.mercury_integrity_auditor.models import AuditFinding, AuditSection


def _check_algorithmic_complexity() -> list[AuditFinding]:
    """Verifica complexidade algorítmica potencial."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    nested_loops = []
    list_comprehensions_nested = []
    recursive_funcs = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            indent_stack = []
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                indent = len(line) - len(line.lstrip())
                
                # Detecta loops aninhados
                if stripped.startswith(('for ', 'while ')):
                    # Conta nível de indentação
                    level = indent // 4
                    if level >= 2:
                        nested_loops.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80], level))
                
                # Detecta list comprehensions aninhadas
                if '[' in stripped and 'for ' in stripped and ']' in stripped:
                    if stripped.count('for ') >= 2:
                        list_comprehensions_nested.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                
                # Detecta recursão
                if stripped.startswith('def '):
                    func_name = stripped.split('(')[0].replace('def ', '').strip()
                    # Verifica se a função chama a si mesma
                    remaining = '\n'.join(lines[i+1:i+50])
                    if f"{func_name}(" in remaining and not f"def {func_name}" in remaining:
                        recursive_funcs.append((str(f.relative_to(PROJECT_ROOT)), i+1, func_name))
        except Exception:
            pass
    
    if nested_loops:
        findings.append(AuditFinding(
            id="PERF-001",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Nested Loops Detected: {len(nested_loops)}",
            description=f"Loops aninhados (potencial O(n²+)): {nested_loops[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Revisar complexidade. Considerar: vectorização (numpy/pandas), sets/dicts para lookup O(1), algoritmos mais eficientes.",
        ))
    else:
        findings.append(AuditFinding(
            id="PERF-001",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="No Obvious Nested Loops",
            description="Nenhum loop aninhado óbvio detectado.",
            location=str(MERCURY_AI_DIR),
        ))
    
    if list_comprehensions_nested:
        findings.append(AuditFinding(
            id="PERF-002",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_INFO,
            title=f"Nested List Comprehensions: {len(list_comprehensions_nested)}",
            description=f"List comprehensions aninhadas: {list_comprehensions_nested[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Verificar se necessário. Pode ser mais legível como loops explícitos ou usar itertools.",
        ))
    
    if recursive_funcs:
        findings.append(AuditFinding(
            id="PERF-003",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Recursive Functions: {len(recursive_funcs)}",
            description=f"Funções recursivas detectadas: {recursive_funcs[:3]}. Risco de stack overflow e overhead.",
            location=str(MERCURY_AI_DIR),
            recommendation="Converter para iterativo se possível. Usar @lru_cache para memoização se recursão necessária.",
        ))
    
    return findings


def _check_memory_usage() -> list[AuditFinding]:
    """Verifica uso de memória e potenciais leaks."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    large_objects = []
    global_accumulators = []
    unclosed_resources = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                # Objetos grandes (DataFrames, arrays, listas grandes)
                if any(kw in stripped for kw in [
                    "pd.DataFrame(", "np.array(", "np.zeros(", "np.ones(",
                    "[] * ", "[0] * ", "list(range(", "dict.fromkeys("
                ]):
                    large_objects.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                
                # Acumuladores globais (listas/dicts que crescem indefinidamente)
                if any(kw in stripped for kw in [
                    ".append(", ".extend(", ".update(", "[", "]="
                ]) and not stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'with ', 'try:', 'except:', '#')):
                    # Heurística: variável global sendo modificada
                    if '=' in stripped and not stripped.startswith('    '):
                        var = stripped.split('=')[0].strip()
                        if var and (var[0].islower() or var.isupper()):
                            global_accumulators.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                
                # Recursos não fechados
                if any(kw in stripped for kw in [
                    "open(", "connect(", "session(", "cursor("
                ]) and "with " not in stripped:
                    unclosed_resources.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
        except Exception:
            pass
    
    if large_objects:
        findings.append(AuditFinding(
            id="PERF-004",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_INFO,
            title=f"Large Object Creation: {len(large_objects)}",
            description=f"Criação de objetos potencialmente grandes: {large_objects[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Verificar se objetos grandes são necessários. Usar chunking, generators, ou processamento streaming para datasets grandes.",
        ))
    
    if global_accumulators:
        findings.append(AuditFinding(
            id="PERF-005",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Potential Global Accumulators: {len(global_accumulators)}",
            description=f"Possíveis acumuladores globais (memory leak risk): {global_accumulators[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Evitar listas/dicts globais que crescem indefinidamente. Usar bounded collections, rotating buffers, ou persistência periódica.",
        ))
    
    if unclosed_resources:
        findings.append(AuditFinding(
            id="PERF-006",
            category="PERFORMANCE",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Potentially Unclosed Resources: {len(unclosed_resources)}",
            description=f"Recursos que podem não ser fechados (file handles, DB connections): {unclosed_resources[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Usar context managers (with statement) para files, connections, sessions. Implementar __enter__/__exit__ ou usar try/finally.",
        ))
    
    return findings


def _check_io_blocking() -> list[AuditFinding]:
    """Verifica I/O blocking e oportunidades de async/batching."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    sync_io = []
    async_usage = []
    batching = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            
            # I/O síncrono
            if any(kw in content for kw in [
                "requests.get", "requests.post", "urllib.request",
                "open(", "read(", "write(", "json.load", "json.dump",
                "pd.read_csv", "pd.read_parquet", "pd.read_sql",
            ]):
                sync_io.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Async usage
            if any(kw in content for kw in [
                "async def", "await ", "aiohttp", "asyncpg", "aioredis",
                "asyncio.gather", "asyncio.create_task",
            ]):
                async_usage.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Batching
            if any(kw in content for kw in [
                "batch", "bulk_", "executemany", "insert_many",
                "chunksize", "iterator", "yield",
            ]):
                batching.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if sync_io and not async_usage:
        findings.append(AuditFinding(
            id="PERF-007",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Sync I/O Without Async Alternative: {len(set(sync_io))} files",
            description=f"I/O síncrono detectado sem uso de async: {', '.join(list(set(sync_io))[:5])}",
            location=str(MERCURY_AI_DIR),
            recommendation="Considerar async/await para I/O bound operations (HTTP, DB, FS). Usar aiohttp, asyncpg, aiofiles. Batching para reduzir round-trips.",
        ))
    elif async_usage:
        findings.append(AuditFinding(
            id="PERF-007",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="Async I/O Usage Found",
            description=f"Uso de async/await detectado em: {', '.join(list(set(async_usage))[:3])}",
            location=str(MERCURY_AI_DIR),
        ))
    
    if batching:
        findings.append(AuditFinding(
            id="PERF-008",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="Batching/Streaming Patterns Found",
            description=f"Padrões de batching/streaming: {', '.join(list(set(batching))[:3])}",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_database_performance() -> list[AuditFinding]:
    """Verifica performance de database."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    db_issues = []
    connection_pooling = []
    raw_sql = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            
            # N+1 queries pattern (loop com query)
            lines = content.split('\n')
            in_loop = False
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith(('for ', 'while ')):
                    in_loop = True
                elif in_loop and any(kw in stripped for kw in [
                    "execute(", "query(", "select(", "session.query",
                    "cursor.execute", "fetchone", "fetchall"
                ]):
                    db_issues.append((str(f.relative_to(PROJECT_ROOT)), i+1, "Possible N+1: " + stripped[:60]))
                elif stripped and not stripped.startswith(' ') and not stripped.startswith('\t'):
                    in_loop = False
            
            # Connection pooling
            if any(kw in content for kw in [
                "pool", "Pool(", "connection_pool", "NullPool",
                "queuepool", "create_engine.*pool",
            ]):
                connection_pooling.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Raw SQL (potencial injection, não otimizado)
            if any(kw in content for kw in [
                "execute(\"SELECT", "execute(\"INSERT", "execute(\"UPDATE",
                "text(\"SELECT", "text(\"INSERT", "raw_sql",
            ]):
                raw_sql.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if db_issues:
        findings.append(AuditFinding(
            id="PERF-009",
            category="PERFORMANCE",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Potential N+1 Queries: {len(db_issues)}",
            description=f"Queries dentro de loops (N+1 problem): {db_issues[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Usar eager loading (joins, selectinload), batch queries, ou IN clauses. Evitar query por item em loop.",
        ))
    
    if connection_pooling:
        findings.append(AuditFinding(
            id="PERF-010",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="Connection Pooling Configured",
            description=f"Connection pooling detectado: {', '.join(list(set(connection_pooling))[:3])}",
            location=str(MERCURY_AI_DIR),
        ))
    elif raw_sql or db_issues:
        findings.append(AuditFinding(
            id="PERF-010",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Database Usage Without Connection Pooling",
            description="Uso de database detectado mas sem connection pooling explícito.",
            location=str(MERCURY_AI_DIR),
            recommendation="Configurar connection pooling (SQLAlchemy pool, psycopg2 pool). Reduz overhead de conexão.",
        ))
    
    return findings


def _check_caching() -> list[AuditFinding]:
    """Verifica estratégia de caching."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    caching = []
    lru_cache = []
    redis_cache = []
    memoization = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            
            if "@lru_cache" in content or "functools.lru_cache" in content:
                lru_cache.append(str(f.relative_to(PROJECT_ROOT)))
            if "redis" in content.lower() and ("cache" in content.lower() or "setex" in content or "get(" in content):
                redis_cache.append(str(f.relative_to(PROJECT_ROOT)))
            if any(kw in content for kw in [
                "@cache", "cachetools", "diskcache", "joblib.Memory",
                "memoize", "memoization",
            ]):
                memoization.append(str(f.relative_to(PROJECT_ROOT)))
            if any(kw in content for kw in ["cache", "Cache"]):
                caching.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    has_caching = len(lru_cache) > 0 or len(redis_cache) > 0 or len(memoization) > 0
    
    if has_caching:
        findings.append(AuditFinding(
            id="PERF-011",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="Caching Strategy Found",
            description=f"Caching: lru_cache={len(lru_cache)}, redis={len(redis_cache)}, memoization={len(memoization)}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="PERF-011",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="No Explicit Caching Strategy",
            description="Nenhuma estratégia de caching explícita detectada (lru_cache, redis, cachetools, etc.).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar caching para: computação pesada repetida, dados de mercado, configurações, resultados de ML. Usar @lru_cache para funções puras, Redis para distributed cache.",
        ))
    
    return findings


def _check_profiling_benchmarking() -> list[AuditFinding]:
    """Verifica profiling e benchmarking."""
    findings = []
    
    profile_files = list(MERCURY_AI_DIR.rglob("*profile*.py"))
    profile_files += list(MERCURY_AI_DIR.rglob("*benchmark*.py"))
    profile_files += list(PROJECT_ROOT.rglob("*profile*.py"))
    profile_files += list(PROJECT_ROOT.rglob("*benchmark*.py"))
    
    # Scripts de benchmark
    bench_scripts = list(PROJECT_ROOT.rglob("run_*benchmark*.py"))
    bench_scripts += list(PROJECT_ROOT.rglob("*benchmark*.py"))
    perf_audit = PROJECT_ROOT / "PERFORMANCE_AUDIT.md"
    perf_audit_final = PROJECT_ROOT / "PERFORMANCE_AUDIT_FINAL.md"
    perf_bench = PROJECT_ROOT / "PERFORMANCE_BENCHMARK_FINAL.md"
    
    has_profiling = len(profile_files) > 0 or len(bench_scripts) > 0
    has_docs = perf_audit.exists() or perf_audit_final.exists() or perf_bench.exists()
    
    if has_profiling or has_docs:
        findings.append(AuditFinding(
            id="PERF-012",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="Profiling/Benchmarking Found",
            description=f"Módulos: {len(profile_files)}, Scripts: {len(bench_scripts)}, Docs: {has_docs}",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="PERF-012",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="No Profiling/Benchmarking Infrastructure",
            description="Não há infraestrutura de profiling/benchmarking (scripts, módulos, docs).",
            location=str(PROJECT_ROOT),
            recommendation="Adicionar: pytest-benchmark, cProfile/snakeviz, py-spy, memory_profiler. Criar benchmarks para critical paths (signal gen, order exec, risk calc).",
        ))
    
    return findings


def _check_critical_latency() -> list[AuditFinding]:
    """Verifica paths de latência crítica."""
    findings = []
    
    # Paths críticos típicos em trading
    critical_paths = [
        ("signal", "generation", "signal_generation"),
        ("order", "execution", "order_execution"),
        ("risk", "check", "risk_check"),
        ("position", "update", "position_update"),
        ("pnl", "calculation", "pnl_calculation"),
        ("market", "data", "market_data"),
    ]
    
    found_paths = []
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            for kw1, kw2, name in critical_paths:
                if kw1 in content and kw2 in content:
                    found_paths.append(name)
        except Exception:
            pass
    
    found_paths = list(set(found_paths))
    
    if found_paths:
        findings.append(AuditFinding(
            id="PERF-013",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_INFO,
            title=f"Critical Latency Paths Identified: {len(found_paths)}",
            description=f"Paths críticos detectados: {', '.join(found_paths)}. Verificar latência < 1ms para order exec, < 10ms para signal gen.",
            location=str(MERCURY_AI_DIR),
            recommendation="Instrumentar latência em paths críticos. Usar time.perf_counter() para medir. Target: order exec < 1ms, signal gen < 10ms, risk check < 5ms.",
        ))
    else:
        findings.append(AuditFinding(
            id="PERF-013",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Critical Latency Paths Not Identified",
            description="Não foi possível identificar paths de latência crítica (signal, order, risk, position, pnl).",
            location=str(MERCURY_AI_DIR),
            recommendation="Mapear e instrumentar critical paths. Definir SLAs de latência. Adicionar métricas/alertas.",
        ))
    
    return findings


def _check_resource_utilization() -> list[AuditFinding]:
    """Verifica utilização de recursos."""
    findings = []
    
    # Verifica se há monitoring de recursos
    monitoring_files = list(MERCURY_AI_DIR.rglob("*monitor*.py"))
    monitoring_files += list(MERCURY_AI_DIR.rglob("*metric*.py"))
    monitoring_files += list(MERCURY_AI_DIR.rglob("*health*.py"))
    monitoring_files += list(PROJECT_ROOT.rglob("*monitor*.py"))
    monitoring_files += list(PROJECT_ROOT.rglob("*metric*.py"))
    
    # Verifica requirements para monitoring libs
    req_txt = PROJECT_ROOT / "requirements.txt"
    has_prometheus = False
    has_psutil = False
    has_datadog = False
    
    if req_txt.exists():
        content = req_txt.read_text(encoding="utf-8").lower()
        has_prometheus = "prometheus" in content
        has_psutil = "psutil" in content
        has_datadog = "datadog" in content or "ddtrace" in content
    
    has_monitoring = len(monitoring_files) > 0 or has_prometheus or has_psutil or has_datadog
    
    if has_monitoring:
        findings.append(AuditFinding(
            id="PERF-014",
            category="PERFORMANCE",
            severity=LOW,
            status=STATUS_PASS,
            title="Resource Monitoring Found",
            description=f"Monitoring: modules={len(monitoring_files)}, prometheus={has_prometheus}, psutil={has_psutil}, datadog={has_datadog}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="PERF-014",
            category="PERFORMANCE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="No Resource Monitoring",
            description="Não há monitoring de recursos (CPU, RAM, disk, network, GC).",
            location=str(MERCURY_AI_DIR),
            recommendation="Adicionar: psutil para system metrics, prometheus_client para export, health checks. Alertas para CPU>80%, RAM>85%, GC pauses>100ms.",
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de performance."""
    section = AuditSection(
        name="16. Performance Audit",
        description="Verifica performance: complexidade algorítmica, memória, I/O, DB, caching, profiling, latência crítica, recursos",
    )
    
    all_findings = []
    all_findings.extend(_check_algorithmic_complexity())
    all_findings.extend(_check_memory_usage())
    all_findings.extend(_check_io_blocking())
    all_findings.extend(_check_database_performance())
    all_findings.extend(_check_caching())
    all_findings.extend(_check_profiling_benchmarking())
    all_findings.extend(_check_critical_latency())
    all_findings.extend(_check_resource_utilization())
    
    section.findings = all_findings
    
    has_fail = any(f.status == STATUS_FAIL for f in all_findings)
    has_warning = any(f.status == STATUS_WARNING for f in all_findings)
    
    if has_fail:
        section.status = STATUS_FAIL
    elif has_warning:
        section.status = STATUS_WARNING
    else:
        section.status = STATUS_PASS
    
    return section