"""
Configuração do Mercury Integrity Auditor.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Diretórios
MERCURY_AI_DIR = PROJECT_ROOT / "mercury_ai"
TESTS_DIR = PROJECT_ROOT / "tests"
TOOLS_DIR = PROJECT_ROOT / "tools"
DOT_MERCURY_DIR = PROJECT_ROOT / ".mercury"
AUDIT_OUTPUT_DIR = PROJECT_ROOT / ".mercury" / "audits"

# Timestamp da auditoria
AUDIT_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Arquivos de saída
REPORT_MD = AUDIT_OUTPUT_DIR / f"MERCURY_INTEGRITY_AUDIT_{AUDIT_TIMESTAMP}.md"
REPORT_JSON = AUDIT_OUTPUT_DIR / f"MERCURY_INTEGRITY_AUDIT_{AUDIT_TIMESTAMP}.json"

# Exclusões de scan
EXCLUDE_DIRS = {
    "__pycache__",
    ".venv",
    ".pytest_cache",
    ".git",
    "node_modules",
    ".mypy_cache",
    "egg-info",
}

# Arquivos a ignorar
EXCLUDE_FILES = {
    "__init__.py",  # será processado, mas não como módulo standalone
}

# Status possíveis
STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_INCONCLUSIVE = "INCONCLUSIVE"
STATUS_WARNING = "WARNING"
STATUS_INFO = "INFO"

# Severidades
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"