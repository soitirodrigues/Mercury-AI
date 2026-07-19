try:
    import streamlit as st
except ImportError:
    st = None
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

def render_provider_health_dashboard(manager: MercuryDataProvider):

    if st is None:
        return
    st.title("Monitoramento de Providers")
    
    # Refresh controls
    col1, col2 = st.columns([1, 4])
    if col1.button("Atualizar"):
        st.rerun()
    auto_refresh = col2.checkbox("Atualização automática")
    if auto_refresh:
        st.empty() # Placeholder for future logic

    # Display status table
    data = []
    for name, reg in manager._registry.items():
        status_icon = "🟢" if reg.health.status == ProviderStatus.ACTIVE else ("🟡" if reg.health.status == ProviderStatus.ERROR else "🔴")
        data.append({
            "Provider": name,
            "Status": f"{status_icon} {reg.health.status.value}",
            "Latência (ms)": f"{reg.metrics.latency_ms:.2f}",
            "Uptime (%)": f"{reg.metrics.uptime_percentage:.2f}",
            "Qualidade": reg.metrics.quality_score
        })
    
    st.table(data)
    
    if st.button("Ver Histórico"):
        st.write("Histórico detalhado do provedor selecionado...")
