from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.analysis.market_thesis_builder import MarketThesisBuilder
from mercury_ai.analysis.decision_trace_engine import DecisionTraceEngine
from mercury_ai.analysis.institutional_contribution import InstitutionalContribution
from mercury_ai.config.institutional_weights import (
    INSTITUTIONAL_WEIGHTS,
    INSTITUTIONAL_WEIGHTS_SUM,
)
from mercury_ai.analysis.confluence_helpers import (
    has_conflict,
    clamp_score,
    dominant_direction,
)

# Mapeamento de engine_name de produção → domínio canônico (lowercase)
# em INSTITUTIONAL_WEIGHTS (config.institutional_weights).
# Garante que cada engine receba o peso institucional correto em vez
# de cair no fallback 1.0.
ENGINE_NAME_TO_DOMAIN = {
    "Trend": "trend",
    "SmartMoney": "smart_money",
    "StructureEngine": "market_structure",
    "SwingEngine": "market_structure",
    "FairValueGapEngine": "market_structure",
    "LiquidityEngine": "liquidity",
    "LiquidityEventEngine": "liquidity",
    "VolatilityEngine": "volatility",
    "RiskEngine": "volatility",
    "VolumeEngine": "smart_money",
    "VWAPEngine": "support_resistance",
    "MomentumEngine": "trend",
    "ContextEngine": "market_condition",
    "ConsistencyEngine": "market_condition",
}

class ConfluenceEngine:
    """
    Motor de confluência institucional — agregação ponderada de evidências.

    SRP: responsabilidade única de agregar evidências e calcular
    o score de confluência. A construção da tese (MarketThesis) é
    delegada ao MarketThesisBuilder, que é injetado via construtor.

    As engines internas (RiskEngine, ConfidenceEngine, MarketStateEngine,
    ConfluenceScoreEngine) são injetadas pelo orquestrador
    (MercuryDecisionEngine), não instanciadas aqui.
    """

    def __init__(
        self,
        thesis_builder: MarketThesisBuilder,
        trace_engine: DecisionTraceEngine | None = None,
    ):
        self.thesis_builder = thesis_builder
        self.trace_engine = trace_engine or DecisionTraceEngine()

    def analyze(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> tuple[ConfluenceResult, list[InstitutionalContribution]]:
        bullish_score = 0.0
        bearish_score = 0.0
        conflicting_signals = False
        contributions: list[InstitutionalContribution] = []
        active_domains: set[str] = set()

        # Weighted Aggregation (usa pesos canônicos)
        for evidence in evidence_bundle.evidences:
            # MTFEngine prefixa engine_name com o timeframe (ex: "H1 - Trend").
            # Removemos o prefixo para que o lookup em ENGINE_NAME_TO_DOMAIN
            # encontre o domínio correto e a evidência não seja descartada.
            clean_name = (
                evidence.engine_name.split(" - ", 1)[-1]
                if " - " in evidence.engine_name
                else evidence.engine_name
            )
            domain = ENGINE_NAME_TO_DOMAIN.get(clean_name, "market_condition")
            weight = INSTITUTIONAL_WEIGHTS.get(domain, 1.0)
            contribution = (evidence.strength / 100.0) * weight

            if evidence.direction == "BULLISH":
                bullish_score += contribution
            elif evidence.direction == "BEARISH":
                bearish_score += contribution

            active_domains.add(domain)

            # Build per-engine contribution for explainability
            contributions.append(InstitutionalContribution(
                engine_name=evidence.engine_name,
                weight=weight,
                raw_score=evidence.strength,
                weighted_score=round(contribution, 4),
                direction=evidence.direction,
                confidence=evidence.confidence,
                explanation=(
                    f"{evidence.engine_name}: direcao={evidence.direction}, "
                    f"strength={evidence.strength:.1f}, "
                    f"peso={weight}, "
                    f"contribuicao_ponderada={contribution:.4f}"
                ),
            ))

        # Risk & Conflict Penalty
        risk_penalty = (
            context.risk_assessment.institutional_risk_score
            * 0.15
        )
        conflict_penalty = 0.0
        if has_conflict(bullish_score, bearish_score):
            conflicting_signals = True
            conflict_penalty = (
                min(
                    bullish_score,
                    bearish_score
                ) * 0.30
            )

        # Score institucional de confluência
        total_weighted_score = max(
            bullish_score,
            bearish_score
        )

        net_score = (
            total_weighted_score
            - risk_penalty
            - conflict_penalty
        )

        # Normalização por domínios ativos:
        # Nem sempre os 8 domínios institucionais têm evidências. Dividir o
        # score por INSTITUTIONAL_WEIGHTS_SUM (100.0 fixo) subdimensiona o
        # acordo quando poucos domínios estão ativos. Normalizamos pelo
        # somatório de pesos dos domínios que efetivamente contribuíram.
        active_weights_sum = sum(
            INSTITUTIONAL_WEIGHTS.get(d, 0.0) for d in active_domains
        )
        if active_weights_sum <= 0.0:
            active_weights_sum = INSTITUTIONAL_WEIGHTS_SUM

        # Escala proporcional: se apenas parte dos domínios está ativa,
        # amplificamos o score para a escala 0-100 completa, permitindo
        # comparação justa entre cenários com diferentes números de evidências.
        scale_factor = INSTITUTIONAL_WEIGHTS_SUM / active_weights_sum
        normalized_score = net_score * scale_factor

        normalized_score = clamp_score(normalized_score, floor=5.0, ceiling=100.0)

        # Determine dominant direction
        direction = dominant_direction(bullish_score, bearish_score)

        # Construção da tese (delegada ao builder injetado)
        thesis = self.thesis_builder.build(context, evidence_bundle)

        return (
            ConfluenceResult(
                buy_score=bullish_score,
                sell_score=bearish_score,
                neutral_score=0.0,
                agreement_percentage=(normalized_score / INSTITUTIONAL_WEIGHTS_SUM) * 100.0,
                conflicting_signals=conflicting_signals,
                independent_confirmations=len(evidence_bundle.evidences),
                weighted_score=normalized_score,
                confidence=thesis.confidence.confidence_score,
                dominant_direction=direction,
                evidences=tuple(thesis.confirmations),
                warnings=(),
            ),
            contributions,
        )
