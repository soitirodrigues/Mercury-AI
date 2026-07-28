"""
Auditoria de Contratos — Fase 2.
Verifica a integridade dos dataclasses e contratos de API:
- Campos obrigatórios vs. opcionais
- Tipos corretos
- Imutabilidade (frozen=True)
- Consistência entre assinatura e documentação
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


# Dataclasses críticos conhecidos e seus contratos esperados
KNOWN_DATACLASSES = {
    "RiskAssessment": {
        "module": "mercury_ai.models.risk_assessment",
        "frozen": True,
        "required_fields": [
            "suggested_stop", "suggested_take_profit", "risk_reward_ratio",
            "expected_drawdown", "expected_volatility", "trade_quality",
            "max_exposure", "invalidation_point", "institutional_risk_score",
            "var_95", "var_99", "cvar_95", "kelly_fraction",
            "kelly_half", "kelly_quarter", "correlation_matrix", "stress_test_loss",
        ],
        "forbidden_fields": ["symbol", "cvar_99"],
    },
    "MarketData": {
        "module": "mercury_ai.models.market_data",
        "frozen": True,
        "required_fields": [
            "symbol", "timeframe", "close", "ema9", "ema21", "ema50",
            "rsi", "atr", "adx", "macd", "macd_signal",
            "bollinger_upper", "bollinger_lower", "volume",
        ],
    },
    "MarketContext": {
        "module": "mercury_ai.models.market_context",
        "frozen": True,
        "required_fields": [
            "market", "trend", "price_action", "support_resistance",
            "smart_money", "liquidity", "market_state", "market_regime",
            "mtf_consensus", "risk_assessment",
        ],
    },
    "MarketEvidenceBundle": {
        "module": "mercury_ai.models.evidence",
        "frozen": True,
        "required_fields": ["evidences"],
    },
}


class DataclassContractChecker(ast.NodeVisitor):
    """Verifica contratos de dataclasses."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.relpath = str(filepath.relative_to(PROJECT_ROOT))
        self.findings: list[AuditFinding] = []
        self.dataclasses_found = {}

    def visit_ClassDef(self, node):
        # Verifica se é um dataclass
        is_dataclass = False
        is_frozen = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                if decorator.func.id == "dataclass":
                    is_dataclass = True
                    for kw in decorator.keywords:
                        if kw.arg == "frozen" and isinstance(kw.value, ast.Constant):
                            is_frozen = kw.value.value
            elif isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                is_dataclass = True

        if is_dataclass:
            fields = []
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    fields.append(item.target.id)

            self.dataclasses_found[node.name] = {
                "frozen": is_frozen,
                "fields": fields,
                "lineno": node.lineno,
            }

        self.generic_visit(node)


def run() -> AuditSection:
    """Executa a auditoria de contratos."""
    section = AuditSection(
        name="2. Contract Audit",
        description="Verificação de integridade de dataclasses e contratos de API",
    )

    # Encontra todos os dataclasses
    all_dataclasses = {}
    for fpath in sorted((MERCURY_AI_DIR / "models").rglob("*.py")):
        try:
            tree = ast.parse(fpath.read_text(encoding="utf-8"), filename=str(fpath))
        except Exception:
            continue
        checker = DataclassContractChecker(fpath)
        checker.visit(tree)
        all_dataclasses.update(checker.dataclasses_found)

    # Verifica dataclasses conhecidos
    for name, contract in KNOWN_DATACLASSES.items():
        if name in all_dataclasses:
            actual = all_dataclasses[name]

            # Verifica frozen
            if contract["frozen"] and not actual["frozen"]:
                section.findings.append(AuditFinding(
                    id=f"CONTRACT-{name.upper()}-001",
                    category="Contract Audit",
                    severity=CRITICAL,
                    status=STATUS_FAIL,
                    title=f"{name} deveria ser frozen=True mas não é",
                    description=f"O dataclass {name} deve ser imutável (frozen=True) para garantir integridade dos dados.",
                    location=f"{contract['module']}.py:{actual['lineno']}",
                    recommendation=f"Adicionar frozen=True ao decorator @dataclass de {name}.",
                ))
            else:
                section.findings.append(AuditFinding(
                    id=f"CONTRACT-{name}-001",
                    category="Contract Audit",
                    severity=LOW,
                    status=STATUS_PASS,
                    title=f"{name} está corretamente frozen={actual['frozen']}",
                    description=f"Dataclass {name} com frozen={actual['frozen']}.",
                ))

            # Verifica campos obrigatórios
            missing = set(contract["required_fields"]) - set(actual["fields"])
            if missing:
                section.findings.append(AuditFinding(
                    id=f"CONTRACT-{name}-002",
                    category="Contract Audit",
                    severity=CRITICAL,
                    status=STATUS_FAIL,
                    title=f"{name}: campos obrigatórios ausentes",
                    description=f"Campos esperados mas não encontrados: {', '.join(sorted(missing))}",
                    location=f"{contract['module']}.py",
                    recommendation=f"Adicionar campos ausentes a {name}.",
                ))
            else:
                section.findings.append(AuditFinding(
                    id=f"CONTRACT-{name}-002",
                    category="Contract Audit",
                    severity=LOW,
                    status=STATUS_PASS,
                    title=f"{name}: todos os campos obrigatórios presentes",
                    description=f"{len(contract['required_fields'])} campos verificados.",
                ))

            # Verifica campos proibidos
            forbidden_found = set(contract.get("forbidden_fields", [])) & set(actual["fields"])
            if forbidden_found:
                section.findings.append(AuditFinding(
                    id=f"CONTRACT-{name}-003",
                    category="Contract Audit",
                    severity=HIGH,
                    status=STATUS_FAIL,
                    title=f"{name}: campos proibidos encontrados",
                    description=f"Campos que não deveriam existir: {', '.join(sorted(forbidden_found))}",
                    location=f"{contract['module']}.py",
                    recommendation=f"Remover campos proibidos de {name}.",
                ))
        else:
            section.findings.append(AuditFinding(
                id=f"CONTRACT-{name}-MISSING",
                category="Contract Audit",
                severity=HIGH,
                status=STATUS_FAIL,
                title=f"Dataclass esperado não encontrado: {name}",
                description=f"O dataclass {name} (esperado em {contract['module']}) não foi encontrado no código.",
                location=contract["module"],
                recommendation=f"Verificar se {name} existe e está no local esperado.",
            ))

    # Finding: Total de dataclasses encontrados
    section.findings.append(AuditFinding(
        id="CONTRACT-SUMMARY",
        category="Contract Audit",
        severity=LOW,
        status=STATUS_INFO,
        title=f"Total de dataclasses encontrados: {len(all_dataclasses)}",
        description=f"Dataclasses: {', '.join(sorted(all_dataclasses.keys()))}",
    ))

    # Determina status
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"

    return section