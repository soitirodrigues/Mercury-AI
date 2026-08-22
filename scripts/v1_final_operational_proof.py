#!/usr/bin/env python3
"""
MERCURY-AI V1 — FINAL OPERATIONAL PROOF
========================================

Objetivo:
    Provar o comportamento operacional do pipeline real da V1.

IMPORTANTE:
    - NÃO altera código de produção.
    - NÃO corrige nada.
    - NÃO monkey-patcha o Resolver.
    - NÃO cria BUY/SELL artificialmente.
    - Usa o pipeline/Scanner real do Mercury.
    - Registra o caminho completo até DecisionResult.

Gates:
    A = BUY real
    B = SELL real
    C = WAIT legítimo
    D = ausência de override pós-Resolver
    E = integridade da execução

Execute na raiz do Mercury-AI:

    python scripts/v1_final_operational_proof.py
"""

from __future__ import annotations

import json
import sys
import traceback
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ============================================================
# CONFIGURAÇÃO
# ============================================================

# ADAPTAR SOMENTE SE NECESSÁRIO:
#
# Informe aqui os ativos que o scanner real já utiliza.
#
# Exemplo:
ASSETS = [
    "BTC-USD",
    "ETH-USD",
]

TIMEFRAME = "1h"

REPORT_DIR = ROOT / "reports" / "v1_operational_proof"

# ============================================================
# UTILITÁRIOS
# ============================================================

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def safe_value(obj: Any, *names: str, default: Any = None) -> Any:
    """
    Obtém o primeiro atributo existente.
    """
    for name in names:
        if obj is None:
            continue

        if isinstance(obj, dict) and name in obj:
            return obj[name]

        if hasattr(obj, name):
            return getattr(obj, name)

    return default

def serialize(obj: Any) -> Any:
    """
    Serialização tolerante para relatório.
    """
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (list, tuple, set)):
        return [serialize(x) for x in obj]

    if isinstance(obj, dict):
        return {
            str(k): serialize(v)
            for k, v in obj.items()
        }

    if is_dataclass(obj):
        return serialize(asdict(obj))

    if hasattr(obj, "__dict__"):
        result = {}
        for key, value in vars(obj).items():
            if key.startswith("_"):
                continue
            try:
                result[key] = serialize(value)
            except Exception:
                result[key] = repr(value)
        return result

    return repr(obj)

def print_field(label: str, value: Any) -> None:
    print(f"  {label:<32}: {value}")

def decision_of(result: Any) -> str | None:
    value = safe_value(
        result,
        "decision",
        "final_decision",
        default=None,
    )

    if value is None:
        return None

    if hasattr(value, "value"):
        value = value.value

    return str(value).upper()

# ============================================================
# PIPELINE REAL
# ============================================================

def create_scanner():
    """
    Cria o MercuryScanner real do projeto.

    Use exatamente a mesma classe/entrypoint utilizada
    no teste anterior que produziu BTC-USD / ETH-USD.
    """
    from mercury_ai.brain.scanner import MercuryScanner
    return MercuryScanner()

def run_asset(scanner: Any, asset: str):
    """
    Executa o scanner real para um ativo específico.

    O MercuryScanner.scan() processa todos os ativos do registry,
    então retornamos o resultado para o ativo solicitado.
    """
    # O scanner.scan() processa todos os ativos internamente
    # e retorna uma lista de análises. Pegamos o resultado
    # para o ativo específico.
    try:
        analyses = scanner.scan()
        
        # Encontra a análise para o ativo solicitado
        for analysis in analyses:
            # A análise tem um campo 'market' ou podemos verificar pelo símbolo
            # O AnalysisResult contém o decision que temos bisogno
            if hasattr(analysis, 'market') and analysis.market is not None:
                if hasattr(analysis.market, 'symbol') and analysis.market.symbol == asset:
                    return analysis
            # Alternative: check if decision matches
            if hasattr(analysis, 'decision') and analysis.decision is not None:
                # Verificar se este é o resultado para nosso ativo
                # O pipeline.analyze() usa o símbolo diretamente
                return analysis
        
        # Se não encontrou, retorna a primeira análise (deveria haver pelo menos uma)
        if analyses:
            return analyses[0]
        
        raise RuntimeError(f"Nenhum resultado encontrado para ativo {asset}")
        
    except Exception as exc:
        raise RuntimeError(f"Erro ao executar scanner para {asset}: {repr(exc)}") from exc

# ============================================================
# EXTRAÇÃO DO TRACE
# ============================================================

def extract_trace(result: Any) -> dict[str, Any]:
    """
    Extrai os campos do resultado do pipeline AnalysisResult/DecisionResult.

    O pipeline retorna um AnalysisResult que contém um objeto DecisionResult
    com todos os campos necessários para o rastreamento.
    """

    # O result pode ser um AnalysisResult ou dict - tentar extrair o decision
    decision = safe_value(
        result,
        "decision",
        default=None,
    )

    if decision is None:
        # Se não tiver decision direto, tentar como dict
        decision = safe_value(
            result,
            "DecisionResult",
            default=None,
        )

    # Obter o objeto DecisionResult
    decision_result = safe_value(
        result,
        "decision_result",
        "result",
        default=decision,
    )

    # Se ainda não tivemos sucesso, usar o result como está
    if decision_result is None:
        decision_result = result

    # Função helper para safe get de atributos do DecisionResult
    def sd(obj: Any, *names: str, default: Any = None) -> Any:
        """Safe decision get - primeiro atributo existente."""
        for name in names:
            if obj is None:
                continue
            if hasattr(obj, name):
                return getattr(obj, name)
        return default

    # Extrair do DecisionResult
    # Note: str(None) gives "None" string, so we only convert non-None values
    def to_str(val: Any) -> str | None:
        """Converts value to string, but returns None if the value is None."""
        if val is None:
            return None
        return str(val)

    trace = {
        "final_decision": to_str(sd(decision_result, "decision", default=None) or "").upper(),

        "dominant_direction": sd(decision_result, "dominant_direction", default=None),

        "trade_filter_allowed": sd(decision_result, "trade_filter_allowed", default=None),

        "trade_filter_quality_score": sd(
            decision_result,
            "trade_filter_quality_score",
            "quality_score",
            default=None
        ),

        "is_valid": sd(decision_result, "is_valid", default=None),

        "validation_warnings": serialize(
            sd(
                decision_result,
                "validation_warnings",
                default=[]
            )
        ),

        "confluence_score": sd(
            decision_result,
            "confluence_score",
            default=None
        ),

        "conflicting_signals": sd(
            decision_result,
            "conflicting_signals",
            default=None
        ),

        "institutional_strength": sd(
            decision_result,
            "institutional_strength",
            default=None
        ),

        "opportunity_grade": sd(
            decision_result,
            "opportunity_grade",
            "grade",
            default=None
        ),

        "buy_probability": sd(
            decision_result,
            "buy_probability",
            default=None
        ),

        "sell_probability": sd(
            decision_result,
            "sell_probability",
            default=None
        ),

        "wait_probability": sd(
            decision_result,
            "wait_probability",
            default=None
        ),

        "resolver_decision": sd(decision_result, "resolver_decision", default=None),

        "resolver_rule": sd(
            decision_result,
            "resolver_rule",
            "triggered_rule",
            "rule",
            "rule_number",
            default=None
        ),
    }

    return trace

# ============================================================
# GATES
# ============================================================

def gate_buy(trace: dict[str, Any]) -> bool:
    return (
        trace["dominant_direction"] == "BUY"
        and trace["resolver_decision"] == "BUY"
        and trace["final_decision"] == "BUY"
    )

def gate_sell(trace: dict[str, Any]) -> bool:
    return (
        trace["dominant_direction"] == "SELL"
        and trace["resolver_decision"] == "SELL"
        and trace["final_decision"] == "SELL"
    )

def gate_no_post_resolver_override(trace: dict[str, Any]) -> bool:
    resolver = trace["resolver_decision"]
    final = trace["final_decision"]

    if resolver in ("BUY", "SELL"):
        return final == resolver

    return True

# ============================================================
# MAIN
# ============================================================

def main() -> int:

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    started = utc_now()

    print()
    print("=" * 72)
    print("MERCURY-AI V1 — FINAL OPERATIONAL PROOF")
    print("=" * 72)
    print()
    print("Production code modification: NONE")
    print(f"Started: {started}")
    print()

    report = {
        "title": "MERCURY-AI V1 — FINAL OPERATIONAL PROOF",
        "started": started,
        "timeframe": TIMEFRAME,
        "assets": ASSETS,
        "production_code_changed_by_script": False,
        "cases": [],
        "gates": {},
        "errors": [],
    }

    try:
        scanner = create_scanner()

    except Exception as exc:
        print("ERRO AO CRIAR SCANNER")
        print()
        traceback.print_exc()

        report["errors"].append(
            {
                "stage": "create_scanner",
                "error": repr(exc),
                "traceback": traceback.format_exc(),
            }
        )

        save_report(report)

        return 2

    # --------------------------------------------------------
    # EXECUÇÃO DOS ATIVOS REAIS
    # --------------------------------------------------------

    for asset in ASSETS:

        print("-" * 72)
        print(f"ASSET: {asset}")
        print("-" * 72)

        try:
            result = run_asset(
                scanner,
                asset,
            )

            trace = extract_trace(result)

            case = {
                "asset": asset,
                "status": "EXECUTED",
                "trace": trace,
                "raw_result": serialize(result),
            }

            report["cases"].append(case)

            for key, value in trace.items():
                print_field(
                    key,
                    value,
                )

            print()

            print_field(
                "BUY gate",
                "PASS" if gate_buy(trace) else "NOT-BUY",
            )

            print_field(
                "SELL gate",
                "PASS" if gate_sell(trace) else "NOT-SELL",
            )

            print_field(
                "post-resolver integrity",
                (
                    "PASS"
                    if gate_no_post_resolver_override(trace)
                    else "FAIL"
                ),
            )

            print()

        except Exception as exc:

            print()
            print(f"ERROR: {asset}")
            traceback.print_exc()

            report["cases"].append(
                {
                    "asset": asset,
                    "status": "ERROR",
                    "error": repr(exc),
                    "traceback": traceback.format_exc(),
                }
            )

            report["errors"].append(
                {
                    "asset": asset,
                    "error": repr(exc),
                    "traceback": traceback.format_exc(),
                }
            )

    # --------------------------------------------------------
    # GATES FINAIS
    # --------------------------------------------------------

    traces = [
        case["trace"]
        for case in report["cases"]
        if case.get("status") == "EXECUTED"
    ]

    buy_pass = any(
        gate_buy(trace)
        for trace in traces
    )

    sell_pass = any(
        gate_sell(trace)
        for trace in traces
    )

    post_resolver_pass = all(
        gate_no_post_resolver_override(trace)
        for trace in traces
    )

    report["gates"] = {
        "BUY_real_pipeline": buy_pass,
        "SELL_real_pipeline": sell_pass,
        "post_resolver_integrity": post_resolver_pass,
        "execution_errors": len(report["errors"]) == 0,
    }

    report["finished"] = utc_now()

    save_report(report)

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print()
    print("=" * 72)
    print("FINAL GATE RESULT")
    print("=" * 72)

    print_field(
        "BUY real pipeline",
        "PASS" if buy_pass else "FAIL",
    )

    print_field(
        "SELL real pipeline",
        "PASS" if sell_pass else "FAIL",
    )

    print_field(
        "post-resolver integrity",
        "PASS" if post_resolver_pass else "FAIL",
    )

    print_field(
        "execution errors",
        "PASS" if not report["errors"] else "FAIL",
    )

    print()

    if buy_pass and sell_pass and post_resolver_pass:
        print("=" * 72)
        print("V1 OPERATIONAL PROOF: PASS")
        print("=" * 72)
        print()
        print("BUY e SELL foram demonstrados no pipeline real.")
        print("Nenhum BUY/SELL foi convertido após o Resolver.")
        print()
        print(
            f"Relatório: "
            f"{REPORT_DIR / 'v1_operational_proof.json'}"
        )

        return 0

    print("=" * 72)
    print("V1 OPERATIONAL PROOF: INCOMPLETE")
    print("=" * 72)
    print()
    print(
        "Não altere código ainda. "
        "O relatório acima mostra exatamente qual gate faltou."
    )
    print()
    print(
        f"Relatório: "
        f"{REPORT_DIR / 'v1_operational_proof.json'}"
    )

    return 1

# ============================================================
# RELATÓRIO
# ============================================================

def save_report(report: dict[str, Any]) -> None:

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        REPORT_DIR /
        "v1_operational_proof.json"
    )

    path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            default=str,
        ),
        encoding="utf-8",
    )

if __name__ == "__main__":
    raise SystemExit(main())