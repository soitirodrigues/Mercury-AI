import json
import os

import pytest
from mercury_ai.core.security_center import SecurityCenter


def test_security_center_functionality():
    sc = SecurityCenter(state_path="")  # in-memory only

    # Log events
    sc.log_event("admin", "LOGIN", "System", "INFO")
    sc.log_event("scanner", "SCAN", "Provider", "INFO")
    sc.log_event("admin", "DELETE", "Snapshot", "CRITICAL")

    # Audit Trail check
    trail = sc.generate_audit_trail()
    assert len(trail) == 3
    assert trail[2]["severity"] == "CRITICAL"

    # Security Report check
    report = sc.generate_security_report()
    assert report["total_events"] == 3
    assert report["critical_events"] == 1
    assert report["status"] == "WARNING"


def test_persistence_roundtrip(tmp_path):
    """Eventos logados são persistidos e recarregados em uma nova instância."""
    state_file = str(tmp_path / "audit_trail.json")

    sc1 = SecurityCenter(state_path=state_file)
    sc1.log_event("admin", "LOGIN", "System", "INFO")
    sc1.log_event("admin", "DELETE", "Snapshot", "CRITICAL")

    # Arquivo foi criado em disco
    assert os.path.exists(state_file)

    # Nova instância carrega o trail do disco
    sc2 = SecurityCenter(state_path=state_file)
    trail = sc2.generate_audit_trail()
    assert len(trail) == 2
    assert trail[0]["action"] == "LOGIN"
    assert trail[1]["severity"] == "CRITICAL"


def test_load_on_init(tmp_path):
    """SecurityCenter carrega eventos pré-existentes do disco na inicialização."""
    state_file = str(tmp_path / "audit_trail.json")

    # Escreve um trail pré-existente manualmente
    pre_existing = [
        {"user": "scanner", "action": "SCAN", "target": "Provider", "severity": "INFO", "timestamp": "2026-01-01T00:00:00"},
        {"user": "admin", "action": "CONFIG", "target": "System", "severity": "WARNING", "timestamp": "2026-01-01T00:01:00"},
    ]
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(pre_existing, f)

    sc = SecurityCenter(state_path=state_file)
    trail = sc.generate_audit_trail()
    assert len(trail) == 2
    assert trail[0]["user"] == "scanner"
    assert trail[1]["severity"] == "WARNING"


def test_save_on_log_event(tmp_path):
    """Cada log_event persiste imediatamente em disco."""
    state_file = str(tmp_path / "audit_trail.json")

    sc = SecurityCenter(state_path=state_file)
    sc.log_event("admin", "LOGIN", "System", "INFO")

    # Lê o arquivo diretamente para confirmar persistência
    with open(state_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["action"] == "LOGIN"


def test_empty_state_path_in_memory(tmp_path):
    """state_path='' mantém comportamento in-memory sem tocar disco."""
    # Usa subdiretório próprio para evitar conflito com backups do conftest
    work_dir = tmp_path / "sc_work"
    work_dir.mkdir()
    sc = SecurityCenter(state_path="")
    sc.log_event("admin", "LOGIN", "System", "INFO")
    assert len(sc.generate_audit_trail()) == 1
    # Nenhum arquivo de audit trail criado no diretório de trabalho
    assert len(list(work_dir.iterdir())) == 0


def test_corrupted_file_starts_empty(tmp_path):
    """Arquivo corrompido resulta em trail vazio, sem exceção."""
    state_file = str(tmp_path / "audit_trail.json")
    with open(state_file, "w", encoding="utf-8") as f:
        f.write("{not valid json")

    sc = SecurityCenter(state_path=state_file)
    assert len(sc.generate_audit_trail()) == 0


def test_thread_safety(tmp_path):
    """log_event concorrente não perde eventos nem corrompe o arquivo."""
    state_file = str(tmp_path / "audit_trail.json")
    sc = SecurityCenter(state_path=state_file)

    import threading

    def log_many():
        for i in range(50):
            sc.log_event("user", f"ACTION_{i}", "target", "INFO")

    threads = [threading.Thread(target=log_many) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    trail = sc.generate_audit_trail()
    assert len(trail) == 200  # 4 threads × 50 eventos
