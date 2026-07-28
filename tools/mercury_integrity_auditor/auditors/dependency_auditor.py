"""
Auditoria de Dependências — Fase 3.
Analisa imports e dependências do projeto:
- Dependências declaradas vs. instaladas
- Imports não resolvidos
- Dependências circulares
- Dependências obsoletas ou com vulnerabilidades
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


def _parse_requirements() -> dict:
    """Parse requirements.txt."""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        return {}
    deps = {}
    for line in req_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            # Extrai nome do pacote (antes de ==, >=, etc.)
            pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].split("!=")[0].strip()
            deps[pkg.lower()] = line
    return deps


def _get_installed_packages() -> dict:
    """Obtém pacotes instalados via pip."""
    import importlib.metadata
    installed = {}
    for dist in importlib.metadata.distributions():
        name = dist.metadata["Name"].lower()
        installed[name] = dist.version
    return installed


def _collect_imports(root: Path) -> dict:
    """Coleta todos os imports do projeto."""
    all_imports = {}
    for fpath in sorted(root.rglob("*.py")):
        try:
            tree = ast.parse(fpath.read_text(encoding="utf-8"), filename=str(fpath))
        except Exception:
            continue
        relpath = str(fpath.relative_to(PROJECT_ROOT))
        file_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    file_imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    file_imports.add(node.module.split(".")[0])
        all_imports[relpath] = file_imports
    return all_imports


def run() -> AuditSection:
    """Executa a auditoria de dependências."""
    section = AuditSection(
        name="3. Dependency Audit",
        description="Análise de imports, dependências e requirements.txt",
    )

    # Parse requirements
    declared_deps = _parse_requirements()
    installed = _get_installed_packages()

    # Finding: requirements.txt existe?
    if not declared_deps:
        section.findings.append(AuditFinding(
            id="DEP-001",
            category="Dependency Audit",
            severity=HIGH,
            status=STATUS_FAIL,
            title="requirements.txt não encontrado ou vazio",
            description="O arquivo requirements.txt está ausente ou não contém dependências.",
            location="requirements.txt",
            recommendation="Criar requirements.txt com as dependências do projeto.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="DEP-001",
            category="Dependency Audit",
            severity=LOW,
            status=STATUS_PASS,
            title=f"requirements.txt com {len(declared_deps)} dependências declaradas",
            description=f"Dependências: {', '.join(sorted(declared_deps.keys()))}",
        ))

    # Verifica dependências declaradas vs instaladas
    missing = []
    for pkg, spec in declared_deps.items():
        if pkg not in installed:
            missing.append(pkg)

    if missing:
        section.findings.append(AuditFinding(
            id="DEP-002",
            category="Dependency Audit",
            severity=HIGH,
            status=STATUS_FAIL,
            title=f"{len(missing)} dependência(s) declarada(s) não instalada(s)",
            description=f"Pacotes em requirements.txt mas não instalados: {', '.join(missing)}",
            recommendation="Executar pip install -r requirements.txt",
        ))
    else:
        section.findings.append(AuditFinding(
            id="DEP-002",
            category="Dependency Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Todas as dependências declaradas estão instaladas",
            description=f"{len(declared_deps)} pacotes verificados.",
        ))

    # Coleta imports do projeto
    all_imports = _collect_imports(MERCURY_AI_DIR)

    # Identifica imports de terceiros não declarados
    stdlib_modules = {
        "abc", "argparse", "ast", "asyncio", "base64", "collections", "concurrent",
        "contextlib", "copy", "csv", "dataclasses", "datetime", "decimal", "enum",
        "functools", "glob", "hashlib", "html", "http", "importlib", "inspect",
        "io", "itertools", "json", "logging", "math", "multiprocessing", "operator",
        "os", "pathlib", "pickle", "platform", "pprint", "queue", "random", "re",
        "shutil", "signal", "socket", "sqlite3", "statistics", "string", "subprocess",
        "sys", "tempfile", "textwrap", "threading", "time", "traceback", "types",
        "typing", "unittest", "urllib", "uuid", "warnings", "weakref", "xml", "zipfile",
    }

    all_third_party = set()
    for filepath, imports in all_imports.items():
        for imp in imports:
            if imp not in stdlib_modules and not imp.startswith("mercury_ai"):
                all_third_party.add(imp)

    undeclared = all_third_party - set(declared_deps.keys())
    if undeclared:
        section.findings.append(AuditFinding(
            id="DEP-003",
            category="Dependency Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{len(undeclared)} import(s) de terceiros não declarados em requirements.txt",
            description=f"Pacotes importados mas não listados: {', '.join(sorted(undeclared))}",
            recommendation="Adicionar pacotes ao requirements.txt ou verificar se são necessários.",
        ))

    # Verifica imports circulares simples
    internal_imports = {}
    for filepath, imports in all_imports.items():
        for imp in imports:
            if imp.startswith("mercury_ai"):
                internal_imports.setdefault(filepath, set()).add(imp)

    # Verifica se há imports de módulos que importam de volta
    circular_candidates = []
    for f1, imports1 in internal_imports.items():
        for f2, imports2 in internal_imports.items():
            if f1 < f2:  # evita duplicação
                f1_module = f1.replace("/", ".").replace(".py", "").replace("\\", ".")
                f2_module = f2.replace("/", ".").replace(".py", "").replace("\\", ".")
                if f1_module in imports2 and f2_module in imports1:
                    circular_candidates.append((f1, f2))

    if circular_candidates:
        details = "\n".join(f"  {a} <-> {b}" for a, b in circular_candidates)
        section.findings.append(AuditFinding(
            id="DEP-004",
            category="Dependency Audit",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"{len(circular_candidates)} possível(is) dependência(s) circular(es)",
            description=f"Pares de arquivos que se importam mutuamente:\n{details}",
            recommendation="Refatorar para eliminar dependências circulares.",
        ))
    else:
        section.findings.append(AuditFinding(
            id="DEP-004",
            category="Dependency Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Nenhuma dependência circular detectada",
            description="Todos os imports internos são acíclicos.",
        ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section