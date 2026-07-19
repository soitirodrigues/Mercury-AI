import pytest
from mercury_ai.core.observability_center import ObservabilityCenter

def test_observability_center():
    oc = ObservabilityCenter()
    oc.record_engine_time("SmartMoneyEngine", 0.05)
    oc.record_provider_latency("Yahoo", 0.1)
    oc.record_asset_time("BTC-USD", 0.2)
    
    metrics = oc.get_metrics()
    assert metrics["engine_times"]["SmartMoneyEngine"] == 0.05
    assert metrics["provider_latencies"]["Yahoo"] == 0.1
    assert metrics["asset_times"]["BTC-USD"] == 0.2
    assert "cpu_percent" in metrics
    assert "ram_percent" in metrics
