"""S33-E.5 — Dashboard wiring tests (mocks/controlados, SEM Yahoo real).

Prova:
1. run_dashboard_scan chama o scanner UMA unica vez.
2. Chamada utiliza workers=4.
3-8. ScanReport propagado com scan_id/status preservados
     (COMPLETE/PARTIAL/TIMEOUT/ERROR).
9. Resultados parciais nao descartados.
10. top3 proveniente do ScanReport preservado.
11. Nenhuma segunda execucao para montar a resposta.
12-14. SIGNAL-ONLY: sem broker LIVE, sem ordens.
"""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from mercury_ai.brain import scan_service as svc
from mercury_ai.brain.scanner import (
    SCAN_DEFAULT_CYCLE_TIMEOUT_S,
    SCAN_DEFAULT_WORKERS,
    ScanReport,
)


def _fake_report(status="COMPLETE", scan_id="scan-e5-001", n_ranked=3, n_per=4):
    ranked = [SimpleNamespace(market=SimpleNamespace(symbol=f"S{i}")) for i in range(n_ranked)]
    top3 = list(ranked[:3])
    per_asset = [
        {"scan_id": scan_id, "symbol": f"S{i}", "outcome": "RANKED" if i < n_ranked else "SKIPPED_DATA_QUALITY_FAIL"}
        for i in range(n_per)
    ]
    return ScanReport(
        scan_id=scan_id,
        status=status,
        ranked=ranked,
        top3=top3,
        symbols_total=n_per,
        symbols_completed=n_per if status != "TIMEOUT" else 0,
        symbols_timeout=n_per if status == "TIMEOUT" else 0,
        symbols_error=1 if status == "ERROR" else 0,
        per_asset=per_asset,
        duration_s=1.23,
        cycle_timeout_s=SCAN_DEFAULT_CYCLE_TIMEOUT_S,
        workers=SCAN_DEFAULT_WORKERS,
    )


class _FakeScanner:
    def __init__(self, report):
        self._report = report
        self.calls = []
        self.last_scan_report = None

    def scan(self, workers=1, cycle_timeout_s=290.0):
        self.calls.append({"workers": workers, "cycle_timeout_s": cycle_timeout_s})
        self.last_scan_report = self._report
        return list(self._report.ranked)


def test_single_execution_workers4_and_report_propagated(tmp_path):
    rep = _fake_report(status="COMPLETE")
    sc = _FakeScanner(rep)
    ranked, out = svc.run_dashboard_scan(scanner=sc, persist=True, base_dir=tmp_path)
    assert len(sc.calls) == 1, "UMA unica execucao por ANALYZE NOW"
    assert sc.calls[0]["workers"] == 4, "workers=4 validado S33-E.4"
    assert sc.calls[0]["cycle_timeout_s"] == 290.0, "cycle_timeout=290s inalterado"
    assert out is rep, "ScanReport real propagado (identidade)"
    assert out.scan_id == "scan-e5-001"
    assert out.status == "COMPLETE"
    assert ranked == list(rep.ranked)
    # persistencia preserva envelope
    stored = svc.load_scan_report("scan-e5-001", base_dir=tmp_path)
    assert stored["scan_id"] == "scan-e5-001"
    assert stored["status"] == "COMPLETE"
    latest = svc.load_latest_scan_report(base_dir=tmp_path)
    assert latest["scan_id"] == "scan-e5-001"


def test_partial_preserved_not_converted_to_complete(tmp_path):
    rep = _fake_report(status="PARTIAL", scan_id="scan-partial")
    sc = _FakeScanner(rep)
    _, out = svc.run_dashboard_scan(scanner=sc, persist=True, base_dir=tmp_path)
    assert out.status == "PARTIAL"
    stored = svc.load_latest_scan_report(base_dir=tmp_path)
    assert stored["status"] == "PARTIAL", "NAO converter PARTIAL->COMPLETE"
    assert len(stored["per_asset"]) == 4, "parciais nao descartados"
    assert stored["symbols_completed"] == 4


def test_timeout_preserved_not_converted(tmp_path):
    rep = _fake_report(status="TIMEOUT", scan_id="scan-timeout", n_ranked=0, n_per=2)
    rep.per_asset = [
        {"scan_id": "scan-timeout", "symbol": "S0", "outcome": "TIMEOUT"},
        {"scan_id": "scan-timeout", "symbol": "S1", "outcome": "TIMEOUT"},
    ]
    rep.symbols_completed = 0
    rep.symbols_timeout = 2
    sc = _FakeScanner(rep)
    ranked, out = svc.run_dashboard_scan(scanner=sc, persist=True, base_dir=tmp_path)
    assert out.status == "TIMEOUT"
    assert ranked == []
    stored = svc.load_latest_scan_report(base_dir=tmp_path)
    assert stored["status"] == "TIMEOUT", "NAO converter TIMEOUT->COMPLETE"


def test_error_preserved(tmp_path):
    rep = _fake_report(status="ERROR", scan_id="scan-error")
    rep.error = "ranking failed"
    sc = _FakeScanner(rep)
    _, out = svc.run_dashboard_scan(scanner=sc, persist=True, base_dir=tmp_path)
    assert out.status == "ERROR"
    stored = svc.load_latest_scan_report(base_dir=tmp_path)
    assert stored["status"] == "ERROR"


def test_top3_per_asset_from_report_preserved(tmp_path):
    rep = _fake_report(status="COMPLETE", scan_id="scan-top3")
    sc = _FakeScanner(rep)
    _, out = svc.run_dashboard_scan(scanner=sc, persist=True, base_dir=tmp_path)
    stored = svc.load_latest_scan_report(base_dir=tmp_path)
    assert [t["symbol"] for t in stored["top3"]] == ["S0", "S1", "S2"]
    assert len(stored["per_asset"]) == 4
    assert all(r["scan_id"] == "scan-top3" for r in stored["per_asset"])


def test_no_second_execution_to_build_response(tmp_path):
    rep = _fake_report()
    sc = _FakeScanner(rep)
    sc.scan = MagicMock(side_effect=sc.scan)
    svc.run_dashboard_scan(scanner=sc, persist=True, base_dir=tmp_path)
    assert sc.scan.call_count == 1, "nenhuma segunda execucao"


def test_signal_only_no_live_broker_no_orders():
    ev = svc.signal_only_evidence()
    assert ev["read_only"] is True, "SIGNAL-ONLY: settings.READ_ONLY"
    assert ev["forbidden_imports"] == [], "sem broker LIVE/OrderExecutor"
    assert ev["order_calls"] == [], "nenhuma criacao de ordem"
    assert ev["signal_only"] is True
    # prova estatica adicional: nenhuma chamada real (AST) a OrderExecutor/ordens
    import ast
    tree = ast.parse(Path(svc.__file__).read_text(encoding="utf-8"))
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute):
                called.add(f.attr)
            elif isinstance(f, ast.Name):
                called.add(f.id)
    assert "OrderExecutor" not in called
    assert not ({"create_order", "send_order", "execute_order", "place_order"} & called)


def test_defaults_match_validated_path():
    assert svc.DASHBOARD_SCAN_WORKERS == 4
    assert svc.DASHBOARD_CYCLE_TIMEOUT_S == 290.0
    assert SCAN_DEFAULT_WORKERS == 4
    assert SCAN_DEFAULT_CYCLE_TIMEOUT_S == 290.0
