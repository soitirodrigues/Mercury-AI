"""
Auditoria de Cobertura — Fase 9.
Verifica a cobertura de código e testes:
- Cobertura de testes unitários
- Cobertura de branches
- Arquivos não testados
- Métricas de qualidade de cobertura
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.mercury_integrity_auditor.config import (
    PROJECT_ROOT,
    MERCURY_AI_DIR,
    TESTS_DIR,
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


def _run_coverage() -> dict:
    """Executa pytest com cobertura e retorna os resultados."""
    try:
        # Tenta executar pytest com coverage
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--cov=mercury_ai", "--cov-report=json", "-q"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )
        
        # Tenta ler o arquivo de cobertura gerado
        coverage_file = PROJECT_ROOT / "coverage.json"
        if coverage_file.exists():
            with open(coverage_file, "r") as f:
                return json.load(f)
        
        # Se não houver arquivo, tenta parsear a saída
        return {"error": "coverage_file_not_found", "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}


def _analyze_coverage_data(coverage_data: dict) -> dict:
    """Analisa os dados de cobertura e retorna métricas."""
    if "error" in coverage_data:
        return {"error": coverage_data["error"]}
    
    files = coverage_data.get("files", {})
    total_lines = 0
    covered_lines = 0
    total_branches = 0
    covered_branches = 0
    uncovered_files = []
    
    for filepath, file_data in files.items():
        if "mercury_ai" not in filepath:
            continue
            
        summary = file_data.get("summary", {})
        total_lines += summary.get("num_statements", 0)
        covered_lines += summary.get("covered_lines", 0)
        total_branches += summary.get("num_branches", 0)
        covered_branches += summary.get("covered_branches", 0)
        
        # Arquivos com cobertura baixa
        if summary.get("num_statements", 0) > 0:
            coverage_pct = (summary.get("covered_lines", 0) / summary.get("num_statements", 1)) * 100
            if coverage_pct < 50:
                uncovered_files.append({
                    "file": filepath,
                    "coverage": coverage_pct,
                    "statements": summary.get("num_statements", 0),
                })
    
    line_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
    branch_coverage = (covered_branches / total_branches * 100) if total_branches > 0 else 0
    
    return {
        "total_lines": total_lines,
        "covered_lines": covered_lines,
        "line_coverage": line_coverage,
        "total_branches": total_branches,
        "covered_branches": covered_branches,
        "branch_coverage": branch_coverage,
        "uncovered_files": uncovered_files,
        "files_analyzed": len(files),
    }


def _find_untested_modules() -> list:
    """Encontra módulos do mercury_ai que não têm testes correspondentes."""
    untested = []
    
    # Coleta todos os módulos Python em mercury_ai
    mercury_modules = set()
    for fpath in MERCURY_AI_DIR.rglob("*.py"):
        if fpath.name == "__init__.py":
            continue
        rel_path = fpath.relative_to(MERCURY_AI_DIR)
        module_path = str(rel_path.with_suffix("")).replace("/", ".")
        mercury_modules.add(module_path)
    
    # Coleta módulos testados (baseado em imports nos testes)
    tested_modules = set()
    for fpath in TESTS_DIR.rglob("*.py"):
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        # Procura imports de mercury_ai
        for line in content.split("\n"):
            if "from mercury_ai" in line or "import mercury_ai" in line:
                # Extrai o módulo
                parts = line.replace("from ", "").replace("import ", "").split()
                if parts:
                    module = parts[0].split(".")[0] + "." + ".".join(parts[0].split(".")[1:])
                    tested_modules.add(module)
    
    # Módulos não testados
    for module in mercury_modules:
        if module not in tested_modules and not module.startswith("mercury_ai."):
            continue
        # Verifica se há algum teste que importe este módulo
        has_test = any(module.startswith(tested) or tested.startswith(module) for tested in tested_modules)
        if not has_test:
            untested.append(module)
    
    return untested


def run() -> AuditSection:
    """Executa a auditoria de cobertura."""
    section = AuditSection(
        name="9. Coverage Audit",
        description="Verificação da cobertura de código e testes",
    )
    
    # 1. Executa cobertura
    print("  Executando análise de cobertura...")
    coverage_data = _run_coverage()
    analysis = _analyze_coverage_data(coverage_data)
    
    if "error" in analysis:
        section.findings.append(AuditFinding(
            id="COV-001",
            category="Coverage Audit",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Falha ao obter dados de cobertura",
            description=f"Erro: {analysis['error']}. Cobertura não pôde ser medida.",
            recommendation="Verificar se pytest-cov está instalado e configurado.",
        ))
    else:
        # Finding 1: Cobertura de linhas
        line_cov = analysis["line_coverage"]
        if line_cov >= 80:
            status = STATUS_PASS
            severity = LOW
        elif line_cov >= 50:
            status = STATUS_WARNING
            severity = MEDIUM
        else:
            status = STATUS_FAIL
            severity = HIGH
            
        section.findings.append(AuditFinding(
            id="COV-001",
            category="Coverage Audit",
            severity=severity,
            status=status,
            title=f"Cobertura de linhas: {line_cov:.1f}%",
            description=f"Linhas cobertas: {analysis['covered_lines']}/{analysis['total_lines']} em {analysis['files_analyzed']} arquivos.",
            evidence=f"Branch coverage: {analysis['branch_coverage']:.1f}% ({analysis['covered_branches']}/{analysis['total_branches']})",
        ))
        
        # Finding 2: Cobertura de branches
        branch_cov = analysis["branch_coverage"]
        if branch_cov >= 70:
            status = STATUS_PASS
            severity = LOW
        elif branch_cov >= 40:
            status = STATUS_WARNING
            severity = MEDIUM
        else:
            status = STATUS_FAIL
            severity = HIGH
            
        section.findings.append(AuditFinding(
            id="COV-002",
            category="Coverage Audit",
            severity=severity,
            status=status,
            title=f"Cobertura de branches: {branch_cov:.1f}%",
            description=f"Branches cobertos: {analysis['covered_branches']}/{analysis['total_branches']}.",
        ))
        
        # Finding 3: Arquivos com cobertura baixa
        if analysis["uncovered_files"]:
            section.findings.append(AuditFinding(
                id="COV-003",
                category="Coverage Audit",
                severity=MEDIUM,
                status=STATUS_WARNING,
                title=f"{len(analysis['uncovered_files'])} arquivos com cobertura < 50%",
                description="Arquivos com baixa cobertura: " + ", ".join(
                    f"{f['file']} ({f['coverage']:.1f}%)" for f in analysis["uncovered_files"][:10]
                ),
                recommendation="Adicionar testes para os módulos com baixa cobertura.",
            ))
        else:
            section.findings.append(AuditFinding(
                id="COV-003",
                category="Coverage Audit",
                severity=LOW,
                status=STATUS_PASS,
                title="Todos os arquivos têm cobertura >= 50%",
                description="Nenhum arquivo com cobertura criticamente baixa.",
            ))
    
    # 2. Módulos não testados
    print("  Verificando módulos sem testes...")
    untested = _find_untested_modules()
    
    if untested:
        section.findings.append(AuditFinding(
            id="COV-004",
            category="Coverage Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{len(untested)} módulos sem testes diretos",
            description="Módulos que podem não ter testes: " + ", ".join(untested[:15]),
            recommendation="Criar testes unitários para módulos críticos sem cobertura.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="COV-004",
            category="Coverage Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Todos os módulos têm testes associados",
            description="Cada módulo do mercury_ai tem pelo menos um teste que o importa.",
        ))
    
    # Determina status da seção
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"
    
    return section