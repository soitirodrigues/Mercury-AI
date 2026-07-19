try:
    import streamlit as st
except ImportError:
    st = None
try:
    import plotly.express as px
except ImportError:
    px = None
import pandas as pd
from mercury_ai.core.asset_registry import AssetRegistry

def render_market_map_panel(registry: AssetRegistry):
    if st is None or px is None:
        return
    st.title("Mapa de Ativos e Heatmap")
    
    assets = registry.filter_assets()
    if not assets:
        st.warning("Nenhum ativo cadastrado.")
        return
        
    data = [{"Símbolo": a.symbol, "Categoria": a.category, "Liquidez": a.liquidity, "Spread": a.spread, "Score": a.previous_score} for a in assets]
    df = pd.DataFrame(data)
    
    # Heatmap
    fig = px.treemap(df, path=['Categoria', 'Símbolo'], values='Liquidez', color='Score', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Estado do Mercado")
    market_status = {"XP": "Aberto", "Clear": "Aberto", "Cripto": "24/7"}
    st.table(pd.DataFrame(list(market_status.items()), columns=["Mercado", "Status"]))
