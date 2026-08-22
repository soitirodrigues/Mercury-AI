"""Rolling Queue — fila controlada de análise M5 com prioridades.

Prioridades:
  P1: ativos cujo candle M5 acabou de fechar (freshness mudou)
  P2: ativos stale
  P3: ativos ainda não atualizados no ciclo

Nunca bloquear Top-3 esperando todos os ativos se já houver resultados válidos.
Distinguir TOP3_PARTIAL vs TOP3_COMPLETE.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from enum import Enum

from .asset_state import AssetScanState
from .freshness import FreshnessGate


class Top3Status(str, Enum):
    PARTIAL = "TOP3_PARTIAL"
    COMPLETE = "TOP3_COMPLETE"
    EMPTY = "TOP3_EMPTY"


@dataclass(order=True)
class QueueEntry:
    priority: int  # 1=highest
    symbol: str = field(compare=False)
    reason: str = field(default="", compare=False)
    state: Optional[AssetScanState] = field(default=None, compare=False)


class RollingQueue:
    """Fila com 3 níveis de prioridade para o ciclo M5."""

    def __init__(self, freshness_gate: Optional[FreshnessGate] = None):
        self.gate = freshness_gate or FreshnessGate()

    def build(
        self,
        universe: List[str],
        states: Dict[str, AssetScanState],
        latest_candles: Dict[str, Optional[datetime]],
        cycle_start: Optional[datetime] = None,
    ) -> List[QueueEntry]:
        """Constrói fila ordenada P1 -> P2 -> P3.

        Args:
            universe: lista de símbolos a escanear
            states: mapa symbol -> AssetScanState (antes do ciclo)
            latest_candles: mapa symbol -> latest_available_candle (UTC aware, pode ser None)
            cycle_start: quando o ciclo começou (para desempate)
        """
        if cycle_start is None:
            cycle_start = datetime.now(timezone.utc)

        p1: List[QueueEntry] = []
        p2: List[QueueEntry] = []
        p3: List[QueueEntry] = []

        for sym in universe:
            state = states.get(sym)
            latest = latest_candles.get(sym)

            # Sem estado prévio => precisa escanear (P3, mas com prioridade alta se for burst inicial)
            if state is None:
                p3.append(QueueEntry(priority=3, symbol=sym, reason="no prior state", state=None))
                continue

            # Se provider sem dados neste ciclo => não prioriza (fica em P3, mas será DATA_UNAVAILABLE)
            # A decisão de pular é do scanner, não da fila; fila apenas ordena.
            # Para priorização, tratamos DATA_UNAVAILABLE como P3 (não bloqueante).

            # Verificar freshness
            # state.decision_candle_timestamp é ISO; converter para datetime se existir
            from .freshness import FreshnessGate as FG
            gate = self.gate
            fr = gate.check_state(state.decision_candle_timestamp, latest, now=cycle_start)

            if fr.status == "DATA_UNAVAILABLE":
                # Provider sem vela nova — não é stale, mas precisa tentar novamente
                # Colocar em P3 (não bloqueia Top-3)
                p3.append(QueueEntry(priority=3, symbol=sym, reason=f"data unavailable: {fr.reason}", state=state))
            elif fr.status == "FRESH":
                # Já está fresh neste ciclo — não precisa re-escanear agora
                # P3 (já atualizado)
                p3.append(QueueEntry(priority=3, symbol=sym, reason=f"fresh: {fr.reason}", state=state))
            elif fr.status == "STALE":
                # Distinguir P1 vs P2:
                #  P1: stale e latest_candle == expected_latest (candle acabou de fechar) => acabou de ficar stale
                #  P2: stale há mais tempo (age grande) ou stale por múltiplas velas
                # Heurística: se age < 600s (2 velas), é P1 (candle recém-fechado).
                #             caso contrário P2.
                age = fr.age_seconds
                # Delta em velas
                if latest is not None and state.decision_candle_timestamp:
                    try:
                        dec_dt = datetime.fromisoformat(state.decision_candle_timestamp.replace("Z", "+00:00"))
                        if dec_dt.tzinfo is None:
                            dec_dt = dec_dt.replace(tzinfo=timezone.utc)
                        from .temporal import floor_m5
                        dec_dt = floor_m5(dec_dt)
                        latest_f = floor_m5(latest) if latest.tzinfo else floor_m5(latest.replace(tzinfo=timezone.utc))
                        delta_velas = int((latest_f - dec_dt).total_seconds() / 300)
                    except Exception:
                        delta_velas = 99
                else:
                    delta_velas = 99

                if delta_velas == 1 and (age is not None and age < 600):
                    p1.append(QueueEntry(priority=1, symbol=sym, reason=f"just closed: {fr.reason}", state=state))
                else:
                    p2.append(QueueEntry(priority=2, symbol=sym, reason=f"stale: {fr.reason}", state=state))
            else:
                p3.append(QueueEntry(priority=3, symbol=sym, reason=f"other: {fr.reason}", state=state))

        # Ordenar dentro de cada nível por idade (mais antigo primeiro) e depois symbol para determinismo
        def sort_key(e: QueueEntry):
            age = e.state.age_seconds() if e.state else 999999
            if age is None:
                age = 999999
            return (age * -1, e.symbol)  # mais antigo primeiro => age maior, mas queremos stale mais antigo primeiro

        # Para P1/P2: priorizar mais stale (age maior) primeiro
        p1.sort(key=lambda e: (-(e.state.age_seconds() or 0), e.symbol))
        p2.sort(key=lambda e: (-(e.state.age_seconds() or 0), e.symbol))
        p3.sort(key=lambda e: (e.symbol,))  # determinístico

        return p1 + p2 + p3

    def top3_status(
        self,
        ranked_states: List[AssetScanState],
        pending_symbols: List[str],
    ) -> Top3Status:
        """Determina se Top-3 é PARTIAL, COMPLETE ou EMPTY.

        - COMPLETE: nenhum símbolo pendente que poderia entrar no Top-3
                    (todos os ativos elegíveis foram processados ou mantidos validamente)
        - PARTIAL: há ativos pendentes ainda não processados neste ciclo
        - EMPTY: nenhum elegível
        """
        if not ranked_states:
            return Top3Status.EMPTY
        if pending_symbols:
            return Top3Status.PARTIAL
        return Top3Status.COMPLETE

    def pending_symbols(
        self,
        universe: List[str],
        states: Dict[str, AssetScanState],
        processed: set,
    ) -> List[str]:
        """Ativos do universo ainda não processados neste ciclo."""
        return [s for s in universe if s not in processed]
