"""
Auditoria de Integridade — Fase 10.
Verifica a integridade dos dados e do sistema:
- Integridade de arquivos de configuração
- Integridade de dados de mercado (JSONs)
- Integridade de modelos serializados
- Checksums e validações de consistência
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.mercury_integrity_auditor.config import (
    PROJECT_ROOT,
    MERCURY_AI_DIR,
    DOT_MERCURY_DIR,
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


def _check_config_integrity() -> list:
    """Verifica integridade dos arquivos de configuração."""
    findings = []
    
    config_files = [
        PROJECT_ROOT / "config.json",
        PROJECT_ROOT / "config_ai.py",
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / "models.json",
    ]
    
    for config_file in config_files:
        if not config_file.exists():
            findings.append(AuditFinding(
                id=f"INT-CFG-{config_file.name.upper()}",
                category="Integrity Audit",
                severity=HIGH,
                status=STATUS_FAIL,
                title=f"Arquivo de configuração ausente: {config_file.name}",
                description=f"Esperado em {config_file}",
                recommendation="Restaurar arquivo de configuração ou criar padrão.",
            ))
            continue
        
        # Verifica se é JSON válido (para .json)
        if config_file.suffix == ".json":
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    json.load(f)
                findings.append(AuditFinding(
                    id=f"INT-CFG-{config_file.name.upper()}",
                    category="Integrity Audit",
                    severity=LOW,
                    status=STATUS_PASS,
                    title=f"Configuração válida: {config_file.name}",
                    description="JSON bem formado e legível.",
                ))
            except json.JSONDecodeError as e:
                findings.append(AuditFinding(
                    id=f"INT-CFG-{config_file.name.upper()}",
                    category="Integrity Audit",
                    severity=CRITICAL,
                    status=STATUS_FAIL,
                    title=f"Configuração inválida: {config_file.name}",
                    description=f"Erro de parsing JSON: {e}",
                    recommendation="Corrigir sintaxe JSON no arquivo de configuração.",
                ))
    
    return findings


def _check_runtime_reports_integrity() -> list:
    """Verifica integridade dos relatórios de runtime (JSONs)."""
    findings = []
    
    runtime_files = list(PROJECT_ROOT.glob("runtime_report_*.json"))
    
    if not runtime_files:
        findings.append(AuditFinding(
            id="INT-RUNTIME-001",
            category="Integrity Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Nenhum relatório de runtime encontrado",
            description="Esperados arquivos runtime_report_*.json na raiz do projeto.",
        ))
        return findings
    
    valid_count = 0
    invalid_count = 0
    empty_count = 0
    schema_errors = 0
    
    expected_keys = {"symbol", "timestamp", "price", "indicators", "decision", "metadata"}
    
    for rf in runtime_files[:100]:  # Limita a 100 arquivos para performance
        try:
            with open(rf, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not data:
                empty_count += 1
                continue
            
            # Verifica schema básico
            if isinstance(data, dict):
                missing_keys = expected_keys - set(data.keys())
                if missing_keys:
                    schema_errors += 1
                else:
                    valid_count += 1
            else:
                schema_errors += 1
                
        except json.JSONDecodeError:
            invalid_count += 1
        except Exception:
            invalid_count += 1
    
    total_checked = valid_count + invalid_count + empty_count + schema_errors
    
    if invalid_count > 0:
        findings.append(AuditFinding(
            id="INT-RUNTIME-002",
            category="Integrity Audit",
            severity=HIGH,
            status=STATUS_FAIL,
            title=f"{invalid_count} relatórios de runtime com JSON inválido",
            description=f"De {total_checked} arquivos verificados, {invalid_count} falharam no parsing.",
            recommendation="Verificar e corrigir arquivos JSON corrompidos.",
        ))
    else:
        findings.append(AuditFinding(
            id="INT-RUNTIME-002",
            category="Integrity Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Todos os relatórios de runtime têm JSON válido",
            description=f"{valid_count} arquivos verificados com sucesso.",
        ))
    
    if empty_count > 0:
        findings.append(AuditFinding(
            id="INT-RUNTIME-003",
            category="Integrity Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{empty_count} relatórios de runtime vazios",
            description="Arquivos JSON existem mas estão vazios ({}).",
        ))
    
    if schema_errors > 0:
        findings.append(AuditFinding(
            id="INT-RUNTIME-004",
            category="Integrity Audit",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"{schema_errors} relatórios com schema incompleto",
            description=f"Chaves esperadas: {expected_keys}. Alguns relatórios faltam campos obrigatórios.",
        ))
    else:
        findings.append(AuditFinding(
            id="INT-RUNTIME-004",
            category="Integrity Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Schema dos relatórios de runtime consistente",
            description=f"Todos os {valid_count} relatórios válidos têm as chaves esperadas.",
        ))
    
    return findings


def _check_dot_mercury_integrity() -> list:
    """Verifica integridade do diretório .mercury (artefatos do Project Mapper)."""
    findings = []
    
    expected_artifacts = [
        "MODULE_INDEX.md",
        "DEPENDENCY_MAP.md",
        "dependency_graph.json",
        "call_graph.json",
        "ARCHITECTURE_AUDIT.md",
        "mercury_snapshot.json",
    ]
    
    missing = []
    for artifact in expected_artifacts:
        if not (DOT_MERCURY_DIR / artifact).exists():
            missing.append(artifact)
    
    if missing:
        findings.append(AuditFinding(
            id="INT-DOTMERCURY-001",
            category="Integrity Audit",
            severity=HIGH,
            status=STATUS_FAIL,
            title=f"{len(missing)} artefatos do Project Mapper ausentes",
            description=f"Arquivos esperados em .mercury/: {', '.join(missing)}",
            recommendation="Executar Project Mapper para gerar artefatos faltantes.",
        ))
    else:
        findings.append(AuditFinding(
            id="INT-DOTMERCURY-001",
            category="Integrity Audit",
            severity=LOW,
            status=STATUS_PASS,
            title="Todos os artefatos do Project Mapper presentes",
            description=f"{len(expected_artifacts)} arquivos verificados em .mercury/.",
        ))
    
    # Verifica se os JSONs são válidos
    for artifact in ["dependency_graph.json", "call_graph.json", "mercury_snapshot.json"]:
        filepath = DOT_MERCURY_DIR / artifact
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    json.load(f)
                findings.append(AuditFinding(
                    id=f"INT-DOTMERCURY-{artifact.upper()}",
                    category="Integrity Audit",
                    severity=LOW,
                    status=STATUS_PASS,
                    title=f"Artefato válido: {artifact}",
                    description="JSON bem formado.",
                ))
            except json.JSONDecodeError as e:
                findings.append(AuditFinding(
                    id=f"INT-DOTMERCURY-{artifact.upper()}",
                    category="Integrity Audit",
                    severity=HIGH,
                    status=STATUS_FAIL,
                    title=f"Artefato corrompido: {artifact}",
                    description=f"Erro JSON: {e}",
                ))
    
    return findings


def _check_models_integrity() -> list:
    """Verifica integridade do arquivo models.json."""
    findings = []
    
    models_file = PROJECT_ROOT / "models.json"
    if not models_file.exists():
        findings.append(AuditFinding(
            id="INT-MODELS-001",
            category="Integrity Audit",
            severity=HIGH,
            status=STATUS_FAIL,
            title="models.json não encontrado",
            description="Arquivo de definição de modelos ausente.",
        ))
        return findings
    
    try:
        with open(models_file, "r", encoding="utf-8") as f:
            models = json.load(f)
        
        if not isinstance(models, dict):
            findings.append(AuditFinding(
                id="INT-MODELS-002",
                category="Integrity Audit",
                severity=HIGH,
                status=STATUS_FAIL,
                title="models.json tem estrutura inválida",
                description="Esperado objeto/dicionário no nível superior.",
            ))
            return findings
        
        model_count = len(models)
        findings.append(AuditFinding(
            id="INT-MODELS-001",
            category="Integrity Audit",
            severity=LOW,
            status=STATUS_PASS,
            title=f"models.json válido com {model_count} modelos",
            description="Estrutura JSON correta.",
        ))
        
        # Verifica se cada modelo tem campos esperados
        expected_model_keys = {"type", "params", "version"}
        incomplete = 0
        for name, model in models.items():
            if not isinstance(model, dict):
                incomplete += 1
                continue
            missing = expected_model_keys - set(model.keys())
            if missing:
                incomplete += 1
        
        if incomplete > 0:
            findings.append(AuditFinding(
                id="INT-MODELS-003",
                category="Integrity Audit",
                severity=MEDIUM,
                status=STATUS_WARNING,
                title=f"{incomplete} modelos com campos incompletos",
                description=f"Campos esperados: {expected_model_keys}",
            ))
        else:
            findings.append(AuditFinding(
                id="INT-MODELS-003",
                category="Integrity Audit",
                severity=LOW,
                status=STATUS_PASS,
                title="Todos os modelos têm campos completos",
                description=f"Verificados {model_count} modelos.",
            ))
            
    except json.JSONDecodeError as e:
        findings.append(AuditFinding(
            id="INT-MODELS-002",
            category="Integrity Audit",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="models.json corrompido",
            description=f"Erro JSON: {e}",
        ))
    
    return findings


def _check_checksums() -> list:
    """Verifica checksums de arquivos críticos."""
    findings = []
    
    critical_files = [
        PROJECT_ROOT / "config.json",
        PROJECT_ROOT / "main.py",
        PROJECT_ROOT / "requirements.txt",
    ]
    
    for cf in critical_files:
        if cf.exists():
            try:
                content = cf.read_bytes()
                sha256 = hashlib.sha256(content).hexdigest()[:16]
                findings.append(AuditFinding(
                    id=f"INT-CHECKSUM-{cf.name.upper()}",
                    category="Integrity Audit",
                    severity=LOW,
                    status=STATUS_INFO,
                    title=f"Checksum {cf.name}: {sha256}",
                    description=f"SHA256 (primeiros 16 chars): {sha256}",
                ))
            except Exception as e:
                findings.append(AuditFinding(
                    id=f"INT-CHECKSUM-{cf.name.upper()}",
                    category="Integrity Audit",
                    severity=MEDIUM,
                    status=STATUS_WARNING,
                    title=f"Falha ao calcular checksum de {cf.name}",
                    description=str(e),
                ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de integridade."""
    section = AuditSection(
        name="10. Integrity Audit",
        description="Verificação da integridade de configurações, dados e artefatos",
    )
    
    # 1. Configurações
    print("  Verificando integridade de configurações...")
    section.findings.extend(_check_config_integrity())
    
    # 2. Relatórios de runtime
    print("  Verificando integridade de relatórios de runtime...")
    section.findings.extend(_check_runtime_reports_integrity())
    
    # 3. Artefatos .mercury
    print("  Verificando artefatos do Project Mapper...")
    section.findings.extend(_check_dot_mercury_integrity())
    
    # 4. Models.json
    print("  Verificando models.json...")
    section.findings.extend(_check_models_integrity())
    
    # 5. Checksums
    print("  Calculando checksums...")
    section.findings.extend(_check_checksums())
    
    # Determina status da seção
    if any(f.status == STATUS_FAIL for f in section.findings):
        section.status = "FAIL"
    elif any(f.status == STATUS_WARNING for f in section.findings):
        section.status = "WARNING"
    else:
        section.status = "PASS"
    
    return section