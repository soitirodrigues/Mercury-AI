"""
Modelos de dados para o relatório de auditoria.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class AuditFinding:
    """Um achado individual da auditoria."""
    id: str
    category: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str  # PASS, FAIL, INCONCLUSIVE, WARNING, INFO
    title: str
    description: str
    location: str = ""
    evidence: str = ""
    recommendation: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AuditSection:
    """Uma seção do relatório de auditoria."""
    name: str
    description: str
    findings: list = field(default_factory=list)
    status: str = "PENDING"  # PENDING, PASS, FAIL, WARNING

    @property
    def pass_count(self) -> int:
        return sum(1 for f in self.findings if f.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for f in self.findings if f.status == "FAIL")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.status == "WARNING")

    @property
    def info_count(self) -> int:
        return sum(1 for f in self.findings if f.status == "INFO")

    @property
    def inconclusive_count(self) -> int:
        return sum(1 for f in self.findings if f.status == "INCONCLUSIVE")


@dataclass
class AuditReport:
    """Relatório completo da auditoria."""
    project: str = "Mercury AI V1"
    audit_date: str = field(default_factory=lambda: datetime.now().isoformat())
    sections: list = field(default_factory=list)
    release_gate_verdict: str = "PENDING"  # GO / NO_GO / CONDITIONAL
    release_gate_reason: str = ""

    @property
    def total_findings(self) -> int:
        return sum(len(s.findings) for s in self.sections)

    @property
    def total_pass(self) -> int:
        return sum(s.pass_count for s in self.sections)

    @property
    def total_fail(self) -> int:
        return sum(s.fail_count for s in self.sections)

    @property
    def total_warning(self) -> int:
        return sum(s.warning_count for s in self.sections)

    @property
    def total_critical(self) -> int:
        return sum(1 for s in self.sections for f in s.findings if f.severity == "CRITICAL" and f.status == "FAIL")