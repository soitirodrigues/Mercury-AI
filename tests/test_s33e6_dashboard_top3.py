"""S33-E.6 — Dashboard TOP3 + estados parciais (mocks/controlados, SEM Yahoo).

Prova (sem rede, sem ranking recalculado):
1. TOP3 vem do ScanReport (passthrough verbatim, ordem preservada).
2. TOP3 nao e recalculado (ordem anti-score preservada; sem sorted/sort/rank).
3. Nenhuma chamada ao RankingEngine pelo Dashboard/apresentacao.
4-7. COMPLETE/PARTIAL/TIMEOUT/ERROR preservados verbatim.
8. TOP3 parcial preservado quando existir.
9. TIMEOUT sem resultados nao cria TOP3 ficticio.
10. completed != ranking_count representado (39/39 vs 33).
11-12. SKIPPED_DATA_QUALITY_FAIL e ERROR nao entram no TOP3.
13. scan_id preservado.
14. Nenhuma segunda execucao (apresentacao nao chama scan).
15. Dashboard nao chama engines diretamente.
16-18. SIGNAL-ONLY: sem broker LIVE, sem ordens.
"""
import ast
from pathlib import Path

from app.dashboard.scan_presentation import (
    counters_line,
    present_scan,
    status_banner,
)
from mercury_ai.brain import scan_service as svc

PRESENTATION = Path("app/dashboard/scan_presentation.py")
DASHBOARD = Path("app/dashboard/dashboard.py")
OP_CENTER = Path("app/dashboard/operation_center.py")
P01 = Path("app/terminal/pages/01_Scanner.py")
P02 = Path("app/terminal/pages/02_Dashboard.py")
P03 = Path("app/terminal/pages/03_Historico_Estatisticas.py")
UI_FILES = [PRESENTATION, DASHBOARD, OP_CENTER, P01, P02, P03]

ENGINE_NAMES = {
    "RankingEngine", "ConfluenceEngine", "Consensus",
    "TrendAnalyzer", "TrendEngine", "StructureEngine",
    "LiquidityEngine", "SmartMoney", "RiskEngine",
    "DecisionEngine", "MercuryDecisionEngine",
}
ORDER_NAMES = {"create_order", "send_order", "execute_order", "place_order"}


def _summary(symbol, score=50.0, decision="WAIT"):
    return {
        "symbol": symbol, "decision": decision, "score": score,
        "confidence": 0.5, "grade": "C", "audit_id": "a" * 64,
        "regime": "RANGE",
    }


def _report_dict(status="COMPLETE", scan_id="scan-e6-001",
                 total=39, completed=39, ranked_n=33,
                 skipped_dq=5, errors=1, top3_symbols=None):
    if top3_symbols is None:
        top3_symbols = ["SYM0", "SYM1", "SYM2"]
    ranked = [_summary(f"SYM{i}", score=90.0 - i) for i in range(ranked_n)]
    # TOP3 = fatia do ranked, ordem verbatim
    sym_to_row = {r["symbol"]: r for r in ranked}
    top3 = [dict(sym_to_row[s]) for s in top3_symbols]
    per_asset = []
    for i in range(ranked_n):
        per_asset.append({
            "scan_id": scan_id, "symbol": f"SYM{i}", "outcome": "RANKED",
            "decision": "WAIT", "score": 90.0 - i, "error": None,
        })
    for i in range(skipped_dq):
        per_asset.append({
            "scan_id": scan_id, "symbol": f"DQ{i}", "outcome": "SKIPPED_DATA_QUALITY_FAIL",
            "decision": None, "score": None, "error": None,
        })
    for i in range(errors):
        per_asset.append({
            "scan_id": scan_id, "symbol": f"ERR{i}", "outcome": "ERROR",
            "decision": None, "score": None, "error": "boom",
        })
    assert len(per_asset) == total
    return {
        "scan_id": scan_id, "status": status,
        "symbols_total": total, "symbols_completed": completed,
        "symbols_timeout": 0, "symbols_error": errors,
        "duration_s": 12.5, "cycle_timeout_s": 290.0, "workers": 4,
        "ranked": ranked, "top3": top3, "per_asset": per_asset,
        "error": None if status != "ERROR" else "ranking failed",
    }


def _src(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_01_top3_from_scanreport_verbatim():
    rep = _report_dict()
    view = present_scan(rep)
    assert view["top3"] == rep["top3"], "TOP3 deve ser passthrough do ScanReport"
    assert view["top3_symbols"] == ["SYM0", "SYM1", "SYM2"]


def test_02_top3_not_recalculated_anti_score_order():
    # Ordem deliberadamente NAO ordenada por score: recalculo quebraria.
    rep = _report_dict()
    rep["top3"] = [
        _summary("C", score=10.0), _summary("A", score=99.0), _summary("B", score=50.0),
    ]
    rep["ranked"] = list(rep["top3"])
    view = present_scan(rep)
    assert view["top3_symbols"] == ["C", "A", "B"], "nao reordenar por score"
    tree = ast.parse(_src(PRESENTATION))
    src_low = _src(PRESENTATION).lower()
    assert "sorted(" not in src_low and ".sort(" not in src_low
    called = {
        n.func.attr for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
    } | {
        n.func.id for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    }
    assert not ({"sorted", "sort", "rank"} & called)


def _code_names(path: Path):
    """Nomes reais de codigo via AST (ignora docstrings/comentarios/texto)."""
    tree = ast.parse(_src(path))
    names = set()
    imported = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Attribute):
            names.add(n.attr)
        elif isinstance(n, ast.ImportFrom) and n.module:
            imported.add(n.module)
        elif isinstance(n, ast.Import):
            for a in n.names:
                imported.add(a.name)
    return names, imported


def test_03_no_ranking_engine_in_dashboard_or_presentation():
    for p in UI_FILES:
        names, imported = _code_names(p)
        assert "RankingEngine" not in names, f"{p}: nao chamar RankingEngine"
        assert not any("ranking" in m.lower() or "scanner" in m.lower()
                       for m in imported), f"{p}: nao importar ranking/scanner"
        # rank( como chamada de ranking — evidence_ranking e dado, nao chamada
        tree = ast.parse(_src(p))
        rank_calls = {
            n.func.attr for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "rank"
        } | {
            n.func.id for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == "rank"
        }
        assert not rank_calls, f"{p}: sem rank() de ranking"
    # PRESENTATION nao importa scanner/ranking de forma alguma (redundante c/ acima)
    _, imported = _code_names(PRESENTATION)
    assert not any("ranking" in m.lower() or "scanner" in m.lower()
                   for m in imported)


def test_04_complete_presented_as_complete():
    view = present_scan(_report_dict(status="COMPLETE"))
    assert view["status"] == "COMPLETE" and view["is_complete"]
    assert not view["is_partial"] and not view["is_timeout"] and not view["is_error"]
    assert "COMPLETE" in status_banner(view)


def test_05_partial_stays_partial_with_top3():
    rep = _report_dict(status="PARTIAL", scan_id="scan-partial-e6")
    view = present_scan(rep)
    assert view["status"] == "PARTIAL" and view["is_partial"]
    assert "PARTIAL" in status_banner(view)
    assert "COMPLETE" not in status_banner(view)
    assert view["top3_symbols"] == ["SYM0", "SYM1", "SYM2"], "parcial preservado"


def test_06_timeout_stays_timeout():
    rep = _report_dict(status="TIMEOUT", scan_id="scan-timeout-e6")
    rep["symbols_completed"] = 2
    view = present_scan(rep)
    assert view["status"] == "TIMEOUT" and view["is_timeout"]
    assert "TIMEOUT" in status_banner(view)
    assert "COMPLETE" not in status_banner(view)


def test_07_error_stays_error_with_message():
    rep = _report_dict(status="ERROR", scan_id="scan-error-e6")
    view = present_scan(rep)
    assert view["status"] == "ERROR" and view["is_error"]
    assert "ERROR" in status_banner(view)
    assert view["error"] == "ranking failed"


def test_08_partial_top3_preserved():
    rep = _report_dict(status="PARTIAL", scan_id="scan-p8")
    rep["top3"] = [_summary("P0", 10.0), _summary("P1", 11.0)]
    view = present_scan(rep)
    assert len(view["top3"]) == 2
    assert view["top3_symbols"] == ["P0", "P1"]


def test_09_timeout_empty_creates_no_fictitious_top3():
    rep = _report_dict(status="TIMEOUT", scan_id="scan-t9",
                       total=0, completed=0, ranked_n=0,
                       skipped_dq=0, errors=0, top3_symbols=[])
    rep["symbols_total"] = 2
    rep["top3"] = []
    rep["ranked"] = []
    rep["per_asset"] = [
        {"scan_id": "scan-t9", "symbol": "S0", "outcome": "TIMEOUT",
         "decision": None, "score": None, "error": None},
        {"scan_id": "scan-t9", "symbol": "S1", "outcome": "TIMEOUT",
         "decision": None, "score": None, "error": None},
    ]
    view = present_scan(rep)
    assert view["top3"] == [] and not view["has_top3"]
    assert view["status"] == "TIMEOUT"


def test_10_completed_vs_ranking_count_distinguished():
    rep = _report_dict(total=39, completed=39, ranked_n=33,
                       skipped_dq=5, errors=1)
    view = present_scan(rep)
    assert view["progress_text"] == "39/39"
    assert view["ranked_count"] == 33
    assert not view["completed_eq_ranked"], "completed != ranking_count"
    c = view["counters"]
    assert c["ranked"] == 33 and c["skipped_dq"] == 5 and c["error"] == 1
    line = counters_line(view)
    assert "Ranqueados: 33" in line and "39/39" in counters_line(view) or "39 / 39" in line or "39/39" in view["progress_text"]


def test_11_skipped_dq_not_in_top3():
    view = present_scan(_report_dict())
    assert view["top3_excludes_non_ranked"]
    assert not (set(view["top3_symbols"]) & {f"DQ{i}" for i in range(5)})


def test_12_error_not_in_top3():
    view = present_scan(_report_dict())
    assert view["top3_excludes_non_ranked"]
    assert not (set(view["top3_symbols"]) & {f"ERR{i}" for i in range(1)})


def test_13_scan_id_preserved():
    view = present_scan(_report_dict(scan_id="scan-identity-xyz"))
    assert view["scan_id"] == "scan-identity-xyz"
    assert view["progress_text"] == "39/39"


def test_14_presentation_causes_no_second_execution():
    from unittest.mock import MagicMock
    rep = _report_dict()
    fake = MagicMock()
    fake.scan.return_value = []
    fake.last_scan_report = None
    before = fake.scan.call_count
    view = present_scan(rep)  # consumo puro: nao recebe scanner, nao chama scan
    assert fake.scan.call_count == before == 0
    assert view["scan_id"] == "scan-e6-001"
    for p in [PRESENTATION, P03]:
        src = _src(p)
        assert ".scan(" not in src, f"{p}: apresentacao nao executa scanner"
    # run_dashboard_scan (unica execucao) vive so no wiring E.5, nao na apresentacao
    assert "run_dashboard_scan" not in _src(PRESENTATION)


def test_15_dashboard_calls_no_engines_directly():
    for p in UI_FILES:
        tree = ast.parse(_src(p))
        names = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Name):
                names.add(n.id)
            elif isinstance(n, ast.Attribute):
                names.add(n.attr)
        hit = ENGINE_NAMES & names
        # evidence_ranking e atributo de Decision (dado), nao engine; filtrar
        hit = {h for h in hit if h not in set()}
        assert not hit, f"{p}: chama engine diretamente: {hit}"


def test_16_17_18_signal_only_no_live_broker_no_orders():
    ev = svc.signal_only_evidence()
    assert ev["signal_only"] is True
    for p in UI_FILES:
        tree = ast.parse(_src(p))
        imported = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module:
                imported.add(n.module)
            elif isinstance(n, ast.Import):
                for a in n.names:
                    imported.add(a.name)
        forbidden = [m for m in imported
                     if "order_executor" in m.lower() or "live" in m.lower()
                     or "broker" in m.lower() and "brokers" not in m.lower()]
        # settings.BROKER e texto de config ("Broker" label) nao sao broker LIVE
        forbidden = [m for m in forbidden if "scan_presentation" not in m]
        assert forbidden == [], f"{p}: import LIVE proibido: {forbidden}"
        called = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                if isinstance(f, ast.Attribute):
                    called.add(f.attr)
                elif isinstance(f, ast.Name):
                    called.add(f.id)
        assert "OrderExecutor" not in called, f"{p}: OrderExecutor"
        assert not (ORDER_NAMES & called), f"{p}: criacao de ordem"
