"""S33-E.5 — Dashboard wiring (transporte, SEM inteligencia).

Conecta o Dashboard ao caminho operacional ja validado (S33-E.3/E.4):

    MercuryScanner.scan(workers=4)  ->  scanner.last_scan_report (ScanReport)

Regras deste modulo (sprint S33-E.5):
- UMA execucao por ANALYZE NOW (nunca scan()+scan()).
- workers=4, cycle_timeout=290s (defaults importados do scanner, nao duplicados).
- Nao toca engines, pesos, thresholds, ranking, universo, timeframes, Yahoo.
- Nao converte PARTIAL->COMPLETE nem TIMEOUT->COMPLETE; parciais preservados.
- SIGNAL-ONLY: este modulo nunca importa broker LIVE nem OrderExecutor
  e nunca cria ordens. Leitura de settings.READ_ONLY apenas para evidencia.
- Persistencia minima: reusa ScanReport.to_dict() (serializacao existente);
  escrita atomica (tmp + os.replace) em reports/scan_reports/<scan_id>.json
  + ponteiro latest.json. Nao cria segundo banco nem segundo formato:
  o formato e o dict ja existente do ScanReport.
- Auditoria Fase 5: nenhum mecanismo adequado existia (ScanReport vivia so
  em memoria em `scanner.last_scan_report` e cada pagina Streamlit criava
  `MercuryScanner()` novo descartando o envelope). Arquivo JSON e o
  transporte minimo que sobrevive a rerun/timeout/termino do processo.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from mercury_ai.brain.scanner import (
    SCAN_DEFAULT_CYCLE_TIMEOUT_S,
    SCAN_DEFAULT_WORKERS,
    MercuryScanner,
    ScanReport,
)

# Caminho validado S33-E.4 (parametro operacional, nao estrategia).
DASHBOARD_SCAN_WORKERS = SCAN_DEFAULT_WORKERS  # 4
DASHBOARD_CYCLE_TIMEOUT_S = SCAN_DEFAULT_CYCLE_TIMEOUT_S  # 290.0

# Persistencia minima do envelope (data/ e gitignored: nao polui git status).
SCAN_REPORTS_DIR = Path("data/scan_reports")
LATEST_POINTER = "latest.json"


def _reports_dir(base_dir: Optional[Path] = None) -> Path:
    return Path(base_dir) if base_dir is not None else SCAN_REPORTS_DIR


def persist_scan_report(
    report: ScanReport, base_dir: Optional[Path] = None
) -> Path:
    """Persiste ScanReport.to_dict() de forma atomica. Nunca converte status."""
    target_dir = _reports_dir(base_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    payload: Dict[str, Any] = report.to_dict()
    dest = target_dir / f"{report.scan_id}.json"
    latest = target_dir / LATEST_POINTER
    for path in (dest, latest):
        fd, tmp = tempfile.mkstemp(
            suffix=".tmp", prefix=".scan_", dir=str(target_dir)
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, default=str)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
    return dest


def load_latest_scan_report(
    base_dir: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """Le o ultimo ScanReport persistido (dict do to_dict()). None se ausente."""
    latest = _reports_dir(base_dir) / LATEST_POINTER
    if not latest.exists():
        return None
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


def load_scan_report(
    scan_id: str, base_dir: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    """Le um ScanReport especifico por scan_id. None se ausente."""
    dest = _reports_dir(base_dir) / f"{scan_id}.json"
    if not dest.exists():
        return None
    with open(dest, "r", encoding="utf-8") as f:
        return json.load(f)


def run_dashboard_scan(
    scanner: Optional[MercuryScanner] = None,
    workers: int = DASHBOARD_SCAN_WORKERS,
    cycle_timeout_s: float = DASHBOARD_CYCLE_TIMEOUT_S,
    persist: bool = True,
    base_dir: Optional[Path] = None,
) -> Tuple[Any, ScanReport]:
    """Executa UMA vez o caminho validado e retorna (ranked, ScanReport).

    - Instancia MercuryScanner so se nenhum for injetado (testes injetam fake).
    - Chama scanner.scan(workers=..., cycle_timeout_s=...) EXATAMENTE uma vez.
    - Le scanner.last_scan_report (envelope real, nao reconstruido).
    - Persiste via persist_scan_report (sobrevive a rerun/timeout).
    - Nao executa segunda analise para montar a resposta.
    """
    sc = scanner if scanner is not None else MercuryScanner()
    ranked = sc.scan(workers=workers, cycle_timeout_s=cycle_timeout_s)
    report = sc.last_scan_report
    if report is None:  # pragma: no cover — defensivo, scan sempre preenche
        raise RuntimeError("scan() nao produziu last_scan_report")
    if persist:
        persist_scan_report(report, base_dir=base_dir)
    return ranked, report


def signal_only_evidence() -> Dict[str, Any]:
    """Evidencia SIGNAL-ONLY sem importar broker/execucao.

    Retorna READ_ONLY flag + prova estatica de que este modulo nao referencia
    OrderExecutor/broker LIVE/criacao de ordens.
    """
    import ast

    from mercury_ai.config import settings

    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            for a in node.names:
                imported.add(a.name)
    forbidden = [m for m in imported if "order_executor" in m or "broker" in m.lower()]
    # Deteccao por AST (nos Call/Attribute), nao por substring: evita que os
    # proprios literais/docstring desta funcao gerem falso positivo.
    order_names = {"create_order", "send_order", "execute_order", "place_order"}
    order_calls = sorted(
        {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in order_names
        }
        | {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in order_names
        }
    )
    return {
        "read_only": bool(getattr(settings, "READ_ONLY", True)),
        "forbidden_imports": forbidden,
        "order_calls": order_calls,
        "signal_only": bool(getattr(settings, "READ_ONLY", True))
        and not forbidden
        and not order_calls,
    }
