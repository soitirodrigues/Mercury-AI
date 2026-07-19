try:
    import streamlit as st
except ImportError:
    st = None
from mercury_ai.core.health_center import HealthCenter

def render_health_center_panel(health_center: HealthCenter):
    if st is None:
        return
    st.title("Centro de Saúde Institucional")
    
    # System Metrics
    metrics = health_center.get_system_metrics()
    col1, col2, col3 = st.columns(3)
    col1.metric("CPU", f"{metrics['cpu_percent']}%")
    col2.metric("RAM", f"{metrics['ram_percent']}%")
    col3.metric("Threads", metrics['threads'])
    
    st.divider()
    
    # Component Health
    st.subheader("Saúde dos Componentes")
    health = health_center.get_component_health()
    
    cols = st.columns(4)
    for i, (comp, status) in enumerate(health.items()):
        cols[i % 4].metric(comp, status)
