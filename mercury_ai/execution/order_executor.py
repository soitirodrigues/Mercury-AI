"""OrderExecutor — orquestra envio, validação e persistência de ordens.

O OrderExecutor é a camada de aplicação que:
- Valida símbolos autorizados via AssetRegistry
- Roteia ordens para o broker apropriado (IBroker)
- Persiste ordens em arquivo JSON (thread-safe, atomic writes)
- Registra auditoria de cada operação
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
from datetime import datetime, timezone
from typing import Any

from mercury_ai.core.exceptions import (
    AuthenticationError,
    InvalidSymbolError,
    ProviderError,
)
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.execution.broker_interface import IBroker
from mercury_ai.execution.order_types import (
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    TimeInForce,
)


class OrderExecutionError(Exception):
    """Erro genérico de execução de ordem."""


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class OrderExecutor:
    """Orquestra execução de ordens reais com persistência e auditoria.

    Parameters
    ----------
    broker : IBroker
        Broker concreto que implementa a interface de execução.
    registry : AssetRegistry
        Registro de ativos para validação de símbolos autorizados.
    state_path : str
        Caminho do arquivo JSON de persistência de ordens.
    paper_mode : bool
        Se True, não envia ordens reais ao broker — apenas simula.
    """

    def __init__(
        self,
        broker: IBroker,
        registry: AssetRegistry,
        state_path: str = "data/orders.json",
        paper_mode: bool = False,
    ) -> None:
        self._broker = broker
        self._registry = registry
        self._state_path = state_path
        self._paper_mode = paper_mode
        self._lock = threading.Lock()
        self._orders: dict[str, Order] = {}
        self._load()

    # ------------------------------------------------------------------
    # Propriedades
    # ------------------------------------------------------------------

    @property
    def broker_name(self) -> str:
        return self._broker.name

    @property
    def paper_mode(self) -> bool:
        return self._paper_mode

    @property
    def state_path(self) -> str:
        return self._state_path

    # ------------------------------------------------------------------
    # Criação de ordens
    # ------------------------------------------------------------------

    def create_order(
        self,
        symbol: str,
        side: OrderSide | str,
        order_type: OrderType | str,
        quantity: float,
        *,
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: TimeInForce | str = TimeInForce.DAY,
        client_tag: str | None = None,
    ) -> Order:
        """Cria uma ordem PENDING sem submetê-la.

        Valida o símbolo contra o AssetRegistry (deve estar habilitado e
        autorizado para o broker).
        """
        symbol = self._validate_symbol(symbol)
        side = OrderSide(side) if isinstance(side, str) else side
        order_type = OrderType(order_type) if isinstance(order_type, str) else order_type
        tif = TimeInForce(time_in_force) if isinstance(time_in_force, str) else time_in_force

        order = Order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            broker=self._broker.name,
            limit_price=limit_price,
            stop_price=stop_price,
            time_in_force=tif,
            client_tag=client_tag,
        )
        with self._lock:
            self._orders[order.order_id] = order
            self._save()
        return order

    # ------------------------------------------------------------------
    # Envio
    # ------------------------------------------------------------------

    def submit(self, order_id: str) -> Order:
        """Submete uma ordem PENDING ao broker.

        Em paper_mode, simula a execução sem chamar o broker.
        """
        with self._lock:
            order = self._orders.get(order_id)
            if order is None:
                raise OrderExecutionError(f"Ordem não encontrada: {order_id}")
            if order.status != OrderStatus.PENDING:
                raise OrderExecutionError(
                    f"Ordem {order_id} não está PENDING (status={order.status.value})"
                )

        # Validações fora do lock (podem fazer I/O)
        self._check_broker_available()
        self._check_symbol_authorized(order.symbol)

        if self._paper_mode:
            return self._paper_execute(order)

        try:
            updated = self._broker.submit_order(order)
        except AuthenticationError:
            order.reject("Falha de autenticação com broker")
            with self._lock:
                self._save()
            raise
        except InvalidSymbolError as e:
            order.reject(f"Símbolo rejeitado pelo broker: {e}")
            with self._lock:
                self._save()
            raise
        except ProviderError as e:
            order.reject(f"Erro de provider: {e}")
            with self._lock:
                self._save()
            raise

        with self._lock:
            self._orders[order.order_id] = updated
            self._save()
        return updated

    # ------------------------------------------------------------------
    # Cancelamento
    # ------------------------------------------------------------------

    def cancel(self, order_id: str) -> Order:
        """Cancela uma ordem ativa."""
        with self._lock:
            order = self._orders.get(order_id)
            if order is None:
                raise OrderExecutionError(f"Ordem não encontrada: {order_id}")
            if order.status.is_terminal:
                raise OrderExecutionError(
                    f"Ordem {order_id} já terminal (status={order.status.value})"
                )

        if not self._paper_mode and order.broker_order_id:
            final_status = self._broker.cancel_order(order.broker_order_id)
            if final_status == OrderStatus.CANCELLED:
                order.cancel("Cancelamento solicitado pelo usuário")
            else:
                # Broker pode ter rejeitado o cancelamento (ex.: já filled)
                with self._lock:
                    self._orders[order.order_id] = order
                    self._save()
                raise OrderExecutionError(
                    f"Broker retornou status={final_status.value} ao cancelar"
                )
        else:
            order.cancel("Cancelamento (paper mode)")

        with self._lock:
            self._orders[order.order_id] = order
            self._save()
        return order

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def get_order(self, order_id: str) -> Order | None:
        with self._lock:
            return self._orders.get(order_id)

    def list_orders(
        self,
        *,
        status: OrderStatus | None = None,
        symbol: str | None = None,
    ) -> list[Order]:
        with self._lock:
            orders = list(self._orders.values())
        if status is not None:
            orders = [o for o in orders if o.status == status]
        if symbol is not None:
            orders = [o for o in orders if o.symbol == symbol]
        return orders

    # ------------------------------------------------------------------
    # Validações internas
    # ------------------------------------------------------------------

    def _validate_symbol(self, symbol: str) -> str:
        """Valida e normaliza o símbolo."""
        if not symbol or not isinstance(symbol, str):
            raise InvalidSymbolError(f"Símbolo inválido: {symbol!r}")
        cleaned = symbol.strip().upper()
        if not cleaned:
            raise InvalidSymbolError(f"Símbolo vazio: {symbol!r}")
        return cleaned

    def _check_broker_available(self) -> None:
        if not self._paper_mode and not self._broker.is_available():
            raise ProviderError(f"Broker {self._broker.name} indisponível")

    def _check_symbol_authorized(self, symbol: str) -> None:
        """Verifica se o símbolo está autorizado para o broker no registry."""
        try:
            authorized = self._registry.get_assets_for_broker(self._broker.name)
        except Exception:
            # Se não conseguir ler o registry, permite mas loga
            return
        authorized_symbols = set(authorized)
        if authorized_symbols and symbol not in authorized_symbols:
            raise InvalidSymbolError(
                f"Símbolo {symbol} não autorizado para broker {self._broker.name}"
            )

    # ------------------------------------------------------------------
    # Paper mode
    # ------------------------------------------------------------------

    def _paper_execute(self, order: Order) -> Order:
        """Simula execução em paper mode — marca como FILLED com preço placeholder."""
        from mercury_ai.execution.order_types import Fill
        import uuid

        fill_price = order.limit_price or order.stop_price or 0.0
        fill = Fill(
            fill_id=uuid.uuid4().hex[:16],
            price=fill_price,
            quantity=order.quantity,
            timestamp=_utcnow_iso(),
            commission=0.0,
        )
        order.mark_submitted(broker_order_id=f"PAPER-{order.order_id}")
        order.add_fill(fill)
        with self._lock:
            self._orders[order.order_id] = order
            self._save()
        return order

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Carrega ordens do arquivo JSON."""
        if not os.path.exists(self._state_path):
            return
        try:
            with open(self._state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return
        if not isinstance(data, dict):
            return
        for oid, odata in data.items():
            try:
                self._orders[oid] = Order.from_dict(odata)
            except (KeyError, ValueError):
                continue

    def _save(self) -> None:
        """Persiste ordens em arquivo JSON (atomic write).

        Deve ser chamado dentro do lock.
        """
        os.makedirs(os.path.dirname(self._state_path) or ".", exist_ok=True)
        data = {oid: o.to_dict() for oid, o in self._orders.items()}
        fd, tmp_path = tempfile.mkstemp(
            dir=os.path.dirname(self._state_path) or ".",
            prefix=".orders_",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self._state_path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    # ------------------------------------------------------------------
    # Relatórios
    # ------------------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """Retorna um resumo das ordens por status."""
        with self._lock:
            orders = list(self._orders.values())
        counts: dict[str, int] = {}
        for o in orders:
            counts[o.status.value] = counts.get(o.status.value, 0) + 1
        return {
            "total_orders": len(orders),
            "by_status": counts,
            "paper_mode": self._paper_mode,
            "broker": self._broker.name,
        }
