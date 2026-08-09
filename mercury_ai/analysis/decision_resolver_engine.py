from dataclasses import dataclass
from typing import Optional

from mercury_ai.config import settings


@dataclass(frozen=True)
class DecisionResolverResult:
    decision: str
    confidence_override: Optional[float]
    triggered_rule: int


class DecisionResolverEngine:
    """
    Motor institucional de resolução da decisão final.

    Modelo C — Híbrido Institucional:

        Confluence define a direção.
        Probability qualifica com thresholds.
        O Resolver arbitra a decisão final.

    Regras (em ordem de prioridade):

        1. is_valid == False
           → WAIT (confidence_override = 0.0)

        2. dominant_direction == NEUTRAL
           → WAIT

        3. confluence_score < regime_threshold
           → WAIT (confluência institucional insuficiente)
           O threshold é adaptativo conforme o regime de mercado.

        4. opportunity_grade == "D"
           → WAIT

        5. conflicting_signals == True
           AND opportunity_grade in ("C", "D")
           → WAIT

        6. dominant_direction == BUY
           → BUY

        7. dominant_direction == SELL
           → SELL

        8. Fallback
           → WAIT
    """

    # Threshold institucional mínimo de confluência para permitir entrada.
    # Abaixo deste valor, não há força direcional suficiente para agir.
    # Mantido como fallback para compatibilidade retroativa.
    CONFLUENCE_MIN_THRESHOLD: float = 40.0

    def __init__(self, min_threshold: float = 40.0):
        """
        Inicializa o resolver com threshold configurável.

        Args:
            min_threshold: Threshold base de confluência (default 40.0).
                           Será multiplicado pelo fator do regime de mercado.
        """
        self._min_threshold = min_threshold

    def _get_regime_threshold(self, market_regime=None) -> float:
        """
        Calcula o threshold de confluência adaptativo conforme o regime.

        Em regimes de tendência forte, o threshold é reduzido (mais agressivo).
        Em regimes de consolidação/compressão, o threshold é elevado
        (mais seletivo, exigindo maior confluência).

        O resultado é sempre limitado entre FLOOR e CAP definidos em settings.

        Args:
            market_regime: Pode ser MarketRegimeEnum, MarketRegime (objeto
                           com atributo .regime), string ou None.

        Returns:
            Threshold de confluência adaptativo e clampado.
        """
        # Extrair nome do regime em string
        regime_name = "UNKNOWN"

        if market_regime is not None:
            # MarketRegimeEnum diretamente
            if hasattr(market_regime, "name"):
                regime_name = market_regime.name
            # MarketRegime objeto com atributo .regime
            elif hasattr(market_regime, "regime"):
                inner = market_regime.regime
                if hasattr(inner, "name"):
                    regime_name = inner.name
                else:
                    regime_name = str(inner)
            # String direta
            elif isinstance(market_regime, str):
                regime_name = market_regime
            else:
                regime_name = str(market_regime)

        # Buscar multiplicador do regime (default 1.0 para UNKNOWN)
        multiplier = settings.CONFLUENCE_THRESHOLD_MULTIPLIERS.get(
            regime_name, 1.0
        )

        # Calcular threshold adaptativo
        threshold = self._min_threshold * multiplier

        # Clamping entre floor e cap
        threshold = max(
            settings.CONFLUENCE_THRESHOLD_FLOOR,
            min(threshold, settings.CONFLUENCE_THRESHOLD_CAP),
        )

        return threshold

    def resolve(
        self,
        dominant_direction: str,
        is_valid: bool,
        opportunity_grade: str = "C",
        conflicting_signals: bool = False,
        confluence_score: float = 100.0,
        market_regime=None,
    ) -> DecisionResolverResult:

        confidence_override: Optional[float] = None

        # Regra 1: Validação
        if not is_valid:
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=0.0,
                triggered_rule=1,
            )

        # Regra 2: Direção neutra
        if dominant_direction == "NEUTRAL":
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=2,
            )

        # Regra 3: Confluência institucional insuficiente (threshold adaptativo)
        regime_threshold = self._get_regime_threshold(market_regime)
        if confluence_score < regime_threshold:
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=3,
            )

        # Regra 4: Oportunidade muito baixa
        if opportunity_grade == "D":
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=4,
            )

        # Regra 5: Conflito com força insuficiente
        if conflicting_signals and opportunity_grade in ("C", "D"):
            return DecisionResolverResult(
                decision="WAIT",
                confidence_override=None,
                triggered_rule=5,
            )

        # Regra 6: BUY
        if dominant_direction == "BUY":
            return DecisionResolverResult(
                decision="BUY",
                confidence_override=None,
                triggered_rule=6,
            )

        # Regra 7: SELL
        if dominant_direction == "SELL":
            return DecisionResolverResult(
                decision="SELL",
                confidence_override=None,
                triggered_rule=7,
            )

        # Regra 8: Fallback
        return DecisionResolverResult(
            decision="WAIT",
            confidence_override=None,
            triggered_rule=8,
        )