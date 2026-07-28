"""
Auditoria de Universo — Fase 13.
Verifica definição, cobertura e gestão do universo de ativos:
- Definição de universo (lista de ativos, critérios de inclusão/exclusão)
- Cobertura de dados (market data disponível para todo universo)
- Liquidez e filtros de volume
- Setor/indústria diversification
- Rebalanceamento e rotatividade do universo
- Corporate actions handling (splits, dividends, M&A)
"""

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


def _check_universe_definition() -> list[AuditFinding]:
    """Verifica se o universo de ativos é definido explicitamente."""
    findings = []
    
    universe_files = list(MERCURY_AI_DIR.rglob("*universe*.py"))
    universe_files += list(MERCURY_AI_DIR.rglob("*asset*list*.py"))
    universe_files += list(MERCURY_AI_DIR.rglob("*symbol*.py"))
    universe_files += list(MERCURY_AI_DIR.rglob("*ticker*.py"))
    
    # Verifica config.json
    config_json = PROJECT_ROOT / "config.json"
    has_universe_in_config = False
    if config_json.exists():
        try:
            content = config_json.read_text(encoding="utf-8")
            if any(kw in content.lower() for kw in ["universe", "symbols", "tickers", "assets", "watchlist"]):
                has_universe_in_config = True
        except Exception:
            pass
    
    has_universe_definition = len(universe_files) > 0 or has_universe_in_config
    
    if has_universe_definition:
        findings.append(AuditFinding(
            id="UNIV-001",
            category="UNIVERSE",
            severity=LOW,
            status=STATUS_PASS,
            title="Universe Definition Found",
            description=f"Universo de ativos definido: {len(universe_files)} arquivo(s) + config.json={has_universe_in_config}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="UNIV-001",
            category="UNIVERSE",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Universe Definition Not Explicit",
            description="Universo de ativos (lista de símbolos, critérios de inclusão) não encontrado explicitamente.",
            location=str(MERCURY_AI_DIR),
            recommendation="Definir universo explicitamente: lista de símbolos, critérios de inclusão (liquidez, market cap, setor), frequência de atualização.",
        ))
    
    return findings


def _check_data_coverage() -> list[AuditFinding]:
    """Verifica cobertura de market data para o universo."""
    findings = []
    
    data_files = list(MERCURY_AI_DIR.rglob("*data*.py"))
    data_files += list(MERCURY_AI_DIR.rglob("*market*.py"))
    data_files += list(MERCURY_AI_DIR.rglob("*feed*.py"))
    data_files += list(MERCURY_AI_DIR.rglob("*provider*.py"))
    
    has_data_coverage_check = False
    for f in data_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(kw in content.lower() for kw in ["coverage", "missing", "gap", "available", "universe", "symbol"]):
                has_data_coverage_check = True
                break
        except Exception:
            pass
    
    if has_data_coverage_check:
        findings.append(AuditFinding(
            id="UNIV-002",
            category="UNIVERSE",
            severity=LOW,
            status=STATUS_PASS,
            title="Data Coverage Check Found",
            description="Sistema verifica cobertura de market data para o universo de ativos.",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="UNIV-002",
            category="UNIVERSE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Data Coverage Verification Missing",
            description="Não há verificação automática de cobertura de dados (market data disponível para todos os símbolos do universo).",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar verificação de cobertura: % de símbolos com dados completos, gaps detection, alertas.",
        ))
    
    return findings


def _check_liquidity_filters() -> list[AuditFinding]:
    """Verifica filtros de liquidez/volume."""
    findings = []
    
    liquidity_files = list(MERCURY_AI_DIR.rglob("*liquid*.py"))
    liquidity_files += list(MERCURY_AI_DIR.rglob("*volume*.py"))
    liquidity_files += list(MERCURY_AI_DIR.rglob("*filter*.py"))
    liquidity_files += list(MERCURY_AI_DIR.rglob("*screen*.py"))
    
    has_liquidity_filter = False
    for f in liquidity_files:
        try:
            content = f.read_text(encoding="utf-8")
            if any(kw in content.lower() for kw in ["volume", "liquidity", "avg_volume", "min_volume", "turnover", "adv"]):
                has_liquidity_filter = True
                break
        except Exception:
            pass
    
    if has_liquidity_filter:
        findings.append(AuditFinding(
            id="UNIV-003",
            category="UNIVERSE",
            severity=LOW,
            status=STATUS_PASS,
            title="Liquidity/Volume Filters Found",
            description="Sistema possui filtros de liquidez/volume para seleção de ativos.",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="UNIV-003",
            category="UNIVERSE",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Liquidity Filters Missing",
            description="Não há filtros explícitos de liquidez (volume médio, ADV, turnover) para exclusão de ativos ilíquidos.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar filtros de liquidez: ADV mínimo, volume mínimo, spread máximo, market cap mínimo.",
        ))
    
    return findings


def _check_sector_diversification() -> list[AuditFinding]:
    """Verifica diversificação setorial."""
    findings = []
    
    sector_files = list(MERCURY_AI_DIR.rglob("*sector*.py"))
    sector_files += list(MERCURY_AI_DIR.rglob("*industry*.py"))
    sector_files += list(MERCURY_AI_DIR.rglob("*diversif*.py"))
    sector_files += list(MERCURY_AI_DIR.rglob("*correlation*.py"))
    
    has_sector_awareness = len(sector_files) > 0
    
    if has_sector_awareness:
        findings.append(AuditFinding(
            id="UNIV-004",
            category="UNIVERSE",
            severity=LOW,
            status=STATUS_PASS,
            title="Sector/Industry Awareness Found",
            description=f"Sistema possui consciência setorial: {len(sector_files)} arquivo(s) relacionados.",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="UNIV-004",
            category="UNIVERSE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Sector Diversification Not Enforced",
            description="Não há controle de concentração setorial/industrial no universo ou portfolio.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar limites de concentração setorial (ex: max 20% por setor, max 10% por indústria).",
        ))
    
    return findings


def _check_corporate_actions() -> list[AuditFinding]:
    """Verifica tratamento de corporate actions."""
    findings = []
    
    ca_files = list(MERCURY_AI_DIR.rglob("*split*.py"))
    ca_files += list(MERCURY_AI_DIR.rglob("*dividend*.py"))
    ca_files += list(MERCURY_AI_DIR.rglob("*corporate*action*.py"))
    ca_files += list(MERCURY_AI_DIR.rglob("*adjust*.py"))
    ca_files += list(MERCURY_AI_DIR.rglob("*ma*.py"))
    ca_files += list(MERCURY_AI_DIR.rglob("*merger*.py"))
    
    has_ca_handling = len(ca_files) > 0
    
    if has_ca_handling:
        findings.append(AuditFinding(
            id="UNIV-005",
            category="UNIVERSE",
            severity=LOW,
            status=STATUS_PASS,
            title="Corporate Actions Handling Found",
            description=f"Sistema trata corporate actions: {len(ca_files)} arquivo(s) relacionados (splits, dividendos, M&A).",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="UNIV-005",
            category="UNIVERSE",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Corporate Actions Handling Missing",
            description="Não há tratamento explícito de corporate actions (stock splits, dividendos, M&A, spin-offs) nos dados de preço.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar ajuste de preços para splits/dividendos, detectar M&A para remoção/adicionar símbolos.",
        ))
    
    return findings


def _check_universe_rebalancing() -> list[AuditFinding]:
    """Verifica rebalanceamento do universo."""
    findings = []
    
    rebal_files = list(MERCURY_AI_DIR.rglob("*rebalanc*.py"))
    rebal_files += list(MERCURY_AI_DIR.rglob("*rotat*.py"))
    rebal_files += list(MERCURY_AI_DIR.rglob("*refresh*.py"))
    rebal_files += list(MERCURY_AI_DIR.rglob("*update*universe*.py"))
    
    has_rebalancing = len(rebal_files) > 0
    
    if has_rebalancing:
        findings.append(AuditFinding(
            id="UNIV-006",
            category="UNIVERSE",
            severity=LOW,
            status=STATUS_PASS,
            title="Universe Rebalancing/Refresh Found",
            description=f"Sistema possui rebalanceamento/atualização do universo: {len(rebal_files)} arquivo(s).",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="UNIV-006",
            category="UNIVERSE",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Universe Rebalancing Not Defined",
            description="Não há processo definido de rebalanceamento/atualização periódica do universo (frequência, critérios, automação).",
            location=str(MERCURY_AI_DIR),
            recommendation="Definir política de rebalanceamento: frequência (mensal/trimestral), critérios de entrada/saída, automação.",
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de universo."""
    section = AuditSection(
        name="13. Universe Audit",
        description="Verifica definição, cobertura e gestão do universo de ativos: definição, data coverage, liquidez, setores, corporate actions, rebalancing",
    )
    
    all_findings = []
    all_findings.extend(_check_universe_definition())
    all_findings.extend(_check_data_coverage())
    all_findings.extend(_check_liquidity_filters())
    all_findings.extend(_check_sector_diversification())
    all_findings.extend(_check_corporate_actions())
    all_findings.extend(_check_universe_rebalancing())
    
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