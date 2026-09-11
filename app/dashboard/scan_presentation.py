"""S33-E.6 — Apresentacao operacional do ScanReport (SEM inteligencia).

Camada PURA de apresentacao/consumo. Regras absolutas deste modulo:
- NUNCA recalcula ranking, NUNCA ordena, NUNCA filtra top3, NUNCA cria score.
- NUNCA chama MercuryScanner.scan, RankingEngine, ConfluenceEngine, Consensus,
  indicadores, Trend/Structure/Liquidity/SmartMoney/Risk/DecisionEngine.
- NUNCA importa broker LIVE nem OrderExecutor; NUNCA cria ordens (SIGNAL-ONLY).
- TOP3 vem EXCLUSIVAMENTE de ScanReport.top3 (ou dict ja serializado via
  ScanReport.to_dict()), na ordem armazenada, verbatim.
- Status COMPLETE/PARTIAL/TIMEOUT/ERROR preservado verbatim, nunca convertido.
- completed/total/ranked/skipped/errors distinguidos (completed != ranking_count).
- SKIPPED_DATA_QUALITY_FAIL e ERROR nunca entram no TOP3 (verificacao, nao filtro).
- scan_id preservado verbatim; progresso usa apenas completed/total reais.
- Nenhuma chamada de rede (Yahoo), nenhum timer falso de progresso.

Aceita tanto o objeto ScanReport (com .to_dict()) quanto o dict ja
serializado. Retorna um view-model imutavel-em-pratica (dicts/listas novas
rasas, sem reordenar) para o Streamlit consumir.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

SCAN_STATUSES = ("COMPLETE", "PARTIAL", "TIMEOUT", "ERROR")

_ERROR_OUTCOMES = frozenset({"ERROR", "EXCEPTION"})
_TIMEOUT_OUTCOME = "TIMEOUT"
_RANKED_OUTCOME = "RANKED"
_DISCARDED_OUTCOME = "DISCARDED_SCORE"
_SKIPPED_PREFIX = "SKIPPED_"
_SKIPPED_DQ = "SKIPPED_DATA_QUALITY_FAIL"


def to_report_dict(report: Any) -> Optional[Dict[str, Any]]:
    """Normaliza ScanReport-objeto ou dict para dict. None preservado."""
    if report is None:
        return None
    to_dict = getattr(report, "to_dict", None)
    if callable(to_dict):
        data = to_dict()
        if isinstance(data, dict):
            return data
        raise TypeError("ScanReport.to_dict() nao retornou dict")
    if isinstance(report, dict):
        return report
    if isinstance(report, Mapping):  # pragma: no cover — defensivo
        return dict(report)
    raise TypeError(f"tipo de report nao suportado: {type(report).__name__}")


def _as_list(value: Any) -> List[Any]:
    return list(value) if isinstance(value, (list, tuple)) else []


def present_scan(report: Any) -> Dict[str, Any]:
    """Constroi o view-model de apresentacao a partir do ScanReport.

    - top3: passthrough verbatim na ordem armazenada (SEM sorted/sort/rank).
    - contadores derivados APENAS de per_asset/outcome + len(ranked/top3).
    - status/scan_id/error/duration preservados verbatim.
    """
    data = to_report_dict(report)
    if data is None:
        raise ValueError("ScanReport ausente (None): sem dados para apresentar")
    if not isinstance(data, dict):
        raise TypeError("ScanReport invalido para apresentacao")

    status = data.get("status")
    scan_id = data.get("scan_id")
    total = data.get("symbols_total", 0) or 0
    completed = data.get("symbols_completed", 0) or 0

    ranked = _as_list(data.get("ranked", []))
    top3 = _as_list(data.get("top3", []))
    per_asset = _as_list(data.get("per_asset", []))

    n_ranked = len(ranked)
    n_per = len(per_asset)
    n_skipped = sum(
        1 for r in per_asset
        if isinstance(r, dict) and str(r.get("outcome", "")).startswith(_SKIPPED_PREFIX)
    )
    n_skipped_dq = sum(
        1 for r in per_asset
        if isinstance(r, dict) and r.get("outcome") == _SKIPPED_DQ
    )
    n_error = sum(
        1 for r in per_asset
        if isinstance(r, dict) and r.get("outcome") in _ERROR_OUTCOMES
    )
    n_timeout_rows = sum(
        1 for r in per_asset
        if isinstance(r, dict) and r.get("outcome") == _TIMEOUT_OUTCOME
    )
    n_discarded = sum(
        1 for r in per_asset
        if isinstance(r, dict) and r.get("outcome") == _DISCARDED_OUTCOME
    )

    # Simbolos ranqueados (para verificacao de exclusao, NAO para filtrar top3).
    ranked_symbols = {
        r.get("symbol") for r in ranked
        if isinstance(r, dict) and r.get("symbol") is not None
    }
    top3_symbols = [
        t.get("symbol") for t in top3
        if isinstance(t, dict)
    ]
    non_ranked_symbols = {
        r.get("symbol") for r in per_asset
        if isinstance(r, dict)
        and r.get("outcome") != _RANKED_OUTCOME
        and r.get("symbol") is not None
    }
    # TOP3 deve ser subconjunto de RANKED; skipped/error nunca dentro do TOP3.
    top3_excludes_non_ranked = all(s not in non_ranked_symbols for s in top3_symbols)

    progress_text = f"{completed}/{total}"

    return {
        "scan_id": scan_id,
        "status": status,
        "is_complete": status == "COMPLETE",
        "is_partial": status == "PARTIAL",
        "is_timeout": status == "TIMEOUT",
        "is_error": status == "ERROR",
        "completed": completed,
        "total": total,
        "progress_text": progress_text,
        "ranked_count": n_ranked,
        "per_asset_total": n_per,
        "top3": top3,  # passthrough: mesma ordem, mesmos itens
        "top3_symbols": top3_symbols,
        "has_top3": len(top3) > 0,
        "ranked": ranked,
        "per_asset": per_asset,
        "duration_s": data.get("duration_s"),
        "cycle_timeout_s": data.get("cycle_timeout_s"),
        "workers": data.get("workers"),
        "symbols_timeout": data.get("symbols_timeout", 0) or 0,
        "symbols_error": data.get("symbols_error", 0) or 0,
        "error": data.get("error"),
        "counters": {
            "ranked": n_ranked,
            "skipped": n_skipped,
            "skipped_dq": n_skipped_dq,
            "error": n_error,
            "timeout_rows": n_timeout_rows,
            "discarded_score": n_discarded,
            "per_asset_total": n_per,
        },
        "top3_excludes_non_ranked": top3_excludes_non_ranked,
        "completed_eq_ranked": (completed == n_ranked),
    }


def status_banner(view: Mapping[str, Any]) -> str:
    """Rotulo textual do estado — verbatim, sem conversao."""
    status = view.get("status")
    if status == "COMPLETE":
        return "COMPLETE — execução concluída"
    if status == "PARTIAL":
        return "PARTIAL — resultados parciais (universo não concluído)"
    if status == "TIMEOUT":
        return "TIMEOUT — ciclo esgotado; parciais preservados se existirem"
    if status == "ERROR":
        return "ERROR — falha do ciclo; ver detalhe abaixo"
    return f"STATUS DESCONHECIDO: {status!r}"


def counters_line(view: Mapping[str, Any]) -> str:
    """Linha operacional: distingue RANKED de SKIPPED/ERROR."""
    c = view.get("counters", {})
    return (
        f"Ranqueados: {c.get('ranked', 0)} | "
        f"Data quality: {c.get('skipped_dq', 0)} "
        f"(skipped total {c.get('skipped', 0)}) | "
        f"Erros: {c.get('error', 0)} | "
        f"Timeouts: {c.get('timeout_rows', 0)} | "
        f"Processados: {view.get('progress_text', '?')}"
    )
