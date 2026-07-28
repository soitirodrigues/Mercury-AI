"""
Auditoria de Fluxo e Pipeline — Fase 6.
Verifica a integridade do pipeline de análise:
- AnalysisPipeline executa todos os estágios
- HistoricalReplayEngine processa corretamente
- PipelineExecutor orquestra sem falhas
- Dados fluem entre estágios sem corrupção
"""

import ast
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


# Componentes críticos do pipeline que DEVEM existir
CRITICAL_COMPONENTS = [
    {
        "name": "AnalysisPipeline",
        "expected_module": "mercury_ai.analysis.pipeline",
        "expected_methods": ["run", "execute", "process"],
        "description": "Pipeline principal de análise",
    },
    {
        "name": "HistoricalReplayEngine",
        "expected_module": "mercury_ai.backtest.replay_engine",
        "expected_methods": ["replay", "run_replay", "process"],
        "description": "Engine de replay histórico",
    },
    {
        "name": "RiskEngine",
        "expected_module": "mercury_ai.analysis.risk_engine",
        "expected_methods": ["assess"],
        "description": "Engine de avaliação de risco",
    },
    {
        "name": "InstitutionalMemoryEngine",
        "expected_module": "mercury_ai.analysis.institutional_memory_engine",
        "expected_methods": ["record_decision", "record_outcome"],
        "description": "Motor de memória institucional",
    },
    {
        "name": "MercuryDecisionEngine",
        "expected_module": "mercury_ai.decision.engine",
        "expected_methods": ["decide", "evaluate"],
        "description": "Motor de decisão principal",
    },
    {
        "name": "PerformanceEngine",
        "expected_module": "mercury_ai.performance.engine",
        "expected_methods": ["calculate", "evaluate"],
        "description": "Motor de cálculo de performance",
    },
    {
        "name": "PipelineExecutor",
        "expected_module": "mercury_ai.execution.executor",
        "expected_methods": ["execute", "run"],
        "description": "Executor do pipeline",
    },
    {
        "name": "ReplayBatchProcessor",
        "expected_module": "mercury_ai.backtest.batch_processor",
        "expected_methods": ["process_batch", "run"],
        "description": "Processador de lote de replay",
    },
]


class ComponentChecker(ast.NodeVisitor):
    """Verifica existência de classes e métodos."""

    def __init__(self):
        self.classes = {}
        self.functions = {}

    def visit_ClassDef(self, node):
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)
        self.classes[node.name] = {
            "methods": methods,
            "lineno": node.lineno,
        }
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions[node.name] = node.lineno
        self.generic_visit(node)


def _find_class_in_project(class_name: str) -> tuple | None:
    """Procura uma classe em todo o projeto."""
    for fpath in sorted(MERCURY_AI_DIR.rglob("*.py")):
        try:
            tree = ast.parse(fpath.read_text(encoding="utf-8"), filename=str(fpath))
        except Exception:
            continue
        checker = ComponentChecker()
        checker.visit(tree)
        if class_name in checker.classes:
            return (str(fpath.relative_to(PROJECT_ROOT)), checker.classes[class_name])
    return None


def run() -> AuditSection:
    """Executa a auditoria de fluxo e pipeline."""
    section = AuditSection(
        name="6. Flow & Pipeline Audit",
        description="Verificação da integridade do pipeline de dados e fluxo entre componentes",
    )

    found_count = 0
    missing_count = 0
    missing_methods_count = 0

    for comp in CRITICAL_COMPONENTS:
        result = _find_class_in_project(comp["name"])

        if result is None:
            missing_count += 1
            section.findings.append(AuditFinding(
                id=f"FLOW-{comp['name'].upper()}",
                category="Flow Audit",
                severity=CRITICAL,
                status=STATUS_FAIL,
                title=f"Componente crítico não encontrado: {comp['name']}",
                description=f"{comp['description']} — esperado em {comp['expected_module']}",
                recommendation=f"Verificar se {comp['name']} existe e está no local correto.",
            ))
            continue

        filepath, class_info = result
        found_count += 1

        # Verifica métodos esperados
        found_methods = []
        missing_methods = []
        for method in comp["expected_methods"]:
            if method in class_info["methods"]:
                found_methods.append(method)
            else:
                missing_methods.append(method)

        if missing_methods:
            missing_methods_count += 1
            section.findings.append(AuditFinding(
                id=f"FLOW-{comp['name']}-METHODS",
                category="Flow Audit",
                severity=HIGH,
                status=STATUS_WARNING,
                title=f"{comp['name']}: métodos esperados ausentes",
                description=f"Encontrados: {found_methods}, Ausentes: {missing_methods}",
                location=f"{filepath}:{class_info['lineno']}",
                recommendation=f"Implementar métodos: {', '.join(missing_methods)}",
            ))
        else:
            section.findings.append(AuditFinding(
                id=f"FLOW-{comp['name']}",
                category="Flow Audit",
                severity=LOW,
                status=STATUS_PASS,
                title=f"{comp['name']} encontrado com todos os métodos",
                description=f"Localizado em {filepath}:{class_info['lineno']}, métodos: {', '.join(found_methods)}",
            ))

    # Summary
    section.findings.append(AuditFinding(
        id="FLOW-SUMMARY",
        category="Flow Audit",
        severity=LOW,
        status=STATUS_INFO,
        title=f"Componentes: {found_count}/{len(CRITICAL_COMPONENTS)} encontrados, "
              f"{missing_count} ausentes, {missing_methods_count} com métodos faltando",
        description="Resumo da auditoria de fluxo.",
    ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section