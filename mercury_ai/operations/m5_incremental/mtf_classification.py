"""MTF — classificação de reusabilidade por componente.

Investiga gargalo MTFAnalysis ~78% e classifica cada componente.
NÃO assume que qualquer indicador pode ser incremental.

Categorias:
  SAFE_INCREMENTAL      — pode reutilizar quando só 1 vela M5 mudou
  REQUIRES_FULL_RECALC  — exige recálculo integral
  UNKNOWN               — não otimizar silenciosamente
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(frozen=True)
class ComponentClassification:
    component: str
    verdict: str  # SAFE_INCREMENTAL | REQUIRES_FULL_RECALC | UNKNOWN
    reason: str
    evidence: str


# Classificação baseada em inspeção de código 2026-09-02
# Critério: se o componente é stateless sobre janela rolante e depende de
#  toda a janela histórica (rolling ewm com span grande), não é SAFE_INCREMENTAL
#  sem prova de equivalência matemática.

MTF_CLASSIFICATIONS: List[ComponentClassification] = [
    # ── Por timeframe / por engine dentro de MTFEngine.analyze ──
    ComponentClassification(
        component="MarketDataService.get_data(TF, period=1mo) — fetch",
        verdict="REQUIRES_FULL_RECALC",
        reason="Cada TF baixa janela de 1 mês via yfinance. Não há fetcher incremental por vela; "
               "última vela precisa ser buscada do provider. Cache só seguro com candle-timestamp check.",
        evidence="MTFEngine.analyze loopa 5 TFs com MarketDataService.get_data(symbol, interval=TF_interval, period=1mo) sequencialmente.",
    ),
    ComponentClassification(
        component="IndicatorEngine.calculate(df) por TF (EMA 9/21/50, RSI14, ATR14, MACD, Bollinger14)",
        verdict="REQUIRES_FULL_RECALC",
        reason="Indicadores são rolling stateful sobre janela inteira (ewm span até 50, rolling 14). "
               "Recálculo incremental exigiria manter estado e aplicar delta; implementação atual recalcula df.copy() integralmente. "
               "Não há prova de equivalência incremental.",
        evidence="IndicatorEngine.calculate faz df.copy() + ewm/rolling sobre close/high/low/volume full-window.",
    ),
    ComponentClassification(
        component="TrendAnalyzer.analyze(market) por TF",
        verdict="UNKNOWN",
        reason="Depende de MarketData (indicadores) e lógica de tendência; se MarketData for incremental, Trend poderia ser SAFE, "
               "mas não há teste de equivalência incremental vs full recalc.",
        evidence="TrendAnalyzer consome MarketData (já derivado de IndicatorEngine). Sem teste de paridade.",
    ),
    ComponentClassification(
        component="LiquidityEngine.analyze(df, swings, profile) por TF",
        verdict="UNKNOWN",
        reason="Depende de swing detection sobre df full + MarketStructure profile. Swing detection é sensível a pivot window "
               "e pode mudar com 1 nova vela, mas não provado se pode ser incremental.",
        evidence="MTFEngine: swings, _ = structure.swing_engine.detect_swings(df); profile, str_evs = structure.evaluate(df); liquidity.analyze(df, swings, profile)",
    ),
    ComponentClassification(
        component="VolatilityEngine.analyze(df, market) por TF",
        verdict="UNKNOWN",
        reason="ATR e volatilidade são rolling; mesma cautela de IndicatorEngine. Não classificado como SAFE sem prova.",
        evidence="VolatilityEngine consome df + market (indicadores).",
    ),
    ComponentClassification(
        component="MarketStructureIntelligenceEngine (swing + profile) por TF",
        verdict="REQUIRES_FULL_RECALC",
        reason="detect_swings e evaluate dependem de janela histórica para pivôs e estrutura (BOS/CHoCH). "
               "1 nova vela pode invalidar pivôs anteriores; reuso exigiria recomputar estrutura sobre janela nova.",
        evidence="structure.swing_engine.detect_swings(df)[0]; structure.evaluate(df) inside loop.",
    ),
    ComponentClassification(
        component="MTFConsensus aggregation (_build_consensus)",
        verdict="SAFE_INCREMENTAL",
        reason="Agregação pura sobre engine_results[engine][TF]=direction (5 TFs x 4 engines = 20 direções). "
               "Se todas as direções por TF estiverem disponíveis (frescas), a agregação é determinística e barata (~0.1ms). "
               "É seguro recalcular sempre a partir das direções (não precisa cache).",
        evidence="MTFEngine._build_consensus apenas conta BULLISH/BEARISH e calcula alignment/conflict scores.",
    ),
    ComponentClassification(
        component="Prefixo engine_name 'TF - name' + timeframe tagging",
        verdict="SAFE_INCREMENTAL",
        reason="Transformação nominal (replace) sem custo computacional; sempre refeita.",
        evidence="replace(e, engine_name=f\"{tf} - {e.engine_name}\")",
    ),
    # ── Fora de MTF mas relevante para scanner contínuo ──
    ComponentClassification(
        component="DataNormalizer.normalize(df)",
        verdict="SAFE_INCREMENTAL",
        reason="Normalização idempotente (lowercase + renomeio + duplicação open..Close). Barata e segura para reuso se df já normalizado.",
        evidence="DataNormalizer.normalize duplica colunas lower+Cap.",
    ),
    ComponentClassification(
        component="DataQualityEngine.validate(df)",
        verdict="REQUIRES_FULL_RECALC",
        reason="Validação inclui check de gaps temporais, outliers, NaN, timestamps — deve rodar sobre df final antes de decidir. "
               "Não reutilizar resultado de df antigo.",
        evidence="DataQualityEngine.validate verifica index gaps, NaT, duplicatas, z-score.",
    ),
    ComponentClassification(
        component="StructureAnalysis (fora MTF, no pipeline principal)",
        verdict="REQUIRES_FULL_RECALC",
        reason="Mesma lógica de MarketStructureIntelligenceEngine mas sobre M5 5d window; sensível a nova vela.",
        evidence="AnalysisPipeline StructureAnalysis stage: structure_intel_engine.evaluate(df)",
    ),
    ComponentClassification(
        component="ConfluenceEngine / ConfidenceEngine / ProbabilityEngine",
        verdict="REQUIRES_FULL_RECALC",
        reason="Agregações ponderadas sobre evidências atuais; qualquer mudança de evidência muda score. "
               "Não cacheável isoladamente.",
        evidence="MercuryDecisionEngine orquestra Confidence->Confluence->Probability sobre resolved_bundle atual.",
    ),
    ComponentClassification(
        component="DecisionResolverEngine",
        verdict="REQUIRES_FULL_RECALC",
        reason="Regras puras mas dependem de confluence_score + grade + regime atuais; recalcular sempre. "
               "NÃO ALTERAR neste sprint (preservado).",
        evidence="DecisionResolverEngine.resolve(dominant_direction, is_valid, grade, conflict, confluence_score, regime)",
    ),
    ComponentClassification(
        component="Ranking Top-3 fórmula",
        verdict="SAFE_INCREMENTAL",
        reason="Fórmula é pura e barata; recalcular sobre DecisionResults frescos é seguro e necessário. "
               "Não há estado incremental complexo — apenas reordenar.",
        evidence="top3_scanner fórmula: confluence + confidence*0.30 + grade_bonus + prob*0.20, sort determinístico.",
    ),
]


def report() -> Dict[str, List[str]]:
    by_verdict: Dict[str, List[str]] = {"SAFE_INCREMENTAL": [], "REQUIRES_FULL_RECALC": [], "UNKNOWN": []}
    for c in MTF_CLASSIFICATIONS:
        by_verdict[c.verdict].append(c.component)
    return by_verdict


def to_dict_list() -> List[Dict[str, str]]:
    return [
        {"component": c.component, "verdict": c.verdict, "reason": c.reason, "evidence": c.evidence}
        for c in MTF_CLASSIFICATIONS
    ]
