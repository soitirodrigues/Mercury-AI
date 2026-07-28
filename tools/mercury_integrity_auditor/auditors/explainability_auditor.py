"""
Auditoria de Explicabilidade — Fase 11.
Verifica se o sistema possui capacidades de explicabilidade:
- Feature importance disponível
- SHAP values ou similar
- Explicações de decisões de trading
- Logs de decisão auditáveis
- Model cards / documentação de modelos
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


def _check_feature_importance() -> list[AuditFinding]:
    """Verifica se há feature importance implementado."""
    findings = []
    
    # Procura por arquivos que implementam feature importance
    fi_files = list(MERCURY_AI_DIR.rglob("*feature*importance*.py"))
    fi_files += list(MERCURY_AI_DIR.rglob("*feature_importance*.py"))
    fi_files += list(MERCURY_AI_DIR.rglob("*shap*.py"))
    fi_files += list(MERCURY_AI_DIR.rglob("*explain*.py"))
    
    if fi_files:
        findings.append(AuditFinding(
            id="EXP-001",
            category="EXPLAINABILITY",
            severity=LOW,
            status=STATUS_PASS,
            title="Feature Importance / SHAP Implementation Found",
            description=f"Encontrados {len(fi_files)} arquivo(s) relacionados a feature importance/SHAP: {[str(f.relative_to(PROJECT_ROOT)) for f in fi_files]}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="EXP-001",
            category="EXPLAINABILITY",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Feature Importance / SHAP Not Implemented",
            description="Nenhuma implementação de feature importance, SHAP values ou explicabilidade de modelos encontrada.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar feature importance (ex: SHAP, permutation importance) para modelos de ML.",
        ))
    
    return findings


def _check_decision_logging() -> list[AuditFinding]:
    """Verifica se decisões de trading são logadas com explicação."""
    findings = []
    
    # Procura por logging de decisões
    decision_files = list(MERCURY_AI_DIR.rglob("*decision*.py"))
    decision_files += list(MERCURY_AI_DIR.rglob("*trade*log*.py"))
    decision_files += list(MERCURY_AI_DIR.rglob("*audit*log*.py"))
    
    has_decision_logging = False
    for f in decision_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(kw in content.lower() for kw in ["decision", "explain", "reason", "rationale", "why"]):
                has_decision_logging = True
                break
        except Exception:
            pass
    
    if has_decision_logging:
        findings.append(AuditFinding(
            id="EXP-002",
            category="EXPLAINABILITY",
            severity=LOW,
            status=STATUS_PASS,
            title="Decision Logging with Explanations Found",
            description="Sistema possui logging de decisões com explicações/razões.",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="EXP-002",
            category="EXPLAINABILITY",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Decision Logging with Explanations Missing",
            description="Decisões de trading não são logadas com explicações auditáveis (por que entrou/saiu, quais features dispararam).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar logging estruturado de decisões com feature contributions e rationale.",
        ))
    
    return findings


def _check_model_cards() -> list[AuditFinding]:
    """Verifica se existem model cards / documentação de modelos."""
    findings = []
    
    model_card_files = list(PROJECT_ROOT.rglob("MODEL_CARD*"))
    model_card_files += list(PROJECT_ROOT.rglob("model_card*"))
    model_card_files += list(PROJECT_ROOT.rglob("*model*card*.md"))
    model_card_files += list(MERCURY_AI_DIR.rglob("*model*doc*.md"))
    
    # Também verifica models.json
    models_json = PROJECT_ROOT / "models.json"
    has_models_json = models_json.exists()
    
    if model_card_files or has_models_json:
        findings.append(AuditFinding(
            id="EXP-003",
            category="EXPLAINABILITY",
            severity=LOW,
            status=STATUS_PASS,
            title="Model Documentation Found",
            description=f"Encontrada documentação de modelos: {len(model_card_files)} model card(s) + models.json={has_models_json}",
            location=str(PROJECT_ROOT),
        ))
    else:
        findings.append(AuditFinding(
            id="EXP-003",
            category="EXPLAINABILITY",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Model Cards / Documentation Missing",
            description="Não existem model cards ou documentação formal dos modelos (performance, limitações, uso pretendido, dados de treino).",
            location=str(PROJECT_ROOT),
            recommendation="Criar model cards seguindo padrão (ex: Google Model Cards) para cada modelo em produção.",
        ))
    
    return findings


def _check_counterfactual_explanations() -> list[AuditFinding]:
    """Verifica se há explicações contrafactuais (what-if)."""
    findings = []
    
    cf_files = list(MERCURY_AI_DIR.rglob("*counterfactual*.py"))
    cf_files += list(MERCURY_AI_DIR.rglob("*whatif*.py"))
    cf_files += list(MERCURY_AI_DIR.rglob("*what_if*.py"))
    
    if cf_files:
        findings.append(AuditFinding(
            id="EXP-004",
            category="EXPLAINABILITY",
            severity=LOW,
            status=STATUS_PASS,
            title="Counterfactual Explanations Found",
            description=f"Encontrados {len(cf_files)} arquivo(s) relacionados a explicações contrafactuais.",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="EXP-004",
            category="EXPLAINABILITY",
            severity=LOW,
            status=STATUS_INFO,
            title="Counterfactual Explanations Not Implemented",
            description="Explicações contrafactuais (what-if analysis) não implementadas. Opcional para V1.",
            location=str(MERCURY_AI_DIR),
            recommendation="Considerar implementar para versões futuras: 'O que aconteceria se feature X tivesse valor Y?'.",
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de explicabilidade."""
    section = AuditSection(
        name="11. Explainability Audit",
        description="Verifica capacidades de explicabilidade: feature importance, decision logging, model cards, counterfactuals",
    )
    
    all_findings = []
    all_findings.extend(_check_feature_importance())
    all_findings.extend(_check_decision_logging())
    all_findings.extend(_check_model_cards())
    all_findings.extend(_check_counterfactual_explanations())
    
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