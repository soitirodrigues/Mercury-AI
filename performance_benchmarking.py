"""Performance benchmarking — verificação de regressão de runtime do Mercury AI V1.

Mede o tempo de execução do pipeline real (AnalysisPipeline) e compara as
métricas atuais contra o baseline histórico gravado pelo próprio pipeline em
``runtime_report_{symbol}_{timestamp}.json`` na raiz do projeto
(ver ``mercury_ai/core/analysis_pipeline.py``, escrita de runtime_report).

CORREÇÃO B2 (SPRINT FORENSE 2):
  - Import de ``PipelineExecutor`` corrigido para o local canônico
    (``mercury_ai.core.pipeline_executor``). O namespace ``mercury_ai.brain``
    tem ``__init__.py`` vazio e não reexporta o símbolo — era a origem do
    ImportError reproduzido.
  - ``PipelineStageTimer`` implementado (antes: referência a símbolo
    inexistente -> NameError em runtime).
  - ``stage_timer`` inicializa ``_pipeline_metrics`` (antes: UnboundLocalError).
  - ``benchmark_pipeline()`` executa o pipeline real (AnalysisPipeline) em vez
    do contrato fictício ``load_data/validate/process/generate_report``, que
    NÃO existe em ``PipelineExecutor`` (que expõe apenas ``execute``).
  - ``load_historical_metrics()`` lê o formato real dos relatórios
    (``{"symbol": str, "stages": [{"engine_name", "execution_time", ...}]}``)
    do diretório correto (raiz do projeto).
  - ``check_regression()`` compara por ``engine_name`` com threshold 0.1 (10%)
    e levanta ``PerformanceRegressionError`` em regressão (contrato canônico de
    ``check_regression.py`` da raiz).
"""
import json
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from statistics import mean

from mercury_ai.core.pipeline_executor import PipelineExecutor

# Métricas coletadas pelos cronômetros de estágio (nome do estágio -> tempos em s).
_pipeline_metrics: dict = {}


class PerformanceRegressionError(Exception):
    """Levantada quando uma métrica atual regride além do threshold."""


class _StageTimer:
    """Cronômetro exposto por PipelineStageTimer (atributo ``.duration`` em s)."""

    __slots__ = ("duration",)

    def __init__(self):
        self.duration = 0.0


@contextmanager
def PipelineStageTimer(stage_name: str):
    """Cronometra um estágio; expõe ``timer.duration`` e registra a métrica."""
    start = time.perf_counter()
    timer = _StageTimer()
    try:
        yield timer
    finally:
        timer.duration = time.perf_counter() - start
        _pipeline_metrics.setdefault(stage_name, []).append(timer.duration)


def stage_timer(stage_name: str):
    """Decorator que cronometra uma função e registra a métrica do estágio."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            with PipelineStageTimer(stage_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def benchmark_pipeline(symbol: str = "BTC-USD") -> float:
    """Executa o pipeline real (AnalysisPipeline) para ``symbol`` e retorna o tempo total (s).

    O pipeline grava ``runtime_report_{symbol}_{timestamp}.json`` na raiz do
    projeto, com os tempos por estágio (engine_name/execution_time) que
    alimentam ``check_regression()``.

    Observação honesta: exige acesso ao provider de dados (rede). Se o
    pipeline falhar, ``analyze`` retorna um ``AnalysisResult`` de erro — o
    benchmark não "quebra silenciosamente", e o relatório de runtime escrito
    será parcial.
    """
    # Imports pesados carregados apenas quando o benchmark é executado.
    from mercury_ai.core.analysis_pipeline import AnalysisPipeline
    from mercury_ai.data.market_data import MarketDataService
    from mercury_ai.models.analysis_result import AnalysisResult
    from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

    executor = PipelineExecutor()
    provider = MercuryDataProvider()
    pipeline = AnalysisPipeline(
        market_service=MarketDataService(provider=provider),
        providers=[provider],
    )

    start = time.perf_counter()
    executor.execute(
        "AnalysisPipeline.analyze",
        pipeline.analyze,
        AnalysisResult,
        symbol=symbol,
    )
    total_time = time.perf_counter() - start
    print(f"\nTotal pipeline execution time: {total_time:.4f} seconds")
    return total_time


def load_historical_metrics() -> dict:
    """Carrega, por ``engine_name``, os tempos dos ``runtime_report_*.json`` da raiz.

    Formato real dos relatórios (RuntimeReport.to_dict):
        ``{"symbol": str, "stages": [{"engine_name": str, "execution_time": float, ...}]}``

    Retorna ``{engine_name: [execution_time, ...]}``. Relatórios ilegíveis
    (OSError/JSONDecodeError) são ignorados sem interromper a leitura.
    """
    metrics: dict = {}
    reports_dir = Path(__file__).resolve().parent  # raiz do projeto
    for report_file in sorted(reports_dir.glob("runtime_report_*.json")):
        try:
            with open(report_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        for stage in data.get("stages", []):
            engine = stage.get("engine_name")
            exec_time = stage.get("execution_time")
            if engine and isinstance(exec_time, (int, float)):
                metrics.setdefault(engine, []).append(exec_time)
    return metrics


def check_regression(current_metrics: dict, threshold: float = 0.1) -> bool:
    """Compara métricas atuais contra o baseline histórico.

    Regressão quando ``current_time > historical_avg * (1 + threshold)``.
    Sem baseline disponível -> não é possível verificar (retorna False, com
    aviso explícito — não trata "sem baseline" como aprovação silenciosa).
    Em regressão -> levanta ``PerformanceRegressionError`` (contrato canônico).
    Retorna True quando verificou e nenhuma métrica regrediu.
    """
    historical = load_historical_metrics()
    if not historical:
        print("No historical data found - cannot check regression")
        return False

    regressions = []
    for stage, current_time in current_metrics.items():
        if not isinstance(current_time, (int, float)):
            continue
        historical_times = historical.get(stage, [])
        if not historical_times:
            continue
        historical_avg = mean(historical_times)
        if current_time > historical_avg * (1 + threshold):
            regressions.append(
                f"{stage}: {current_time:.4f}s vs avg {historical_avg:.4f}s"
            )

    if regressions:
        raise PerformanceRegressionError(
            "Threshold exceeded: " + "; ".join(regressions)
        )
    print("All performance metrics within acceptable thresholds")
    return True


def _load_latest_metrics() -> dict:
    """Métricas do relatório mais recente, como ``{engine_name: execution_time}``."""
    reports_dir = Path(__file__).resolve().parent
    reports = sorted(reports_dir.glob("runtime_report_*.json"))
    if not reports:
        return {}
    try:
        with open(reports[-1], "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    current = {}
    for stage in data.get("stages", []):
        engine = stage.get("engine_name")
        exec_time = stage.get("execution_time")
        if engine and isinstance(exec_time, (int, float)):
            current[engine] = exec_time
    return current


if __name__ == "__main__":
    try:
        benchmark_pipeline()
        current_metrics = _load_latest_metrics()
        if current_metrics:
            check_regression(current_metrics)
        else:
            print("No current metrics produced by benchmark")
        sys.exit(0)
    except PerformanceRegressionError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)
