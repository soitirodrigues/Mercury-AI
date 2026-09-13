"""S33-E.6 — Builder AnalysisResult -> Signal (PROPAGACAO, sem recalculo).

Regras absolutas deste modulo (SIGNAL-ONLY):
- NAO altera thresholds, pesos, ProbabilityEngine, ConfluenceEngine,
  ConfidenceEngine, DecisionResolver, RiskEngine, InstitutionalScore ou
  qualquer regra de decisao. Nao importa esses motores.
- NAO recalcula risco: entry_price/stop_loss/take_profit/invalidation/
  risk_reward sao copiados de MarketData/RiskAssessment ja calculados.
  entry_price = market.close (preco de referencia do sistema, o mesmo usado
  pelo RiskEngine) — propagacao, nao calculo.
- NAO recalcula MTF: propaga o MTFConsensus ja existente (decision ou
  context); timeframe ausente/rejeitado/erro e registrado com o estado
  verdadeiro, nunca inventado. Sem consenso -> "absent" explicito.
- NAO cria frase generica: reason = decision_rationale/exec_summary reais
  do Narrative/Explainability (ou o texto verbatim dos estados terminais).
- NAO executa ordens, NAO importa broker/OrderExecutor, NAO cria dados de
  mercado: last_m5_ts vem do chamador (pipeline anexa df.index[-1]) ou de
  market_df explicito; sem vela conhecida -> next_m5 None -> EXPIRED.
- signal_ts default = DeterministicClock.utcnow() (deterministico sob replay).
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional

from mercury_ai.models.signal import Signal
from mercury_ai.signals.m5_timing import compute_entry_window, compute_next_m5, parse_utc, to_iso_utc
from mercury_ai.utils.deterministic_clock import DeterministicClock

_MTF_ORDER = ("M1", "M5", "M15", "H1", "H4")


def _extract_last_m5(result: Any, last_m5_ts: Any, market_df: Any) -> Optional[str]:
    """Resolve last_m5_ts: explicito > AnalysisResult.last_candle_ts > market_df.

    Nunca usa wall-clock. Retorna ISO aware-UTC ou None.
    """
    for candidate in (last_m5_ts, getattr(result, "last_candle_ts", None)):
        parsed = parse_utc(candidate)
        if parsed is not None:
            return to_iso_utc(parsed)
    try:
        if market_df is not None and not market_df.empty:
            idx_last = market_df.index[-1]
            iso = idx_last.isoformat() if hasattr(idx_last, "isoformat") else str(idx_last)
            parsed = parse_utc(iso)
            if parsed is not None:
                return to_iso_utc(parsed)
    except Exception:
        pass
    return None


def _extract_mtf_summary(result: Any) -> Dict[str, Any]:
    """Contexto MTF ja existente -> dict honesto por timeframe."""
    per_tf: Dict[str, Any] = {tf: "absent" for tf in _MTF_ORDER}
    consensus = None
    decision = getattr(result, "decision", None)
    if decision is not None:
        consensus = getattr(decision, "mtf_consensus", None)
    if consensus is None:
        context = getattr(result, "context", None)
        if context is not None:
            consensus = getattr(context, "mtf_consensus", None)
    if consensus is None:
        return {
            "status": "absent",
            "global_bias": "UNKNOWN",
            "local_bias": "UNKNOWN",
            "alignment_score": 0.0,
            "conflict_detected": False,
            "summary": "",
            "timeframes": per_tf,
        }
    status_map = getattr(consensus, "timeframe_status", None) or {}
    errors = getattr(consensus, "timeframe_errors", None) or {}
    for tf in _MTF_ORDER:
        state = status_map.get(tf, "absent")
        try:
            err = errors.get(tf)
        except AttributeError:
            err = None
        per_tf[tf] = f"{state}:{err}" if err else state
    return {
        "status": "present",
        "global_bias": getattr(consensus, "global_bias", "UNKNOWN"),
        "local_bias": getattr(consensus, "local_bias", "UNKNOWN"),
        "alignment_score": float(getattr(consensus, "alignment_score", 0.0) or 0.0),
        "conflict_detected": bool(getattr(consensus, "conflict_detected", False)),
        "summary": getattr(consensus, "summary", "") or "",
        "timeframes": per_tf,
    }


def _extract_reason(result: Any) -> str:
    """Justificativa real da decisao (Narrative/Explainability/terminal)."""
    decision = getattr(result, "decision", None)
    explanation = getattr(decision, "explanation", None) if decision is not None else None
    if isinstance(explanation, str):
        return explanation
    if explanation is not None:
        for attr in ("decision_rationale", "exec_summary"):
            text = getattr(explanation, attr, "") or ""
            if text:
                return text
    if decision is not None:
        for attr in ("summary", "technical_reason"):
            text = getattr(decision, attr, "") or ""
            if text:
                return text
    return ""


def _extract_regime(result: Any) -> str:
    for holder in (getattr(result, "market_regime", None),
                   getattr(getattr(result, "decision", None), "market_regime", None),
                   getattr(getattr(result, "context", None), "market_regime", None)):
        if holder is None:
            continue
        enum_val = getattr(holder, "regime", holder)
        value = getattr(enum_val, "value", enum_val)
        if value is not None and str(value):
            return str(value)
    return "UNKNOWN"


def _signal_id(symbol: str, decision: str, audit_id: str, signal_ts: Optional[str], next_m5: Optional[str]) -> str:
    raw = "|".join([symbol or "?", decision or "?", audit_id or "", signal_ts or "", next_m5 or ""])
    return "sig_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def build_signal_from_analysis(
    result: Any,
    *,
    signal_ts: Any = None,
    last_m5_ts: Any = None,
    market_df: Any = None,
) -> Signal:
    """Constroi o Signal formal a partir de um AnalysisResult real.

    Propagacao pura: nenhum motor e chamado, nenhuma formula e reaplicada.
    WAIT permanece WAIT (OPPORTUNITY != SIGNAL — selecao e trabalho do E.7).
    """
    market = getattr(result, "market", None)
    decision = getattr(result, "decision", None)
    risk = getattr(result, "risk_assessment", None)
    confluence = getattr(result, "confluence", None)

    symbol = getattr(market, "symbol", None) or "?"
    action = getattr(decision, "decision", "UNKNOWN") or "UNKNOWN"
    if hasattr(action, "value"):
        action = action.value

    sig_dt = parse_utc(signal_ts)
    if sig_dt is None:
        sig_dt = parse_utc(DeterministicClock.utcnow())
    signal_iso = to_iso_utc(sig_dt)

    last_iso = _extract_last_m5(result, last_m5_ts, market_df)
    next_iso = compute_next_m5(last_iso)
    window = compute_entry_window(signal_iso, next_iso)

    close = getattr(market, "close", None)
    entry_price = float(close) if isinstance(close, (int, float)) and close > 0 else None

    def _f(obj: Any, name: str, default: float = 0.0) -> float:
        try:
            val = getattr(obj, name, default)
            return float(val) if val is not None else default
        except (TypeError, ValueError):
            return default

    stop = getattr(risk, "suggested_stop", None) if risk is not None else None
    take = getattr(risk, "suggested_take_profit", None) if risk is not None else None
    inv = getattr(risk, "invalidation_point", None) if risk is not None else None
    stop_loss = float(stop) if isinstance(stop, (int, float)) and stop > 0 else None
    take_profit = float(take) if isinstance(take, (int, float)) and take > 0 else None
    invalidation = float(inv) if isinstance(inv, (int, float)) and inv != 0 else None
    risk_reward = _f(risk, "risk_reward_ratio", 0.0)

    reason = _extract_reason(result)
    audit_id = getattr(decision, "audit_id", "") or ""

    # Forward-bias M5: confirmação de continuação p/ a PRÓXIMA vela
    # (classificação pura sobre df fechado + MTF; nunca altera decisão/score).
    # CONTRATO anti-repaint: forward_bias exige SOMENTE velas fechadas.
    # market_df inclui a vela em formação (última linha, parcial — com um
    # único tick, High==Low==Close => range 0 => "range nulo" EXPIRED falso
    # em TODOS os ativos). Drop explícito da última linha aqui.
    _mtf = _extract_mtf_summary(result)
    try:
        from mercury_ai.signals.forward_bias import forward_bias as _fwd
        _closed = market_df.iloc[:-1] if market_df is not None and len(market_df) >= 4 else market_df
        _fb = _fwd(_closed, action, _mtf)
    except Exception:
        _fb = {"state": "EXPIRED", "reason": "forward-bias indisponível", "direction": "NONE"}

    explanation = getattr(decision, "explanation", None) if decision is not None else None
    strong = ()
    if explanation is not None and not isinstance(explanation, str):
        try:
            strong = tuple(str(e) for e in (getattr(explanation, "strong_evidences", ()) or ()))[:5]
        except TypeError:
            strong = ()

    return Signal(
        asset=symbol,
        action=action,
        confidence=_f(decision, "confidence", 0.0),
        score=_f(decision, "score", 0.0),
        entry=entry_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
        timeframe=getattr(market, "timeframe", None) or "M5",
        evidences=strong,
        explanation=reason,
        signal_id=_signal_id(symbol, action, audit_id, signal_iso, next_iso),
        signal_ts=signal_iso,
        last_m5_ts=last_iso,
        next_m5_ts=next_iso,
        entry_price=entry_price,
        entry_window_start=window["start"],
        entry_window_end=window["end"],
        entry_window_seconds=window["seconds"],
        seconds_to_next_m5=window["seconds_to_next_m5"],
        entry_valid_for_next_m5=window["valid"],
        entry_timing_state=window["state"],
        invalidation=invalidation,
        risk_reward=risk_reward,
        probability_buy=_f(decision, "buy_probability", 0.0),
        probability_sell=_f(decision, "sell_probability", 0.0),
        probability_wait=_f(decision, "wait_probability", 0.0),
        confluence=_f(confluence, "weighted_score", 0.0),
        quality=_f(decision, "quality", 0.0),
        institutional_score=_f(decision, "score", 0.0),
        grade=getattr(decision, "grade", "N/A") or "N/A",
        mtf_summary=_extract_mtf_summary(result),
        market_regime=_extract_regime(result),
        reason=reason,
        audit_id=audit_id,
        forward_state=str((_fb or {}).get("state", "EXPIRED")),
        forward_reason=str((_fb or {}).get("reason", "")),
        forward_direction=str((_fb or {}).get("direction", "NONE")),
    )
