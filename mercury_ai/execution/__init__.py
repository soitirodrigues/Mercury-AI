"""Módulo de execução de ordens reais.

Exporta as classes principais para envio, gestão e persistência de ordens.
"""
from mercury_ai.execution.order_types import (
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    TimeInForce,
)
from mercury_ai.execution.broker_interface import IBroker
from mercury_ai.execution.order_executor import OrderExecutor, OrderExecutionError
from mercury_ai.execution.brokers.demo_broker import DemoBroker

__all__ = [
    "Order",
    "OrderSide",
    "OrderStatus",
    "OrderType",
    "TimeInForce",
    "IBroker",
    "OrderExecutor",
    "OrderExecutionError",
    "DemoBroker",
]
