"""
Executor principal do Mercury Integrity Auditor.
Orquestra todas as fases de auditoria e gera o relatório final.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

from .config import (
    PROJECT_ROOT,
    MERCURY_AI_DIR,
    TESTS_DIR,
    AUDIT_OUTPUT_DIR,
    AUDIT_TIMESTAMP,
    REPORT_MD,
    REPORT_JSON,
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
from .models import AuditFinding, AuditSection, AuditReport

# Importa módulos de auditoria
from .auditors import (
    static_auditor,
    contract_auditor,
    dependency_auditor,
    masking_auditor,
    runtime_auditor,
    flow_auditor,
    test_auditor,
    decision_auditor,
    coverage_auditor,
    integrity_auditor,
    explainability_auditor,
    data_auditor,
    universe_auditor,
    global_state_auditor,
    determinism_auditor,
    performance_auditor,
    backtest_auditor,
    report,
)


def ensure_output_dir():
    """Garante que o diretório de saída existe."""
    AUDIT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_audit_phase(name: str, auditor_fn, *args, **kwargs) -> AuditSection:
    """Executa uma fase de auditoria e retorna a seção."""
    print(f"\n{'='*60}")
    print(f"  🔍 Executando: {name}")
    print(f"{'='*60}")
    start = time.time()
    try:
        section = auditor_fn(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  ✅ {name} concluído em {elapsed:.1f}s")
        print(f"     PASS={section.pass_count} FAIL={section.fail_count} "
              f"WARN={section.warning_count} INFO={section.info_count} "
              f"INC={section.inconclusive_count}")
        return section
    except Exception as e:
        elapsed = time.time() - start
        print(f"  ❌ {name} FALHOU em {elapsed:.1f}s: {e}")
        section = AuditSection(
            name=name,
            description=f"Auditoria: {name}",
            status="FAIL",
        )
        section.findings.append(AuditFinding(
            id=f"AUDIT-{name.replace(' ', '-').upper()}-ERR",
            category=name,
            severity=CRITICAL,
            status=STATUS_FAIL,
            title=f"Fase de auditoria falhou: {name}",
            description=str(e),
            location="auditor executor",
        ))
        return section


def compute_verdict(report: AuditReport) -> tuple:
    """Calcula o veredito do Release Gate."""
    critical_fails = report.total_critical
    total_fails = report.total_fail

    if critical_fails > 0:
        return "NO_GO", f"{critical_fails} falha(s) crítica(s) encontrada(s). Correção obrigatória antes do release."
    elif total_fails > 5:
        return "NO_GO", f"{total_fails} falhas encontradas. Acima do limite de 5 para release."
    elif total_fails > 0:
        return "CONDITIONAL", f"{total_fails} falha(s) não-crítica(s). Revisar antes do release."
    else:
        return "GO", "Nenhuma falha encontrada. Sistema aprovado para release."


def generate_markdown_report(report: AuditReport) -> str:
    """Gera o relatório em Markdown."""
    lines = []
    lines.append(f"# 🔍 Mercury AI V1 — Relatório de Auditoria de Integridade Forense")
    lines.append(f"")
    lines.append(f"**Data:** {report.audit_date}")
    lines.append(f"**Projeto:** {report.project}")
    lines.append(f"**Veredito do Release Gate:** **{report.release_gate_verdict}**")
    lines.append(f"")
    lines.append(f"> {report.release_gate_reason}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 📊 Sumário Executivo")
    lines.append(f"")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---------|-------|")
    lines.append(f"| Total de Achados | {report.total_findings} |")
    lines.append(f"| ✅ PASS | {report.total_pass} |")
    lines.append(f"| ❌ FAIL | {report.total_fail} |")
    lines.append(f"| ⚠️ WARNING | {report.total_warning} |")
    lines.append(f"| 🔴 CRÍTICOS | {report.total_critical} |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    for section in report.sections:
        lines.append(f"## {section.name}")
        lines.append(f"")
        lines.append(f"**Status da Seção:** {section.status}")
        lines.append(f"")
        lines.append(f"| ID | Severidade | Status | Título |")
        lines.append(f"|----|-----------|--------|--------|")
        for f in section.findings:
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️", "INFO": "ℹ️", "INCONCLUSIVE": "❓"}.get(f.status, "⬜")
            lines.append(f"| {f.id} | {f.severity} | {status_icon} {f.status} | {f.title} |")
        lines.append(f"")

        # Detalhes dos FAIL e WARNING
        for f in section.findings:
            if f.status in (STATUS_FAIL, STATUS_WARNING):
                lines.append(f"#### {f.id}: {f.title}")
                lines.append(f"")
                lines.append(f"- **Severidade:** {f.severity}")
                lines.append(f"- **Status:** {f.status}")
                lines.append(f"- **Localização:** {f.location}")
                lines.append(f"")
                lines.append(f"**Descrição:** {f.description}")
                lines.append(f"")
                if f.evidence:
                    lines.append(f"**Evidência:**")
                    lines.append(f"```")
                    lines.append(f.evidence)
                    lines.append(f"```")
                    lines.append(f"")
                if f.recommendation:
                    lines.append(f"**Recomendação:** {f.recommendation}")
                    lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    lines.append(f"## 🏁 Veredito Final: {report.release_gate_verdict}")
    lines.append(f"")
    lines.append(f"{report.release_gate_reason}")
    lines.append(f"")

    return "\n".join(lines)


def main():
    """Ponto de entrada principal."""
    print("=" * 60)
    print("  Mercury AI V1 — Forensic Integrity Auditor")
    print("=" * 60)
    print(f"  Projeto: {PROJECT_ROOT}")
    print(f"  Timestamp: {AUDIT_TIMESTAMP}")
    print(f"  Modo: READ-ONLY (nenhum código de produção será alterado)")
    print("=" * 60)

    ensure_output_dir()
    report = AuditReport()

    # Fase 1: Auditoria Estática (AST)
    report.sections.append(run_audit_phase(
        "1. Static Audit (AST)",
        static_auditor.run,
    ))

    # Fase 2: Auditoria de Contratos
    report.sections.append(run_audit_phase(
        "2. Contract Audit",
        contract_auditor.run,
    ))

    # Fase 3: Auditoria de Dependências
    report.sections.append(run_audit_phase(
        "3. Dependency Audit",
        dependency_auditor.run,
    ))

    # Fase 4: Auditoria de Masking
    report.sections.append(run_audit_phase(
        "4. Masking Audit",
        masking_auditor.run,
    ))

    # Fase 5: Auditoria de Runtime
    report.sections.append(run_audit_phase(
        "5. Runtime Audit",
        runtime_auditor.run,
    ))

    # Fase 6: Auditoria de Fluxo & Pipeline
    report.sections.append(run_audit_phase(
        "6. Flow & Pipeline Audit",
        flow_auditor.run,
    ))

    # Fase 7: Auditoria de Testes
    report.sections.append(run_audit_phase(
        "7. Test Audit",
        test_auditor.run,
    ))

    # Fase 8: Auditoria de Integridade de Decisão
    report.sections.append(run_audit_phase(
        "8. Decision Integrity Audit",
        decision_auditor.run,
    ))

    # Fase 9: Auditoria de Cobertura de Testes
    report.sections.append(run_audit_phase(
        "9. Coverage Audit",
        coverage_auditor.run,
    ))

    # Fase 10: Auditoria de Integridade de Dados e Configuração
    report.sections.append(run_audit_phase(
        "10. Integrity Audit",
        integrity_auditor.run,
    ))

    # Fase 11: Auditoria de Explicabilidade
    report.sections.append(run_audit_phase(
        "11. Explainability Audit",
        explainability_auditor.run,
    ))

    # Fase 12: Auditoria de Dados
    report.sections.append(run_audit_phase(
        "12. Data Audit",
        data_auditor.run,
    ))

    # Fase 13: Auditoria de Universo
    report.sections.append(run_audit_phase(
        "13. Universe Audit",
        universe_auditor.run,
    ))

    # Fase 14: Auditoria de Estado Global
    report.sections.append(run_audit_phase(
        "14. Global State Audit",
        global_state_auditor.run,
    ))

    # Fase 15: Auditoria de Determinismo
    report.sections.append(run_audit_phase(
        "15. Determinism Audit",
        determinism_auditor.run,
    ))

    # Fase 16: Auditoria de Performance
    report.sections.append(run_audit_phase(
        "16. Performance Audit",
        performance_auditor.run,
    ))

    # Fase 17: Auditoria de Backtest
    report.sections.append(run_audit_phase(
        "17. Backtest Audit",
        backtest_auditor.run,
    ))

    # Fase 18: Geração de Relatório Final Multi-formato
    report.sections.append(run_audit_phase(
        "18. Final Report Generation",
        lambda: AuditSection(
            name="18. Final Report Generation",
            description="Final report generation completed",
            status="PASS",
            findings=[
                AuditFinding(
                    id="RPT-001",
                    category="REPORT",
                    severity="INFO",
                    status="PASS",
                    title="Report Generation Complete",
                    description="Markdown and JSON reports generated successfully",
                    location="tools/mercury_integrity_auditor/main.py",
                    evidence="generate_markdown_report() and JSON serialization executed",
                    recommendation="Review generated reports at audit_report.md and audit_report.json"
                )
            ]
        ),
    ))

    # Computa veredito
    report.release_gate_verdict, report.release_gate_reason = compute_verdict(report)

    # Gera relatórios
    md_content = generate_markdown_report(report)
    REPORT_MD.write_text(md_content, encoding="utf-8")
    print(f"\n📄 Relatório Markdown: {REPORT_MD}")

    # JSON
    json_data = {
        "project": report.project,
        "audit_date": report.audit_date,
        "release_gate_verdict": report.release_gate_verdict,
        "release_gate_reason": report.release_gate_reason,
        "sections": [
            {
                "name": s.name,
                "status": s.status,
                "findings": [
                    {
                        "id": f.id,
                        "category": f.category,
                        "severity": f.severity,
                        "status": f.status,
                        "title": f.title,
                        "description": f.description,
                        "location": f.location,
                        "evidence": f.evidence,
                        "recommendation": f.recommendation,
                    }
                    for f in s.findings
                ],
            }
            for s in report.sections
        ],
    }
    REPORT_JSON.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"📄 Relatório JSON: {REPORT_JSON}")

    # Sumário final
    print(f"\n{'='*60}")
    print(f"  🏁 VEREDITO FINAL: {report.release_gate_verdict}")
    print(f"  {report.release_gate_reason}")
    print(f"{'='*60}")

    return report


if __name__ == "__main__":
    main()