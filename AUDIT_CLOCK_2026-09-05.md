# Auditoria Completa de Tempo/Clock — Mercury-AI

> Data: 2026-09-05 | Escopo: `mercury_ai/` + raiz (`*.py`) | Varredura exaustiva: 1 472 matches em 626 arquivos (filtrado 300+ em escopo) 

## 1. Metodologia

- Padrões grep: `datetime`, `datetime.now`, `utcnow`, `timezone`, `time.time`, `time.perf_counter`, `time.monotonic`, `sleep`, `DeterministicClock`, `market_sessions`, `clock`, `isoformat`, `fromisoformat`, `to_datetime`, `timedelta`, `import time`
- Ignore: `.venv`, `.git`, `.mercury`, `__pycache__`, `.pytest_cache`, `snapshots`, `logs`
- Contexto extraído via AST: classe/função envoltória
- Classificação: **SYSTEM_WALL** vs **DETERMINISTIC** vs **CANDLE_TIME** vs **MONOTONIC** vs **DELAY** + replay-safe

## 2. Sumário Quantitativo (escopo mercury_ai+raiz)

| Tipo | Qtd |
|---|---|
| CLOCK_REF | 188 |
| DETERMINISTIC | 132 |
| IMPORT | 128 |
| DETERMINISTIC_CONTROL | 113 |
| SYSTEM_WALL_UTC | 67 |
| DELAY | 62 |
| MONOTONIC | 61 |
| SERIALIZE | 57 |
| DURATION | 45 |
| WALL_EPOCH | 34 |
| TZ_AWARE | 30 |
| PARSE | 28 |
| CANDLE_TIME | 13 |
| SYSTEM_WALL_NAIVE | 11 |
| SYSTEM_WALL_DEPRECATED | 6 |
| SESSION | 2 |

| Replay-safe | Qtd |
|---|---|
| - | 318 |
| SIM | 315 |
| SIM (infra replay) | 113 |
| CONDICIONAL (intencional wall, fora do replay) | 66 |
| SIM (não contamina decisão) | 61 |
| SIM se origem candle | 28 |
| NÃO se usado para lógica de decisão | 27 |
| SIM (fora do caminho determinístico) | 24 |
| NÃO (quebra replay, timezone local) | 11 |
| CONDICIONAL (TTL wall, não decisão) | 7 |
| NÃO | 6 |
| NÃO se em pipeline replay | 1 |

## 3. Mapa por Arquivo (Top prioritários)

| Arquivo | Ocorrências |
|---|---|
| `s32_c_parallel_clock_isolation.py` | 112 |
| `mercury_ai/operations/m5_sprint64/live_session64.py` | 40 |
| `test_clock_isolation.py` | 39 |
| `s32_c_parallel_clock_isolation_focused.py` | 38 |
| `test_s31_04.py` | 38 |
| `mercury_ai/core/analysis_pipeline.py` | 35 |
| `mercury_ai/operations/m5_sprint63/fault_harness.py` | 34 |
| `test_historical_replay_integration.py` | 33 |
| `s32_07_parallel_replay_stress.py` | 32 |
| `mercury_ai/operations/m5_sprint6/live_session.py` | 28 |
| `mercury_ai/operations/m5_sprint61/live_session61.py` | 26 |
| `mercury_ai/operations/m5_sprint62/live_session62.py` | 26 |
| `mercury_ai/operations/m5_sprint63/live_session63.py` | 24 |
| `mercury_ai/analysis/tests/test_historical_replay_engine.py` | 19 |
| `test_s31_03_parallel_replay.py` | 19 |
| `mercury_ai/operations/m5_operational/runner.py` | 18 |
| `mercury_ai/operations/m5_incremental/temporal.py` | 16 |
| `test_interleavings.py` | 16 |
| `test_s31_03.py` | 16 |
| `mercury_ai/analysis/benchmark_framework.py` | 10 |
| `mercury_ai/operations/m5_operational/clock.py` | 10 |
| `test_s31_14.py` | 10 |
| `s32_e3_task2_g_deterministic.py` | 9 |
| `s32_e3_task2_g_natural.py` | 9 |
| `test_s31_07.py` | 9 |
| `_audit_script.py` | 8 |
| `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py` | 8 |
| `run_decision_scenarios.py` | 8 |
| `s32_e3_bridge_closure_execution.py` | 8 |
| `s32_e3_f04_close_test.py` | 8 |
| `test_s31_17.py` | 8 |
| `mercury_ai/analysis/historical_replay_engine.py` | 7 |
| `mercury_ai/operations/m5_incremental/asset_state.py` | 7 |
| `s32_e3_task2_g_extended.py` | 7 |
| `mercury_ai/core/pipeline_audit_middleware.py` | 6 |
| `mercury_ai/operations/m5_incremental/cache_tracker.py` | 6 |
| `mercury_ai/operations/m5_incremental/freshness.py` | 6 |
| `mercury_ai/operations/m5_operational/watchdog.py` | 6 |
| `test_s31_05.py` | 6 |
| `mercury_ai/analysis/tests/test_institutional_analytics_engine.py` | 5 |
| `mercury_ai/data/mercury_data_provider.py` | 5 |
| `mercury_ai/operations/m5_incremental/rolling_queue.py` | 5 |
| `mercury_ai/operations/m5_sprint64/audit.py` | 5 |
| `mercury_ai/providers/market_provider.py` | 5 |
| `mercury_ai/providers/yahoo_finance_provider.py` | 5 |
| `performance_benchmarking.py` | 5 |
| `run_determinism_test.py` | 5 |
| `test_s31_06.py` | 5 |
| `test_s31_15.py` | 5 |
| `test_s31_16.py` | 5 |
| `mercury_ai/analysis/candlestick_engine.py` | 4 |
| `mercury_ai/analysis/performance_analytics.py` | 4 |
| `mercury_ai/analysis/replay_batch_processor.py` | 4 |
| `mercury_ai/providers/future_tradingview_provider.py` | 4 |
| `s32_02e_crash_harness_signals.py` | 4 |
| `s32_03e_post_replace_crash_boundary.py` | 4 |
| `s32_e3_task1_f_test.py` | 4 |
| `test_gate3.py` | 4 |
| `test_gate3_buy.py` | 4 |
| `mercury_ai/analysis/health_checker.py` | 3 |

## 4. DeterministicClock — Fonte Única de Verdade

**Arquivo:** `mercury_ai/utils/deterministic_clock.py` (73 linhas)

```python
import threading
from datetime import datetime, timezone
from typing import Optional


class DeterministicClock:
    """Relógio determinístico thread-safe para análise reproduzível.

    Cada thread possui seu próprio estado de tempo via threading.local(),
    garantindo isolamento completo entre threads concurrentes.
    """

    _local = threading.local()

    @classmethod
    def _get_current_time(cls) -> Optional[datetime]:
        """Obtém o _current_time específico desta thread."""
        # Use object getattr with default to safely access thread-local storage
        return getattr(cls._local, '_current_time', None)

    @classmethod
    def _set_current_time(cls, dt: datetime) -> None:
        """Define o _current_time específico desta thread via threading.local().

        O threading.local() garante que cada thread tenha sua própria instância
        de _current_time, evitando contaminação entre threads concurrentes.
        """
        # Set the attribute on the thread-local storage
        # This ensures each thread has its own _current_time
        cls._local._current_time = dt

    @classmethod
    def set_time(cls, dt: datetime) -> None:
        """Define o tempo determinístico para a thread corrente.

        A thread corrente passa a observar este tempo isoladamente
        das demais threads, até que seja chamado reset() ou restore().
        """
        cls._set_current_time(dt)

    @classmethod
    def utcnow(cls) -> datetime:
        """Retorna o tempo da thread corrente, ou o relógio real se não houver tempo definidio.

        Se a thread corrente tiver um _current_time definido (via set_time),
        retorna-o. Caso contrário, retorna o relógio real UTC.
        """
        current = cls._get_current_time()
        if current is not None:
            return current
        return datetime.now(timezone.utc).replace(tzinfo=None)

    @classmethod
    def reset(cls) -> None:
        """Limpa o tempo determinístico da thread corrente, voltando 
```

- **Thread-safe:** `threading.local()` — cada thread tem `_current_time` isolado.
- **API:** `set_time(dt)`, `utcnow()`, `snapshot()`, `restore(state)`, `reset()`
- **Semântica `utcnow()`:** se `snapshot != None` → retorna candle time congelado; senão → `datetime.now(timezone.utc).replace(tzinfo=None)` (naive UTC wall).
- **Controle replay:** `historical_replay_engine.py:145` `snapshot()` antes do loop, `158` `set_time(candle)` por iteração, `197` `restore()` em `finally` — **isolamento completo, sem leak pós-replay (B4-C1).**
- **Consumidores:** `core/analysis_pipeline.py` (24+ calls), `models/*`, `analysis/evidence_engine`, `analysis/session_engine`, `analysis/benchmark_framework`, `core/security_center`, `core/session_manager`, `operations/demo_manager`
- **Replay-safe:** SIM — único relógio replay-safe do sistema. Todo caminho de decisão deve usar este.

## 5. Inventário Exaustivo por Ocorrência (mercury_ai + raiz)

| # | Arquivo:linha | Padrão | Classe::Função | Código | Tipo | Replay-safe |
|---|---|---|---|---|---|---|
| 1 | `_audit_script.py:24` | timezone | `-::-` | `("timezone",               re.compile(r"\btimezone\b")),` | TZ_AWARE | SIM |
| 2 | `_audit_script.py:25` | timedelta | `-::-` | `("timedelta",              re.compile(r"\btimedelta\b")),` | DURATION | SIM |
| 3 | `_audit_script.py:27` | pd.to_datetime | `-::-` | `("pd.to_datetime",         re.compile(r"pd\.to_datetime\|pandas\.to_datetime\|to_datetime\s*\(")),` | CANDLE_TIME | SIM |
| 4 | `_audit_script.py:28` | pd.Timestamp | `-::-` | `("pd.Timestamp",           re.compile(r"pd\.Timestamp\|pd\.to_datetime")),` | CANDLE_TIME | SIM |
| 5 | `_audit_script.py:34` | sleep( | `-::-` | `("sleep(",                 re.compile(r"(?<!\.)\bsleep\s*\(")),  # bare sleep (from time import sleep)` | DELAY | SIM |
| 6 | `_audit_script.py:35` | DeterministicClock | `-::-` | `("DeterministicClock",     re.compile(r"\bDeterministicClock\b")),` | DETERMINISTIC | SIM |
| 7 | `_audit_script.py:36` | market_sessions | `-::-` | `("market_sessions",        re.compile(r"market_sessions")),` | SESSION | - |
| 8 | `_audit_script.py:37` | clock var | `-::-` | `("clock var",              re.compile(r"\bclock\b", re.I)),` | CLOCK_REF | - |
| 9 | `debug_atomic_insights.py:10` | import time | `-::-` | `import time` | IMPORT | - |
| 10 | `debug_atomic_test2.py:5` | import time | `-::-` | `import time` | IMPORT | - |
| 11 | `debug_atomic_test2.py:21` | time.time | `-::-` | `write_data = {"test": "new_data", "timestamp": time.time()}` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 12 | `debug_exact.py:10` | import time | `-::-` | `import time` | IMPORT | - |
| 13 | `debug_keyerror.py:6` | import time | `-::-` | `import time` | IMPORT | - |
| 14 | `debug_keyerror.py:33` | time.sleep | `-::-` | `time.sleep(1)` | DELAY | SIM |
| 15 | `debug_path.py:8` | import time | `-::-` | `import time` | IMPORT | - |
| 16 | `debug_result.py:6` | import time | `-::-` | `import time` | IMPORT | - |
| 17 | `debug_result.py:38` | time.sleep | `-::-` | `time.sleep(1)` | DELAY | SIM |
| 18 | `debug_result2.py:6` | import time | `-::-` | `import time` | IMPORT | - |
| 19 | `debug_result2.py:37` | time.sleep | `-::-` | `time.sleep(1)` | DELAY | SIM |
| 20 | `debug_test.py:9` | import time | `-::-` | `import time` | IMPORT | - |
| 21 | `f_test_final.py:29` | time.sleep | `-::-` | `time.sleep(0.01)  # Small delay to ensure we're before os.replace` | DELAY | SIM |
| 22 | `h_test_final.py:29` | time.sleep | `-::-` | `time.sleep(0.005)` | DELAY | SIM |
| 23 | `mercury_ai/analysis/benchmark_framework.py:15` | import time | `-::-` | `import time` | IMPORT | - |
| 24 | `mercury_ai/analysis/benchmark_framework.py:30` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 25 | `mercury_ai/analysis/benchmark_framework.py:142` | time.perf_counter | `MercuryBenchmarkFramework::_run_single_symbol` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 26 | `mercury_ai/analysis/benchmark_framework.py:161` | time.perf_counter | `MercuryBenchmarkFramework::_run_single_symbol` | `end_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 27 | `mercury_ai/analysis/benchmark_framework.py:182` | isoformat | `MercuryBenchmarkFramework::_run_single_symbol` | `timestamp=DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 28 | `mercury_ai/analysis/benchmark_framework.py:391` | time.perf_counter | `MercuryBenchmarkFramework::run_benchmark` | `wall_start = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 29 | `mercury_ai/analysis/benchmark_framework.py:463` | time.perf_counter | `MercuryBenchmarkFramework::run_benchmark` | `wall_end = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 30 | `mercury_ai/analysis/benchmark_framework.py:500` | time.perf_counter | `MercuryBenchmarkFramework::run_quick_benchmark` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 31 | `mercury_ai/analysis/benchmark_framework.py:515` | time.perf_counter | `MercuryBenchmarkFramework::run_quick_benchmark` | `end_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 32 | `mercury_ai/analysis/benchmark_framework.py:523` | isoformat | `MercuryBenchmarkFramework::run_quick_benchmark` | `timestamp=DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 33 | `mercury_ai/analysis/candlestick_engine.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 34 | `mercury_ai/analysis/candlestick_engine.py:22` | time.perf_counter | `CandlestickEngine::analyze` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 35 | `mercury_ai/analysis/candlestick_engine.py:25` | time.perf_counter | `CandlestickEngine::analyze` | `exec_time = time.perf_counter() - start_time` | MONOTONIC | SIM (não contamina decisão) |
| 36 | `mercury_ai/analysis/candlestick_engine.py:61` | time.perf_counter | `CandlestickEngine::analyze` | `exec_time = time.perf_counter() - start_time` | MONOTONIC | SIM (não contamina decisão) |
| 37 | `mercury_ai/analysis/data_quality_engine.py:3` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 38 | `mercury_ai/analysis/data_quality_engine.py:36` | datetime.now | `DataQualityEngine::generate_report` | `delay = (datetime.now() - df.index.max()).total_seconds()` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 39 | `mercury_ai/analysis/evidence_engine.py:8` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 40 | `mercury_ai/analysis/evidence_engine.py:33` | isoformat | `EvidenceEngine::process` | `timestamp=DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 41 | `mercury_ai/analysis/health_checker.py:8` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 42 | `mercury_ai/analysis/health_checker.py:35` | clock var | `HealthChecker::check` | `"Clock": "OK",` | CLOCK_REF | - |
| 43 | `mercury_ai/analysis/health_checker.py:51` | isoformat | `HealthChecker::check` | `timestamp=DeterministicClock.utcnow().isoformat()` | DETERMINISTIC | SIM |
| 44 | `mercury_ai/analysis/historical_replay_engine.py:21` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 45 | `mercury_ai/analysis/historical_replay_engine.py:94` | import time | `HistoricalReplayEngine::run_replay` | `import time as time_module` | IMPORT | - |
| 46 | `mercury_ai/analysis/historical_replay_engine.py:143` | clock var | `HistoricalReplayEngine::run_replay` | `# que o clock NÃO permaneça congelado em timestamp histórico após o` | CLOCK_REF | - |
| 47 | `mercury_ai/analysis/historical_replay_engine.py:145` | DeterministicClock | `HistoricalReplayEngine::run_replay` | `clock_state = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 48 | `mercury_ai/analysis/historical_replay_engine.py:157` | pd.to_datetime | `HistoricalReplayEngine::run_replay` | `current_time = pd.to_datetime(timestamps[i]).to_pydatetime()` | CANDLE_TIME | SIM |
| 49 | `mercury_ai/analysis/historical_replay_engine.py:158` | DeterministicClock | `HistoricalReplayEngine::run_replay` | `DeterministicClock.set_time(current_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 50 | `mercury_ai/analysis/historical_replay_engine.py:197` | DeterministicClock | `HistoricalReplayEngine::run_replay` | `DeterministicClock.restore(clock_state)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 51 | `mercury_ai/analysis/institutional_analytics_engine.py:6` | timedelta | `-::-` | `from datetime import datetime, timedelta` | DURATION | SIM |
| 52 | `mercury_ai/analysis/institutional_analytics_engine.py:86` | timezone | `InstitutionalAnalyticsEngine::_load_data` | `# naive UTC (tempo real) e timezone-aware (replay com dataset` | TZ_AWARE | SIM |
| 53 | `mercury_ai/analysis/institutional_analytics_engine.py:95` | pd.to_datetime | `InstitutionalAnalyticsEngine::_load_data` | `df["timestamp"] = pd.to_datetime(` | CANDLE_TIME | SIM |
| 54 | `mercury_ai/analysis/institutional_memory_engine.py:7` | import time | `-::-` | `import time` | IMPORT | - |
| 55 | `mercury_ai/analysis/institutional_memory_engine.py:124` | time.sleep | `InstitutionalMemoryEngine::flush` | `time.sleep(0.05 * (2 ** i))` | DELAY | SIM |
| 56 | `mercury_ai/analysis/live_monitor.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 57 | `mercury_ai/analysis/notification_center.py:4` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 58 | `mercury_ai/analysis/notification_center.py:11` | isoformat | `Notification::-` | `timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())` | DETERMINISTIC | SIM |
| 59 | `mercury_ai/analysis/performance_analytics.py:6` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 60 | `mercury_ai/analysis/performance_analytics.py:20` | datetime.fromisoformat | `PerformanceAnalytics::analyze_performance` | `entry_time = datetime.fromisoformat(data['timestamp'])` | PARSE | SIM se origem candle |
| 61 | `mercury_ai/analysis/performance_analytics.py:28` | timezone | `PerformanceAnalytics::analyze_performance` | `# Normalize entry_time to match df index timezone` | TZ_AWARE | SIM |
| 62 | `mercury_ai/analysis/performance_analytics.py:29` | datetime.fromisoformat | `PerformanceAnalytics::analyze_performance` | `entry_time = datetime.fromisoformat(data['timestamp'])` | PARSE | SIM se origem candle |
| 63 | `mercury_ai/analysis/replay_batch_processor.py:14` | import time | `-::-` | `import time` | IMPORT | - |
| 64 | `mercury_ai/analysis/replay_batch_processor.py:110` | time.perf_counter | `ReplayBatchProcessor::run_batch` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 65 | `mercury_ai/analysis/replay_batch_processor.py:134` | time.perf_counter | `ReplayBatchProcessor::run_batch` | `total_wall_time = time.perf_counter() - start_time` | MONOTONIC | SIM (não contamina decisão) |
| 66 | `mercury_ai/analysis/replay_batch_processor.py:170` | import time | `ReplayBatchProcessor::_run_single_symbol` | `import time as time_module` | IMPORT | - |
| 67 | `mercury_ai/analysis/session_engine.py:2` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 68 | `mercury_ai/analysis/session_engine.py:12` | DeterministicClock | `SessionEngine::analyze` | `hour = DeterministicClock.utcnow().hour` | DETERMINISTIC | SIM |
| 69 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:12` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 70 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:189` | DeterministicClock | `TestDeterministicClockIsolation::-` | `"""B4-C1: DeterministicClock deve ser isolado durante o replay.` | DETERMINISTIC | SIM |
| 71 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:192` | clock var | `TestDeterministicClockIsolation::-` | `após run_replay, o clock NÃO pode permanecer no passado (contaminação` | CLOCK_REF | - |
| 72 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:197` | clock var | `TestDeterministicClockIsolation::test_clock_restored_after_normal_replay` | `"""A) Restauração normal: clock volta ao relógio real após replay."""` | CLOCK_REF | - |
| 73 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:198` | DeterministicClock | `TestDeterministicClockIsolation::test_clock_restored_after_normal_replay` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 74 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:202` | DeterministicClock | `TestDeterministicClockIsolation::test_clock_restored_after_normal_replay` | `assert DeterministicClock._current_time is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 75 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:205` | clock var | `TestDeterministicClockIsolation::test_clock_restored_after_exception` | `"""B) Restauração após exceção: clock volta ao real mesmo com erro.` | CLOCK_REF | - |
| 76 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:209` | DeterministicClock | `TestDeterministicClockIsolation::test_clock_restored_after_exception` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 77 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:229` | DeterministicClock | `TestDeterministicClockIsolation::test_clock_restored_after_exception` | `assert DeterministicClock._current_time is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 78 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:233` | DeterministicClock | `TestDeterministicClockIsolation::test_double_replay_deterministic_and_clock_restored` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 79 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:237` | DeterministicClock | `TestDeterministicClockIsolation::test_double_replay_deterministic_and_clock_restored` | `clock_after_a = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 80 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:240` | DeterministicClock | `TestDeterministicClockIsolation::test_double_replay_deterministic_and_clock_restored` | `clock_after_b = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 81 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:255` | DeterministicClock | `TestDeterministicClockIsolation::test_no_contamination_of_normal_execution` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 82 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:259` | DeterministicClock | `TestDeterministicClockIsolation::test_no_contamination_of_normal_execution` | `assert DeterministicClock._current_time is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 83 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:263` | DeterministicClock | `TestDeterministicClockIsolation::test_no_contamination_of_normal_execution` | `assert DeterministicClock._current_time is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 84 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:267` | DeterministicClock | `TestDeterministicClockIsolation::test_no_contamination_of_normal_execution` | `assert DeterministicClock._current_time is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 85 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:270` | clock var | `TestDeterministicClockIsolation::test_empty_replay_does_not_touch_clock` | `"""Replay vazio (dados insuficientes) não altera o estado do clock."""` | CLOCK_REF | - |
| 86 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:271` | DeterministicClock | `TestDeterministicClockIsolation::test_empty_replay_does_not_touch_clock` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 87 | `mercury_ai/analysis/tests/test_historical_replay_engine.py:282` | DeterministicClock | `TestDeterministicClockIsolation::test_empty_replay_does_not_touch_clock` | `assert DeterministicClock._current_time is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 88 | `mercury_ai/analysis/tests/test_institutional_analytics_engine.py:4` | pd.to_datetime | `-::-` | `Valida a correção R2 (B4-C5): `pd.to_datetime` com `format="mixed"` + `utc=True`` | CANDLE_TIME | SIM |
| 89 | `mercury_ai/analysis/tests/test_institutional_analytics_engine.py:85` | pd.Timestamp | `-::test_valid_timestamp_not_lost` | `assert df.loc[0, "timestamp"] == pd.Timestamp(expected_naive_utc)` | CANDLE_TIME | SIM |
| 90 | `mercury_ai/analysis/tests/test_institutional_analytics_engine.py:151` | pd.Timestamp | `-::test_mixed_timestamps_all_preserved` | `expected_order = sorted(pd.Timestamp(e) for _t, e in mix)` | CANDLE_TIME | SIM |
| 91 | `mercury_ai/analysis/tests/test_institutional_analytics_engine.py:157` | pd.Timestamp | `-::test_mixed_timestamps_all_preserved` | `epochs_in = {pd.Timestamp(ts).timestamp() for ts, _exp in mix}` | CANDLE_TIME | SIM |
| 92 | `mercury_ai/analysis/tests/test_institutional_analytics_engine.py:158` | pd.Timestamp | `-::test_mixed_timestamps_all_preserved` | `epochs_out = {pd.Timestamp(t).timestamp() for t in df["timestamp"]}` | CANDLE_TIME | SIM |
| 93 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:2` | timezone | `-::-` | `"""B4-C5 - Testes de replay com dataset timezone-aware (snapshot save).` | TZ_AWARE | SIM |
| 94 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:5` | DeterministicClock | `-::-` | `(ex.: Europe/London) faz o DeterministicClock virar tz-aware e a pipeline` | DETERMINISTIC | SIM |
| 95 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:8` | clock var | `-::-` | `preservar o determinismo e restaurar o clock ao final.` | CLOCK_REF | - |
| 96 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:19` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 97 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:79` | clock var | `-::test_replay_tz_aware_dataset_no_crash` | `# Clock determinístico restaurado ao final (relógio real = None).` | CLOCK_REF | - |
| 98 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:80` | DeterministicClock | `-::test_replay_tz_aware_dataset_no_crash` | `assert DeterministicClock.snapshot() is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 99 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:96` | DeterministicClock | `-::test_replay_naive_dataset_no_crash` | `assert DeterministicClock.snapshot() is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 100 | `mercury_ai/analysis/tests/test_replay_tzaware_snapshot.py:114` | DeterministicClock | `-::test_replay_tz_aware_deterministic` | `assert DeterministicClock.snapshot() is None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 101 | `mercury_ai/brain/tests/test_mercury_decision_benchmark.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 102 | `mercury_ai/brain/tests/test_mercury_decision_benchmark.py:63` | time.time | `-::test_decision_engine_benchmark` | `start_time = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 103 | `mercury_ai/brain/tests/test_mercury_decision_benchmark.py:66` | time.time | `-::test_decision_engine_benchmark` | `end_time = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 104 | `mercury_ai/calendar/economic_calendar.py:1` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 105 | `mercury_ai/calendar/economic_calendar.py:8` | datetime.now | `EconomicCalendar::get_events` | `today = datetime.now().strftime("%Y-%m-%d")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 106 | `mercury_ai/core/analysis_pipeline.py:6` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 107 | `mercury_ai/core/analysis_pipeline.py:167` | DeterministicClock | `AnalysisPipeline::_record_telemetry` | `execution_time = (DeterministicClock.utcnow() - start_time).total_seconds()` | DETERMINISTIC | SIM |
| 108 | `mercury_ai/core/analysis_pipeline.py:200` | isoformat | `AnalysisPipeline::_record_telemetry` | `start_time=start_time.isoformat(),` | SERIALIZE | SIM |
| 109 | `mercury_ai/core/analysis_pipeline.py:201` | isoformat | `AnalysisPipeline::_record_telemetry` | `end_time=DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 110 | `mercury_ai/core/analysis_pipeline.py:214` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 111 | `mercury_ai/core/analysis_pipeline.py:231` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 112 | `mercury_ai/core/analysis_pipeline.py:257` | isoformat | `AnalysisPipeline::analyze` | `timestamp=DeterministicClock.utcnow().isoformat(), asset=symbol, timeframe=DEFAULT_TIMEFRAME,` | DETERMINISTIC | SIM |
| 113 | `mercury_ai/core/analysis_pipeline.py:291` | isoformat | `AnalysisPipeline::analyze` | `timestamp=DeterministicClock.utcnow().isoformat(), asset=symbol, timeframe=DEFAULT_TIMEFRAME,` | DETERMINISTIC | SIM |
| 114 | `mercury_ai/core/analysis_pipeline.py:309` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 115 | `mercury_ai/core/analysis_pipeline.py:318` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 116 | `mercury_ai/core/analysis_pipeline.py:325` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 117 | `mercury_ai/core/analysis_pipeline.py:330` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 118 | `mercury_ai/core/analysis_pipeline.py:335` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 119 | `mercury_ai/core/analysis_pipeline.py:341` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 120 | `mercury_ai/core/analysis_pipeline.py:346` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 121 | `mercury_ai/core/analysis_pipeline.py:351` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 122 | `mercury_ai/core/analysis_pipeline.py:356` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 123 | `mercury_ai/core/analysis_pipeline.py:361` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 124 | `mercury_ai/core/analysis_pipeline.py:367` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 125 | `mercury_ai/core/analysis_pipeline.py:372` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 126 | `mercury_ai/core/analysis_pipeline.py:377` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 127 | `mercury_ai/core/analysis_pipeline.py:382` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 128 | `mercury_ai/core/analysis_pipeline.py:387` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 129 | `mercury_ai/core/analysis_pipeline.py:419` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 130 | `mercury_ai/core/analysis_pipeline.py:435` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 131 | `mercury_ai/core/analysis_pipeline.py:455` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 132 | `mercury_ai/core/analysis_pipeline.py:460` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 133 | `mercury_ai/core/analysis_pipeline.py:465` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 134 | `mercury_ai/core/analysis_pipeline.py:472` | DeterministicClock | `AnalysisPipeline::analyze` | `start = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 135 | `mercury_ai/core/analysis_pipeline.py:475` | isoformat | `AnalysisPipeline::analyze` | `timestamp=DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 136 | `mercury_ai/core/analysis_pipeline.py:524` | DeterministicClock | `AnalysisPipeline::analyze` | `atomic_json_write(f"runtime_report_{symbol}_{DeterministicClock.utcnow().strftime('%Y%m%d%H%M%S')}.json", self.runtime_r` | DETERMINISTIC | SIM |
| 137 | `mercury_ai/core/analysis_pipeline.py:543` | isoformat | `AnalysisPipeline::analyze` | `timestamp=DeterministicClock.utcnow().isoformat(), asset=symbol, timeframe=DEFAULT_TIMEFRAME,` | DETERMINISTIC | SIM |
| 138 | `mercury_ai/core/analysis_pipeline.py:565` | isoformat | `AnalysisPipeline::analyze` | `timestamp=DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 139 | `mercury_ai/core/analysis_pipeline.py:583` | isoformat | `AnalysisPipeline::analyze` | `timestamp=DeterministicClock.utcnow().isoformat(), asset=symbol, timeframe=DEFAULT_TIMEFRAME,` | DETERMINISTIC | SIM |
| 140 | `mercury_ai/core/analysis_pipeline.py:626` | isoformat | `AnalysisPipeline::_build_terminal_result` | `timestamp=DeterministicClock.utcnow().isoformat(), asset=symbol, timeframe=DEFAULT_TIMEFRAME,` | DETERMINISTIC | SIM |
| 141 | `mercury_ai/core/asset_registry.py:5` | import time | `-::-` | `import time` | IMPORT | - |
| 142 | `mercury_ai/core/asset_registry.py:107` | time.time | `AssetRegistry::update_asset_stats` | `self.assets[symbol].last_operated = time.time()` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 143 | `mercury_ai/core/health_center.py:2` | import time | `-::-` | `import time` | IMPORT | - |
| 144 | `mercury_ai/core/health_center.py:16` | time.time | `HealthCenter::get_system_metrics` | `"timestamp": time.time()` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 145 | `mercury_ai/core/job_manager.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 146 | `mercury_ai/core/job_manager.py:30` | time.sleep | `JobManager::_job_loop` | `time.sleep(self.interval)` | DELAY | SIM |
| 147 | `mercury_ai/core/observability_center.py:2` | import time | `-::-` | `import time` | IMPORT | - |
| 148 | `mercury_ai/core/observability_center.py:30` | time.time | `ObservabilityCenter::get_metrics` | `"timestamp": time.time()` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 149 | `mercury_ai/core/pipeline_audit_middleware.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 150 | `mercury_ai/core/pipeline_audit_middleware.py:6` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 151 | `mercury_ai/core/pipeline_audit_middleware.py:22` | datetime.now | `PipelineAuditMiddleware::__call__` | `start_ts = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 152 | `mercury_ai/core/pipeline_audit_middleware.py:23` | time.perf_counter | `PipelineAuditMiddleware::__call__` | `t0 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 153 | `mercury_ai/core/pipeline_audit_middleware.py:39` | time.perf_counter | `PipelineAuditMiddleware::__call__` | `duration_ms = (time.perf_counter() - t0) * 1000.0` | MONOTONIC | SIM (não contamina decisão) |
| 154 | `mercury_ai/core/pipeline_audit_middleware.py:42` | datetime.now | `PipelineAuditMiddleware::__call__` | `timestamp=datetime.now(timezone.utc).isoformat(),` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 155 | `mercury_ai/core/pipeline_profiler.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 156 | `mercury_ai/core/pipeline_profiler.py:49` | time.perf_counter | `PipelineProfiler::start_stage` | `builder.start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 157 | `mercury_ai/core/pipeline_profiler.py:54` | time.perf_counter | `PipelineProfiler::end_stage` | `builder.end_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 158 | `mercury_ai/core/security_center.py:10` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 159 | `mercury_ai/core/security_center.py:19` | isoformat | `AuditEvent::-` | `timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())` | DETERMINISTIC | SIM |
| 160 | `mercury_ai/core/session_manager.py:3` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 161 | `mercury_ai/core/session_manager.py:14` | isoformat | `SessionManager::__init__` | `self.timestamp = DeterministicClock.utcnow().isoformat()` | DETERMINISTIC | SIM |
| 162 | `mercury_ai/data/mercury_data_provider.py:3` | import time | `-::-` | `import time` | IMPORT | - |
| 163 | `mercury_ai/data/mercury_data_provider.py:112` | time.monotonic | `MercuryDataProvider::get_candles` | `now = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 164 | `mercury_ai/data/mercury_data_provider.py:122` | time.time | `MercuryDataProvider::get_candles` | `start_time = time.time()` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 165 | `mercury_ai/data/mercury_data_provider.py:124` | time.time | `MercuryDataProvider::get_candles` | `if time.time() - start_time > timeout:` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 166 | `mercury_ai/data/mercury_data_provider.py:134` | time.sleep | `MercuryDataProvider::get_candles` | `time.sleep(2 ** attempt)` | DELAY | SIM (fora do caminho determinístico) |
| 167 | `mercury_ai/database/history_logger.py:3` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 168 | `mercury_ai/database/history_logger.py:36` | datetime.now | `HistoryLogger::save` | `datetime.now(),` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 169 | `mercury_ai/database/snapshot_logger.py:25` | timezone | `-::_sanitize_filename_component` | `'+01:00' em timestamps timezone-aware).` | TZ_AWARE | SIM |
| 170 | `mercury_ai/database/tests/test_snapshot_logger.py:2` | timezone | `-::-` | `"""B4-C5 - Testes R1: SnapshotLogger aceita timestamps timezone-aware.` | TZ_AWARE | SIM |
| 171 | `mercury_ai/database/tests/test_snapshot_logger.py:52` | pd.Timestamp | `-::_epoch` | `return pd.Timestamp(iso_str).timestamp()` | CANDLE_TIME | SIM |
| 172 | `mercury_ai/execution/brokers/demo_broker.py:9` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 173 | `mercury_ai/execution/brokers/demo_broker.py:20` | datetime.now | `-::_utcnow_iso` | `return datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 174 | `mercury_ai/execution/order_executor.py:16` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 175 | `mercury_ai/execution/order_executor.py:45` | datetime.now | `-::_utcnow_iso` | `return datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 176 | `mercury_ai/execution/order_types.py:8` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 177 | `mercury_ai/execution/order_types.py:84` | datetime.now | `-::_utcnow_iso` | `return datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 178 | `mercury_ai/models/analysis_result.py:4` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 179 | `mercury_ai/models/analysis_result.py:49` | isoformat | `AnalysisResult::-` | `timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())` | DETERMINISTIC | SIM |
| 180 | `mercury_ai/models/evidence.py:6` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 181 | `mercury_ai/models/evidence.py:21` | isoformat | `Evidence::-` | `timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())` | DETERMINISTIC | SIM |
| 182 | `mercury_ai/models/evidence.py:43` | isoformat | `Evidence::create` | `ts = timestamp if timestamp is not None else DeterministicClock.utcnow().isoformat()` | DETERMINISTIC | SIM |
| 183 | `mercury_ai/models/memory_audit.py:4` | import time | `-::-` | `import time` | IMPORT | - |
| 184 | `mercury_ai/news/news_provider.py:1` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 185 | `mercury_ai/news/news_provider.py:8` | datetime.now | `NewsProvider::get_news` | `now = datetime.now().strftime("%d/%m/%Y %H:%M")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 186 | `mercury_ai/operations/demo_manager.py:7` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 187 | `mercury_ai/operations/demo_manager.py:33` | isoformat | `DemoOperationsManager::run_simulation` | `'timestamp': DeterministicClock.utcnow().isoformat(),` | DETERMINISTIC | SIM |
| 188 | `mercury_ai/operations/m5_incremental/asset_state.py:19` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 189 | `mercury_ai/operations/m5_incremental/asset_state.py:91` | datetime.now | `AssetScanState::mark_processing` | `self.updated_at = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 190 | `mercury_ai/operations/m5_incremental/asset_state.py:101` | datetime.now | `AssetScanState::mark_error` | `self.updated_at = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 191 | `mercury_ai/operations/m5_incremental/asset_state.py:113` | datetime.fromisoformat | `AssetScanState::age_seconds` | `dt = datetime.fromisoformat(self.decision_timestamp.replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 192 | `mercury_ai/operations/m5_incremental/asset_state.py:115` | timezone | `AssetScanState::age_seconds` | `dt = dt.replace(tzinfo=timezone.utc)` | TZ_AWARE | SIM |
| 193 | `mercury_ai/operations/m5_incremental/asset_state.py:117` | datetime.now | `AssetScanState::age_seconds` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 194 | `mercury_ai/operations/m5_incremental/asset_state.py:119` | timezone | `AssetScanState::age_seconds` | `now = now.replace(tzinfo=timezone.utc)` | TZ_AWARE | SIM |
| 195 | `mercury_ai/operations/m5_incremental/cache_tracker.py:13` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 196 | `mercury_ai/operations/m5_incremental/cache_tracker.py:68` | datetime.now | `CacheTracker::put` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 197 | `mercury_ai/operations/m5_incremental/cache_tracker.py:144` | isoformat | `CacheTracker::check` | `reason=f"cached {cached.isoformat()} < latest {effective_required.isoformat()} (nova vela disponível)",` | SERIALIZE | SIM |
| 198 | `mercury_ai/operations/m5_incremental/cache_tracker.py:151` | isoformat | `CacheTracker::check` | `reason=f"cached == required ({cached.isoformat()})",` | SERIALIZE | SIM |
| 199 | `mercury_ai/operations/m5_incremental/cache_tracker.py:160` | isoformat | `CacheTracker::check` | `reason=f"cached {cached.isoformat()} < required {required_candle.isoformat()} — REFRESH REQUIRED",` | SERIALIZE | SIM |
| 200 | `mercury_ai/operations/m5_incremental/cache_tracker.py:169` | isoformat | `CacheTracker::check` | `reason=f"cached {cached.isoformat()} > required {required_candle.isoformat()} (inconsistente)",` | SERIALIZE | SIM |
| 201 | `mercury_ai/operations/m5_incremental/freshness.py:14` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 202 | `mercury_ai/operations/m5_incremental/freshness.py:64` | datetime.now | `FreshnessGate::check` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 203 | `mercury_ai/operations/m5_incremental/freshness.py:115` | isoformat | `FreshnessGate::check` | `reason=f"decision_candle == latest_candle ({decision_candle.isoformat()})",` | SERIALIZE | SIM |
| 204 | `mercury_ai/operations/m5_incremental/freshness.py:126` | isoformat | `FreshnessGate::check` | `reason=f"decision_candle {decision_candle.isoformat()} < latest {latest_candle.isoformat()} ({delta_candles} vela(s) atr` | SERIALIZE | SIM |
| 205 | `mercury_ai/operations/m5_incremental/freshness.py:136` | isoformat | `FreshnessGate::check` | `reason=f"decision_candle {decision_candle.isoformat()} > latest {latest_candle.isoformat()} (inconsistente/futuro)",` | SERIALIZE | SIM |
| 206 | `mercury_ai/operations/m5_incremental/freshness.py:149` | datetime.fromisoformat | `FreshnessGate::check_state` | `dec = datetime.fromisoformat(state_decision_candle_iso.replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 207 | `mercury_ai/operations/m5_incremental/rolling_queue.py:14` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 208 | `mercury_ai/operations/m5_incremental/rolling_queue.py:58` | datetime.now | `RollingQueue::build` | `cycle_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 209 | `mercury_ai/operations/m5_incremental/rolling_queue.py:101` | datetime.fromisoformat | `RollingQueue::build` | `dec_dt = datetime.fromisoformat(state.decision_candle_timestamp.replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 210 | `mercury_ai/operations/m5_incremental/rolling_queue.py:103` | timezone | `RollingQueue::build` | `dec_dt = dec_dt.replace(tzinfo=timezone.utc)` | TZ_AWARE | SIM |
| 211 | `mercury_ai/operations/m5_incremental/rolling_queue.py:106` | timezone | `RollingQueue::build` | `latest_f = floor_m5(latest) if latest.tzinfo else floor_m5(latest.replace(tzinfo=timezone.utc))` | TZ_AWARE | SIM |
| 212 | `mercury_ai/operations/m5_incremental/temporal.py:12` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 213 | `mercury_ai/operations/m5_incremental/temporal.py:18` | timezone | `-::_ensure_utc` | `"""Garante datetime timezone-aware UTC. Naive -> assume UTC."""` | TZ_AWARE | SIM |
| 214 | `mercury_ai/operations/m5_incremental/temporal.py:20` | timezone | `-::_ensure_utc` | `return dt.replace(tzinfo=timezone.utc)` | TZ_AWARE | SIM |
| 215 | `mercury_ai/operations/m5_incremental/temporal.py:21` | timezone | `-::_ensure_utc` | `return dt.astimezone(timezone.utc)` | TZ_AWARE | SIM |
| 216 | `mercury_ai/operations/m5_incremental/temporal.py:47` | timedelta | `-::ceil_m5` | `return floored + timedelta(minutes=5)` | DURATION | SIM |
| 217 | `mercury_ai/operations/m5_incremental/temporal.py:49` | timedelta | `-::ceil_m5` | `return floored + timedelta(minutes=5)` | DURATION | SIM |
| 218 | `mercury_ai/operations/m5_incremental/temporal.py:70` | datetime.now | `-::expected_latest_candle_open` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 219 | `mercury_ai/operations/m5_incremental/temporal.py:77` | timedelta | `-::expected_latest_candle_open` | `return floored - timedelta(minutes=5)` | DURATION | SIM |
| 220 | `mercury_ai/operations/m5_incremental/temporal.py:106` | datetime.now | `-::current_candle` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 221 | `mercury_ai/operations/m5_incremental/temporal.py:113` | datetime.now | `-::previous_candle` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 222 | `mercury_ai/operations/m5_incremental/temporal.py:114` | timedelta | `-::previous_candle` | `return floor_m5(now) - timedelta(minutes=5)` | DURATION | SIM |
| 223 | `mercury_ai/operations/m5_incremental/temporal.py:120` | datetime.now | `-::next_candle` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 224 | `mercury_ai/operations/m5_incremental/temporal.py:135` | pd.Timestamp | `-::decision_candle_timestamp_from_df` | `if isinstance(ts, pd.Timestamp):` | CANDLE_TIME | SIM |
| 225 | `mercury_ai/operations/m5_incremental/temporal.py:142` | pd.to_datetime | `-::decision_candle_timestamp_from_df` | `return _ensure_utc(pd.to_datetime(ts).to_pydatetime())` | CANDLE_TIME | SIM |
| 226 | `mercury_ai/operations/m5_incremental/temporal.py:152` | datetime.now | `-::decision_age_seconds` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 227 | `mercury_ai/operations/m5_incremental/temporal.py:166` | datetime.now | `-::candle_age_seconds` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 228 | `mercury_ai/operations/m5_operational/clock.py:1` | sleep( | `-::-` | `"""M5 Clock / Cycle Scheduler — alinhado ao candle M5, não sleep() acumulativo."""` | DELAY | SIM (fora do caminho determinístico) |
| 229 | `mercury_ai/operations/m5_operational/clock.py:4` | import time | `-::-` | `import time` | IMPORT | - |
| 230 | `mercury_ai/operations/m5_operational/clock.py:8` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 231 | `mercury_ai/operations/m5_operational/clock.py:33` | datetime.now | `M5Clock::_next_boundary` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 232 | `mercury_ai/operations/m5_operational/clock.py:46` | datetime.now | `M5Clock::_loop` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 233 | `mercury_ai/operations/m5_operational/clock.py:54` | time.sleep | `M5Clock::_loop` | `time.sleep(chunk)` | DELAY | SIM (fora do caminho determinístico) |
| 234 | `mercury_ai/operations/m5_operational/clock.py:62` | isoformat | `M5Clock::_loop` | `logger.info("[M5Clock] triggering cycle %s target=%s", cycle_id, target.isoformat())` | SERIALIZE | SIM |
| 235 | `mercury_ai/operations/m5_operational/clock.py:79` | clock var | `M5Clock::start` | `self._thread = threading.Thread(target=_loop, name="m5-clock", daemon=True)` | CLOCK_REF | - |
| 236 | `mercury_ai/operations/m5_operational/clock.py:103` | datetime.now | `M5Clock::run_cycles_blocking` | `target_start = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 237 | `mercury_ai/operations/m5_operational/clock.py:115` | timedelta | `M5Clock::run_cycles_blocking` | `cur = cur + timedelta(minutes=5)` | DURATION | SIM |
| 238 | `mercury_ai/operations/m5_operational/runner.py:17` | import time | `-::-` | `import time` | IMPORT | - |
| 239 | `mercury_ai/operations/m5_operational/runner.py:25` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 240 | `mercury_ai/operations/m5_operational/runner.py:42` | time.perf_counter | `-::_analyze_one_isolated` | `t0 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 241 | `mercury_ai/operations/m5_operational/runner.py:63` | time.perf_counter | `-::_analyze_one_isolated` | `wall_ms = (time.perf_counter() - t0) * 1000` | MONOTONIC | SIM (não contamina decisão) |
| 242 | `mercury_ai/operations/m5_operational/runner.py:110` | timezone | `-::_analyze_one_isolated` | `from datetime import datetime as _dt, timezone as _tz` | TZ_AWARE | SIM |
| 243 | `mercury_ai/operations/m5_operational/runner.py:187` | time.perf_counter | `-::_analyze_one_isolated` | `"wall_ms": round((time.perf_counter() - t0) * 1000, 1),` | MONOTONIC | SIM (não contamina decisão) |
| 244 | `mercury_ai/operations/m5_operational/runner.py:225` | datetime.now | `M5OperationalRunner::_next_target_candle` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 245 | `mercury_ai/operations/m5_operational/runner.py:284` | isoformat | `M5OperationalRunner::run_cycle` | `"target_candle": (target_candle or self._next_target_candle()).isoformat(),` | SERIALIZE | SIM |
| 246 | `mercury_ai/operations/m5_operational/runner.py:293` | time.perf_counter | `M5OperationalRunner::run_cycle` | `cycle_start_wall = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 247 | `mercury_ai/operations/m5_operational/runner.py:294` | datetime.now | `M5OperationalRunner::run_cycle` | `cycle_start_iso = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 248 | `mercury_ai/operations/m5_operational/runner.py:295` | isoformat | `M5OperationalRunner::run_cycle` | `target_iso = target_candle.isoformat()` | SERIALIZE | SIM |
| 249 | `mercury_ai/operations/m5_operational/runner.py:382` | time.perf_counter | `M5OperationalRunner::_refresh_deadlines` | `now_t = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 250 | `mercury_ai/operations/m5_operational/runner.py:403` | time.perf_counter | `M5OperationalRunner::run_cycle` | `now_wall = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 251 | `mercury_ai/operations/m5_operational/runner.py:431` | time.perf_counter | `M5OperationalRunner::run_cycle` | `now2 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 252 | `mercury_ai/operations/m5_operational/runner.py:457` | time.perf_counter | `M5OperationalRunner::run_cycle` | `elapsed_ms = (time.perf_counter() - cycle_start_wall) * 1000` | MONOTONIC | SIM (não contamina decisão) |
| 253 | `mercury_ai/operations/m5_operational/runner.py:637` | time.perf_counter | `M5OperationalRunner::run_cycle` | `if time.perf_counter() > deadline_wall:` | MONOTONIC | SIM (não contamina decisão) |
| 254 | `mercury_ai/operations/m5_operational/runner.py:647` | time.perf_counter | `M5OperationalRunner::run_cycle` | `wall_ms = (time.perf_counter() - cycle_start_wall) * 1000` | MONOTONIC | SIM (não contamina decisão) |
| 255 | `mercury_ai/operations/m5_operational/runner.py:686` | datetime.now | `M5OperationalRunner::run_cycle` | `"cycle_end": datetime.now(timezone.utc).isoformat(),` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 256 | `mercury_ai/operations/m5_operational/watchdog.py:4` | import time | `-::-` | `import time` | IMPORT | - |
| 257 | `mercury_ai/operations/m5_operational/watchdog.py:42` | time.monotonic | `CycleWatchdog::__init__` | `self._last_progress_t = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 258 | `mercury_ai/operations/m5_operational/watchdog.py:43` | time.monotonic | `CycleWatchdog::__init__` | `self._start_t = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 259 | `mercury_ai/operations/m5_operational/watchdog.py:57` | time.monotonic | `CycleWatchdog::notify_progress` | `self._last_progress_t = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 260 | `mercury_ai/operations/m5_operational/watchdog.py:62` | time.monotonic | `CycleWatchdog::_loop` | `now = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 261 | `mercury_ai/operations/m5_operational/watchdog.py:87` | time.monotonic | `CycleWatchdog::start` | `self._start_t = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 262 | `mercury_ai/operations/m5_sprint6/alerts.py:7` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 263 | `mercury_ai/operations/m5_sprint6/alerts.py:44` | datetime.now | `AlertSink::emit` | `timestamp=datetime.now(timezone.utc).isoformat(),` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 264 | `mercury_ai/operations/m5_sprint6/deadline.py:32` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 265 | `mercury_ai/operations/m5_sprint6/deadline.py:48` | timedelta | `-::next_candle_start_for` | `return floor_m5(_ensure_utc(target_candle)) + timedelta(minutes=5)` | DURATION | SIM |
| 266 | `mercury_ai/operations/m5_sprint6/live_session.py:14` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 267 | `mercury_ai/operations/m5_sprint6/live_session.py:19` | clock var | `-::-` | `from mercury_ai.operations.m5_operational.clock import M5Clock` | CLOCK_REF | - |
| 268 | `mercury_ai/operations/m5_sprint6/live_session.py:38` | datetime.fromisoformat | `-::_parse_cycle_wall` | `base = datetime.fromisoformat(str(cs).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 269 | `mercury_ai/operations/m5_sprint6/live_session.py:42` | timedelta | `-::_parse_cycle_wall` | `return base + timedelta(milliseconds=float(ms))` | DURATION | SIM |
| 270 | `mercury_ai/operations/m5_sprint6/live_session.py:46` | datetime.fromisoformat | `-::_parse_cycle_wall` | `return datetime.fromisoformat(str(ce).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 271 | `mercury_ai/operations/m5_sprint6/live_session.py:108` | datetime.now | `LiveSession::run` | `self.start_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 272 | `mercury_ai/operations/m5_sprint6/live_session.py:112` | clock var | `LiveSession::run` | `# target_candle incremental de 5m e no-overlap garantido. Prova live clock` | CLOCK_REF | - |
| 273 | `mercury_ai/operations/m5_sprint6/live_session.py:114` | datetime.now | `LiveSession::run` | `target_start = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 274 | `mercury_ai/operations/m5_sprint6/live_session.py:125` | datetime.fromisoformat | `LiveSession::run` | `target_dt = datetime.fromisoformat(str(target_iso).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 275 | `mercury_ai/operations/m5_sprint6/live_session.py:127` | datetime.now | `LiveSession::run` | `target_dt = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 276 | `mercury_ai/operations/m5_sprint6/live_session.py:132` | datetime.fromisoformat | `LiveSession::run` | `cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 277 | `mercury_ai/operations/m5_sprint6/live_session.py:134` | datetime.now | `LiveSession::run` | `cs_dt = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 278 | `mercury_ai/operations/m5_sprint6/live_session.py:136` | datetime.fromisoformat | `LiveSession::run` | `ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None` | PARSE | SIM se origem candle |
| 279 | `mercury_ai/operations/m5_sprint6/live_session.py:145` | timedelta | `LiveSession::run` | `decision_ready_dt = cs_dt + timedelta(milliseconds=float(first_fresh_ms))` | DURATION | SIM |
| 280 | `mercury_ai/operations/m5_sprint6/live_session.py:182` | isoformat | `LiveSession::run` | `enriched_cycle["target_candle_close"] = tcc.isoformat()` | SERIALIZE | SIM |
| 281 | `mercury_ai/operations/m5_sprint6/live_session.py:185` | timedelta | `LiveSession::run` | `enriched_cycle["first_fresh_decision"] = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))).isoformat() if first_fr` | DURATION | SIM |
| 282 | `mercury_ai/operations/m5_sprint6/live_session.py:186` | timedelta | `LiveSession::run` | `enriched_cycle["first_top3"] = (cs_dt + timedelta(milliseconds=float(first_top3_ms))).isoformat() if first_top3_ms is no` | DURATION | SIM |
| 283 | `mercury_ai/operations/m5_sprint6/live_session.py:187` | isoformat | `LiveSession::run` | `enriched_cycle["decision_ready"] = decision_ready_dt.isoformat() if decision_ready_dt else None` | SERIALIZE | SIM |
| 284 | `mercury_ai/operations/m5_sprint6/live_session.py:188` | isoformat | `LiveSession::run` | `enriched_cycle["next_candle_start"] = ncs.isoformat()` | SERIALIZE | SIM |
| 285 | `mercury_ai/operations/m5_sprint6/live_session.py:192` | isoformat | `LiveSession::run` | `enriched_cycle["cycle_complete"] = ce_dt.isoformat() if ce_dt else None` | SERIALIZE | SIM |
| 286 | `mercury_ai/operations/m5_sprint6/live_session.py:201` | isoformat | `LiveSession::run` | `"target_candle_close": tcc.isoformat(),` | SERIALIZE | SIM |
| 287 | `mercury_ai/operations/m5_sprint6/live_session.py:202` | isoformat | `LiveSession::run` | `"next_candle_start": ncs.isoformat(),` | SERIALIZE | SIM |
| 288 | `mercury_ai/operations/m5_sprint6/live_session.py:203` | isoformat | `LiveSession::run` | `"decision_ready": decision_ready_dt.isoformat() if decision_ready_dt else None,` | SERIALIZE | SIM |
| 289 | `mercury_ai/operations/m5_sprint6/live_session.py:211` | datetime.now | `LiveSession::run` | `self.end_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 290 | `mercury_ai/operations/m5_sprint6/live_session.py:222` | datetime.fromisoformat | `LiveSession::run` | `datetime.fromisoformat(str(r["target_candle"]).replace("Z","+00:00")),` | PARSE | SIM se origem candle |
| 291 | `mercury_ai/operations/m5_sprint6/live_session.py:223` | datetime.fromisoformat | `LiveSession::run` | `(datetime.fromisoformat(str(r["cycle_start"]).replace("Z","+00:00")) + timedelta(milliseconds=float(r["first_fresh_decis` | DURATION | SIM |
| 292 | `mercury_ai/operations/m5_sprint6/live_session.py:238` | datetime.fromisoformat | `LiveSession::run` | `pt = datetime.fromisoformat(str(prev["target_candle"]).replace("Z","+00:00"))` | PARSE | SIM se origem candle |
| 293 | `mercury_ai/operations/m5_sprint6/live_session.py:239` | datetime.fromisoformat | `LiveSession::run` | `ct2 = datetime.fromisoformat(str(cur["target_candle"]).replace("Z","+00:00"))` | PARSE | SIM se origem candle |
| 294 | `mercury_ai/operations/m5_sprint61/__init__.py:1` | clock var | `-::-` | `"""M5 Sprint 6.1 — LIVE CLOCK INTEGRITY / REAL-TIME CERTIFICATION."""` | CLOCK_REF | - |
| 295 | `mercury_ai/operations/m5_sprint61/live_clock_integrity.py:26` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 296 | `mercury_ai/operations/m5_sprint61/live_clock_integrity.py:83` | isoformat | `-::_iso` | `return _ensure_utc(dt).isoformat()` | SERIALIZE | SIM |
| 297 | `mercury_ai/operations/m5_sprint61/live_clock_integrity.py:101` | timedelta | `-::classify_cycle` | `next_start = target + timedelta(minutes=5)` | DURATION | SIM |
| 298 | `mercury_ai/operations/m5_sprint61/live_session61.py:18` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 299 | `mercury_ai/operations/m5_sprint61/live_session61.py:23` | clock var | `-::-` | `from mercury_ai.operations.m5_operational.clock import M5Clock` | CLOCK_REF | - |
| 300 | `mercury_ai/operations/m5_sprint61/live_session61.py:85` | datetime.now | `Sprint61LiveSession::_wait_for_next_boundary` | `now = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 301 | `mercury_ai/operations/m5_sprint61/live_session61.py:90` | time.sleep | `Sprint61LiveSession::_wait_for_next_boundary` | `time.sleep(0.05)` | DELAY | SIM (fora do caminho determinístico) |
| 302 | `mercury_ai/operations/m5_sprint61/live_session61.py:91` | datetime.now | `Sprint61LiveSession::_wait_for_next_boundary` | `return datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 303 | `mercury_ai/operations/m5_sprint61/live_session61.py:95` | time.sleep | `Sprint61LiveSession::_wait_for_next_boundary` | `time.sleep(chunk)` | DELAY | SIM (fora do caminho determinístico) |
| 304 | `mercury_ai/operations/m5_sprint61/live_session61.py:96` | sleep( | `Sprint61LiveSession::-` | `# loop recalcula nxt a partir do novo now (evita acumulo sleep(300) incorreto)` | DELAY | SIM (fora do caminho determinístico) |
| 305 | `mercury_ai/operations/m5_sprint61/live_session61.py:99` | datetime.now | `Sprint61LiveSession::run` | `self.start_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 306 | `mercury_ai/operations/m5_sprint61/live_session61.py:109` | datetime.now | `Sprint61LiveSession::run` | `target_start = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 307 | `mercury_ai/operations/m5_sprint61/live_session61.py:116` | datetime.fromisoformat | `Sprint61LiveSession::run` | `cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 308 | `mercury_ai/operations/m5_sprint61/live_session61.py:118` | datetime.now | `Sprint61LiveSession::run` | `cs_dt = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 309 | `mercury_ai/operations/m5_sprint61/live_session61.py:120` | datetime.fromisoformat | `Sprint61LiveSession::run` | `target_dt = datetime.fromisoformat(str(r.get("target_candle")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 310 | `mercury_ai/operations/m5_sprint61/live_session61.py:124` | timedelta | `Sprint61LiveSession::run` | `decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 311 | `mercury_ai/operations/m5_sprint61/live_session61.py:173` | datetime.now | `Sprint61LiveSession::run` | `now_probe = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 312 | `mercury_ai/operations/m5_sprint61/live_session61.py:181` | time.sleep | `Sprint61LiveSession::run` | `time.sleep(sleep_for)` | DELAY | SIM (fora do caminho determinístico) |
| 313 | `mercury_ai/operations/m5_sprint61/live_session61.py:184` | datetime.now | `Sprint61LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 314 | `mercury_ai/operations/m5_sprint61/live_session61.py:187` | clock var | `Sprint61LiveSession::run` | `# mas se clock_now for exatamente na fronteira, floor==clock_now, ainda ok (target <= clock)` | CLOCK_REF | - |
| 315 | `mercury_ai/operations/m5_sprint61/live_session61.py:193` | time.sleep | `Sprint61LiveSession::run` | `time.sleep(wait_s)` | DELAY | SIM (fora do caminho determinístico) |
| 316 | `mercury_ai/operations/m5_sprint61/live_session61.py:194` | datetime.now | `Sprint61LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 317 | `mercury_ai/operations/m5_sprint61/live_session61.py:202` | datetime.fromisoformat | `Sprint61LiveSession::run` | `cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 318 | `mercury_ai/operations/m5_sprint61/live_session61.py:206` | timedelta | `Sprint61LiveSession::run` | `decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 319 | `mercury_ai/operations/m5_sprint61/live_session61.py:247` | datetime.now | `Sprint61LiveSession::run` | `self.end_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 320 | `mercury_ai/operations/m5_sprint61/live_session61.py:255` | datetime.fromisoformat | `Sprint61LiveSession::run` | `td = datetime.fromisoformat(str(ec["target_candle"]).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 321 | `mercury_ai/operations/m5_sprint61/live_session61.py:257` | datetime.now | `Sprint61LiveSession::run` | `td = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 322 | `mercury_ai/operations/m5_sprint61/live_session61.py:259` | datetime.fromisoformat | `Sprint61LiveSession::run` | `dr = datetime.fromisoformat(str(ec["decision_ready"]).replace("Z", "+00:00")) if ec.get("decision_ready") else None` | PARSE | SIM se origem candle |
| 323 | `mercury_ai/operations/m5_sprint61/live_session61.py:358` | clock var | `Sprint61LiveSession::write_artifacts` | `lines.append(f"- Live clock certification: {s.get('live_clock_certification')}  pass_rate {s.get('next_candle_pass_rate'` | CLOCK_REF | - |
| 324 | `mercury_ai/operations/m5_sprint62/live_session62.py:9` | import time | `-::-` | `import time` | IMPORT | - |
| 325 | `mercury_ai/operations/m5_sprint62/live_session62.py:14` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 326 | `mercury_ai/operations/m5_sprint62/live_session62.py:19` | clock var | `-::-` | `from mercury_ai.operations.m5_operational.clock import M5Clock` | CLOCK_REF | - |
| 327 | `mercury_ai/operations/m5_sprint62/live_session62.py:96` | datetime.now | `Sprint62LiveSession::run` | `self.start_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 328 | `mercury_ai/operations/m5_sprint62/live_session62.py:102` | time.perf_counter | `Sprint62LiveSession::run` | `session_start_perf = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 329 | `mercury_ai/operations/m5_sprint62/live_session62.py:111` | datetime.now | `Sprint62LiveSession::run` | `now_probe = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 330 | `mercury_ai/operations/m5_sprint62/live_session62.py:118` | time.sleep | `Sprint62LiveSession::run` | `time.sleep(sleep_for)` | DELAY | SIM (fora do caminho determinístico) |
| 331 | `mercury_ai/operations/m5_sprint62/live_session62.py:120` | datetime.now | `Sprint62LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 332 | `mercury_ai/operations/m5_sprint62/live_session62.py:127` | isoformat | `Sprint62LiveSession::run` | `self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target {target_dt.isoformat(` | SERIALIZE | SIM |
| 333 | `mercury_ai/operations/m5_sprint62/live_session62.py:138` | time.sleep | `Sprint62LiveSession::run` | `time.sleep(wait_s)` | DELAY | SIM (fora do caminho determinístico) |
| 334 | `mercury_ai/operations/m5_sprint62/live_session62.py:139` | datetime.now | `Sprint62LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 335 | `mercury_ai/operations/m5_sprint62/live_session62.py:156` | datetime.fromisoformat | `Sprint62LiveSession::run` | `cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 336 | `mercury_ai/operations/m5_sprint62/live_session62.py:160` | datetime.fromisoformat | `Sprint62LiveSession::run` | `ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None` | PARSE | SIM se origem candle |
| 337 | `mercury_ai/operations/m5_sprint62/live_session62.py:169` | timedelta | `Sprint62LiveSession::run` | `decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 338 | `mercury_ai/operations/m5_sprint62/live_session62.py:170` | timedelta | `Sprint62LiveSession::run` | `first_fresh_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 339 | `mercury_ai/operations/m5_sprint62/live_session62.py:171` | timedelta | `Sprint62LiveSession::run` | `first_top3_dt = (cs_dt + timedelta(milliseconds=float(first_top3_ms))) if first_top3_ms is not None else None` | DURATION | SIM |
| 340 | `mercury_ai/operations/m5_sprint62/live_session62.py:174` | timedelta | `Sprint62LiveSession::run` | `next_start_dt = target_dt + timedelta(minutes=5)` | DURATION | SIM |
| 341 | `mercury_ai/operations/m5_sprint62/live_session62.py:196` | clock var | `Sprint62LiveSession::run` | `self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", cycle_id, f"target_is_future but PASS — integrity bug target {gate_` | CLOCK_REF | - |
| 342 | `mercury_ai/operations/m5_sprint62/live_session62.py:224` | isoformat | `Sprint62LiveSession::run` | `"cycle_start": cycle_start_dt.isoformat() if cycle_start_dt else r.get("cycle_start"),` | SERIALIZE | SIM |
| 343 | `mercury_ai/operations/m5_sprint62/live_session62.py:225` | isoformat | `Sprint62LiveSession::run` | `"first_fresh_decision": first_fresh_dt.isoformat() if first_fresh_dt else None,` | SERIALIZE | SIM |
| 344 | `mercury_ai/operations/m5_sprint62/live_session62.py:226` | isoformat | `Sprint62LiveSession::run` | `"first_top3": first_top3_dt.isoformat() if first_top3_dt else None,` | SERIALIZE | SIM |
| 345 | `mercury_ai/operations/m5_sprint62/live_session62.py:229` | isoformat | `Sprint62LiveSession::run` | `"cycle_complete": cycle_complete_dt.isoformat() if cycle_complete_dt else r.get("cycle_end"),` | SERIALIZE | SIM |
| 346 | `mercury_ai/operations/m5_sprint62/live_session62.py:247` | datetime.now | `Sprint62LiveSession::run` | `self.end_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 347 | `mercury_ai/operations/m5_sprint62/live_session62.py:249` | time.perf_counter | `Sprint62LiveSession::run` | `session_wall_s = time.perf_counter() - session_start_perf` | MONOTONIC | SIM (não contamina decisão) |
| 348 | `mercury_ai/operations/m5_sprint62/live_session62.py:312` | clock var | `Sprint62LiveSession::run` | `# All target <= clock check §3 §15` | CLOCK_REF | - |
| 349 | `mercury_ai/operations/m5_sprint62/live_session62.py:481` | datetime.now | `Sprint62LiveSession::write_artifacts` | `ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 350 | `mercury_ai/operations/m5_sprint63/fault_harness.py:20` | import time | `-::-` | `import time` | IMPORT | - |
| 351 | `mercury_ai/operations/m5_sprint63/fault_harness.py:26` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 352 | `mercury_ai/operations/m5_sprint63/fault_harness.py:56` | datetime.now | `-::_now_iso` | `return datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 353 | `mercury_ai/operations/m5_sprint63/fault_harness.py:62` | datetime.fromisoformat | `-::_make_incident` | `det = datetime.fromisoformat(detection_time.replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 354 | `mercury_ai/operations/m5_sprint63/fault_harness.py:63` | datetime.fromisoformat | `-::_make_incident` | `comp = datetime.fromisoformat(recovery_complete.replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 355 | `mercury_ai/operations/m5_sprint63/fault_harness.py:102` | datetime.now | `-::run_data_provider_failure` | `target = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 356 | `mercury_ai/operations/m5_sprint63/fault_harness.py:114` | isoformat | `-::run_data_provider_failure` | `inc = _make_incident("DATA_PROVIDER_FAILURE", cid, target.isoformat(), target_sym,` | SERIALIZE | SIM |
| 357 | `mercury_ai/operations/m5_sprint63/fault_harness.py:146` | datetime.now | `-::run_worker_crash` | `target = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 358 | `mercury_ai/operations/m5_sprint63/fault_harness.py:149` | time.perf_counter | `-::run_worker_crash` | `t0 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 359 | `mercury_ai/operations/m5_sprint63/fault_harness.py:152` | time.perf_counter | `-::run_worker_crash` | `recovery_time = time.perf_counter() - t0` | MONOTONIC | SIM (não contamina decisão) |
| 360 | `mercury_ai/operations/m5_sprint63/fault_harness.py:160` | isoformat | `-::run_worker_crash` | `inc = _make_incident("WORKER_CRASH", cid, target.isoformat(), target_sym,` | SERIALIZE | SIM |
| 361 | `mercury_ai/operations/m5_sprint63/fault_harness.py:191` | time.sleep | `-::slow` | `time.sleep(0.6)` | DELAY | SIM (fora do caminho determinístico) |
| 362 | `mercury_ai/operations/m5_sprint63/fault_harness.py:200` | datetime.now | `-::run_timeout_test` | `target = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 363 | `mercury_ai/operations/m5_sprint63/fault_harness.py:207` | isoformat | `-::run_timeout_test` | `inc = _make_incident("WORKER_TIMEOUT", cid, target.isoformat(), target_sym,` | SERIALIZE | SIM |
| 364 | `mercury_ai/operations/m5_sprint63/fault_harness.py:237` | datetime.now | `-::run_per_asset_isolation` | `target = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 365 | `mercury_ai/operations/m5_sprint63/fault_harness.py:249` | isoformat | `-::run_per_asset_isolation` | `inc = _make_incident("PER_ASSET_EXCEPTION", cid, target.isoformat(), failing_sym,` | SERIALIZE | SIM |
| 366 | `mercury_ai/operations/m5_sprint63/fault_harness.py:268` | datetime.now | `-::run_queue_pressure` | `target = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 367 | `mercury_ai/operations/m5_sprint63/fault_harness.py:275` | isoformat | `-::run_queue_pressure` | `inc = _make_incident("QUEUE_PRESSURE", cid, target.isoformat(), syms[0],` | SERIALIZE | SIM |
| 368 | `mercury_ai/operations/m5_sprint63/fault_harness.py:293` | time.monotonic | `-::run_watchdog_stall` | `t0 = time.monotonic()` | MONOTONIC | SIM (não contamina decisão) |
| 369 | `mercury_ai/operations/m5_sprint63/fault_harness.py:296` | time.sleep | `-::run_watchdog_stall` | `time.sleep(stall_threshold_s + 0.25)` | DELAY | SIM (fora do caminho determinístico) |
| 370 | `mercury_ai/operations/m5_sprint63/fault_harness.py:298` | time.sleep | `-::run_watchdog_stall` | `time.sleep(0.15)` | DELAY | SIM (fora do caminho determinístico) |
| 371 | `mercury_ai/operations/m5_sprint63/fault_harness.py:302` | time.monotonic | `-::run_watchdog_stall` | `recovery_time = time.monotonic() - t0` | MONOTONIC | SIM (não contamina decisão) |
| 372 | `mercury_ai/operations/m5_sprint63/fault_harness.py:305` | datetime.now | `-::run_watchdog_stall` | `inc = _make_incident("WATCHDOG_STALL", cid, floor_m5(datetime.now(timezone.utc)).isoformat(), "WATCHDOG",` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 373 | `mercury_ai/operations/m5_sprint63/fault_harness.py:321` | datetime.now | `-::run_graceful_shutdown` | `target = floor_m5(datetime.now(timezone.utc))` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 374 | `mercury_ai/operations/m5_sprint63/fault_harness.py:330` | time.sleep | `-::run_graceful_shutdown` | `time.sleep(0.35)` | DELAY | SIM (fora do caminho determinístico) |
| 375 | `mercury_ai/operations/m5_sprint63/fault_harness.py:339` | isoformat | `-::run_graceful_shutdown` | `inc = _make_incident(f"GRACEFUL_{signal_name}", cid, target.isoformat(), signal_name,` | SERIALIZE | SIM |
| 376 | `mercury_ai/operations/m5_sprint63/fault_harness.py:354` | clock var | `-::run_restart_integrity` | `from mercury_ai.operations.m5_operational.clock import M5Clock` | CLOCK_REF | - |
| 377 | `mercury_ai/operations/m5_sprint63/fault_harness.py:356` | clock var | `-::run_restart_integrity` | `clock = M5Clock(runner=runner, config=cfg)` | CLOCK_REF | - |
| 378 | `mercury_ai/operations/m5_sprint63/fault_harness.py:358` | clock var | `-::run_restart_integrity` | `r1 = clock.run_cycles_blocking(count=2)` | CLOCK_REF | - |
| 379 | `mercury_ai/operations/m5_sprint63/fault_harness.py:362` | datetime.fromisoformat | `-::run_restart_integrity` | `prev_dt = datetime.fromisoformat(str(previous_target).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 380 | `mercury_ai/operations/m5_sprint63/fault_harness.py:363` | clock var | `-::run_restart_integrity` | `# Simulate restart: new runner/clock, should continue from next candle` | CLOCK_REF | - |
| 381 | `mercury_ai/operations/m5_sprint63/fault_harness.py:364` | timedelta | `-::run_restart_integrity` | `expected_next = floor_m5(prev_dt + timedelta(minutes=5))` | DURATION | SIM |
| 382 | `mercury_ai/operations/m5_sprint63/fault_harness.py:372` | isoformat | `-::run_restart_integrity` | `no_dup = previous_target != next_target and next_target == expected_next.isoformat()` | SERIALIZE | SIM |
| 383 | `mercury_ai/operations/m5_sprint63/fault_harness.py:375` | isoformat | `-::run_restart_integrity` | `inc = _make_incident("RESTART_INTEGRITY", r2[0].get("cycle_id", "restart") if r2 else "restart", expected_next.isoformat` | SERIALIZE | SIM |
| 384 | `mercury_ai/operations/m5_sprint63/live_session63.py:10` | import time | `-::-` | `import time, uuid, json` | IMPORT | - |
| 385 | `mercury_ai/operations/m5_sprint63/live_session63.py:13` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 386 | `mercury_ai/operations/m5_sprint63/live_session63.py:18` | clock var | `-::-` | `from mercury_ai.operations.m5_operational.clock import M5Clock` | CLOCK_REF | - |
| 387 | `mercury_ai/operations/m5_sprint63/live_session63.py:83` | datetime.now | `Sprint63LiveSession::run` | `self.start_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 388 | `mercury_ai/operations/m5_sprint63/live_session63.py:89` | time.perf_counter | `Sprint63LiveSession::run` | `session_start_perf = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 389 | `mercury_ai/operations/m5_sprint63/live_session63.py:95` | datetime.now | `Sprint63LiveSession::run` | `now_probe = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 390 | `mercury_ai/operations/m5_sprint63/live_session63.py:102` | time.sleep | `Sprint63LiveSession::run` | `time.sleep(sleep_for)` | DELAY | SIM (fora do caminho determinístico) |
| 391 | `mercury_ai/operations/m5_sprint63/live_session63.py:104` | datetime.now | `Sprint63LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 392 | `mercury_ai/operations/m5_sprint63/live_session63.py:109` | isoformat | `Sprint63LiveSession::run` | `self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target {target_dt.isoformat(` | SERIALIZE | SIM |
| 393 | `mercury_ai/operations/m5_sprint63/live_session63.py:116` | time.sleep | `Sprint63LiveSession::run` | `time.sleep(wait_s)` | DELAY | SIM (fora do caminho determinístico) |
| 394 | `mercury_ai/operations/m5_sprint63/live_session63.py:117` | datetime.now | `Sprint63LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 395 | `mercury_ai/operations/m5_sprint63/live_session63.py:129` | datetime.fromisoformat | `Sprint63LiveSession::run` | `cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 396 | `mercury_ai/operations/m5_sprint63/live_session63.py:133` | timedelta | `Sprint63LiveSession::run` | `decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 397 | `mercury_ai/operations/m5_sprint63/live_session63.py:134` | timedelta | `Sprint63LiveSession::run` | `first_fresh_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 398 | `mercury_ai/operations/m5_sprint63/live_session63.py:135` | timedelta | `Sprint63LiveSession::run` | `first_top3_dt = (cs_dt + timedelta(milliseconds=float(r.get("first_top3_ms")))) if r.get("first_top3_ms") is not None el` | DURATION | SIM |
| 399 | `mercury_ai/operations/m5_sprint63/live_session63.py:137` | datetime.fromisoformat | `Sprint63LiveSession::run` | `ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None` | PARSE | SIM se origem candle |
| 400 | `mercury_ai/operations/m5_sprint63/live_session63.py:141` | timedelta | `Sprint63LiveSession::run` | `next_start_dt = target_dt + timedelta(minutes=5)` | DURATION | SIM |
| 401 | `mercury_ai/operations/m5_sprint63/live_session63.py:155` | clock var | `Sprint63LiveSession::run` | `self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", cycle_id, f"target_is_future but PASS — integrity bug target {gate_` | CLOCK_REF | - |
| 402 | `mercury_ai/operations/m5_sprint63/live_session63.py:176` | isoformat | `Sprint63LiveSession::run` | `"cycle_start": cycle_start_dt.isoformat() if cycle_start_dt else r.get("cycle_start"),` | SERIALIZE | SIM |
| 403 | `mercury_ai/operations/m5_sprint63/live_session63.py:177` | isoformat | `Sprint63LiveSession::run` | `"first_fresh_decision": first_fresh_dt.isoformat() if first_fresh_dt else None,` | SERIALIZE | SIM |
| 404 | `mercury_ai/operations/m5_sprint63/live_session63.py:178` | isoformat | `Sprint63LiveSession::run` | `"first_top3": first_top3_dt.isoformat() if first_top3_dt else None,` | SERIALIZE | SIM |
| 405 | `mercury_ai/operations/m5_sprint63/live_session63.py:181` | isoformat | `Sprint63LiveSession::run` | `"cycle_complete": ce_dt.isoformat() if ce_dt else r.get("cycle_end"),` | SERIALIZE | SIM |
| 406 | `mercury_ai/operations/m5_sprint63/live_session63.py:196` | datetime.now | `Sprint63LiveSession::run` | `self.end_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 407 | `mercury_ai/operations/m5_sprint63/live_session63.py:198` | time.perf_counter | `Sprint63LiveSession::run` | `session_wall_s = time.perf_counter() - session_start_perf` | MONOTONIC | SIM (não contamina decisão) |
| 408 | `mercury_ai/operations/m5_sprint64/artifact.py:8` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 409 | `mercury_ai/operations/m5_sprint64/artifact.py:23` | datetime.now | `-::_now_iso` | `return datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 410 | `mercury_ai/operations/m5_sprint64/audit.py:8` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 411 | `mercury_ai/operations/m5_sprint64/audit.py:17` | datetime.now | `-::_now_iso` | `return datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 412 | `mercury_ai/operations/m5_sprint64/audit.py:112` | timedelta | `AuditRecord::from_cycle_report` | `from datetime import timedelta` | DURATION | SIM |
| 413 | `mercury_ai/operations/m5_sprint64/audit.py:113` | datetime.fromisoformat | `AuditRecord::from_cycle_report` | `tdt = datetime.fromisoformat(str(target).replace("Z", "+00:00")) if target else None` | PARSE | SIM se origem candle |
| 414 | `mercury_ai/operations/m5_sprint64/audit.py:114` | timedelta | `AuditRecord::from_cycle_report` | `next_start = (tdt + timedelta(minutes=5)).isoformat() if tdt else None` | DURATION | SIM |
| 415 | `mercury_ai/operations/m5_sprint64/events.py:5` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 416 | `mercury_ai/operations/m5_sprint64/events.py:74` | datetime.now | `ObservabilityEvent::new` | `timestamp=datetime.now(timezone.utc).isoformat(),` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 417 | `mercury_ai/operations/m5_sprint64/live_session64.py:10` | import time | `-::-` | `import time, uuid, json, hashlib, tempfile, os` | IMPORT | - |
| 418 | `mercury_ai/operations/m5_sprint64/live_session64.py:13` | timezone | `-::-` | `from datetime import datetime, timezone, timedelta` | DURATION | SIM |
| 419 | `mercury_ai/operations/m5_sprint64/live_session64.py:104` | datetime.now | `Sprint64LiveSession::run` | `self.start_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 420 | `mercury_ai/operations/m5_sprint64/live_session64.py:116` | time.perf_counter | `Sprint64LiveSession::run` | `session_start_perf = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 421 | `mercury_ai/operations/m5_sprint64/live_session64.py:122` | datetime.now | `Sprint64LiveSession::run` | `now_probe = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 422 | `mercury_ai/operations/m5_sprint64/live_session64.py:129` | time.sleep | `Sprint64LiveSession::run` | `time.sleep(sleep_for)` | DELAY | SIM (fora do caminho determinístico) |
| 423 | `mercury_ai/operations/m5_sprint64/live_session64.py:131` | datetime.now | `Sprint64LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 424 | `mercury_ai/operations/m5_sprint64/live_session64.py:136` | isoformat | `Sprint64LiveSession::run` | `self.alerts.emit("CLOCK_INTEGRITY_FAIL", "CRITICAL", f"cycle-{idx}", f"CLOCK_INTEGRITY_FAIL target {target_dt.isoformat(` | SERIALIZE | SIM |
| 425 | `mercury_ai/operations/m5_sprint64/live_session64.py:143` | time.sleep | `Sprint64LiveSession::run` | `time.sleep(wait_s)` | DELAY | SIM (fora do caminho determinístico) |
| 426 | `mercury_ai/operations/m5_sprint64/live_session64.py:144` | datetime.now | `Sprint64LiveSession::run` | `clock_now_at_start = datetime.now(timezone.utc)` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 427 | `mercury_ai/operations/m5_sprint64/live_session64.py:149` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("CYCLE_START", self.session_id, cycle_id, target_dt.isoformat()))` | SERIALIZE | SIM |
| 428 | `mercury_ai/operations/m5_sprint64/live_session64.py:150` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("TARGET_SELECTED", self.session_id, cycle_id, target_dt.isoformat()))` | SERIALIZE | SIM |
| 429 | `mercury_ai/operations/m5_sprint64/live_session64.py:151` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DATA_START", self.session_id, cycle_id, target_dt.isoformat()))` | SERIALIZE | SIM |
| 430 | `mercury_ai/operations/m5_sprint64/live_session64.py:152` | isoformat | `Sprint64LiveSession::run` | `clock_start_iso = clock_now_at_start.isoformat()` | SERIALIZE | SIM |
| 431 | `mercury_ai/operations/m5_sprint64/live_session64.py:161` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DATA_TIMEOUT", self.session_id, cycle_id, target_dt.isoformat(), asset=sy` | SERIALIZE | SIM |
| 432 | `mercury_ai/operations/m5_sprint64/live_session64.py:163` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DATA_UNAVAILABLE", self.session_id, cycle_id, target_dt.isoformat(), asse` | SERIALIZE | SIM |
| 433 | `mercury_ai/operations/m5_sprint64/live_session64.py:165` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DATA_ERROR", self.session_id, cycle_id, target_dt.isoformat(), asset=sym)` | SERIALIZE | SIM |
| 434 | `mercury_ai/operations/m5_sprint64/live_session64.py:167` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DATA_COMPLETE", self.session_id, cycle_id, target_dt.isoformat(), asset=s` | SERIALIZE | SIM |
| 435 | `mercury_ai/operations/m5_sprint64/live_session64.py:169` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("WORKER_COMPLETE", self.session_id, cycle_id, target_dt.isoformat(), asset` | SERIALIZE | SIM |
| 436 | `mercury_ai/operations/m5_sprint64/live_session64.py:171` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("QUEUE_PRESSURE", self.session_id, cycle_id, target_dt.isoformat(), detail` | SERIALIZE | SIM |
| 437 | `mercury_ai/operations/m5_sprint64/live_session64.py:175` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new(et, self.session_id, cycle_id, target_dt.isoformat(), details=wd))` | SERIALIZE | SIM |
| 438 | `mercury_ai/operations/m5_sprint64/live_session64.py:176` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("ANALYSIS_COMPLETE", self.session_id, cycle_id, target_dt.isoformat()))` | SERIALIZE | SIM |
| 439 | `mercury_ai/operations/m5_sprint64/live_session64.py:177` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("RANKING_COMPLETE", self.session_id, cycle_id, target_dt.isoformat()))` | SERIALIZE | SIM |
| 440 | `mercury_ai/operations/m5_sprint64/live_session64.py:179` | datetime.fromisoformat | `Sprint64LiveSession::run` | `cs_dt = datetime.fromisoformat(str(r.get("cycle_start")).replace("Z", "+00:00"))` | PARSE | SIM se origem candle |
| 441 | `mercury_ai/operations/m5_sprint64/live_session64.py:183` | datetime.fromisoformat | `Sprint64LiveSession::run` | `ce_dt = datetime.fromisoformat(str(r.get("cycle_end")).replace("Z", "+00:00")) if r.get("cycle_end") else None` | PARSE | SIM se origem candle |
| 442 | `mercury_ai/operations/m5_sprint64/live_session64.py:187` | timedelta | `Sprint64LiveSession::run` | `decision_ready_dt = (cs_dt + timedelta(milliseconds=float(first_fresh_ms))) if first_fresh_ms is not None else None` | DURATION | SIM |
| 443 | `mercury_ai/operations/m5_sprint64/live_session64.py:188` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DECISION_READY", self.session_id, cycle_id, target_dt.isoformat(), detail` | SERIALIZE | SIM |
| 444 | `mercury_ai/operations/m5_sprint64/live_session64.py:189` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("DECISION_EMITTED", self.session_id, cycle_id, target_dt.isoformat(), deta` | SERIALIZE | SIM |
| 445 | `mercury_ai/operations/m5_sprint64/live_session64.py:203` | isoformat | `Sprint64LiveSession::run` | `"cycle_start": cs_dt.isoformat() if cs_dt else r.get("cycle_start"),` | SERIALIZE | SIM |
| 446 | `mercury_ai/operations/m5_sprint64/live_session64.py:204` | timedelta | `Sprint64LiveSession::run` | `"first_fresh_decision": (cs_dt + timedelta(milliseconds=float(first_fresh_ms))).isoformat() if first_fresh_ms is not Non` | DURATION | SIM |
| 447 | `mercury_ai/operations/m5_sprint64/live_session64.py:207` | isoformat | `Sprint64LiveSession::run` | `"cycle_complete": ce_dt.isoformat() if ce_dt else r.get("cycle_end"),` | SERIALIZE | SIM |
| 448 | `mercury_ai/operations/m5_sprint64/live_session64.py:220` | time.perf_counter | `Sprint64LiveSession::run` | `t0 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 449 | `mercury_ai/operations/m5_sprint64/live_session64.py:222` | time.perf_counter | `Sprint64LiveSession::run` | `t1 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 450 | `mercury_ai/operations/m5_sprint64/live_session64.py:225` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("AUDIT_COLLISION", self.session_id, cycle_id, target_dt.isoformat(), detai` | SERIALIZE | SIM |
| 451 | `mercury_ai/operations/m5_sprint64/live_session64.py:230` | isoformat | `Sprint64LiveSession::run` | `self.event_stream.emit(ObservabilityEvent.new("ARTIFACT_WRITTEN", self.session_id, cycle_id, target_dt.isoformat(), deta` | SERIALIZE | SIM |
| 452 | `mercury_ai/operations/m5_sprint64/live_session64.py:233` | datetime.now | `Sprint64LiveSession::run` | `self.end_wall = datetime.now(timezone.utc).isoformat()` | SYSTEM_WALL_UTC | CONDICIONAL (intencional wall, fora do replay) |
| 453 | `mercury_ai/operations/m5_sprint64/live_session64.py:255` | clock var | `Sprint64LiveSession::run` | `# aggregate live clock` | CLOCK_REF | - |
| 454 | `mercury_ai/operations/m5_sprint64/live_session64.py:278` | time.perf_counter | `Sprint64LiveSession::run` | `t0 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 455 | `mercury_ai/operations/m5_sprint64/live_session64.py:280` | time.perf_counter | `Sprint64LiveSession::run` | `t1 = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 456 | `mercury_ai/operations/m5_sprint64/live_session64.py:294` | time.perf_counter | `Sprint64LiveSession::run` | `"session_wall_s": time.perf_counter() - session_start_perf,` | MONOTONIC | SIM (não contamina decisão) |
| 457 | `mercury_ai/providers/future_tradingview_provider.py:20` | import time | `-::-` | `import time` | IMPORT | - |
| 458 | `mercury_ai/providers/future_tradingview_provider.py:79` | time.monotonic | `_CacheEntry::__init__` | `self.expires_at = time.monotonic() + ttl_seconds` | MONOTONIC | SIM (não contamina decisão) |
| 459 | `mercury_ai/providers/future_tradingview_provider.py:82` | time.monotonic | `_CacheEntry::is_valid` | `return time.monotonic() < self.expires_at` | MONOTONIC | SIM (não contamina decisão) |
| 460 | `mercury_ai/providers/future_tradingview_provider.py:231` | time.sleep | `FutureTradingViewProvider::_fetch_with_retry` | `time.sleep(wait)` | DELAY | SIM (fora do caminho determinístico) |
| 461 | `mercury_ai/providers/market_provider.py:3` | import time | `-::-` | `import time` | IMPORT | - |
| 462 | `mercury_ai/providers/market_provider.py:195` | time.time | `MercuryDataProvider::get_candles` | `start = time.time()` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 463 | `mercury_ai/providers/market_provider.py:199` | time.time | `MercuryDataProvider::get_candles` | `elapsed = time.time() - start` | WALL_EPOCH | CONDICIONAL (TTL wall, não decisão) |
| 464 | `mercury_ai/providers/market_provider.py:217` | time.sleep | `MercuryDataProvider::get_candles` | `time.sleep(0.5)` | DELAY | SIM (fora do caminho determinístico) |
| 465 | `mercury_ai/providers/market_provider.py:225` | time.sleep | `MercuryDataProvider::get_candles` | `time.sleep(0.5)` | DELAY | SIM (fora do caminho determinístico) |
| 466 | `mercury_ai/providers/yahoo_finance_provider.py:2` | import time | `-::-` | `import time` | IMPORT | - |
| 467 | `mercury_ai/providers/yahoo_finance_provider.py:4` | timedelta | `-::-` | `from datetime import datetime, timedelta` | DURATION | SIM |
| 468 | `mercury_ai/providers/yahoo_finance_provider.py:30` | time.monotonic | `_CacheEntry::__init__` | `self.expires_at = time.monotonic() + ttl_seconds` | MONOTONIC | SIM (não contamina decisão) |
| 469 | `mercury_ai/providers/yahoo_finance_provider.py:33` | time.monotonic | `_CacheEntry::is_valid` | `return time.monotonic() < self.expires_at` | MONOTONIC | SIM (não contamina decisão) |
| 470 | `mercury_ai/providers/yahoo_finance_provider.py:114` | time.sleep | `YahooFinanceProvider::_fetch_with_retry` | `time.sleep(wait)` | DELAY | SIM (fora do caminho determinístico) |
| 471 | `mercury_ai/sessions/market_sessions.py:1` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 472 | `mercury_ai/sessions/market_sessions.py:9` | datetime.utcnow | `MarketSessions::get_current_session` | `hour = datetime.utcnow().hour` | SYSTEM_WALL_DEPRECATED | NÃO |
| 473 | `mercury_ai/sessions/market_sessions.py:27` | datetime.utcnow | `MarketSessions::is_high_liquidity` | `hour = datetime.utcnow().hour` | SYSTEM_WALL_DEPRECATED | NÃO |
| 474 | `mercury_ai/sessions/tests/test_market_sessions.py:1` | market_sessions | `-::-` | `from mercury_ai.sessions.market_sessions import MarketSessions` | SESSION | - |
| 475 | `mercury_ai/utils/atomic_io.py:20` | import time | `-::-` | `import time` | IMPORT | - |
| 476 | `mercury_ai/utils/atomic_io.py:161` | time.sleep | `-::atomic_json_write` | `time.sleep(backoff_base * (2 ** attempt))` | DELAY | SIM (fora do caminho determinístico) |
| 477 | `mercury_ai/utils/deterministic_clock.py:2` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 478 | `mercury_ai/utils/deterministic_clock.py:6` | DeterministicClock | `DeterministicClock::-` | `class DeterministicClock:` | DETERMINISTIC | SIM |
| 479 | `mercury_ai/utils/deterministic_clock.py:51` | datetime.now | `DeterministicClock::utcnow` | `return datetime.now(timezone.utc).replace(tzinfo=None)` | SYSTEM_WALL_UTC | NÃO se em pipeline replay |
| 480 | `mercury_ai/utils/performance_collector.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 481 | `mercury_ai/utils/performance_collector.py:37` | time.perf_counter | `PerformanceCollector::stage` | `builder.start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 482 | `mercury_ai/utils/performance_collector.py:42` | time.perf_counter | `PerformanceCollector::stage` | `builder.end_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 483 | `mercury_ai/utils/report_generator.py:5` | import datetime | `-::-` | `import datetime` | IMPORT | - |
| 484 | `mercury_ai/utils/report_generator.py:16` | datetime.now | `BenchmarkReportGenerator::__init__` | `"timestamp": datetime.datetime.now().isoformat()` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 485 | `mercury_ai/utils/stress_tester.py:1` | import time | `-::-` | `import time` | IMPORT | - |
| 486 | `mercury_ai/utils/stress_tester.py:30` | time.perf_counter | `StressTester::run` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 487 | `mercury_ai/utils/stress_tester.py:38` | time.perf_counter | `StressTester::run` | `end_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 488 | `performance_benchmarking.py:28` | import time | `-::-` | `import time` | IMPORT | - |
| 489 | `performance_benchmarking.py:55` | time.perf_counter | `-::PipelineStageTimer` | `start = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 490 | `performance_benchmarking.py:60` | time.perf_counter | `-::PipelineStageTimer` | `timer.duration = time.perf_counter() - start` | MONOTONIC | SIM (não contamina decisão) |
| 491 | `performance_benchmarking.py:102` | time.perf_counter | `-::benchmark_pipeline` | `start = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 492 | `performance_benchmarking.py:109` | time.perf_counter | `-::benchmark_pipeline` | `total_time = time.perf_counter() - start` | MONOTONIC | SIM (não contamina decisão) |
| 493 | `run_decision_scenarios.py:24` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 494 | `run_decision_scenarios.py:40` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 495 | `run_decision_scenarios.py:325` | import time | `DecisionScenarioTester::_run_scenario` | `import time` | IMPORT | - |
| 496 | `run_decision_scenarios.py:327` | time.perf_counter | `DecisionScenarioTester::_run_scenario` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 497 | `run_decision_scenarios.py:410` | time.perf_counter | `DecisionScenarioTester::_run_scenario` | `execution_time = (time.perf_counter() - start_time) * 1000` | MONOTONIC | SIM (não contamina decisão) |
| 498 | `run_decision_scenarios.py:626` | datetime.now | `DecisionScenarioTester::generate_certification_report` | `timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 499 | `run_decision_scenarios.py:781` | datetime.now | `DecisionScenarioTester::generate_coverage_report` | `timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 500 | `run_decision_scenarios.py:1009` | datetime.now | `DecisionScenarioTester::save_results` | `timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 501 | `run_determinism_test.py:25` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 502 | `run_determinism_test.py:38` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 503 | `run_determinism_test.py:270` | datetime.now | `DeterminismTester::generate_report` | `timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 504 | `run_determinism_test.py:394` | DeterministicClock | `DeterminismTester::generate_report` | `5. **Deterministic Clock**: Uses `DeterministicClock` for all timestamps` | DETERMINISTIC | SIM |
| 505 | `run_determinism_test.py:451` | datetime.now | `DeterminismTester::save_results` | `results_file = output_dir / f"determinism_results_{self.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 506 | `run_institutional_replay.py:3` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 507 | `run_institutional_replay.py:36` | datetime.now | `-::generate_performance_report` | `lines.append(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")` | SYSTEM_WALL_NAIVE | NÃO (quebra replay, timezone local) |
| 508 | `run_instrumented.py:7` | pd.to_datetime | `MockProvider::get_data` | `return pd.DataFrame({'Open': [10], 'High': [11], 'Low': [9], 'Close': [10], 'Volume': [10]}, index=pd.to_datetime(['2025` | CANDLE_TIME | SIM |
| 509 | `s32_02_crash_harness.py:23` | import time | `-::-` | `import time` | IMPORT | - |
| 510 | `s32_02_crash_harness.py:86` | time.sleep | `-::run_atomic_json_write_test` | `time.sleep(kill_after_seconds)` | DELAY | SIM |
| 511 | `s32_02e_crash_harness_signals.py:6` | sleep( | `-::-` | `inter-process signaling instead of timing-based sleep().` | DELAY | SIM |
| 512 | `s32_02e_crash_harness_signals.py:22` | import time | `-::-` | `import time` | IMPORT | - |
| 513 | `s32_02e_crash_harness_signals.py:136` | time.sleep | `-::run_atomic_json_write_with_signals` | `time.sleep(0.1)` | DELAY | SIM |
| 514 | `s32_02e_crash_harness_signals.py:211` | sleep( | `-::main` | `print("timing-based sleep(). Real OS process termination.")` | DELAY | SIM |
| 515 | `s32_03_crash_matrix.py:14` | import time | `-::-` | `import time` | IMPORT | - |
| 516 | `s32_03_crash_matrix.py:67` | time.sleep | `-::run_atomic_json_write_cycle` | `time.sleep(kill_delay)` | DELAY | SIM |
| 517 | `s32_03e_post_replace_crash_boundary.py:33` | import time | `-::-` | `import time` | IMPORT | - |
| 518 | `s32_03e_post_replace_crash_boundary.py:108` | time.sleep | `-::run_atomic_json_write_handshake_test` | `time.sleep(kill_after_seconds)` | DELAY | SIM |
| 519 | `s32_03e_post_replace_crash_boundary.py:259` | time.time | `-::run_s32_e3_cycles` | `test_data = {"test": "S32-E3", "cycle": cycle, "timestamp": time.time()}` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 520 | `s32_03e_post_replace_crash_boundary.py:283` | time.sleep | `-::run_s32_e3_cycles` | `time.sleep(0.2)` | DELAY | SIM |
| 521 | `s32_07_parallel_replay_stress.py:6` | clock var | `-::-` | `each using snapshot()/restore() pattern to isolate clock state.` | CLOCK_REF | - |
| 522 | `s32_07_parallel_replay_stress.py:8` | clock var | `-::-` | `Goal: Verify that snapshot/restore prevents clock cross-contamination between parallel replays.` | CLOCK_REF | - |
| 523 | `s32_07_parallel_replay_stress.py:14` | import time | `-::-` | `import time` | IMPORT | - |
| 524 | `s32_07_parallel_replay_stress.py:16` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 525 | `s32_07_parallel_replay_stress.py:20` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 526 | `s32_07_parallel_replay_stress.py:30` | datetime ctor | `-::-` | `"A": datetime(2025, 1, 1, 10, 0, 0),` | IMPORT | - |
| 527 | `s32_07_parallel_replay_stress.py:31` | datetime ctor | `-::-` | `"B": datetime(2025, 1, 1, 11, 0, 0),` | IMPORT | - |
| 528 | `s32_07_parallel_replay_stress.py:32` | datetime ctor | `-::-` | `"C": datetime(2025, 1, 1, 12, 0, 0),` | IMPORT | - |
| 529 | `s32_07_parallel_replay_stress.py:33` | datetime ctor | `-::-` | `"D": datetime(2025, 1, 1, 13, 0, 0),` | IMPORT | - |
| 530 | `s32_07_parallel_replay_stress.py:38` | clock var | `-::run_replay_with_snapshot_restore` | `"""Run a single replay with snapshot()/restore() pattern for clock isolation.` | CLOCK_REF | - |
| 531 | `s32_07_parallel_replay_stress.py:40` | clock var | `-::run_replay_with_snapshot_restore` | `This is the PATTERN that fixes the clock contamination issue:` | CLOCK_REF | - |
| 532 | `s32_07_parallel_replay_stress.py:46` | clock var | `-::run_replay_with_snapshot_restore` | `# Set unique replay_id and clock time for this replay` | CLOCK_REF | - |
| 533 | `s32_07_parallel_replay_stress.py:48` | DeterministicClock | `-::run_replay_with_snapshot_restore` | `DeterministicClock.set_time(start_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 534 | `s32_07_parallel_replay_stress.py:50` | clock var | `-::run_replay_with_snapshot_restore` | `# STEP 1: Snapshot the clock state BEFORE replay` | CLOCK_REF | - |
| 535 | `s32_07_parallel_replay_stress.py:51` | DeterministicClock | `-::run_replay_with_snapshot_restore` | `pre_snapshot = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 536 | `s32_07_parallel_replay_stress.py:58` | DeterministicClock | `-::run_replay_with_snapshot_restore` | `"start_time": DeterministicClock.utcnow(),` | DETERMINISTIC | SIM |
| 537 | `s32_07_parallel_replay_stress.py:63` | clock var | `-::run_replay_with_snapshot_restore` | `# Simulate replay processing with periodic clock checks` | CLOCK_REF | - |
| 538 | `s32_07_parallel_replay_stress.py:65` | clock var | `-::run_replay_with_snapshot_restore` | `# Check clock state - should reflect this replay's set time` | CLOCK_REF | - |
| 539 | `s32_07_parallel_replay_stress.py:66` | DeterministicClock | `-::run_replay_with_snapshot_restore` | `current_time = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 540 | `s32_07_parallel_replay_stress.py:74` | time.sleep | `-::run_replay_with_snapshot_restore` | `time.sleep(0.1)` | DELAY | SIM |
| 541 | `s32_07_parallel_replay_stress.py:76` | clock var | `-::run_replay_with_snapshot_restore` | `# STEP 2: RESTORE the clock state to pre-replay state` | CLOCK_REF | - |
| 542 | `s32_07_parallel_replay_stress.py:77` | clock var | `-::run_replay_with_snapshot_restore` | `# This prevents clock contamination for subsequent operations` | CLOCK_REF | - |
| 543 | `s32_07_parallel_replay_stress.py:78` | DeterministicClock | `-::run_replay_with_snapshot_restore` | `DeterministicClock.restore(pre_snapshot)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 544 | `s32_07_parallel_replay_stress.py:81` | DeterministicClock | `-::run_replay_with_snapshot_restore` | `engine_state["end_time"] = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 545 | `s32_07_parallel_replay_stress.py:115` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `print(f"  Clock state after restore: hour {result['state']['decisions'][0]['clock_hour']}:00")` | CLOCK_REF | - |
| 546 | `s32_07_parallel_replay_stress.py:128` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `# Extract clock hours from each replay's decisions (AFTER restore)` | CLOCK_REF | - |
| 547 | `s32_07_parallel_replay_stress.py:137` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `print(f"Replay {rid}: clock hours observed = {sorted(hours)}")` | CLOCK_REF | - |
| 548 | `s32_07_parallel_replay_stress.py:144` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `print("Expected vs Actual clock hours AFTER restore:")` | CLOCK_REF | - |
| 549 | `s32_07_parallel_replay_stress.py:149` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `# After restore, the clock should be back to the state before this replay started` | CLOCK_REF | - |
| 550 | `s32_07_parallel_replay_stress.py:181` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `print("✓ No clock cross-contamination detected after snapshot/restore")` | CLOCK_REF | - |
| 551 | `s32_07_parallel_replay_stress.py:188` | clock var | `-::test_parallel_replay_stress_with_snapshot_restore` | `overall = "FAIL - Clock cross-contamination detected despite snapshot/restore"` | CLOCK_REF | - |
| 552 | `s32_07_parallel_replay_stress.py:196` | DeterministicClock | `-::test_parallel_replay_stress_with_snapshot_restore` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 553 | `s32_c_parallel_clock_isolation.py:2` | clock var | `-::-` | `S32-C — Parallel Clock Isolation Closure Test` | CLOCK_REF | - |
| 554 | `s32_c_parallel_clock_isolation.py:4` | DeterministicClock | `-::-` | `Objective: Prove empirically that DeterministicClock instances remain isolated` | DETERMINISTIC | SIM |
| 555 | `s32_c_parallel_clock_isolation.py:8` | clock var | `-::-` | `Replay A → clock A` | CLOCK_REF | - |
| 556 | `s32_c_parallel_clock_isolation.py:9` | clock var | `-::-` | `Replay B → clock B` | CLOCK_REF | - |
| 557 | `s32_c_parallel_clock_isolation.py:10` | clock var | `-::-` | `Replay C → clock C` | CLOCK_REF | - |
| 558 | `s32_c_parallel_clock_isolation.py:11` | clock var | `-::-` | `Replay D → clock D` | CLOCK_REF | - |
| 559 | `s32_c_parallel_clock_isolation.py:23` | import time | `-::-` | `import time` | IMPORT | - |
| 560 | `s32_c_parallel_clock_isolation.py:25` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 561 | `s32_c_parallel_clock_isolation.py:31` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 562 | `s32_c_parallel_clock_isolation.py:36` | clock var | `-::test_s32_c_01_baseline_clock_ownership` | `S32-C-01: Baseline do Clock` | CLOCK_REF | - |
| 563 | `s32_c_parallel_clock_isolation.py:45` | clock var | `-::test_s32_c_01_baseline_clock_ownership` | `print("S32-C-01: Baseline do Clock")` | CLOCK_REF | - |
| 564 | `s32_c_parallel_clock_isolation.py:48` | clock var | `-::test_s32_c_01_baseline_clock_ownership` | `# Reset clock` | CLOCK_REF | - |
| 565 | `s32_c_parallel_clock_isolation.py:49` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 566 | `s32_c_parallel_clock_isolation.py:52` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `# By default, DeterministicClock uses class variables` | DETERMINISTIC | SIM |
| 567 | `s32_c_parallel_clock_isolation.py:53` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `initial_time = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 568 | `s32_c_parallel_clock_isolation.py:57` | datetime ctor | `-::test_s32_c_01_baseline_clock_ownership` | `set_time_a = datetime(2025, 1, 15, 10, 0, 0)` | IMPORT | - |
| 569 | `s32_c_parallel_clock_isolation.py:58` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `DeterministicClock.set_time(set_time_a)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 570 | `s32_c_parallel_clock_isolation.py:59` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `after_set = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 571 | `s32_c_parallel_clock_isolation.py:64` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `is_shared = DeterministicClock._current_time is not None` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 572 | `s32_c_parallel_clock_isolation.py:66` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `print(f"\n_central_time after set: {DeterministicClock._current_time}")` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 573 | `s32_c_parallel_clock_isolation.py:68` | DeterministicClock | `-::test_s32_c_01_baseline_clock_ownership` | `print(f"_lock is also class-level: {DeterministicClock._lock}")` | DETERMINISTIC | SIM |
| 574 | `s32_c_parallel_clock_isolation.py:73` | clock var | `-::test_s32_c_01_baseline_clock_ownership` | `print("This means concurrent threads share the same clock state, causing potential contamination.")` | CLOCK_REF | - |
| 575 | `s32_c_parallel_clock_isolation.py:101` | clock var | `-::test_s32_c_02_instrumentation_observation` | `# Reset clock` | CLOCK_REF | - |
| 576 | `s32_c_parallel_clock_isolation.py:102` | DeterministicClock | `-::test_s32_c_02_instrumentation_observation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 577 | `s32_c_parallel_clock_isolation.py:108` | clock var | `-::worker_observation` | `"""Observa o clock durante a execução, coletando dados por thread."""` | CLOCK_REF | - |
| 578 | `s32_c_parallel_clock_isolation.py:112` | DeterministicClock | `-::worker_observation` | `time_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 579 | `s32_c_parallel_clock_isolation.py:115` | DeterministicClock | `-::worker_observation` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 580 | `s32_c_parallel_clock_isolation.py:116` | DeterministicClock | `-::worker_observation` | `time_after_set = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 581 | `s32_c_parallel_clock_isolation.py:130` | datetime ctor | `-::test_s32_c_02_instrumentation_observation` | `("A", datetime(2025, 1, 15, 10, 0, 0)),` | IMPORT | - |
| 582 | `s32_c_parallel_clock_isolation.py:131` | datetime ctor | `-::test_s32_c_02_instrumentation_observation` | `("B", datetime(2025, 1, 15, 10, 0, 1)),` | IMPORT | - |
| 583 | `s32_c_parallel_clock_isolation.py:132` | datetime ctor | `-::test_s32_c_02_instrumentation_observation` | `("C", datetime(2025, 1, 15, 10, 0, 2)),` | IMPORT | - |
| 584 | `s32_c_parallel_clock_isolation.py:133` | datetime ctor | `-::test_s32_c_02_instrumentation_observation` | `("D", datetime(2025, 1, 15, 10, 0, 3)),` | IMPORT | - |
| 585 | `s32_c_parallel_clock_isolation.py:173` | clock var | `-::test_s32_c_03_barrier_synchronization` | `A lê clock B lê clock C lê clock D lê clock` | CLOCK_REF | - |
| 586 | `s32_c_parallel_clock_isolation.py:182` | DeterministicClock | `-::test_s32_c_03_barrier_synchronization` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 587 | `s32_c_parallel_clock_isolation.py:193` | clock var | `-::worker_barrier` | `"""Worker that sets clock and waits at barrier."""` | CLOCK_REF | - |
| 588 | `s32_c_parallel_clock_isolation.py:196` | clock var | `-::worker_barrier` | `# Set clock before barrier` | CLOCK_REF | - |
| 589 | `s32_c_parallel_clock_isolation.py:197` | DeterministicClock | `-::worker_barrier` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 590 | `s32_c_parallel_clock_isolation.py:206` | clock var | `-::worker_barrier` | `# After barrier - read clock` | CLOCK_REF | - |
| 591 | `s32_c_parallel_clock_isolation.py:207` | DeterministicClock | `-::worker_barrier` | `clock_after = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 592 | `s32_c_parallel_clock_isolation.py:208` | DeterministicClock | `-::worker_barrier` | `clock_shared = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 593 | `s32_c_parallel_clock_isolation.py:222` | datetime ctor | `-::test_s32_c_03_barrier_synchronization` | `("A", datetime(2025, 1, 15, 10, 0, 0)),` | IMPORT | - |
| 594 | `s32_c_parallel_clock_isolation.py:223` | datetime ctor | `-::test_s32_c_03_barrier_synchronization` | `("B", datetime(2025, 1, 15, 10, 0, 1)),` | IMPORT | - |
| 595 | `s32_c_parallel_clock_isolation.py:224` | datetime ctor | `-::test_s32_c_03_barrier_synchronization` | `("C", datetime(2025, 1, 15, 10, 0, 2)),` | IMPORT | - |
| 596 | `s32_c_parallel_clock_isolation.py:225` | datetime ctor | `-::test_s32_c_03_barrier_synchronization` | `("D", datetime(2025, 1, 15, 10, 0, 3)),` | IMPORT | - |
| 597 | `s32_c_parallel_clock_isolation.py:243` | clock var | `-::test_s32_c_03_barrier_synchronization` | `# Check if clock values are consistent after barrier` | CLOCK_REF | - |
| 598 | `s32_c_parallel_clock_isolation.py:247` | clock var | `-::test_s32_c_03_barrier_synchronization` | `print(f"\nUnique shared clock values after barrier: {unique_shared} (expected: 1 if shared, 4 if isolated)")` | CLOCK_REF | - |
| 599 | `s32_c_parallel_clock_isolation.py:254` | clock var | `-::test_s32_c_04_internal_clock_contamination` | `S32-C-04: Internal Clock Contamination Test` | CLOCK_REF | - |
| 600 | `s32_c_parallel_clock_isolation.py:262` | clock var | `-::test_s32_c_04_internal_clock_contamination` | `A internal clock == T_A internal clock == T_B internal clock == T_C internal clock == T_D` | CLOCK_REF | - |
| 601 | `s32_c_parallel_clock_isolation.py:266` | clock var | `-::test_s32_c_04_internal_clock_contamination` | `A internal clock == T_BA internal clock == T_C...` | CLOCK_REF | - |
| 602 | `s32_c_parallel_clock_isolation.py:269` | clock var | `-::test_s32_c_04_internal_clock_contamination` | `print("S32-C-04: Internal Clock Contamination Test")` | CLOCK_REF | - |
| 603 | `s32_c_parallel_clock_isolation.py:272` | DeterministicClock | `-::test_s32_c_04_internal_clock_contamination` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 604 | `s32_c_parallel_clock_isolation.py:283` | clock var | `-::worker_clock_contamination` | `"""Testa contaminação do clock durante execução concurrent."""` | CLOCK_REF | - |
| 605 | `s32_c_parallel_clock_isolation.py:290` | DeterministicClock | `-::worker_clock_contamination` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 606 | `s32_c_parallel_clock_isolation.py:292` | clock var | `-::worker_clock_contamination` | `# Immediately read back the clock` | CLOCK_REF | - |
| 607 | `s32_c_parallel_clock_isolation.py:293` | DeterministicClock | `-::worker_clock_contamination` | `observed_time = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 608 | `s32_c_parallel_clock_isolation.py:294` | DeterministicClock | `-::worker_clock_contamination` | `observed_utcnow = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 609 | `s32_c_parallel_clock_isolation.py:311` | datetime ctor | `-::test_s32_c_04_internal_clock_contamination` | `("A", datetime(2025, 1, 15, 10, 0, 0)),` | IMPORT | - |
| 610 | `s32_c_parallel_clock_isolation.py:312` | datetime ctor | `-::test_s32_c_04_internal_clock_contamination` | `("B", datetime(2025, 1, 15, 10, 0, 1)),` | IMPORT | - |
| 611 | `s32_c_parallel_clock_isolation.py:313` | datetime ctor | `-::test_s32_c_04_internal_clock_contamination` | `("C", datetime(2025, 1, 15, 10, 0, 2)),` | IMPORT | - |
| 612 | `s32_c_parallel_clock_isolation.py:314` | datetime ctor | `-::test_s32_c_04_internal_clock_contamination` | `("D", datetime(2025, 1, 15, 10, 0, 3)),` | IMPORT | - |
| 613 | `s32_c_parallel_clock_isolation.py:377` | DeterministicClock | `-::test_s32_c_05_repetition_adversarial` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 614 | `s32_c_parallel_clock_isolation.py:386` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `{"A": datetime(2025, 1, 15, 10, 0, 0), "B": datetime(2025, 1, 15, 10, 0, 1),` | IMPORT | - |
| 615 | `s32_c_parallel_clock_isolation.py:387` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `"C": datetime(2025, 1, 15, 10, 0, 2), "D": datetime(2025, 1, 15, 10, 0, 3)},` | IMPORT | - |
| 616 | `s32_c_parallel_clock_isolation.py:389` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `{"A": datetime(2025, 1, 15, 11, 10, 0), "B": datetime(2025, 1, 15, 11, 10, 1),` | IMPORT | - |
| 617 | `s32_c_parallel_clock_isolation.py:390` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `"C": datetime(2025, 1, 15, 11, 10, 2), "D": datetime(2025, 1, 15, 11, 10, 3)},` | IMPORT | - |
| 618 | `s32_c_parallel_clock_isolation.py:392` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `{"A": datetime(2025, 1, 15, 14, 30, 0), "B": datetime(2025, 1, 15, 14, 30, 1),` | IMPORT | - |
| 619 | `s32_c_parallel_clock_isolation.py:393` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `"C": datetime(2025, 1, 15, 14, 30, 2), "D": datetime(2025, 1, 15, 14, 30, 3)},` | IMPORT | - |
| 620 | `s32_c_parallel_clock_isolation.py:409` | datetime ctor | `-::test_s32_c_05_repetition_adversarial` | `base = datetime(2025, 1, 15, 10, 0, 0)` | IMPORT | - |
| 621 | `s32_c_parallel_clock_isolation.py:411` | timedelta | `-::test_s32_c_05_repetition_adversarial` | `"A": base + __import__('datetime').timedelta(minutes=round_num * 10),` | DURATION | SIM |
| 622 | `s32_c_parallel_clock_isolation.py:412` | timedelta | `-::test_s32_c_05_repetition_adversarial` | `"B": base + __import__('datetime').timedelta(minutes=round_num * 10 + 1),` | DURATION | SIM |
| 623 | `s32_c_parallel_clock_isolation.py:413` | timedelta | `-::test_s32_c_05_repetition_adversarial` | `"C": base + __import__('datetime').timedelta(minutes=round_num * 10 + 2),` | DURATION | SIM |
| 624 | `s32_c_parallel_clock_isolation.py:414` | timedelta | `-::test_s32_c_05_repetition_adversarial` | `"D": base + __import__('datetime').timedelta(minutes=round_num * 10 + 3),` | DURATION | SIM |
| 625 | `s32_c_parallel_clock_isolation.py:425` | DeterministicClock | `-::worker_adversarial` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 626 | `s32_c_parallel_clock_isolation.py:426` | DeterministicClock | `-::worker_adversarial` | `observed = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 627 | `s32_c_parallel_clock_isolation.py:479` | clock var | `-::test_s32_c_06_interleaving_adversarial` | `Registrar qual thread observou qual clock.` | CLOCK_REF | - |
| 628 | `s32_c_parallel_clock_isolation.py:485` | DeterministicClock | `-::test_s32_c_06_interleaving_adversarial` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 629 | `s32_c_parallel_clock_isolation.py:504` | clock var | `-::test_s32_c_06_interleaving_adversarial` | `# Reset clock` | CLOCK_REF | - |
| 630 | `s32_c_parallel_clock_isolation.py:505` | DeterministicClock | `-::test_s32_c_06_interleaving_adversarial` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 631 | `s32_c_parallel_clock_isolation.py:509` | datetime ctor | `-::test_s32_c_06_interleaving_adversarial` | `"A": datetime(2025, 1, 15, 10, 0, 0),` | IMPORT | - |
| 632 | `s32_c_parallel_clock_isolation.py:510` | datetime ctor | `-::test_s32_c_06_interleaving_adversarial` | `"B": datetime(2025, 1, 15, 10, 0, 1),` | IMPORT | - |
| 633 | `s32_c_parallel_clock_isolation.py:511` | datetime ctor | `-::test_s32_c_06_interleaving_adversarial` | `"C": datetime(2025, 1, 15, 10, 0, 2),` | IMPORT | - |
| 634 | `s32_c_parallel_clock_isolation.py:512` | datetime ctor | `-::test_s32_c_06_interleaving_adversarial` | `"D": datetime(2025, 1, 15, 10, 0, 3),` | IMPORT | - |
| 635 | `s32_c_parallel_clock_isolation.py:530` | DeterministicClock | `-::worker_interleaved` | `DeterministicClock.set_time(expected)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 636 | `s32_c_parallel_clock_isolation.py:531` | DeterministicClock | `-::worker_interleaved` | `observed = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 637 | `s32_c_parallel_clock_isolation.py:571` | clock var | `-::test_s32_c_07_replay_result_integrity` | `Além do clock, comparar:` | CLOCK_REF | - |
| 638 | `s32_c_parallel_clock_isolation.py:583` | DeterministicClock | `-::test_s32_c_07_replay_result_integrity` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 639 | `s32_c_parallel_clock_isolation.py:592` | DeterministicClock | `-::test_s32_c_07_replay_result_integrity` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 640 | `s32_c_parallel_clock_isolation.py:623` | clock var | `-::run_replay_isolated` | `"""Run a single replay in isolation, capturing clock state."""` | CLOCK_REF | - |
| 641 | `s32_c_parallel_clock_isolation.py:624` | clock var | `-::run_replay_isolated` | `# Capture clock before` | CLOCK_REF | - |
| 642 | `s32_c_parallel_clock_isolation.py:625` | DeterministicClock | `-::run_replay_isolated` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 643 | `s32_c_parallel_clock_isolation.py:636` | clock var | `-::run_replay_isolated` | `# Capture clock after` | CLOCK_REF | - |
| 644 | `s32_c_parallel_clock_isolation.py:637` | DeterministicClock | `-::run_replay_isolated` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 645 | `s32_c_parallel_clock_isolation.py:671` | clock var | `-::test_s32_c_07_replay_result_integrity` | `# Check if clock was contaminated (went from deterministic back to real)` | CLOCK_REF | - |
| 646 | `s32_c_parallel_clock_isolation.py:674` | clock var | `-::test_s32_c_07_replay_result_integrity` | `# Clock should be restored to original state` | CLOCK_REF | - |
| 647 | `s32_c_parallel_clock_isolation.py:715` | DeterministicClock | `-::test_s32_c_08_final_state_recovery` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 648 | `s32_c_parallel_clock_isolation.py:744` | DeterministicClock | `-::test_s32_c_08_final_state_recovery` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 649 | `s32_c_parallel_clock_isolation.py:745` | clock var | `-::test_s32_c_08_final_state_recovery` | `print(f"Clock before replay: {clock_before}")` | CLOCK_REF | - |
| 650 | `s32_c_parallel_clock_isolation.py:755` | DeterministicClock | `-::test_s32_c_08_final_state_recovery` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 651 | `s32_c_parallel_clock_isolation.py:756` | clock var | `-::test_s32_c_08_final_state_recovery` | `print(f"Clock after replay: {clock_after}")` | CLOCK_REF | - |
| 652 | `s32_c_parallel_clock_isolation.py:802` | clock var | `-::test_s32_c_09_r2_classification` | `# S32-C-04: Clock contamination` | CLOCK_REF | - |
| 653 | `s32_c_parallel_clock_isolation.py:825` | clock var | `-::test_s32_c_09_r2_classification` | `"S32-C-04 (Clock contamination)": is_pass_04,` | CLOCK_REF | - |
| 654 | `s32_c_parallel_clock_isolation.py:852` | clock var | `-::test_s32_c_09_r2_classification` | `r2_status = "Cannot observe internal state due to shared clock - need infrastructure fix"` | CLOCK_REF | - |
| 655 | `s32_c_parallel_clock_isolation.py:932` | clock var | `-::test_s32_c_12_regression` | `print("Note: No new failures should be introduced by the clock isolation tests.")` | CLOCK_REF | - |
| 656 | `s32_c_parallel_clock_isolation.py:989` | clock var | `-::test_s32_c_14_repository_integrity` | `clock isolation` | CLOCK_REF | - |
| 657 | `s32_c_parallel_clock_isolation.py:1075` | clock var | `-::test_s32_c_15_r2_closure_report` | `report_content = """# S32-C Parallel Clock Isolation Closure Report` | CLOCK_REF | - |
| 658 | `s32_c_parallel_clock_isolation.py:1078` | DeterministicClock | `-::test_s32_c_15_r2_closure_report` | `**Objective**: Prove empirically that DeterministicClock instances remain isolated during concurrent replay execution.` | DETERMINISTIC | SIM |
| 659 | `s32_c_parallel_clock_isolation.py:1101` | DeterministicClock | `-::test_s32_c_15_r2_closure_report` | `1. DeterministicClock._current_time is [SHARED/THREAD-LOCAL] state` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 660 | `s32_c_parallel_clock_isolation.py:1146` | clock var | `-::test_s32_c_16_gate_final` | `print("  R2 = NOT PROVEN:    Need to fix clock infrastructure first")` | CLOCK_REF | - |
| 661 | `s32_c_parallel_clock_isolation.py:1155` | clock var | `-::-` | `print("S32-C - Parallel Clock Isolation Closure Test Suite")` | CLOCK_REF | - |
| 662 | `s32_c_parallel_clock_isolation.py:1162` | DeterministicClock | `-::-` | `# Note: Some tests modify global state (DeterministicClock), so order matters` | DETERMINISTIC | SIM |
| 663 | `s32_c_parallel_clock_isolation.py:1164` | clock var | `-::-` | `print("\n--- Running S32-C-01: Baseline Clock Ownership ---")` | CLOCK_REF | - |
| 664 | `s32_c_parallel_clock_isolation.py:1173` | clock var | `-::-` | `print("\n--- Running S32-C-04: Internal Clock Contamination ---")` | CLOCK_REF | - |
| 665 | `s32_c_parallel_clock_isolation_focused.py:2` | clock var | `-::-` | `S32-C — Parallel Clock Isolation Closure Test (Focused Version)` | CLOCK_REF | - |
| 666 | `s32_c_parallel_clock_isolation_focused.py:4` | DeterministicClock | `-::-` | `This test focuses on the core question: is DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 667 | `s32_c_parallel_clock_isolation_focused.py:13` | import time | `-::-` | `import time` | IMPORT | - |
| 668 | `s32_c_parallel_clock_isolation_focused.py:15` | timezone | `-::-` | `from datetime import datetime, timezone` | TZ_AWARE | SIM |
| 669 | `s32_c_parallel_clock_isolation_focused.py:21` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 670 | `s32_c_parallel_clock_isolation_focused.py:26` | clock var | `-::test_baseline_shared_state` | `S32-C-01: Baseline do Clock` | CLOCK_REF | - |
| 671 | `s32_c_parallel_clock_isolation_focused.py:35` | clock var | `-::test_baseline_shared_state` | `print("S32-C-01: Baseline do Clock - SHARED STATE CONFIRMED")` | CLOCK_REF | - |
| 672 | `s32_c_parallel_clock_isolation_focused.py:38` | DeterministicClock | `-::test_baseline_shared_state` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 673 | `s32_c_parallel_clock_isolation_focused.py:41` | datetime ctor | `-::test_baseline_shared_state` | `set_time = datetime(2025, 1, 15, 10, 0, 0)` | IMPORT | - |
| 674 | `s32_c_parallel_clock_isolation_focused.py:42` | DeterministicClock | `-::test_baseline_shared_state` | `DeterministicClock.set_time(set_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 675 | `s32_c_parallel_clock_isolation_focused.py:45` | DeterministicClock | `-::test_baseline_shared_state` | `current = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 676 | `s32_c_parallel_clock_isolation_focused.py:52` | DeterministicClock | `-::test_baseline_shared_state` | `print("This means concurrent threads sharing the same DeterministicClock instance")` | DETERMINISTIC | SIM |
| 677 | `s32_c_parallel_clock_isolation_focused.py:60` | clock var | `-::test_concurrent_clock_observation` | `S32-C-04: Internal Clock Contamination Test (focused version)` | CLOCK_REF | - |
| 678 | `s32_c_parallel_clock_isolation_focused.py:66` | clock var | `-::test_concurrent_clock_observation` | `print("S32-C-04: Concurrent Clock Observation Test")` | CLOCK_REF | - |
| 679 | `s32_c_parallel_clock_isolation_focused.py:69` | DeterministicClock | `-::test_concurrent_clock_observation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 680 | `s32_c_parallel_clock_isolation_focused.py:77` | clock var | `-::worker_observation` | `"""Observe clock as a worker would."""` | CLOCK_REF | - |
| 681 | `s32_c_parallel_clock_isolation_focused.py:81` | DeterministicClock | `-::worker_observation` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 682 | `s32_c_parallel_clock_isolation_focused.py:84` | DeterministicClock | `-::worker_observation` | `observed_current = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 683 | `s32_c_parallel_clock_isolation_focused.py:85` | DeterministicClock | `-::worker_observation` | `observed_utcnow = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 684 | `s32_c_parallel_clock_isolation_focused.py:100` | datetime ctor | `-::test_concurrent_clock_observation` | `"A": datetime(2025, 1, 15, 10, 0, 0),` | IMPORT | - |
| 685 | `s32_c_parallel_clock_isolation_focused.py:101` | datetime ctor | `-::test_concurrent_clock_observation` | `"B": datetime(2025, 1, 15, 10, 0, 1),` | IMPORT | - |
| 686 | `s32_c_parallel_clock_isolation_focused.py:102` | datetime ctor | `-::test_concurrent_clock_observation` | `"C": datetime(2025, 1, 15, 10, 0, 2),` | IMPORT | - |
| 687 | `s32_c_parallel_clock_isolation_focused.py:103` | datetime ctor | `-::test_concurrent_clock_observation` | `"D": datetime(2025, 1, 15, 10, 0, 3),` | IMPORT | - |
| 688 | `s32_c_parallel_clock_isolation_focused.py:145` | clock var | `-::test_barrier_synchronized_observation` | `Tests clock observation with barrier synchronization to maximize race conditions.` | CLOCK_REF | - |
| 689 | `s32_c_parallel_clock_isolation_focused.py:148` | clock var | `-::test_barrier_synchronized_observation` | `print("S32-C-03: Barrier-Synchronized Clock Observation")` | CLOCK_REF | - |
| 690 | `s32_c_parallel_clock_isolation_focused.py:151` | DeterministicClock | `-::test_barrier_synchronized_observation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 691 | `s32_c_parallel_clock_isolation_focused.py:157` | clock var | `-::worker_barrier` | `"""Set clock and observe at barrier point."""` | CLOCK_REF | - |
| 692 | `s32_c_parallel_clock_isolation_focused.py:161` | DeterministicClock | `-::worker_barrier` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 693 | `s32_c_parallel_clock_isolation_focused.py:170` | clock var | `-::worker_barrier` | `# After barrier - observe clock` | CLOCK_REF | - |
| 694 | `s32_c_parallel_clock_isolation_focused.py:171` | DeterministicClock | `-::worker_barrier` | `observed_current = DeterministicClock._current_time` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 695 | `s32_c_parallel_clock_isolation_focused.py:182` | datetime ctor | `-::test_barrier_synchronized_observation` | `datetime(2025, 1, 15, 10, 0, i) for i in range(4)` | IMPORT | - |
| 696 | `s32_c_parallel_clock_isolation_focused.py:218` | DeterministicClock | `-::test_replay_integrity` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 697 | `s32_c_parallel_clock_isolation_focused.py:250` | clock var | `-::run_replay_isolated` | `"""Run a single replay and capture clock state."""` | CLOCK_REF | - |
| 698 | `s32_c_parallel_clock_isolation_focused.py:251` | DeterministicClock | `-::run_replay_isolated` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 699 | `s32_c_parallel_clock_isolation_focused.py:261` | DeterministicClock | `-::run_replay_isolated` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 700 | `s32_c_parallel_clock_isolation_focused.py:288` | clock var | `-::test_replay_integrity` | `print(f"\nTest {'PASS' if is_pass else 'FAIL'}: {'Clocks restored' if is_pass else 'Clock not restored'}")` | CLOCK_REF | - |
| 701 | `s32_c_parallel_clock_isolation_focused.py:351` | clock var | `-::test_s32_c_09_r2_classification` | `r2_reason = "Shared clock state prevents per-thread isolation proof"` | CLOCK_REF | - |
| 702 | `s32_c_parallel_clock_isolation_focused.py:376` | clock var | `-::-` | `print("S32-C - Parallel Clock Isolation Closure (Focused)")` | CLOCK_REF | - |
| 703 | `s32_e3_bridge_closure_execution.py:17` | import time | `-::-` | `import time` | IMPORT | - |
| 704 | `s32_e3_bridge_closure_execution.py:154` | time.time | `-::run_g_cycle` | `start_time = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 705 | `s32_e3_bridge_closure_execution.py:156` | time.time | `-::run_g_cycle` | `while time.time() - start_time < max_handshake_wait:` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 706 | `s32_e3_bridge_closure_execution.py:165` | time.time | `-::run_g_cycle` | `print(f"  G Cycle {cycle_num}: HANDHAKE_READY observed at {time.time()-start_time:.2f}s")` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 707 | `s32_e3_bridge_closure_execution.py:171` | time.sleep | `-::run_g_cycle` | `time.sleep(0.1)` | DELAY | SIM |
| 708 | `s32_e3_bridge_closure_execution.py:356` | time.sleep | `-::run_g_cycles_10` | `time.sleep(0.3)` | DELAY | SIM |
| 709 | `s32_e3_bridge_closure_execution.py:437` | time.sleep | `-::run_f_cycle` | `time.sleep(kill_delay)` | DELAY | SIM |
| 710 | `s32_e3_bridge_closure_execution.py:565` | time.sleep | `-::run_f_cycles_10` | `time.sleep(0.2)` | DELAY | SIM |
| 711 | `s32_e3_bridge_closure_pid_proof.py:16` | import time | `-::-` | `import time` | IMPORT | - |
| 712 | `s32_e3_f04_close_test.py:5` | sleep( | `-::-` | `Proves, without sleep() as evidence, that:` | DELAY | SIM |
| 713 | `s32_e3_f04_close_test.py:25` | import time | `-::-` | `import time` | IMPORT | - |
| 714 | `s32_e3_f04_close_test.py:50` | time.time | `-::get_cycle_data` | `"timestamp": time.time(),` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 715 | `s32_e3_f04_close_test.py:211` | time.time | `-::run_g_cycle` | `f"RELEASE {time.time()} "` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 716 | `s32_e3_f04_close_test.py:313` | time.time | `-::run_regression_tests` | `compile_start = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 717 | `s32_e3_f04_close_test.py:320` | time.time | `-::run_regression_tests` | `compile_duration = time.time() - compile_start` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 718 | `s32_e3_f04_close_test.py:324` | time.time | `-::run_regression_tests` | `pytest_start = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 719 | `s32_e3_f04_close_test.py:332` | time.time | `-::run_regression_tests` | `pytest_duration = time.time() - pytest_start` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 720 | `s32_e3_pid_replace_kill_proof.py:5` | import time | `-::-` | `import time` | IMPORT | - |
| 721 | `s32_e3_pid_replace_kill_proof.py:172` | time.time | `-::run_forensic_proof` | `"timestamp": int(time.time()),` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 722 | `s32_e3_task1_f_test.py:13` | import time | `-::-` | `import time` | IMPORT | - |
| 723 | `s32_e3_task1_f_test.py:78` | time.sleep | `-::run_f_test_cycle` | `time.sleep(kill_delay)` | DELAY | SIM |
| 724 | `s32_e3_task1_f_test.py:134` | time.time | `-::run_f_times_10` | `data_to_write = {"test": "F-point", "timestamp": time.time()}` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 725 | `s32_e3_task1_f_test.py:161` | time.sleep | `-::run_f_times_10` | `time.sleep(0.1)` | DELAY | SIM |
| 726 | `s32_e3_task2_g_basic.py:13` | import time | `-::-` | `import time` | IMPORT | - |
| 727 | `s32_e3_task2_g_basic.py:136` | time.sleep | `-::run_g_basic_cycles` | `time.sleep(0.3)` | DELAY | SIM |
| 728 | `s32_e3_task2_g_deterministic.py:9` | sleep( | `-::-` | `- NO sleep() or kill_after_seconds timing` | DELAY | SIM |
| 729 | `s32_e3_task2_g_deterministic.py:19` | import time | `-::-` | `import time` | IMPORT | - |
| 730 | `s32_e3_task2_g_deterministic.py:28` | sleep( | `-::run_g_deterministic_test` | `Run G deterministically without sleep().` | DELAY | SIM |
| 731 | `s32_e3_task2_g_deterministic.py:85` | time.time | `-::run_g_deterministic_test` | `start_time = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 732 | `s32_e3_task2_g_deterministic.py:87` | time.time | `-::run_g_deterministic_test` | `while time.time() - start_time < max_handshake_wait:` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 733 | `s32_e3_task2_g_deterministic.py:97` | time.time | `-::run_g_deterministic_test` | `print(f"  Cycle: HANDHAKE_READY observed at {time.time()-start_time:.2f}s")` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 734 | `s32_e3_task2_g_deterministic.py:101` | time.sleep | `-::run_g_deterministic_test` | `time.sleep(0.1)` | DELAY | SIM |
| 735 | `s32_e3_task2_g_deterministic.py:184` | time.time | `-::run_g_deterministic_cycles` | `test_data = {"test": "G-point", "cycle": cycle, "timestamp": time.time()}` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 736 | `s32_e3_task2_g_deterministic.py:193` | time.sleep | `-::run_g_deterministic_cycles` | `time.sleep(0.2)` | DELAY | SIM |
| 737 | `s32_e3_task2_g_extended.py:13` | import time | `-::-` | `import time` | IMPORT | - |
| 738 | `s32_e3_task2_g_extended.py:74` | time.time | `-::run_g_deterministic_with_retries` | `start_time = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 739 | `s32_e3_task2_g_extended.py:76` | time.time | `-::run_g_deterministic_with_retries` | `while time.time() - start_time < 5.0:  # max 5s to observe handshake` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 740 | `s32_e3_task2_g_extended.py:85` | time.time | `-::run_g_deterministic_with_retries` | `print(f"  HANDHAKE_READY observed at {time.time()-start_time:.2f}s")` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 741 | `s32_e3_task2_g_extended.py:89` | time.sleep | `-::run_g_deterministic_with_retries` | `time.sleep(0.2)` | DELAY | SIM |
| 742 | `s32_e3_task2_g_extended.py:102` | time.sleep | `-::run_g_deterministic_with_retries` | `time.sleep(post_handshake_wait)` | DELAY | SIM |
| 743 | `s32_e3_task2_g_extended.py:185` | time.sleep | `-::run_g_extended_wait_cycles` | `time.sleep(0.3)` | DELAY | SIM |
| 744 | `s32_e3_task2_g_natural.py:6` | sleep( | `-::-` | `e então observamos o resultado. Elimina o sleep()/kill() forçados.` | DELAY | SIM |
| 745 | `s32_e3_task2_g_natural.py:13` | import time | `-::-` | `import time` | IMPORT | - |
| 746 | `s32_e3_task2_g_natural.py:75` | time.time | `-::run_g_natural_completion` | `start_time = time.time()` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 747 | `s32_e3_task2_g_natural.py:77` | time.time | `-::run_g_natural_completion` | `while time.time() - start_time < 5.0:` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 748 | `s32_e3_task2_g_natural.py:86` | time.time | `-::run_g_natural_completion` | `print(f"  HANDHAKE_READY observed at {time.time()-start_time:.2f}s")` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 749 | `s32_e3_task2_g_natural.py:90` | time.sleep | `-::run_g_natural_completion` | `time.sleep(0.2)` | DELAY | SIM |
| 750 | `s32_e3_task2_g_natural.py:114` | time.sleep | `-::run_g_natural_completion` | `time.sleep(0.5)` | DELAY | SIM |
| 751 | `s32_e3_task2_g_natural.py:116` | time.time | `-::run_g_natural_completion` | `if time.time() - start_time > max_total_wait:` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 752 | `s32_e3_task2_g_natural.py:201` | time.sleep | `-::run_g_natural_cycles` | `time.sleep(0.5)` | DELAY | SIM |
| 753 | `stress_test_replay.py:3` | import time | `-::-` | `import time` | IMPORT | - |
| 754 | `stress_test_replay.py:30` | time.perf_counter | `-::run_stress_test` | `start_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 755 | `stress_test_replay.py:34` | time.perf_counter | `-::run_stress_test` | `end_time = time.perf_counter()` | MONOTONIC | SIM (não contamina decisão) |
| 756 | `test_3_cycles.py:93` | time.time | `-::-` | `data = {"_state": "NEW", "timestamp": int(time.time()), "cycle": cycle, "test": "test"}` | WALL_EPOCH | NÃO se usado para lógica de decisão |
| 757 | `test_3_cycles.py:98` | time.sleep | `-::-` | `time.sleep(0.3)` | DELAY | SIM |
| 758 | `test_atomic_simple.py:40` | import time | `-::-` | `import time` | IMPORT | - |
| 759 | `test_clock_isolation.py:1` | DeterministicClock | `-::-` | `"""Test script for DeterministicClock thread-local isolation."""` | DETERMINISTIC | SIM |
| 760 | `test_clock_isolation.py:4` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 761 | `test_clock_isolation.py:7` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 762 | `test_clock_isolation.py:11` | clock var | `-::test_thread_local_isolation` | `"""Test that each thread has its own isolated clock state."""` | CLOCK_REF | - |
| 763 | `test_clock_isolation.py:13` | DeterministicClock | `-::test_thread_local_isolation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 764 | `test_clock_isolation.py:16` | datetime ctor | `-::test_thread_local_isolation` | `set_time_a = datetime(2025, 1, 15, 10, 0, 0)` | IMPORT | - |
| 765 | `test_clock_isolation.py:17` | DeterministicClock | `-::test_thread_local_isolation` | `DeterministicClock.set_time(set_time_a)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 766 | `test_clock_isolation.py:18` | DeterministicClock | `-::test_thread_local_isolation` | `after_set = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 767 | `test_clock_isolation.py:22` | DeterministicClock | `-::test_thread_local_isolation` | `main_time = DeterministicClock._get_current_time()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 768 | `test_clock_isolation.py:27` | clock var | `-::test_thread_local_isolation` | `print("PASS: Main thread has isolated clock state\n")` | CLOCK_REF | - |
| 769 | `test_clock_isolation.py:31` | clock var | `-::test_worker_isolation` | `"""Test that worker threads don't contaminate each other's clock."""` | CLOCK_REF | - |
| 770 | `test_clock_isolation.py:33` | DeterministicClock | `-::test_worker_isolation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 771 | `test_clock_isolation.py:39` | DeterministicClock | `-::worker_set_and_read` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 772 | `test_clock_isolation.py:40` | DeterministicClock | `-::worker_set_and_read` | `observed = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 773 | `test_clock_isolation.py:48` | datetime ctor | `-::test_worker_isolation` | `args=(datetime(2025, 1, 15, 10, 0, 0), results, 'A'))` | IMPORT | - |
| 774 | `test_clock_isolation.py:50` | datetime ctor | `-::test_worker_isolation` | `args=(datetime(2025, 1, 15, 10, 0, 1), results, 'B'))` | IMPORT | - |
| 775 | `test_clock_isolation.py:69` | clock var | `-::test_worker_isolation` | `print("PASS: Worker threads have isolated clock state\n")` | CLOCK_REF | - |
| 776 | `test_clock_isolation.py:75` | DeterministicClock | `-::test_barrier_adversarial` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 777 | `test_clock_isolation.py:80` | clock var | `-::worker_barrier` | `'''Sets clock and reads after barrier - should only see its own time'''` | CLOCK_REF | - |
| 778 | `test_clock_isolation.py:81` | DeterministicClock | `-::worker_barrier` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 779 | `test_clock_isolation.py:84` | import time | `-::worker_barrier` | `import time` | IMPORT | - |
| 780 | `test_clock_isolation.py:85` | time.sleep | `-::worker_barrier` | `time.sleep(0.01)` | DELAY | SIM (fora do caminho determinístico) |
| 781 | `test_clock_isolation.py:87` | DeterministicClock | `-::worker_barrier` | `clock_after = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 782 | `test_clock_isolation.py:88` | DeterministicClock | `-::worker_barrier` | `clock_shared = DeterministicClock._get_current_time()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 783 | `test_clock_isolation.py:100` | datetime ctor | `-::test_barrier_adversarial` | `('A', datetime(2025, 1, 15, 10, 0, 0)),` | IMPORT | - |
| 784 | `test_clock_isolation.py:101` | datetime ctor | `-::test_barrier_adversarial` | `('B', datetime(2025, 1, 15, 10, 0, 1)),` | IMPORT | - |
| 785 | `test_clock_isolation.py:102` | datetime ctor | `-::test_barrier_adversarial` | `('C', datetime(2025, 1, 15, 10, 0, 2)),` | IMPORT | - |
| 786 | `test_clock_isolation.py:103` | datetime ctor | `-::test_barrier_adversarial` | `('D', datetime(2025, 1, 15, 10, 0, 3)),` | IMPORT | - |
| 787 | `test_clock_isolation.py:123` | clock var | `-::test_barrier_adversarial` | `print(f'  WARNING: {r["worker_id"]} sees shared clock != expected')` | CLOCK_REF | - |
| 788 | `test_clock_isolation.py:135` | DeterministicClock | `-::test_50_rounds` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 789 | `test_clock_isolation.py:145` | datetime ctor | `-::test_50_rounds` | `{"A": datetime(2025, 1, 15, 10, 0, 0), "B": datetime(2025, 1, 15, 10, 0, 1),` | IMPORT | - |
| 790 | `test_clock_isolation.py:146` | datetime ctor | `-::test_50_rounds` | `"C": datetime(2025, 1, 15, 10, 0, 2), "D": datetime(2025, 1, 15, 10, 0, 3)},` | IMPORT | - |
| 791 | `test_clock_isolation.py:148` | datetime ctor | `-::test_50_rounds` | `{"A": datetime(2025, 1, 15, 11, 10, 0), "B": datetime(2025, 1, 15, 11, 10, 1),` | IMPORT | - |
| 792 | `test_clock_isolation.py:149` | datetime ctor | `-::test_50_rounds` | `"C": datetime(2025, 1, 15, 11, 10, 2), "D": datetime(2025, 1, 15, 11, 10, 3)},` | IMPORT | - |
| 793 | `test_clock_isolation.py:151` | datetime ctor | `-::test_50_rounds` | `{"A": datetime(2025, 1, 15, 14, 30, 0), "B": datetime(2025, 1, 15, 14, 30, 1),` | IMPORT | - |
| 794 | `test_clock_isolation.py:152` | datetime ctor | `-::test_50_rounds` | `"C": datetime(2025, 1, 15, 14, 30, 2), "D": datetime(2025, 1, 15, 14, 30, 3)},` | IMPORT | - |
| 795 | `test_clock_isolation.py:162` | DeterministicClock | `-::worker_round` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 796 | `test_clock_isolation.py:163` | DeterministicClock | `-::worker_round` | `observed = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 797 | `test_clock_isolation.py:202` | DeterministicClock | `-::-` | `print("ALL TESTS PASSED - DeterministicClock thread-local isolation working correctly!")` | DETERMINISTIC | SIM |
| 798 | `test_gate3.py:6` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 799 | `test_gate3.py:9` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 800 | `test_gate3.py:12` | clock var | `-::-` | `# Reset clock to ensure deterministic behavior` | CLOCK_REF | - |
| 801 | `test_gate3.py:13` | datetime ctor | `-::-` | `DeterministicClock.set_time(datetime(2025, 1, 1, 9, 30, 0))` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 802 | `test_gate3_buy.py:6` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 803 | `test_gate3_buy.py:9` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 804 | `test_gate3_buy.py:11` | clock var | `-::-` | `# Reset clock` | CLOCK_REF | - |
| 805 | `test_gate3_buy.py:12` | datetime ctor | `-::-` | `DeterministicClock.set_time(datetime(2025, 1, 1, 9, 30, 0))` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 806 | `test_historical_replay_integration.py:1` | DeterministicClock | `-::-` | `"""Test script for HistoricalReplayEngine DeterministicClock integration (S32-D-08)."""` | DETERMINISTIC | SIM |
| 807 | `test_historical_replay_integration.py:4` | import time | `-::-` | `import time` | IMPORT | - |
| 808 | `test_historical_replay_integration.py:5` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 809 | `test_historical_replay_integration.py:9` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 810 | `test_historical_replay_integration.py:35` | clock var | `-::test_historical_replay_parallel_isolation` | `# Track clock states before and after each replay` | CLOCK_REF | - |
| 811 | `test_historical_replay_integration.py:41` | clock var | `-::run_replay_isolated` | `"""Run replay in isolated thread with clock state tracking."""` | CLOCK_REF | - |
| 812 | `test_historical_replay_integration.py:44` | clock var | `-::run_replay_isolated` | `# Capture clock state before replay` | CLOCK_REF | - |
| 813 | `test_historical_replay_integration.py:45` | DeterministicClock | `-::run_replay_isolated` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 814 | `test_historical_replay_integration.py:59` | clock var | `-::run_replay_isolated` | `# Capture clock state after replay` | CLOCK_REF | - |
| 815 | `test_historical_replay_integration.py:60` | DeterministicClock | `-::run_replay_isolated` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 816 | `test_historical_replay_integration.py:74` | clock var | `-::run_replay_isolated` | `# The key check: clock_after should either be None (real clock) or the last set time` | CLOCK_REF | - |
| 817 | `test_historical_replay_integration.py:94` | clock var | `-::test_historical_replay_parallel_isolation` | `print(f"    Clock before: {result['clock_before']}")` | CLOCK_REF | - |
| 818 | `test_historical_replay_integration.py:95` | clock var | `-::test_historical_replay_parallel_isolation` | `print(f"    Clock after: {result['clock_after']}")` | CLOCK_REF | - |
| 819 | `test_historical_replay_integration.py:106` | clock var | `-::test_historical_replay_parallel_isolation` | `print(f"    Clock after is valid datetime: OK")` | CLOCK_REF | - |
| 820 | `test_historical_replay_integration.py:109` | clock var | `-::test_historical_replay_parallel_isolation` | `print(f"    WARNING: Clock after is invalid - possible contamination!")` | CLOCK_REF | - |
| 821 | `test_historical_replay_integration.py:111` | clock var | `-::test_historical_replay_parallel_isolation` | `# Also verify that each thread's clock is independent` | CLOCK_REF | - |
| 822 | `test_historical_replay_integration.py:113` | clock var | `-::test_historical_replay_parallel_isolation` | `print(f"Test {'PASS' if contamination_count == 0 else 'FAIL'}: {'Clock isolation maintained' if contamination_count == 0` | CLOCK_REF | - |
| 823 | `test_historical_replay_integration.py:116` | clock var | `-::test_historical_replay_parallel_isolation` | `print("PASS: HistoricalReplayEngine parallel execution maintains clock isolation\n")` | CLOCK_REF | - |
| 824 | `test_historical_replay_integration.py:120` | clock var | `-::test_replay_clock_recovery` | `"""S32-D-10: Test clock recovery after replay."""` | CLOCK_REF | - |
| 825 | `test_historical_replay_integration.py:121` | clock var | `-::test_replay_clock_recovery` | `print("=== S32-D-10: Clock Recovery Test ===")` | CLOCK_REF | - |
| 826 | `test_historical_replay_integration.py:126` | clock var | `-::test_replay_clock_recovery` | `# Capture clock state before replay` | CLOCK_REF | - |
| 827 | `test_historical_replay_integration.py:127` | DeterministicClock | `-::test_replay_clock_recovery` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 828 | `test_historical_replay_integration.py:128` | clock var | `-::test_replay_clock_recovery` | `print(f"Clock before replay: {clock_before}")` | CLOCK_REF | - |
| 829 | `test_historical_replay_integration.py:143` | clock var | `-::test_replay_clock_recovery` | `# Capture clock state after replay` | CLOCK_REF | - |
| 830 | `test_historical_replay_integration.py:144` | DeterministicClock | `-::test_replay_clock_recovery` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 831 | `test_historical_replay_integration.py:145` | clock var | `-::test_replay_clock_recovery` | `print(f"Clock after replay: {clock_after}")` | CLOCK_REF | - |
| 832 | `test_historical_replay_integration.py:147` | clock var | `-::test_replay_clock_recovery` | `# Check recovery: clock_after should equal clock_before (or be None for real clock)` | CLOCK_REF | - |
| 833 | `test_historical_replay_integration.py:149` | clock var | `-::test_replay_clock_recovery` | `print("PASS: Clock state unchanged (same object reference)")` | CLOCK_REF | - |
| 834 | `test_historical_replay_integration.py:151` | clock var | `-::test_replay_clock_recovery` | `print("PASS: Clock state recovered to original value")` | CLOCK_REF | - |
| 835 | `test_historical_replay_integration.py:153` | clock var | `-::test_replay_clock_recovery` | `print("INFO: Clock restored to real mode (None) - also valid")` | CLOCK_REF | - |
| 836 | `test_historical_replay_integration.py:159` | clock var | `-::test_replay_clock_recovery` | `print("PASS: Clock recovered within 1 second (essentially unchanged)")` | CLOCK_REF | - |
| 837 | `test_historical_replay_integration.py:161` | clock var | `-::test_replay_clock_recovery` | `print(f"WARN: Clock difference of {abs((clock_after - clock_before).total_seconds())} seconds")` | CLOCK_REF | - |
| 838 | `test_historical_replay_integration.py:163` | clock var | `-::test_replay_clock_recovery` | `print("PASS: Clock recovery test completed\n")` | CLOCK_REF | - |
| 839 | `test_interleavings.py:1` | DeterministicClock | `-::-` | `"""Test script for DeterministicClock interleavings adversarial patterns."""` | DETERMINISTIC | SIM |
| 840 | `test_interleavings.py:4` | import time | `-::-` | `import time` | IMPORT | - |
| 841 | `test_interleavings.py:5` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 842 | `test_interleavings.py:8` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 843 | `test_interleavings.py:14` | DeterministicClock | `-::test_interleavings` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 844 | `test_interleavings.py:20` | DeterministicClock | `-::test_interleavings` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 845 | `test_interleavings.py:29` | time.sleep | `-::worker` | `time.sleep(delay_before)` | DELAY | SIM |
| 846 | `test_interleavings.py:31` | DeterministicClock | `-::worker` | `DeterministicClock.set_time(expected_time)` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 847 | `test_interleavings.py:33` | clock var | `-::worker` | `# Read clock immediately after set` | CLOCK_REF | - |
| 848 | `test_interleavings.py:34` | DeterministicClock | `-::worker` | `observed = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 849 | `test_interleavings.py:37` | time.sleep | `-::worker` | `time.sleep(delay_after)` | DELAY | SIM |
| 850 | `test_interleavings.py:56` | datetime ctor | `-::test_interleavings` | `datetime(2025, 1, 15, 10, 0, 0),` | IMPORT | - |
| 851 | `test_interleavings.py:57` | datetime ctor | `-::test_interleavings` | `datetime(2025, 1, 15, 10, 0, 1),` | IMPORT | - |
| 852 | `test_interleavings.py:58` | datetime ctor | `-::test_interleavings` | `datetime(2025, 1, 15, 10, 0, 2),` | IMPORT | - |
| 853 | `test_interleavings.py:59` | datetime ctor | `-::test_interleavings` | `datetime(2025, 1, 15, 10, 0, 3),` | IMPORT | - |
| 854 | `test_interleavings.py:91` | clock var | `-::test_interleavings` | `print("PASS: All interleaving patterns maintain clock isolation\n")` | CLOCK_REF | - |
| 855 | `test_s28_07.py:11` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 856 | `test_s28_07.py:36` | isoformat | `MockSnapshot::__init__` | `self.timestamp = DeterministicClock.utcnow().isoformat()` | DETERMINISTIC | SIM |
| 857 | `test_s31_03.py:5` | clock var | `-::-` | `Cada replay deve preservar independentemente: replay_id, clock, audit_id, resultado, analytics, learning, memory.` | CLOCK_REF | - |
| 858 | `test_s31_03.py:19` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 859 | `test_s31_03.py:49` | clock var | `-::run_single_replay` | `# Capture clock state before` | CLOCK_REF | - |
| 860 | `test_s31_03.py:50` | DeterministicClock | `-::run_single_replay` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 861 | `test_s31_03.py:67` | clock var | `-::run_single_replay` | `# Capture clock state after` | CLOCK_REF | - |
| 862 | `test_s31_03.py:68` | DeterministicClock | `-::run_single_replay` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 863 | `test_s31_03.py:71` | clock var | `-::run_single_replay` | `# Get clock state after restore` | CLOCK_REF | - |
| 864 | `test_s31_03.py:72` | DeterministicClock | `-::run_single_replay` | `clock_now = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 865 | `test_s31_03.py:73` | DeterministicClock | `-::run_single_replay` | `print(f"Replay #{replay_idx}: DeterministicClock.utcnow() = {clock_now}")` | DETERMINISTIC | SIM |
| 866 | `test_s31_03.py:110` | clock var | `-::main` | `# Reset deterministic clock before tests` | CLOCK_REF | - |
| 867 | `test_s31_03.py:111` | DeterministicClock | `-::main` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 868 | `test_s31_03.py:112` | DeterministicClock | `-::main` | `print(f"DeterministicClock reset. Current time: {DeterministicClock.utcnow()}")` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 869 | `test_s31_03.py:159` | clock var | `-::main` | `print(f"  No clock contamination observed: {all_no_contamination}")` | CLOCK_REF | - |
| 870 | `test_s31_03.py:164` | clock var | `-::main` | `print("and no clock contamination was observed.")` | CLOCK_REF | - |
| 871 | `test_s31_03.py:170` | clock var | `-::main` | `print("Replays produced results but clock contamination was observed.")` | CLOCK_REF | - |
| 872 | `test_s31_03.py:171` | DeterministicClock | `-::main` | `print("This indicates the shared DeterministicClock._lock may cause")` | DETERMINISTIC | SIM |
| 873 | `test_s31_03_parallel_replay.py:5` | clock var | `-::-` | `Cada replay deve preservar independentemente: replay_id, clock, audit_id, resultado, analytics, learning, memory.` | CLOCK_REF | - |
| 874 | `test_s31_03_parallel_replay.py:14` | import datetime | `-::-` | `from datetime import datetime` | IMPORT | - |
| 875 | `test_s31_03_parallel_replay.py:15` | import time | `-::-` | `import time` | IMPORT | - |
| 876 | `test_s31_03_parallel_replay.py:26` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 877 | `test_s31_03_parallel_replay.py:56` | clock var | `-::run_single_replay` | `# Capture clock state before` | CLOCK_REF | - |
| 878 | `test_s31_03_parallel_replay.py:57` | DeterministicClock | `-::run_single_replay` | `clock_before = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 879 | `test_s31_03_parallel_replay.py:74` | clock var | `-::run_single_replay` | `# Capture clock state after` | CLOCK_REF | - |
| 880 | `test_s31_03_parallel_replay.py:75` | DeterministicClock | `-::run_single_replay` | `clock_after = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 881 | `test_s31_03_parallel_replay.py:112` | clock var | `-::run_single_replay` | `# Verify clock state is not contaminated (should be None after restore)` | CLOCK_REF | - |
| 882 | `test_s31_03_parallel_replay.py:113` | clock var | `-::run_single_replay` | `# The clock should be restored to its previous state` | CLOCK_REF | - |
| 883 | `test_s31_03_parallel_replay.py:114` | DeterministicClock | `-::run_single_replay` | `clock_check = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 884 | `test_s31_03_parallel_replay.py:115` | DeterministicClock | `-::run_single_replay` | `print(f"Replay #{replay_idx}: DeterministicClock.utcnow() = {clock_check}")` | DETERMINISTIC | SIM |
| 885 | `test_s31_03_parallel_replay.py:144` | clock var | `-::main` | `# Reset deterministic clock before tests` | CLOCK_REF | - |
| 886 | `test_s31_03_parallel_replay.py:145` | DeterministicClock | `-::main` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 887 | `test_s31_03_parallel_replay.py:146` | DeterministicClock | `-::main` | `print(f"DeterministicClock reset. Current time: {DeterministicClock.utcnow()}")` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 888 | `test_s31_03_parallel_replay.py:195` | clock var | `-::main` | `print(f"  - No clock contamination observed: {all_no_contamination}")` | CLOCK_REF | - |
| 889 | `test_s31_03_parallel_replay.py:203` | clock var | `-::main` | `print("   and no clock contamination was observed.")` | CLOCK_REF | - |
| 890 | `test_s31_03_parallel_replay.py:211` | clock var | `-::main` | `print("   Replays produced results but clock contamination was observed.")` | CLOCK_REF | - |
| 891 | `test_s31_03_parallel_replay.py:212` | DeterministicClock | `-::main` | `print("   This indicates the shared DeterministicClock._lock may cause")` | DETERMINISTIC | SIM |
| 892 | `test_s31_04.py:2` | DeterministicClock | `-::-` | `S31-04 — DeterministicClock Hardening Test` | DETERMINISTIC | SIM |
| 893 | `test_s31_04.py:6` | clock var | `-::-` | `Objetivo: descobrir se o clock compartilhado gera interferência real.` | CLOCK_REF | - |
| 894 | `test_s31_04.py:19` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 895 | `test_s31_04.py:43` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print("S31-04 — DeterministicClock Hardening Test")` | DETERMINISTIC | SIM |
| 896 | `test_s31_04.py:55` | clock var | `-::test_s31_04_clock_hardening` | `# Reset clock` | CLOCK_REF | - |
| 897 | `test_s31_04.py:56` | DeterministicClock | `-::test_s31_04_clock_hardening` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 898 | `test_s31_04.py:57` | DeterministicClock | `-::test_s31_04_clock_hardening` | `clock_1_before = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 899 | `test_s31_04.py:58` | clock var | `-::test_s31_04_clock_hardening` | `print(f"Clock reset. utcnow() before: {clock_1_before}")` | SYSTEM_WALL_DEPRECATED | NÃO |
| 900 | `test_s31_04.py:70` | clock var | `-::test_s31_04_clock_hardening` | `# Capture clock state after replay A` | CLOCK_REF | - |
| 901 | `test_s31_04.py:71` | DeterministicClock | `-::test_s31_04_clock_hardening` | `clock_1_after = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 902 | `test_s31_04.py:72` | DeterministicClock | `-::test_s31_04_clock_hardening` | `snapshot_1 = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 903 | `test_s31_04.py:73` | clock var | `-::test_s31_04_clock_hardening` | `print(f"Clock utcnow() after Replay A: {clock_1_after}")` | SYSTEM_WALL_DEPRECATED | NÃO |
| 904 | `test_s31_04.py:74` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print(f"DeterministicClock.snapshot() after Replay A: {snapshot_1}")` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 905 | `test_s31_04.py:79` | clock var | `-::test_s31_04_clock_hardening` | `# Reset clock to simulate "normal" period` | CLOCK_REF | - |
| 906 | `test_s31_04.py:80` | DeterministicClock | `-::test_s31_04_clock_hardening` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 907 | `test_s31_04.py:81` | DeterministicClock | `-::test_s31_04_clock_hardening` | `clock_2_before = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 908 | `test_s31_04.py:82` | clock var | `-::test_s31_04_clock_hardening` | `print(f"Clock reset (normal period). utcnow() before Replay B: {clock_2_before}")` | SYSTEM_WALL_DEPRECATED | NÃO |
| 909 | `test_s31_04.py:93` | clock var | `-::test_s31_04_clock_hardening` | `# Capture clock state after replay B` | CLOCK_REF | - |
| 910 | `test_s31_04.py:94` | DeterministicClock | `-::test_s31_04_clock_hardening` | `clock_2_after = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 911 | `test_s31_04.py:95` | DeterministicClock | `-::test_s31_04_clock_hardening` | `snapshot_2 = DeterministicClock.snapshot()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 912 | `test_s31_04.py:96` | clock var | `-::test_s31_04_clock_hardening` | `print(f"Clock utcnow() after Replay B: {clock_2_after}")` | SYSTEM_WALL_DEPRECATED | NÃO |
| 913 | `test_s31_04.py:97` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print(f"DeterministicClock.snapshot() after Replay B: {snapshot_2}")` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 914 | `test_s31_04.py:99` | clock var | `-::test_s31_04_clock_hardening` | `# === PHASE 3: Verify clock isolation ===` | CLOCK_REF | - |
| 915 | `test_s31_04.py:100` | clock var | `-::test_s31_04_clock_hardening` | `print("\n--- PHASE 3: Verify clock isolation ---")` | CLOCK_REF | - |
| 916 | `test_s31_04.py:105` | clock var | `-::test_s31_04_clock_hardening` | `# The key test: after reset + replay B, the clock should behave as if` | CLOCK_REF | - |
| 917 | `test_s31_04.py:109` | clock var | `-::test_s31_04_clock_hardening` | `# (the clock should have been reset)` | CLOCK_REF | - |
| 918 | `test_s31_04.py:114` | DeterministicClock | `-::test_s31_04_clock_hardening` | `final_clock = DeterministicClock.utcnow()` | DETERMINISTIC | SIM |
| 919 | `test_s31_04.py:115` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print(f"Final DeterministicClock.utcnow(): {final_clock}")` | DETERMINISTIC | SIM |
| 920 | `test_s31_04.py:119` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print("S31-04 — DeterministicClock Hardening Results")` | DETERMINISTIC | SIM |
| 921 | `test_s31_04.py:124` | clock var | `-::test_s31_04_clock_hardening` | `print(f"  Final clock state: {final_clock}")` | CLOCK_REF | - |
| 922 | `test_s31_04.py:129` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print("   DeterministicClock hardening validated - no interference detected")` | DETERMINISTIC | SIM |
| 923 | `test_s31_04.py:134` | clock var | `-::test_s31_04_clock_hardening` | `print("   Potential clock interference detected between sequential replays")` | CLOCK_REF | - |
| 924 | `test_s31_04.py:136` | DeterministicClock | `-::test_s31_04_clock_hardening` | `print("   - Considerar hardening do DeterministicClock com thread-local storage")` | DETERMINISTIC | SIM |
| 925 | `test_s31_04.py:145` | clock var | `-::test_s31_04_parallel_vs_sequential` | `print("S31-04 Bonus: Parallel vs Sequential Clock Comparison")` | CLOCK_REF | - |
| 926 | `test_s31_04.py:155` | DeterministicClock | `-::test_s31_04_parallel_vs_sequential` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 927 | `test_s31_04.py:159` | DeterministicClock | `-::test_s31_04_parallel_vs_sequential` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 928 | `test_s31_04.py:170` | DeterministicClock | `-::test_s31_04_parallel_vs_sequential` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 929 | `test_s31_04.py:205` | DeterministicClock | `-::-` | `print("\nThis test validates the DeterministicClock hardening without masking")` | DETERMINISTIC | SIM |
| 930 | `test_s31_05.py:19` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 931 | `test_s31_05.py:52` | DeterministicClock | `-::test_replay_determinism_identical_inputs` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 932 | `test_s31_05.py:62` | DeterministicClock | `-::test_replay_determinism_identical_inputs` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 933 | `test_s31_05.py:119` | DeterministicClock | `-::test_replay_determinism_different_inputs` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 934 | `test_s31_05.py:129` | DeterministicClock | `-::test_replay_determinism_different_inputs` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 935 | `test_s31_05.py:174` | DeterministicClock | `-::test_replay_id_uniqueness` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 936 | `test_s31_06.py:23` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 937 | `test_s31_06.py:53` | clock var | `-::test_s31_06_learning_analytics_chain` | `# Reset clock` | CLOCK_REF | - |
| 938 | `test_s31_06.py:54` | DeterministicClock | `-::test_s31_06_learning_analytics_chain` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 939 | `test_s31_06.py:99` | DeterministicClock | `-::test_s31_06_learning_analytics_chain` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 940 | `test_s31_06.py:166` | DeterministicClock | `-::test_s31_06_replay_id_primacy` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 941 | `test_s31_07.py:28` | DeterministicClock | `-::-` | `from mercury_ai.utils.deterministic_clock import DeterministicClock` | DETERMINISTIC | SIM |
| 942 | `test_s31_07.py:65` | clock var | `-::test_s31_07_persistence_restart` | `# Reset clock` | CLOCK_REF | - |
| 943 | `test_s31_07.py:66` | DeterministicClock | `-::test_s31_07_persistence_restart` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 944 | `test_s31_07.py:103` | clock var | `-::test_s31_07_persistence_restart` | `print("\n--- RESTART: Reset clock and reload ---")` | CLOCK_REF | - |
| 945 | `test_s31_07.py:105` | clock var | `-::test_s31_07_persistence_restart` | `# Reset clock (simulating restart)` | CLOCK_REF | - |
| 946 | `test_s31_07.py:106` | DeterministicClock | `-::test_s31_07_persistence_restart` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 947 | `test_s31_07.py:107` | clock var | `-::test_s31_07_persistence_restart` | `print(f"  Clock reset after restart")` | CLOCK_REF | - |
| 948 | `test_s31_07.py:204` | DeterministicClock | `-::test_s31_07_identifier_preservation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 949 | `test_s31_07.py:226` | DeterministicClock | `-::test_s31_07_identifier_preservation` | `DeterministicClock.reset()` | DETERMINISTIC_CONTROL | SIM (infra replay) |
| 950 | `test_s31_14.py:7` | clock var | `-::-` | `R2: Stress Replay Clock Race → RISK OBSERVED` | CLOCK_REF | - |
| 951 | `test_s31_14.py:34` | DeterministicClock | `-::-` | `"descricao": "Parallel Replay Clock Race - Shared DeterministicClock interference in parallel execution",` | DETERMINISTIC | SIM |
| 952 | `test_s31_14.py:36` | DeterministicClock | `-::-` | `"Identified risk: shared DeterministicClock._lock causes interference in "` | DETERMINISTIC | SIM |
| 953 | `test_s31_14.py:37` | clock var | `-::-` | `"ThreadPoolExecutor execution (3 of 4 replays showed clock contamination). "` | CLOCK_REF | - |
| 954 | `test_s31_14.py:38` | clock var | `-::-` | `"Experimentally verified clock state leakage between parallel replays "` | CLOCK_REF | - |
| 955 | `test_s31_14.py:44` | DeterministicClock | `-::-` | `"Per spec: risk from shared DeterministicClock class-level across "` | DETERMINISTIC | SIM |
| 956 | `test_s31_14.py:48` | DeterministicClock | `-::-` | `"Sprint 31 - S31-03 test confirmed shared DeterministicClock._lock causes "` | DETERMINISTIC | SIM |
| 957 | `test_s31_14.py:49` | clock var | `-::-` | `"interference in ThreadPoolExecutor (3 of 4 replays showed clock contamination). "` | CLOCK_REF | - |
| 958 | `test_s31_14.py:50` | clock var | `-::-` | `"Risk experimentally verified with concrete evidence of clock state leakage."` | CLOCK_REF | - |
| 959 | `test_s31_14.py:94` | clock var | `-::-` | `print("- R2: RISK OBSERVED - clock interference identified in parallel replay")` | CLOCK_REF | - |
| 960 | `test_s31_15.py:34` | DeterministicClock | `-::test_s31_15_final_c2_gate` | `# S31-04: DeterministicClock Hardening` | DETERMINISTIC | SIM |
| 961 | `test_s31_15.py:35` | DeterministicClock | `-::test_s31_15_final_c2_gate` | `print("\n4. S31-04: DeterministicClock Hardening - PASS")` | DETERMINISTIC | SIM |
| 962 | `test_s31_15.py:87` | clock var | `-::test_s31_15_final_c2_gate` | `print(f"R2 (Parallel Replay Clock Race): {r2}")` | CLOCK_REF | - |
| 963 | `test_s31_15.py:106` | clock var | `-::test_s31_15_final_c2_gate` | `print(f"   - R2: Parallel replay clock interference risk identified")` | CLOCK_REF | - |
| 964 | `test_s31_15.py:108` | clock var | `-::test_s31_15_final_c2_gate` | `print(f"   - All infrastructure blocks resolved (compile, clock isolation, strategy integrity)")` | CLOCK_REF | - |
| 965 | `test_s31_16.py:7` | clock var | `-::-` | `E2E comprovado; replay determinístico; persistence íntegra; clock seguro;` | CLOCK_REF | - |
| 966 | `test_s31_16.py:34` | clock var | `-::test_s31_16_v1_closure_gate` | `print("   - R2 (Parallel Replay Clock Race): RISK OBSERVED")` | CLOCK_REF | - |
| 967 | `test_s31_16.py:41` | DeterministicClock | `-::test_s31_16_v1_closure_gate` | `"S31-04: DeterministicClock Hardening → PASS (sequential)",` | DETERMINISTIC | SIM |
| 968 | `test_s31_16.py:73` | clock var | `-::test_s31_16_v1_closure_gate` | `"Clock seguro": True,  # S31-04 + S31-13` | CLOCK_REF | - |
| 969 | `test_s31_16.py:103` | clock var | `-::test_s31_16_v1_closure_gate` | `"- R2: Parallel replay clock interference risk identified but not fully verified for P/L corruption (RISK OBSERVED)\n"` | CLOCK_REF | - |
| 970 | `test_s31_17.py:40` | DeterministicClock | `-::generate_evidence_pack` | `{"test": "S31-03: Parallel Replay Stress", "observation": "RISK OBSERVED - clock interference in ThreadPoolExecutor", "c` | DETERMINISTIC | SIM |
| 971 | `test_s31_17.py:41` | clock var | `-::generate_evidence_pack` | `{"test": "S31-16: V1 Closure Gate", "observation": "R2 RISK OBSERVED - critical reservation remains open", "classificati` | CLOCK_REF | - |
| 972 | `test_s31_17.py:44` | DeterministicClock | `-::generate_evidence_pack` | `{"test": "S31-04: DeterministicClock Hardening", "observation": "Sequential hardening validated; class-level clock share` | DETERMINISTIC | SIM |
| 973 | `test_s31_17.py:45` | clock var | `-::generate_evidence_pack` | `{"test": "S31-15: Final C2 Gate", "observation": "Clock isolation pattern validated across all gates", "classification":` | CLOCK_REF | - |
| 974 | `test_s31_17.py:81` | clock var | `-::generate_evidence_pack` | `{"test": "S31-14: Reservation Closure Matrix", "observation": "R1=NOT PROVEN, R2=RISK OBSERVED documented per specificat` | CLOCK_REF | - |
| 975 | `test_s31_17.py:84` | clock var | `-::generate_evidence_pack` | `{"test": "S31-15: Final C2 Gate", "observation": "11/12 gates PASS; R1=NOT PROVEN, R2=RISK OBSERVED; C2 = PASS WITH RESE` | CLOCK_REF | - |
| 976 | `test_s31_17.py:133` | clock var | `-::generate_evidence_pack` | `print(f"  - R2: Parallel replay clock interference risk identified but not fully verified for P/L corruption (RISK OBSER` | CLOCK_REF | - |
| 977 | `test_s31_17.py:137` | clock var | `-::generate_evidence_pack` | `print(f"  ✅ Todos blocks de infraestrutura resolvidos (compile, clock isolation, strategy integrity)")` | CLOCK_REF | - |

## 6. Análise por Domínio Prioritário

### 6.1 `mercury_ai/utils/deterministic_clock.py`
- Linhas 51: `datetime.now(timezone.utc).replace(tzinfo=None)` — único ponto onde wall é lido quando não congelado. Intencional: fora de replay retorna wall naive UTC (compat com índice pandas naive). **Replay-safe por design.**
- Linhas 6-73: todo o arquivo é replay-safe.

### 6.2 `mercury_ai/core/analysis_pipeline.py` (≈ 650 linhas, 30 ocorrências)
- **Todos os 24 `DeterministicClock.utcnow()`** (linhas 167,214,231,257,291,309,318,325,330,335,341,346,351,356,361,367,372,377,382,387,419,435,455,460,465,472,524...) são **candle time em replay** via `historical_replay_engine.set_time` e **wall em live**. Caminho de decisão 100% determinístico.
- L167 `execution_time = (DeterministicClock.utcnow() - start_time)` — telemetria determinística (0s se start_time também determinístico em replay; correto).
- L200-201 `start_time.isoformat() / DeterministicClock.utcnow().isoformat()` — serialização determinística.
- L524 `strftime('%Y%m%d%H%M%S')` sobre deterministic clock para nome de arquivo runtime_report — replay-safe.
- **Veredito: 100% replay-safe. Nenhum `datetime.now` direto.**

### 6.3 `mercury_ai/operations/m5_*` (operacional live)
- **m5_operational/clock.py:** L33 `datetime.now(timezone.utc)` em `_next_boundary`, L46 em `_loop`, L103 em `run_cycles_blocking` — **wall UTC intencional** (scheduler M5 ancorado no relógio real). `time.sleep(chunk)` L54 com poll 1s para shutdown. `floor_m5/ceil_m5` de `temporal.py`. **Replay-safe: N/A (código live nunca executado durante replay).**
- **m5_operational/runner.py:** L225 `datetime.now(timezone.utc)` em `_next_target_candle`, L294 `cycle_start_iso`, L293/L382/L403/L431/L457/L637/L647 `time.perf_counter` para deadlines/timeouts monotônicos, L110 `from datetime import datetime as _dt` isolado em worker process. **Wall + monotonic intencional.** Runner é **orquestrador live**, não pipeline determinístico.
- **m5_operational/watchdog.py:** `time.monotonic` exclusivo (L42,43,57,62,87) — **monotônico puro, sem wall.**
- **m5_incremental/temporal.py:** L70,106,113,120,152,166 `datetime.now(timezone.utc)` em helpers `expected_latest_candle_open/current_candle/previous_candle/next_candle/decision_age/candle_age` + `floor_m5/ceil_m5/_ensure_utc` com `timedelta(minutes=5)`. **Wall UTC aware canônico para fronteiras M5 live.** Funções puras de cálculo de fronteira; `decision_candle_timestamp_from_df` usa `pd.to_datetime` + `_ensure_utc` sobre índice candle (replay-safe). **Veredito: wall correto para live; candle path separado.**
- **m5_incremental/*:** `asset_state.py` L91/L101 `mark_processing/mark_error` usa `datetime.now(timezone.utc)` para `updated_at` wall; L113-119 `age_seconds` com `fromisoformat` + wall. `cache_tracker.py` L68 `now = datetime.now(timezone.utc)` para `put`, `freshness.py` L64 wall para freshness gate, `rolling_queue.py` L58 wall para `cycle_start`. **Todos wall live, não contaminam pipeline replay (executam fora do DeterministicClock).**
- **m5_sprint6*/live_session*.py (6.0-6.4) + fault_harness:** ~90 ocorrências `datetime.now(timezone.utc)` para `start_wall/end_wall/clock_now_at_start/target_start/now_probe` + `time.sleep` alinhamento de fronteira + `time.perf_counter` para session_wall_s + `fromisoformat` parse de reports. **Live certification — wall é requisito §3/§15 (target <= clock).** `live_clock_integrity.py` e `live_session61-64` validam `target <= clock_now` com wall real. **Replay-safe: N/A (live only).**

### 6.4 `mercury_ai/data/market_data.py`
- **Zero ocorrências de tempo.** Apenas normalização `DataNormalizer.normalize(df)`. **Replay-safe trivial.** Caminho de dados puro, sem relógio.

### 6.5 `mercury_ai/providers/*`
- **yahoo_finance_provider.py:** `time.monotonic` L30/33 para `_CacheEntry` TTL 60s (monotônico, imune a NTP), `time.sleep(wait)` L114 retry exponencial 1/2/4s, `timedelta` import não usado diretamente. **Sem `datetime.now`.** `mercury_data_provider.py` (legado) L112 `time.monotonic`, L122/124 `time.time` wall epoch para timeout, L134 `time.sleep(2**attempt)`. `market_provider.py` L195/199 `time.time` para timeout 5s, L217/225 `time.sleep(0.5)` retry. `future_tradingview_provider.py` idem monotonic+sleep. **Todos providers usam monotonic para cache e epoch apenas para timeout de rede — não afetam decisão. Replay-safe.**
- **Cache TTL 60s wall:** stale-not-future por design; replay bypassa provider (usa HistoricalReplayProvider fatia inclusiva 0..i).

### 6.6 `mercury_ai/analysis/*` (engines)
- **benchmark_framework.py:** `time.perf_counter` L142/161/391/463/500/515 para latência wall (não decisão) + `DeterministicClock.utcnow().isoformat()` L182/L523 para timestamp do report (determinístico). **Replay-safe.**
- **candlestick_engine.py:** `time.perf_counter` L22/25/61 para exec_time wall. **Replay-safe.**
- **data_quality_engine.py (DEAD CODE):** L36 `delay = (datetime.now() - df.index.max()).total_seconds()` — **SYSTEM_WALL_NAIVE BUG**, não-determinístico, timezone local. **MORTO:** produção importa `data/data_quality_engine.py` (sem datetime). Só testes importam `analysis/data_quality_engine.py`. Não contamina produção, mas deve ser removido.
- **evidence_engine.py:** L33 `DeterministicClock.utcnow().isoformat()` — **replay-safe.**
- **health_checker.py:** `DeterministicClock.utcnow().isoformat()` L51 — replay-safe.
- **historical_replay_engine.py:** Infra determinística canônica — ver §4.
- **institutional_analytics_engine.py:** L95 `pd.to_datetime(..., format="mixed", utc=True)` — **candle time, preserva naive vs aware (B4-C5 fix).** Sem wall.
- **institutional_memory_engine.py:** `time.sleep(0.05*2**i)` L124 backoff flush — wall delay operacional, não decisão.
- **notification_center.py:** `DeterministicClock.utcnow().isoformat()` default_factory — replay-safe.
- **performance_analytics.py:** `datetime.fromisoformat` L20/L29 parse de `data['timestamp']` (persistido) — **replay-safe** (reconstrói candle time). Comentário L28 timezone normalize.
- **replay_batch_processor.py:** `time.perf_counter` L110/134 wall para total_wall_time — replay-safe.
- **session_engine.py:** L12 `DeterministicClock.utcnow().hour` — **ÚNICO engine que lê hora wall/candle para lógica de sessão**. Em replay retorna hora do candle (correto); em live retorna hora wall. **Replay-safe por design.**
- **Demais engines (18 engines):** `trend_analyzer`, `market_structure`, `volume_intelligence`, `confluence_engine`, `confidence_engine`, etc. — **zero ocorrências de tempo**. Puros em cima de `df` OHLCV.

### 6.7 Outros arquivos relevantes
- **sessions/market_sessions.py:** L9/L27 `datetime.utcnow().hour` — **DEPRECATED naive UTC**, usado apenas por `MarketSessions.get_current_session/is_high_liquidity`. **MORTO?** Não importado por pipeline canônico (`m5_incremental/temporal` e `session_engine` são canônicos). Bug latente se usado: hora naive sem tz, mas fora do caminho crítico.
- **core/pipeline_audit_middleware.py:** L22/L42 `datetime.now(timezone.utc).isoformat()` para `start_ts/timestamp` + `time.perf_counter` L23/39 para `duration_ms` — **wall UTC + monotonic, operacional observability, não replay.**
- **core/asset_registry.py:** L107 `time.time()` epoch para `last_operated` — wall epoch, não decisão.
- **core/health_center.py, observability_center.py:** `time.time()` epoch para metrics — wall.
- **core/job_manager.py:** `time.sleep(interval)` loop — delay operacional.
- **core/pipeline_profiler.py, utils/performance_collector.py, utils/stress_tester.py, performance_benchmarking.py:** `time.perf_counter` exclusivo — wall monotônico para profiling.
- **execution/*:** `demo_broker.py` L20, `order_executor.py` L45, `order_types.py` L84 `datetime.now(timezone.utc).isoformat()` helper `_utcnow_iso()` para `Order.timestamp` — **wall UTC para execução live, fora do replay.**
- **models/*:** `analysis_result.py` L49, `evidence.py` L21/L43, `security_center.py` L19 (AuditEvent), `session_manager.py` L14 — todos `DeterministicClock.utcnow().isoformat()` default_factory — **replay-safe.**
- **calendar/economic_calendar.py:** L8 `datetime.now().strftime("%Y-%m-%d")` — **SYSTEM_WALL_NAIVE**, mock estático de calendário econômico. **Morto/auxiliar**, não usado por pipeline.
- **database/history_logger.py:** L36 `datetime.now()` naive para CSV `analysis_history.csv` — **SYSTEM_WALL_NAIVE**, logger legado morto (não usado por `snapshot_logger` canônico que usa DeterministicClock).
- **news/news_provider.py:** L8 `datetime.now().strftime("%d/%m/%Y %H:%M")` — mock de notícia, morto.
- **utils/report_generator.py:** L16 `datetime.datetime.now().isoformat()` naive para `BenchmarkReportGenerator` metadata — **auxiliar wall, não pipeline.**

## 7. Matriz de Risco Replay

| Categoria | Exemplo | Risco | Ação |
|---|---|---|---|
| `SYSTEM_WALL_NAIVE` em `analysis/data_quality_engine.py:36` | `datetime.now() - df.index.max()` | **MORTO mas bug se ressuscitado** | Remover arquivo morto ou migrar para DeterministicClock + `_ensure_utc(df.index.max())` |
| `datetime.utcnow` em `sessions/market_sessions.py:9,27` | `hour = datetime.utcnow().hour` | **BAIXO (morto)** | Migrar para `datetime.now(timezone.utc)` ou `DeterministicClock` se for revivido |
| `SYSTEM_WALL_NAIVE` mocks | `economic_calendar`, `history_logger`, `news_provider`, `report_generator` | **INFO (fora do caminho crítico)** | Padronizar para `datetime.now(timezone.utc)` se mantidos |
| `time.time` para cache TTL | `yahoo_finance_provider` já usa `monotonic` (correto); `mercury_data_provider` legado usa `time.time` | **BAIXO** | Migrar restante para `monotonic` |
| `wall` em `m5_*` live | `datetime.now(timezone.utc)` scheduler/live_session | **Nenhum (intencional)** | Manter wall — live exige relógio real |
| `DeterministicClock` faltando | — | **Nenhum pendente** | Pipeline já 100% determinístico |

## 8. Evidências com Caminhos Relativos (exaustivo)

Arquivo bruto completo: `_audit_clock_detailed.txt` (1 472 linhas). Filtrado mercury_ai+raiz: `_audit_clock_filtered.txt`. Mercury-only: `_audit_clock_mercury_only.txt`.

### 8.1 Contagem por padrão (filtrado mercury_ai+raiz)

- `DeterministicClock`: 223
- `clock var`: 192
- `datetime.now`: 78
- `isoformat`: 77
- `import time`: 61
- `time.sleep`: 53
- `datetime ctor`: 53
- `time.perf_counter`: 49
- `timezone`: 41
- `time.time`: 34
- `timedelta`: 33
- `datetime.fromisoformat`: 29
- `import datetime`: 16
- `time.monotonic`: 12
- `sleep(`: 9
- `pd.Timestamp`: 7
- `pd.to_datetime`: 6
- `market_sessions`: 2
- `datetime.utcnow`: 2

### 8.2 Lista exaustiva (reproduzida do §5)

Ver tabela do §5 (todas as 300+ linhas com arquivo exato, linha, classe/função, código, tipo, replay-safe). Cada linha é evidência com caminho relativo.

## 9. Conclusão — Veredito

**APROVADO COM RESSALVAS MENORES.**

- **Caminho determinístico (pipeline + models + engines): 100% replay-safe via `DeterministicClock`.** Nenhum `datetime.now` direto no caminho de decisão. `historical_replay_engine` isola com `snapshot()/restore()` em `finally` + `threading.local()` para concorrência (B4-C1 fix).
- **Caminho live/operacional (M5 clock/runner/live_session/watchdog/providers): wall UTC + monotonic intencionais — correto e separado do replay.**
- **Candle time:** `pd.to_datetime` + `decision_candle_timestamp_from_df` + `temporal._ensure_utc` preservam timezone (B4-C5) e evitam look-ahead (fatia 0..i).
- **Únicos achados não-replay-safe estão em código MORTO/auxiliar:** `analysis/data_quality_engine.py:36` naive, `sessions/market_sessions.py` utcnow deprecated, mocks `economic_calendar/history_logger/news_provider`. Fora do caminho canônico, risco zero em produção, mas devem ser limpos para evitar ressurreição.
- **Monotonic correto:** `time.perf_counter` para latências, `time.monotonic` para cache TTL 60s e watchdog — imune a NTP.
- **Nenhum `time.time` crítico em decisão.** Apenas metrics/cache TTL.
- **Nenhum `sleep` em pipeline.** Apenas backoff/retry e scheduler M5.

### Recomendações

1. **Remover/arquivar** `mercury_ai/analysis/data_quality_engine.py` (duplicata morta) — já documentado como `VIVO_TESTS_TOOLS` apenas.
2. **Migrar** `sessions/market_sessions.py` de `utcnow` para `datetime.now(timezone.utc)` ou `DeterministicClock` se for reativado; hoje morto — baixa prioridade.
3. **Padronizar** mocks auxiliares (`economic_calendar`, `history_logger`, `news_provider`, `report_generator`) para `datetime.now(timezone.utc)` se mantidos.
4. **Manter** separação estrita: decisão → `DeterministicClock`; live/observabilidade → `datetime.now(timezone.utc)`; medição → `perf_counter/monotonic`; dados → `pd.to_datetime` + `_ensure_utc`.

---
*Gerado por auditoria automatizada exaustiva em 2026-09-05. Fontes: grep AST + leitura direta dos arquivos prioritários listados no §6.*
