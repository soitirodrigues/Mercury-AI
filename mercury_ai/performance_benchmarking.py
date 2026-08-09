"""Performance benchmarking — verificação de regressão de runtime.

Este módulo verifica se as métricas de execução atuais regrediram em relação
a um baseline histórico. A regra e o local do baseline reproduzem EXATAMENTE
o contrato já existente no projeto (mercury_ai/analysis/check_regression.py e
check_regression.py na raiz):

    - threshold default = 0.1 (10%)
    - regressão se  current_time > historical_avg * (1 + threshold)
    - baseline em runtime_reports/ (arquivos JSON flat {estágio: tempo})
    - sem baseline disponível → não é possível verificar → sai sem erro

O corpo original desta função foi perdido (arquivo contém '# ... existing code ...'
e a versão intacta não existe no histórico git). A reconstrução abaixo preserva
a API pública original (BenchmarkError, check_regression, __main__ com exit 0/1)
e a mensagem de erro original ('Threshold exceeded: {details}').
"""
import sys
import glob
import json
import os
from statistics import mean


class BenchmarkError(Exception):
    pass


def _load_historical_metrics():
    """Carrega métricas de runtime por estágio (formato flat {estágio: tempo})."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(repo_root, "runtime_reports")
    metrics = []
    for path in sorted(glob.glob(os.path.join(reports_dir, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            metrics.append(data)
    return metrics


def check_regression(threshold=0.1):
    """Compara métricas atuais contra o baseline histórico; levanta BenchmarkError se regredir.

    Mesma regra dos módulos check_regression.py do projeto:
        regressão se current_time > historical_avg * (1 + threshold).
    Sem baseline histórico disponível, não é possível verificar — encerra sem erro
    (mesmo comportamento do performance_benchmarking.py da raiz).
    """
    reports = _load_historical_metrics()
    if not reports:
        print("No historical data found - cannot check regression")
        return

    current = reports[-1]
    historical = reports[:-1]

    threshold_exceeded = False
    details = []
    for stage, current_time in current.items():
        historical_times = [
            r[stage] for r in historical if stage in r
            and isinstance(r[stage], (int, float))
        ]
        if not historical_times:
            continue
        historical_avg = mean(historical_times)
        if current_time > historical_avg * (1 + threshold):
            threshold_exceeded = True
            details.append(
                f"{stage}: {current_time:.2f}s vs avg {historical_avg:.2f}s"
            )

    if threshold_exceeded:
        raise BenchmarkError(f"Threshold exceeded: {details}")
    print("All performance metrics within acceptable thresholds")


if __name__ == "__main__":
    try:
        check_regression()
        sys.exit(0)
    except BenchmarkError as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)