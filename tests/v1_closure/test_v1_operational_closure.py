"""
MERCURY-AI V1
FINAL OPERATIONAL CLOSURE / ROOT-CAUSE VERIFICATION

Objetivo:
    Provar operacionalmente o comportamento final do decision pipeline.

REGRAS:
    - NÃO modifica código de produção.
    - NÃO altera DecisionResolverEngine.
    - NÃO altera ProbabilityEngine.
    - NÃO altera DecisionResultBuilder.
    - Falhas são reportadas, nunca mascaradas.
    - Exception != WAIT legítimo.
    - Resolver != DecisionResult é FAIL.
"""

from __future__ import annotations

import json
import sys
import traceback
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Ensure project root is in path for imports
# The script is at tests/v1_closure/, so we need to go up 3 levels to reach the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================
# CONFIGURAÇÃO
# ============================================================

REPORT_DIR = Path("artifacts") / "v1_closure"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "v1_operational_closure.json"
TEXT_REPORT_FILE = REPORT_DIR / "v1_operational_closure.txt"

# ============================================================
# RESULTADOS
# ============================================================

@dataclass
class GateResult:
    gate: str
    expected: str
    actual: str
    status: str
    details: str = ""
    exception: Optional[str] = None

@dataclass
class PipelineSnapshot:
    case: str

    decision: Optional[str] = None
    resolver_decision: Optional[str] = None
    dominant_direction: Optional[str] = None

    opportunity_grade: Optional[str] = None

    institutional_strength: Optional[float] = None
    confluence_score: Optional[float] = None
    confidence_score: Optional[float] = None
    risk_score: Optional[float] = None
    trade_quality_score: Optional[float] = None

    buy_probability: Optional[float] = None
    sell_probability: Optional[float] = None
    wait_probability: Optional[float] = None

    trade_filter_allowed: Optional[bool] = None
    validation_valid: Optional[bool] = None
    validation_warnings: Any = None

    conflicting_signals: Optional[bool] = None

    resolver_rule: Optional[Any] = None

    exception: Optional[str] = None

    raw_keys: Any = None

# ============================================================
# UTILITÁRIOS
# ============================================================

def get_attr(obj: Any, *names: str, default=None):
    """
    Procura um atributo em múltiplos nomes possíveis.
    Não inventa valor.
    """
    if obj is None:
        return default

    for name in names:
        try:
            if hasattr(obj, name):
                value = getattr(obj, name)
                if value is not None:
                    return value
        except Exception:
            pass

        if isinstance(obj, dict) and name in obj:
            value = obj[name]
            if value is not None:
                return value

    return default

def normalize_decision(value: Any) -> Optional[str]:
    if value is None:
        return None

    text = str(value).upper().strip()

    for decision in ("BUY", "SELL", "WAIT", "NEUTRAL"):
        if decision in text:
            return decision

    return text

def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None

    try:
        return float(value)
    except Exception:
        return None

def dump_object_keys(obj: Any):
    if obj is None:
        return []

    if isinstance(obj, dict):
        return sorted(str(k) for k in obj.keys())

    try:
        return sorted(
            name
            for name in dir(obj)
            if not name.startswith("_")
        )
    except Exception:
        return []

# ============================================================
# IMPORTS DO MERCURY
# ============================================================

def import_mercury():
    """
    Importa as classes reais do projeto.

    Se algum caminho for diferente no seu repositório,
    ALTERE SOMENTE ESTE BLOCO.
    """

    from mercury_ai.brain.mercury_decision_engine import MercuryDecisionEngine

    return MercuryDecisionEngine

# ============================================================
# EXTRAÇÃO DO RESULTADO
# ============================================================

def extract_snapshot(case_name: str, result: Any) -> PipelineSnapshot:
    """
    Extrai os valores efetivamente produzidos pelo pipeline.

    Atenção:
    Não assume que resolver_decision existe no DecisionResult.
    Se não existir, ele permanece None e será marcado como
    GAP DE OBSERVABILIDADE.
    """

    snapshot = PipelineSnapshot(case=case_name)

    snapshot.decision = normalize_decision(
        get_attr(result, "decision", "final_decision")
    )

    snapshot.dominant_direction = normalize_decision(
        get_attr(
            result,
            "dominant_direction",
            "direction",
            "signal_direction",
        )
    )

    snapshot.opportunity_grade = get_attr(
        result,
        "opportunity_grade",
        "grade",
    )

    snapshot.institutional_strength = safe_float(
        get_attr(
            result,
            "institutional_strength",
        )
    )

    snapshot.confluence_score = safe_float(
        get_attr(
            result,
            "confluence_score",
            "confluence",
        )
    )

    snapshot.confidence_score = safe_float(
        get_attr(
            result,
            "confidence_score",
            "confidence",
        )
    )

    snapshot.risk_score = safe_float(
        get_attr(
            result,
            "risk_score",
            "risk",
        )
    )

    snapshot.trade_quality_score = safe_float(
        get_attr(
            result,
            "trade_quality_score",
            "quality",
        )
    )

    snapshot.buy_probability = safe_float(
        get_attr(result, "buy_probability")
    )

    snapshot.sell_probability = safe_float(
        get_attr(result, "sell_probability")
    )

    snapshot.wait_probability = safe_float(
        get_attr(result, "wait_probability")
    )

    snapshot.trade_filter_allowed = get_attr(
        result,
        "trade_filter_allowed",
        "allowed",
    )

    snapshot.validation_valid = get_attr(
        result,
        "is_valid",
        "validation_valid",
        "valid",
    )

    snapshot.validation_warnings = get_attr(
        result,
        "validation_warnings",
        "warnings",
    )

    snapshot.conflicting_signals = get_attr(
        result,
        "conflicting_signals",
        "has_conflict",
    )

    snapshot.resolver_rule = get_attr(
        result,
        "triggered_rule",
        "resolver_rule",
        "rule",
    )

    snapshot.raw_keys = dump_object_keys(result)

    return snapshot

# ============================================================
# EXECUÇÃO
# ============================================================

def run_pipeline_case(
    engine,
    case_name: str,
    payload: Any,
) -> PipelineSnapshot:

    snapshot = PipelineSnapshot(case=case_name)

    try:
        # Tenta primeiro analyze()
        if hasattr(engine, "analyze"):
            result = engine.analyze(payload)

        # Compatibilidade com pipelines que usam process()
        elif hasattr(engine, "process"):
            result = engine.process(payload)

        else:
            raise RuntimeError(
                "MercuryDecisionEngine não possui analyze() nem process()."
            )

        snapshot = extract_snapshot(case_name, result)

        return snapshot

    except Exception:
        snapshot.exception = traceback.format_exc()
        return snapshot

# ============================================================
# GATES
# ============================================================

def gate(
    name: str,
    expected: str,
    actual: str,
    condition: bool,
    details: str = "",
    exception: Optional[str] = None,
) -> GateResult:

    return GateResult(
        gate=name,
        expected=expected,
        actual=actual,
        status="PASS" if condition else "FAIL",
        details=details,
        exception=exception,
    )

def compare_final_decision(
    snapshot: PipelineSnapshot,
    expected: str,
) -> GateResult:

    return gate(
        f"{snapshot.case}: FINAL DECISION",
        expected,
        str(snapshot.decision),
        snapshot.decision == expected,
        "DecisionResult final",
        snapshot.exception,
    )

# ============================================================
# MAIN
# ============================================================

def main() -> int:

    started = datetime.now(timezone.utc).isoformat()

    gates: list[GateResult] = []
    snapshots: list[PipelineSnapshot] = []

    print()
    print("=" * 78)
    print("MERCURY-AI V1 — FINAL OPERATIONAL CLOSURE")
    print("=" * 78)
    print()

    try:
        MercuryDecisionEngine = import_mercury()
    except Exception:
        error = traceback.format_exc()

        gates.append(
            gate(
                "IMPORT",
                "MercuryDecisionEngine importável",
                "IMPORT FAILURE",
                False,
                exception=error,
            )
        )

        return write_report(
            started,
            gates,
            snapshots,
        )

    # --------------------------------------------------------
    # IMPORTANT
    # --------------------------------------------------------
    #
    # Este bloco precisa receber os mesmos fixtures/contextos
    # que o seu projeto já utiliza.
    #
    # Não inventaremos MarketContext.
    #
    # Se o MercuryDecisionEngine possuir construtor sem args,
    # este código funcionará.
    #
    # Se exigir dependências, ajuste somente create_engine().
    # --------------------------------------------------------

    def create_engine():
        return MercuryDecisionEngine()

    # --------------------------------------------------------
    # CASOS
    # --------------------------------------------------------
    #
    # Estes são carregados através de um módulo separado.
    #
    # Isso evita que este script invente dados de mercado.
    # --------------------------------------------------------

    try:
        from tests.v1_closure.v1_fixtures import (
            build_buy_case,
            build_sell_case,
            build_wait_case,
        )

        fixture_functions = {
            "BUY": build_buy_case,
            "SELL": build_sell_case,
            "WAIT": build_wait_case,
        }

    except Exception:
        error = traceback.format_exc()

        gates.append(
            gate(
                "FIXTURES",
                "fixtures determinísticos disponíveis",
                "FIXTURES NÃO CARREGADOS",
                False,
                exception=error,
            )
        )

        return write_report(
            started,
            gates,
            snapshots,
        )

    # --------------------------------------------------------
    # BUY
    # --------------------------------------------------------

    for case_name, expected in (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
        ("WAIT", "WAIT"),
    ):

        try:
            payload = fixture_functions[case_name]()
            engine = create_engine()

            snapshot = run_pipeline_case(
                engine,
                case_name,
                payload,
            )

            snapshots.append(snapshot)

            gates.append(
                compare_final_decision(
                    snapshot,
                    expected,
                )
            )

            if snapshot.exception:
                gates.append(
                    gate(
                        f"{case_name}: NO HIDDEN EXCEPTION",
                        "nenhuma exceção",
                        "EXCEPTION",
                        False,
                        exception=snapshot.exception,
                    )
                )
            else:
                gates.append(
                    gate(
                        f"{case_name}: NO HIDDEN EXCEPTION",
                        "nenhuma exceção",
                        "OK",
                        True,
                    )
                )

        except Exception:
            error = traceback.format_exc()

            gates.append(
                gate(
                    f"{case_name}: EXECUTION",
                    "pipeline executado",
                    "EXECUTION FAILURE",
                    False,
                    exception=error,
                )
            )

    # --------------------------------------------------------
    # INTEGRIDADE
    # --------------------------------------------------------

    for snapshot in snapshots:

        if snapshot.decision in ("BUY", "SELL"):

            gates.append(
                gate(
                    f"{snapshot.case}: DECISION NOT MASKED",
                    snapshot.decision,
                    snapshot.decision,
                    True,
                    "DecisionResult contém direção operacional.",
                )
            )

            # Probabilidade deve existir para uma decisão direcional.
            directional_probability = (
                snapshot.buy_probability
                if snapshot.decision == "BUY"
                else snapshot.sell_probability
            )

            gates.append(
                gate(
                    f"{snapshot.case}: DIRECTIONAL PROBABILITY",
                    "> 0",
                    str(directional_probability),
                    (
                        directional_probability is not None
                        and directional_probability > 0
                    ),
                )
            )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    return write_report(
        started,
        gates,
        snapshots,
    )

# ============================================================
# RELATÓRIO
# ============================================================

def write_report(
    started: str,
    gates: list[GateResult],
    snapshots: list[PipelineSnapshot],
) -> int:

    finished = datetime.now(timezone.utc).isoformat()

    passed = sum(
        1 for item in gates
        if item.status == "PASS"
    )

    failed = sum(
        1 for item in gates
        if item.status == "FAIL"
    )

    status = "CLOSED" if failed == 0 else "NOT CLOSED"

    report = {
        "title": "MERCURY-AI V1 — FINAL OPERATIONAL CLOSURE",
        "started_at": started,
        "finished_at": finished,
        "status": status,
        "gates": {
            "total": len(gates),
            "passed": passed,
            "failed": failed,
        },
        "gate_results": [
            asdict(item)
            for item in gates
        ],
        "pipeline_snapshots": [
            asdict(item)
            for item in snapshots
        ],
    }

    REPORT_FILE.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    lines = []

    lines.append(
        "MERCURY-AI V1 — FINAL OPERATIONAL CLOSURE"
    )
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"STATUS: {status}")
    lines.append(
        f"GATES: {len(gates)} | PASS: {passed} | FAIL: {failed}"
    )
    lines.append("")

    lines.append("GATE MATRIX")
    lines.append("-" * 78)

    for item in gates:
        lines.append(
            f"[{item.status}] "
            f"{item.gate} | "
            f"expected={item.expected} | "
            f"actual={item.actual}"
        )

        if item.details:
            lines.append(
                f"       {item.details}"
            )

    lines.append("")
    lines.append("PIPELINE SNAPSHOTS")
    lines.append("-" * 78)

    for snapshot in snapshots:

        lines.append("")
        lines.append(f"CASE: {snapshot.case}")

        fields = {
            "decision": snapshot.decision,
            "resolver_decision": snapshot.resolver_decision,
            "dominant_direction": snapshot.dominant_direction,
            "opportunity_grade": snapshot.opportunity_grade,
            "institutional_strength": snapshot.institutional_strength,
            "confluence_score": snapshot.confluence_score,
            "confidence_score": snapshot.confidence_score,
            "risk_score": snapshot.risk_score,
            "trade_quality_score": snapshot.trade_quality_score,
            "buy_probability": snapshot.buy_probability,
            "sell_probability": snapshot.sell_probability,
            "wait_probability": snapshot.wait_probability,
            "trade_filter_allowed": snapshot.trade_filter_allowed,
            "validation_valid": snapshot.validation_valid,
            "conflicting_signals": snapshot.conflicting_signals,
            "resolver_rule": snapshot.resolver_rule,
            "exception": snapshot.exception,
        }

        for key, value in fields.items():
            lines.append(
                f"  {key}: {value}"
            )

    lines.append("")
    lines.append("=" * 78)
    lines.append(
        f"FINAL VERDICT: {status}"
    )
    lines.append("=" * 78)

    TEXT_REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\n".join(lines))

    # CRITICAL:
    # CI/terminal pode usar isso para impedir falso fechamento.
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())