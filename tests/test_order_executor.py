"""Testes para o módulo de execução de ordens.

Cobre:
- order_types: Order, Fill, enums, state transitions, serialização
- broker_interface: IBroker Protocol
- order_executor: criação, envio, cancelamento, persistência, validação
- demo_broker: DemoBroker comportamento
"""
import json
import os
import tempfile
from pathlib import Path

import pytest

from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.core.exceptions import InvalidSymbolError, ProviderError
from mercury_ai.execution.broker_interface import IBroker
from mercury_ai.execution.brokers.demo_broker import DemoBroker
from mercury_ai.execution.order_executor import OrderExecutor, OrderExecutionError
from mercury_ai.execution.order_types import (
    Fill,
    Order,
    OrderSide,
    OrderStateError,
    OrderStatus,
    OrderType,
    TimeInForce,
)


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def tmp_orders_file(tmp_path):
    return str(tmp_path / "orders.json")


@pytest.fixture
def tmp_registry_dir(tmp_path):
    return str(tmp_path)


@pytest.fixture
def registry(tmp_registry_dir):
    return AssetRegistry(registry_file=str(Path(tmp_registry_dir) / "asset_registry.json"))


@pytest.fixture
def demo_broker():
    return DemoBroker(commission_per_trade=1.50, fill_price_override=100.0)


@pytest.fixture
def executor(demo_broker, registry, tmp_orders_file):
    return OrderExecutor(
        broker=demo_broker,
        registry=registry,
        state_path=tmp_orders_file,
        paper_mode=True,
    )


# ======================================================================
# order_types — Enums
# ======================================================================

class TestOrderEnums:
    def test_order_side_values(self):
        assert OrderSide.BUY.value == "BUY"
        assert OrderSide.SELL.value == "SELL"

    def test_order_type_values(self):
        assert OrderType.MARKET.value == "MARKET"
        assert OrderType.LIMIT.value == "LIMIT"
        assert OrderType.STOP.value == "STOP"
        assert OrderType.STOP_LIMIT.value == "STOP_LIMIT"

    def test_time_in_force_values(self):
        assert TimeInForce.DAY.value == "DAY"
        assert TimeInForce.GTC.value == "GTC"
        assert TimeInForce.IOC.value == "IOC"
        assert TimeInForce.FOK.value == "FOK"

    def test_order_status_is_terminal(self):
        assert OrderStatus.FILLED.is_terminal
        assert OrderStatus.CANCELLED.is_terminal
        assert OrderStatus.REJECTED.is_terminal
        assert OrderStatus.EXPIRED.is_terminal
        assert not OrderStatus.PENDING.is_terminal
        assert not OrderStatus.SUBMITTED.is_terminal
        assert not OrderStatus.PARTIAL.is_terminal


# ======================================================================
# order_types — Fill
# ======================================================================

class TestFill:
    def test_fill_creation(self):
        fill = Fill(
            fill_id="f1",
            price=50.25,
            quantity=100,
            timestamp="2024-01-01T00:00:00+00:00",
            commission=2.50,
        )
        assert fill.fill_id == "f1"
        assert fill.price == 50.25
        assert fill.quantity == 100
        assert fill.commission == 2.50

    def test_fill_default_commission(self):
        fill = Fill(fill_id="f1", price=10.0, quantity=5, timestamp="ts")
        assert fill.commission == 0.0

    def test_fill_to_dict(self):
        fill = Fill(fill_id="f1", price=10.0, quantity=5, timestamp="ts", commission=1.0)
        d = fill.to_dict()
        assert d["fill_id"] == "f1"
        assert d["price"] == 10.0
        assert d["quantity"] == 5
        assert d["commission"] == 1.0

    def test_fill_from_dict(self):
        d = {"fill_id": "f1", "price": 10.0, "quantity": 5, "timestamp": "ts", "commission": 1.0}
        fill = Fill.from_dict(d)
        assert fill.fill_id == "f1"
        assert fill.price == 10.0

    def test_fill_roundtrip(self):
        fill = Fill(fill_id="f1", price=42.5, quantity=10, timestamp="ts", commission=0.5)
        assert Fill.from_dict(fill.to_dict()) == fill


# ======================================================================
# order_types — Order
# ======================================================================

class TestOrder:
    def test_market_order_creation(self):
        order = Order(
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100,
        )
        assert order.symbol == "AAPL"
        assert order.side == OrderSide.BUY
        assert order.order_type == OrderType.MARKET
        assert order.quantity == 100
        assert order.status == OrderStatus.PENDING
        assert order.filled_quantity == 0
        assert order.remaining_quantity == 100
        assert order.avg_fill_price is None
        assert len(order.order_id) == 16

    def test_limit_order_requires_limit_price(self):
        with pytest.raises(ValueError, match="limit_price"):
            Order(
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=100,
            )

    def test_stop_order_requires_stop_price(self):
        with pytest.raises(ValueError, match="stop_price"):
            Order(
                symbol="AAPL",
                side=OrderSide.SELL,
                order_type=OrderType.STOP,
                quantity=100,
            )

    def test_stop_limit_requires_both_prices(self):
        with pytest.raises(ValueError, match="limit_price"):
            Order(
                symbol="AAPL",
                side=OrderSide.SELL,
                order_type=OrderType.STOP_LIMIT,
                quantity=100,
                stop_price=150.0,
            )

    def test_quantity_must_be_positive(self):
        with pytest.raises(ValueError, match="quantity"):
            Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=0)

    def test_negative_price_rejected(self):
        with pytest.raises(ValueError, match="limit_price"):
            Order(
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=100,
                limit_price=-10.0,
            )

    def test_filled_quantity_and_avg_price(self):
        order = Order(
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100,
        )
        f1 = Fill(fill_id="f1", price=100.0, quantity=60, timestamp="t1", commission=1.0)
        f2 = Fill(fill_id="f2", price=102.0, quantity=40, timestamp="t2", commission=1.0)
        order.add_fill(f1)
        assert order.filled_quantity == 60
        assert order.remaining_quantity == 40
        assert order.avg_fill_price == 100.0
        order.add_fill(f2)
        assert order.filled_quantity == 100
        assert order.remaining_quantity == 0
        # avg = (100*60 + 102*40) / 100 = 100.8
        assert order.avg_fill_price == pytest.approx(100.8)
        assert order.total_commission == 2.0

    def test_order_to_dict_from_dict_roundtrip(self):
        order = Order(
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100,
            limit_price=150.0,
            broker="DEMO",
            client_tag="test-tag",
        )
        d = order.to_dict()
        assert d["symbol"] == "AAPL"
        assert d["side"] == "BUY"
        assert d["order_type"] == "LIMIT"
        assert d["limit_price"] == 150.0
        restored = Order.from_dict(d)
        assert restored.symbol == order.symbol
        assert restored.side == order.side
        assert restored.order_type == order.order_type
        assert restored.quantity == order.quantity
        assert restored.limit_price == order.limit_price
        assert restored.order_id == order.order_id

    def test_mark_submitted(self):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        order.mark_submitted(broker_order_id="B-123")
        assert order.status == OrderStatus.SUBMITTED
        assert order.broker_order_id == "B-123"

    def test_cannot_mark_submitted_if_terminal(self):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        order.cancel("test")
        with pytest.raises(OrderStateError):
            order.mark_submitted(broker_order_id="B-123")

    def test_cancel(self):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        order.cancel("user requested")
        assert order.status == OrderStatus.CANCELLED
        assert order.reject_reason == "user requested"

    def test_reject(self):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        order.reject("invalid")
        assert order.status == OrderStatus.REJECTED
        assert order.reject_reason == "invalid"

    def test_expire(self):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        order.expire()
        assert order.status == OrderStatus.EXPIRED

    def test_cannot_add_fill_to_terminal(self):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        order.cancel("test")
        fill = Fill(fill_id="f1", price=100.0, quantity=10, timestamp="ts")
        with pytest.raises(OrderStateError):
            order.add_fill(fill)


# ======================================================================
# broker_interface — IBroker Protocol
# ======================================================================

class TestIBroker:
    def test_demo_broker_implements_ibroker(self, demo_broker):
        # runtime_checkable Protocol verifica métodos/atributos
        assert isinstance(demo_broker, IBroker)

    def test_demo_broker_name(self, demo_broker):
        assert demo_broker.name == "DEMO"

    def test_demo_broker_supports_symbol(self, demo_broker):
        assert demo_broker.supports_symbol("AAPL")
        assert demo_broker.supports_symbol("PETR4.SA")
        assert not demo_broker.supports_symbol("")
        assert not demo_broker.supports_symbol("   ")


# ======================================================================
# demo_broker — DemoBroker
# ======================================================================

class TestDemoBroker:
    def test_submit_market_order_fills(self, demo_broker):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=100)
        result = demo_broker.submit_order(order)
        assert result.status == OrderStatus.FILLED
        assert result.filled_quantity == 100
        assert result.broker_order_id is not None
        assert result.broker_order_id.startswith("DEMO-")

    def test_submit_limit_order_uses_limit_price(self, demo_broker):
        order = Order(
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=50,
            limit_price=150.0,
        )
        result = demo_broker.submit_order(order)
        assert result.status == OrderStatus.FILLED
        assert result.fills[0].price == 100.0  # fill_price_override

    def test_submit_with_commission(self, demo_broker):
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        result = demo_broker.submit_order(order)
        assert result.fills[0].commission == 1.50
        assert result.total_commission == 1.50

    def test_submit_when_disconnected_raises(self, demo_broker):
        demo_broker.disconnect()
        order = Order(symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.MARKET, quantity=10)
        with pytest.raises(ProviderError, match="não está conectado"):
            demo_broker.submit_order(order)

    def test_cancel_order_returns_cancelled(self, demo_broker):
        status = demo_broker.cancel_order("DEMO-abc123")
        assert status == OrderStatus.CANCELLED

    def test_connect_disconnect(self, demo_broker):
        assert demo_broker.is_available()
        demo_broker.disconnect()
        assert not demo_broker.is_available()
        demo_broker.connect()
        assert demo_broker.is_available()


# ======================================================================
# order_executor — OrderExecutor
# ======================================================================

class TestOrderExecutor:
    def test_create_order(self, executor):
        order = executor.create_order(
            symbol="AAPL",
            side="BUY",
            order_type="MARKET",
            quantity=100,
        )
        assert order.status == OrderStatus.PENDING
        assert order.broker == "DEMO"
        assert order.symbol == "AAPL"
        # Deve estar persistido
        assert os.path.exists(executor.state_path)

    def test_create_order_invalid_symbol(self, executor):
        with pytest.raises(InvalidSymbolError):
            executor.create_order(symbol="", side="BUY", order_type="MARKET", quantity=10)

    def test_submit_paper_mode(self, executor):
        order = executor.create_order(
            symbol="AAPL", side="BUY", order_type="MARKET", quantity=100
        )
        result = executor.submit(order.order_id)
        assert result.status == OrderStatus.FILLED
        assert result.filled_quantity == 100

    def test_submit_nonexistent_order(self, executor):
        with pytest.raises(OrderExecutionError, match="não encontrada"):
            executor.submit("nonexistent-id")

    def test_submit_non_pending_order(self, executor):
        order = executor.create_order(
            symbol="AAPL", side="BUY", order_type="MARKET", quantity=10
        )
        executor.submit(order.order_id)
        # Já está FILLED — não pode re-submeter
        with pytest.raises(OrderExecutionError, match="não está PENDING"):
            executor.submit(order.order_id)

    def test_cancel_order(self, executor):
        order = executor.create_order(
            symbol="AAPL", side="BUY", order_type="MARKET", quantity=10
        )
        result = executor.cancel(order.order_id)
        assert result.status == OrderStatus.CANCELLED

    def test_cancel_terminal_order(self, executor):
        order = executor.create_order(
            symbol="AAPL", side="BUY", order_type="MARKET", quantity=10
        )
        executor.submit(order.order_id)  # -> FILLED
        with pytest.raises(OrderExecutionError, match="já terminal"):
            executor.cancel(order.order_id)

    def test_get_order(self, executor):
        order = executor.create_order(
            symbol="AAPL", side="BUY", order_type="MARKET", quantity=10
        )
        retrieved = executor.get_order(order.order_id)
        assert retrieved is not None
        assert retrieved.order_id == order.order_id

    def test_get_order_none(self, executor):
        assert executor.get_order("nonexistent") is None

    def test_list_orders_all(self, executor):
        executor.create_order(symbol="AAPL", side="BUY", order_type="MARKET", quantity=10)
        executor.create_order(symbol="MSFT", side="SELL", order_type="MARKET", quantity=5)
        orders = executor.list_orders()
        assert len(orders) == 2

    def test_list_orders_by_status(self, executor):
        o1 = executor.create_order(symbol="AAPL", side="BUY", order_type="MARKET", quantity=10)
        executor.create_order(symbol="MSFT", side="SELL", order_type="MARKET", quantity=5)
        executor.submit(o1.order_id)  # -> FILLED
        pending = executor.list_orders(status=OrderStatus.PENDING)
        assert len(pending) == 1
        assert pending[0].symbol == "MSFT"
        filled = executor.list_orders(status=OrderStatus.FILLED)
        assert len(filled) == 1
        assert filled[0].symbol == "AAPL"

    def test_list_orders_by_symbol(self, executor):
        executor.create_order(symbol="AAPL", side="BUY", order_type="MARKET", quantity=10)
        executor.create_order(symbol="MSFT", side="SELL", order_type="MARKET", quantity=5)
        executor.create_order(symbol="AAPL", side="SELL", order_type="MARKET", quantity=3)
        aapl = executor.list_orders(symbol="AAPL")
        assert len(aapl) == 2

    def test_persistence_roundtrip(self, executor, tmp_orders_file):
        order = executor.create_order(
            symbol="AAPL", side="BUY", order_type="MARKET", quantity=100
        )
        executor.submit(order.order_id)
        order_id = order.order_id

        # Novo executor lê do mesmo arquivo
        executor2 = OrderExecutor(
            broker=DemoBroker(),
            registry=AssetRegistry(registry_file=str(Path(tmp_orders_file).parent / "asset_registry.json")),
            state_path=tmp_orders_file,
            paper_mode=True,
        )
        restored = executor2.get_order(order_id)
        assert restored is not None
        assert restored.symbol == "AAPL"
        assert restored.status == OrderStatus.FILLED
        assert restored.filled_quantity == 100

    def test_summary(self, executor):
        executor.create_order(symbol="AAPL", side="BUY", order_type="MARKET", quantity=10)
        executor.create_order(symbol="MSFT", side="SELL", order_type="MARKET", quantity=5)
        s = executor.summary()
        assert s["total_orders"] == 2
        assert s["by_status"].get("PENDING") == 2
        assert s["paper_mode"] is True
        assert s["broker"] == "DEMO"

    def test_symbol_authorization_with_registry(self, demo_broker, registry, tmp_orders_file, tmp_registry_dir, monkeypatch):
        """Testa que símbolos não autorizados são rejeitados."""
        # get_assets_for_broker usa caminho hardcoded "data/brokers/{broker}.json"
        # relativo ao cwd, então precisamos mudar o cwd para tmp_registry_dir
        monkeypatch.chdir(tmp_registry_dir)

        # Cria broker file com símbolos autorizados
        brokers_dir = Path("data") / "brokers"
        brokers_dir.mkdir(parents=True, exist_ok=True)
        broker_file = brokers_dir / "DEMO.json"
        broker_file.write_text(json.dumps(["AAPL", "MSFT"]))

        # Registra assets
        registry.register_asset(
            symbol="AAPL",
            category="stock",
            priority=1,
            profile="moderate",
            enabled=True,
        )
        registry.register_asset(
            symbol="GOOG",
            category="stock",
            priority=1,
            profile="moderate",
            enabled=True,
        )

        executor = OrderExecutor(
            broker=demo_broker,
            registry=registry,
            state_path=tmp_orders_file,
            paper_mode=True,
        )

        # AAPL autorizado
        order_ok = executor.create_order(symbol="AAPL", side="BUY", order_type="MARKET", quantity=10)
        result = executor.submit(order_ok.order_id)
        assert result.status == OrderStatus.FILLED

        # GOOG não autorizado
        order_bad = executor.create_order(symbol="GOOG", side="BUY", order_type="MARKET", quantity=10)
        with pytest.raises(InvalidSymbolError, match="não autorizado"):
            executor.submit(order_bad.order_id)

    def test_live_mode_broker_unavailable(self, registry, tmp_orders_file):
        """Em live mode, broker indisponível levanta ProviderError."""
        broker = DemoBroker()
        broker.disconnect()
        executor = OrderExecutor(
            broker=broker,
            registry=registry,
            state_path=tmp_orders_file,
            paper_mode=False,
        )
        order = executor.create_order(symbol="AAPL", side="BUY", order_type="MARKET", quantity=10)
        with pytest.raises(ProviderError, match="indisponível"):
            executor.submit(order.order_id)
