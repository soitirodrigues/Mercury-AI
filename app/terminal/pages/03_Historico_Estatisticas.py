import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.analysis.operational_history import OperationalHistory
from mercury_ai.analysis.performance_statistics import PerformanceStatistics

st.title("Histórico e Estatísticas")

st.subheader("Trading Journal")
history = OperationalHistory().query()
st.dataframe(pd.DataFrame(history))

st.subheader("Performance Estatística")
st.json(PerformanceStatistics().calculate())
