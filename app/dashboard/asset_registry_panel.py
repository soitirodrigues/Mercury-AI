try:
    import streamlit as st
except ImportError:
    st = None
import pandas as pd
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

def render_asset_registry_dashboard(registry: AssetRegistry, manager: MercuryDataProvider):
    if st is None:
        return
    st.title("Gerenciamento de Ativos - Painel Institucional")
    
    # Load assets
    assets = registry.filter_assets()
    if not assets:
        st.warning("Nenhum ativo cadastrado.")
        return
        
    # Prepare data for dataframe/editor
    data = []
    for asset in assets:
        # Check provider health
        is_healthy = manager.provider_status(asset.provider)
        status_icon = "🟢" if is_healthy else "🔴"
        
        data.append({
            "Símbolo": asset.symbol,
            "Habilitado": asset.enabled,
            "Prioridade": asset.priority,
            "Status Provider": status_icon,
            "Spread": asset.spread,
            "Mercado": asset.market,
            "Provider": asset.provider,
            "Fallback": asset.fallback_provider,
            "Categoria": asset.category,
            "Perfil": asset.profile
        })
        
    df = pd.DataFrame(data)
    
    # UI Controls
    st.subheader("Ativos Cadastrados")
    
    # st.data_editor provides built-in filtering, sorting, and editing
    edited_df = st.data_editor(
        df,
        column_config={
            "Prioridade": st.column_config.NumberColumn("Prioridade", min_value=1, max_value=5),
            "Habilitado": st.column_config.CheckboxColumn("Habilitado"),
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Save edits
    if st.button("Salvar Alterações"):
        for _, row in edited_df.iterrows():
            registry.set_enabled(row["Símbolo"], row["Habilitado"])
            registry.set_priority(row["Símbolo"], int(row["Prioridade"]))
        st.success("Alterações salvas!")
        st.rerun()

    # Cadastro
    st.subheader("Cadastrar Novo Ativo")
    with st.form("new_asset"):
        col1, col2 = st.columns(2)
        symbol = col1.text_input("Símbolo")
        category = col2.selectbox("Categoria", ["Forex", "Cripto", "Commodities", "Índices", "Ações"])
        priority = col1.slider("Prioridade", 1, 5)
        profile = col2.selectbox("Perfil", ["Demo", "Replay", "Produção"])
        
        if st.form_submit_button("Cadastrar"):
            registry.register_asset(symbol, category, priority, profile)
            st.success(f"Ativo {symbol} cadastrado!")
            st.rerun()
