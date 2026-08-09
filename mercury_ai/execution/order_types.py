"""Tipos de dados para o módulo de execução de ordens.

Define Order, OrderSide, OrderType, OrderStatus, TimeInForce e Fill.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import uuid


class OrderSide(str, Enum):
    """Lado da ordem."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Tipo da ordem."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderStatus(str, Enum):
    """Status da ordem no ciclo de vida."""
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

    @property
    def is_terminal(self) -> bool:
        """Retorna True se o status é terminal (não muda mais)."""
        return self in (OrderStatus.FILLED, OrderStatus.CANCELLED,
                        OrderStatus.REJECTED, OrderStatus.EXPIRED)


class TimeInForce(str, Enum):
    """Validade da ordem."""
    DAY = "DAY"
    GTC = "GTC"  # Good Till Cancelled
    IOC = "IOC"  # Immediate Or Cancel
    FOK = "FOK"  # Fill Or Kill


@dataclass
class Fill:
    """Execução parcial ou total de uma ordem."""
    fill_id: str
    price: float
    quantity: float
    timestamp: str  # ISO-8601 UTC
    commission: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "fill_id": self.fill_id,
            "price": self.price,
            "quantity": self.quantity,
            "timestamp": self.timestamp,
            "commission": self.commission,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Fill":
        return cls(
            fill_id=data["fill_id"],
            price=data["price"],
            quantity=data["quantity"],
            timestamp=data["timestamp"],
            commission=data.get("commission", 0.0),
        )


def _utcnow_iso() -> str:
    """Retorna timestamp atual em ISO-8601 UTC."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Order:
    """Representa uma ordem de trading.

    Campos imutáveis após criação: order_id, created_at, side, order_type,
    symbol, quantity. Campos mutáveis: status, fills, broker_order_id,
    updated_at, reject_reason.
    """
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    broker: str = ""
    limit_price: float | None = None
    stop_price: float | None = None
    time_in_force: TimeInForce = TimeInForce.DAY
    order_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    broker_order_id: str | None = None
    status: OrderStatus = OrderStatus.PENDING
    fills: list[Fill] = field(default_factory=list)
    created_at: str = field(default_factory=_utcnow_iso)
    updated_at: str = field(default_factory=_utcnow_iso)
    reject_reason: str | None = None
    client_tag: str | None = None  # tag livre para rastreabilidade

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"quantity deve ser > 0, recebeu {self.quantity}")
        if self.order_type in (OrderType.LIMIT, OrderType.STOP_LIMIT) and self.limit_price is None:
            raise ValueError(
                f"limit_price é obrigatório para order_type={self.order_type.value}"
            )
        if self.order_type in (OrderType.STOP, OrderType.STOP_LIMIT) and self.stop_price is None:
            raise ValueError(
                f"stop_price é obrigatório para order_type={self.order_type.value}"
            )
        if self.limit_price is not None and self.limit_price <= 0:
            raise ValueError(f"limit_price deve ser > 0, recebeu {self.limit_price}")
        if self.stop_price is not None and self.stop_price <= 0:
            raise ValueError(f"stop_price deve ser > 0, recebeu {self.stop_price}")

    # ------------------------------------------------------------------
    # Propriedades calculadas
    # ------------------------------------------------------------------

    @property
    def filled_quantity(self) -> float:
        """Quantidade total já executada."""
        return sum(f.quantity for f in self.fills)

    @property
    def remaining_quantity(self) -> float:
        """Quantidade restante a executar."""
        return self.quantity - self.filled_quantity

    @property
    def avg_fill_price(self) -> float | None:
        """Preço médio ponderado das execuções, ou None se nenhuma fill."""
        total_qty = self.filled_quantity
        if total_qty == 0:
            return None
        return sum(f.price * f.quantity for f in self.fills) / total_qty

    @property
    def total_commission(self) -> float:
        """Comissão total acumulada."""
        return sum(f.commission for f in self.fills)

    # ------------------------------------------------------------------
    # Serialização
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "broker_order_id": self.broker_order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "order_type": self.order_type.value,
            "quantity": self.quantity,
            "limit_price": self.limit_price,
            "stop_price": self.stop_price,
            "time_in_force": self.time_in_force.value,
            "broker": self.broker,
            "status": self.status.value,
            "fills": [f.to_dict() for f in self.fills],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "reject_reason": self.reject_reason,
            "client_tag": self.client_tag,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Order":
        fills = [Fill.from_dict(f) for f in data.get("fills", [])]
        obj = cls.__new__(cls)
        obj.symbol = data["symbol"]
        obj.side = OrderSide(data["side"])
        obj.order_type = OrderType(data["order_type"])
        obj.quantity = data["quantity"]
        obj.broker = data.get("broker", "")
        obj.limit_price = data.get("limit_price")
        obj.stop_price = data.get("stop_price")
        obj.time_in_force = TimeInForce(data.get("time_in_force", "DAY"))
        obj.order_id = data["order_id"]
        obj.broker_order_id = data.get("broker_order_id")
        obj.status = OrderStatus(data["status"])
        obj.fills = fills
        obj.created_at = data["created_at"]
        obj.updated_at = data["updated_at"]
        obj.reject_reason = data.get("reject_reason")
        obj.client_tag = data.get("client_tag")
        return obj

    # ------------------------------------------------------------------
    # Transições de estado
    # ------------------------------------------------------------------

    def _touch(self) -> None:
        self.updated_at = _utcnow_iso()

    def mark_submitted(self, broker_order_id: str | None = None) -> None:
        """Marca a ordem como submetida ao broker."""
        if self.status != OrderStatus.PENDING:
            raise OrderStateError(
                f"Não pode marcar SUBMITTED: status atual={self.status.value}"
            )
        self.status = OrderStatus.SUBMITTED
        if broker_order_id is not None:
            self.broker_order_id = broker_order_id
        self._touch()

    def add_fill(self, fill: Fill) -> None:
        """Adiciona uma execução parcial ou total à ordem."""
        if self.status.is_terminal:
            raise OrderStateError(
                f"Não pode adicionar fill: status terminal={self.status.value}"
            )
        self.fills.append(fill)
        if self.filled_quantity >= self.quantity:
            self.status = OrderStatus.FILLED
        elif self.filled_quantity > 0:
            self.status = OrderStatus.PARTIAL
        self._touch()

    def cancel(self, reason: str | None = None) -> None:
        """Cancela a ordem se ainda não está terminal."""
        if self.status.is_terminal:
            raise OrderStateError(
                f"Não pode cancelar: status terminal={self.status.value}"
            )
        self.status = OrderStatus.CANCELLED
        self.reject_reason = reason
        self._touch()

    def reject(self, reason: str) -> None:
        """Rejeita a ordem."""
        if self.status.is_terminal:
            raise OrderStateError(
                f"Não pode rejeitar: status terminal={self.status.value}"
            )
        self.status = OrderStatus.REJECTED
        self.reject_reason = reason
        self._touch()

    def expire(self) -> None:
        """Expira a ordem."""
        if self.status.is_terminal:
            raise OrderStateError(
                f"Não pode expirar: status terminal={self.status.value}"
            )
        self.status = OrderStatus.EXPIRED
        self._touch()


class OrderStateError(Exception):
    """Erro de transição de estado ilegal em uma Order."""
