import pytest
from mercury_ai.core.health_center import HealthCenter
from mercury_ai.providers.mercury_data_provider import MercuryDataProviderManager
from app.dashboard.health_center_panel import render_health_center_panel

def test_health_center_data():
    manager = MercuryDataProviderManager()
    hc = HealthCenter(manager)
    
    metrics = hc.get_system_metrics()
    assert "cpu_percent" in metrics
    assert "ram_percent" in metrics
    assert "threads" in metrics
    
    health = hc.get_component_health()
    assert "Scanner" in health
    assert health["Scanner"] == "🟢"

def test_health_center_panel_load():
    # Verify panel loads without streamlit installed (or with it mocked)
    manager = MercuryDataProviderManager()
    hc = HealthCenter(manager)
    render_health_center_panel(hc)
    assert True
