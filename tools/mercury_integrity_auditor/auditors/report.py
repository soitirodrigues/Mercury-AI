"""
Módulo de Geração de Relatórios — Fase 18.
Gera relatórios finais abrangentes em múltiplos formatos:
- Markdown detalhado
- JSON estruturado
- HTML para visualização
- Resumo executivo
- Métricas consolidadas
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.mercury_integrity_auditor.config import (
    PROJECT_ROOT,
    AUDIT_OUTPUT_DIR,
    AUDIT_TIMESTAMP,
)
from tools.mercury_integrity_auditor.models import AuditFinding, AuditReport, AuditSection


def generate_html_report(report: AuditReport) -> str:
    """Gera relatório em HTML."""
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='pt-BR'>")
    html.append("<head>")
    html.append("    <meta charset='UTF-8'>")
    html.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html.append(f"    <title>Mercury AI V1 - Auditoria de Integridade Forense</title>")
    html.append("    <style>")
    html.append("        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }")
    html.append("        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }")
    html.append("        h1 { color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; }")
    html.append("        h2 { color: #16213e; border-left: 4px solid #e94560; padding-left: 15px; }")
    html.append("        h3 { color: #0f3460; }")
    html.append("        .verdict { padding: 20px; border-radius: 8px; margin: 20px 0; font-weight: bold; font-size: 1.2em; text-align: center; }")
    html.append("        .verdict.GO { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }")
    html.append("        .verdict.NO_GO { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }")
    html.append("        .verdict.CONDITIONAL { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }")
    html.append("        .verdict.PENDING { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }")
    html.append("        table { width: 100%; border-collapse: collapse; margin: 15px 0; }")
    html.append("        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }")
    html.append("        th { background: #1a1a2e; color: white; }")
    html.append("        tr:hover { background: #f8f9fa; }")
    html.append("        .status-PASS { color: #28a745; font-weight: bold; }")
    html.append("        .status-FAIL { color: #dc3545; font-weight: bold; }")
    html.append("        .status-WARNING { color: #ffc107; font-weight: bold; }")
    html.append("        .status-INFO { color: #17a2b8; font-weight: bold; }")
    html.append("        .status-INCONCLUSIVE { color: #6c757d; font-weight: bold; }")
    html.append("        .severity-CRITICAL { background: #f8d7da; }")
    html.append("        .severity-HIGH { background: #fff3cd; }")
    html.append("        .severity-MEDIUM { background: #d1ecf1; }")
    html.append("        .severity-LOW { background: #d4edda; }")
    html.append("        .finding { margin: 15px 0; padding: 15px; border-radius: 4px; border-left: 4px solid #e94560; background: #fafafa; }")
    html.append("        .finding-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }")
    html.append("        .finding-id { font-family: monospace; font-weight: bold; }")
    html.append("        .evidence { background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 0.9em; overflow-x: auto; }")
    html.append("        .summary-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }")
    html.append("        .card { padding: 20px; border-radius: 8px; text-align: center; }")
    html.append("        .card.total { background: #1a1a2e; color: white; }")
    html.append("        .card.pass { background: #d4edda; color: #155724; }")
    html.append("        .card.fail { background: #f8d7da; color: #721c24; }")
    html.append("        .card.warning { background: #fff3cd; color: #856404; }")
    html.append("        .card.critical { background: #f5c6cb; color: #721c24; }")
    html.append("        .card-value { font-size: 2.5em; font-weight: bold; }")
    html.append("        .card-label { font-size: 0.9em; opacity: 0.8; }")
    html.append("        pre { background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }")
    html.append("        code { font-family: 'Monaco', 'Consolas', monospace; }")
    html.append("        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 0.9em; }")
    html.append("    </style>")
    html.append("</head>")
    html.append("<body>")
    html.append("    <div class='container'>")
    
    # Header
    html.append(f"        <h1>🔍 Mercury AI V1 — Relatório de Auditoria de Integridade Forense</h1>")
    html.append(f"        <p><strong>Data:</strong> {report.audit_date}</p>")
    html.append(f"        <p><strong>Projeto:</strong> {report.project}</p>")
    
    # Verdict
    verdict_class = report.release_gate_verdict
    html.append(f"        <div class='verdict {verdict_class}'>")
    html.append(f"            Veredito do Release Gate: {report.release_gate_verdict}")
    html.append(f"        </div>")
    html.append(f"        <p style='text-align: center;'>{report.release_gate_reason}</p>")
    
    # Summary Cards
    html.append("        <div class='summary-cards'>")
    html.append(f"            <div class='card total'><div class='card-value'>{report.total_findings}</div><div class='card-label'>Total de Achados</div></div>")
    html.append(f"            <div class='card pass'><div class='card-value'>{report.total_pass}</div><div class='card-label'>✅ PASS</div></div>")
    html.append(f"            <div class='card fail'><div class='card-value'>{report.total_fail}</div><div class='card-label'>❌ FAIL</div></div>")
    html.append(f"            <div class='card warning'><div class='card-value'>{report.total_warning}</div><div class='card-label'>⚠️ WARNING</div></div>")
    html.append(f"            <div class='card critical'><div class='card-value'>{report.total_critical}</div><div class='card-label'>🔴 CRÍTICOS</div></div>")
    html.append("        </div>")
    
    # Sections
    for section in report.sections:
        html.append(f"        <h2>{section.name}</h2>")
        html.append(f"        <p><strong>Status da Seção:</strong> <span class='status-{section.status}'>{section.status}</span></p>")
        html.append(f"        <p>{section.description}</p>")
        
        # Table
        html.append("        <table>")
        html.append("            <thead>")
        html.append("                <tr>")
        html.append("                    <th>ID</th>")
        html.append("                    <th>Severidade</th>")
        html.append("                    <th>Status</th>")
        html.append("                    <th>Título</th>")
        html.append("                </tr>")
        html.append("            </thead>")
        html.append("            <tbody>")
        
        for f in section.findings:
            status_class = f"status-{f.status}"
            severity_class = f"severity-{f.severity}"
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️", "INFO": "ℹ️", "INCONCLUSIVE": "❓"}.get(f.status, "⬜")
            html.append(f"                <tr class='{severity_class}'>")
            html.append(f"                    <td class='finding-id'>{f.id}</td>")
            html.append(f"                    <td>{f.severity}</td>")
            html.append(f"                    <td class='{status_class}'>{status_icon} {f.status}</td>")
            html.append(f"                    <td>{f.title}</td>")
            html.append(f"                </tr>")
        
        html.append("            </tbody>")
        html.append("        </table>")
        
        # Details for FAIL and WARNING
        for f in section.findings:
            if f.status in ("FAIL", "WARNING"):
                html.append(f"        <div class='finding'>")
                html.append(f"            <div class='finding-header'>")
                html.append(f"                <span class='finding-id'>{f.id}</span>")
                html.append(f"                <span class='status-{f.status}'>{f.status}</span>")
                html.append(f"            </div>")
                html.append(f"            <h3>{f.title}</h3>")
                html.append(f"            <p><strong>Severidade:</strong> {f.severity}</p>")
                html.append(f"            <p><strong>Localização:</strong> {f.location or 'N/A'}</p>")
                html.append(f"            <p><strong>Descrição:</strong> {f.description}</p>")
                if f.evidence:
                    html.append(f"            <p><strong>Evidência:</strong></p>")
                    html.append(f"            <div class='evidence'>{f.evidence}</div>")
                if f.recommendation:
                    html.append(f"            <p><strong>Recomendação:</strong> {f.recommendation}</p>")
                html.append(f"        </div>")
    
    # Footer
    html.append("        <div class='footer'>")
    html.append(f"            <p>Relatório gerado em {datetime.now().isoformat()}</p>")
    html.append(f"            <p>Mercury AI V1 — Forensic Integrity Auditor</p>")
    html.append("        </div>")
    
    html.append("    </div>")
    html.append("</body>")
    html.append("</html>")
    
    return "\n".join(html)


def generate_executive_summary(report: AuditReport) -> str:
    """Gera resumo executivo em Markdown."""
    lines = []
    lines.append("# 📋 Resumo Executivo — Mercury AI V1 Auditoria Forense")
    lines.append("")
    lines.append(f"**Data:** {report.audit_date}")
    lines.append(f"**Projeto:** {report.project}")
    lines.append(f"**Veredito:** **{report.release_gate_verdict}**")
    lines.append("")
    lines.append(f"> {report.release_gate_reason}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Métricas Principais")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Total de Achados | {report.total_findings} |")
    lines.append(f"| ✅ PASS | {report.total_pass} |")
    lines.append(f"| ❌ FAIL | {report.total_fail} |")
    lines.append(f"| ⚠️ WARNING | {report.total_warning} |")
    lines.append(f"| 🔴 CRÍTICOS | {report.total_critical} |")
    lines.append("")
    
    # Top issues
    critical_fails = [f for s in report.sections for f in s.findings if f.severity == "CRITICAL" and f.status == "FAIL"]
    high_fails = [f for s in report.sections for f in s.findings if f.severity == "HIGH" and f.status == "FAIL"]
    
    if critical_fails:
        lines.append("## 🔴 Falhas Críticas (Ação Imediata)")
        lines.append("")
        for f in critical_fails:
            lines.append(f"- **{f.id}**: {f.title}")
            lines.append(f"  - {f.description}")
            if f.recommendation:
                lines.append(f"  - *Ação:* {f.recommendation}")
        lines.append("")
    
    if high_fails:
        lines.append("## 🟠 Falhas de Alta Severidade")
        lines.append("")
        for f in high_fails[:10]:  # Limita a 10
            lines.append(f"- **{f.id}**: {f.title}")
            lines.append(f"  - {f.description}")
        lines.append("")
    
    # Section summary
    lines.append("## 📑 Resumo por Seção")
    lines.append("")
    lines.append("| Seção | Status | PASS | FAIL | WARN | INFO |")
    lines.append("|-------|--------|------|------|------|------|")
    for section in report.sections:
        lines.append(f"| {section.name} | {section.status} | {section.pass_count} | {section.fail_count} | {section.warning_count} | {section.info_count} |")
    lines.append("")
    
    return "\n".join(lines)


def generate_consolidated_metrics(report: AuditReport) -> dict:
    """Gera métricas consolidadas para análise programática."""
    metrics = {
        "audit_date": report.audit_date,
        "project": report.project,
        "verdict": report.release_gate_verdict,
        "verdict_reason": report.release_gate_reason,
        "totals": {
            "findings": report.total_findings,
            "pass": report.total_pass,
            "fail": report.total_fail,
            "warning": report.total_warning,
            "critical": report.total_critical,
        },
        "by_severity": {
            "CRITICAL": sum(1 for s in report.sections for f in s.findings if f.severity == "CRITICAL"),
            "HIGH": sum(1 for s in report.sections for f in s.findings if f.severity == "HIGH"),
            "MEDIUM": sum(1 for s in report.sections for f in s.findings if f.severity == "MEDIUM"),
            "LOW": sum(1 for s in report.sections for f in s.findings if f.severity == "LOW"),
        },
        "by_status": {
            "PASS": report.total_pass,
            "FAIL": report.total_fail,
            "WARNING": report.total_warning,
            "INFO": sum(1 for s in report.sections for f in s.findings if f.status == "INFO"),
            "INCONCLUSIVE": sum(1 for s in report.sections for f in s.findings if f.status == "INCONCLUSIVE"),
        },
        "sections": [
            {
                "name": s.name,
                "status": s.status,
                "pass": s.pass_count,
                "fail": s.fail_count,
                "warning": s.warning_count,
                "info": s.info_count,
                "inconclusive": s.inconclusive_count,
            }
            for s in report.sections
        ],
        "critical_findings": [
            {
                "id": f.id,
                "section": s.name,
                "title": f.title,
                "description": f.description,
                "recommendation": f.recommendation,
            }
            for s in report.sections
            for f in s.findings
            if f.severity == "CRITICAL" and f.status == "FAIL"
        ],
    }
    return metrics


def save_all_reports(report: AuditReport, output_dir: Path = None) -> dict:
    """Salva todos os formatos de relatório."""
    if output_dir is None:
        output_dir = AUDIT_OUTPUT_DIR
    
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = AUDIT_TIMESTAMP
    
    saved_files = {}
    
    # 1. Markdown (já gerado no main.py, mas podemos salvar versão estendida)
    md_file = output_dir / f"MERCURY_INTEGRITY_AUDIT_{timestamp}_FULL.md"
    # O markdown principal já é salvo pelo main.py
    
    # 2. HTML
    html_content = generate_html_report(report)
    html_file = output_dir / f"MERCURY_INTEGRITY_AUDIT_{timestamp}.html"
    html_file.write_text(html_content, encoding="utf-8")
    saved_files["html"] = str(html_file)
    
    # 3. Resumo Executivo
    exec_summary = generate_executive_summary(report)
    exec_file = output_dir / f"MERCURY_INTEGRITY_AUDIT_{timestamp}_EXECUTIVE.md"
    exec_file.write_text(exec_summary, encoding="utf-8")
    saved_files["executive_summary"] = str(exec_file)
    
    # 4. Métricas Consolidadas (JSON)
    metrics = generate_consolidated_metrics(report)
    metrics_file = output_dir / f"MERCURY_INTEGRITY_AUDIT_{timestamp}_METRICS.json"
    metrics_file.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    saved_files["metrics"] = str(metrics_file)
    
    # 5. JSON completo (já salvo pelo main.py)
    
    return saved_files


def run(report: AuditReport = None) -> AuditSection:
    """
    Executa a geração de relatórios.
    Se report for fornecido, gera os relatórios adicionais.
    Retorna uma seção de auditoria com o status da geração.
    """
    section = AuditSection(
        name="18. Report Generation",
        description="Geração de relatórios finais em múltiplos formatos",
    )
    
    if report is None:
        section.findings.append(AuditFinding(
            id="REPORT-001",
            category="Report Generation",
            severity=HIGH,
            status=STATUS_FAIL,
            title="Nenhum relatório de auditoria fornecido",
            description="O módulo de relatório requer um objeto AuditReport para gerar os outputs.",
        ))
        section.status = "FAIL"
        return section
    
    try:
        print("  Gerando relatório HTML...")
        print("  Gerando resumo executivo...")
        print("  Gerando métricas consolidadas...")
        
        saved = save_all_reports(report)
        
        section.findings.append(AuditFinding(
            id="REPORT-001",
            category="Report Generation",
            severity=LOW,
            status=STATUS_PASS,
            title="Relatórios gerados com sucesso",
            description=f"Arquivos criados: {', '.join(saved.keys())}",
            evidence="\n".join(f"{k}: {v}" for k, v in saved.items()),
        ))
        
        section.status = "PASS"
        
    except Exception as e:
        section.findings.append(AuditFinding(
            id="REPORT-001",
            category="Report Generation",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="Falha na geração de relatórios",
            description=str(e),
        ))
        section.status = "FAIL"
    
    return section