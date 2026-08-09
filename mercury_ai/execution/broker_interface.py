"""Interface de broker para execução de ordens.

Define o Protocol IBroker que brokers concretos devem implementar.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from mercury_ai.execution.order_types import Order, OrderStatus


@runtime_checkable
class IBroker(Protocol):
    """Interface que todo broker de execução deve implementar.

    Um broker é responsável por:
    - Validar credenciais e disponibilidade
    - Submeter ordens ao venue de execução
    - Consultar status de ordens
    - Cancelar ordens
    """

    @property
    def name(self) -> str:
        """Nome identificador do broker (ex.: 'XP', 'BINANCE')."""
        ...

    def is_available(self) -> bool:
        """Retorna True se o broker está disponível para execução."""
        ...

    def supports_symbol(self, symbol: str) -> bool:
        """Retorna True se o broker suporta o símbolo dado."""
        ...

    def submit_order(self, order: Order) -> Order:
        """Submete uma ordem ao venue de execução.

        Deve:
        - Validar credenciais/disponibilidade
        - Validar suporte ao símbolo
        - Enviar a ordem
        - Atualizar status (SUBMITTED, FILLED, REJECTED) e broker_order_id
        - Retornar a ordem atualizada

        Raises:
            ProviderError: se o broker não estiver disponível
            InvalidSymbolError: se o símbolo não for suportado
            AuthenticationError: se credenciais inválidas
        """
        ...

    def cancel_order(self, broker_order_id: str) -> OrderStatus:
        """Cancela uma ordem no broker pelo broker_order_id.

        Retorna o status final após a tentativa de cancelamento.
        """
        ...

    def get_order_status(self, broker_order_id: str) -> OrderStatus:
        """Consulta o status atual de uma ordem no broker."""
        ...
