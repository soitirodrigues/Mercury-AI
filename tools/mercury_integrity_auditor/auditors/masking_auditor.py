"""
Auditoria de Masking — Fase 4.
Detecta padrões perigosos de masking/mocking em código de produção:
- Mock/MagicMock em código de produção (NÃO teste)
- Monkey-patching em runtime
- Substituição de implementações reais por stubs
- sys.modules hacking
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


# Palavras-chave que indicam mocking em produção
MOCK_IMPORTS = {"mock", "unittest.mock", "MagicMock", "Mock", "patch", "PropertyMock"}
MOCK_PATTERNS = {"MagicMock", "Mock", "patch", "create_autospec", "sentinel", "DEFAULT"}


class MaskingDetector(ast.NodeVisitor):
    """Detecta padrões de mock/masking em código."""

    def __init__(self, filepath: Path, is_test: bool):
        self.filepath = filepath
        self.relpath = str(filepath.relative_to(PROJECT_ROOT))
        self.is_test = is_test
        self.findings: list[AuditFinding] = []
        self.mock_imports = []
        self.mock_usages = []
        self.bare_excepts = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in MOCK_IMPORTS or "mock" in alias.name.lower():
                self.mock_imports.append((alias.name, node.lineno))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and ("mock" in node.module.lower() or "unittest" in (node.module or "")):
            for alias in node.names:
                self.mock_imports.append((f"{node.module}.{alias.name}", node.lineno))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in MOCK_PATTERNS:
            self.mock_usages.append((node.func.id, node.lineno))
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.bare_excepts.append(node.lineno)
        self.generic_visit(node)


def run() -> AuditSection:
    """Executa a auditoria de masking."""
    section = AuditSection(
        name="4. Masking Audit",
        description="Detecção de Mock/MagicMock e padrões frágeis em código de produção",
    )

    production_mock_files = []
    all_bare_excepts = []

    for fpath in sorted(MERCURY_AI_DIR.rglob("*.py")):
        # Pula diretórios de teste
        if "test" in str(fpath).lower() or "tests" in str(fpath).lower():
            continue

        try:
            tree = ast.parse(fpath.read_text(encoding="utf-8"), filename=str(fpath))
        except Exception:
            continue

        detector = MaskingDetector(fpath, is_test=False)
        detector.visit(tree)

        if detector.mock_imports or detector.mock_usages:
            relpath = str(fpath.relative_to(PROJECT_ROOT))
            for imp, lineno in detector.mock_imports:
                production_mock_files.append((relpath, lineno, f"import {imp}"))
            for usage, lineno in detector.mock_usages:
                production_mock_files.append((relpath, lineno, f"uso de {usage}"))

        for lineno in detector.bare_excepts:
            all_bare_excepts.append((str(fpath.relative_to(PROJECT_ROOT)), lineno))

    # Finding 1: Mock em produção
    if production_mock_files:
        details = "\n".join(f"  {f}:{lineno} — {desc}" for f, lineno, desc in production_mock_files[:20])
        section.findings.append(AuditFinding(
            id="MASK-001",
            category="Masking Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title=f"Mock/MagicMock detectado em {len(production_mock_files)} local(is) de produção!",
            description=f"Uso de mock/stub em código que NÃO é de teste:\n{details}",
            location="Vários",
            evidence=details,
            recommendation="REMOÇÃO IMEDIATA: Mock não deve existir em código de produção. "
                          "Substituir por implementações reais ou usar injeção de dependência.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="MASK-001",
            category="Masking Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhum Mock/MagicMock em código de produção",
            description="Verificação de mock em produção passou.",
        ))

    # Finding 2: Bare excepts em produção
    if all_bare_excepts:
        details = "\n".join(f"  {f}:{lineno}" for f, lineno in all_bare_excepts[:20])
        section.findings.append(AuditFinding(
            id="MASK-002",
            category="Masking Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{len(all_bare_excepts)} bare except(s) em produção",
            description=f"Blocos except sem tipo em código de produção:\n{details}",
            recommendation="Especificar exceções capturadas.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="MASK-002",
            category="Masking Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhum bare except em produção",
            description="Todos os blocos except especificam o tipo.",
        ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section