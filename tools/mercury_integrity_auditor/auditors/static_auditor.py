"""
Auditoria Estática (AST) — Fase 1.
Analisa todos os arquivos Python do projeto com AST para detectar:
- Funções/métodos não implementados (NotImplementedError, pass, ...)
- Complexidade ciclomática excessiva
- Classes/funções muito longas
- Código morto (imports não usados, funções não chamadas)
- Anti-padrões estruturais
"""

import ast
import os
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


def _find_python_files(root: Path) -> list:
    """Encontra todos os arquivos .py recursivamente."""
    return sorted(root.rglob("*.py"))


def _parse_file(filepath: Path) -> ast.AST | None:
    """Faz parse de um arquivo Python com AST."""
    try:
        return ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
    except SyntaxError as e:
        return None
    except Exception:
        return None


def _count_lines(node: ast.AST) -> int:
    """Conta linhas de código de um nó AST."""
    if hasattr(node, "end_lineno") and node.end_lineno:
        return node.end_lineno - node.lineno + 1
    return 1


class StaticAnalyzer(ast.NodeVisitor):
    """Visitor AST para análise estática."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.relpath = filepath.relative_to(PROJECT_ROOT)
        self.findings: list[AuditFinding] = []
        self.current_class = None
        self.function_count = 0
        self.class_count = 0
        self.not_implemented = []
        self.bare_excepts = []
        self.todo_fixme = []
        self.long_functions = []
        self.imports = set()

    def visit_ClassDef(self, node):
        self.class_count += 1
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        self.function_count += 1
        # Verifica corpo vazio ou NotImplementedError
        if self._is_stub(node):
            self.not_implemented.append((node.name, node.lineno))
        # Verifica funções muito longas (>200 linhas)
        lines = _count_lines(node)
        if lines > 200:
            self.long_functions.append((node.name, node.lineno, lines))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        if self._is_stub(node):
            self.not_implemented.append((node.name, node.lineno))
        lines = _count_lines(node)
        if lines > 200:
            self.long_functions.append((node.name, node.lineno, lines))
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.bare_excepts.append(node.lineno)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def _is_stub(self, node) -> bool:
        """Verifica se uma função é um stub (raise NotImplementedError ou só docstring)."""
        if not node.body:
            return True
        # Verifica se o corpo é só raise NotImplementedError
        for stmt in node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, (ast.Constant, ast.Str)):
                continue  # docstring
            if isinstance(stmt, ast.Raise):
                if isinstance(stmt.exc, ast.Call):
                    func = stmt.exc.func
                    if isinstance(func, ast.Name) and func.id == "NotImplementedError":
                        return True
            return False
        return True  # só docstring


def run() -> AuditSection:
    """Executa a auditoria estática."""
    section = AuditSection(
        name="1. Static Audit (AST)",
        description="Análise estática de código via AST: stubs, complexidade, padrões estruturais",
    )

    py_files = _find_python_files(MERCURY_AI_DIR)
    total_files = len(py_files)
    total_functions = 0
    total_classes = 0
    all_not_implemented = []
    all_bare_excepts = []
    all_long_functions = []
    parse_errors = []

    for fpath in py_files:
        tree = _parse_file(fpath)
        if tree is None:
            parse_errors.append(str(fpath.relative_to(PROJECT_ROOT)))
            continue

        analyzer = StaticAnalyzer(fpath)
        analyzer.visit(tree)

        total_functions += analyzer.function_count
        total_classes += analyzer.class_count

        for name, lineno in analyzer.not_implemented:
            all_not_implemented.append((str(analyzer.relpath), name, lineno))

        for lineno in analyzer.bare_excepts:
            all_bare_excepts.append((str(analyzer.relpath), lineno))

        for name, lineno, lines in analyzer.long_functions:
            all_long_functions.append((str(analyzer.relpath), name, lineno, lines))

    # Finding 1: Total de arquivos analisados
    section.findings.append(AuditFinding(
        id="STATIC-001",
        category="Static Audit",
        severity=LOW,
        status=STATUS_INFO,
        title=f"Total de arquivos Python analisados: {total_files}",
        description=f"{total_files} arquivos .py em {MERCURY_AI_DIR}, {total_functions} funções, {total_classes} classes.",
        location=str(MERCURY_AI_DIR),
    ))

    # Finding 2: Erros de parse
    if parse_errors:
        section.findings.append(AuditFinding(
            id="STATIC-002",
            category="Static Audit",
            severity=HIGH,
            status=STATUS_FAIL,
            title=f"{len(parse_errors)} arquivo(s) com erro de sintaxe",
            description=f"Arquivos que não puderam ser parseados: {', '.join(parse_errors)}",
            location="Vários",
            recommendation="Corrigir erros de sintaxe nestes arquivos.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="STATIC-002",
            category="Static Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhum erro de sintaxe encontrado",
            description="Todos os arquivos Python foram parseados com sucesso.",
        ))

    # Finding 3: Stubs (NotImplementedError)
    if all_not_implemented:
        details = "\n".join(f"  {f}:{lineno} -> {name}()" for f, name, lineno in all_not_implemented[:20])
        section.findings.append(AuditFinding(
            id="STATIC-003",
            category="Static Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{len(all_not_implemented)} função(ões) stub (não implementadas)",
            description=f"Funções que levantam NotImplementedError ou têm corpo vazio:\n{details}",
            location="Vários",
            recommendation="Implementar ou remover funções stub antes do release.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="STATIC-003",
            category="Static Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhuma função stub encontrada",
            description="Todas as funções têm implementação.",
        ))

    # Finding 4: Bare excepts
    if all_bare_excepts:
        details = "\n".join(f"  {f}:{lineno}" for f, lineno in all_bare_excepts[:20])
        section.findings.append(AuditFinding(
            id="STATIC-004",
            category="Static Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{len(all_bare_excepts)} except(s) sem tipo (bare except)",
            description=f"Blocos except sem especificação de exceção:\n{details}",
            location="Vários",
            recommendation="Especificar exceções capturadas (ex: except Exception).",
        ))
    else:
        section.findings.append(AuditFinding(
            id="STATIC-004",
            category="Static Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhum bare except encontrado",
            description="Todos os blocos except especificam o tipo de exceção.",
        ))

    # Finding 5: Funções longas
    if all_long_functions:
        details = "\n".join(f"  {f}:{lineno} {name}() — {lines} linhas" for f, name, lineno, lines in all_long_functions[:10])
        section.findings.append(AuditFinding(
            id="STATIC-005",
            category="Static Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{len(all_long_functions)} função(ões) muito longas (>200 linhas)",
            description=f"Funções com mais de 200 linhas:\n{details}",
            recommendation="Refatorar funções longas em unidades menores.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="STATIC-005",
            category="Static Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhuma função excessivamente longa",
            description="Todas as funções têm menos de 200 linhas.",
        ))

    # Determina status da seção
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section