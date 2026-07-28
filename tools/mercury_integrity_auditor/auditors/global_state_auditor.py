"""
Auditoria de Estado Global — Fase 14.
Verifica gestão de estado global, singletons, variáveis globais:
- Variáveis globais mutáveis
- Singletons e padrões de estado compartilhado
- Configuração global (config.json, env vars)
- Estado de runtime (posições, ordens, PnL)
- Thread safety / concorrência
- Persistência e recuperação de estado
"""

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
    STATUS_INCONCLUSIVE,
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW,
)
from tools.mercury_integrity_auditor.models import AuditFinding, AuditSection


def _check_global_variables() -> list[AuditFinding]:
    """Verifica variáveis globais mutáveis no código."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    global_vars = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Detecta variáveis globais (no nível do módulo, não dentro de função/classe)
                if (stripped and not stripped.startswith('#') and 
                    not stripped.startswith('def ') and not stripped.startswith('class ') and
                    not stripped.startswith('import ') and not stripped.startswith('from ') and
                    '=' in stripped and not stripped.startswith('    ') and not stripped.startswith('\t')):
                    # Verifica se parece com variável global mutável
                    var_name = stripped.split('=')[0].strip()
                    if var_name.isupper() or var_name[0].islower():
                        # Pode ser constante ou variável global
                        if not var_name.isupper():  # não é constante (UPPER_CASE)
                            global_vars.append((str(f.relative_to(PROJECT_ROOT)), i+1, var_name))
        except Exception:
            pass
    
    # Filtra falsos positivos (constantes, configurações)
    mutable_globals = [g for g in global_vars if not g[2].isupper() and len(g[2]) > 2]
    
    if mutable_globals:
        findings.append(AuditFinding(
            id="GST-001",
            category="GLOBAL_STATE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Potential Mutable Global Variables: {len(mutable_globals)}",
            description=f"Variáveis globais potencialmente mutáveis encontradas: {mutable_globals[:5]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Evitar variáveis globais mutáveis. Usar dependency injection, context managers, ou classes de estado.",
        ))
    else:
        findings.append(AuditFinding(
            id="GST-001",
            category="GLOBAL_STATE",
            severity=LOW,
            status=STATUS_PASS,
            title="No Mutable Global Variables Detected",
            description="Nenhuma variável global mutável óbvia detectada no código.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_singletons() -> list[AuditFinding]:
    """Verifica uso de padrões Singleton."""
    findings = []
    
    singleton_files = list(MERCURY_AI_DIR.rglob("*singleton*.py"))
    singleton_files += list(MERCURY_AI_DIR.rglob("*instance*.py"))
    
    # Procura por padrões singleton no código
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    singleton_patterns = []
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(pattern in content for pattern in [
                "__new__", "get_instance", "_instance", "singleton", 
                "@singleton", "metaclass=Singleton", "__instance__"
            ]):
                singleton_patterns.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if singleton_patterns:
        findings.append(AuditFinding(
            id="GST-002",
            category="GLOBAL_STATE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Singleton Patterns Found: {len(singleton_patterns)}",
            description=f"Padrões Singleton detectados em: {', '.join(singleton_patterns[:3])}",
            location=str(MERCURY_AI_DIR),
            recommendation="Avaliar se singletons são necessários. Preferir dependency injection para testabilidade.",
        ))
    else:
        findings.append(AuditFinding(
            id="GST-002",
            category="GLOBAL_STATE",
            severity=LOW,
            status=STATUS_PASS,
            title="No Singleton Patterns Detected",
            description="Nenhum padrão Singleton explícito detectado.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_global_config() -> list[AuditFinding]:
    """Verifica configuração global."""
    findings = []
    
    config_json = PROJECT_ROOT / "config.json"
    config_py = list(MERCURY_AI_DIR.rglob("config.py"))
    config_py += list(PROJECT_ROOT.rglob("config.py"))
    env_files = list(PROJECT_ROOT.rglob(".env*"))
    
    has_config = config_json.exists() or len(config_py) > 0
    has_env = len(env_files) > 0
    
    if has_config:
        findings.append(AuditFinding(
            id="GST-003",
            category="GLOBAL_STATE",
            severity=LOW,
            status=STATUS_PASS,
            title="Global Configuration Found",
            description=f"Configuração global: config.json={config_json.exists()}, config.py={len(config_py)}, .env={has_env}",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="GST-003",
            category="GLOBAL_STATE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Global Configuration Not Structured",
            description="Não há arquivo de configuração centralizado (config.json, config.py, .env).",
            location=str(PROJECT_ROOT),
            recommendation="Centralizar configuração em config.json ou config.py com validação (pydantic).",
        ))
    
    # Verifica se config.json é válido
    if config_json.exists():
        try:
            json.loads(config_json.read_text(encoding="utf-8"))
            findings.append(AuditFinding(
                id="GST-003b",
                category="GLOBAL_STATE",
                severity=LOW,
                status=STATUS_PASS,
                title="config.json Valid JSON",
                description="config.json é JSON válido e parseável.",
                location=str(config_json),
            ))
        except json.JSONDecodeError as e:
            findings.append(AuditFinding(
                id="GST-003b",
                category="GLOBAL_STATE",
                severity=HIGH,
                status=STATUS_FAIL,
                title="config.json Invalid JSON",
                description=f"config.json contém JSON inválido: {e}",
                location=str(config_json),
                recommendation="Corrigir sintaxe JSON em config.json.",
            ))
    
    return findings


def _check_runtime_state() -> list[AuditFinding]:
    """Verifica gestão de estado de runtime (posições, ordens, PnL)."""
    findings = []
    
    state_files = list(MERCURY_AI_DIR.rglob("*state*.py"))
    state_files += list(MERCURY_AI_DIR.rglob("*position*.py"))
    state_files += list(MERCURY_AI_DIR.rglob("*order*.py"))
    state_files += list(MERCURY_AI_DIR.rglob("*portfolio*.py"))
    state_files += list(MERCURY_AI_DIR.rglob("*pnl*.py"))
    state_files += list(MERCURY_AI_DIR.rglob("*account*.py"))
    
    has_runtime_state = len(state_files) > 0
    
    if has_runtime_state:
        findings.append(AuditFinding(
            id="GST-004",
            category="GLOBAL_STATE",
            severity=LOW,
            status=STATUS_PASS,
            title="Runtime State Management Found",
            description=f"Gestão de estado de runtime: {len(state_files)} arquivo(s) (posições, ordens, portfolio, PnL).",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="GST-004",
            category="GLOBAL_STATE",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Runtime State Management Not Explicit",
            description="Não há módulos explícitos para gestão de estado de runtime (posições abertas, ordens pendentes, PnL, portfolio).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar state management: PositionManager, OrderManager, Portfolio, PnL tracker com persistência.",
        ))
    
    return findings


def _check_thread_safety() -> list[AuditFinding]:
    """Verifica thread safety / concorrência."""
    findings = []
    
    threading_files = list(MERCURY_AI_DIR.rglob("*thread*.py"))
    threading_files += list(MERCURY_AI_DIR.rglob("*lock*.py"))
    threading_files += list(MERCURY_AI_DIR.rglob("*async*.py"))
    threading_files += list(MERCURY_AI_DIR.rglob("*concurrent*.py"))
    
    # Procura por imports de threading/asyncio
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    uses_threading = False
    uses_asyncio = False
    has_locks = False
    
    for f in py_files:
        try:
            content = f.read_text(encoding="utf-8")
            if "import threading" in content or "from threading" in content:
                uses_threading = True
            if "import asyncio" in content or "from asyncio" in content:
                uses_asyncio = True
            if any(kw in content for kw in ["Lock()", "RLock()", "Semaphore", "Event()", "Condition()", "with lock"]):
                has_locks = True
        except Exception:
            pass
    
    if uses_threading or uses_asyncio:
        if has_locks:
            findings.append(AuditFinding(
                id="GST-005",
                category="GLOBAL_STATE",
                severity=LOW,
                status=STATUS_PASS,
                title="Thread Safety Mechanisms Found",
                description=f"Concorrência detectada: threading={uses_threading}, asyncio={uses_asyncio}, locks={has_locks}",
                location=str(MERCURY_AI_DIR),
            ))
        else:
            findings.append(AuditFinding(
                id="GST-005",
                category="GLOBAL_STATE",
                severity=HIGH,
                status=STATUS_WARNING,
                title="Concurrency Without Explicit Locking",
                description=f"Sistema usa concorrência (threading={uses_threading}, asyncio={uses_asyncio}) mas sem locks explícitos detectados.",
                location=str(MERCURY_AI_DIR),
                recommendation="Verificar race conditions. Usar locks, queues, ou estruturas thread-safe para estado compartilhado.",
            ))
    else:
        findings.append(AuditFinding(
            id="GST-005",
            category="GLOBAL_STATE",
            severity=LOW,
            status=STATUS_INFO,
            title="No Concurrency Detected",
            description="Sistema não parece usar threading/asyncio explicitamente. Single-threaded.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def _check_state_persistence() -> list[AuditFinding]:
    """Verifica persistência e recuperação de estado."""
    findings = []
    
    persist_files = list(MERCURY_AI_DIR.rglob("*persist*.py"))
    persist_files += list(MERCURY_AI_DIR.rglob("*checkpoint*.py"))
    persist_files += list(MERCURY_AI_DIR.rglob("*snapshot*.py"))
    persist_files += list(MERCURY_AI_DIR.rglob("*recover*.py"))
    persist_files += list(MERCURY_AI_DIR.rglob("*serializ*.py"))
    persist_files += list(MERCURY_AI_DIR.rglob("*pickle*.py"))
    persist_files += list(MERCURY_AI_DIR.rglob("*json*.py"))
    
    # Verifica .mercury directory para state files
    dot_mercury = PROJECT_ROOT / ".mercury"
    has_state_files = dot_mercury.exists() and any(dot_mercury.rglob("*.json"))
    
    has_persistence = len(persist_files) > 0 or has_state_files
    
    if has_persistence:
        findings.append(AuditFinding(
            id="GST-006",
            category="GLOBAL_STATE",
            severity=LOW,
            status=STATUS_PASS,
            title="State Persistence/Recovery Found",
            description=f"Persistência de estado: {len(persist_files)} módulos + .mercury state files={has_state_files}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="GST-006",
            category="GLOBAL_STATE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="State Persistence/Recovery Not Implemented",
            description="Não há mecanismo explícito de persistência/recuperação de estado (checkpoints, snapshots, serialization).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar checkpointing periódico de estado crítico (posições, ordens, config) para recovery após crash/restart.",
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de estado global."""
    section = AuditSection(
        name="14. Global State Audit",
        description="Verifica gestão de estado global: variáveis globais, singletons, config, runtime state, thread safety, persistência",
    )
    
    all_findings = []
    all_findings.extend(_check_global_variables())
    all_findings.extend(_check_singletons())
    all_findings.extend(_check_global_config())
    all_findings.extend(_check_runtime_state())
    all_findings.extend(_check_thread_safety())
    all_findings.extend(_check_state_persistence())
    
    section.findings = all_findings
    
    # Determina status geral da seção
    has_fail = any(f.status == STATUS_FAIL for f in all_findings)
    has_warning = any(f.status == STATUS_WARNING for f in all_findings)
    
    if has_fail:
        section.status = STATUS_FAIL
    elif has_warning:
        section.status = STATUS_WARNING
    else:
        section.status = STATUS_PASS
    
    return section