"""DemoBroker — broker de simulação para paper trading.

Implementa IBroker simulando fills instantâneos sem venue real.
Útil para testes, desenvolvimento e validação de estratégias.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from mercury_ai.execution.order_types import (
    Fill,
    Order,
    OrderStatus,
    OrderType,
)


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DemoBroker:
    """Broker de simulação que preenche ordens instantaneamente.

    Atributos
    ---------
    name : str
        Identificador fixo "DEMO".
    commission_per_trade : float
        Comissão fixa por trade (default 0.0).
    fill_price_override : float | None
        Se definido, usa este preço para todos os fills. Caso contrário,
        usa limit_price/stop_price ou 0.0 para ordens MARKET.
    """

    def __init__(
        self,
        *,
        commission_per_trade: float = 0.0,
        fill_price_override: float | None = None,
    ) -> None:
        self._commission = commission_per_trade
        self._fill_price_override = fill_price_override
        self._connected = True

    # ------------------------------------------------------------------
    # IBroker
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        return "DEMO"

    def is_available(self) -> bool:
        return self._connected

    def supports_symbol(self, symbol: str) -> bool:
        # DemoBroker suporta qualquer símbolo não-vazio
        return bool(symbol and isinstance(symbol, str) and symbol.strip())

    def submit_order(self, order: Order) -> Order:
        if not self._connected:
            from mercury_ai.core.exceptions import ProviderError
            raise ProviderError("DemoBroker não está conectado")
        if not self.supports_symbol(order.symbol):
            from mercury_ai.core.exceptions import InvalidSymbolError
            raise InvalidSymbolError(f"Símbolo não suportado: {order.symbol}")

        broker_order_id = f"DEMO-{uuid.uuid4().hex[:12]}"
        order.mark_submitted(broker_order_id=broker_order_id)

        fill_price = self._fill_price_override
        if fill_price is None:
            if order.order_type in (OrderType.LIMIT, OrderType.STOP_LIMIT):
                fill_price = order.limit_price or 0.0
            elif order.order_type == OrderType.STOP:
                fill_price = order.stop_price or 0.0
            else:
                fill_price = 0.0

        fill = Fill(
            fill_id=uuid.uuid4().hex[:16],
            price=fill_price,
            quantity=order.quantity,
            timestamp=_utcnow_iso(),
            commission=self._commission,
        )
        order.add_fill(fill)
        return order

    def cancel_order(self, broker_order_id: str) -> OrderStatus:
        # Em demo, cancelamento sempre bem-sucedido se a ordem não está terminal
        return OrderStatus.CANCELLED

    def get_order_status(self, broker_order_id: str) -> OrderStatus:
        # DemoBroker não mantém estado interno entre chamadas
        return OrderStatus.FILLED

    # ------------------------------------------------------------------
    # Controle de conexão (para testes)
    # ------------------------------------------------------------------

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False
