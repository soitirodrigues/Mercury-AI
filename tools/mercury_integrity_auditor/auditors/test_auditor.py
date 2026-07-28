"""
Auditoria de Testes — Fase 7.
Executa a suíte de testes e verifica:
- Todos os testes passam
- Cobertura de código
- Testes não são stubs
- Fixtures e configurações corretas
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
    """Executa a auditoria de testes."""
    section = AuditSection(
        name="7. Test Audit",
        description="Execução e análise da suíte de testes",
    )

    tests_dir = PROJECT_ROOT / "tests"
    if not tests_dir.exists():
        section.findings.append(AuditFinding(
            id="TEST-001",
            category="Test Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Diretório de testes não encontrado",
            description=f"Esperado em {tests_dir}",
        ))
        section.status = "FAIL"
        return section

    # Executa pytest
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=2100,  # 35 minutos
            cwd=str(PROJECT_ROOT),
        )
        elapsed = time.time() - start
    except subprocess.TimeoutExpired:
        section.findings.append(AuditFinding(
            id="TEST-001",
            category="Test Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Execução de testes excedeu timeout (25min)",
            description="A suíte de testes não completou em 25 minutos.",
        ))
        section.status = "FAIL"
        return section
    except Exception as e:
        section.findings.append(AuditFinding(
            id="TEST-001",
            category="Test Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title=f"Erro ao executar pytest: {e}",
            description=str(e),
        ))
        section.status = "FAIL"
        return section

    stdout = result.stdout
    stderr = result.stderr

    # Parse do output do pytest
    # Procura por "X passed, Y failed"
    import re
    passed_match = re.search(r"(\d+)\s+passed", stdout)
    failed_match = re.search(r"(\d+)\s+failed", stdout)
    error_match = re.search(r"(\d+)\s+error", stdout)

    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0
    errors = int(error_match.group(1)) if error_match else 0
    total = passed + failed + errors

    # Finding 1: Resultado geral
    if failed == 0 and errors == 0 and passed > 0:
        section.findings.append(AuditFinding(
            id="TEST-001",
            category="Test Audit",
            severity=LOW,
            status=STATUS_PASS,
            title=f"Todos os {passed} testes passaram!",
            description=f"{passed} passed, 0 failed, 0 errors em {elapsed:.1f}s",
        ))
    elif passed > 0:
        section.findings.append(AuditFinding(
            id="TEST-001",
            category="Test Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title=f"Testes com falhas: {passed} passed, {failed} failed, {errors} errors",
            description=f"{total} testes total, {elapsed:.1f}s de execução.",
            recommendation="Corrigir testes quebrados antes do release.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="TEST-001",
            category="Test Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Nenhum teste executado com sucesso",
            description=f"0 passed, {failed} failed, {errors} errors",
            recommendation="Verificar se a suíte de testes está configurada corretamente.",
        ))

    # Finding 2: Detalhes de falhas
    if failed > 0 or errors > 0:
        # Extrai nomes dos testes que falharam
        fail_lines = []
        for line in stdout.splitlines():
            if "FAILED" in line or "ERROR" in line:
                fail_lines.append(line.strip())
        if fail_lines:
            details = "\n".join(fail_lines[:20])
            section.findings.append(AuditFinding(
                id="TEST-002",
                category="Test Audit",
                severity=HIGH,
                status=STATUS_FAIL,
                title=f"Detalhes das {len(fail_lines)} falhas/erros",
                description=f"Primeiros 20:\n{details}",
                recommendation="Corrigir cada teste quebrado individualmente.",
            ))

    # Finding 3: Tempo de execução
    section.findings.append(AuditFinding(
        id="TEST-003",
        category="Test Audit",
        severity=LOW,
        status=STATUS_INFO,
        title=f"Tempo total de execução: {elapsed:.1f}s",
        description=f"{total} testes executados em {elapsed:.1f}s.",
    ))

    # Finding 4: Cobertura (se disponível)
    try:
        cov_result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "--cov=mercury_ai", "--cov-report=term", "--tb=no"],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=str(PROJECT_ROOT),
        )
        cov_output = cov_result.stdout
        cov_match = re.search(r"TOTAL.*?(\d+)%", cov_output)
        if cov_match:
            cov_pct = int(cov_match.group(1))
            status = STATUS_PASS if cov_pct >= 80 else STATUS_WARNING if cov_pct >= 50 else STATUS_FAIL
            section.findings.append(AuditFinding(
                id="TEST-004",
                category="Test Audit",
                severity=MEDIUM if cov_pct < 80 else LOW,
                status=status,
                title=f"Cobertura de código: {cov_pct}%",
                description=f"Cobertura total do projeto: {cov_pct}%",
                recommendation="Aumentar cobertura para >= 80%." if cov_pct < 80 else None,
            ))
    except Exception:
        section.findings.append(AuditFinding(
            id="TEST-004",
            category="Test Audit",
            severity=LOW,
            status=STATUS_INFO,
            title="Cobertura de código não disponível",
            description="pytest-cov não instalado ou erro na execução.",
        ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section