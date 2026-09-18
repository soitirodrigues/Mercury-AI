from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME


@dataclass(frozen=True)
class Signal:
    """
    SIGNAL operacional formal (S33-E.6).

    Completa o contrato existente em vez de criar um segundo modelo.
    PROPAGACAO pura: nenhum campo aqui altera thresholds/pesos/engines.
    Campos legados (asset/action/entry/explanation) preservados para
    compatibilidade; symbol/decision/entry_price sao aliases operacionais.

    ENTRY WINDOW RULE (derivada de signal_ts/last_m5_ts/next_m5_ts):
    next_m5_ts = strict ceil M5 apos last_m5_ts; VALID sse
    signal_ts < next_m5_ts (janela [signal_ts, next_m5_ts), seconds > 0),
    EXPIRED caso contrario (protecao contra falso timing).
    """

    asset: str

    action: str

    confidence: float

    score: float

    entry: float | None = None

    stop_loss: float | None = None

    take_profit: float | None = None

    timeframe: str = DEFAULT_TIMEFRAME

    strategy: str = ""

    evidences: Tuple[str, ...] = field(default_factory=tuple)

    explanation: str = ""

    # --- S33-E.6: identidade/temporal (operacional) ---
    signal_id: str = ""
    signal_ts: Optional[str] = None
    last_m5_ts: Optional[str] = None
    next_m5_ts: Optional[str] = None
    entry_price: float | None = None
    entry_window_start: Optional[str] = None
    entry_window_end: Optional[str] = None
    entry_window_seconds: float = 0.0
    seconds_to_next_m5: Optional[float] = None
    entry_valid_for_next_m5: bool = False
    entry_timing_state: str = "EXPIRED"

    # --- S33-E.6: risco (propagado do RiskEngine, sem recalculo) ---
    invalidation: float | None = None
    risk_reward: float = 0.0

    # --- Exit plan TP1+BE (propagado do RiskEngine; sem recalculo) ---
    take_profit_1r: float | None = None
    breakeven_trigger: float | None = None
    exit_plan: str = "TP1_50_BE_RUNNER_2R"

    # --- S33-E.6: decisao (propagada, sem alterar regras) ---
    probability_buy: float = 0.0
    probability_sell: float = 0.0
    probability_wait: float = 0.0
    confluence: float = 0.0
    quality: float = 0.0
    institutional_score: float = 0.0
    grade: str = "N/A"
    mtf_summary: Dict[str, Any] = field(default_factory=dict)
    market_regime: str = "UNKNOWN"
    reason: str = ""
    audit_id: str = ""

    # --- Forward-bias M5 (classificação p/ PRÓXIMA vela; sem alterar decisão) ---
    forward_state: str = "EXPIRED"
    forward_reason: str = ""
    forward_direction: str = "NONE"
    # Flags SMC do forward (p/ gates automáticos; sem alterar decisão):
    # displacement=True => trigger N é vela de força (exigido p/ selo A);
    # exhausted=True => pavio oposto dominante/corpo raquítico (corta selo A/B).
    forward_displacement: bool = False
    forward_exhausted: bool = False

    # --- Sessão operacional (propagada de session_analysis; sem recalcular) ---
    # session_thin=True => liquidez<50 (SYDNEY fina): spread/slippage alto
    # na Hezilex — capa selo em C automaticamente (gate F8 automático).
    session: str = "UNKNOWN"
    session_liquidity: float | None = None
    session_thin: bool = False

    # --- Preditor da PRÓXIMA vela (SMC estrutural: topos/fundos; sem alterar decisão) ---
    # direction: BULLISH/BEARISH/NEUTRAL — para onde o preço VAI em N+1.
    # agrees: True concorda c/ decision | False discorda (gate G4) | None NEUTRAL/sem direção.
    next_direction: str = "NEUTRAL"
    next_confidence: float = 0.0
    next_reason: str = ""
    next_structure: str = "RANGE"
    next_key_level: float | None = None
    next_key_kind: str = "NONE"
    next_agrees: bool | None = None

    # --- Filtros institucionais M5 (observáveis puros; sem bloquear) ---
    # Calculados por mercury_ai.signals.m5_institutional_filters sobre df_closed
    # (só velas fechadas). Propagação pura p/ auditoria/exibição — nenhum gate
    # bloqueante: amostra 55 ciclos/127 TOP3 não sustenta bloqueio (G0 49.6%).
    # trigger_body_ratio: corpo/range da trigger N (mediana WIN 0.634 vs LOSS 0.513).
    # trigger_aligned: trigger N fechou na direção da decisão (None = doji/sem direção).
    # trigger_range_atr: range_N / ATR14 (p75 WIN 1.495 vs LOSS 1.082; cap 2.0).
    # ema200_aligned: close_N vs EMA200 a favor (50.5% vs 47.2% — sem edge isolado).
    # ema200_dist_atr: |px-EMA200|/ATR14 (None se df < 200 fechadas).
    trigger_body_ratio: float | None = None
    trigger_aligned: bool | None = None
    trigger_range_atr: float | None = None
    ema200_aligned: bool | None = None
    ema200_dist_atr: float | None = None
    # --- SMC Engine (4 métricas pedidas; observáveis, sem bloquear) ---
    # has_liquidity_sweep: sweep estrutural (lookback 20) a favor da decisão.
    # has_fvg: FVG/im-balance aberto a favor (gap >= 0.2*ATR, não preenchido).
    # has_inducement: mini-sweep interno (lookback 5, 12 velas) — indução do varejo.
    # in_premium_discount_zone: preço no lado institucional da fib 50% (BUY<50%, SELL>50%).
    # Medição 2026-09-14: FVG-ok 55.3%, FVG+IDM 59.3%, combo+zona 83.3% (5/6, n.s.)
    # => LINHA DE ESTUDO, nunca bloqueio (cobertura 4.7%).
    has_liquidity_sweep: bool | None = None
    in_premium_discount_zone: bool | None = None
    has_fvg: bool | None = None
    has_inducement: bool | None = None
    # --- RSI+ADX audit-only (2026-09-15; observavel, NUNCA bloqueia) ---
    # rsi: RSI-14 Wilder (0-100, 50 neutro). adx: forca tendencia (trend>=20).
    # plus_di/minus_di: direcao (+DI>-DI => comprador domina).
    # rsi_adx_approved: True=>passa no gate auditivo; False=>rejeitado por
    # lateralidade/exaustao; None=>incalculavel. Agregado 38 ativos
    # 48.98%->48.46% (-0.52pp): NAO usar como bloqueio.
    rsi: float | None = None
    adx: float | None = None
    plus_di: float | None = None
    minus_di: float | None = None
    rsi_adx_approved: bool | None = None
    # --- Prompt-analise M5 audit-only (2026-09-15; mesmo padrao, NUNCA bloqueia) ---
    # bollinger_pos: posicao close_N vs BB20/2 (ABOVE_UPPER|TOUCH_UPPER|INSIDE|
    #   TOUCH_LOWER|BELOW_LOWER). rsi_value: alias nominal de rsi (prompt).
    # reversal_candle: BULLISH_REVERSAL|BEARISH_REVERSAL|NONE (martelo/engolfo).
    # sr_distance: distancia ao S/R (pivot 3, 48 fechadas) em ATRs.
    # band_expansion: True=bandas abrindo | False=contraindo | None=incalculavel.
    # bb_upper/middle/lower/bandwidth: valores BB20/2 p/ painel/logs.
    bollinger_pos: str | None = None
    rsi_value: float | None = None
    reversal_candle: str | None = None
    sr_distance: float | None = None
    band_expansion: bool | None = None
    bb_upper: float | None = None
    bb_middle: float | None = None
    bb_lower: float | None = None
    bb_bandwidth: float | None = None
    # --- Trendlines LTA/LTB audit-only (2026-09-15; mesmo padrao, NUNCA bloqueia) ---
    # lta_exists/ltb_exists: diagonal valida (>=2 toques, slope certo).
    # trendline_bias: BULLISH (LTA intacta) | BEARISH (LTB intacta) | NEUTRAL.
    # trendline_aligned: True=a favor da decisao | False=rompida/contra | None=sem diagonal.
    # trendline_distance_atr: distancia do close a linha do lado da decisao (ATRs).
    # trendline_detail: "LTA 3 toques slope ... + LTB ..." p/ painel.
    lta_exists: bool | None = None
    ltb_exists: bool | None = None
    trendline_bias: str | None = None
    trendline_aligned: bool | None = None
    trendline_distance_atr: float | None = None
    trendline_detail: str = ""
    # --- Filtro noticias audit-only (2026-09-15; mesmo padrao, NUNCA bloqueia motor) ---
    # news_risk: BLOCK (3★ ±30min: EVITAR) | CAUTION (2★ ±30min: forca nas velas,
    #   exigir confirmacao extra) | CLEAR | UNKNOWN. blocked/caution: bools p/ selo.
    # news_event: "NFP (USD 3★ 09:30)" | None. news_detail: frase p/ painel.
    news_risk: str = "CLEAR"
    news_blocked: bool = False
    news_caution: bool = False
    news_event: str | None = None
    news_detail: str = ""
    # --- Selo N3 audit-only (2026-09-16; mesmo padrao, NUNCA bloqueia) ---
    # Reversao em topos/fundos multiplos: >=3 toques sem rompimento.
    # n3_touches/n3_level: zona a favor (None = sem zona). n3_tight: True =
    # amplitude <=0.1% (padrao ouro do protocolo). n3_rejection: pinbar/engolfo
    # na trigger. n3_wr_hist: win rate do backtest do ativo (None se n<5).
    # n3_score: toques x wr x bonus_rejeicao x prox (p/ Top-3 N3 e painel).
    n3_touches: int | None = None
    n3_level: float | None = None
    n3_tight: bool | None = None
    n3_rejection: bool | None = None
    n3_wr_hist: float | None = None
    n3_score: float | None = None
    n3_detail: str = ""
    # --- Entry mode (2026-09-16; EXECUCAO, nunca filtro de sinal) ---
    # LIMIT_OTE (preferencial: limite na regiao OTE/FVG) vs MARKET
    # (vela exausta/sem pullback). Calculado por signal_builder a partir
    # de has_fvg +OTE: com FVG aberto => LIMIT_OTE, sem => MARKET.
    # Nao altera decisao/score/ranking; so orienta o executor.
    entry_mode: str = "MARKET"
    entry_zone: float | None = None

    # --- Reentrada protegida G1/G2 (2026-09-16; PLANO prospectivo, nunca bloqueia) ---
    # Plano de reentrada emitido JUNTO com o sinal (como a IA de referência):
    # reentry_allowed: True = se a vela de entrada fechar contra COM proteção
    #   (pavio de rejeição >=40% ou displacement renovado), reentrar na mesma
    #   direção na abertura da próxima vela. False = não reentrar (stop seco).
    # reentry_max_gales: teto de reentradas (2 = G1+G2). reentry_g2_session_only:
    #   G2 só em Tokyo/London/NY. reentry_rule: texto legível p/ painel.
    # Campos de FEEDBACK (preenchidos pós-fechamento pelo outcome engine):
    # reentry_result: WIN | REENTRY_G1 | REENTRY_G2 | LOSS_FINAL | None (aberto).
    # reentry_gales_used: quantos gales foram usados no desfecho.
    reentry_allowed: bool = True
    reentry_max_gales: int = 2
    reentry_g2_session_only: bool = True
    reentry_rule: str = ""
    reentry_result: str | None = None
    reentry_gales_used: int | None = None

    # --- Liquidity Sweep Reversal (2026-09-17; observável, NUNCA bloqueia) ---
    # Edge medido fora da amostra: GBPUSD base 54.8-55.7% (treino/teste),
    # combinada c/ 2 gales 92.9%. Válido SÓ em ativos validados (GBP*).
    # sweep_reversal: True = última vela fechada é sweep+rejeição válido.
    # sweep_direction/sweep_level/sweep_wick: direção, nível varrido, pavio.
    # sweep_asset_validated: ativo tem edge medido p/ este padrão.
    # sweep_detail: texto auditável p/ painel.
    sweep_reversal: bool = False
    sweep_direction: str = "NONE"
    sweep_level: float | None = None
    sweep_wick: float | None = None
    sweep_asset_validated: bool = False
    sweep_detail: str = ""
    # sweep_override: True = este sinal foi GERADO pelo sweep engine (pipeline
    # original era WAIT). Marca explícita p/ auditoria — nunca esconde origem.
    sweep_override: bool = False

    # --- Edge Tracker (2026-09-18; observável, NUNCA bloqueia) ---
    # Desempenho medido do ativo no histórico real (reports/top3_*.jsonl).
    # edge_n: amostra; edge_winrate: assertividade combinada (com gales);
    # edge_status: EDGE (>=60%) | NEUTRO | ANTI_EDGE (<=35% e n>=10) |
    # INSUFICIENTE (n<5). Bloqueio automático NUNCA — decisão do operador.
    edge_n: int = 0
    edge_winrate: float | None = None
    edge_status: str = "INSUFICIENTE"

    @property
    def symbol(self) -> str:
        """Alias operacional: symbol == asset (contrato S33-E.6)."""
        return self.asset

    @property
    def decision(self) -> str:
        """Alias operacional: decision == action (contrato S33-E.6)."""
        return self.action

    @property
    def valid_for_next_m5(self) -> bool:
        """Alias legivel da validade temporal."""
        return self.entry_valid_for_next_m5

    def to_dict(self) -> Dict[str, Any]:
        """Serializa TODOS os campos (nenhum campo critico some)."""
        data = asdict(self)
        # aliases operacionais exigidos pelo contrato (transportaveis)
        data["symbol"] = self.asset
        data["decision"] = self.action
        return data