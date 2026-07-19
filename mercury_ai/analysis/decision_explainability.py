from dataclasses import dataclass, field
from typing import Tuple
from mercury_ai.analysis.institutional_contribution import InstitutionalContribution


@dataclass(frozen=True)
class DecisionExplainability:
    """
    Camada de explainability institucional do Mercury AI.

    Responde à pergunta: "Por que o Mercury decidiu BUY, SELL ou WAIT?"
    sem alterar nenhuma fórmula, peso, score ou regra de negócio.

    Apenas coleta o resultado produzido pelos engines e o organiza
    em uma estrutura rastreável e auditável.

    Attributes:
        decision: Decisão final (BUY, SELL, WAIT)
        reason: Razão textual da decisão
        dominant_direction: Direção dominante da confluência
        opportunity_grade: Grade de oportunidade (A+, A, B, C, D)
        conflicting_signals: Se há sinais conflitantes
        institutional_score: Score institucional final
        confidence: Confiança calibrada final
        triggered_rule: Número da regra do DecisionResolver que disparou (1-7)
        contributions: Lista de contribuições individuais das engines
        decision_chain: Cadeia de decisão passo a passo
    """
    decision: str
    reason: str
    dominant_direction: str
    opportunity_grade: str
    conflicting_signals: bool
    institutional_score: float
    confidence: float
    triggered_rule: int
    contributions: Tuple[InstitutionalContribution, ...] = field(default_factory=tuple)
    decision_chain: Tuple[str, ...] = field(default_factory=tuple)