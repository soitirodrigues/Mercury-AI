"""
Auditoria de Determinismo — Fase 15.
Verifica reprodutibilidade determinística:
- Seeds fixos (random, numpy, torch, etc.)
- Operações não-determinísticas (hash, dict iteration, set, threading)
- Timestamps / time-based logic
- Floating point non-determinism
- External dependencies (API, DB, filesystem)
- Replay / deterministic replay capability
"""

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


def _check_fixed_seeds() -> list[AuditFinding]:
    """Verifica uso de seeds fixos para reprodutibilidade."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    seed_usage = []
    random_imports = []
    numpy_random = []
    torch_random = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Detecta seeds
                if any(kw in stripped for kw in [
                    "random.seed", "np.random.seed", "numpy.random.seed",
                    "torch.manual_seed", "tf.random.set_seed", "seed("
                ]):
                    seed_usage.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                # Detecta imports de random
                if "import random" in stripped or "from random" in stripped:
                    random_imports.append(str(f.relative_to(PROJECT_ROOT)))
                if "np.random" in content or "numpy.random" in content:
                    numpy_random.append(str(f.relative_to(PROJECT_ROOT)))
                if "torch" in content and ("manual_seed" in content or "cuda.manual_seed" in content):
                    torch_random.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    has_explicit_seeds = len(seed_usage) > 0
    uses_random = len(random_imports) > 0
    uses_numpy_random = len(numpy_random) > 0
    uses_torch = len(torch_random) > 0
    
    if has_explicit_seeds:
        findings.append(AuditFinding(
            id="DET-001",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title=f"Fixed Seeds Found: {len(seed_usage)}",
            description=f"Seeds explícitos definidos: {seed_usage[:3]}",
            location=str(MERCURY_AI_DIR),
        ))
    elif uses_random or uses_numpy_random or uses_torch:
        findings.append(AuditFinding(
            id="DET-001",
            category="DETERMINISM",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Random Libraries Used Without Fixed Seeds",
            description=f"Usa random={uses_random}, numpy.random={uses_numpy_random}, torch={uses_torch} mas sem seeds fixos detectados.",
            location=str(MERCURY_AI_DIR),
            recommendation="Definir seeds fixos no entry point: random.seed(42), np.random.seed(42), torch.manual_seed(42).",
        ))
    else:
        findings.append(AuditFinding(
            id="DET-001",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_INFO,
            title="No Random Libraries Detected",
            description="Não detectado uso de bibliotecas de aleatoriedade.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_non_deterministic_ops() -> list[AuditFinding]:
    """Verifica operações não-determinísticas."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    non_det_ops = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Operações não-determinísticas conhecidas
                if any(kw in stripped for kw in [
                    "hash(", "id(", "set(", "frozenset(",
                    "threading.", "multiprocessing.", "asyncio.",
                    "time.time()", "time.perf_counter()", "datetime.now()",
                    "uuid.uuid4()", "os.urandom", "secrets.",
                    "dict(", "{", "}.items()", "}.keys()", "}.values()",
                ]):
                    # Filtra falsos positivos
                    if not any(skip in stripped for skip in ["#", '"', "'", "test_", "mock"]):
                        non_det_ops.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
        except Exception:
            pass
    
    # Agrupa por tipo
    hash_ops = [o for o in non_det_ops if "hash(" in o[2]]
    time_ops = [o for o in non_det_ops if any(kw in o[2] for kw in ["time.", "datetime.now"])]
    uuid_ops = [o for o in non_det_ops if "uuid" in o[2]]
    thread_ops = [o for o in non_det_ops if any(kw in o[2] for kw in ["threading", "multiprocessing", "asyncio"])]
    dict_iter_ops = [o for o in non_det_ops if any(kw in o[2] for kw in [".items()", ".keys()", ".values()"])]
    
    if hash_ops:
        findings.append(AuditFinding(
            id="DET-002",
            category="DETERMINISM",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Hash Operations: {len(hash_ops)}",
            description=f"Uso de hash() (não-determinístico entre runs Python): {hash_ops[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Evitar hash() para lógica de negócio. Usar hashlib com seed fixo ou IDs determinísticos.",
        ))
    
    if time_ops:
        findings.append(AuditFinding(
            id="DET-003",
            category="DETERMINISM",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Time-Based Operations: {len(time_ops)}",
            description=f"Operações baseadas em tempo (não-determinísticas): {time_ops[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Injetar tempo como dependência (time_provider) para testes determinísticos. Usar freezegun em testes.",
        ))
    
    if uuid_ops:
        findings.append(AuditFinding(
            id="DET-004",
            category="DETERMINISM",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"UUID Generation: {len(uuid_ops)}",
            description=f"Geração de UUID aleatórios: {uuid_ops[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Para testes: usar uuid determinístico (uuid5 com namespace fixo) ou mock.",
        ))
    
    if thread_ops:
        findings.append(AuditFinding(
            id="DET-005",
            category="DETERMINISM",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Concurrency Operations: {len(thread_ops)}",
            description=f"Operações de concorrência (ordem não-determinística): {thread_ops[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Evitar concorrência em lógica crítica. Se necessário, usar locks determinísticos ou single-threaded para replay.",
        ))
    
    if dict_iter_ops:
        findings.append(AuditFinding(
            id="DET-006",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_INFO,
            title=f"Dict Iteration Order: {len(dict_iter_ops)}",
            description=f"Iteração de dict (ordem garantida desde Python 3.7, mas não confiar para lógica crítica): {dict_iter_ops[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Ordem de dict é preservada em Python 3.7+, mas para determinismo estrito usar sorted() ou OrderedDict.",
        ))
    
    if not any([hash_ops, time_ops, uuid_ops, thread_ops, dict_iter_ops]):
        findings.append(AuditFinding(
            id="DET-002",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title="No Obvious Non-Deterministic Operations",
            description="Nenhuma operação obviamente não-determinística detectada.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_floating_point() -> list[AuditFinding]:
    """Verifica problemas de ponto flutuante."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    fp_issues = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Comparações de float diretas
                if "==" in stripped and any(kw in stripped for kw in ["float", "0.1", "0.2", "0.3", ".1", ".2", ".3"]):
                    if not stripped.startswith("#"):
                        fp_issues.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                # Uso de decimal para precisão
                if "from decimal import" in stripped or "import decimal" in stripped:
                    fp_issues.append((str(f.relative_to(PROJECT_ROOT)), i+1, "Decimal usage: " + stripped[:60]))
        except Exception:
            pass
    
    if fp_issues:
        findings.append(AuditFinding(
            id="DET-007",
            category="DETERMINISM",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Floating Point Comparisons: {len(fp_issues)}",
            description=f"Possíveis comparações de ponto flutuante: {fp_issues[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Usar math.isclose() ou decimal.Decimal para comparações financeiras. Evitar == com floats.",
        ))
    else:
        findings.append(AuditFinding(
            id="DET-007",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title="No Floating Point Comparison Issues Detected",
            description="Nenhuma comparação direta de floats detectada.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_external_dependencies() -> list[AuditFinding]:
    """Verifica dependências externas não-determinísticas."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    ext_deps = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            # APIs externas, DB, filesystem, network
            if any(kw in content for kw in [
                "requests.", "httpx.", "aiohttp.", "urllib.",
                "sqlite3", "psycopg", "sqlalchemy", "pymongo",
                "redis.", "kafka.", "pika.",
                "open(", "Path(", "os.path", "shutil.",
                "subprocess.", "os.system", "popen",
            ]):
                ext_deps.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if ext_deps:
        findings.append(AuditFinding(
            id="DET-008",
            category="DETERMINISM",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"External Dependencies: {len(set(ext_deps))} files",
            description=f"Dependências externas (API, DB, FS, network) em: {', '.join(set(list(ext_deps)[:5]))}",
            location=str(MERCURY_AI_DIR),
            recommendation="Isolar dependências externas atrás de interfaces. Usar mocks/fakes para testes determinísticos. Implementar replay de dados externos.",
        ))
    else:
        findings.append(AuditFinding(
            id="DET-008",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title="No External Dependencies Detected",
            description="Nenhuma dependência externa óbvia detectada no código core.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_deterministic_replay() -> list[AuditFinding]:
    """Verifica capacidade de replay determinístico."""
    findings = []
    
    replay_files = list(MERCURY_AI_DIR.rglob("*replay*.py"))
    replay_files += list(MERCURY_AI_DIR.rglob("*deterministic*.py"))
    replay_files += list(PROJECT_ROOT.rglob("*replay*.py"))
    replay_files += list(PROJECT_ROOT.rglob("*deterministic*.py"))
    
    # Verifica scripts de replay
    run_replay = PROJECT_ROOT / "run_deterministic_replay_scenarios.py"
    run_instrumented = PROJECT_ROOT / "run_instrumented.py"
    run_institutional = PROJECT_ROOT / "run_institutional_replay.py"
    
    has_replay_scripts = run_replay.exists() or run_instrumented.exists() or run_institutional.exists()
    has_replay_modules = len(replay_files) > 0
    
    if has_replay_scripts or has_replay_modules:
        findings.append(AuditFinding(
            id="DET-009",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title="Deterministic Replay Capability Found",
            description=f"Scripts de replay: {run_replay.exists()}, instrumented: {run_instrumented.exists()}, institutional: {run_institutional.exists()}. Módulos: {len(replay_files)}",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="DET-009",
            category="DETERMINISM",
            severity=HIGH,
            status=STATUS_WARNING,
            title="No Deterministic Replay Capability",
            description="Não há scripts ou módulos para replay determinístico de cenários.",
            location=str(PROJECT_ROOT),
            recommendation="Implementar deterministic replay: gravar inputs (market data, signals, orders) e reproduzir exatamente. Essencial para debugging e validação.",
        ))
    
    return findings


def _check_environment_isolation() -> list[AuditFinding]:
    """Verifica isolamento de ambiente para determinismo."""
    findings = []
    
    # Verifica .venv, requirements.txt, pyproject.toml
    req_txt = PROJECT_ROOT / "requirements.txt"
    pyproject = PROJECT_ROOT / "pyproject.toml"
    venv = PROJECT_ROOT / ".venv"
    dockerfile = PROJECT_ROOT / "Dockerfile"
    docker_compose = PROJECT_ROOT / "docker-compose.yml"
    
    has_pinned_deps = False
    if req_txt.exists():
        content = req_txt.read_text(encoding="utf-8")
        # Verifica se versões estão pinadas (==)
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        pinned = [l for l in lines if '==' in l and not any(skip in l for skip in ['>=', '<=', '~=', '>'])]
        has_pinned_deps = len(pinned) / max(len(lines), 1) > 0.8
    
    if has_pinned_deps:
        findings.append(AuditFinding(
            id="DET-010",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title="Dependencies Pinned",
            description="requirements.txt tem versões pinadas (==) na maioria das dependências.",
            location=str(req_txt),
        ))
    else:
        findings.append(AuditFinding(
            id="DET-010",
            category="DETERMINISM",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Dependencies Not Fully Pinned",
            description="requirements.txt não tem versões pinadas consistentemente. Risco de drift de dependências.",
            location=str(req_txt) if req_txt.exists() else str(PROJECT_ROOT),
            recommendation="Pin todas as dependências com == em requirements.txt ou usar pip-tools/poetry lockfile.",
        ))
    
    if dockerfile.exists() or docker_compose.exists():
        findings.append(AuditFinding(
            id="DET-011",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_PASS,
            title="Containerization Found",
            description=f"Dockerfile={dockerfile.exists()}, docker-compose={docker_compose.exists()}. Bom para reprodutibilidade de ambiente.",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="DET-011",
            category="DETERMINISM",
            severity=LOW,
            status=STATUS_INFO,
            title="No Containerization",
            description="Sem Dockerfile/docker-compose. Ambiente depende de configuração manual.",
            location=str(PROJECT_ROOT),
            recommendation="Considerar Docker para reprodutibilidade total de ambiente (OS, libs, Python version).",
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de determinismo."""
    section = AuditSection(
        name="15. Determinism Audit",
        description="Verifica reprodutibilidade determinística: seeds, operações não-determinísticas, FP, deps externas, replay, env isolation",
    )
    
    all_findings = []
    all_findings.extend(_check_fixed_seeds())
    all_findings.extend(_check_non_deterministic_ops())
    all_findings.extend(_check_floating_point())
    all_findings.extend(_check_external_dependencies())
    all_findings.extend(_check_deterministic_replay())
    all_findings.extend(_check_environment_isolation())
    
    section.findings = all_findings
    
    has_fail = any(f.status == STATUS_FAIL for f in all_findings)
    has_warning = any(f.status == STATUS_WARNING for f in all_findings)
    
    if has_fail:
        section.status = STATUS_FAIL
    elif has_warning:
        section.status = STATUS_WARNING
    else:
        section.status = STATUS_PASS
    
    return section