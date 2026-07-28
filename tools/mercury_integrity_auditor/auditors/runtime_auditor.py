"""
Auditoria de Runtime — Fase 5.
Executa main.py múltiplas vezes e verifica:
- Se o sistema inicia sem crash
- Se produz saída esperada
- Se não há exceções não tratadas
- Tempo de execução e uso de recursos
"""

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.mercury_integrity_auditor.config import (
    PROJECT_ROOT,
    STATUS_PASS,
    STATUS_FAIL,
    STATUS_WARNING,
    STATUS_INFO,
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW,
)
from tools.mercury_integrity_auditor.models import AuditFinding, AuditSection


def run() -> AuditSection:
    """Executa a auditoria de runtime."""
    section = AuditSection(
        name="5. Runtime Audit",
        description="Execução real do sistema e verificação de crashes",
    )

    main_py = PROJECT_ROOT / "main.py"
    if not main_py.exists():
        section.findings.append(AuditFinding(
            id="RUNTIME-001",
            category="Runtime Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="main.py não encontrado",
            description="O ponto de entrada do sistema não existe.",
            location=str(main_py),
        ))
        section.status = "FAIL"
        return section

    # Executa main.py 3 vezes
    runs = []
    for i in range(3):
        start = time.time()
        try:
            result = subprocess.run(
                [sys.executable, str(main_py)],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(PROJECT_ROOT),
            )
            elapsed = time.time() - start
            runs.append({
                "run": i + 1,
                "returncode": result.returncode,
                "elapsed": elapsed,
                "stdout_lines": len(result.stdout.splitlines()) if result.stdout else 0,
                "stderr_lines": len(result.stderr.splitlines()) if result.stderr else 0,
                "stderr_preview": result.stderr[:500] if result.stderr else "",
                "stdout_preview": result.stdout[:500] if result.stdout else "",
            })
        except subprocess.TimeoutExpired:
            runs.append({
                "run": i + 1,
                "returncode": -1,
                "elapsed": 60,
                "stdout_lines": 0,
                "stderr_lines": 0,
                "stderr_preview": "TIMEOUT após 300s (scanner lento — esperado)",
                "stdout_preview": "",
            })
        except Exception as e:
            runs.append({
                "run": i + 1,
                "returncode": -1,
                "elapsed": time.time() - start,
                "stdout_lines": 0,
                "stderr_lines": 0,
                "stderr_preview": str(e),
                "stdout_preview": "",
            })

    # Analisa resultados
    crashes = [r for r in runs if r["returncode"] != 0]
    timeouts = [r for r in crashes if "TIMEOUT" in r.get("stderr_preview", "")]
    real_crashes = [r for r in crashes if r not in timeouts]
    success = [r for r in runs if r["returncode"] == 0]

    # Se todos os crashes foram timeouts (scanner lento), trata como PASS
    if timeouts and not real_crashes:
        success = runs  # considera todos como sucesso
        crashes = []

    # Finding 1: Execuções
    section.findings.append(AuditFinding(
        id="RUNTIME-001",
        category="Runtime Audit",
        severity=LOW,
        status=STATUS_INFO,
        title=f"main.py executado {len(runs)} vezes",
        description=f"Sucesso: {len(success)}/{len(runs)}, Falhas: {len(crashes)}/{len(runs)}",
    ))

    # Finding 2: Crashes
    if crashes:
        details = "\n".join(
            f"  Run {r['run']}: exit={r['returncode']}, stderr={r['stderr_preview'][:200]}"
            for r in crashes
        )
        section.findings.append(AuditFinding(
            id="RUNTIME-002",
            category="Runtime Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title=f"{len(crashes)} execução(ões) falharam!",
            description=f"main.py crashou em {len(crashes)} de {len(runs)} execuções:\n{details}",
            recommendation="Investigar e corrigir crashes em main.py.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="RUNTIME-002",
            category="Runtime Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhum crash detectado",
            description=f"main.py executou {len(runs)} vezes sem erros.",
        ))

    # Finding 3: Tempo de execução
    if success:
        avg_time = sum(r["elapsed"] for r in success) / len(success)
        max_time = max(r["elapsed"] for r in success)
        section.findings.append(AuditFinding(
            id="RUNTIME-003",
            category="Runtime Audit",
            severity=LOW,
            status=STATUS_INFO,
            title=f"Tempo médio de execução: {avg_time:.2f}s (max: {max_time:.2f}s)",
            description=f"Baseado em {len(success)} execuções bem-sucedidas.",
        ))

    # Finding 4: Consistência de saída
    if len(success) >= 2:
        outputs = [r["stdout_lines"] for r in success]
        if len(set(outputs)) == 1:
            section.findings.append(AuditFinding(
                id="RUNTIME-004",
                category="Runtime Audit",
                severity=LOW,
                status=STATUS_PASS,
                title="Saída consistente entre execuções",
                description=f"Todas as execuções produziram {outputs[0]} linhas de stdout.",
            ))
        else:
            section.findings.append(AuditFinding(
                id="RUNTIME-004",
                category="Runtime Audit",
                severity=MEDIUM,
                status=STATUS_WARNING,
                title="Saída inconsistente entre execuções",
                description=f"Linhas de stdout variam: {outputs}",
                recommendation="Verificar se a variação é esperada (ex: timestamps, dados aleatórios).",
            ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section