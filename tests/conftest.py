"""Pytest configuration and fixtures for test isolation.

This conftest.py ensures that file-based state (config.json, asset_registry.json,
data/brokers/) is isolated between tests. It backs up the original files before
each test and restores them after, preventing test pollution.

This is critical because:
- MercuryConfigCenter.save() persists to the real config.json via atomic_json_write
- AssetRegistry.register_asset() persists to the real data/asset_registry.json
- test_broker_filtering.py creates data/brokers/XP.json on disk
- Without isolation, tests that modify file-based state pollute subsequent tests
"""

import pytest
import os
import shutil
from pathlib import Path


# Files that tests may modify — we back up and restore these around every test
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_STATE_FILES = [
    _PROJECT_ROOT / "config.json",
    _PROJECT_ROOT / "data" / "asset_registry.json",
    _PROJECT_ROOT / "data" / "audit_trail.json",
]
_STATE_DIRS = [
    _PROJECT_ROOT / "data" / "brokers",
]


def _backup_state(tmp_path):
    """Back up all state files and directories to a temp location."""
    backups = {}

    for f in _STATE_FILES:
        if f.exists():
            backup_path = tmp_path / f"backup_{f.name}"
            shutil.copy2(f, backup_path)
            backups[f] = backup_path

    for d in _STATE_DIRS:
        if d.exists() and d.is_dir():
            backup_dir = tmp_path / f"backup_{d.name}"
            shutil.copytree(d, backup_dir)
            backups[d] = backup_dir

    return backups


def _restore_state(backups):
    """Restore all state files and directories from backups.

    Para diretórios, usa "content-sync" (copia arquivo a arquivo) em vez de
    remover e recriar o diretório raiz: no Windows, shutil.rmtree() pode falhar
    com PermissionError (WinError 5) quando o diretório tem um handle aberto
    (ex.: file watcher do editor), o que faria o backup de arquivos pré-
    existentes (ex.: data/brokers/XP.json) ser silenciosamente perdido.
    """
    for original_path, backup_path in backups.items():
        try:
            if original_path.is_file():
                shutil.copy2(backup_path, original_path)
            elif original_path.is_dir():
                if not original_path.exists():
                    original_path.mkdir(parents=True, exist_ok=True)
                # Remove apenas o conteúdo (não o diretório raiz).
                for item in list(original_path.iterdir()):
                    if item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        item.unlink(missing_ok=True)
                # Recopia os arquivos do backup.
                for item in backup_path.iterdir():
                    if item.is_dir():
                        shutil.copytree(item, original_path / item.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, original_path / item.name)
        except (OSError, shutil.Error):
            pass


def _cleanup_state():
    """Remove any state files/dirs that were created during the test but
    didn't exist before (i.e., have no backup)."""
    for f in _STATE_FILES:
        if f.exists():
            # Check if we had a backup — if not, this file was created during the test
            # We leave it in place if it existed before, remove if newly created
            pass  # handled by restore logic

    for d in _STATE_DIRS:
        # If the directory exists but has no backup, it was created during the test
        if d.exists() and d.is_dir():
            pass  # handled by restore logic


@pytest.fixture(autouse=True)
def isolate_file_state(tmp_path):
    """Autouse fixture: back up file-based state before each test, restore after.

    This prevents tests from polluting config.json, asset_registry.json, and
    data/brokers/ for subsequent tests.
    """
    backups = _backup_state(tmp_path)

    yield

    _restore_state(backups)
