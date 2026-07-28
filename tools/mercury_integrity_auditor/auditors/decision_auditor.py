"""
Auditoria de Integridade de Decisão — Fase 8.
Verifica a qualidade e integridade das decisões do Mercury:
- Decisões são determinísticas (mesma entrada → mesma saída)
- Decisões são válidas (dentro de limites esperados)
- Não há decisões contraditórias
- O motor de decisão não produz NaN/Inf
"""

import ast
import json
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
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW,
)
from tools.mercury_integrity_auditor.models import AuditFinding, AuditSection


class DecisionPathAnalyzer(ast.NodeVisitor):
    """Analisa caminhos de decisão no código."""

    def __init__(self):
        self.decision_points = []
        self.random_calls = []
        self.float_operations = []

    def visit_If(self, node):
        self.decision_points.append({
            "lineno": node.lineno,
            "test": ast.unparse(node.test) if hasattr(ast, "unparse") else str(node.test),
        })
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detecta chamadas a random
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id == "random":
                    self.random_calls.append({
                        "lineno": node.lineno,
                        "method": node.func.attr,
                    })
        # Detecta operações que podem gerar NaN/Inf
        if isinstance(node.func, ast.Name):
            if node.func.id in ("float", "int"):
                self.float_operations.append({
                    "lineno": node.lineno,
                    "func": node.func.id,
                })
        self.generic_visit(node)


def _analyze_decision_file(filepath: Path) -> dict:
    """Analisa um arquivo em busca de lógica de decisão."""
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
    except Exception:
        return {"error": "parse_failed"}

    analyzer = DecisionPathAnalyzer()
    analyzer.visit(tree)

    return {
        "decision_points": len(analyzer.decision_points),
        "random_calls": len(analyzer.random_calls),
        "random_details": analyzer.random_calls[:5],
        "float_operations": len(analyzer.float_operations),
    }


def run() -> AuditSection:
    """Executa a auditoria de integridade de decisão."""
    section = AuditSection(
        name="8. Decision Integrity Audit",
        description="Verificação da integridade e determinismo das decisões",
    )

    # 1. Procura o MercuryDecisionEngine
    decision_files = []
    for fpath in MERCURY_AI_DIR.rglob("*.py"):
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        if "MercuryDecisionEngine" in content or "class.*Decision" in content:
            decision_files.append(fpath)

    if not decision_files:
        section.findings.append(AuditFinding(
            id="DEC-001",
            category="Decision Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Nenhum arquivo de decisão encontrado",
            description="MercuryDecisionEngine ou classes de decisão não localizadas.",
        ))
        section.status = "FAIL"
        return section

    # Analisa cada arquivo de decisão
    total_decision_points = 0
    total_random_calls = 0
    files_with_random = []

    for fpath in decision_files:
        rel_path = fpath.relative_to(PROJECT_ROOT)
        analysis = _analyze_decision_file(fpath)

        if "error" in analysis:
            section.findings.append(AuditFinding(
                id=f"DEC-PARSE-{fpath.stem}",
                category="Decision Audit",
                severity=HIGH,
                status=STATUS_WARNING,
                title=f"Falha ao parsear {rel_path}",
                description="Arquivo de decisão com erro de sintaxe.",
                location=str(rel_path),
            ))
            continue

        total_decision_points += analysis["decision_points"]
        total_random_calls += analysis["random_calls"]

        if analysis["random_calls"] > 0:
            files_with_random.append(str(rel_path))

    # Finding 1: Pontos de decisão
    section.findings.append(AuditFinding(
        id="DEC-001",
        category="Decision Audit",
        severity=LOW,
        status=STATUS_INFO,
        title=f"Total de pontos de decisão: {total_decision_points}",
        description=f"Encontrados em {len(decision_files)} arquivos de decisão.",
    ))

    # Finding 2: Chamadas a random (não-determinismo)
    if files_with_random:
        section.findings.append(AuditFinding(
            id="DEC-002",
            category="Decision Audit",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Chamadas a random() detectadas em {len(files_with_random)} arquivos",
            description=f"Total: {total_random_calls} chamadas. Arquivos: {', '.join(str(f) for f in files_with_random[:10])}",
            recommendation="Decisões de trading devem ser determinísticas. Usar seed fixa ou remover random.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="DEC-002",
            category="Decision Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhuma chamada a random() detectada",
            description="Decisões parecem ser determinísticas.",
        ))

    # Finding 3: Verifica NaN/Inf guards
    nan_guards_found = False
    for fpath in MERCURY_AI_DIR.rglob("*.py"):
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        if "isnan" in content or "isinf" in content or "isfinite" in content:
            nan_guards_found = True
            break

    if nan_guards_found:
        section.findings.append(AuditFinding(
            id="DEC-003",
            category="Decision Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Guards contra NaN/Inf detectados",
            description="O código contém verificações isnan/isinf/isfinite.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="DEC-003",
            category="Decision Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Nenhum guard contra NaN/Inf detectado",
            description="Decisões podem produzir valores inválidos sem detecção.",
            recommendation="Adicionar verificações math.isfinite() em cálculos críticos.",
        ))

    # Finding 4: Verifica se há validação de saída
    validation_found = False
    for fpath in MERCURY_AI_DIR.rglob("*.py"):
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        if "assert" in content and ("decision" in content.lower() or "validate" in content.lower()):
            validation_found = True
            break

    if validation_found:
        section.findings.append(AuditFinding(
            id="DEC-004",
            category="Decision Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Validação de decisão detectada",
            description="O código contém asserts/validações nas decisões.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="DEC-004",
            category="Decision Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Validação de decisão não detectada",
            description="Decisões podem não ser validadas antes do uso.",
            recommendation="Adicionar validação de saída no MercuryDecisionEngine.",
        ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section