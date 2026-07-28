"""
Auditoria de Dados — Fase 12.
Verifica qualidade, integridade e rastreabilidade dos dados:
- Schema validation
- Data lineage / provenance
- Missing data handling
- Data drift detection
- Train/test leakage prevention
- PII / sensitive data handling
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


def _check_data_schema_validation() -> list[AuditFinding]:
    """Verifica se há validação de schema de dados de entrada."""
    findings = []
    
    schema_files = list(MERCURY_AI_DIR.rglob("*schema*.py"))
    schema_files += list(MERCURY_AI_DIR.rglob("*validation*.py"))
    schema_files += list(MERCURY_AI_DIR.rglob("*pydantic*.py"))
    schema_files += list(MERCURY_AI_DIR.rglob("*dataclass*.py"))
    
    has_schema_validation = False
    for f in schema_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(kw in content for kw in ["BaseModel", "validate", "schema", "pydantic", "dataclass", "Field"]):
                has_schema_validation = True
                break
        except Exception:
            pass
    
    if has_schema_validation:
        findings.append(AuditFinding(
            id="DATA-001",
            category="DATA",
            severity=LOW,
            status=STATUS_PASS,
            title="Data Schema Validation Found",
            description="Sistema possui validação de schema de dados (pydantic, dataclasses, ou similar).",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="DATA-001",
            category="DATA",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Data Schema Validation Missing",
            description="Não há validação formal de schema para dados de entrada (market data, config, features).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar validação de schema com pydantic ou similar para todos os inputs de dados.",
        ))
    
    return findings


def _check_data_lineage() -> list[AuditFinding]:
    """Verifica se há rastreabilidade de lineage dos dados."""
    findings = []
    
    lineage_files = list(MERCURY_AI_DIR.rglob("*lineage*.py"))
    lineage_files += list(MERCURY_AI_DIR.rglob("*provenance*.py"))
    lineage_files += list(MERCURY_AI_DIR.rglob("*data*version*.py"))
    
    # Verifica se há versionamento de dados (DVC, etc)
    dvc_files = list(PROJECT_ROOT.rglob(".dvc*"))
    dvc_files += list(PROJECT_ROOT.rglob("dvc.yaml"))
    dvc_files += list(PROJECT_ROOT.rglob("dvc.lock"))
    
    has_lineage = len(lineage_files) > 0 or len(dvc_files) > 0
    
    if has_lineage:
        findings.append(AuditFinding(
            id="DATA-002",
            category="DATA",
            severity=LOW,
            status=STATUS_PASS,
            title="Data Lineage / Versioning Found",
            description=f"Encontrado rastreabilidade de dados: {len(lineage_files)} arquivos lineage + DVC={len(dvc_files)>0}",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="DATA-002",
            category="DATA",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Data Lineage / Versioning Missing",
            description="Não há rastreabilidade de lineage dos dados (origem, transformações, versionamento).",
            location=str(PROJECT_ROOT),
            recommendation="Implementar data lineage tracking e considerar DVC para versionamento de datasets.",
        ))
    
    return findings


def _check_missing_data_handling() -> list[AuditFinding]:
    """Verifica tratamento de dados faltantes."""
    findings = []
    
    missing_files = list(MERCURY_AI_DIR.rglob("*missing*.py"))
    missing_files += list(MERCURY_AI_DIR.rglob("*imput*.py"))
    missing_files += list(MERCURY_AI_DIR.rglob("*nan*.py"))
    missing_files += list(MERCURY_AI_DIR.rglob("*fillna*.py"))
    
    has_missing_handling = False
    for f in missing_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(kw in content.lower() for kw in ["fillna", "dropna", "interpolate", "impute", "missing", "nan", "null"]):
                has_missing_handling = True
                break
        except Exception:
            pass
    
    if has_missing_handling:
        findings.append(AuditFinding(
            id="DATA-003",
            category="DATA",
            severity=LOW,
            status=STATUS_PASS,
            title="Missing Data Handling Found",
            description="Sistema possui tratamento explícito de dados faltantes (NaN, None, gaps).",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="DATA-003",
            category="DATA",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Missing Data Handling Not Explicit",
            description="Tratamento de dados faltantes (gaps em market data, NaN em features) não encontrado explicitamente.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar política explícita de tratamento de missing data (forward fill, interpolate, drop, flag).",
        ))
    
    return findings


def _check_data_drift_detection() -> list[AuditFinding]:
    """Verifica detecção de data drift."""
    findings = []
    
    drift_files = list(MERCURY_AI_DIR.rglob("*drift*.py"))
    drift_files += list(MERCURY_AI_DIR.rglob("*monitor*.py"))
    drift_files += list(MERCURY_AI_DIR.rglob("*evidently*.py"))
    drift_files += list(MERCURY_AI_DIR.rglob("*whylogs*.py"))
    
    has_drift_detection = len(drift_files) > 0
    
    if has_drift_detection:
        findings.append(AuditFinding(
            id="DATA-004",
            category="DATA",
            severity=LOW,
            status=STATUS_PASS,
            title="Data Drift Detection Found",
            description=f"Encontrados {len(drift_files)} arquivo(s) relacionados a detecção de data drift.",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="DATA-004",
            category="DATA",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Data Drift Detection Not Implemented",
            description="Não há monitoramento de data drift (distribuição de features mudando ao longo do tempo).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar data drift detection (ex: Evidently AI, whylogs, KS-test, PSI) para features críticas.",
        ))
    
    return findings


def _check_train_test_leakage() -> list[AuditFinding]:
    """Verifica prevenção de leakage train/test."""
    findings = []
    
    # Procura por práticas de ML que podem indicar leakage
    ml_files = list(MERCURY_AI_DIR.rglob("*train*.py"))
    ml_files += list(MERCURY_AI_DIR.rglob("*model*.py"))
    ml_files += list(MERCURY_AI_DIR.rglob("*feature*.py"))
    ml_files += list(MERCURY_AI_DIR.rglob("*pipeline*.py"))
    
    has_leakage_prevention = False
    leakage_indicators = []
    
    for f in ml_files:
        try:
            content = f.read_text(encoding="utf-8")
            # Boas práticas
            if any(kw in content for kw in ["TimeSeriesSplit", "PurgedKFold", "CombinatorialPurgedKFold", "embargo", "gap"]):
                has_leakage_prevention = True
            # Indicadores de risco
            if any(kw in content for kw in ["train_test_split", "random_state", "shuffle=True"]) and "TimeSeriesSplit" not in content:
                leakage_indicators.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if has_leakage_prevention:
        findings.append(AuditFinding(
            id="DATA-005",
            category="DATA",
            severity=LOW,
            status=STATUS_PASS,
            title="Train/Test Leakage Prevention Found",
            description="Sistema usa validação temporal adequada (TimeSeriesSplit, PurgedKFold, embargo/gap).",
            location=str(MERCURY_AI_DIR),
        ))
    elif leakage_indicators:
        findings.append(AuditFinding(
            id="DATA-005",
            category="DATA",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Potential Train/Test Leakage Risk",
            description=f"Arquivos usam train_test_split aleatório sem validação temporal: {', '.join(leakage_indicators[:3])}",
            location=str(MERCURY_AI_DIR),
            recommendation="Substituir random split por validação temporal (TimeSeriesSplit, PurgedKFold) para séries temporais financeiras.",
        ))
    else:
        findings.append(AuditFinding(
            id="DATA-005",
            category="DATA",
            severity=MEDIUM,
            status=STATUS_INCONCLUSIVE,
            title="Train/Test Leakage Prevention Unclear",
            description="Não foi possível determinar se há prevenção de leakage. Verificar manualmente pipelines de ML.",
            location=str(MERCURY_AI_DIR),
            recommendation="Auditar manualmente: usar TimeSeriesSplit, evitar look-ahead bias, implementar embargo/gap.",
        ))
    
    return findings


def _check_pii_handling() -> list[AuditFinding]:
    """Verifica tratamento de dados sensíveis/PII."""
    findings = []
    
    # Em trading, PII não é comum, mas verifica se há logs com dados sensíveis
    log_files = list(MERCURY_AI_DIR.rglob("*log*.py"))
    log_files += list(MERCURY_AI_DIR.rglob("*config*.py"))
    log_files += list(PROJECT_ROOT.rglob("*.env*"))
    
    has_env_files = len(list(PROJECT_ROOT.rglob(".env*"))) > 0
    has_secrets_in_config = False
    
    for f in log_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(kw in content.lower() for kw in ["password", "secret", "key", "token", "api_key"]):
                has_secrets_in_config = True
                break
        except Exception:
            pass
    
    if has_secrets_in_config:
        findings.append(AuditFinding(
            id="DATA-006",
            category="DATA",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Potential Secrets in Code/Config",
            description="Possíveis secrets (password, api_key, token) encontrados em arquivos de config/log.",
            location=str(MERCURY_AI_DIR),
            recommendation="Mover secrets para variáveis de ambiente ou vault. Nunca commitar secrets.",
        ))
    elif has_env_files:
        findings.append(AuditFinding(
            id="DATA-006",
            category="DATA",
            severity=LOW,
            status=STATUS_PASS,
            title="Environment Files Found for Secrets",
            description="Arquivos .env encontrados - secrets devem estar em variáveis de ambiente.",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="DATA-006",
            category="DATA",
            severity=LOW,
            status=STATUS_INFO,
            title="No PII/Secrets Detected",
            description="Nenhum dado sensível (PII, secrets) detectado em config/logs. Trading data typically não contém PII.",
            location=str(MERCURY_AI_DIR),
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de dados."""
    section = AuditSection(
        name="12. Data Audit",
        description="Verifica qualidade, integridade e rastreabilidade dos dados: schema, lineage, missing data, drift, leakage, PII",
    )
    
    all_findings = []
    all_findings.extend(_check_data_schema_validation())
    all_findings.extend(_check_data_lineage())
    all_findings.extend(_check_missing_data_handling())
    all_findings.extend(_check_data_drift_detection())
    all_findings.extend(_check_train_test_leakage())
    all_findings.extend(_check_pii_handling())
    
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