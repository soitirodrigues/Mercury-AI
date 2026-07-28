"""
Auditoria de Backtest — Fase 17.
Verifica integridade e viés em backtests:
- Data leakage (look-ahead bias)
- Survivorship bias
- Transaction costs (slippage, commission, spread)
- Overfitting (parameter optimization, curve fitting)
- Out-of-sample validation
- Walk-forward analysis
- Monte Carlo / bootstrap validation
- Realistic execution simulation
- Position sizing / risk management
- Performance metrics robustness
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.mercury_integrity_auditor.config import (
    PROJECT_ROOT,
    MERCURY_AI_DIR,
    TESTS_DIR,
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


def _check_data_leakage() -> list[AuditFinding]:
    """Verifica data leakage / look-ahead bias."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    leakage_patterns = []
    future_data_access = []
    shift_usage = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8")
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                # Acesso a dados futuros (shift negativo, iloc futuro)
                if any(kw in stripped for kw in [
                    "shift(-", "shift(-1", "shift(-2", "shift(-3",
                    ".iloc[", ".loc[", "iat[", "at[",
                ]) and any(fw in stripped for fw in [">", "+", "future", "next", "t+1", "t+2"]):
                    future_data_access.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                
                # Uso de shift para features (pode ser leakage se mal usado)
                if "shift(" in stripped and not stripped.startswith("#"):
                    shift_usage.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
                
                # Patterns suspeitos de leakage
                if any(kw in stripped.lower() for kw in [
                    "future", "lookahead", "look-ahead", "peek", "tomorrow",
                    "next_bar", "next_candle", "forward_fill", "ffill",
                ]) and not stripped.startswith("#"):
                    leakage_patterns.append((str(f.relative_to(PROJECT_ROOT)), i+1, stripped[:80]))
        except Exception:
            pass
    
    if future_data_access:
        findings.append(AuditFinding(
            id="BACK-001",
            category="BACKTEST",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title=f"Potential Look-Ahead Bias: {len(future_data_access)}",
            description=f"Acesso a dados futuros detectado: {future_data_access[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="CRÍTICO: Verificar se features usam apenas dados disponíveis no momento da decisão. Usar shift(1+) para features lagged. Nunca usar shift(-n) ou iloc futuro em features de entrada.",
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-001",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title="No Obvious Look-Ahead Bias",
            description="Nenhum acesso óbvio a dados futuros detectado.",
            location=str(MERCURY_AI_DIR),
        ))
    
    if shift_usage:
        findings.append(AuditFinding(
            id="BACK-002",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Shift Usage in Features: {len(shift_usage)}",
            description=f"Uso de shift() em features: {shift_usage[:3]}. Verificar se shift > 0 (lag) e não shift < 0 (lead).",
            location=str(MERCURY_AI_DIR),
            recommendation="Auditar cada uso de shift(). Features devem usar shift(1+) apenas. Target/label pode usar shift(-1) mas NUNCA features de entrada.",
        ))
    
    if leakage_patterns:
        findings.append(AuditFinding(
            id="BACK-003",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Suspicious Leakage Patterns: {len(leakage_patterns)}",
            description=f"Patterns suspeitos: {leakage_patterns[:3]}",
            location=str(MERCURY_AI_DIR),
            recommendation="Revisar cada ocorrência. ffill/bfill pode causar leakage se aplicado antes de split train/test. Forward fill apenas em dados históricos já conhecidos.",
        ))
    
    return findings


def _check_survivorship_bias() -> list[AuditFinding]:
    """Verifica survivorship bias."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    universe_filtering = []
    delisted_handling = []
    static_universe = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8")
            
            # Filtro de universo baseado em performance atual
            if any(kw in content.lower() for kw in [
                "universe", "filter", "select", "screen",
            ]) and any(kw in content.lower() for kw in [
                "volume", "market_cap", "price >", "liquidity",
                "active", "listed", "exist",
            ]):
                universe_filtering.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Tratamento de delisted
            if any(kw in content.lower() for kw in [
                "delisted", "delist", "removed", "suspended",
                "bankrupt", "merged", "acquired",
            ]):
                delisted_handling.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Universo estático (hardcoded)
            if any(kw in content for kw in [
                "SYMBOLS =", "TICKERS =", "UNIVERSE =", "ASSETS =",
                "['AAPL'", "['PETR4'", "['VALE3'",
            ]):
                static_universe.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if universe_filtering and not delisted_handling:
        findings.append(AuditFinding(
            id="BACK-004",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Universe Filtering Without Delisted Handling: {len(set(universe_filtering))} files",
            description=f"Filtro de universo detectado mas sem tratamento de delisted: {', '.join(list(set(universe_filtering))[:3])}",
            location=str(MERCURY_AI_DIR),
            recommendation="Survivorship bias: usar universo point-in-time (PIT). Incluir ativos delisted/merged. Usar dados de constituintes históricos de índices. Não filtrar apenas ativos que 'sobreviveram'.",
        ))
    elif delisted_handling:
        findings.append(AuditFinding(
            id="BACK-004",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title="Delisted Handling Found",
            description=f"Tratamento de ativos delisted: {', '.join(list(set(delisted_handling))[:3])}",
            location=str(MERCURY_AI_DIR),
        ))
    
    if static_universe:
        findings.append(AuditFinding(
            id="BACK-005",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Static Universe Detected: {len(set(static_universe))} files",
            description=f"Universo hardcoded/estático: {', '.join(list(set(static_universe))[:3])}. Risco de survivorship bias.",
            location=str(MERCURY_AI_DIR),
            recommendation="Usar universo dinâmico point-in-time. Carregar constituintes históricos de benchmarks (IBOV, SP500, etc.) na data de cada rebalance.",
        ))
    
    return findings


def _check_transaction_costs() -> list[AuditFinding]:
    """Verifica custos de transação realistas."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    has_commission = False
    has_slippage = False
    has_spread = False
    has_market_impact = False
    cost_values = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if any(kw in content for kw in ["commission", "comissao", "fee", "taxa", "brokerage"]):
                has_commission = True
            if any(kw in content for kw in ["slippage", "slip", "deslizamento"]):
                has_slippage = True
            if any(kw in content for kw in ["spread", "bid_ask", "bidask", "bid-ask"]):
                has_spread = True
            if any(kw in content for kw in ["market_impact", "impact", "market impact", "slippage_model"]):
                has_market_impact = True
            
            # Extrai valores numéricos de custos
            import re
            for match in re.finditer(r'(commission|fee|slippage|spread)\s*[=:]\s*([\d.]+)', content):
                cost_values.append((str(f.relative_to(PROJECT_ROOT)), match.group(1), match.group(2)))
        except Exception:
            pass
    
    cost_components = sum([has_commission, has_slippage, has_spread, has_market_impact])
    
    if cost_components >= 3:
        findings.append(AuditFinding(
            id="BACK-006",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title=f"Comprehensive Transaction Costs: {cost_components}/4 components",
            description=f"Commission={has_commission}, Slippage={has_slippage}, Spread={has_spread}, MarketImpact={has_market_impact}. Values: {cost_values[:5]}",
            location=str(MERCURY_AI_DIR),
        ))
    elif cost_components >= 1:
        findings.append(AuditFinding(
            id="BACK-006",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Partial Transaction Costs: {cost_components}/4 components",
            description=f"Commission={has_commission}, Slippage={has_slippage}, Spread={has_spread}, MarketImpact={has_market_impact}. Faltando componentes.",
            location=str(MERCURY_AI_DIR),
            recommendation="Adicionar todos: commission (fixo + %), slippage (bps ou % do volume), spread (bid-ask), market impact (função do volume/ADV). Calibrar com dados reais.",
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-006",
            category="BACKTEST",
            severity=CRITICAL,
            status=STATUS_FAIL,
            title="No Transaction Costs Modeled",
            description="Nenhum custo de transação detectado. Backtest sem custos = resultados irreais.",
            location=str(MERCURY_AI_DIR),
            recommendation="CRÍTICO: Implementar custos realistas. Mínimo: commission + slippage. Idealmente: spread + market impact. Validar com corretora/dados reais.",
        ))
    
    return findings


def _check_overfitting() -> list[AuditFinding]:
    """Verifica overfitting / curve fitting."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    param_optimization = []
    grid_search = []
    walk_forward = []
    purged_cv = []
    combinatorial = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            # Otimização de parâmetros
            if any(kw in content for kw in [
                "optimize", "optuna", "hyperopt", "bayesian",
                "parameter", "param_grid", "grid_search", "gridsearch",
                "random_search", "randomsearch",
            ]):
                param_optimization.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Grid search explícito
            if "grid_search" in content or "gridsearch" in content or "param_grid" in content:
                grid_search.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Walk-forward
            if any(kw in content for kw in [
                "walk_forward", "walkforward", "walk forward",
                "expanding_window", "rolling_window", "time_series_split",
            ]):
                walk_forward.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Purged/Embargo CV (Lopez de Prado)
            if any(kw in content for kw in [
                "purged", "embargo", "combinatorial_purged", "cv_purged",
                "mlfinlab", "cross_validation",
            ]):
                purged_cv.append(str(f.relative_to(PROJECT_ROOT)))
            
            # Explosão combinatória
            if any(kw in content for kw in [
                "itertools.product", "product(", "combinations(",
                "parameter_space", "search_space",
            ]):
                combinatorial.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if param_optimization and not walk_forward and not purged_cv:
        findings.append(AuditFinding(
            id="BACK-007",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title=f"Parameter Optimization Without Robust Validation: {len(set(param_optimization))} files",
            description=f"Otimização detectada: {', '.join(list(set(param_optimization))[:3])}. Sem walk-forward ou purged CV.",
            location=str(MERCURY_AI_DIR),
            recommendation="Overfitting risk alto. Usar: walk-forward analysis, purged/embargo CV (Lopez de Prado), nested CV. Separar train/val/test temporalmente. Limitar parâmetros (Occam's razor).",
        ))
    elif walk_forward or purged_cv:
        findings.append(AuditFinding(
            id="BACK-007",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title="Robust Validation Found",
            description=f"Walk-forward={len(walk_forward)}, PurgedCV={len(purged_cv)}",
            location=str(MERCURY_AI_DIR),
        ))
    
    if grid_search and combinatorial:
        findings.append(AuditFinding(
            id="BACK-008",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="Large Parameter Space Search",
            description=f"Grid search + espaço combinatório grande: {len(set(grid_search))} grid, {len(set(combinatorial))} combinatorial. Risco de multiple testing / data snooping.",
            location=str(MERCURY_AI_DIR),
            recommendation="Corrigir multiple testing: Bonferroni, FDR, ou usar Bayesian optimization com prior. Definir search space pequeno e justificado. Preferir fewer params com economic rationale.",
        ))
    
    return findings


def _check_out_of_sample() -> list[AuditFinding]:
    """Verifica validação out-of-sample."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    oos_split = []
    train_test_split = []
    temporal_split = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if any(kw in content for kw in [
                "out_of_sample", "outofsample", "oos", "test_set",
                "holdout", "hold_out", "validation_set",
            ]):
                oos_split.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "train_test_split", "train_test", "test_size",
                "sklearn.model_selection", "train_test_split",
            ]):
                train_test_split.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "time_series_split", "timeseriessplit", "temporal",
                "date_split", "split_by_date", "cutoff_date",
            ]):
                temporal_split.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if oos_split or temporal_split:
        findings.append(AuditFinding(
            id="BACK-009",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title="Out-of-Sample Validation Found",
            description=f"OOS={len(oos_split)}, TemporalSplit={len(temporal_split)}",
            location=str(MERCURY_AI_DIR),
        ))
    elif train_test_split and not temporal_split:
        findings.append(AuditFinding(
            id="BACK-009",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Random Train/Test Split (Not Temporal)",
            description=f"train_test_split aleatório detectado: {', '.join(list(set(train_test_split))[:3])}. Vaza informação temporal!",
            location=str(MERCURY_AI_DIR),
            recommendation="NUNCA usar random split em séries temporais. Usar TimeSeriesSplit, cutoff date, ou expanding/rolling window. Train deve ser estritamente anterior a test.",
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-009",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="No Explicit Out-of-Sample Validation",
            description="Não há validação out-of-sample explícita detectada.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar: split temporal (ex: 70/30 por data), walk-forward, ou purged CV. Reportar métricas OOS separadamente de in-sample.",
        ))
    
    return findings


def _check_walk_forward() -> list[AuditFinding]:
    """Verifica walk-forward analysis."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    walk_forward = []
    anchored = []
    rolling = []
    expanding = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if "walk_forward" in content or "walkforward" in content:
                walk_forward.append(str(f.relative_to(PROJECT_ROOT)))
            if "anchored" in content and "walk" in content:
                anchored.append(str(f.relative_to(PROJECT_ROOT)))
            if "rolling" in content and ("window" in content or "retrain" in content):
                rolling.append(str(f.relative_to(PROJECT_ROOT)))
            if "expanding" in content and ("window" in content or "retrain" in content):
                expanding.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if walk_forward or anchored or rolling or expanding:
        findings.append(AuditFinding(
            id="BACK-010",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title="Walk-Forward Analysis Found",
            description=f"WalkForward={len(walk_forward)}, Anchored={len(anchored)}, Rolling={len(rolling)}, Expanding={len(expanding)}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-010",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title="No Walk-Forward Analysis",
            description="Não há walk-forward analysis detectado. Single backtest = overfitting risk.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar walk-forward: anchored (fixed train start) ou rolling (fixed train size). Re-treinar/otimizar a cada período. Reportar métricas agregadas OOS.",
        ))
    
    return findings


def _check_monte_carlo() -> list[AuditFinding]:
    """Verifica Monte Carlo / bootstrap validation."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    monte_carlo = []
    bootstrap = []
    permutation = []
    synthetic = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if any(kw in content for kw in [
                "monte_carlo", "montecarlo", "mc_simulation",
                "simulate", "simulation",
            ]):
                monte_carlo.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "bootstrap", "resample", "resampling",
            ]):
                bootstrap.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "permutation", "shuffle", "randomize",
            ]):
                permutation.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "synthetic", "generate_data", "fake_data",
                "garch", "hmm", "regime",
            ]):
                synthetic.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    if monte_carlo or bootstrap or permutation or synthetic:
        findings.append(AuditFinding(
            id="BACK-011",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title="Monte Carlo / Bootstrap Validation Found",
            description=f"MC={len(monte_carlo)}, Bootstrap={len(bootstrap)}, Permutation={len(permutation)}, Synthetic={len(synthetic)}",
            location=str(MERCURY_AI_DIR),
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-011",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_INFO,
            title="No Monte Carlo / Bootstrap Validation",
            description="Não há validação via Monte Carlo, bootstrap, ou permutation tests.",
            location=str(MERCURY_AI_DIR),
            recommendation="Adicionar: bootstrap confidence intervals para métricas, permutation test para significância, Monte Carlo para path distribution. Útil para validar robustez de Sharpe, drawdown, etc.",
        ))
    
    return findings


def _check_execution_simulation() -> list[AuditFinding]:
    """Verifica simulação de execução realista."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    order_types = []
    partial_fills = []
    rejection = []
    latency = []
    queue_position = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if any(kw in content for kw in [
                "limit_order", "market_order", "stop_order", "stop_limit",
                "order_type", "ordertype",
            ]):
                order_types.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "partial_fill", "partialfill", "fill_ratio",
                "partial", "filled_qty", "remaining",
            ]):
                partial_fills.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "reject", "rejected", "cancel", "cancelled",
                "order_reject", "cancel_reject",
            ]):
                rejection.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "latency", "delay", "execution_delay",
                "network_latency", "processing_time",
            ]):
                latency.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "queue", "queue_position", "priority",
                "time_priority", "price_time",
            ]):
                queue_position.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    realism_score = sum([
        len(order_types) > 0,
        len(partial_fills) > 0,
        len(rejection) > 0,
        len(latency) > 0,
        len(queue_position) > 0,
    ])
    
    if realism_score >= 3:
        findings.append(AuditFinding(
            id="BACK-012",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title=f"Realistic Execution Simulation: {realism_score}/5",
            description=f"OrderTypes={len(order_types)>0}, PartialFills={len(partial_fills)>0}, Rejection={len(rejection)>0}, Latency={len(latency)>0}, Queue={len(queue_position)>0}",
            location=str(MERCURY_AI_DIR),
        ))
    elif realism_score >= 1:
        findings.append(AuditFinding(
            id="BACK-012",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Partial Execution Simulation: {realism_score}/5",
            description=f"Simulação parcial. Faltando: order types, partial fills, rejection, latency, queue position.",
            location=str(MERCURY_AI_DIR),
            recommendation="Melhorar simulador: suportar limit/market/stop orders, partial fills, rejects/cancels, latency model, queue position para limit orders. Usar dados de book (L2) se disponível.",
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-012",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Naive Execution Simulation",
            description="Simulação de execução ingênua (preço de fechamento, fill instantâneo, sem rejeição).",
            location=str(MERCURY_AI_DIR),
            recommendation="CRÍTICO para live trading: implementar simulador realista. Mínimo: slippage model + commission. Idealmente: order book simulation, latency, partial fills, rejects.",
        ))
    
    return findings


def _check_position_sizing_risk() -> list[AuditFinding]:
    """Verifica position sizing e risk management no backtest."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    position_sizing = []
    kelly = []
    volatility_target = []
    max_position = []
    stop_loss = []
    drawdown_control = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if any(kw in content for kw in [
                "position_size", "positionsize", "sizing",
                "allocat", "weight", "capital_alloc",
            ]):
                position_sizing.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "kelly", "kelly_criterion", "kellycriterion",
            ]):
                kelly.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "vol_target", "volatility_target", "target_vol",
                "risk_parity", "riskparity",
            ]):
                volatility_target.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "max_position", "maxposition", "position_limit",
                "max_weight", "maxweight", "concentration",
            ]):
                max_position.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "stop_loss", "stoploss", "stop_loss_pct",
                "trailing_stop", "trailingstop",
            ]):
                stop_loss.append(str(f.relative_to(PROJECT_ROOT)))
            
            if any(kw in content for kw in [
                "max_drawdown", "maxdrawdown", "drawdown_limit",
                "dd_limit", "risk_limit",
            ]):
                drawdown_control.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    risk_components = sum([
        len(position_sizing) > 0,
        len(kelly) > 0 or len(volatility_target) > 0,
        len(max_position) > 0,
        len(stop_loss) > 0,
        len(drawdown_control) > 0,
    ])
    
    if risk_components >= 3:
        findings.append(AuditFinding(
            id="BACK-013",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title=f"Comprehensive Risk Management: {risk_components}/5",
            description=f"PositionSizing={len(position_sizing)>0}, VolTarget/Kelly={len(kelly)>0 or len(volatility_target)>0}, MaxPos={len(max_position)>0}, StopLoss={len(stop_loss)>0}, DDControl={len(drawdown_control)>0}",
            location=str(MERCURY_AI_DIR),
        ))
    elif risk_components >= 1:
        findings.append(AuditFinding(
            id="BACK-013",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Partial Risk Management: {risk_components}/5",
            description=f"Gestão de risco parcial. Componentes: sizing, vol target, max pos, stop loss, drawdown control.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar framework completo: position sizing (vol target/kelly), max position/concentration limits, stop loss/trailing, max drawdown circuit breaker. Backtest deve respeitar mesmos limites do live.",
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-013",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title="No Risk Management in Backtest",
            description="Backtest sem position sizing ou risk management. Resultados não representam estratégia real.",
            location=str(MERCURY_AI_DIR),
            recommendation="Adicionar risk management idêntico ao live: position sizing, limits, stops, drawdown controls. Backtest sem risk mgmt = overstated returns.",
        ))
    
    return findings


def _check_performance_metrics() -> list[AuditFinding]:
    """Verifica robustez de métricas de performance."""
    findings = []
    
    py_files = list(MERCURY_AI_DIR.rglob("*.py"))
    test_files = list(TESTS_DIR.rglob("*.py"))
    all_files = py_files + test_files
    
    metrics_used = []
    sharpe = []
    sortino = []
    calmar = []
    max_dd = []
    var_cvar = []
    tail_ratio = []
    statistical_significance = []
    
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8").lower()
            
            if any(kw in content for kw in [
                "sharpe", "sortino", "calmar", "sterling",
                "information_ratio", "treynor", "jensen",
            ]):
                metrics_used.append(str(f.relative_to(PROJECT_ROOT)))
            
            if "sharpe" in content:
                sharpe.append(str(f.relative_to(PROJECT_ROOT)))
            if "sortino" in content:
                sortino.append(str(f.relative_to(PROJECT_ROOT)))
            if "calmar" in content:
                calmar.append(str(f.relative_to(PROJECT_ROOT)))
            if "max_drawdown" in content or "maxdrawdown" in content:
                max_dd.append(str(f.relative_to(PROJECT_ROOT)))
            if any(kw in content for kw in ["var(", "cvar", "conditional_var", "expected_shortfall", "es_"]):
                var_cvar.append(str(f.relative_to(PROJECT_ROOT)))
            if any(kw in content for kw in ["tail_ratio", "tailratio", "gain_to_pain", "profit_factor"]):
                tail_ratio.append(str(f.relative_to(PROJECT_ROOT)))
            if any(kw in content for kw in [
                "p_value", "pvalue", "significance", "t_test", "ttest",
                "bootstrap_ci", "confidence_interval",
            ]):
                statistical_significance.append(str(f.relative_to(PROJECT_ROOT)))
        except Exception:
            pass
    
    metric_diversity = sum([
        len(sharpe) > 0,
        len(sortino) > 0,
        len(calmar) > 0,
        len(max_dd) > 0,
        len(var_cvar) > 0,
        len(tail_ratio) > 0,
    ])
    
    if metric_diversity >= 4 and statistical_significance:
        findings.append(AuditFinding(
            id="BACK-014",
            category="BACKTEST",
            severity=LOW,
            status=STATUS_PASS,
            title=f"Robust Performance Metrics: {metric_diversity}/6 + Statistical Significance",
            description=f"Sharpe={len(sharpe)>0}, Sortino={len(sortino)>0}, Calmar={len(calmar)>0}, MaxDD={len(max_dd)>0}, VaR/CVaR={len(var_cvar)>0}, TailRatio={len(tail_ratio)>0}, StatSig={len(statistical_significance)>0}",
            location=str(MERCURY_AI_DIR),
        ))
    elif metric_diversity >= 2:
        findings.append(AuditFinding(
            id="BACK-014",
            category="BACKTEST",
            severity=MEDIUM,
            status=STATUS_WARNING,
            title=f"Limited Performance Metrics: {metric_diversity}/6",
            description=f"Métricas limitadas. Sharpe sozinho é insuficiente. Adicionar: Sortino, Calmar, MaxDD, VaR/CVaR, Tail Ratio. Testar significância estatística.",
            location=str(MERCURY_AI_DIR),
            recommendation="Reportar múltiplas métricas. Sharpe assume normalidade - usar Sortino (downside risk), Calmar (drawdown), VaR/CVaR (tail risk). Adicionar confidence intervals via bootstrap.",
        ))
    else:
        findings.append(AuditFinding(
            id="BACK-014",
            category="BACKTEST",
            severity=HIGH,
            status=STATUS_WARNING,
            title="Insufficient Performance Metrics",
            description="Métricas de performance insuficientes ou apenas Sharpe. Não captura tail risk, drawdown, significância.",
            location=str(MERCURY_AI_DIR),
            recommendation="Implementar suite completa: return, vol, Sharpe, Sortino, Calmar, MaxDD, VaR 95/99, CVaR, Tail Ratio, Profit Factor. Bootstrap CI para todas. Testar significância vs benchmark.",
        ))
    
    return findings


def run() -> AuditSection:
    """Executa a auditoria de backtest."""
    section = AuditSection(
        name="17. Backtest Audit",
        description="Verifica integridade de backtests: data leakage, survivorship bias, transaction costs, overfitting, OOS validation, walk-forward, Monte Carlo, execution simulation, risk management, performance metrics",
    )
    
    all_findings = []
    all_findings.extend(_check_data_leakage())
    all_findings.extend(_check_survivorship_bias())
    all_findings.extend(_check_transaction_costs())
    all_findings.extend(_check_overfitting())
    all_findings.extend(_check_out_of_sample())
    all_findings.extend(_check_walk_forward())
    all_findings.extend(_check_monte_carlo())
    all_findings.extend(_check_execution_simulation())
    all_findings.extend(_check_position_sizing_risk())
    all_findings.extend(_check_performance_metrics())
    
    section.findings = all_findings
    
    has_fail = any(f.status == STATUS_FAIL for f in all_findings)
    has_warning = any(f.status == STATUS_WARNING for f in all_findings)
    
    if has_fail:
        section.status = STATUS_FAIL
    elif has_warning:
        section.status = STATUS_WARNING
    else:
        section.status = STATUS_PASS
    
    return section