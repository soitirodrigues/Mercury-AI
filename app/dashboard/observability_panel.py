try:
    import streamlit as st
except ImportError:
    st = None
import psutil
import time
from mercury_ai.providers.manager import MercuryProviderManager

def render_observability_dashboard(manager: MercuryProviderManager):
    if st is None:
        return
    st.title("Painel de Observabilidade")
    
    # System Metrics (Mocked for now)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CPU", f"{psutil.cpu_percent()}%")
    col2.metric("RAM", f"{psutil.virtual_memory().percent}%")
    col3.metric("Disco", f"{psutil.disk_usage('/').percent}%")
    col4.metric("Rede", "🟢 OK")

    st.divider()

    # Application Metrics
    st.subheader("Componentes do Sistema")
    
    comp_cols = st.columns(3)
    comp_cols[0].metric("Latência Pipeline", "1.5s")
    comp_cols[1].metric("Threads Ativas", f"{psutil.Process().num_threads()}")
    comp_cols[2].metric("Fila", "0")

    # Status Indicators
    status_data = {
        "Scanner": "🟢",
        "Pipeline": "🟢",
        "Replay": "🟢",
        "Dashboard": "🟢",
        "Logs": "🟢",
        "Snapshots": "🟢",
        "Health": "🟢"
    }
    
    st.table(st.DataFrame.from_dict(status_data, orient='index', columns=['Status']))
