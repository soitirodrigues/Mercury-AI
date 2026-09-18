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
            "conflict_score": 0.0,
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
        "conflict_score": float(getattr(consensus, "conflict_score", 0.0) or 0.0),
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

    # Exit plan TP1+BE (propagação pura do RiskEngine; sem recalcular).
    _tp1 = getattr(risk, "take_profit_1r", None) if risk is not None else None
    _be = getattr(risk, "breakeven_trigger", None) if risk is not None else None
    take_profit_1r = float(_tp1) if isinstance(_tp1, (int, float)) and _tp1 > 0 else None
    breakeven_trigger = float(_be) if isinstance(_be, (int, float)) and _be > 0 else None
    exit_plan = getattr(risk, "exit_plan", "TP1_50_BE_RUNNER_2R") or "TP1_50_BE_RUNNER_2R"

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

    # Preditor da PRÓXIMA vela (SMC estrutural: topos/fundos — replica a
    # leitura do trader institucional; nunca altera decisão/score).
    try:
        from mercury_ai.signals.next_candle_predictor import (
            predict_next_candle as _predict, predictor_agrees as _agrees)
        _pred = _predict(_closed)
        _agree = _agrees(_pred, action)
    except Exception:
        _pred = {"direction": "NEUTRAL", "confidence": 0.0, "reason": "preditor indisponível",
                 "structure": "RANGE", "key_level": None, "key_kind": "NONE", "reasons": []}
        _agree = None

    explanation = getattr(decision, "explanation", None) if decision is not None else None
    strong = ()
    if explanation is not None and not isinstance(explanation, str):
        try:
            strong = tuple(str(e) for e in (getattr(explanation, "strong_evidences", ()) or ()))[:5]
        except TypeError:
            strong = ()

    # Sessão operacional (propagação pura de session_analysis; sem recalcular).
    _sess = getattr(result, "session_analysis", None)
    _sess_name = getattr(_sess, "session", None) if _sess is not None else None
    _sess_liq = getattr(_sess, "liquidity_score", None) if _sess is not None else None
    try:
        _sess_liq_f = float(_sess_liq) if _sess_liq is not None else None
    except (TypeError, ValueError):
        _sess_liq_f = None
    _sess_thin = bool(_sess_liq_f is not None and _sess_liq_f < 50)

    # Filtros institucionais M5 (observáveis puros sobre df fechado;
    # sem bloquear, sem alterar decisão/score — ver m5_institutional_filters).
    try:
        from mercury_ai.signals.m5_institutional_filters import (
            institutional_flags as _inst_flags)
        _inst = _inst_flags(_closed, action)
    except Exception:
        _inst = {"trigger_body_ratio": None, "trigger_aligned": None,
                 "trigger_range_atr": None, "ema200_aligned": None,
                 "ema200_dist_atr": None, "rsi": None, "adx": None,
                 "plus_di": None, "minus_di": None,
                 "rsi_adx_approved": None, "bollinger_pos": None,
                 "rsi_value": None, "reversal_candle": None,
                 "sr_distance": None, "band_expansion": None,
                 "bb_upper": None, "bb_middle": None, "bb_lower": None,
                 "bb_bandwidth": None, "lta_exists": None, "ltb_exists": None,
                 "trendline_bias": None, "trendline_aligned": None,
                 "trendline_distance_atr": None, "trendline_detail": ""}

    # Selo N3 (observavel audit-only; NUNCA bloqueia o motor).
    try:
        from mercury_ai.signals.m5_institutional_filters import n3_flags as _n3
        _n3d = _n3(_closed, action, symbol)
    except Exception:
        _n3d = {}

    # Entry mode (EXECUCAO, nunca filtro): limite na regiao OTE/FVG quando
    # ha FVG aberto a favor; mercado caso contrario (vela exausta/sem pullback).
    # Zona = ponto medio do gap quando disponivel via smc (senao entry_price).
    try:
        _has_fvg = bool((_inst or {}).get("has_fvg"))
    except Exception:
        _has_fvg = False
    _entry_mode = "LIMIT_OTE" if _has_fvg else "MARKET"
    _entry_zone = None
    if _has_fvg:
        try:
            from mercury_ai.analysis.institutional_confirmation import atr14 as _a14, detect_fvg as _dfvg
            _atr_v = _a14(_closed)
            _fv = _dfvg(_closed, _atr_v) if _atr_v else {}
            _top, _bot = _fv.get("top"), _fv.get("bottom")
            if _top is not None and _bot is not None:
                _entry_zone = round((float(_top) + float(_bot)) / 2.0, 5)
        except Exception:
            _entry_zone = None
    if _entry_zone is None:
        _entry_zone = entry_price

    # Filtro de noticias (observavel audit-only; NUNCA bloqueia o motor).
    try:
        from mercury_ai.calendar.news_filter import assess_symbol as _news
        _nw = _news(symbol)
    except Exception:
        _nw = {"risk": "UNKNOWN", "blocked": False, "caution": False,
               "event": None, "detail": ""}

    # Plano de reentrada protegida G1/G2 (prospectivo; NUNCA altera decisão).
    # Regra legível para o painel: quando reentrar, quando parar.
    _re_rule = ""
    _re_allowed = action in ("BUY", "SELL")
    if _re_allowed:
        try:
            from mercury_ai.signals.reentry_engine import (
                MAX_GALES as _MG, REJECTION_WICK_MIN as _RW)
            _re_rule = (
                f"Se a vela de entrada fechar contra: reentrar na mesma direção "
                f"na abertura da próxima vela SOMENTE se houver proteção "
                f"(pavio de rejeição >= {_RW:.0%} do range ou displacement renovado). "
                f"Máx {_MG} gales (G1/G2); G2 só em Tokyo/London/NY. "
                f"Sem proteção ou após G2: STOP (LOSS_FINAL)."
            )
        except Exception:
            _re_rule = "reentrada protegida: até 2 gales com confirmação de rejeição"

    # Liquidity Sweep Reversal (observável; NUNCA altera decisão/score).
    try:
        from mercury_ai.signals.liquidity_sweep_engine import (
            asset_validated as _sw_ok, detect_sweep_reversal as _sweep)
        _sw = _sweep(_closed)
        _sw_valid = _sw_ok(symbol)
    except Exception:
        _sw = {"direction": "NONE", "swept_level": None, "wick_ratio": 0.0,
               "in_session": False, "reason": "sweep engine indisponível"}
        _sw_valid = False

    # MODO ATIVO (2026-09-17, autorizado pelo operador): sweep+rejeição em
    # ativo validado GERA sinal quando o pipeline decidiu WAIT/UNKNOWN.
    # Edge medido: GBPUSD 54.9% (n=102), ETH 56.1% (n=171) — base > 52%.
    # Regras duras: somente ativo validado, somente em sessão, nunca
    # sobrescreve BUY/SELL existente (só preenche o vazio de WAIT).
    _sw_override = False
    if (action not in ("BUY", "SELL")
            and _sw_valid
            and (_sw or {}).get("direction") in ("BUY", "SELL")
            and (_sw or {}).get("in_session")):
        action = str(_sw["direction"])
        _sw_override = True
        reason = (f"SWEEP-REVERSAL ativo: {_sw.get('reason', '')} | "
                  f"pipeline original: WAIT")
        _re_allowed = True
        try:
            from mercury_ai.signals.reentry_engine import (
                MAX_GALES as _MG2, REJECTION_WICK_MIN as _RW2)
            _re_rule = (
                f"Se a vela de entrada fechar contra: reentrar na mesma direção "
                f"na abertura da próxima vela SOMENTE se houver proteção "
                f"(pavio de rejeição >= {_RW2:.0%} do range ou displacement renovado). "
                f"Máx {_MG2} gales (G1/G2); G2 só em Tokyo/London/NY. "
                f"Sem proteção ou após G2: STOP (LOSS_FINAL)."
            )
        except Exception:
            pass

    # Edge Tracker (observável; NUNCA altera decisão/score/ranking):
    # desempenho medido do ativo no histórico real de sinais.
    try:
        from mercury_ai.signals.edge_tracker import symbol_edge as _sym_edge
        _edge = _sym_edge(symbol)
    except Exception:
        _edge = {"edge_n": 0, "edge_winrate": None, "edge_status": "INSUFICIENTE"}

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
        take_profit_1r=take_profit_1r,
        breakeven_trigger=breakeven_trigger,
        exit_plan=exit_plan,
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
        forward_displacement=bool((_fb or {}).get("displacement", False)),
        forward_exhausted=bool((_fb or {}).get("exhausted", False)),
        next_direction=str((_pred or {}).get("direction", "NEUTRAL")),
        next_confidence=float((_pred or {}).get("confidence", 0.0) or 0.0),
        next_reason=" | ".join((_pred or {}).get("reasons", []) or [])[:500],
        next_structure=str((_pred or {}).get("structure", "RANGE")),
        next_key_level=(float((_pred or {}).get("key_level"))
                        if (_pred or {}).get("key_level") is not None else None),
        next_key_kind=str((_pred or {}).get("key_kind", "NONE")),
        next_agrees=_agree,
        session=str(_sess_name) if _sess_name else "UNKNOWN",
        session_liquidity=_sess_liq_f,
        session_thin=_sess_thin,
        trigger_body_ratio=(_inst or {}).get("trigger_body_ratio"),
        trigger_aligned=(_inst or {}).get("trigger_aligned"),
        trigger_range_atr=(_inst or {}).get("trigger_range_atr"),
        ema200_aligned=(_inst or {}).get("ema200_aligned"),
        ema200_dist_atr=(_inst or {}).get("ema200_dist_atr"),
        has_liquidity_sweep=(_inst or {}).get("has_liquidity_sweep"),
        in_premium_discount_zone=(_inst or {}).get("in_premium_discount_zone"),
        has_fvg=(_inst or {}).get("has_fvg"),
        has_inducement=(_inst or {}).get("has_inducement"),
        rsi=(_inst or {}).get("rsi"),
        adx=(_inst or {}).get("adx"),
        plus_di=(_inst or {}).get("plus_di"),
        minus_di=(_inst or {}).get("minus_di"),
        rsi_adx_approved=(_inst or {}).get("rsi_adx_approved"),
        bollinger_pos=(_inst or {}).get("bollinger_pos"),
        rsi_value=(_inst or {}).get("rsi_value"),
        reversal_candle=(_inst or {}).get("reversal_candle"),
        sr_distance=(_inst or {}).get("sr_distance"),
        band_expansion=(_inst or {}).get("band_expansion"),
        bb_upper=(_inst or {}).get("bb_upper"),
        bb_middle=(_inst or {}).get("bb_middle"),
        bb_lower=(_inst or {}).get("bb_lower"),
        bb_bandwidth=(_inst or {}).get("bb_bandwidth"),
        lta_exists=(_inst or {}).get("lta_exists"),
        ltb_exists=(_inst or {}).get("ltb_exists"),
        trendline_bias=(_inst or {}).get("trendline_bias"),
        trendline_aligned=(_inst or {}).get("trendline_aligned"),
        trendline_distance_atr=(_inst or {}).get("trendline_distance_atr"),
        trendline_detail=str((_inst or {}).get("trendline_detail", "") or ""),
        n3_touches=(_n3d or {}).get("n3_touches"),
        n3_level=(_n3d or {}).get("n3_level"),
        n3_tight=(_n3d or {}).get("n3_tight"),
        n3_rejection=(_n3d or {}).get("n3_rejection"),
        n3_wr_hist=(_n3d or {}).get("n3_wr_hist"),
        n3_score=(_n3d or {}).get("n3_score"),
        n3_detail=str((_n3d or {}).get("n3_detail", "") or ""),
        entry_mode=_entry_mode,
        entry_zone=_entry_zone,
        news_risk=str((_nw or {}).get("risk", "UNKNOWN")),
        news_blocked=bool((_nw or {}).get("blocked", False)),
        news_caution=bool((_nw or {}).get("caution", False)),
        news_event=(_nw or {}).get("event"),
        news_detail=str((_nw or {}).get("detail", "") or ""),
        reentry_allowed=_re_allowed,
        reentry_rule=_re_rule,
        sweep_reversal=bool((_sw or {}).get("direction", "NONE") != "NONE"),
        sweep_direction=str((_sw or {}).get("direction", "NONE")),
        sweep_level=(float((_sw or {}).get("swept_level"))
                     if (_sw or {}).get("swept_level") is not None else None),
        sweep_wick=(float((_sw or {}).get("wick_ratio"))
                    if (_sw or {}).get("wick_ratio") is not None else None),
        sweep_asset_validated=_sw_valid,
        sweep_detail=str((_sw or {}).get("reason", "") or ""),
        sweep_override=_sw_override,
        edge_n=_edge.get("edge_n", 0),
        edge_winrate=_edge.get("edge_winrate"),
        edge_status=str(_edge.get("edge_status", "INSUFICIENTE")),
    )
