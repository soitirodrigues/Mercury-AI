import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
from mercury_ai.config.assets import SUPPORTED_ASSETS
from mercury_ai.analysis.operational_history import OperationalHistory
from mercury_ai.analysis.performance_statistics import PerformanceStatistics

st.set_page_config(page_title="Modo Demo", layout="wide")
st.title("🧪 Modo de Operação Demo")

# Configuração
assets = [symbol for asset_list in SUPPORTED_ASSETS.values() for symbol in asset_list]
selected_assets = st.multiselect("Selecionar Ativos", assets, default=[assets[0]])
timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"])

if st.button("Executar Demo"):
    with st.spinner("Executando pipeline em modo Demo..."):
        provider = YahooFinanceProvider()
        pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]),
            providers=[provider]
        )
        
        results = []
        for symbol in selected_assets:
            res = pipeline.analyze(symbol)
            results.append({
                "Ativo": symbol,
                "Decisão": res.decision.decision,
                "Confiança": f"{res.decision.confidence*100:.1f}%",
                "Prob. Buy": f"{res.decision.buy_probability:.1f}%",
                "Timestamp": res.timestamp[:19]
            })
            
        st.dataframe(pd.DataFrame(results))
        
        st.subheader("Histórico Operacional")
        st.dataframe(pd.DataFrame(OperationalHistory().query()))
        
        st.subheader("Performance Estatística")
        st.json(PerformanceStatistics().calculate())
