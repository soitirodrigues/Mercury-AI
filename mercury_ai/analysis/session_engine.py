from typing import List
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.models.session_analysis import SessionAnalysis
from mercury_ai.config import sessions

class SessionEngine:
    """
    Analisa a sessão de mercado institucional (Sydney, Tokyo, London, New York).
    """

    def analyze(self) -> SessionAnalysis:
        hour = DeterministicClock.utcnow().hour
        evidences: List[str] = []
        
        session = self._detect_session(hour, evidences)
        overlap = self._detect_overlap(hour, evidences)
        quality = self._calculate_quality(session, overlap, evidences)
        liquidity = self._calculate_liquidity(session, overlap, evidences)
        explanation = self._build_explanation(evidences)
        
        return SessionAnalysis(
            session=session,
            overlap=overlap,
            quality=quality,
            liquidity_score=liquidity,
            explanation=explanation
        )

    def _detect_session(self, hour: int, evidences: List[str]) -> str:
        # Horários UTC aproximados — prioriza sessões mais ativas
        # London: 8-16 UTC | New York: 13-21 UTC | Tokyo: 0-9 UTC | Sydney: 21-6 UTC
        if 8 <= hour < 16:  # London (mais ativa, tem prioridade sobre Tokyo no overlap 8-9)
            evidences.append("Sessão de Londres.")
            return sessions.LONDON
        elif 13 <= hour < 21:  # New York
            evidences.append("Sessão de Nova York.")
            return sessions.NEW_YORK
        elif 0 <= hour < 8:  # Tokyo (0-8, evitando overlap com London)
            evidences.append("Sessão de Tokyo.")
            return sessions.TOKYO
        elif 21 <= hour < 24 or 0 <= hour < 0:  # Sydney (21-24 UTC)
            evidences.append("Sessão de Sydney.")
            return sessions.SYDNEY

        evidences.append("Período de baixa liquidez — mercado fechado.")
        return sessions.CLOSED

    def _detect_overlap(self, hour: int, evidences: List[str]) -> bool:
        # Overlaps comuns
        if 13 <= hour < 16:  # London / NY
            evidences.append("Sobreposição Londres/Nova York — alta liquidez.")
            return True
        elif 8 <= hour < 9:  # Tokyo / London
            evidences.append("Sobreposição Tokyo/Londres.")
            return True
        evidences.append("Sem sobreposição de sessões.")
        return False

    def _calculate_quality(self, session: str, overlap: bool, evidences: List[str]) -> float:
        if overlap:
            return 100.0
        elif session in [sessions.LONDON, sessions.NEW_YORK]:
            return 85.0
        elif session in [sessions.TOKYO]:
            return 60.0
        return 10.0

    def _calculate_liquidity(self, session: str, overlap: bool, evidences: List[str]) -> float:
        if overlap:
            return 100.0
        elif session in [sessions.LONDON, sessions.NEW_YORK]:
            return 90.0
        elif session in [sessions.TOKYO]:
            return 50.0
        return 20.0

    def _build_explanation(self, evidences: List[str]) -> str:
        return "\n".join([f"- {e}" for e in evidences])
