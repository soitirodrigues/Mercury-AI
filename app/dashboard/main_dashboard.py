try:
    import streamlit as st
except ImportError:
    st = None
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider
from mercury_ai.core.health_center import HealthCenter
from app.auth import require_auth, render_logout_button
from app.dashboard.asset_registry_panel import render_asset_registry_dashboard
from app.dashboard.provider_health_panel import render_provider_health_dashboard
from app.dashboard.observability_panel import render_observability_dashboard
from app.dashboard.health_center_panel import render_health_center_panel
from app.dashboard.market_map_panel import render_market_map_panel

def main():
    if st is None:
        return
    st.set_page_config(layout="wide", page_title="Mercury AI Institucional")
    require_auth()
    render_logout_button()
    
    # Initialize components
    registry = AssetRegistry()
    manager = MercuryDataProvider()
    health_center = HealthCenter(manager)
    
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Painéis", [
        "Mapa de Mercado",
        "Ativos",
        "Provedores",
        "Observabilidade",
        "Saúde do Sistema"
    ])
    
    if page == "Mapa de Mercado":
        render_market_map_panel(registry)
    elif page == "Ativos":
        render_asset_registry_dashboard(registry, manager)
    elif page == "Provedores":
        render_provider_health_dashboard(manager)
    elif page == "Observabilidade":
        render_observability_dashboard(manager)
    elif page == "Saúde do Sistema":
        render_health_center_panel(health_center)
